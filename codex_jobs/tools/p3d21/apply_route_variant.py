#!/usr/bin/env python3
"""Create a local p3d21 candidate by changing only rampenwege[2] and [11]."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
CELL_M = 1.2
R8_OLD_CENTER = np.array([152.54985704503775, 28.48954534572434])

# Local perpendicular offsets in metres. Signs are relative to the path's
# left normal in map coordinates (x,z). Widths are Gaussian sigma in metres.
VARIANTS = {
    "29": {
        "rampe_2": [(20.055, 2.4, 3.0, 1.0), (40.0, 2.1, 3.6, -1.0)],
        "rampe_11": [(28.0, 1.8, 4.5, 1.0)],
    },
    "30": {
        # Smaller, broader offsets keep the crossing and adjacent route pairs
        # close to V24 while moving each measured residual off the centerline.
        "rampe_2": [(20.055, 1.0, 3.0, 1.0), (40.0, 1.0, 4.0, -1.0)],
        "rampe_11": [(28.0, 1.0, 5.0, 1.0)],
    },
    "3": {
        # Third and final route geometry: keep rampe_11 fixed and use the
        # smallest local changes on rampe_2 while retaining transfer V29.
        "rampe_2": [(20.055, 0.6, 4.0, 1.0), (40.0, 0.6, 4.5, -1.0)],
        "rampe_11": [],
    },
}


def sample_path(raw: list[list[float]], step: float = 0.25) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(raw, dtype=np.float64)
    length = np.r_[0.0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    t = np.arange(0.0, length[-1] + 1e-6, step)
    return np.column_stack((np.interp(t, length, p[:, 0]), np.interp(t, length, p[:, 1]))), t


def deform(raw: list[list[float]], features: list[tuple[float, float, float, float]]) -> np.ndarray:
    p = np.asarray(raw, dtype=np.float64)
    map_station = np.r_[0.0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    station_m = map_station * CELL_M
    delta_m = np.zeros_like(p)
    for center_m, amplitude_m, sigma_m, sign in features:
        station_map = center_m / CELL_M
        target = np.array([np.interp(station_map, map_station, p[:, axis]) for axis in range(2)])
        before = np.array([np.interp(max(0.0, station_map - 0.25), map_station, p[:, axis]) for axis in range(2)])
        after = np.array([np.interp(min(map_station[-1], station_map + 0.25), map_station, p[:, axis]) for axis in range(2)])
        tangent = (after - before) * CELL_M
        tangent /= max(float(np.hypot(*tangent)), 1e-12)
        normal = np.array([-tangent[1], tangent[0]])
        weight = np.exp(-0.5 * ((station_m - center_m) / sigma_m) ** 2)
        delta_m += (sign * amplitude_m * weight)[:, None] * normal[None, :]
    return (p * CELL_M + delta_m) / CELL_M


def official_crossing_center(data: dict, paths: list[list[list[float]]]) -> list[float]:
    """Reproduce r8_kreuzung.py's event-centre calculation for rampe_2x11."""
    nx, ny, rs = int(data["nx"]), int(data["ny"]), int(data["rs"])
    sampled = [sample_path(path) for path in paths]
    P = np.concatenate([item[0] for item in sampled])
    RI = np.concatenate([np.full(len(item[0]), i, dtype=np.int32) for i, item in enumerate(sampled)])
    LL = np.concatenate([item[1] for item in sampled])
    pairs = cKDTree(P).query_pairs(6.0, output_type="ndarray")
    pairs = pairs[(RI[pairs[:, 0]] != RI[pairs[:, 1]]) | (np.abs(LL[pairs[:, 0]] - LL[pairs[:, 1]]) > 8.0)]
    points: list[np.ndarray] = []
    kinds: list[str] = []
    for a, b in pairs:
        i, j = int(RI[a]), int(RI[b])
        if {i, j} == {2, 11}:
            points.append((P[a] + P[b]) / 2.0)
            kinds.append(f"rampe_{i}x{j}")

    # Include ramp/dorfweg contacts and all ramp endpoints before clustering,
    # because the official single-link cluster centroid includes those too.
    dw = np.zeros((ny, nx), dtype=bool)
    for x, z in data["wege"]:
        dw[int(z), int(x)] = True
    wega = np.frombuffer(base64.b64decode(data["WEGA"]), dtype=np.uint8).reshape(ny * rs + 1, nx * rs + 1)
    dw |= wega[:-1:rs, :-1:rs] > 20
    rz = np.zeros((ny, nx), dtype=bool)
    for path, _ in sampled:
        rz[np.clip(path[:, 1].astype(int), 0, ny - 1), np.clip(path[:, 0].astype(int), 0, nx - 1)] = True
    dwo = dw & ~ndi.binary_dilation(rz, iterations=1)
    dz, dx = np.nonzero(dwo)
    road_cells = np.column_stack((dx + 0.5, dz + 0.5))
    road_tree = cKDTree(road_cells) if len(road_cells) else None
    if road_tree is not None:
        distance, _ = road_tree.query(P, distance_upper_bound=1.5)
        for ix in np.flatnonzero(np.isfinite(distance)):
            if int(RI[ix]) in (2, 11):
                points.append(P[ix])
                kinds.append(f"rampe_{int(RI[ix])}xdorfweg")
    for i in range(len(paths)):
        if i in (2, 11):
            points.extend((sampled[i][0][0], sampled[i][0][-1]))
            kinds.extend((f"rampe_{i}_anfang", f"rampe_{i}_ende"))

    # Only the connected single-link component carrying rampe_2x11 is needed.
    centers = np.asarray(points, dtype=np.float64)
    uf_pairs = cKDTree(centers).query_pairs(4.0, output_type="ndarray")
    parent = np.arange(len(centers))

    def root(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = int(parent[i])
        return i

    for a, b in uf_pairs:
        ra, rb = root(int(a)), root(int(b))
        if ra != rb:
            parent[ra] = rb
    groups: dict[int, list[int]] = {}
    for i in range(len(centers)):
        groups.setdefault(root(i), []).append(i)
    candidates = []
    for group in groups.values():
        group_kinds = [kinds[i] for i in group]
        if not any("rampe_2x11" in kind or "rampe_11x2" in kind for kind in group_kinds):
            continue
        selected = [i for i in group if not kinds[i].startswith("dorfweg_knoten")]
        center = centers[selected].mean(axis=0)
        candidates.append((float(np.linalg.norm(center - R8_OLD_CENTER)), center, group_kinds))
    if not candidates:
        raise RuntimeError("Offizieller R8-Cluster rampe_2x11 wurde nicht rekonstruiert")
    _, center, _ = min(candidates, key=lambda item: item[0])
    return center.tolist()


def wall_distances(vector: dict, path: list[list[float]]) -> dict:
    line = LineString(np.asarray(path, dtype=np.float64) * CELL_M)
    measures = []
    for wall in vector.get("waende", []):
        raw = wall.get("mittellinie_m", [])
        if len(raw) > 1:
            dist = float(LineString(raw).distance(line))
            measures.append({"wall": wall.get("name", "?"), "distance_m": dist})
    return min(measures, key=lambda item: item["distance_m"]) if measures else None


def nearest_wall_at(vector: dict, coord_map: np.ndarray) -> dict | None:
    point = Point(*(np.asarray(coord_map, dtype=np.float64) * CELL_M))
    measures = []
    for wall in vector.get("waende", []):
        raw = wall.get("mittellinie_m", [])
        if len(raw) > 1:
            measures.append({"wall": wall.get("name", "?"),
                             "distance_m": float(LineString(raw).distance(point))})
    return min(measures, key=lambda item: item["distance_m"]) if measures else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=RELIEF3D / "relief_daten.json.gz")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--variant", choices=sorted(VARIANTS), default=None)
    args = ap.parse_args()
    env = __import__("os").environ
    variant = args.variant or env.get("P3D21_WEGE_VAR", env.get("RELIEF_KREUZUNG_VAR", "29"))
    if variant not in VARIANTS:
        raise ValueError(f"Unbekannte lokale Wegvariante: {variant}")
    transfer_variant = env.get("RELIEF_KREUZUNG_VAR", "29")
    source_bytes = args.source.read_bytes()
    data = json.loads(gzip.decompress(source_bytes))
    vector = json.loads((RELIEF3D / "neu/vektor.json").read_text(encoding="utf-8"))
    rs = int(data["rs"])
    wx = np.frombuffer(base64.b64decode(data["WV"]), dtype="<f4").reshape(
        int(data["ny"]) * rs + 1, int(data["nx"]) * rs + 1,
    )
    before_paths = [list(map(list, path)) for path in data["rampenwege"]]
    after_paths = [list(map(list, path)) for path in data["rampenwege"]]
    route_indices = {"rampe_2": 2, "rampe_11": 11}
    changes = {}
    for name, index in route_indices.items():
        old = np.asarray(before_paths[index], dtype=np.float64)
        features = VARIANTS[variant][name]
        new = deform(before_paths[index], features) if features else old.copy()
        after_paths[index] = new.tolist()
        old_line, new_line = LineString(old), LineString(new)
        old_cumulative = np.r_[0.0, np.cumsum(np.hypot(*np.diff(old, axis=0).T))] * CELL_M
        changes[name] = {
            "route_index": index,
            "old_vertex_count": int(len(old)), "new_vertex_count": int(len(new)),
            "old_length_m": float(old_line.length * CELL_M),
            "new_length_m": float(new_line.length * CELL_M),
            "start_before_map": old[0].tolist(), "start_after_map": new[0].tolist(),
            "end_before_map": old[-1].tolist(), "end_after_map": new[-1].tolist(),
            "max_displacement_m": float(np.max(np.linalg.norm((new - old) * CELL_M, axis=1))),
            "endpoint_wall_centerline_distances_m": {
                "start_before": nearest_wall_at(vector, old[0]),
                "start_after": nearest_wall_at(vector, new[0]),
                "end_before": nearest_wall_at(vector, old[-1]),
                "end_after": nearest_wall_at(vector, new[-1]),
            },
            "endpoint_is_water": {
                "start_before": bool(wx[int(round(old[0, 1] * rs)), int(round(old[0, 0] * rs))] > -900),
                "start_after": bool(wx[int(round(new[0, 1] * rs)), int(round(new[0, 0] * rs))] > -900),
                "end_before": bool(wx[int(round(old[-1, 1] * rs)), int(round(old[-1, 0] * rs))] > -900),
                "end_after": bool(wx[int(round(new[-1, 1] * rs)), int(round(new[-1, 0] * rs))] > -900),
            },
            "min_wall_centerline_before": wall_distances(vector, before_paths[index]),
            "min_wall_centerline_after": wall_distances(vector, after_paths[index]),
            "waypoints": [],
        }
        for station_m, label in (
            (20.055, "R4 rampe_2"), (27.917, "R5 rampe_11"),
            (37.865, "G5 158.2|30.6"), (39.752, "G5 159.5|28.5"),
            (42.072, "G5 161.4|28.1"), (47.4, "rampe_11 third bend"),
        ):
            if (name == "rampe_2" and label.startswith("G5")) or (name == "rampe_2" and label.startswith("R4")) or (name == "rampe_11" and label.startswith(("R5", "rampe_11"))):
                st = station_m / CELL_M
                old_coord = np.array([np.interp(st, old_cumulative / CELL_M, old[:, axis]) for axis in range(2)])
                new_coord = np.array([np.interp(st, old_cumulative / CELL_M, new[:, axis]) for axis in range(2)])
                changes[name]["waypoints"].append({
                    "label": label, "station_old_m": station_m,
                    "before_map": old_coord.tolist(), "after_same_nominal_station_map": new_coord.tolist(),
                    "shift_m": float(np.linalg.norm((new_coord - old_coord) * CELL_M)),
                })
    data["rampenwege"] = after_paths
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(gzip.compress(payload, compresslevel=9, mtime=0))
    out_sha = hashlib.sha256(args.out.read_bytes()).hexdigest()
    gate_center = official_crossing_center(data, after_paths)
    old_crossings = LineString(before_paths[2]).intersection(LineString(before_paths[11]))
    new_crossings = LineString(after_paths[2]).intersection(LineString(after_paths[11]))
    def points(geom):
        if geom.geom_type == "Point":
            return [[float(geom.x), float(geom.y)]]
        if hasattr(geom, "geoms"):
            return [[float(item.x), float(item.y)] for item in geom.geoms if item.geom_type == "Point"]
        return []
    report = {
        "variant": variant,
        "source_before_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_after_sha256": out_sha,
        "transfer_variant": transfer_variant,
        "source_data_changes": [
            f"rampenwege[{i}]" for i in range(len(before_paths))
            if after_paths[i] != before_paths[i]
        ],
        "other_rampenwege_semantically_unchanged": all(
            data["rampenwege"][i] == before_paths[i]
            for i in range(len(before_paths))
            if after_paths[i] == before_paths[i]
        ),
        "official_R8_gate_center_map": gate_center,
        "old_route_intersections_map": points(old_crossings),
        "new_route_intersections_map": points(new_crossings),
        "routes": changes,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
