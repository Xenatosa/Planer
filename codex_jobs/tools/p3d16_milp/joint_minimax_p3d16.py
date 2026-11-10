#!/usr/bin/env python3
"""Joint local R8 minimax model with p3d15 ramp-profile constraints.

The continuous variables include both route profiles and a 0.25-map-unit
surface raster. In R3 mode, the exact Gaussian residual operator used by the
p3d15 MILP is present with at most six flagged D1 sections. This makes the
reported step a joint feasibility bound instead of a bound for one frozen
profile.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
from scipy.spatial import cKDTree
from shapely.geometry import LineString, box

ROOT = Path(__file__).resolve().parents[3]
RELIEF = ROOT / "team/art/dorfmap_grundgeruest/relief3d/relief_daten.json.gz"
CELL_M = 1.2
SAMPLE_STEP = 0.25
R3_SIGMA = 8.0
R3_TOL = 0.075
R3_SECTION_SAMPLES = 16
SLOPE_MAX = 0.60
PLANE_RADIUS_M = 2.0
PLANE_TOL_M = 0.02
PLANE_SLOPE_MAX = 0.03
PAIR_RADIUS_M = 4.5
SAME_ROUTE_ARC_FACTOR = 1.25
END_PIN_COORD = 1.0
WALL_TAIL_START = 40.0
WALL_TAIL_TOL = 0.25
CROSSING = np.array([152.5, 28.5], dtype=np.float64)
D1_BOUNDS = (126.0, 0.0, 168.0, 43.0)


def profile_path(raw: list[list[float]]) -> tuple[np.ndarray, np.ndarray]:
    path = np.asarray(raw, dtype=np.float64)
    cumulative = np.r_[0.0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))]
    station = np.arange(0.0, cumulative[-1] + 1e-7, SAMPLE_STEP)
    coords = np.column_stack((
        np.interp(station, cumulative, path[:, 0]),
        np.interp(station, cumulative, path[:, 1]),
    ))
    return station, coords


def bilinear_row(x: float, z: float, x0: float, z0: float, fs: int, width: int) -> dict[int, float]:
    u, v = (x - x0) * fs, (z - z0) * fs
    ix, iz = int(np.floor(u)), int(np.floor(v))
    ix, iz = min(max(ix, 0), width - 2), min(max(iz, 0), width - 2)
    fu, fv = u - ix, v - iz
    return {
        iz * width + ix: (1.0 - fu) * (1.0 - fv),
        iz * width + ix + 1: fu * (1.0 - fv),
        (iz + 1) * width + ix: (1.0 - fu) * fv,
        (iz + 1) * width + ix + 1: fu * fv,
    }


def route_pairs(profiles: list[dict]) -> list[tuple[int, int, int, int, float]]:
    coords = [np.asarray(p["coords"]) * CELL_M for p in profiles]
    stations = [np.asarray(p["station"]) * CELL_M for p in profiles]
    trees = [cKDTree(c) for c in coords]
    pairs = []
    for a in range(len(profiles)):
        for b in range(a, len(profiles)):
            if a == b:
                lists = trees[a].query_ball_point(coords[a], PAIR_RADIUS_M)
                candidates = ((i, j) for i, js in enumerate(lists) for j in sorted(js) if j > i)
            else:
                lists = trees[b].query_ball_tree(trees[a], PAIR_RADIUS_M)
                candidates = ((i, j) for j, ii in enumerate(lists) for i in sorted(ii))
            for i, j in candidates:
                distance = float(np.linalg.norm(coords[a][i] - coords[b][j]))
                if distance > PAIR_RADIUS_M + 1e-9:
                    continue
                if a == b and stations[a][j] - stations[a][i] <= SAME_ROUTE_ARC_FACTOR * distance + 1e-9:
                    continue
                pairs.append((a, i, b, j, distance))
    return pairs


def local_r8_mask(data: dict, fs: int) -> tuple[np.ndarray, float, float, list[tuple[int, int]]]:
    nx, ny, rs = int(data["nx"]), int(data["ny"]), int(data["rs"])
    fine_shape = (ny * fs + 1, nx * fs + 1)
    ramp_points = [profile_path(p)[1] for p in data["rampenwege"]]
    road_cells = np.zeros((ny, nx), dtype=bool)
    for x, z in data["wege"]:
        road_cells[int(z), int(x)] = True
    road_cells |= np.frombuffer(base64.b64decode(data["WEGA"]), dtype=np.uint8).reshape(
        ny * rs + 1, nx * rs + 1,
    )[:-1:rs, :-1:rs] > 20
    ramp_cells = np.zeros_like(road_cells)
    for path in ramp_points:
        ramp_cells[np.clip(path[:, 1].astype(int), 0, ny - 1),
                    np.clip(path[:, 0].astype(int), 0, nx - 1)] = True
    _road_without_ramps = road_cells & ~ndi.binary_dilation(ramp_cells, iterations=1)

    mask = np.zeros(fine_shape, dtype=bool)
    for path in ramp_points:
        mask[np.clip(np.rint(path[:, 1] * fs).astype(int), 0, fine_shape[0] - 1),
             np.clip(np.rint(path[:, 0] * fs).astype(int), 0, fine_shape[1] - 1)] = True
    mask = ndi.distance_transform_edt(~mask) / fs <= 1.5
    mask[:-1, :-1] |= np.kron(road_cells, np.ones((fs, fs), dtype=bool))
    cx, cz = map(float, CROSSING)
    ix0, ix1 = round((cx - 4.0) * fs), round((cx + 4.0) * fs)
    iz0, iz1 = round((cz - 4.0) * fs), round((cz + 4.0) * fs)
    local = mask[iz0:iz1 + 1, ix0:ix1 + 1].copy()
    zz, xx = np.mgrid[iz0:iz1 + 1, ix0:ix1 + 1]
    local &= np.hypot(xx / fs - cx, zz / fs - cz) <= 4.0 + 1e-9
    pairs: list[tuple[int, int]] = []
    height, width = local.shape
    for ys, xs in zip(*np.nonzero(local)):
        a = ys * width + xs
        if ys + 1 < height and local[ys + 1, xs]:
            pairs.append((a, (ys + 1) * width + xs))
        if xs + 1 < width and local[ys, xs + 1]:
            pairs.append((a, ys * width + xs + 1))
    return local, ix0 / fs, iz0 / fs, pairs


def solve(data: dict, grade: float, r3_limit: int | None, out: Path) -> dict:
    rs = int(data["rs"])
    ny, nx = int(data["ny"]), int(data["nx"])
    gb = np.frombuffer(base64.b64decode(data["GB"]), dtype=np.float32).reshape(ny * rs + 1, nx * rs + 1)
    tile = box(*D1_BOUNDS)
    profiles = []
    for index, raw in enumerate(data["rampenwege"]):
        path = np.asarray(raw, dtype=np.float64)
        if not LineString(path).intersects(tile):
            continue
        station, coords = profile_path(raw)
        h0 = ndi.map_coordinates(gb, [coords[:, 1] * rs, coords[:, 0] * rs], order=1, mode="nearest")
        profiles.append({"index": index, "station": station, "coords": coords, "h0": h0.astype(np.float64)})
    profiles.sort(key=lambda p: p["index"])
    if [p["index"] for p in profiles] != [2, 11]:
        raise RuntimeError(f"Expected D1 routes [2, 11], found {[p['index'] for p in profiles]}")

    lengths = [len(p["h0"]) for p in profiles]
    h_offsets = np.cumsum([0, *lengths[:-1]]).astype(int).tolist()
    total_h = sum(lengths)
    lo_h = np.empty(total_h, dtype=np.float64)
    hi_h = np.empty(total_h, dtype=np.float64)
    r3_sections = []
    section_lookup = []
    for route, p in enumerate(profiles):
        h0, station, coords = p["h0"], p["station"], p["coords"]
        x0, z0, x1, z1 = D1_BOUNDS
        edge = np.minimum.reduce((coords[:, 0] - x0, x1 - coords[:, 0], coords[:, 1] - z0, z1 - coords[:, 1])) * CELL_M
        fixed = (station <= END_PIN_COORD + 1e-9) | (station >= station[-1] - END_PIN_COORD - 1e-9)
        fixed |= edge < 3.0 - 1e-8
        lo, hi = h0 - 2.0, h0 + 2.0
        if p["index"] == 11:
            tail = station >= WALL_TAIL_START - 1e-9
            lo[tail] = np.maximum(lo[tail], h0[tail] - WALL_TAIL_TOL)
            hi[tail] = np.minimum(hi[tail], h0[tail] + WALL_TAIL_TOL)
        lo[fixed], hi[fixed] = h0[fixed], h0[fixed]
        lo_h[h_offsets[route]:h_offsets[route] + len(h0)] = lo
        hi_h[h_offsets[route]:h_offsets[route] + len(h0)] = hi
        if r3_limit is not None:
            for k in range(0, len(h0), R3_SECTION_SAMPLES):
                x, z = coords[k]
                inside = D1_BOUNDS[0] <= x <= D1_BOUNDS[2] and D1_BOUNDS[1] <= z <= D1_BOUNDS[3]
                section_lookup.append((route, k, inside))
                r3_sections.append((route, k // R3_SECTION_SAMPLES))
    r3_sections = list(dict.fromkeys(r3_sections))
    binary_index = {item: total_h + 0 for item in []}

    local, x0, z0, neighbor_pairs = local_r8_mask(data, int(data["FW"]["fs"]))
    fs = int(data["FW"]["fs"])
    height, width = local.shape
    surface_count = height * width
    surface_start = total_h
    t_index = surface_start + surface_count
    plane_h = t_index + 1
    plane_gx = plane_h + 1
    plane_gz = plane_h + 2
    binary_start = plane_gz + 1
    if r3_limit is None:
        binary_index = {}
    else:
        binary_index = {item: binary_start + i for i, item in enumerate(r3_sections)}
    nvars = binary_start + len(binary_index)

    lower = np.full(nvars, -np.inf, dtype=np.float64)
    upper = np.full(nvars, np.inf, dtype=np.float64)
    lower[:total_h], upper[:total_h] = lo_h, hi_h
    lower[t_index] = 0.0
    lower[plane_h] = float(min(np.min(p["h0"]) for p in profiles) - 2.0)
    upper[plane_h] = float(max(np.max(p["h0"]) for p in profiles) + 2.0)
    lower[plane_gx:plane_gz + 1], upper[plane_gx:plane_gz + 1] = -PLANE_SLOPE_MAX, PLANE_SLOPE_MAX
    integrality = np.zeros(nvars, dtype=np.uint8)
    for j in binary_index.values():
        lower[j], upper[j], integrality[j] = 0.0, 1.0, 1

    row_i: list[int] = []
    col_i: list[int] = []
    vals: list[float] = []
    rhs: list[float] = []

    def add(row: dict[int, float], bound: float) -> None:
        rid = len(rhs)
        for col, value in row.items():
            if abs(value) > 1e-13:
                row_i.append(rid)
                col_i.append(int(col))
                vals.append(float(value))
        rhs.append(float(bound))

    # R8 checker local road-neighbor pairs, each bounded by the same minimax step.
    for a, b in neighbor_pairs:
        va, vb = surface_start + a, surface_start + b
        add({va: 1.0, vb: -1.0, t_index: -1.0}, 0.0)
        add({va: -1.0, vb: 1.0, t_index: -1.0}, 0.0)

    # Mesh axis samples agree with the exact ramp variables within 2 cm.
    axis_count = 0
    for route, p in enumerate(profiles):
        for k, (x, z) in enumerate(p["coords"]):
            if not (x0 - 1e-9 <= x <= x0 + (width - 1) / fs + 1e-9 and z0 - 1e-9 <= z <= z0 + (height - 1) / fs + 1e-9):
                continue
            row = {surface_start + j: v for j, v in bilinear_row(float(x), float(z), x0, z0, fs, width).items()}
            hidx = h_offsets[route] + k
            add({**row, hidx: -1.0}, 0.02)
            add({**{j: -v for j, v in row.items()}, hidx: 1.0}, 0.02)
            axis_count += 1

    # The entire 2 m plane core is held at the MILP plane within 2 cm.
    plane_count = 0
    for iz in range(height):
        for ix in range(width):
            x, z = x0 + ix / fs, z0 + iz / fs
            dx, dz = (x - CROSSING[0]) * CELL_M, (z - CROSSING[1]) * CELL_M
            if np.hypot(dx, dz) > PLANE_RADIUS_M + 1e-9:
                continue
            si = surface_start + iz * width + ix
            add({si: 1.0, plane_h: -1.0, plane_gx: -dx, plane_gz: -dz}, PLANE_TOL_M)
            add({si: -1.0, plane_h: 1.0, plane_gx: dx, plane_gz: dz}, PLANE_TOL_M)
            plane_count += 1
    polygon_bound = PLANE_SLOPE_MAX * np.cos(np.pi / 32.0)
    for angle in np.arange(32) * (2.0 * np.pi / 32.0):
        add({plane_gx: float(np.cos(angle)), plane_gz: float(np.sin(angle))}, polygon_bound)

    # The profile section gradient and p3d15 monotonic source-descending rows.
    for route, p in enumerate(profiles):
        start = h_offsets[route]
        for k in range(len(p["h0"]) - 1):
            add({start + k + 1: 1.0, start + k: -1.0}, SLOPE_MAX * SAMPLE_STEP)
            add({start + k: 1.0, start + k + 1: -1.0}, SLOPE_MAX * SAMPLE_STEP)
            if p["h0"][k + 1] <= p["h0"][k] + 1e-9:
                add({start + k + 1: 1.0, start + k: -1.0}, 0.0)

    # Exact Gaussian R3 operator; at most six violating sections start in D1.
    r3_d1_terms = []
    if r3_limit is not None:
        for route, p in enumerate(profiles):
            h0, start = p["h0"], h_offsets[route]
            operator = np.eye(len(h0), dtype=np.float64) - ndi.gaussian_filter1d(
                np.eye(len(h0), dtype=np.float64), sigma=R3_SIGMA, axis=0, mode="nearest",
            )
            for k, op_row in enumerate(operator):
                active = np.flatnonzero(np.abs(op_row) > 1e-12)
                sec = k // R3_SECTION_SAMPLES
                bidx = binary_index[(route, sec)]
                row = {start + int(j): float(op_row[j]) for j in active}
                max_value = sum(float(op_row[j]) * (hi_h[start + j] if op_row[j] >= 0 else lo_h[start + j]) for j in active)
                min_value = sum(float(op_row[j]) * (lo_h[start + j] if op_row[j] >= 0 else hi_h[start + j]) for j in active)
                upper_relax = max(0.0, max_value - R3_TOL)
                lower_relax = max(0.0, -min_value - R3_TOL)
                add({**row, bidx: -upper_relax}, R3_TOL)
                add({**{j: -v for j, v in row.items()}, bidx: -lower_relax}, R3_TOL)
        for route, k, inside in section_lookup:
            if inside:
                r3_d1_terms.append(binary_index[(route, k // R3_SECTION_SAMPLES)])
        add({j: 1.0 for j in sorted(set(r3_d1_terms))}, float(r3_limit))

    # Same-route and cross-route pairs from p3d15, with the selected physical grade.
    pairs = route_pairs(profiles)
    for ra, ia, rb, ib, distance in pairs:
        va, vb = h_offsets[ra] + ia, h_offsets[rb] + ib
        bound = grade * distance
        add({va: 1.0, vb: -1.0}, bound)
        add({va: -1.0, vb: 1.0}, bound)

    matrix = coo_matrix((vals, (row_i, col_i)), shape=(len(rhs), nvars)).tocsr()
    objective = np.zeros(nvars, dtype=np.float64)
    objective[t_index] = 1.0
    result = milp(
        objective, integrality=integrality, bounds=Bounds(lower, upper),
        constraints=LinearConstraint(matrix, np.full(len(rhs), -np.inf), np.asarray(rhs)),
        options={"presolve": True, "mip_rel_gap": 0.0, "time_limit": 600},
    )
    summary = {
        "status": str(result.message), "status_code": int(result.status), "success": bool(result.success),
        "g_m_per_m": grade, "r3_D1_limit": r3_limit, "plane_radius_m": PLANE_RADIUS_M,
        "axis_tolerance_m": 0.02, "plane_tolerance_m": PLANE_TOL_M,
        "plane_slope_limit_pct": 3.0, "same_route_arc_distance_factor": SAME_ROUTE_ARC_FACTOR,
        "route_pair_count": len(pairs), "same_route_pair_count": sum(a == b for a, _, b, _, _ in pairs),
        "R8_neighbor_pair_count": len(neighbor_pairs), "axis_supports": axis_count,
        "plane_core_supports": plane_count, "variables": nvars, "constraints": len(rhs),
        "minimum_neighbor_step_m": float(result.fun) if result.x is not None else None,
        "mip_dual_bound_m": (None if getattr(result, "mip_dual_bound", None) is None else float(result.mip_dual_bound)),
        "mip_gap": (None if getattr(result, "mip_gap", None) is None else float(result.mip_gap)),
    }
    if result.x is not None:
        xsol = result.x
        section_count = int(sum(xsol[j] > 0.5 for j in set(r3_d1_terms))) if r3_limit is not None else None
        summary["r3_sections_D1_solution"] = section_count
        summary["plane_height_m"] = float(xsol[plane_h])
        summary["plane_gradient_x"] = float(xsol[plane_gx])
        summary["plane_gradient_z"] = float(xsol[plane_gz])
        summary["plane_slope_pct"] = float(np.hypot(xsol[plane_gx], xsol[plane_gz]) * 100.0)
        steps = [(abs(xsol[surface_start + a] - xsol[surface_start + b]), a, b) for a, b in neighbor_pairs]
        step, a, b = max(steps, default=(0.0, 0, 0))
        def point(i: int) -> dict:
            iz, ix = divmod(i, width)
            return {"x": x0 + ix / fs, "z": z0 + iz / fs, "height_m": float(xsol[surface_start + i])}
        summary["worst_pair"] = {"step_m": float(step), "a": point(a), "b": point(b)}
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--grade", type=float, choices=(0.45, 0.60), required=True)
    ap.add_argument("--r3-limit", type=int, default=None, help="omit for isolated surface bound without R3 rows")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    with gzip.open(RELIEF, "rt", encoding="utf-8") as f:
        data = json.load(f)
    solve(data, args.grade, args.r3_limit, args.out)


if __name__ == "__main__":
    main()
