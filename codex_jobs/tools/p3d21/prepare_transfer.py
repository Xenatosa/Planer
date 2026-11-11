#!/usr/bin/env python3
"""Rebind the p3d18/V24 raster transfer to one measured local route variant."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
CELL_M = 1.2


def sample_profile(raw: list[list[float]]) -> tuple[np.ndarray, np.ndarray]:
    path = np.asarray(raw, dtype=np.float64)
    cumulative = np.r_[0.0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))]
    station = np.arange(0.0, cumulative[-1] + 1e-7, 0.25)
    coords = np.column_stack((
        np.interp(station, cumulative, path[:, 0]),
        np.interp(station, cumulative, path[:, 1]),
    ))
    return station, coords


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--base-v24", type=Path, default=RELIEF3D / "neu/p3d18_joint_mesh_v24.json")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--r8-center", type=float, nargs=2, required=True)
    args = ap.parse_args()
    raw_source = args.source.read_bytes()
    data = json.loads(gzip.decompress(raw_source))
    source_hash = hashlib.sha256(raw_source).hexdigest()
    payload = json.loads(args.base_v24.read_text(encoding="utf-8"))
    payload["source_relief_sha256"] = source_hash
    payload["R8_gate_center_unrounded_map"] = list(args.r8_center)

    for index in (2, 11):
        name = f"rampe_{index}"
        station, coords = sample_profile(data["rampenwege"][index])
        old = payload["routes"][name]
        old_station = np.asarray(old.get("station_m", []), dtype=np.float64)
        if not len(old_station):
            old_station = np.arange(len(old["solution_h_m"]), dtype=np.float64) * 0.30
        for key in ("source_h_m", "solution_h_m"):
            values = np.asarray(old[key], dtype=np.float64)
            old_station_for_key = old_station
            if len(values) != len(old_station_for_key):
                old_station_for_key = np.linspace(0.0, float(old_station[-1]), len(values))
            target_station_m = station * CELL_M
            # Keep the p3d18 height profile endpoint-to-endpoint while the
            # route's local lateral shift changes its total arclength.
            profile_station = target_station_m * (old_station_for_key[-1] / target_station_m[-1])
            old[key] = np.interp(profile_station, old_station_for_key, values).tolist()
        old["coords_map"] = coords.tolist()
        old["station_map_units"] = station.tolist()
        old["station_m"] = (station * CELL_M).tolist()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_sha256": source_hash,
        "base_transfer_sha256": hashlib.sha256(args.base_v24.read_bytes()).hexdigest(),
        "output": str(args.out),
        "r8_gate_center_unrounded_map": list(args.r8_center),
        "profiles": {name: len(payload["routes"][name]["coords_map"]) for name in ("rampe_2", "rampe_11")},
        "surface_grid_reused_from": str(args.base_v24),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
