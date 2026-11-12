#!/usr/bin/env python3
"""Change only the first <=12 m of the V3 rampe_2 axis for p3d24 probes."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import copy
from pathlib import Path

import numpy as np
from shapely.geometry import LineString

CELL_M = 1.2
JOIN_M = 10.8
VARIANTS = {
    # Keep the start fixed. Rotate the tangent 45 degrees toward the contour,
    # then ease back to the V3 axis before 10.8 m.
    "1": {"name": "same_start_contour_leadin", "start_shift_m": 0.0,
          "initial_turn_deg": 45.0, "join_m": JOIN_M},
    # Move the start 1.2 m to the left of the V3 axis, keeping its tangent,
    # then rejoin smoothly before 10.8 m.
    "2": {"name": "left_contour_shift", "start_shift_m": 1.2,
          "initial_turn_deg": 0.0, "join_m": JOIN_M},
    # Move 1.2 m down the original axis, then turn the lead-in 45 degrees
    # toward the south side and rejoin smoothly before 10.8 m.
    "3": {"name": "axis_shift_plus_flatter_leadin", "start_shift_m": 1.2,
          "start_shift_direction": "axis", "initial_turn_deg": -45.0,
          "join_m": JOIN_M},
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def route_station(path: np.ndarray) -> np.ndarray:
    return np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1) * CELL_M)]


def apply(raw_path: list[list[float]], variant: dict) -> tuple[np.ndarray, dict]:
    old = np.asarray(raw_path, dtype=np.float64)
    station = route_station(old)
    join = float(variant["join_m"])
    tangent = old[1] - old[0]
    tangent /= max(float(np.linalg.norm(tangent)), 1e-12)
    left = np.array([-tangent[1], tangent[0]], dtype=np.float64)
    shift_direction_name = str(variant.get("start_shift_direction", "left"))
    if shift_direction_name == "left":
        shift_direction = left
    elif shift_direction_name == "axis":
        shift_direction = tangent
    else:
        raise ValueError(f"Unbekannte Startverschieberichtung: {shift_direction_name}")
    turn = np.deg2rad(float(variant["initial_turn_deg"]))
    start_shift = float(variant["start_shift_m"])

    new = old.copy()
    for i, s in enumerate(station):
        if s > join + 1e-9:
            continue
        u = min(max(float(s / join), 0.0), 1.0)
        shift = start_shift * (1.0 - 3.0 * u * u + 2.0 * u * u * u)
        lead = np.tan(turn) * s * (1.0 - u) ** 2
        new[i] += (shift * shift_direction + lead * left) / CELL_M

    new_station = route_station(new)
    changed = np.linalg.norm((new - old) * CELL_M, axis=1) > 1e-10
    info = {
        "name": variant["name"],
        "join_station_original_m": join,
        "start_shift_m": start_shift,
        "start_shift_direction": shift_direction_name,
        "initial_turn_deg": float(variant["initial_turn_deg"]),
        "start_before_map": old[0].tolist(),
        "start_after_map": new[0].tolist(),
        "start_displacement_m": float(np.linalg.norm((new[0] - old[0]) * CELL_M)),
        "first_10_8m_axis_length_before_m": float(station[np.searchsorted(station, join)]),
        "first_10_8m_axis_length_after_m": float(new_station[np.searchsorted(station, join)]),
        "max_displacement_m": float(np.max(np.linalg.norm((new - old) * CELL_M, axis=1))),
        "max_displacement_station_m": float(station[int(np.argmax(np.linalg.norm((new - old) * CELL_M, axis=1)))]),
        "changed_vertex_count": int(changed.sum()),
        "changed_station_extent_m": [float(station[np.flatnonzero(changed)[0]]),
                                     float(station[np.flatnonzero(changed)[-1]])],
        "changed_vertices": [
            {
                "station_before_m": float(station[i]),
                "before_map": old[i].tolist(),
                "after_map": new[i].tolist(),
                "displacement_m": float(np.linalg.norm((new[i] - old[i]) * CELL_M)),
            }
            for i in np.flatnonzero(changed)
        ],
        "old_first_10_8m_length_m": float(LineString(old[station <= join + 1e-9]).length * CELL_M),
        "new_first_10_8m_length_m": float(LineString(new[station <= join + 1e-9]).length * CELL_M),
        "old_full_length_m": float(station[-1]),
        "new_full_length_m": float(new_station[-1]),
    }
    return new, info


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="V3 source relief from apply_route_variant.py --variant 3")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--variant", choices=sorted(VARIANTS), default=None)
    args = parser.parse_args()
    variant = args.variant or os.environ.get("P3D24_START_VAR", "1")
    if variant not in VARIANTS:
        raise ValueError(f"P3D24_START_VAR muss einer von {sorted(VARIANTS)} sein")

    source_raw = args.source.read_bytes()
    data = json.loads(gzip.decompress(source_raw))
    original_data = copy.deepcopy(data)
    before_paths = original_data["rampenwege"]
    old_route2 = before_paths[2]
    new_route2, changes = apply(old_route2, VARIANTS[variant])
    data["rampenwege"][2] = new_route2.tolist()
    out_raw = gzip.compress(json.dumps(data, ensure_ascii=False).encode("utf-8"),
                            compresslevel=9, mtime=0)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(out_raw)

    after = json.loads(gzip.decompress(out_raw))
    unchanged = [i for i in range(len(before_paths)) if i != 2]
    report = {
        "tag": "p3d24", "variant": variant, "variant_name": VARIANTS[variant]["name"],
        "input_source_sha256": digest(source_raw), "output_source_sha256": digest(out_raw),
        "source_change_scope": "rampenwege[2] only",
        "other_rampenwege_semantically_unchanged": all(
            after["rampenwege"][i] == before_paths[i] for i in unchanged
        ),
        "rampe_11_unchanged": after["rampenwege"][11] == before_paths[11],
        "all_other_source_fields_unchanged": all(
            after[key] == value for key, value in original_data.items() if key != "rampenwege"
        ),
        "rampenwege_other_than_2_unchanged": all(
            after["rampenwege"][i] == before_paths[i] for i in unchanged
        ),
        "rampe_2": changes,
        "output_source": str(args.out),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
