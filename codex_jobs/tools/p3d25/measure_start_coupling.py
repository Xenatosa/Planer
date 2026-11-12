#!/usr/bin/env python3
"""Measure both p3d18/V24 start areas and the p3d24 R8a pair locations."""
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
PAIRS = {
    "p3d24_v1_rampe_11": ([148.0, 2.25], [148.0, 2.5]),
    "p3d24_v1_endpoint_only_rampe_2": ([128.0, 30.25], [128.0, 30.5]),
    "p3d24_v3_rampe_11": ([147.5, 2.5], [147.5, 2.75]),
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def decoded(data: dict, key: str) -> np.ndarray:
    return np.frombuffer(base64.b64decode(data[key]), dtype=np.float32).reshape(
        int(data["ny"]) * int(data["rs"]) + 1,
        int(data["nx"]) * int(data["rs"]) + 1,
    )


def sample(field: np.ndarray, points: np.ndarray, rs: int) -> np.ndarray:
    p = np.asarray(points, dtype=np.float64)
    return map_coordinates(field, [p[..., 1] * rs, p[..., 0] * rs],
                           order=1, mode="nearest", prefilter=False)


def polygons_for_zones(vectors: dict) -> list[Polygon]:
    return [Polygon(poly) for items in vectors.get("bauzonen", {}).values()
            for zone in items for poly in zone.get("polygon_m", []) if len(poly) >= 4]


def polygons_for_water(vectors: dict) -> list[Polygon]:
    return [Polygon(poly) for item in vectors.get("wasser", [])
            for poly in item.get("polygon_m", []) if len(poly) >= 4]


def route_context(name: str, route: dict, gb: np.ndarray, rs: int,
                  walls: list[tuple[str, LineString]], wall_union,
                  water_union, zone_union, nx: int, ny: int) -> dict:
    coords = np.asarray(route["coords_map"], dtype=np.float64)
    stations = np.asarray(route["station_m"], dtype=np.float64)
    source_h = np.asarray(route["source_h_m"], dtype=np.float64)
    target_h = np.asarray(route["solution_h_m"], dtype=np.float64)
    endpoint, inside = coords[0], coords[min(8, len(coords) - 1)]
    outward = endpoint - inside
    outward /= max(float(np.linalg.norm(outward)), 1e-12)
    side = np.array([-outward[1], outward[0]], dtype=np.float64)
    endpoint_m = endpoint * CELL_M
    footprint = Polygon(np.asarray([
        endpoint_m + outward * along + side * lateral
        for along, lateral in ((-1.2, 3.0), (4.0, 3.0),
                               (4.0, -3.0), (-1.2, -3.0))
    ]))
    endpoint_point = Point(*endpoint_m)
    nearest_wall_name, nearest_wall = min(
        walls, key=lambda item: item[1].distance(endpoint_point),
    )
    keep = stations <= 10.0 + 1e-9
    prof_coords, prof_station = coords[keep], stations[keep]
    terrain = sample(gb, prof_coords, rs)
    target = target_h[keep]
    source = source_h[keep]
    grade = np.diff(target) / np.diff(prof_station) * 100.0
    profile = [{
        "station_m": float(s), "coord_map": p.tolist(),
        "terrain_GB_m": float(g), "source_profile_m": float(sh),
        "V24_target_axis_m": float(th),
    } for s, p, g, sh, th in zip(prof_station, prof_coords, terrain, source, target)]
    along_end = float(np.interp(4.0, stations, target_h))
    terrain_4 = float(np.interp(4.0, prof_station, terrain))
    return {
        "route": name,
        "start_map": endpoint.tolist(),
        "start_world_m": endpoint_m.tolist(),
        "first_interior_sample_map": inside.tolist(),
        "outward_unit_map": outward.tolist(),
        "start_GB_m": float(sample(gb, endpoint[None, :], rs)[0]),
        "start_source_profile_m": float(source_h[0]),
        "start_V24_axis_m": float(target_h[0]),
        "start_nearest_wall_centerline": {
            "name": nearest_wall_name,
            "distance_m": float(nearest_wall.distance(endpoint_point)),
        },
        "start_distance_m": {
            "wall_centerline": float(nearest_wall.distance(endpoint_point)),
            "water_polygon": float(water_union.distance(endpoint_point)),
            "build_zone_polygon": float(zone_union.distance(endpoint_point)),
        },
        "runout_4m_context": {
            "along_extent_m": [-1.2, 4.0], "half_width_m": 3.0,
            "map_edge_clearance_m": float(min(
                footprint.bounds[0], footprint.bounds[1],
                nx * CELL_M - footprint.bounds[2], ny * CELL_M - footprint.bounds[3],
            )),
            "wall_centerline_distance_m": float(wall_union.distance(footprint)),
            "water_polygon_distance_m": float(water_union.distance(footprint)),
            "build_zone_polygon_distance_m": float(zone_union.distance(footprint)),
            "intersects_water": bool(footprint.intersects(water_union)),
            "intersects_build_zone": bool(footprint.intersects(zone_union)),
            "outside_map": bool(footprint.bounds[0] < 0 or footprint.bounds[1] < 0
                                 or footprint.bounds[2] > nx * CELL_M
                                 or footprint.bounds[3] > ny * CELL_M),
        },
        "profile_summary_0_to_10m": {
            "terrain_fall_0_to_4m_m": float(terrain[0] - terrain_4),
            "axis_fall_0_to_4m_m": float(target_h[0] - along_end),
            "terrain_fall_0_to_10m_m": float(terrain[0] - terrain[-1]),
            "axis_fall_0_to_10m_m": float(target_h[0] - target[-1]),
            "max_abs_axis_grade_pct": float(np.max(np.abs(grade))),
            "max_axis_grade_station_m": float(prof_station[int(np.argmax(np.abs(grade)))]),
        },
        "profile_0_to_10m": profile,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=RELIEF3D / "relief_daten.json.gz")
    ap.add_argument("--transfer", type=Path, default=RELIEF3D / "neu/p3d18_joint_mesh_v24.json")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "codex_jobs/tools/p3d25/results/p3d25_startmessung.json")
    args = ap.parse_args()
    source_raw = args.source.read_bytes()
    data = json.loads(gzip.decompress(source_raw))
    transfer_raw = args.transfer.read_bytes()
    transfer = json.loads(transfer_raw)
    vector_path = RELIEF3D / "neu/vektor.json"
    vector_raw = vector_path.read_bytes()
    vectors = json.loads(vector_raw)
    gb = decoded(data, "GB")
    rs, nx, ny = int(data["rs"]), int(data["nx"]), int(data["ny"])
    walls = [(str(w.get("name", "?")), LineString(w["mittellinie_m"]))
             for w in vectors.get("waende", []) if len(w.get("mittellinie_m", [])) > 1]
    wall_union = unary_union([line for _, line in walls])
    water_union = unary_union(polygons_for_water(vectors))
    zone_union = unary_union(polygons_for_zones(vectors))
    routes = {name: route_context(name, transfer["routes"][name], gb, rs,
                                  walls, wall_union, water_union, zone_union,
                                  nx, ny)
              for name in ("rampe_2", "rampe_11")}
    pairs = {}
    for label, (a, b) in PAIRS.items():
        pts = np.asarray([a, b], dtype=np.float64)
        heights = sample(gb, pts, rs)
        pairs[label] = {
            "points_map": [a, b],
            "distance_m": float(np.linalg.norm((pts[1] - pts[0]) * CELL_M)),
            "source_GB_m": heights.tolist(),
            "source_GB_delta_m": float(abs(heights[1] - heights[0])),
            "endpoint_distance_m": {
                "rampe_2": float(np.min(np.linalg.norm((pts[:, None, :] -
                    np.asarray(transfer["routes"]["rampe_2"]["coords_map"])[None, :, :]) * CELL_M, axis=2))),
                "rampe_11": float(np.min(np.linalg.norm((pts[:, None, :] -
                    np.asarray(transfer["routes"]["rampe_11"]["coords_map"])[None, :, :]) * CELL_M, axis=2))),
            },
        }
    result = {
        "tag": "p3d25",
        "markers": {
            "S": "Quellhashes, V24-Profile, GB-Hoehen und Vektorabstaende direkt ausgelesen.",
            "R": "Profilfaelle, Footprint-Abstaende und Modellkopplung aus den Messwerten und dem p3d23-Modell abgeleitet.",
            "A": "Der rechteckige 4-m-Auslauf-Footprint bildet den vollen Gewichtskern mit 3-m-Halbbreite und 1.2-m-Innenbereich ab.",
        },
        "source_relief_sha256": sha(source_raw),
        "transfer_sha256": sha(transfer_raw),
        "vektor_sha256": sha(vector_raw),
        "zellen_relief_sha256": sha((RELIEF3D / "neu/zellen_relief.csv").read_bytes()),
        "routes": routes,
        "reported_p3d24_R8a_pairs_source_GB": pairs,
        "coupling": {
            "shared_model_surface": "One D1 surface raster and one endpoint_r8a_extra_m slack variable cover both route starts.",
            "shared_non_endpoint_constraints": "Both starts are represented in the joint solve alongside the same R3, crossing, plane-core, route-grade, variable-bound, and event-cut families.",
            "spatial_note": "The two starts are separated spatially; the evidence does not indicate shared local raster cells or a direct local terrain constraint between them. Their model coupling is through the joint model and global family slack/feasibility, not physical adjacency.",
            "pair_scope": "The endpoint family adds a start-runout pair set specifically for routes 2 and 11, plus the shared D1 endpoint pairs.",
        },
        "distance_caveat": "Wall distances are to vector centerlines, not generated wall faces; build-zone and water distances use vector polygons.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(args.out), "source_relief_sha256": result["source_relief_sha256"],
                      "routes": {k: {"start_map": v["start_map"], "start_GB_m": v["start_GB_m"],
                                    "start_distance_m": v["start_distance_m"],
                                    "runout_4m_context": v["runout_4m_context"],
                                    "profile_summary_0_to_10m": v["profile_summary_0_to_10m"]}
                                 for k, v in routes.items()},
                      "pairs": pairs}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
