#!/usr/bin/env python3
"""Measure the unchanged p3d18/V24 D1 ramp geometry before p3d21 edits."""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.ndimage import map_coordinates
from shapely.geometry import LineString, Point

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
if str(RELIEF3D) not in sys.path:
    sys.path.insert(0, str(RELIEF3D))
from neu.mesh import TILE_BOUNDS, build_manifest

CELL_M = 1.2
R8_CENTER_MAP = np.array([152.54985704503775, 28.48954534572434])
TURN_STATIONS_M = (9.6, 28.5, 47.4)
ERRORS = {
    "G5_161.4_28.1": (161.4, 28.1),
    "G5_159.5_28.5": (159.5, 28.5),
    "G5_158.2_30.6": (158.2, 30.6),
    "R5_158.0_17.5": (158.0, 17.5),
    "R4_143.1_29.6": (143.1, 29.6),
}


def line_at_station(route: dict, station_m: float) -> np.ndarray:
    s = np.asarray(route["station_m"], dtype=np.float64)
    p = np.asarray(route["coords_map"], dtype=np.float64)
    return np.array([np.interp(station_m, s, p[:, i]) for i in range(2)])


def sample_surface(surface: np.ndarray, points_map: np.ndarray, x0: int, z0: int, rs: int) -> np.ndarray:
    p = np.asarray(points_map, dtype=np.float64)
    rows = (p[..., 1] - z0) * rs
    cols = (p[..., 0] - x0) * rs
    return map_coordinates(surface, [rows, cols], order=1, mode="nearest")


def build() -> dict:
    solution_path = RELIEF3D / "neu/p3d18_joint_mesh_v24.json"
    source_path = RELIEF3D / "relief_daten.json.gz"
    vector_path = RELIEF3D / "neu/vektor.json"
    solution = json.loads(solution_path.read_text(encoding="utf-8"))
    source_bytes = source_path.read_bytes()
    source = json.loads(gzip.decompress(source_bytes))
    vector = json.loads(vector_path.read_text(encoding="utf-8"))

    # Recreate the unchanged V24 transfer in memory so R8-window profiles are
    # measurements of the emitted p3d18 geometry, not a replacement formula.
    manifest = build_manifest(
        source_path, RELIEF3D / "neu/zellen_relief.csv", vector_path,
        RELIEF3D / "neu/felder.npz", variant="2",
    )
    tile = manifest["tiles"]["D1"]
    positions = np.frombuffer(base64.b64decode(tile["vertices_xyz_f32"]), dtype="<f4").reshape(-1, 3)
    x0, z0, x1, z1 = TILE_BOUNDS["D1"]
    rs = int(tile["samples_per_m"])
    surface = positions[:, 1].reshape((int((z1-z0)*rs+1), int((x1-x0)*rs+1))).astype(np.float64)
    center_m = R8_CENTER_MAP * CELL_M

    routes: dict[str, dict] = solution["routes"]
    lines = {name: LineString(np.asarray(routes[name]["coords_map"], dtype=np.float64) * CELL_M)
             for name in ("rampe_11", "rampe_2")}
    crossing = lines["rampe_11"].intersection(lines["rampe_2"])
    crossing_points = []
    if crossing.geom_type == "Point":
        crossing_points = [[float(crossing.x / CELL_M), float(crossing.y / CELL_M)]]
    elif crossing.geom_type == "MultiPoint":
        crossing_points = [[float(p.x / CELL_M), float(p.y / CELL_M)] for p in crossing.geoms]

    route_results = {}
    for name in ("rampe_11", "rampe_2"):
        route = routes[name]
        p = np.asarray(route["coords_map"], dtype=np.float64)
        stations = np.asarray(route["station_m"], dtype=np.float64)
        source_h = np.asarray(route["source_h_m"], dtype=np.float64)
        target_h = np.asarray(route["solution_h_m"], dtype=np.float64)
        line = lines[name]
        r8_station_m = float(line.project(Point(*center_m)))
        r8_nearest_map = np.asarray(line.interpolate(r8_station_m).coords[0]) / CELL_M
        window = (stations >= r8_station_m - 6.0) & (stations <= r8_station_m + 6.0)
        win_s = stations[window]
        win_h = target_h[window]
        segment_grade = np.diff(win_h) / np.diff(win_s) * 100.0
        # Cross-profile at the R8 center and throughout its +/-6 m road window.
        win_p = p[window]
        tangents = np.gradient(win_p * CELL_M, axis=0)
        tangents /= np.maximum(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-12)
        normals = np.column_stack((-tangents[:, 1], tangents[:, 0]))
        cross_results = {}
        for offset_m in (1.5, 4.0):
            plus = win_p + normals * (offset_m / CELL_M)
            minus = win_p - normals * (offset_m / CELL_M)
            hp = sample_surface(surface, plus, x0, z0, rs)
            hm = sample_surface(surface, minus, x0, z0, rs)
            slope = (hp - hm) / (2.0 * offset_m) * 100.0
            cross_results[str(offset_m)] = {
                "mean_abs_pct": float(np.mean(np.abs(slope))),
                "max_abs_pct": float(np.max(np.abs(slope))),
                "at_r8_center_pct": float(slope[np.argmin(np.abs(win_s-r8_station_m))]),
                "elevations_at_r8_center_m": [float(hm[np.argmin(np.abs(win_s-r8_station_m))]),
                                               float(hp[np.argmin(np.abs(win_s-r8_station_m))])],
            }
        route_results[name] = {
            "coordinate_samples": len(p),
            "length_m": float(stations[-1]),
            "start_map": p[0].tolist(), "end_map": p[-1].tolist(),
            "start_elevation_m": float(source_h[0]),
            "end_elevation_m": float(source_h[-1]),
            "fall_m": float(source_h[0] - source_h[-1]),
            "mean_grade_pct": float((source_h[0] - source_h[-1]) / stations[-1] * 100.0),
            "r8_center_station_m": r8_station_m,
            "r8_center_nearest_map": r8_nearest_map.tolist(),
            "r8_center_distance_m": float(line.distance(Point(*center_m))),
            "r8_window_station_m": [float(win_s[0]), float(win_s[-1])],
            "r8_window_source_elevation_m": [float(source_h[window][0]), float(source_h[window][-1])],
            "r8_window_transferred_elevation_m": [float(win_h[0]), float(win_h[-1])],
            "r8_window_mean_grade_pct": float((win_h[-1]-win_h[0])/(win_s[-1]-win_s[0])*100),
            "r8_window_max_abs_segment_grade_pct": float(np.max(np.abs(segment_grade))),
            "r8_window_transverse_profiles": cross_results,
        }
        if name == "rampe_11":
            turns = []
            for station in TURN_STATIONS_M:
                q = line_at_station(route, station)
                q_m = q * CELL_M
                d = float(np.linalg.norm(q_m-center_m))
                turns.append({
                    "station_m": station, "coord_map": q.tolist(),
                    "distance_to_R8_center_m": d,
                    "distance_outside_2m_core_m": d - 2.0,
                    "distance_outside_4m_transition_m": d - 4.0,
                })
            route_results[name]["turns"] = turns

    walls = []
    for wall in vector.get("waende", []):
        points = np.asarray(wall.get("mittellinie_m", []), dtype=np.float64)
        if len(points) > 1:
            walls.append((wall.get("name", "?"), LineString(points)))
    residuals = {}
    for name, coord in ERRORS.items():
        point_map = Point(*coord)
        point_m = Point(*(np.asarray(coord) * CELL_M))
        residuals[name] = {
            "coord_map": list(coord),
            "axes": {
                route_name: {
                    "distance_m": float(LineString(np.asarray(routes[route_name]["coords_map"]) * CELL_M).distance(point_m)),
                    "station_m": float(LineString(np.asarray(routes[route_name]["coords_map"]) * CELL_M).project(point_m)),
                }
                for route_name in ("rampe_2", "rampe_11")
            },
            "nearest_wall_centerline": min(
                ({"name": wall_name,
                  "distance_m": float(wall_line.distance(point_m))}
                 for wall_name, wall_line in walls),
                key=lambda item: item["distance_m"],
            ),
        }

    return {
        "label": "[S] geometry from p3d18 V24 source and unchanged relief; [R] derived distances/profiles",
        "source_relief_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "vektor_json_sha256": hashlib.sha256(vector_path.read_bytes()).hexdigest(),
        "v24_json_sha256": hashlib.sha256(solution_path.read_bytes()).hexdigest(),
        "r8_gate_center_map": R8_CENTER_MAP.tolist(),
        "route_intersections_map": crossing_points,
        "routes": route_results,
        "residuals": residuals,
        "distance_caveat": "Wall distance is to the existing vector wall centerline; it is not the distance to a regenerated wall face.",
    }


if __name__ == "__main__":
    result = build()
    out = RELIEF3D / "pruefung/messung_p3d21_v24.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
