#!/usr/bin/env python3
"""Run unchanged official gates on one p3d33 Float32 direct-transfer field."""
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
MODEL_PATH = Path(__file__).with_name("diagnose_lp_p3d33.py")


def load_model():
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    spec = importlib.util.spec_from_file_location("p3d33_probe_model", MODEL_PATH)
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

    variant = str(solution.get("p3d33_variant", "1"))
    window_start_m, window_end_m = model.P3D33_VARIANTS[variant]
    reference_v3 = json.loads(model.P3D31_V3_REFERENCE.read_text(encoding="utf-8"))["routes"]
    ramp2 = solution["routes"]["rampe_2"]
    station_m = np.asarray(ramp2["station_m"], dtype=np.float64)
    height_new = np.asarray(ramp2["solution_h_m"], dtype=np.float64)
    height_old = np.asarray(reference_v3["rampe_2"]["solution_h_m"], dtype=np.float64)
    variable_mask = ((station_m >= window_start_m - 1e-9)
                     & (station_m <= window_end_m + 1e-9))
    outside_profile_equal = np.array_equal(height_new[~variable_mask], height_old[~variable_mask])
    route_coords = np.asarray(ramp2["coords_map"], dtype=np.float64)
    ramp2_start_fixed = (height_new[0].tobytes() == height_old[0].tobytes())
    route11_new = np.asarray(solution["routes"]["rampe_11"]["solution_h_m"], dtype=np.float64)
    route11_old = np.asarray(reference_v3["rampe_11"]["solution_h_m"], dtype=np.float64)
    route11_fixed = np.array_equal(route11_new, route11_old)
    first = int(np.flatnonzero(variable_mask)[0])
    last = int(np.flatnonzero(variable_mask)[-1])
    step_m = float(station_m[1] - station_m[0])
    slope_left = (height_new[first] - height_new[first - 1]) / step_m
    slope_right = (height_new[first + 1] - height_new[first]) / step_m
    slope_left_end = (height_new[last] - height_new[last - 1]) / step_m
    slope_right_end = (height_new[last + 1] - height_new[last]) / step_m
    second_at_joins = {
        "left_m_per_m2": float((height_new[first - 1] - 2.0 * height_new[first]
                                 + height_new[first + 1]) / step_m**2),
        "right_m_per_m2": float((height_new[last - 1] - 2.0 * height_new[last]
                                  + height_new[last + 1]) / step_m**2),
    }
    route_normals = np.gradient(route_coords, axis=0)
    route_normals /= np.maximum(np.linalg.norm(route_normals, axis=1, keepdims=True), 1e-9)
    route_normals = np.column_stack((-route_normals[:, 1], route_normals[:, 0]))
    local_coords = route_coords.copy()
    local_coords[:, 0] -= float(solution["surface_grid"]["x0"])
    rs = int(source_data["rs"])
    center_h = ndi.map_coordinates(candidate.astype(np.float64),
                                   [local_coords[:, 1] * rs, local_coords[:, 0] * rs],
                                   order=1, mode="nearest")
    side_plus = route_coords + route_normals * 1.5
    side_minus = route_coords - route_normals * 1.5
    side_plus[:, 0] -= float(solution["surface_grid"]["x0"])
    side_minus[:, 0] -= float(solution["surface_grid"]["x0"])
    plus_h = ndi.map_coordinates(candidate.astype(np.float64),
                                 [side_plus[:, 1] * rs, side_plus[:, 0] * rs],
                                 order=1, mode="nearest")
    minus_h = ndi.map_coordinates(candidate.astype(np.float64),
                                  [side_minus[:, 1] * rs, side_minus[:, 0] * rs],
                                  order=1, mode="nearest")
    wob_at_joins = {
        "left_m": float(abs(center_h[first] - 0.5 * (plus_h[first] + minus_h[first]))),
        "right_m": float(abs(center_h[last] - 0.5 * (plus_h[last] + minus_h[last]))),
    }
    slopes = np.gradient(height_new, station_m)
    second_differences = np.gradient(slopes, station_m)
    profile_table = [
        {"station_m": float(station_m[k]), "height_old_m": float(height_old[k]),
         "height_new_m": float(height_new[k]), "slope_m_per_m": float(slopes[k]),
         "second_difference_m_per_m2": float(second_differences[k])}
        for k in np.flatnonzero(variable_mask)
    ]
    if not outside_profile_equal:
        raise RuntimeError("rampe_2-Profil außerhalb des freigegebenen Fensters hat sich geändert")
    if not ramp2_start_fixed or not route11_fixed:
        raise RuntimeError("rampe_2-Start oder rampe_11-Profil ist nicht bitgleich zur p3d31-Referenz")
    if (abs(slope_left - slope_right) > 2e-6
            or abs(slope_left_end - slope_right_end) > 2e-6):
        raise RuntimeError("rampe_2-Fensterübergang ist nicht C1-stetig")

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
    probe_path = Path(f"/tmp/relief_p3d33_{tag}.json.gz")
    probe_path.write_bytes(gzip.compress(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        compresslevel=9,
        mtime=0,
    ))
    loch_path = Path(f"/tmp/gate_loch_p3d33_{tag}.json")
    rules_path = Path(f"/tmp/regeln_p3d33_{tag}.json")
    r8_path = Path(f"/tmp/r8_p3d33_{tag}.json")
    r9_path = Path(f"/tmp/r9_p3d33_{tag}.json")
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
        raise RuntimeError("p3d33-Fenster, Kandidat und p3d17-D1 haben verschiedene Rasterformen")
    unchanged = np.array_equal(candidate[~active_window], p3d17_reference[~active_window])
    if not unchanged:
        raise RuntimeError("Float32-Ausgabe ändert außerhalb des p3d33-Fensters p3d17-Höhen")
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
    result = {
        "candidate_kind": "p3d33 Float32 direct-transfer probe; no mesh build",
        "geometry": solution.get("geometry"),
        "scenario": solution.get("scenario"),
        "source_relief_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "transfer_base": transfer_path.name,
        "transfer_base_sha256": hashlib.sha256(transfer_path.read_bytes()).hexdigest(),
        "D1_height_sha256": hashlib.sha256(candidate.tobytes()).hexdigest(),
        "rampe_2_window_m": [window_start_m, window_end_m],
        "rampe_2_outside_window_bitwise_equal_to_p3d31_v3": outside_profile_equal,
        "rampe_2_start_bitwise_equal_to_p3d31_v3": ramp2_start_fixed,
        "rampe_11_profile_bitwise_equal_to_p3d31_v3": route11_fixed,
        "rampe_2_max_axis_to_emitted_surface_delta_m": float(np.max(np.abs(center_h - height_new))),
        "rampe_2_transition": {
            "left_station_m": float(station_m[first]),
            "left_height_m": float(height_new[first]),
            "left_slope_before_m_per_m": float(slope_left),
            "left_slope_after_m_per_m": float(slope_right),
            "right_station_m": float(station_m[last]),
            "right_height_m": float(height_new[last]),
            "right_slope_before_m_per_m": float(slope_left_end),
            "right_slope_after_m_per_m": float(slope_right_end),
            "second_difference_at_joins_m_per_m2": second_at_joins,
            "official_R3_wob_at_joins_m": wob_at_joins,
            "C1_pass": (abs(slope_left - slope_right) <= 2e-6
                        and abs(slope_left_end - slope_right_end) <= 2e-6),
        },
        "rampe_2_profile_window_table": profile_table,
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
        "rules_by_tile": tiles,
        "D1_rules": tiles["D1"],
        "rules_D1_hits": [hit for hit in rules.get("treffer", []) if hit.get("feld") == "D1"],
        "R8_total": r8.get("summe"),
        "R8_by_rule": r8.get("je_regel", {}),
        "R8_by_tile": r8.get("je_feld", {}),
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
