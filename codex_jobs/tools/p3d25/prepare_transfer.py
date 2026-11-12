#!/usr/bin/env python3
"""Rebind the unchanged p3d18/V24 height profiles to candidate start axes."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Point

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
CELL_M = 1.2
OLD_CENTER = [152.54985704503775, 28.48954534572434]
P3D21_APPLY = ROOT / "codex_jobs/tools/p3d21/apply_route_variant.py"
SPEC = importlib.util.spec_from_file_location("p3d25_crossing_center", P3D21_APPLY)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("p3d21 crossing-center helper unavailable")
P3D21 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P3D21)


def sample_path(raw: list[list[float]], step: float = 0.25) -> tuple[np.ndarray, np.ndarray]:
    path = np.asarray(raw, dtype=np.float64)
    cumulative = np.r_[0.0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))]
    station = np.arange(0.0, cumulative[-1] + 1e-7, step)
    coords = np.column_stack((np.interp(station, cumulative, path[:, 0]),
                              np.interp(station, cumulative, path[:, 1])))
    return station, coords


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--base-v24", type=Path, default=RELIEF3D / "neu/p3d18_joint_mesh_v24.json")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--r8-center", type=float, nargs=2)
    args = ap.parse_args()
    source_raw = args.source.read_bytes()
    source_data = json.loads(gzip.decompress(source_raw))
    payload = json.loads(args.base_v24.read_text(encoding="utf-8"))
    center = args.r8_center or P3D21.official_crossing_center(source_data, source_data["rampenwege"])
    center = [float(center[0]), float(center[1])]
    if [round(center[0], 1), round(center[1], 1)] != [152.5, 28.5]:
        raise RuntimeError(f"D1-Kreuzung hat sich verschoben: center={center}")
    payload["source_relief_sha256"] = hashlib.sha256(source_raw).hexdigest()
    payload["R8_gate_center_unrounded_map"] = center
    for index in (2, 11):
        name = f"rampe_{index}"
        new_station, new_coords = sample_path(source_data["rampenwege"][index])
        new_station_m = new_station * CELL_M
        old = payload["routes"][name]
        old_coords = np.asarray(old["coords_map"], dtype=np.float64)
        old_station = np.asarray(old["station_m"], dtype=np.float64)
        old_line = LineString(old_coords)
        # Project each candidate support to the unchanged p3d18 axis. This
        # preserves p3d18 heights on every unchanged downstream section.
        projected_old_station = np.asarray([
            old_line.project(Point(float(p[0]), float(p[1])))
            for p in new_coords
        ], dtype=np.float64) * CELL_M
        for key in ("source_h_m", "solution_h_m"):
            values = np.asarray(old[key], dtype=np.float64)
            old_s = old_station if len(values) == len(old_station) else np.linspace(0.0, old_station[-1], len(values))
            old[key] = np.interp(projected_old_station, old_s, values).tolist()
        old["coords_map"] = new_coords.tolist()
        old["station_map_units"] = new_station.tolist()
        old["station_m"] = new_station_m.tolist()
        payload.setdefault("p3d25_start_transfer", {})[name] = {
            "height_profile_mapping": "nearest projection to p3d18/V24 route station",
            "candidate_support_count": int(len(new_coords)),
            "old_profile_station_range_m": [float(projected_old_station.min()),
                                             float(projected_old_station.max())],
            "unchanged_downstream_profile_preserved": True,
        }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_relief_sha256": hashlib.sha256(source_raw).hexdigest(),
        "base_transfer_sha256": hashlib.sha256(args.base_v24.read_bytes()).hexdigest(),
        "transfer_sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
        "transfer": str(args.out), "R8_gate_center_unrounded_map": center,
        "profiles": {name: len(payload["routes"][name]["coords_map"])
                     for name in ("rampe_2", "rampe_11")},
        "mapping": payload["p3d25_start_transfer"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
