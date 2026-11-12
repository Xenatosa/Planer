#!/usr/bin/env python3
"""Measure a p3d24 candidate start against source terrain and nearby features."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.ndimage import map_coordinates
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
CELL_M = 1.2


def sample(field: np.ndarray, xy: np.ndarray, rs: int) -> np.ndarray:
    p = np.asarray(xy, dtype=np.float64)
    return map_coordinates(field, [p[..., 1] * rs, p[..., 0] * rs],
                           order=1, mode="nearest")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("1", "2", "3"), required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--transfer", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    source_raw = args.source.read_bytes()
    data = json.loads(gzip.decompress(source_raw))
    rs = int(data["rs"])
    gb = np.frombuffer(base64.b64decode(data["GB"]), dtype=np.float32).reshape(
        int(data["ny"]) * rs + 1, int(data["nx"]) * rs + 1,
    )
    vectors = json.loads((RELIEF3D / "neu/vektor.json").read_text(encoding="utf-8"))
    transfer_raw = args.transfer.read_bytes()
    transfer = json.loads(transfer_raw)
    route = transfer["routes"]["rampe_2"]
    coords = np.asarray(route["coords_map"], dtype=np.float64)
    station = np.asarray(route["station_m"], dtype=np.float64)
    source_h = np.asarray(route["source_h_m"], dtype=np.float64)
    target_h = np.asarray(route["solution_h_m"], dtype=np.float64)
    start = coords[0]
    start_m = start * CELL_M
    inside = coords[min(8, len(coords) - 1)]
    outward = start - inside
    outward /= max(float(np.linalg.norm(outward)), 1e-12)
    side = np.array([-outward[1], outward[0]])
    corners = np.asarray([
        start_m + outward * s + side * w
        for s, w in ((-1.2, 3.0), (4.0, 3.0), (4.0, -3.0), (-1.2, -3.0))
    ])
    runout = Polygon(corners)
    point = Point(*start_m)

    walls = [(str(w.get("name", "?")), LineString(w["mittellinie_m"]))
             for w in vectors.get("waende", []) if len(w.get("mittellinie_m", [])) > 1]
    nearest_wall_name, nearest_wall = min(walls, key=lambda item: item[1].distance(point))
    wall_union = unary_union([line for _, line in walls])
    water_union = unary_union([
        Polygon(poly) for water in vectors.get("wasser", [])
        for poly in water.get("polygon_m", []) if len(poly) >= 4
    ])
    zone_union = unary_union([
        Polygon(poly) for zones in vectors.get("bauzonen", {}).values()
        for zone in zones for poly in zone.get("polygon_m", []) if len(poly) >= 4
    ])
    profile = []
    keep = station <= 10.0 + 1e-9
    terrain = sample(gb, coords[keep], rs)
    seg_grade = np.diff(target_h[keep]) / np.diff(station[keep]) * 100.0
    for s, xy, ground, source_y, target_y in zip(
        station[keep], coords[keep], terrain, source_h[keep], target_h[keep],
    ):
        profile.append({
            "station_m": float(s), "coord_map": xy.tolist(),
            "terrain_GB_m": float(ground), "source_profile_m": float(source_y),
            "target_axis_m": float(target_y),
        })

    result = {
        "variant": args.variant,
        "source_relief_sha256": hashlib.sha256(source_raw).hexdigest(),
        "transfer_base_sha256": hashlib.sha256(transfer_raw).hexdigest(),
        "start_map": start.tolist(), "start_world_m": start_m.tolist(),
        "start_ground_GB_m": float(sample(gb, start[None, :], rs)[0]),
        "start_profile_source_m": float(source_h[0]),
        "start_profile_target_m": float(target_h[0]),
        "start_distances_m": {
            "nearest_wall_centerline": {"name": nearest_wall_name,
                                         "distance_m": float(nearest_wall.distance(point))},
            "water_polygon": float(water_union.distance(point)),
            "build_zone_polygon": float(zone_union.distance(point)),
        },
        "runout_4m_context": {
            "nearest_wall_centerline": float(wall_union.distance(runout)),
            "water_polygon": float(water_union.distance(runout)),
            "build_zone_polygon": float(zone_union.distance(runout)),
            "intersects_water": bool(runout.intersects(water_union)),
            "intersects_build_zone": bool(runout.intersects(zone_union)),
        },
        "profile_summary": {
            "axis_fall_0_to_4m_m": float(target_h[0] - np.interp(4.0, station, target_h)),
            "terrain_fall_0_to_4m_m": float(terrain[0] - np.interp(4.0, station[keep], terrain)),
            "axis_fall_0_to_10m_m": float(target_h[0] - np.interp(10.0, station, target_h)),
            "max_abs_target_segment_grade_pct_0_to_10m": float(np.max(np.abs(seg_grade))),
        },
        "profile_0_to_10m": profile,
        "distance_notes": [
            "Wall distance is to vector centerlines, not wall faces.",
            "The footprint includes 1.2 m inward and 4 m outward along the endpoint tangent with 3 m half-width.",
            "The mesh uses a 4 m full-weight runout and an 8 m outer transition for RELIEF_WEGEND_VAR=1.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(json.dumps({
        "out": str(args.out), "variant": args.variant,
        "start_map": result["start_map"], "start_GB_m": result["start_ground_GB_m"],
        "start_distances_m": result["start_distances_m"],
        "runout_4m_context": result["runout_4m_context"],
        "profile_summary": result["profile_summary"],
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
