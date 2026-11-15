#!/usr/bin/env python3
"""Run unchanged official gates on one p3d36 Float32 direct-transfer field."""
from __future__ import annotations

import base64
import gzip
import hashlib
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
MODEL_PATH = Path(__file__).with_name("diagnose_lp_p3d36.py")


def load_model():
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    p3d33_tools = ROOT / "codex_jobs/tools/p3d33"
    if str(p3d33_tools) not in sys.path:
        sys.path.insert(0, str(p3d33_tools))
    spec = importlib.util.spec_from_file_location("p3d36_probe_model", MODEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("p3d29 model module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run(args: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if completed.returncode not in (0, 1):
        raise RuntimeError(
            f"Checker failed ({completed.returncode}): {args}; "
            f"stdout={completed.stdout[-1000:]}; stderr={completed.stderr[-1000:]}"
        )
    return completed


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: probe_direct_transfer.py MODEL_JSON TRANSFER_BASE OUT_JSON")
    solution_path, transfer_path, out_path = map(Path, sys.argv[1:])
    solution = json.loads(solution_path.read_text(encoding="utf-8"))
    if not solution.get("primal_feasible") or "surface_grid" not in solution:
        raise RuntimeError("No feasible direct-transfer field in solver JSON")

    os.environ["P3D20_MODEL_GITTER_LIMIT"] = "0.020"
    os.environ["P3D20_MODEL_QUER_LIMIT"] = "3.0"
    os.environ["P3D20_MODEL_SINGLE_QUER_LIMIT"] = "20.0"
    model = load_model()
    model.RELIEF = Path(solution["source_relief_path"]).resolve()
    model.R8_GATE_CENTER = np.asarray(solution["r8_center_unrounded_map"], dtype=np.float64)
    model.CROSSING = model.R8_GATE_CENTER.copy()

    from neu import mesh as neu_mesh
    center = model.R8_GATE_CENTER.tolist()
    for slot in ("22", "24"):
        neu_mesh.KREUZUNG_SETTINGS[slot]["solution_file"] = transfer_path.name
        neu_mesh.KREUZUNG_SETTINGS[slot]["crossing_center_map"] = center

    source_bytes = model.RELIEF.read_bytes()
    source_data = json.loads(gzip.decompress(source_bytes))
    fixed, coverage, _, _ = model.p3d17_transfer_context()
    target = np.asarray(solution["surface_grid"]["heights_m"], dtype=np.float64)
    candidate = (fixed + coverage * target).astype("<f4")

    reference_v3 = json.loads(model.P3D31_V3_REFERENCE.read_text(encoding="utf-8"))["routes"]
    profile_meta = solution["p3d36_profile_windows"]
    profile_results = {}
    outside_profile_equal = True
    for route_number in (2, 11):
        route_name = f"rampe_{route_number}"
        route = solution["routes"][route_name]
        station_m = np.asarray(route["station_m"], dtype=np.float64)
        height_new = np.asarray(route["solution_h_m"], dtype=np.float64)
        height_old = np.asarray(reference_v3[route_name]["solution_h_m"], dtype=np.float64)
        coords = np.asarray(route["coords_map"], dtype=np.float64)
        window = profile_meta[route_name]
        start_m, end_m = map(float, window["physical_station_window_m"])
        variable_mask = ((station_m >= start_m - 1e-9)
                         & (station_m <= end_m + 1e-9))
        outside_equal = np.array_equal(height_new[~variable_mask], height_old[~variable_mask])
        outside_profile_equal &= outside_equal
        slopes = np.gradient(height_new, station_m)
        second = np.gradient(slopes, station_m)
        table_start, table_end = (0.0, 55.0) if route_number == 2 else (0.0, 95.0)
        table_indices = np.flatnonzero((station_m >= table_start - 1e-9)
                                        & (station_m <= table_end + 1e-9))
        profile_table = [
            {"station_m": float(station_m[k]), "height_old_m": float(height_old[k]),
             "height_new_m": float(height_new[k]), "slope_m_per_m": float(slopes[k]),
             "second_difference_m_per_m2": float(second[k])}
            for k in table_indices
        ]
        transitions = []
        for seam in solution["p3d36_profile_transitions"]:
            if int(seam["route"]) != route_number:
                continue
            k = int(seam["profile_index"])
            slope_before = float((height_new[k] - height_new[k - 1]) /
                                 (station_m[k] - station_m[k - 1]))
            slope_after = float((height_new[k + 1] - height_new[k]) /
                                (station_m[k + 1] - station_m[k]))
            d2 = float((height_new[k - 1] - 2.0 * height_new[k]
                        + height_new[k + 1]) /
                       ((station_m[k] - station_m[k - 1]) ** 2))
            transitions.append({
                "profile_index": int(k),
                "station_m": float(station_m[k]),
                "height_m": float(height_new[k]),
                "height_old_m": float(height_old[k]),
                "slope_left_m_per_m": slope_before,
                "slope_right_m_per_m": slope_after,
                "slope_delta_m_per_m": slope_after - slope_before,
                "second_difference_m_per_m2": d2,
                "C0_height_continuous": True,
                "C1_pass": abs(slope_after - slope_before) <= 2e-6,
            })
        route_normals = np.gradient(coords, axis=0)
        route_normals /= np.maximum(np.linalg.norm(route_normals, axis=1, keepdims=True), 1e-9)
        route_normals = np.column_stack((-route_normals[:, 1], route_normals[:, 0]))
        local_coords = coords.copy()
        local_coords[:, 0] -= float(solution["surface_grid"]["x0"])
        rs = int(source_data["rs"])
        axis_h = ndi.map_coordinates(candidate.astype(np.float64),
                                      [local_coords[:, 1] * rs, local_coords[:, 0] * rs],
                                      order=1, mode="nearest")
        side_plus = coords + route_normals * 1.5
        side_minus = coords - route_normals * 1.5
        side_plus[:, 0] -= float(solution["surface_grid"]["x0"])
        side_minus[:, 0] -= float(solution["surface_grid"]["x0"])
        plus_h = ndi.map_coordinates(candidate.astype(np.float64),
                                     [side_plus[:, 1] * rs, side_plus[:, 0] * rs],
                                     order=1, mode="nearest")
        minus_h = ndi.map_coordinates(candidate.astype(np.float64),
                                      [side_minus[:, 1] * rs, side_minus[:, 0] * rs],
                                      order=1, mode="nearest")
        for seam in transitions:
            k = int(seam["profile_index"])
            seam["official_R3_wob_m"] = float(abs(axis_h[k] - 0.5 * (plus_h[k] + minus_h[k])))
        profile_results[route_name] = {
            "window_m": [start_m, end_m],
            "variable_samples": int(variable_mask.sum()),
            "outside_window_bitwise_equal_to_p3d31_v3": outside_equal,
            "maximum_axis_to_float32_surface_delta_m": float(np.max(np.abs(axis_h - height_new))),
            "transitions": transitions,
            "profile_table_station_range_m": [table_start, table_end],
            "profile_table": profile_table,
        }
        if any(not item["C1_pass"] for item in transitions):
            raise RuntimeError(f"C1-Übergang rampe_{route_number} verletzt")
    if not outside_profile_equal:
        raise RuntimeError("Ein Rampenprofil außerhalb seines freigegebenen Fensters ist verändert")

    vector_path = RELIEF3D / "neu/vektor.json"
    fields_path = RELIEF3D / "neu/felder.npz"
    old_cross = os.environ.get("RELIEF_KREUZUNG_VAR")
    old_end = os.environ.get("RELIEF_WEGEND_VAR")
    os.environ["RELIEF_KREUZUNG_VAR"] = "24"
    os.environ["RELIEF_WEGEND_VAR"] = "1"
    try:
        manifest = neu_mesh.build_manifest(
            model.RELIEF,
            RELIEF3D / "neu/zellen_relief.csv",
            vector_path,
            fields_path,
            variant="2",
        )
    finally:
        if old_cross is None:
            os.environ.pop("RELIEF_KREUZUNG_VAR", None)
        else:
            os.environ["RELIEF_KREUZUNG_VAR"] = old_cross
        if old_end is None:
            os.environ.pop("RELIEF_WEGEND_VAR", None)
        else:
            os.environ["RELIEF_WEGEND_VAR"] = old_end
    positions = np.frombuffer(
        base64.b64decode(manifest["tiles"]["D1"]["vertices_xyz_f32"]), dtype="<f4",
    ).copy().reshape(-1, 3)
    if len(positions) != candidate.size:
        raise RuntimeError("D1 mesh manifest and direct-transfer raster do not match")
    positions[:, 1] = candidate.ravel()
    manifest["tiles"]["D1"]["vertices_xyz_f32"] = base64.b64encode(positions.tobytes()).decode("ascii")
    manifest["tiles"]["D1"]["height_sha256"] = hashlib.sha256(positions[:, 1].tobytes()).hexdigest()
    package = dict(source_data)
    package["neu_mesh_tiles"] = manifest
    from pruefung import neu_mesh_adapter
    data = neu_mesh_adapter.adapt_data(source_data, package)

    tag = out_path.stem
    work_tmp = Path("/tmp/p3d36")
    work_tmp.mkdir(parents=True, exist_ok=True)
    probe_path = work_tmp / f"relief_p3d36_{tag}.json.gz"
    probe_path.write_bytes(gzip.compress(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        compresslevel=9,
        mtime=0,
    ))
    loch_path = work_tmp / f"gate_loch_p3d36_{tag}.json"
    rules_path = work_tmp / f"regeln_p3d36_{tag}.json"
    r8_path = work_tmp / f"r8_p3d36_{tag}.json"
    r9_path = work_tmp / f"r9_p3d36_{tag}.json"
    env = dict(os.environ)
    env.update({
        "HTML": "index.html",
        "OUT": str(loch_path),
        "RAND": "0.6",
        "NODE_PATH": "/tmp/w3/node_modules",
    })
    node = run(["node", "pruefung/loch_o18g.js"], cwd=RELIEF3D, env=env)
    env["LOCHSCAN"] = str(loch_path)
    run([sys.executable, str(RELIEF3D / "pruefung/pruefe_regeln.py"),
         str(probe_path), str(rules_path)], cwd=RELIEF3D, env=env)
    run([sys.executable, str(RELIEF3D / "pruefung/r8_kreuzung.py"),
         str(probe_path), str(r8_path)], cwd=RELIEF3D, env=env)
    run([sys.executable, str(RELIEF3D / "pruefung/r9_form.py"),
         str(probe_path), str(r9_path)], cwd=RELIEF3D, env=env)

    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    r8 = json.loads(r8_path.read_text(encoding="utf-8"))
    r9 = json.loads(r9_path.read_text(encoding="utf-8"))
    construction_path = solution_path.with_name(solution_path.stem + "_construction.json")
    construction_payload = json.loads(construction_path.read_text(encoding="utf-8"))
    active_window = np.asarray(
        construction_payload["construction"]["active_mask"], dtype=bool,
    )
    p3d17_reference = model.p3d17_reference_output()
    if active_window.shape != candidate.shape or p3d17_reference.shape != candidate.shape:
        raise RuntimeError("p3d36-Fenster, Kandidat und p3d17-D1 haben verschiedene Rasterformen")
    unchanged = np.array_equal(candidate[~active_window], p3d17_reference[~active_window])
    if not unchanged:
        raise RuntimeError("Float32-Ausgabe ändert außerhalb des p3d36-Fensters p3d17-Höhen")
    r8_center = [float(value) for value in solution["r8_center_unrounded_map"]]
    crossing_candidates = r8.get("liste", [])
    crossing_cluster = (min(
        crossing_candidates,
        key=lambda item: ((float(item["x"]) - r8_center[0]) ** 2
                          + (float(item["z"]) - r8_center[1]) ** 2,
                          float(item["x"]), float(item["z"]), str(item.get("art", ""))),
    ) if crossing_candidates else None)
    crossing_quer_hit = None
    if crossing_cluster is not None:
        crossing_quer_hit = next((hit for hit in r8.get("treffer", [])
                                  if hit.get("regel") == "R8_quer"
                                  and float(hit.get("x", -1)) == float(crossing_cluster["x"])
                                  and float(hit.get("z", -1)) == float(crossing_cluster["z"])), None)
    crossing_gate = {
        "requested_label_coordinate_map": [152.5, 28.5],
        "model_center_unrounded_map": r8_center,
        "official_cluster": crossing_cluster,
        "R8_quer_hit": crossing_quer_hit,
        "R8_quer_pass_from_official_checker": crossing_quer_hit is None,
    }
    tiles = {tile: {} for tile in ("D1", "G1", "D2")}
    for hit in rules.get("treffer", []):
        tile = hit.get("feld")
        if tile in tiles:
            tiles[tile][hit["regel"]] = tiles[tile].get(hit["regel"], 0) + 1
    baseline_rules = json.loads((ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_regeln_current_schema.json").read_text(encoding="utf-8"))
    baseline_d2 = [hit for hit in baseline_rules.get("treffer", []) if hit.get("feld") == "D2"]
    current_d2 = [hit for hit in rules.get("treffer", []) if hit.get("feld") == "D2"]
    from collections import Counter
    def hit_key(hit):
        return json.dumps(hit, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    new_d2_keys = list((Counter(map(hit_key, current_d2)) - Counter(map(hit_key, baseline_d2))).elements())
    new_d2 = [json.loads(key) for key in new_d2_keys]
    if new_d2:
        raise RuntimeError(f"p3d36 erzeugt neue pruefe_regeln-Treffer in D2: {new_d2[:5]}")
    baseline_rules_by_rule = baseline_rules.get("je_regel", {})
    current_rules_by_rule = rules.get("je_regel", {})
    rule_deltas_vs_p3d17 = {
        rule: int(current_rules_by_rule.get(rule, 0) - baseline_rules_by_rule.get(rule, 0))
        for rule in sorted(set(current_rules_by_rule) | set(baseline_rules_by_rule))
    }
    rule_plus5_pass = all(delta <= 5 for delta in rule_deltas_vs_p3d17.values())
    r8_baseline = json.loads((ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_r8.json").read_text(encoding="utf-8"))
    r9_baseline = json.loads((ROOT / "codex_jobs/tools/p3d20_r3/official_gates/p3d17_reference_r9.json").read_text(encoding="utf-8"))
    def r8_signature(hit):
        return (str(hit.get("regel", "")), str(hit.get("feld", "")),
                round(float(hit.get("x", 0.0)), 1), round(float(hit.get("z", 0.0)), 1),
                str(hit.get("art", "")), str(hit.get("weg", "")))
    r8_baseline_counts = Counter(map(r8_signature, r8_baseline.get("treffer", [])))
    r8_new_hits = []
    for hit in r8.get("treffer", []):
        key = r8_signature(hit)
        if r8_baseline_counts.get(key, 0):
            r8_baseline_counts[key] -= 1
        else:
            r8_new_hits.append(hit)
    r8_d2 = [hit for hit in r8.get("treffer", []) if hit.get("feld") == "D2"]
    r9_d2 = [hit for hit in r9.get("treffer", []) if hit.get("feld") == "D2"]
    r8a_start_hits = [hit for hit in r8.get("treffer", [])
                      if hit.get("regel") == "R8a_wegende"
                      and hit.get("weg") == "rampe_2_anfang"]
    r8a_d1_hits = [hit for hit in r8.get("treffer", [])
                   if hit.get("regel") == "R8a_wegende" and hit.get("feld") == "D1"]
    target_metrics = {
        "R5_spitze_D1_eq_0": sum(hit.get("regel") == "R5_spitze" and hit.get("feld") == "D1" for hit in rules.get("treffer", [])) == 0,
        "G6_D1_le_3": sum(hit.get("regel") == "G6_facette" and hit.get("feld") == "D1" for hit in rules.get("treffer", [])) <= 3,
        "R8b_D1_le_1": sum(hit.get("regel") == "R8b_delle" and hit.get("feld") == "D1" for hit in r9.get("treffer", [])) <= 1,
        "G3_D1_le_1": sum(hit.get("regel") == "G3_spitze_unten" and hit.get("feld") == "D1" for hit in rules.get("treffer", [])) <= 1,
        "R9w_total_le_280": int(r9.get("je_regel", {}).get("R9w_wellen", 0)) <= 280,
        "G5_total_le_69": int(current_rules_by_rule.get("G5_beule_klippe", 0)) <= 69,
        "G5_D1_le_2": sum(hit.get("regel") == "G5_beule_klippe" and hit.get("feld") == "D1" for hit in rules.get("treffer", [])) <= 2,
        "R5_loch_total_le_22": int(current_rules_by_rule.get("R5_loch", 0)) <= 22,
        "R5_loch_D1_le_5": sum(hit.get("regel") == "R5_loch" and hit.get("feld") == "D1" for hit in rules.get("treffer", [])) <= 5,
        "D1_R4_schlucht_eq_0": sum(hit.get("regel") == "R4_schlucht" and hit.get("feld") == "D1" for hit in rules.get("treffer", [])) == 0,
        "R3_D1_le_6_7_7": all(sum(hit.get("regel") == rule and hit.get("feld") == "D1" for hit in rules.get("treffer", [])) <= maximum
                              for rule, maximum in (("R3_laengs_m", 6), ("R3_quer_pct", 7), ("R3_woelb_m", 7))),
        "per_rule_increase_vs_p3d17_le_5": rule_plus5_pass,
        "D2_no_new_pruefe_regeln_hits": not new_d2,
        "R8_D2_zero": not r8_d2,
        "R9_D2_zero": not r9_d2,
        "R8a_D1_no_unpermitted_hits": all(
            hit.get("ausnahme") == "R8a_ausnahme_rampe2_start" for hit in r8a_d1_hits
        ),
        "rampe_2_start_R8a_exception_not_exceeded": not r8a_start_hits,
        "R8_no_new_hits_vs_p3d17": not r8_new_hits,
    }

    def r3_formula_report(surface: np.ndarray) -> dict:
        result_by_rule = {name: {"sections_D1": 0, "max_section_value": 0.0}
                          for name in ("R3_laengs_m", "R3_quer_pct", "R3_woelb_m")}
        rs = int(source_data["rs"])
        for route_number in (2, 11):
            raw = np.asarray(source_data["rampenwege"][route_number], dtype=np.float64)
            length = np.r_[0.0, np.cumsum(np.hypot(*np.diff(raw, axis=0).T))]
            station = np.arange(0.0, length[-1] + 1e-6, 0.25)
            points = np.column_stack((np.interp(station, length, raw[:, 0]),
                                      np.interp(station, length, raw[:, 1])))
            direction = np.gradient(points, axis=0)
            direction /= np.maximum(np.linalg.norm(direction, axis=1, keepdims=True), 1e-9)
            normal = np.column_stack((-direction[:, 1], direction[:, 0]))

            def sample(coords: np.ndarray) -> np.ndarray:
                full_map = np.asarray(coords, dtype=np.float64)
                return ndi.map_coordinates(
                    np.asarray(surface, dtype=np.float64),
                    [full_map[:, 1] * rs, full_map[:, 0] * rs],
                    order=1, mode="nearest",
                )

            axis_h = sample(points)
            plus_h = sample(points + normal * 1.5)
            minus_h = sample(points - normal * 1.5)
            q = (plus_h - minus_h) / 3.0 * 100.0
            longitudinal = axis_h - ndi.gaussian_filter1d(axis_h, 8, mode="nearest")
            wob = np.abs(axis_h - (plus_h + minus_h) / 2.0)
            values = {
                "R3_laengs_m": (np.abs(longitudinal), 0.08),
                "R3_quer_pct": (np.abs(q), 3.5),
                "R3_woelb_m": (wob, 0.08),
            }
            for rule, (series, threshold) in values.items():
                for start in range(0, len(points), 16):
                    # Match pruefe_regeln.py's field() tile mapping exactly:
                    # x=168 belongs to E1 and z=43 belongs to D2.
                    if not (126.0 <= points[start, 0] < 168.0
                            and 0.0 <= points[start, 1] < 43.0):
                        continue
                    peak = float(np.max(series[start:start + 16], initial=0.0))
                    current = result_by_rule[rule]
                    current["max_section_value"] = max(current["max_section_value"], peak)
                    current["sections_D1"] += int(peak > threshold)
        return result_by_rule

    lp_double = (fixed + coverage * target).astype(np.float64)
    checker_grid = np.frombuffer(
        base64.b64decode(data["GB"]), dtype=np.float32,
    ).reshape(int(data["ny"]) * rs + 1, int(data["nx"]) * rs + 1).copy()
    grid_x0 = int(round(float(solution["surface_grid"]["x0"]) * rs))
    grid_z0 = int(round(float(solution["surface_grid"]["z0"]) * rs))
    full_double = checker_grid.astype(np.float64)
    full_float32 = checker_grid
    yslice = slice(grid_z0, grid_z0 + lp_double.shape[0])
    xslice = slice(grid_x0, grid_x0 + lp_double.shape[1])
    full_double[yslice, xslice] = lp_double
    full_float32[yslice, xslice] = candidate
    r3_double = r3_formula_report(full_double)
    r3_float32 = r3_formula_report(full_float32)
    checker_r3_counts = {
        "R3_laengs_m": int(tiles["D1"].get("R3_laengs_m", 0)),
        "R3_quer_pct": int(tiles["D1"].get("R3_quer_pct", 0)),
        "R3_woelb_m": int(tiles["D1"].get("R3_woelb_m", 0)),
    }
    model_endpoint = solution.get("family_max_relaxation_locations", {}).get("endpoint_r8a", {})
    r8a_checker_d1 = [hit for hit in r8.get("treffer", [])
                      if hit.get("regel") == "R8a_wegende" and hit.get("feld") == "D1"]
    model_vs_checker = {
        "R3_LP_double_formula": r3_double,
        "R3_Float32_formula": r3_float32,
        "R3_official_checker_D1_counts": checker_r3_counts,
        "R3_Float32_formula_counts_match_official_checker": {
            rule: r3_float32[rule]["sections_D1"] == count
            for rule, count in checker_r3_counts.items()
        },
        "R3_LP_hard_rows": solution.get("r3_D1_hard_rows"),
        "R8a_LP_max_violation_m": model_endpoint.get("maximum_violation_m"),
        "R8a_LP_worst_pair": model_endpoint.get("pair"),
        "R8a_official_checker_D1_hit_count": len(r8a_checker_d1),
        "R8a_official_checker_D1_hits": r8a_checker_d1,
    }
    result = {
        "candidate_kind": "p3d36 Float32 direct-transfer probe; no mesh build",
        "geometry": solution.get("geometry"),
        "scenario": solution.get("scenario"),
        "source_relief_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "transfer_base": transfer_path.name,
        "transfer_base_sha256": hashlib.sha256(transfer_path.read_bytes()).hexdigest(),
        "D1_height_sha256": hashlib.sha256(candidate.tobytes()).hexdigest(),
        "profile_outside_each_window_bitwise_equal_to_p3d31_v3": outside_profile_equal,
        "profile_results": profile_results,
        "model_vs_official_checker": model_vs_checker,
        "G1_height_sha256": manifest["tiles"]["G1"].get("height_sha256"),
        "D2_height_sha256": manifest["tiles"]["D2"].get("height_sha256"),
        "outside_window_bitwise_equal_to_p3d17": unchanged,
        "outside_window_vertex_count": int(np.count_nonzero(~active_window)),
        "outside_window_candidate_sha256": hashlib.sha256(
            candidate[~active_window].astype("<f4", copy=False).tobytes()
        ).hexdigest(),
        "outside_window_p3d17_sha256": hashlib.sha256(
            p3d17_reference[~active_window].astype("<f4", copy=False).tobytes()
        ).hexdigest(),
        "rules_total": rules.get("summe"),
        "rules_by_rule": rules.get("je_regel", {}),
        "rules_delta_vs_p3d17_by_rule": rule_deltas_vs_p3d17,
        "rules_plus5_pass": rule_plus5_pass,
        "rules_by_tile": tiles,
        "D2_rules_bitwise_hit_records_equal_to_p3d17": not new_d2 and Counter(map(hit_key, current_d2)) == Counter(map(hit_key, baseline_d2)),
        "D2_new_rules_hits": new_d2,
        "R8_D2_hits": r8_d2,
        "R9_D2_hits": r9_d2,
        "hard_target_checks": target_metrics,
        "hard_targets_pass": all(target_metrics.values()),
        "D1_rules": tiles["D1"],
        "rules_D1_hits": [hit for hit in rules.get("treffer", []) if hit.get("feld") == "D1"],
        "R8_total": r8.get("summe"),
        "R8_by_rule": r8.get("je_regel", {}),
        "R8_by_tile": r8.get("je_feld", {}),
        "R8_new_hits_vs_p3d17": {"count": len(r8_new_hits), "hits": r8_new_hits},
        "R8_D1_hits": [hit for hit in r8.get("treffer", []) if hit.get("feld") == "D1"],
        "R8_crossing_gate": crossing_gate,
        "R8a_hits_by_tile": {
            tile: [hit for hit in r8.get("treffer", [])
                   if hit.get("feld") == tile and hit.get("regel") == "R8a_wegende"]
            for tile in ("D1", "G1", "D2")
        },
        "R9_total": r9.get("summe"),
        "R9_by_rule": r9.get("je_regel", {}),
        "R9_by_tile": r9.get("je_feld", {}),
        "R9_D1_hits": [hit for hit in r9.get("treffer", []) if hit.get("feld") == "D1"],
        "gate_loch_json": str(loch_path),
        "probe_relief": str(probe_path),
        "node_stdout": node.stdout[-1000:],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in {"rules_D1_hits", "R8_D1_hits", "R9_D1_hits"}},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
