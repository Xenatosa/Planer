#!/usr/bin/env python3
"""Serial p3d32 continuous-LP, Priority-Flood and official lazy-cut loop."""
from __future__ import annotations

import base64
import gzip
import hashlib
import heapq
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
TOOLS = ROOT / "codex_jobs/tools/p3d32"
RESULTS = TOOLS / "results"
SOURCE = Path("/tmp/p3d22_v3_source.json.gz")
TRANSFER = RELIEF3D / "neu/p3d21_transfer_base_route3_v29.json"
REFERENCE = RELIEF3D / "neu/p3d17_joint_mesh_v22.json"
BASELINE_RULES = ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_regeln_current_schema.json"
BASELINE_R8 = ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_r8.json"
BASELINE_R9 = ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_r9.json"
EXPECTED_SOURCE_SHA256 = "b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6"
EXPECTED_TRANSFER_SHA256 = "07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287"
FLOOD_EPS_M = 0.001
R5_THRESHOLD_M = 1.0
MAX_PROBE_ROUNDS = 4
MAX_FLOOD_RESOLVES_PER_ROUND = 3


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def checked(args: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"{Path(args[0]).name} failed ({proc.returncode}): {args}; "
            f"stdout={proc.stdout[-2000:]}; stderr={proc.stderr[-2000:]}"
        )
    return proc


def load_model():
    spec = importlib.util.spec_from_file_location(
        "p3d32_lp_model", TOOLS / "diagnose_lp_p3d32.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("p3d32 LP-Modell konnte nicht geladen werden")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.RELIEF = SOURCE
    return module


def make_lp_command(round_no: int, solve_no: int, event_path: Path,
                    flood_path: Path, output_path: Path,
                    *, diagnostic_groups: list[str] | None = None) -> list[str]:
    command = [
        sys.executable, str(TOOLS / "run_lp_p3d32.py"),
        "--geometry", "V3", "--scenario", "joint",
        "--source-relief", str(SOURCE), "--transfer-base", str(TRANSFER),
        "--r8-center", "152.6292918620858", "28.353590994151514",
        "--event-cuts", str(event_path), "--flood-cuts", str(flood_path),
        "--out", str(output_path), "--time-limit", "600", "--keep-solution",
        "--objective-mode", "step", "--reference-solution", str(REFERENCE),
        "--relax-integrality", "--groups",
    ]
    if diagnostic_groups is not None:
        command.pop()
        command.extend(["--groups", *diagnostic_groups])
        command[command.index("--objective-mode") + 1] = "diagnostic"
    return command


def p3d32_priority_flood_floors(solution_path: Path, pass_no: int) -> dict:
    """Compute threshold-minimal 1 mm Epsilon flood floors in the active window."""
    solution = json.loads(solution_path.read_text(encoding="utf-8"))
    if not solution.get("primal_feasible") or "surface_grid" not in solution:
        raise RuntimeError("Priority-Flood benötigt ein primal zulässiges LP-Relief")
    construction_path = solution_path.with_name(solution_path.stem + "_construction.json")
    construction = json.loads(construction_path.read_text(encoding="utf-8"))["construction"]
    active = np.asarray(construction["active_mask"], dtype=bool)
    zero_eps = np.asarray(construction["zero_eps_mask"], dtype=bool)
    cliff = np.asarray(construction["wall_cliff_gorge_mask"], dtype=bool)
    surface = np.asarray(solution["surface_grid"]["heights_m"], dtype=np.float64)
    if not (active.shape == zero_eps.shape == cliff.shape == surface.shape):
        raise RuntimeError("Priority-Flood-Masken und LP-Raster stimmen nicht überein")

    model = load_model()
    fixed, coverage, _, _ = model.p3d17_transfer_context()
    candidate = (fixed + coverage * surface).astype("<f4").astype(np.float64)
    h, w = candidate.shape
    boundary = active & ~ndi.binary_erosion(
        active, structure=np.ones((3, 3), dtype=bool), border_value=0,
    )
    protected = zero_eps | cliff | boundary
    for x, z in (model.P3D32_CROSSING_ANCHOR, model.P3D32_RAMP2_START):
        ix = int(round((float(x) - 126.0) * 2))
        iz = int(round(float(z) * 2))
        if 0 <= iz < h and 0 <= ix < w:
            protected[iz, ix] = True

    visited = np.zeros((h, w), dtype=bool)
    escape = np.full((h, w), np.inf, dtype=np.float64)
    parent = np.full(h * w, -1, dtype=np.int64)
    heap: list[tuple[float, int]] = []
    for iz, ix in zip(*np.nonzero(boundary)):
        index = int(iz * w + ix)
        visited[iz, ix] = True
        escape[iz, ix] = float(candidate[iz, ix])
        heapq.heappush(heap, (float(candidate[iz, ix]), index))
    neighbors = tuple((dz, dx) for dz in (-1, 0, 1) for dx in (-1, 0, 1) if dz or dx)
    while heap:
        level, index = heapq.heappop(heap)
        iz, ix = divmod(index, w)
        for dz, dx in neighbors:
            nz, nx = iz + dz, ix + dx
            if not (0 <= nz < h and 0 <= nx < w and active[nz, nx]) or visited[nz, nx]:
                continue
            visited[nz, nx] = True
            # Barnes-style Priority-Flood with epsilon only when a flat or
            # descending neighbor must be raised to continue the outlet path.
            next_level = (level + FLOOD_EPS_M if candidate[nz, nx] <= level
                          else float(candidate[nz, nx]))
            escape[nz, nx] = next_level
            parent[nz * w + nx] = index
            heapq.heappush(heap, (next_level, nz * w + nx))
    if not np.array_equal(visited, active):
        raise RuntimeError(f"Priority-Flood ließ {int(np.count_nonzero(active & ~visited))} Fensterzellen offen")

    deep = active & ((escape - candidate) > R5_THRESHOLD_M)
    raiseable = deep & ~protected
    floors: list[dict] = []
    raises = np.maximum(0.0, escape - R5_THRESHOLD_M + FLOOD_EPS_M - candidate)
    for iz, ix in zip(*np.nonzero(raiseable & (raises > 1e-6))):
        px, pz = 126.0 + int(ix) / 2.0, int(iz) / 2.0
        minimum = float(escape[iz, ix] - R5_THRESHOLD_M + FLOOD_EPS_M)
        floors.append({
            "kind": "FLOOR", "point": [px, pz],
            "minimum_final_height_m": minimum,
            "priority_flood_escape_height_m": float(escape[iz, ix]),
            "input_height_m": float(candidate[iz, ix]),
            "raise_m": float(minimum - candidate[iz, ix]),
        })
    protected_deep = deep & protected
    details = {
        "pass": pass_no,
        "epsilon_m": FLOOD_EPS_M,
        "threshold_m": R5_THRESHOLD_M,
        "connectivity": "8-neighbor Priority-Flood; active-window boundary nodes are outlets",
        "active_vertices": int(active.sum()),
        "boundary_outlets": int(boundary.sum()),
        "protected_vertices": int((active & protected).sum()),
        "protected_reasons": ["road/ramp/crossing/runout epsilon mask", "cliff zone", "window boundary", "fixed anchors"],
        "floor_constraints_added": len(floors),
        "floor_raise_sum_m_per_vertex": float(sum(item["raise_m"] for item in floors)),
        "floor_raise_max_m": float(max((item["raise_m"] for item in floors), default=0.0)),
        "deep_spill_vertices_left_unraised_for_local_LP": int(protected_deep.sum()),
        "deep_spill_max_depth_m": float(np.max(np.where(deep, escape - candidate, 0.0), initial=0.0)),
        "floors": floors,
    }
    return details


def merge_floors(old: list[dict], new: list[dict]) -> list[dict]:
    merged = {(round(float(c["point"][0]), 6), round(float(c["point"][1]), 6)): c
              for c in old}
    changed = False
    for cut in new:
        key = (round(float(cut["point"][0]), 6), round(float(cut["point"][1]), 6))
        previous = merged.get(key)
        if previous is None or float(cut["minimum_final_height_m"]) > float(previous["minimum_final_height_m"]) + 1e-6:
            merged[key] = cut
            changed = True
    return [merged[key] for key in sorted(merged)], changed


def d2_new_hits(probe: dict) -> dict[str, int]:
    baseline = json.loads(BASELINE_RULES.read_text(encoding="utf-8"))
    old: dict[str, int] = {}
    for hit in baseline.get("treffer", []):
        if hit.get("feld") == "D2":
            name = str(hit.get("regel", ""))
            old[name] = old.get(name, 0) + 1
    now = probe.get("rules_by_tile", {}).get("D2", {})
    return {name: max(0, int(count) - int(old.get(name, 0)))
            for name, count in now.items() if int(count) > int(old.get(name, 0))}


def hard_target_excess(probe: dict, solution: dict) -> dict:
    rules = probe.get("rules_by_rule", {})
    tiles = probe.get("rules_by_tile", {})
    d1 = tiles.get("D1", {})
    r9_d1 = probe.get("R9_by_tile", {}).get("D1", {})
    crossing = probe.get("R8_crossing_gate", {})
    metrics = crossing.get("official_cluster", {}) or {}
    quer_hit = crossing.get("R8_quer_hit")
    endpoint_stage = float(solution.get("family_max_relaxation_locations", {})
                           .get("endpoint_stage", {}).get("maximum_violation_m", 0.0))
    d2_new = d2_new_hits(probe)
    d2_r8 = probe.get("R8_by_tile", {}).get("D2", {})
    d2_r9 = probe.get("R9_by_tile", {}).get("D2", {})
    single_quer = float(solution.get("slack_values", {}).get("safety_single_quer_extra_pp", 0.0))
    return {
        "R5_spitze_D1": int(d1.get("R5_spitze", 0)),
        "G6_D1_excess": max(0, int(d1.get("G6_facette", 0)) - 3),
        "R8b_D1_excess": max(0, int(r9_d1.get("R8b_delle", 0)) - 1),
        "G3_D1_excess": max(0, int(d1.get("G3_spitze_unten", 0))
                              + int(d1.get("G3_spitze_unten_fein", 0)) - 1),
        "R9w_total_excess": max(0, int(probe.get("R9_by_rule", {}).get("R9w_wellen", 0)) - 280),
        "G5_total_excess": max(0, int(rules.get("G5_beule_klippe", 0)) - 69),
        "G5_D1_excess": max(0, int(d1.get("G5_beule_klippe", 0)) - 2),
        "R5_loch_total_excess": max(0, int(rules.get("R5_loch", 0)) - 22),
        "R5_loch_D1_excess": max(0, int(d1.get("R5_loch", 0)) - 5),
        "R4_schlucht_D1": int(d1.get("R4_schlucht", 0)),
        "crossing_stage_excess_m": max(0.0, float(metrics.get("stufe", 0.0)) - 0.116),
        "crossing_gitter_excess_m": max(0.0, float(metrics.get("gitter", 0.0)) - 0.020),
        "crossing_quer_excess_pct": (0.0 if quer_hit is None else
                                      max(0.0, float(quer_hit.get("wert", 0.0)) - 3.0)),
        "R3_laengs_D1_excess": max(0, int(d1.get("R3_laengs_m", 0)) - 6),
        "R3_quer_D1_excess": max(0, int(d1.get("R3_quer_pct", 0)) - 7),
        "R3_woelb_D1_excess": max(0, int(d1.get("R3_woelb_m", 0)) - 7),
        "single_cross_quer_over_20_pct": max(0.0, single_quer - 0.5),
        "R8a_D1_unpermitted": sum(
            hit.get("ausnahme") != "R8a_ausnahme_rampe2_start"
            for hit in probe.get("R8a_hits_by_tile", {}).get("D1", [])
        ),
        "endpoint_stage_model_violation_m": max(0.0, endpoint_stage),
        "D2_new_pruefe_regeln_hits": sum(d2_new.values()),
        "D2_R8_R9_hits": sum(map(int, d2_r8.values())) + sum(map(int, d2_r9.values())),
        "G1_hash_changed": int(probe.get("G1_height_sha256") !=
                                "38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb"),
        "D2_hash_changed": int(probe.get("D2_height_sha256") !=
                                "749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6"),
    }


def gate_score(probe: dict, solution: dict) -> tuple[float, dict]:
    rules = probe.get("rules_by_rule", {})
    d1 = probe.get("rules_by_tile", {}).get("D1", {})
    r8 = probe.get("R8_by_rule", {})
    r9 = probe.get("R9_by_rule", {})
    base_rules = json.loads(BASELINE_RULES.read_text(encoding="utf-8")).get("je_regel", {})
    base_r8 = json.loads(BASELINE_R8.read_text(encoding="utf-8")).get("je_regel", {})
    base_r9 = json.loads(BASELINE_R9.read_text(encoding="utf-8")).get("je_regel", {})
    score = {}
    for name in sorted(set(base_rules) | set(rules)):
        score[f"+5:rule:{name}"] = max(0, int(rules.get(name, 0)) - int(base_rules.get(name, 0)) - 5)
    for name in ("R8_stufe", "R8_gitter", "R8_quer", "R8a_wegende"):
        score[f"+5:R8:{name}"] = max(0, int(r8.get(name, 0)) - int(base_r8.get(name, 0)) - 5)
    for name in ("R8b_delle", "R9_saegezahn", "R9w_wellen"):
        score[f"+5:R9:{name}"] = max(0, int(r9.get(name, 0)) - int(base_r9.get(name, 0)) - 5)
    for name, limit in (("R3_laengs_m", 6), ("R3_quer_pct", 7), ("R3_woelb_m", 7)):
        score[f"D1:{name}"] = max(0, int(d1.get(name, 0)) - limit)
    score.update(hard_target_excess(probe, solution))
    return float(sum(score.values())), score


def hard_lp_recheck(solution: dict) -> dict:
    slacks = solution.get("slack_values", {})
    positive = {name: float(value) for name, value in slacks.items()
                if value is not None and float(value) > 2e-6}
    maxviol = solution.get("p3d31_construction_max_violations", {})
    locality = maxviol.get("locality", {})
    loc_max = max((float(v.get("maximum_violation_m", 0.0)) for v in locality.values()), default=0.0)
    cliff = float(maxviol.get("cliff_curvature_hard", {}).get("maximum_violation_m", 0.0))
    tree = float(maxviol.get("tree_ground", {}).get("maximum_violation_m", 0.0))
    r4 = float(maxviol.get("r4_official_indicator", {}).get("maximum_violation_m", 0.0))
    endpoint_r8a = float(solution.get("family_max_relaxation_locations", {})
                         .get("endpoint_r8a", {}).get("maximum_violation_m", 0.0))
    r8 = solution.get("R8_gate_metrics_solution", {})
    checks = {
        "primal_feasible": bool(solution.get("primal_feasible")),
        "all_slacks_zero": not positive,
        "locality_max_violation_m": loc_max,
        "cliff_form_max_violation_m": cliff,
        "tree_ground_max_violation_m": tree,
        "R4_model_max_violation_m": r4,
        "R8a_model_max_violation_m": endpoint_r8a,
        "R8_stufe_m": float(r8.get("R8_stufe_m", 0.0)),
        "R8_gitter_m": float(r8.get("R8_gitter_m", 0.0)),
        "R8_quer_pct": float(r8.get("R8_quer_pct", 0.0)),
        "R8_limits_pass": (float(r8.get("R8_stufe_m", 0.0)) <= 0.116 + 2e-6
                            and float(r8.get("R8_gitter_m", 0.0)) <= 0.020 + 2e-6
                            and float(r8.get("R8_quer_pct", 0.0)) <= 3.0 + 2e-6),
        "positive_slacks": positive,
    }
    checks["hard_lp_pass"] = bool(
        checks["primal_feasible"] and checks["all_slacks_zero"]
        and loc_max <= 2e-6 and cliff <= 2e-6 and tree <= 2e-6
        and r4 <= 2e-6 and endpoint_r8a <= 2e-6 and checks["R8_limits_pass"]
    )
    return checks


def run_lp_round(round_no: int, event_path: Path) -> tuple[dict, Path, list[dict], list[dict]]:
    prefix = f"p3d32_V3_round{round_no:02d}"
    flood_path = RESULTS / f"{prefix}_flood_cuts.json"
    flood_cuts: list[dict] = []
    dump(flood_path, flood_cuts)
    flood_passes = []
    solution = None
    final_solution_path = None
    for solve_no in range(MAX_FLOOD_RESOLVES_PER_ROUND):
        solution_path = RESULTS / f"{prefix}_lp{solve_no:02d}_model.json"
        env = dict(os.environ)
        env["P3D32_VARIANT"] = os.environ.get("P3D32_VARIANT", "1")
        env["P3D31_VARIANT"] = "1"
        checked(make_lp_command(round_no, solve_no, event_path, flood_path, solution_path), env=env)
        solution = json.loads(solution_path.read_text(encoding="utf-8"))
        final_solution_path = solution_path
        if not solution.get("primal_feasible"):
            return solution, solution_path, flood_passes, flood_cuts
        flood_pass = p3d32_priority_flood_floors(solution_path, solve_no)
        flood_passes.append({key: value for key, value in flood_pass.items() if key != "floors"})
        next_floors, changed = merge_floors(flood_cuts, flood_pass["floors"])
        if not changed:
            break
        flood_cuts = next_floors
        dump(flood_path, flood_cuts)
    else:
        flood_passes[-1]["stopped_at_resolve_limit"] = True
    if solution is None or final_solution_path is None:
        raise RuntimeError("p3d32 Checkerloop ohne LP-Lauf beendet")
    full_flood_path = RESULTS / f"{prefix}_priority_flood.json"
    dump(full_flood_path, {
        "tag": "p3d32", "round": round_no, "passes": flood_passes,
        "floor_cut_count": len(flood_cuts), "floor_cuts": flood_cuts,
        "method": "Priority-Flood with 1 mm epsilon; minimum lift to leave <1.0 m spill depth",
    })
    solution["p3d32_flood_evidence_json"] = str(full_flood_path)
    solution["p3d32_flood_passes"] = flood_passes
    solution["p3d32_flood_floor_count"] = len(flood_cuts)
    solution["p3d32_hard_lp_recheck"] = hard_lp_recheck(solution)
    return solution, final_solution_path, flood_passes, flood_cuts


def gate_details(probe: dict) -> dict:
    rules = probe.get("rules_by_rule", {})
    d1 = probe.get("rules_by_tile", {}).get("D1", {})
    r8 = probe.get("R8_by_rule", {})
    r9 = probe.get("R9_by_rule", {})
    crossing = probe.get("R8_crossing_gate", {}).get("official_cluster", {}) or {}
    return {
        "pruefe_regeln_total": probe.get("rules_total"),
        "pruefe_regeln_D1_G1_D2": {
            tile: sum(map(int, probe.get("rules_by_tile", {}).get(tile, {}).values()))
            for tile in ("D1", "G1", "D2")
        },
        "R8_total": probe.get("R8_total"),
        "R8_D1_G1_D2": {tile: sum(map(int, probe.get("R8_by_tile", {}).get(tile, {}).values()))
                         for tile in ("D1", "G1", "D2")},
        "R9_total": probe.get("R9_total"),
        "R9_D1_G1_D2": {tile: sum(map(int, probe.get("R9_by_tile", {}).get(tile, {}).values()))
                         for tile in ("D1", "G1", "D2")},
        "G5_total_D1": [int(rules.get("G5_beule_klippe", 0)), int(d1.get("G5_beule_klippe", 0))],
        "R5_loch_total_D1": [int(rules.get("R5_loch", 0)), int(d1.get("R5_loch", 0))],
        "G6_D1": int(d1.get("G6_facette", 0)),
        "R5_spitze_D1": int(d1.get("R5_spitze", 0)),
        "R8b_D1": int(probe.get("R9_by_tile", {}).get("D1", {}).get("R8b_delle", 0)),
        "G3_D1": int(d1.get("G3_spitze_unten", 0)) + int(d1.get("G3_spitze_unten_fein", 0)),
        "R4_schlucht_D1": int(d1.get("R4_schlucht", 0)),
        "R3_D1": {k: int(d1.get(k, 0)) for k in ("R3_laengs_m", "R3_quer_pct", "R3_woelb_m")},
        "R9w_total_D1_G1_D2": [int(r9.get("R9w_wellen", 0)),
                                int(probe.get("R9_by_tile", {}).get("D1", {}).get("R9w_wellen", 0)),
                                int(probe.get("R9_by_tile", {}).get("G1", {}).get("R9w_wellen", 0)),
                                int(probe.get("R9_by_tile", {}).get("D2", {}).get("R9w_wellen", 0))],
        "crossing_cluster": crossing,
        "outside_window_bitwise_equal": probe.get("outside_window_bitwise_equal_to_p3d17"),
        "G1_hash": probe.get("G1_height_sha256"),
        "D2_hash": probe.get("D2_height_sha256"),
    }


def locations(probe: dict) -> dict:
    groups = ("G5_beule_klippe", "R5_loch", "R5_spitze", "G6_facette",
              "R4_schlucht", "G3_spitze_unten", "G3_spitze_unten_fein")
    return {name: [hit for hit in probe.get("rules_D1_hits", []) if hit.get("regel") == name]
            for name in groups} | {
        "R8_D1": probe.get("R8_D1_hits", []),
        "R9_D1": probe.get("R9_D1_hits", []),
    }


def compare_rule_tables(probes: list[dict]) -> dict:
    base_rules = json.loads(BASELINE_RULES.read_text(encoding="utf-8"))
    base_r8 = json.loads(BASELINE_R8.read_text(encoding="utf-8"))
    base_r9 = json.loads(BASELINE_R9.read_text(encoding="utf-8"))
    final = probes[-1] if probes else {}
    return {
        "baseline_rules": base_rules.get("je_regel", {}),
        "final_rules": final.get("rules_by_rule", {}),
        "baseline_rules_by_tile": {
            tile: _hits_by_tile(base_rules.get("treffer", []), tile)
            for tile in ("D1", "G1", "D2")
        },
        "final_rules_by_tile": final.get("rules_by_tile", {}),
        "baseline_R8": base_r8.get("je_regel", {}),
        "final_R8": final.get("R8_by_rule", {}),
        "baseline_R8_by_tile": base_r8.get("je_feld", {}),
        "final_R8_by_tile": final.get("R8_by_tile", {}),
        "baseline_R9": base_r9.get("je_regel", {}),
        "final_R9": final.get("R9_by_rule", {}),
        "baseline_R9_by_tile": base_r9.get("je_feld", {}),
        "final_R9_by_tile": final.get("R9_by_tile", {}),
    }


def _hits_by_tile(hits: list[dict], tile: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for hit in hits:
        if hit.get("feld") == tile:
            rule = str(hit.get("regel", ""))
            out[rule] = out.get(rule, 0) + 1
    return out


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"Unerwarteter V3-Quellreliefhash: {SOURCE}")
    if hashlib.sha256(TRANSFER.read_bytes()).hexdigest() != EXPECTED_TRANSFER_SHA256:
        raise RuntimeError(f"Unerwarteter Transferbasis-Hash: {TRANSFER}")
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    if branch != "art/dorfmap-p3d32":
        raise RuntimeError(f"Unerwarteter Arbeitsbranch für p3d32: {branch}")
    variant = os.environ.get("P3D32_VARIANT", "1")
    event_cuts: list[dict] = []
    rounds: list[dict] = []
    probes: list[dict] = []
    prior_scores = []
    for round_no in range(1, MAX_PROBE_ROUNDS + 1):
        prefix = f"p3d32_V3_round{round_no:02d}"
        event_path = RESULTS / f"{prefix}_event_cuts.json"
        dump(event_path, event_cuts)
        solution, solution_path, flood_passes, flood_cuts = run_lp_round(round_no, event_path)
        lp_recheck = solution.get("p3d32_hard_lp_recheck", hard_lp_recheck(solution))
        record = {
            "round": round_no,
            "variant": variant,
            "model_status": solution.get("status"),
            "primal_feasible": solution.get("primal_feasible"),
            "optimality_proven": solution.get("optimality_proven"),
            "variables": solution.get("variables"),
            "constraints": solution.get("constraints"),
            "integer_variable_count": solution.get("integer_variable_count", 0),
            "all_solver_variables_continuous": solution.get("all_solver_variables_continuous"),
            "model_json": str(solution_path),
            "construction_json": str(solution_path.with_name(solution_path.stem + "_construction.json")),
            "event_cuts_before": len(event_cuts),
            "flood_cuts": len(flood_cuts),
            "flood_passes": flood_passes,
            "hard_lp_recheck": lp_recheck,
        }
        if not solution.get("primal_feasible"):
            record["stop_reason"] = "no_primal_feasible_LP_point"
            # One elastic LP group-filter solve identifies the active families.
            diag_path = RESULTS / f"{prefix}_lp_group_filter.json"
            diag_flood_path = RESULTS / f"{prefix}_lp_group_filter_flood_cuts.json"
            dump(diag_flood_path, flood_cuts)
            all_groups = [
                "r3_long", "r3_quer", "r3_wob", "crossing_stage", "axis_supports",
                "plane_core", "endpoint_stage", "safety_gitter", "safety_quer",
                "safety_single_quer", "g5", "r5_hole", "r8b", "r4", "grade_cross",
                "grade_same", "endpoint_r8a", "plane_slope_polygon", "plane_slope_box",
                "variable_bounds", "route_profile_slope", "source_monotone", "g11",
                "p3d29_locality", "p3d31_drainage", "p3d29_cliff_form", "p3d29_tree_ground",
            ]
            env = dict(os.environ)
            env["P3D32_VARIANT"] = variant
            proc = checked(make_lp_command(round_no, 90, event_path, diag_flood_path,
                                           diag_path, diagnostic_groups=all_groups), env=env)
            diag = json.loads(diag_path.read_text(encoding="utf-8"))
            record["lp_group_filter"] = {
                "status": diag.get("status"),
                "positive_slacks": {k: v for k, v in diag.get("slack_values", {}).items()
                                    if v is not None and float(v) > 1e-7},
                "evidence_json": str(diag_path),
                "method": "single all-family elastic LP solve; diagnostic, not an IIS",
            }
            rounds.append(record)
            dump(RESULTS / "p3d32_V3_checker_loop.json", {
                "tag": "p3d32", "variant": variant, "rounds": rounds,
                "best_round": None, "status": record["stop_reason"],
                "method": "serial pure-LP, Priority-Flood and official Float32 checker loop",
            })
            break
        if not lp_recheck.get("hard_lp_pass"):
            record["stop_reason"] = "post_flood_LP_hard_recheck_failed"
            rounds.append(record)
            dump(RESULTS / "p3d32_V3_checker_loop.json", {
                "tag": "p3d32", "variant": variant, "rounds": rounds,
                "best_round": None, "status": record["stop_reason"],
                "method": "serial pure-LP, Priority-Flood and official Float32 checker loop",
            })
            break

        probe_path = RESULTS / f"{prefix}_official_probe.json"
        checked([sys.executable, str(TOOLS / "probe_direct_transfer_p3d32.py"),
                 str(solution_path), str(TRANSFER), str(probe_path)])
        probe = json.loads(probe_path.read_text(encoding="utf-8"))
        cuts_path = RESULTS / f"{prefix}_derived_cuts.json"
        derived = checked([sys.executable, str(TOOLS / "derive_event_cuts_p3d32.py"),
                           str(probe_path), str(cuts_path)])
        derived_summary = json.loads(derived.stdout)
        next_cuts = json.loads(cuts_path.read_text(encoding="utf-8"))
        dedup = {json.dumps(c, sort_keys=True, separators=(",", ":")): c
                 for c in [*event_cuts, *next_cuts]}
        merged_cuts = [dedup[key] for key in sorted(dedup)]
        score, score_parts = gate_score(probe, solution)
        record.update({
            "probe_json": str(probe_path),
            "derived_cuts_json": str(cuts_path),
            "derived_summary": derived_summary,
            "gate_score": score,
            "hard_target_excess": score_parts,
            "gate_totals": gate_details(probe),
            "remaining_D1_hits": locations(probe),
            "new_lazy_cuts": len(next_cuts),
            "lazy_cuts_after_dedup": len(merged_cuts),
            "event_cuts_after": len(merged_cuts),
            "official_probe_rules_by_rule": probe.get("rules_by_rule", {}),
            "official_probe_R8_by_rule": probe.get("R8_by_rule", {}),
            "official_probe_R9_by_rule": probe.get("R9_by_rule", {}),
            "official_probe_rules_by_tile": probe.get("rules_by_tile", {}),
            "official_probe_R8_by_tile": probe.get("R8_by_tile", {}),
            "official_probe_R9_by_tile": probe.get("R9_by_tile", {}),
        })
        rounds.append(record)
        probes.append(probe)
        prior_scores.append(score)
        if score == 0:
            record["stop_reason"] = "all_hard_targets_passed"
        elif merged_cuts == event_cuts:
            record["stop_reason"] = "no_new_official_lazy_cuts"
        elif round_no == MAX_PROBE_ROUNDS:
            record["stop_reason"] = "four_probe_round_limit"
        dump(RESULTS / "p3d32_V3_checker_loop.json", {
            "tag": "p3d32", "variant": variant, "rounds": rounds,
            "best_round": min(rounds, key=lambda item: item.get("gate_score", float("inf"))).get("round"),
            "best_score": min(prior_scores),
            "status": record.get("stop_reason", "continue"),
            "rule_comparison": compare_rule_tables(probes),
            "method": "serial pure-LP, 1 mm Priority-Flood and unchanged official Float32 checker lazy cuts",
        })
        if score == 0 or record.get("stop_reason"):
            break
        event_cuts = merged_cuts
    summary_path = RESULTS / "p3d32_V3_checker_loop.json"
    if not summary_path.exists():
        dump(summary_path, {"tag": "p3d32", "variant": variant, "rounds": rounds,
                            "status": "no_round_completed"})
    print(json.dumps({"summary": str(summary_path), "rounds": len(rounds),
                      "best_round": min((r for r in rounds if "gate_score" in r),
                                        key=lambda r: r["gate_score"], default={}).get("round"),
                      "best_score": min(prior_scores, default=None),
                      "last_stop_reason": rounds[-1].get("stop_reason") if rounds else None},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
