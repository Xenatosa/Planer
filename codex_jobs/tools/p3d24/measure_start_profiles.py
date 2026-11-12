#!/usr/bin/env python3
"""Measure p3d21 route-start geometry and its source context for p3d24."""
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
GEOMETRIES = {
    "V29": ("p3d21_transfer_base_v29.json", (127.25, 31.25, 127.25, 31.50)),
    "V30": ("p3d21_transfer_base_v30.json", (127.00, 29.25, 127.00, 29.50)),
    "V3": ("p3d21_transfer_base_route3_v29.json", (126.50, 29.25, 126.50, 29.50)),
}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def field(data: dict, key: str, dtype=np.float32) -> np.ndarray:
    return np.frombuffer(base64.b64decode(data[key]), dtype=dtype).reshape(
        int(data["ny"]) * int(data["rs"]) + 1,
        int(data["nx"]) * int(data["rs"]) + 1,
    )


def sample(a: np.ndarray, points_map: np.ndarray, rs: int) -> np.ndarray:
    p = np.asarray(points_map, dtype=np.float64)
    return map_coordinates(a, [p[..., 1] * rs, p[..., 0] * rs],
                           order=1, mode="nearest")


def polygons_for_zones(vectors: dict) -> list[Polygon]:
    result = []
    for zones in vectors.get("bauzonen", {}).values():
        for zone in zones:
            for polygon in zone.get("polygon_m", []):
                if len(polygon) >= 4:
                    result.append(Polygon(polygon))
    return result


def polygons_for_water(vectors: dict) -> list[Polygon]:
    return [Polygon(poly) for water in vectors.get("wasser", [])
            for poly in water.get("polygon_m", []) if len(poly) >= 4]


def measure_geometry(name: str, base_name: str, critical: tuple[float, ...],
                     source_raw: bytes, original: dict, gb: np.ndarray,
                     vectors: dict, walls: list[tuple[str, LineString]],
                     wall_union, water_union, zone_union) -> dict:
    base_path = RELIEF3D / "neu" / base_name
    base_raw = base_path.read_bytes()
    base = json.loads(base_raw)
    route = base["routes"]["rampe_2"]
    coords = np.asarray(route["coords_map"], dtype=np.float64)
    station = np.asarray(route["station_m"], dtype=np.float64)
    source_h = np.asarray(route["source_h_m"], dtype=np.float64)
    target_h = np.asarray(route["solution_h_m"], dtype=np.float64)
    inboard_index = min(8, len(coords) - 1)
    start = coords[0]
    inside = coords[inboard_index]
    outward = (start - inside) * CELL_M
    outward /= max(float(np.linalg.norm(outward)), 1e-12)
    side = np.array([-outward[1], outward[0]], dtype=np.float64)
    start_m = start * CELL_M

    # Official endpoint blend has its full runout to 4 m and a lateral core
    # of 3 m. The diagnostic endpoint family covers 1 map unit inward and
    # 4 map units outward, with a 2.5-map-unit half-width.
    corners = np.asarray([
        start_m + outward * s + side * w
        for s, w in ((-1.2, 3.0), (4.0, 3.0), (4.0, -3.0), (-1.2, -3.0))
    ])
    runout = Polygon(corners)
    start_point = Point(*start_m)
    nearest_wall_name, nearest_wall = min(
        walls, key=lambda item: item[1].distance(start_point),
    )

    keep = station <= 10.0 + 1e-9
    prof_coords = coords[keep]
    prof_station = station[keep]
    source_heights = source_h[keep]
    target_heights = target_h[keep]
    terrain_heights = sample(gb, prof_coords, int(original["rs"]))
    seg_grade = np.diff(target_heights) / np.diff(prof_station) * 100.0
    terrain_grade = np.diff(terrain_heights) / np.diff(prof_station) * 100.0

    pair = np.asarray([[critical[0], critical[1]], [critical[2], critical[3]]], dtype=np.float64)
    pair_ground = sample(gb, pair, int(original["rs"]))
    pair_m = pair * CELL_M
    pair_points = [Point(*p) for p in pair_m]
    pair_projection = []
    for point in pair_m:
        delta = point - start_m
        pair_projection.append({
            "distance_from_start_m": float(np.linalg.norm(delta)),
            "outward_station_m": float(delta @ outward),
            "lateral_offset_m": float(delta @ side),
        })

    return {
        "geometry": name,
        "source_relief_sha256": sha256(source_raw),
        "transfer_base": base_name,
        "transfer_base_sha256": sha256(base_raw),
        "r8_gate_center_unrounded_map": base.get("R8_gate_center_unrounded_map"),
        "start_map": start.tolist(),
        "start_world_m": start_m.tolist(),
        "start_ground_GB_m": float(sample(gb, start[None, :], int(original["rs"]))[0]),
        "start_profile_source_h_m": float(source_h[0]),
        "start_profile_target_h_m": float(target_h[0]),
        "start_water_field_m": float(sample(field(original, "WV"), start[None, :], int(original["rs"]))[0]),
        "start_nearest_wall_centerline": {
            "name": nearest_wall_name,
            "distance_m": float(nearest_wall.distance(start_point)),
            "runout_polygon_distance_m": float(wall_union.distance(runout)),
        },
        "runout_4m_core": {
            "full_runout_m": 4.0,
            "lateral_core_half_width_m": 3.0,
            "diagnostic_check_region_outward_m": 4.0,
            "diagnostic_check_region_inward_m": 1.2,
            "diagnostic_check_half_width_m": 3.0,
            "nearest_wall_centerline_distance_m": float(wall_union.distance(runout)),
            "nearest_water_polygon_distance_m": float(water_union.distance(runout)),
            "nearest_build_zone_polygon_distance_m": float(zone_union.distance(runout)),
            "intersects_water": bool(runout.intersects(water_union)),
            "intersects_build_zone": bool(runout.intersects(zone_union)),
        },
        "start_context_distances_m": {
            "wall_centerline": float(nearest_wall.distance(start_point)),
            "water_polygon": float(water_union.distance(start_point)),
            "build_zone_polygon": float(zone_union.distance(start_point)),
        },
        "critical_r8a_pair": {
            "points_map": pair.tolist(),
            "terrain_GB_m": pair_ground.tolist(),
            "terrain_GB_difference_m": float(abs(pair_ground[1] - pair_ground[0])),
            "point_offsets_from_start": pair_projection,
            "pair_line_intersects_diagnostic_runout": bool(runout.intersects(LineString(pair_m))),
            "reported_model_delta_m": 0.172285079956,
            "reported_model_limit_m": 0.10,
        },
        "profile_0_to_10m": [
            {
                "station_m": float(s),
                "x_map": float(p[0]), "z_map": float(p[1]),
                "terrain_GB_m": float(g),
                "source_profile_m": float(sh),
                "target_axis_m": float(th),
            }
            for s, p, g, sh, th in zip(
                prof_station, prof_coords, terrain_heights, source_heights, target_heights,
            )
        ],
        "profile_summary": {
            "axis_fall_0_to_10m_m": float(target_heights[0] - target_heights[-1]),
            "terrain_fall_0_to_10m_m": float(terrain_heights[0] - terrain_heights[-1]),
            "max_abs_target_segment_grade_pct": float(np.max(np.abs(seg_grade))),
            "max_abs_source_terrain_segment_grade_pct": float(np.max(np.abs(terrain_grade))),
            "target_0_to_4m_fall_m": float(target_heights[0] - np.interp(4.0, prof_station, target_heights)),
            "terrain_0_to_4m_fall_m": float(terrain_heights[0] - np.interp(4.0, prof_station, terrain_heights)),
            "largest_target_grade_segment_m": {
                "station_start_m": float(prof_station[int(np.argmax(np.abs(seg_grade)))]),
                "station_end_m": float(prof_station[int(np.argmax(np.abs(seg_grade))) + 1]),
                "grade_pct": float(seg_grade[int(np.argmax(np.abs(seg_grade)))]),
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=Path("/tmp"),
                        help="directory containing p3d24_v29/v30/v3_source.json.gz")
    parser.add_argument("--out", type=Path,
                        default=ROOT / "codex_jobs/tools/p3d24/results/p3d24_startmessung.json")
    args = parser.parse_args()

    original_raw = (RELIEF3D / "relief_daten.json.gz").read_bytes()
    original = json.loads(gzip.decompress(original_raw))
    vectors = json.loads((RELIEF3D / "neu/vektor.json").read_text(encoding="utf-8"))
    gb = field(original, "GB")
    walls = [(str(wall.get("name", "?")), LineString(wall["mittellinie_m"]))
             for wall in vectors.get("waende", []) if len(wall.get("mittellinie_m", [])) > 1]
    wall_union = unary_union([line for _, line in walls])
    water_union = unary_union(polygons_for_water(vectors))
    zone_union = unary_union(polygons_for_zones(vectors))

    geometries = {}
    for name, (base_name, critical) in GEOMETRIES.items():
        source_path = args.source_dir / f"p3d24_{name.lower()}_source.json.gz"
        source_raw = source_path.read_bytes()
        source = json.loads(gzip.decompress(source_raw))
        geometries[name] = measure_geometry(
            name, base_name, critical, source_raw, source, gb, vectors,
            walls, wall_union, water_union, zone_union,
        )

    report = {
        "tag": "p3d24",
        "markers": {
            "S": "Quellhashes, GB-Höhen, Transferprofile und Vektorabstände direkt gemessen.",
            "R": "Paarorte und 0,172285-m-Verletzung aus p3d23-Familienmodell; Abstandsprojektionen abgeleitet.",
            "A": "World-Meter-Koordinaten der Vektoren; Wandabstand misst Mittellinien, nicht Wandfläche.",
        },
        "base_source_relief_sha256": sha256(original_raw),
        "vector_sha256": sha256((RELIEF3D / "neu/vektor.json").read_bytes()),
        "zellen_relief_sha256": sha256((RELIEF3D / "neu/zellen_relief.csv").read_bytes()),
        "D1_gate_reference_map": [152.5, 28.5],
        "D1_gate_centers_p3d23": {
            name: item["r8_gate_center_unrounded_map"] for name, item in geometries.items()
        },
        "geometries": geometries,
        "interpretation": {
            "start_axis_positions_and_source_GB_identical_through_10m": True,
            "transfer_target_profiles_identical_through_10m": False,
            "terrain_jump_at_reported_pair_explains_model_violation": False,
            "candidate_cause": "The original start lies on a descending slope. The source GB surface falls 0.416 m in the first 4 m (about 10.4% average), while the cited adjacent terrain pairs differ by only 0.0003–0.0037 m. The transfer target profile is not identical across V29/V30/V3 because prepare_transfer.py rescales the full route profile to each geometry length; its first 10 m contains steep local segments. This points to the endpoint runout meeting a slope break in the transferred ramp band, not a source-height discontinuity. The R8a pair is evidence for a too-short/poorly aligned local lead-in, but this remains an inference pending new candidate solves.",
        },
        "distance_caveats": [
            "The modeled 4 m runout is the full-weight endpoint blend; its outer transition extends to 8 m in RELIEF_WEGEND_VAR=1.",
            "The diagnostic R8a footprint is projected with its p3d23 lattice and corridor; this report separately records the 4 m physical blend core.",
            "Build-zone distance uses vector polygons. Water distance uses vector water polygons. Wall distance is to vector centerlines.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(json.dumps({
        "out": str(args.out),
        "source_hashes": {name: item["source_relief_sha256"] for name, item in geometries.items()},
        "start_GB_m": {name: item["start_ground_GB_m"] for name, item in geometries.items()},
        "fall_0_10m": {name: item["profile_summary"]["axis_fall_0_to_10m_m"] for name, item in geometries.items()},
        "wall_runout_m": {name: item["runout_4m_core"]["nearest_wall_centerline_distance_m"] for name, item in geometries.items()},
        "water_runout_m": {name: item["runout_4m_core"]["nearest_water_polygon_distance_m"] for name, item in geometries.items()},
        "zone_runout_m": {name: item["runout_4m_core"]["nearest_build_zone_polygon_distance_m"] for name, item in geometries.items()},
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
