#!/usr/bin/env python3
"""Run the p3d23 V24 official-checker-in-the-loop diagnosis, serially."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
TOOLS = ROOT / "codex_jobs/tools/p3d23"
RESULTS = TOOLS / "results"
BASE_CUTS = ROOT / "codex_jobs/tools/p3d20_r3/event_cuts_cumulative05.json"
DERIVER = ROOT / "codex_jobs/tools/p3d20_r3/derive_event_cuts.py"
OLD_GROUPS = [
    "r3_long", "r3_quer", "r3_wob", "crossing_stage", "axis_supports",
    "plane_core", "endpoint_stage", "safety_gitter", "safety_quer",
    "safety_single_quer", "g5", "r5_hole", "r4", "g11",
]
G11_KINDS = ("baeume", "felsen", "findlinge", "steine", "felsbloecke")
BASELINE_RULES = ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_regeln_current_schema.json"
TRANSFER = RELIEF3D / "neu/p3d18_joint_mesh_v24.json"
SOURCE = RELIEF3D / "relief_daten.json.gz"
EMPTY_CUTS = RESULTS / "p3d23_V24_R00_cuts.json"


def checked(args: list[str], *, label: str) -> subprocess.CompletedProcess[str]:
    run = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError(f"{label} failed ({run.returncode}): {run.stderr[-2000:]} {run.stdout[-1000:]}")
    return run


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def gate_score(probe: dict) -> tuple[int, dict]:
    rules = probe.get("rules_by_rule", {})
    d1 = probe.get("rules_by_tile", {}).get("D1", {})
    r8 = probe.get("R8_by_rule", {})
    r9 = probe.get("R9_by_rule", {})
    # Compare against the p3d17 replay in the current checker schema. The
    # historical 596 total omits G11; current-schema rules absent from that
    # replay start at zero so newly emitted rule names are still bounded.
    baseline_rules = json.loads(BASELINE_RULES.read_text(encoding="utf-8")).get("je_regel", {})
    r3_limits = {"R3_laengs_m": 6, "R3_quer_pct": 17, "R3_woelb_m": 19}
    rule_limits = {k: int(baseline_rules.get(k, 0)) + 5
                   for k in sorted(set(baseline_rules) | set(rules))}
    r8_limits = {"R8_stufe": 14, "R8_gitter": 15, "R8_quer": 10, "R8a_wegende": 29}
    r9_limits = {"R8b_delle": 30, "R9_saegezahn": 39, "R9w_wellen": 280}
    excess = {}
    for name, limit in rule_limits.items():
        excess[f"rule:{name}"] = max(0, int(rules.get(name, 0)) - limit)
    for name, limit in r8_limits.items():
        excess[f"R8:{name}"] = max(0, int(r8.get(name, 0)) - limit)
    for name, limit in r9_limits.items():
        excess[f"R9:{name}"] = max(0, int(r9.get(name, 0)) - limit)
    for name, limit in r3_limits.items():
        excess[f"D1:{name}"] = max(0, int(d1.get(name, 0)) - limit)
    return sum(excess.values()), excess


def source_object(data: dict, hit: dict) -> tuple[list, int]:
    kind = str(hit.get("art", ""))
    if kind not in G11_KINDS:
        raise RuntimeError(f"G11-Typ nicht erkannt: {kind!r}")
    x, z = float(hit["x"]), float(hit["z"])
    candidates = []
    for index, item in enumerate(data.get(kind, [])):
        try:
            dx, dz = float(item[0]) - x, float(item[2]) - z
        except (TypeError, ValueError, IndexError):
            continue
        candidates.append((dx * dx + dz * dz, index, item))
    if not candidates:
        raise RuntimeError(f"Kein Objekt fuer G11-Treffer {kind}@{x}|{z}")
    distance2, index, item = min(candidates)
    if distance2 > 0.006:
        raise RuntimeError(f"G11-Objektzuordnung zu ungenau: {kind}@{x}|{z}, d2={distance2}")
    return item, index


def g11_cuts(probe: dict, existing: list[dict]) -> tuple[list[dict], int]:
    relief_path = Path(probe["probe_relief"])
    data = json.loads(gzip.decompress(relief_path.read_bytes()))
    baseline = json.loads(BASELINE_RULES.read_text(encoding="utf-8"))
    old = [h for h in baseline.get("treffer", [])
           if h.get("feld") == "D1" and h.get("regel") == "G11_objekt_schwebt_sinkt"]
    old_keys = {(h.get("art"), round(float(h.get("x", 0)), 1), round(float(h.get("z", 0)), 1)) for h in old}
    seen = {(c.get("art"), round(float(c["point"][0]), 1), round(float(c["point"][1]), 1))
            for c in existing if c.get("kind") == "G11"}
    hits = [h for h in probe.get("rules_D1_hits", [])
            if h.get("regel") == "G11_objekt_schwebt_sinkt"]
    new = []
    for hit in sorted(hits, key=lambda h: (str(h.get("art")), float(h["x"]), float(h["z"]))):
        key = (hit.get("art"), round(float(hit["x"]), 1), round(float(hit["z"]), 1))
        if key in old_keys or key in seen:
            continue
        item, index = source_object(data, hit)
        cut = {
            "kind": "G11", "point": [float(item[0]), float(item[2])],
            "object_height_m": float(item[1]), "art": str(hit.get("art")),
            "source_object_index": int(index), "probe_hit": hit,
        }
        new.append(cut)
        seen.add(key)
    return new, len(hits)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    base = json.loads(BASE_CUTS.read_text(encoding="utf-8"))
    dump(EMPTY_CUTS, base)
    old = json.loads(BASELINE_RULES.read_text(encoding="utf-8"))
    baseline_d1_g11 = sum(h.get("feld") == "D1" and h.get("regel") == "G11_objekt_schwebt_sinkt"
                          for h in old.get("treffer", []))
    rounds = []
    all_cuts = list(base)
    seen_cut_hashes = set()
    best_score = None
    best_round = None
    no_improve = 0
    for round_index in range(1, 9):
        round_name = f"V24_round{round_index:02d}"
        cuts_path = RESULTS / f"p3d23_{round_name}_cuts.json"
        dump(cuts_path, all_cuts)
        solution_path = RESULTS / f"p3d23_{round_name}_model.json"
        solve_cmd = [
            sys.executable, str(TOOLS / "run_diagnostic.py"),
            "--geometry", "V24", "--scenario", "joint", "--groups", *OLD_GROUPS,
            "--source-relief", str(SOURCE), "--transfer-base", str(TRANSFER),
            "--r8-center", "152.54985704503775", "28.48954534572434",
            "--event-cuts", str(cuts_path), "--out", str(solution_path),
            "--time-limit", "600", "--keep-solution",
        ]
        checked(solve_cmd, label=f"solve {round_name}")
        solution = json.loads(solution_path.read_text(encoding="utf-8"))
        if not solution.get("primal_feasible"):
            rounds.append({"round": round_index, "model_status": solution.get("status"),
                           "model_status_code": solution.get("status_code"),
                           "primal_feasible": False, "model_slack_values": solution.get("slack_values"),
                           "cuts_before": len(all_cuts)})
            break
        probe_path = RESULTS / f"p3d23_{round_name}_official_probe.json"
        checked([sys.executable, str(TOOLS / "probe_direct_transfer.py"), str(solution_path),
                 str(TRANSFER), str(probe_path)], label=f"official probe {round_name}")
        probe = json.loads(probe_path.read_text(encoding="utf-8"))
        derived_path = RESULTS / f"p3d23_{round_name}_derived_cuts.json"
        derivation = checked([sys.executable, str(DERIVER), str(probe_path), str(derived_path)],
                             label=f"component derivation {round_name}")
        derived = json.loads(derived_path.read_text(encoding="utf-8"))
        g5_r5_new = [cut for cut in derived if cut.get("kind") in {"G5", "R5"}]
        new_g11, g11_d1_count = g11_cuts(probe, all_cuts)
        next_cuts = [*all_cuts, *g5_r5_new, *new_g11]
        dedup = {}
        for cut in next_cuts:
            key = json.dumps(cut, sort_keys=True, separators=(",", ":"))
            dedup[key] = cut
        next_cuts = [dedup[key] for key in sorted(dedup)]
        score, score_parts = gate_score(probe)
        g5 = probe.get("rules_by_rule", {}).get("G5_beule_klippe", 0)
        r5 = probe.get("rules_by_rule", {}).get("R5_loch", 0)
        g11 = probe.get("rules_by_rule", {}).get("G11_objekt_schwebt_sinkt", 0)
        d1 = probe.get("rules_by_tile", {}).get("D1", {})
        round_record = {
            "round": round_index, "model_status": solution.get("status"),
            "model_status_code": solution.get("status_code"),
            "primal_feasible": solution.get("primal_feasible"),
            "optimality_proven": solution.get("optimality_proven"),
            "model_weighted_l1": solution.get("weighted_l1_value"),
            "model_slack_values": solution.get("slack_values"),
            "model_maximum_normalized_slack": solution.get("maximum_normalized_slack"),
            "official_rules_total": probe.get("rules_total"),
            "official_G5_total_D1": [g5, d1.get("G5_beule_klippe", 0)],
            "official_R5_loch_total_D1": [r5, d1.get("R5_loch", 0)],
            "official_R4_schlucht_total_D1": [probe.get("rules_by_rule", {}).get("R4_schlucht", 0), d1.get("R4_schlucht", 0)],
            "official_G11_total_D1": [g11, g11_d1_count],
            "official_R8_total_by_rule": {"total": probe.get("R8_total"), **probe.get("R8_by_rule", {})},
            "official_R8_D1_by_rule": probe.get("R8_by_tile", {}).get("D1", {}),
            "official_R8_by_tile_D1_G1_D2": {
                tile: probe.get("R8_by_tile", {}).get(tile, {}) for tile in ("D1", "G1", "D2")
            },
            "official_R9_total_by_rule": {"total": probe.get("R9_total"), **probe.get("R9_by_rule", {})},
            "official_R9_D1_by_rule": probe.get("R9_by_tile", {}).get("D1", {}),
            "official_R9_by_tile_D1_G1_D2": {
                tile: probe.get("R9_by_tile", {}).get(tile, {}) for tile in ("D1", "G1", "D2")
            },
            "official_rules_by_tile_D1_G1_D2": {
                tile: probe.get("rules_by_tile", {}).get(tile, {}) for tile in ("D1", "G1", "D2")
            },
            "official_R3_D1": {k: int(d1.get(k, 0)) for k in ("R3_laengs_m", "R3_quer_pct", "R3_woelb_m")},
            "official_R8_D1_crossing_stage": [h for h in probe.get("R8_D1_hits", [])
                                                 if "stufe" in str(h.get("regel", "")).lower()],
            "official_R8_D1_endpoint": [h for h in probe.get("R8_D1_hits", [])
                                         if "wegende" in str(h.get("regel", "")).lower()],
            "fresh_component_derivation": derivation.stdout,
            "new_G5_cuts": sum(c.get("kind") == "G5" for c in g5_r5_new),
            "new_R5_cuts": sum(c.get("kind") == "R5" for c in g5_r5_new),
            "new_G11_cuts": len(new_g11), "cuts_before": len(all_cuts),
            "cuts_after": len(next_cuts), "score": score, "score_excess_by_gate": score_parts,
            "solution_json": str(solution_path), "probe_json": str(probe_path),
            "cut_json": str(cuts_path), "derived_cut_json": str(derived_path),
        }
        rounds.append(round_record)
        if best_score is None or score < best_score:
            best_score, best_round, no_improve = score, round_index, 0
        else:
            no_improve += 1
        cut_hash = hashlib.sha256(json.dumps(next_cuts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if cut_hash in seen_cut_hashes:
            round_record["stop_reason"] = "cut_cycle"
            break
        seen_cut_hashes.add(cut_hash)
        if len(next_cuts) == len(all_cuts):
            round_record["stop_reason"] = "no_new_cuts"
            break
        if no_improve >= 2:
            round_record["stop_reason"] = "two_rounds_without_score_improvement"
            break
        all_cuts = next_cuts
    output = {
        "tag": "p3d23", "geometry": "V24", "baseline_D1_G11_hits": baseline_d1_g11,
        "start_event_cut_count": len(base), "rounds": rounds,
        "best_round": best_round, "best_score": best_score,
        "final_cut_count": len(all_cuts), "method": "serial official checker-in-the-loop; no mesh build",
    }
    out = RESULTS / "p3d23_V24_checker_loop.json"
    dump(out, output)
    print(json.dumps({"out": str(out), "rounds": len(rounds), "best_round": best_round,
                      "best_score": best_score, "last_model_status": rounds[-1].get("model_status") if rounds else None},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
