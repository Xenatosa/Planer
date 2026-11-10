#!/usr/bin/env python3
"""Recompute p3d16 joint R8 lower bound on the emitted 0.5-map-unit mesh raster.

The checker still evaluates neighboring 0.25-map-unit samples bilinearly on
the emitted mesh raster. Route profiles, plane core and R3 are jointly
constrained as in p3d16. The optimal route and surface solution is serialized
so the transfer can be compared point-by-point.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import coo_matrix, csr_matrix, hstack, vstack
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
# Exact unrounded center of the D1 R8 gate cluster; the gate rounds this to
# 152.5|28.5 for display, but uses the unrounded center for its 4-unit mask.
R8_GATE_CENTER = np.array([152.54985704503775, 28.48954534572434], dtype=np.float64)
R8_GATE_RADIUS_MAP = 4.0
R8_GITTER_RADIUS_MAP = 2.0
R8_QUER_RADIUS_MAP = 1.5
R8_GITTER_LIMIT_M = 0.02
R8_QUER_LIMIT_PCT = 3.0
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
    cx, cz = map(float, R8_GATE_CENTER)
    ix0, ix1 = round((cx - R8_GATE_RADIUS_MAP) * fs), round((cx + R8_GATE_RADIUS_MAP) * fs)
    iz0, iz1 = round((cz - R8_GATE_RADIUS_MAP) * fs), round((cz + R8_GATE_RADIUS_MAP) * fs)
    local = mask[iz0:iz1 + 1, ix0:ix1 + 1].copy()
    zz, xx = np.mgrid[iz0:iz1 + 1, ix0:ix1 + 1]
    local &= np.hypot(xx / fs - cx, zz / fs - cz) <= R8_GATE_RADIUS_MAP + 1e-9
    pairs: list[tuple[int, int]] = []
    height, width = local.shape
    for ys, xs in zip(*np.nonzero(local)):
        a = ys * width + xs
        if ys + 1 < height and local[ys + 1, xs]:
            pairs.append((a, (ys + 1) * width + xs))
        if xs + 1 < width and local[ys, xs + 1]:
            pairs.append((a, ys * width + xs + 1))
    return local, ix0 / fs, iz0 / fs, pairs


def solve(data: dict, grade: float, r3_limit: int | None, out: Path, reference_mesh_path: Path | None, axis_tolerance: float, plane_tolerance: float) -> dict:
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

    checker_fs = int(data["FW"]["fs"])
    local, local_x0, local_z0, neighbor_pairs = local_r8_mask(data, checker_fs)
    # D1 mesh vertices use the global relief resolution (rs=2 => 0.5 map units).
    # The whole D1 mesh is part of the joint field; checker points remain at
    # FW.fs=4 and are evaluated bilinearly on these nodes.
    fs = int(data["rs"])
    grid_x0, grid_z0, grid_x1, grid_z1 = D1_BOUNDS
    height = int(round((grid_z1 - grid_z0) * fs)) + 1
    width = int(round((grid_x1 - grid_x0) * fs)) + 1
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

    # Bilinear evaluation at every checker sample on the emitted mesh raster.
    def mesh_row(px: float, pz: float) -> dict[int, float]:
        return bilinear_row(px, pz, grid_x0, grid_z0, fs, width)

    def pair_row(a: int, b: int) -> dict[int, float]:
        checker_width = local.shape[1]
        az, ax = divmod(a, checker_width)
        bz, bx = divmod(b, checker_width)
        row_a = mesh_row(local_x0 + ax / checker_fs, local_z0 + az / checker_fs)
        row_b = mesh_row(local_x0 + bx / checker_fs, local_z0 + bz / checker_fs)
        entries = dict(row_a)
        for index, value in row_b.items():
            entries[index] = entries.get(index, 0.0) - value
        return entries

    # R8 checker local road-neighbor pairs, evaluated bilinearly on the 0.5 grid.
    for a, b in neighbor_pairs:
        entries = {surface_start + j: v for j, v in pair_row(a, b).items()}
        add({**entries, t_index: -1.0}, 0.0)
        add({**{j: -v for j, v in entries.items()}, t_index: -1.0}, 0.0)

    # Mesh axis samples agree with the exact ramp variables within 2 cm.
    axis_count = 0
    for route, p in enumerate(profiles):
        for k, (x, z) in enumerate(p["coords"]):
            if not (grid_x0 - 1e-9 <= x <= grid_x1 + 1e-9 and grid_z0 - 1e-9 <= z <= grid_z1 + 1e-9):
                continue
            row = {surface_start + j: v for j, v in mesh_row(float(x), float(z)).items()}
            hidx = h_offsets[route] + k
            add({**row, hidx: -1.0}, axis_tolerance)
            add({**{j: -v for j, v in row.items()}, hidx: 1.0}, axis_tolerance)
            axis_count += 1

    # Hold the complete plane core at checker resolution, using bilinear mesh values.
    plane_count = 0
    checker_height, checker_width = local.shape
    for iz in range(checker_height):
        for ix in range(checker_width):
            x, z = local_x0 + ix / checker_fs, local_z0 + iz / checker_fs
            dx, dz = (x - CROSSING[0]) * CELL_M, (z - CROSSING[1]) * CELL_M
            if np.hypot(dx, dz) > PLANE_RADIUS_M + 1e-9:
                continue
            entries = {surface_start + j: v for j, v in mesh_row(x, z).items()}
            entries.update({plane_h: -1.0, plane_gx: -dx, plane_gz: -dz})
            add(entries, plane_tolerance)
            add({j: -v for j, v in entries.items()}, plane_tolerance)
            plane_count += 1

    # Encode the unchanged R8 gate's least-squares residual and slope operators
    # directly. The hard plane core remains 2.00 physical metres; these rows
    # only constrain the checker footprints used for its Gitter and Quer values.
    checker_x, checker_z = np.meshgrid(
        local_x0 + np.arange(checker_width, dtype=np.float64) / checker_fs,
        local_z0 + np.arange(checker_height, dtype=np.float64) / checker_fs,
    )
    checker_radius = np.hypot(
        checker_x - R8_GATE_CENTER[0], checker_z - R8_GATE_CENTER[1],
    )
    gitter_mask = local & (checker_radius <= R8_GITTER_RADIUS_MAP + 1e-9)
    quer_mask = local & (checker_radius <= R8_QUER_RADIUS_MAP + 1e-9)

    def gate_support_rows(mask: np.ndarray) -> tuple[np.ndarray, list[dict[int, float]], np.ndarray]:
        iy, ix = np.nonzero(mask)
        xy = np.column_stack((checker_x[iy, ix] - R8_GATE_CENTER[0],
                              checker_z[iy, ix] - R8_GATE_CENTER[1]))
        design = np.column_stack((xy, np.ones(len(xy), dtype=np.float64)))
        supports = [mesh_row(float(px), float(pz)) for px, pz in zip(checker_x[iy, ix], checker_z[iy, ix])]
        return iy * checker_width + ix, supports, design

    def combine_support_rows(weights: np.ndarray, supports: list[dict[int, float]]) -> dict[int, float]:
        entries: dict[int, float] = {}
        for weight, support in zip(weights, supports):
            if abs(float(weight)) <= 1e-13:
                continue
            for column, value in support.items():
                surface_column = surface_start + column
                entries[surface_column] = entries.get(surface_column, 0.0) + float(weight) * value
        return entries

    gitter_ids, gitter_supports, gitter_design = gate_support_rows(gitter_mask)
    gitter_inverse = np.linalg.pinv(gitter_design)
    gitter_index = {int(flat): i for i, flat in enumerate(gitter_ids)}
    gitter_pair_count = 0
    gitter_pairs: list[tuple[int, int]] = []
    checker_stride = int(round(1.0 * checker_fs))
    for i, flat in enumerate(gitter_ids):
        iy, ix = divmod(int(flat), checker_width)
        for dy, dx in ((checker_stride, 0), (0, checker_stride)):
            neighbor_flat = (iy + dy) * checker_width + ix + dx
            j = gitter_index.get(neighbor_flat)
            if j is None:
                continue
            residual_weights = -(
                gitter_design[i] - gitter_design[j]
            ) @ gitter_inverse
            residual_weights[i] += 1.0
            residual_weights[j] -= 1.0
            entries = combine_support_rows(residual_weights, gitter_supports)
            add(entries, R8_GITTER_LIMIT_M)
            add({column: -value for column, value in entries.items()}, R8_GITTER_LIMIT_M)
            gitter_pairs.append((i, j))
            gitter_pair_count += 1

    quer_ids, quer_supports, quer_design = gate_support_rows(quer_mask)
    quer_inverse = np.linalg.pinv(quer_design)
    quer_row_count = 0
    quer_bound = (R8_QUER_LIMIT_PCT / 100.0) * np.cos(np.pi / 32.0)
    for angle in np.arange(32, dtype=np.float64) * (2.0 * np.pi / 32.0):
        weights = np.cos(angle) * quer_inverse[0] + np.sin(angle) * quer_inverse[1]
        entries = combine_support_rows(weights, quer_supports)
        add(entries, quer_bound)
        quer_row_count += 1

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
    if not result.success or result.x is None:
        raise RuntimeError(f"Joint mesh LP/MILP failed: {result.message}")

    # Among exact minimax solutions, preserve the p3d16 feasible profile and
    # mesh as closely as possible. This removes arbitrary values at untargeted
    # variables while leaving the measured lower bound unchanged.
    primary_step = float(result.fun)
    add({t_index: 1.0}, primary_step + 1e-8)
    base_matrix = coo_matrix((vals, (row_i, col_i)), shape=(len(rhs), nvars)).tocsr()
    reference_profiles = json.loads((Path(__file__).resolve().parents[1] / "p3d16_milp/machbarkeit_g45.json").read_text(encoding="utf-8"))["routes"]
    profile_reference = np.concatenate([
        np.asarray(reference_profiles[f"rampe_{p['index']}"]["h_solution"], dtype=np.float64)
        for p in profiles
    ])
    if reference_mesh_path is None:
        reference_g = np.frombuffer(base64.b64decode(data["GB"]), dtype=np.float32).reshape(ny * rs + 1, nx * rs + 1).astype(np.float64)
    else:
        ref_data = json.loads(gzip.decompress(reference_mesh_path.read_bytes()))
        reference_g = np.frombuffer(base64.b64decode(ref_data["GB"]), dtype=np.float32).reshape(ny * rs + 1, nx * rs + 1).astype(np.float64)
    mesh_x = grid_x0 + np.arange(width, dtype=np.float64) / fs
    mesh_z = grid_z0 + np.arange(height, dtype=np.float64) / fs
    mz, mx = np.meshgrid(mesh_z, mesh_x, indexing="ij")
    surface_reference = ndi.map_coordinates(reference_g, [mz.ravel() * rs, mx.ravel() * rs], order=1, mode="nearest")
    slack_count = total_h + surface_count
    nvars_secondary = nvars + slack_count
    secondary_rows = []
    secondary_rhs = []
    secondary_cols = []
    secondary_vals = []
    def add_secondary(row_index: int, entries: dict[int, float], bound: float) -> None:
        for column, value in entries.items():
            if abs(value) > 1e-13:
                secondary_rows.append(row_index)
                secondary_cols.append(column)
                secondary_vals.append(value)
        secondary_rhs.append(bound)
    for index, target in enumerate(profile_reference):
        slack = nvars + index
        add_secondary(len(secondary_rhs), {index: 1.0, slack: -1.0}, float(target))
        add_secondary(len(secondary_rhs), {index: -1.0, slack: -1.0}, -float(target))
    for index, target in enumerate(surface_reference):
        variable = surface_start + index
        slack = nvars + total_h + index
        add_secondary(len(secondary_rhs), {variable: 1.0, slack: -1.0}, float(target))
        add_secondary(len(secondary_rhs), {variable: -1.0, slack: -1.0}, -float(target))
    move_matrix = coo_matrix((secondary_vals, (secondary_rows, secondary_cols)), shape=(len(secondary_rhs), nvars_secondary)).tocsr()
    expanded = hstack([base_matrix, csr_matrix((base_matrix.shape[0], slack_count))], format="csr")
    A2 = vstack([expanded, move_matrix], format="csr")
    b2 = np.asarray([*rhs, *secondary_rhs], dtype=np.float64)
    lower2 = np.r_[lower, np.zeros(slack_count, dtype=np.float64)]
    upper2 = np.r_[upper, np.full(slack_count, np.inf, dtype=np.float64)]
    for index in binary_index.values():
        fixed_value = float(round(result.x[index]))
        lower2[index] = upper2[index] = fixed_value
    c2 = np.zeros(nvars_secondary, dtype=np.float64)
    c2[nvars:nvars + total_h] = 1.0
    c2[nvars + total_h:] = 1.0
    secondary = linprog(c2, A_ub=A2, b_ub=b2, bounds=list(zip(lower2, upper2)), method="highs")
    if not secondary.success or secondary.x is None:
        raise RuntimeError(f"Minimax tie-break LP failed: {secondary.message}")
    result_x = secondary.x[:nvars]
    result.fun = primary_step
    result.x = result_x
    tie_break_movement = float(secondary.fun)

    summary = {
        "status": str(result.message), "status_code": int(result.status), "success": bool(result.success),
        "g_m_per_m": grade, "r3_D1_limit": r3_limit, "plane_radius_m": PLANE_RADIUS_M,
        "axis_tolerance_m": axis_tolerance, "plane_tolerance_m": plane_tolerance,
        "plane_slope_limit_pct": 3.0, "same_route_arc_distance_factor": SAME_ROUTE_ARC_FACTOR,
        "route_pair_count": len(pairs), "same_route_pair_count": sum(a == b for a, _, b, _, _ in pairs),
        "R8_neighbor_pair_count": len(neighbor_pairs), "axis_supports": axis_count,
        "plane_core_supports": plane_count,
        "R8_gate_center_unrounded_map": R8_GATE_CENTER.tolist(),
        "R8_gate_gitter_support_pairs": gitter_pair_count,
        "R8_gate_quer_supports": int(len(quer_ids)),
        "R8_gate_quer_slope_limit_pct": R8_QUER_LIMIT_PCT,
        "variables": nvars, "constraints": len(rhs),
        "minimum_neighbor_step_m": primary_step,
        "tie_break_movement_l1_m": tie_break_movement,
        "tie_break_reference_mesh": reference_mesh_path.name if reference_mesh_path else "GB source field",
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
        surface = xsol[surface_start:surface_start + surface_count]
        steps = []
        for a, b in neighbor_pairs:
            row = pair_row(a, b)
            step_value = abs(sum(value * surface[index] for index, value in row.items()))
            steps.append((step_value, a, b))
        step, a, b = max(steps, default=(0.0, 0, 0))

        def evaluate_supports(supports: list[dict[int, float]]) -> np.ndarray:
            return np.asarray([
                sum(value * surface[index] for index, value in row.items())
                for row in supports
            ], dtype=np.float64)

        gitter_values = evaluate_supports(gitter_supports)
        gitter_residual = gitter_values - gitter_design @ np.linalg.lstsq(
            gitter_design, gitter_values, rcond=None,
        )[0]
        gitter_step = max((abs(float(gitter_residual[i] - gitter_residual[j]))
                           for i, j in gitter_pairs), default=0.0)
        quer_values = evaluate_supports(quer_supports)
        quer_plane = np.linalg.lstsq(quer_design, quer_values, rcond=None)[0]
        quer_slope_pct = float(np.hypot(quer_plane[0], quer_plane[1]) * 100.0)
        summary["R8_gate_metrics_solution"] = {
            "R8_stufe_m": float(step),
            "R8_gitter_m": float(gitter_step),
            "R8_quer_pct": quer_slope_pct,
        }
        def checker_point(i: int) -> dict:
            iz, ix = divmod(i, local.shape[1])
            px, pz = local_x0 + ix / checker_fs, local_z0 + iz / checker_fs
            row = mesh_row(px, pz)
            sampled = sum(value * surface[index] for index, value in row.items())
            return {"x": px, "z": pz, "height_m": float(sampled)}
        summary["worst_pair"] = {"step_m": float(step), "a": checker_point(a), "b": checker_point(b)}
        summary["mesh_raster_spacing_map_units"] = 1.0 / fs
        summary["checker_spacing_map_units"] = 1.0 / checker_fs
        summary["surface_grid"] = {
            "x0": grid_x0, "z0": grid_z0, "spacing": 1.0 / fs,
            "width": width, "height": height,
            "heights_m": surface.reshape(height, width).tolist(),
        }
        summary["routes"] = {
            f"rampe_{p['index']}": {
                "station_map_units": p["station"].tolist(),
                "station_m": (p["station"] * CELL_M).tolist(),
                "coords_map": p["coords"].tolist(),
                "source_h_m": p["h0"].tolist(),
                "solution_h_m": xsol[h_offsets[i]:h_offsets[i] + len(p["h0"])].tolist(),
            }
            for i, p in enumerate(profiles)
        }
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {key: value for key, value in summary.items() if key not in {"surface_grid", "routes"}}
    print(json.dumps(compact, indent=2, sort_keys=True))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--grade", type=float, choices=(0.45, 0.60), required=True)
    ap.add_argument("--r3-limit", type=int, default=None, help="omit for isolated surface bound without R3 rows")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--reference-mesh", type=Path, help="p3d16 relief JSON gzip; its GB field is used only for the deterministic minimax tie-break")
    ap.add_argument("--axis-tolerance", type=float, default=0.0)
    ap.add_argument("--plane-tolerance", type=float, default=0.02)
    args = ap.parse_args()
    with gzip.open(RELIEF, "rt", encoding="utf-8") as f:
        data = json.load(f)
    summary = solve(data, args.grade, args.r3_limit, args.out, args.reference_mesh, args.axis_tolerance, args.plane_tolerance)
    summary["source_relief_sha256"] = hashlib.sha256(RELIEF.read_bytes()).hexdigest()
    summary["tie_break_reference_sha256"] = (
        hashlib.sha256(args.reference_mesh.read_bytes()).hexdigest()
        if args.reference_mesh else None
    )
    args.out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
