#!/usr/bin/env python3
"""Create one deterministic source candidate changing only ramp starts 2 and 11."""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
CELL_M = 1.2
JOIN_M = 10.8
VARIANTS = {
    # p3d24 V1 contour lead-in for rampe_2; rampe_11 starts at its existing
    # 8 m station so its complete runout clears water, wall, and map edge.
    "1": {"name": "r2_v1_contour_r11_inboard_8m", "r2_shift_m": 0.0,
          "r2_shift_direction": "left", "r2_turn_deg": 45.0,
          "r11_trim_m": 8.0},
    # p3d24 V3 axial start shift for both routes; retain its south-turn lead-in.
    "2": {"name": "both_axial_shift_r2_v3_r11_inboard_8m", "r2_shift_m": 1.2,
          "r2_shift_direction": "axis", "r2_turn_deg": -45.0,
          "r11_trim_m": 8.0},
    # Retain the better p3d24-V1 start, lengthen its contour lead-in to 12 m,
    # and move the rampe_11 start 0.5 m farther inboard.
    "3": {"name": "joint_r2_v1_12m_r11_inboard_8_5m", "r2_shift_m": 0.0,
          "r2_shift_direction": "left", "r2_turn_deg": 45.0,
          "r2_join_m": 12.0, "r11_trim_m": 8.5},
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def station_map(path: np.ndarray) -> np.ndarray:
    return np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))]


def transform_r2(raw: list[list[float]], spec: dict) -> tuple[np.ndarray, dict]:
    old = np.asarray(raw, dtype=np.float64)
    station_m = station_map(old) * CELL_M
    tangent = old[1] - old[0]
    tangent /= max(float(np.linalg.norm(tangent)), 1e-12)
    left = np.array([-tangent[1], tangent[0]], dtype=np.float64)
    direction = tangent if spec["r2_shift_direction"] == "axis" else left
    turn = np.deg2rad(float(spec["r2_turn_deg"]))
    join_m = float(spec.get("r2_join_m", JOIN_M))
    new = old.copy()
    for i, s in enumerate(station_m):
        if s > join_m + 1e-9:
            continue
        u = min(max(float(s / join_m), 0.0), 1.0)
        shift = float(spec["r2_shift_m"]) * (1.0 - 3.0 * u * u + 2.0 * u * u * u)
        lead = np.tan(turn) * s * (1.0 - u) ** 2
        new[i] += (shift * direction + lead * left) / CELL_M
    displacement = np.linalg.norm((new - old) * CELL_M, axis=1)
    changed = np.flatnonzero(displacement > 1e-10)
    return new, {
        "start_before_map": old[0].tolist(), "start_after_map": new[0].tolist(),
        "start_displacement_m": float(displacement[0]),
        "max_displacement_m": float(displacement.max(initial=0.0)),
        "max_displacement_station_m": float(station_m[int(np.argmax(displacement))]),
        "changed_station_extent_m": ([float(station_m[changed[0]]), float(station_m[changed[-1]])]
                                     if len(changed) else None),
        "join_station_m": join_m,
        "old_length_m": float(station_m[-1]),
        "new_length_m": float(station_map(new)[-1] * CELL_M),
        "geometry": f"cubic offset/turn, zero derivative at the {join_m:g} m join",
    }


def trim_r11(raw: list[list[float]], trim_m: float) -> tuple[np.ndarray, dict]:
    old = np.asarray(raw, dtype=np.float64)
    stations_m = station_map(old) * CELL_M
    if not 0.0 < trim_m < 10.8 or trim_m >= float(stations_m[-1]):
        raise ValueError("rampe_11 trim must be within the first 10.8 m")
    idx = int(np.searchsorted(stations_m, trim_m, side="right"))
    start = np.asarray([
        np.interp(trim_m, stations_m, old[:, axis]) for axis in range(2)
    ])
    new = np.vstack([start, old[idx:]])
    return new, {
        "start_before_map": old[0].tolist(), "start_after_map": start.tolist(),
        "start_displacement_m": float(np.linalg.norm((start - old[0]) * CELL_M)),
        "trimmed_original_station_m": trim_m,
        "max_displacement_m": trim_m,
        "changed_station_extent_m": [0.0, trim_m],
        "old_length_m": float(stations_m[-1]),
        "new_length_m": float(stations_m[-1] - trim_m),
        "geometry": "start moved to an interpolated point on the unchanged axis; remaining axis is byte-equivalent",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=RELIEF3D / "relief_daten.json.gz")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--variant", choices=tuple(VARIANTS))
    args = ap.parse_args()
    variant = args.variant or os.environ.get("P3D25_START_VAR", "1")
    if variant not in VARIANTS:
        raise ValueError(f"P3D25_START_VAR must be one of {tuple(VARIANTS)}")
    out = args.out or Path(f"/tmp/relief_p3d25_v{variant}_source.json.gz")
    manifest_path = args.manifest or ROOT / f"codex_jobs/tools/p3d25/results/p3d25_v{variant}_manifest.json"

    source_raw = args.source.read_bytes()
    original = json.loads(gzip.decompress(source_raw))
    data = copy.deepcopy(original)
    before_paths = original["rampenwege"]
    spec = VARIANTS[variant]
    new2, info2 = transform_r2(before_paths[2], spec)
    new11, info11 = trim_r11(before_paths[11], float(spec["r11_trim_m"]))
    data["rampenwege"][2] = new2.tolist()
    data["rampenwege"][11] = new11.tolist()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(gzip.compress(payload, compresslevel=9, mtime=0))
    out_raw = out.read_bytes()
    after = json.loads(gzip.decompress(out_raw))
    changed_routes = [i for i, (a, b) in enumerate(zip(before_paths, after["rampenwege"])) if a != b]
    unchanged_fields = all(after[key] == value for key, value in original.items() if key != "rampenwege")
    if changed_routes != [2, 11] or not unchanged_fields:
        raise RuntimeError(f"Unzulässiger Quellumfang: routes={changed_routes}, other_fields={unchanged_fields}")
    # The route geometry beyond the explicit R2 join and the trimmed R11 prefix
    # is checked against the original vertices in the manifest.
    r2_join_map = float(spec.get("r2_join_m", JOIN_M)) / CELL_M
    r2_station_map = station_map(np.asarray(before_paths[2], dtype=np.float64))
    outside_r2 = np.flatnonzero(r2_station_map > r2_join_map + 1e-9)
    if not np.array_equal(new2[outside_r2], np.asarray(before_paths[2], dtype=np.float64)[outside_r2]):
        raise RuntimeError("rampe_2 points after its 10.8 m start window changed")
    r11_station_m = station_map(np.asarray(before_paths[11], dtype=np.float64)) * CELL_M
    first_kept = int(np.searchsorted(r11_station_m, spec["r11_trim_m"], side="right"))
    if not np.array_equal(new11[1:], np.asarray(before_paths[11], dtype=np.float64)[first_kept:]):
        raise RuntimeError("rampe_11 axis after its new start changed")

    manifest = {
        "tag": "p3d25", "variant": variant, "name": spec["name"],
        "input_source_sha256": sha(source_raw), "output_source_sha256": sha(out_raw),
        "source_change_scope": "rampenwege[2] and rampenwege[11] start sections only",
        "changed_route_indices": changed_routes,
        "all_nonroute_source_fields_unchanged": unchanged_fields,
        "all_other_rampenwege_semantically_unchanged": all(
            after["rampenwege"][i] == before_paths[i] for i in range(len(before_paths)) if i not in (2, 11)
        ),
        "rampe_2_after_join_unchanged": True,
        "rampe_11_after_new_start_unchanged": True,
        "variant_parameters": spec,
        "routes": {"rampe_2": info2, "rampe_11": info11},
        "output_source": str(out),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
