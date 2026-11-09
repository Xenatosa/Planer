#!/usr/bin/env python3
"""Find the lowest possible R8 neighbor step under D1 axis and plane supports.

This is a feasibility bound, not a replacement gate: it minimizes the largest
0.25-map-unit height difference in the exact R8 road mask around 152.5|28.5,
while holding the g=0.45 MILP axis profile and r<=2.25 m plane to +/-0.02 m.
The local 0.25-map-unit raster is freer than the delivered 0.5-map-unit mesh,
so a minimum above the requested step would be a conservative conflict proof.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


ROOT = Path(__file__).resolve().parents[3]
RELIEF_DIR = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
DEFAULT_MESH = Path("/tmp/relief_neu_gate_p3d15_final.json.gz")
DEFAULT_MILP = Path(__file__).resolve().parent / "machbarkeit_g45.json"
CENTER = (152.5, 28.5)
CELL_M = 1.2


def read_gzip_json(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def sample_path(raw: list[list[float]], step: float = 0.25) -> np.ndarray:
    path = np.asarray(raw, dtype=np.float64)
    lengths = np.hypot(*np.diff(path, axis=0).T)
    cumulative = np.r_[0.0, np.cumsum(lengths)]
    station = np.arange(0.0, cumulative[-1] + 1e-6, step)
    return np.column_stack((
        np.interp(station, cumulative, path[:, 0]),
        np.interp(station, cumulative, path[:, 1]),
    ))


def bilinear_row(x: float, z: float, x0: float, z0: float, fs: int, width: int) -> dict[int, float]:
    u, v = (x - x0) * fs, (z - z0) * fs
    ix, iz = int(np.floor(u)), int(np.floor(v))
    ix = min(max(ix, 0), width - 2)
    iz = min(max(iz, 0), width - 2)
    fu, fv = u - ix, v - iz
    return {
        iz * width + ix: (1.0 - fu) * (1.0 - fv),
        iz * width + ix + 1: fu * (1.0 - fv),
        (iz + 1) * width + ix: (1.0 - fu) * fv,
        (iz + 1) * width + ix + 1: fu * fv,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mesh", type=Path, default=DEFAULT_MESH)
    ap.add_argument("--milp", type=Path, default=DEFAULT_MILP)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "minimax_r8_surface_p3d15.json")
    ap.add_argument("--axis-tolerance", type=float, default=0.02)
    ap.add_argument("--plane-tolerance", type=float, default=0.02)
    ap.add_argument("--plane-radius-m", type=float, default=2.25)
    args = ap.parse_args()
    data = read_gzip_json(args.mesh)
    solution = json.loads(args.milp.read_text(encoding="utf-8"))
    nx, ny, rs = int(data["nx"]), int(data["ny"]), int(data["rs"])
    fs = int(data["FW"]["fs"])
    fine_shape = (ny * fs + 1, nx * fs + 1)

    # Recreate the road mask used by r8_kreuzung.py.
    ramp_samples = [sample_path(path) for path in data["rampenwege"]]
    road_cells = np.zeros((ny, nx), dtype=bool)
    for x, z in data["wege"]:
        road_cells[int(z), int(x)] = True
    weg_a = np.frombuffer(base64.b64decode(data["WEGA"]), dtype=np.uint8).reshape(
        ny * rs + 1, nx * rs + 1,
    )
    road_cells |= weg_a[:-1:rs, :-1:rs] > 20
    ramp_cells = np.zeros_like(road_cells)
    for path in ramp_samples:
        ramp_cells[np.clip(path[:, 1].astype(int), 0, ny - 1),
                   np.clip(path[:, 0].astype(int), 0, nx - 1)] = True
    _road_without_ramps = road_cells & ~ndi.binary_dilation(ramp_cells, iterations=1)

    road_mask = np.zeros(fine_shape, dtype=bool)
    for path in ramp_samples:
        road_mask[
            np.clip(np.rint(path[:, 1] * fs).astype(int), 0, fine_shape[0] - 1),
            np.clip(np.rint(path[:, 0] * fs).astype(int), 0, fine_shape[1] - 1),
        ] = True
    road_mask = ndi.distance_transform_edt(~road_mask) / fs <= 1.5
    road_mask[:-1, :-1] |= np.kron(road_cells, np.ones((fs, fs), dtype=bool))

    cx, cz = CENTER
    xmin, xmax = cx - 4.0, cx + 4.0
    zmin, zmax = cz - 4.0, cz + 4.0
    ix0, ix1 = round(xmin * fs), round(xmax * fs)
    iz0, iz1 = round(zmin * fs), round(zmax * fs)
    x0, z0 = ix0 / fs, iz0 / fs
    width, height = ix1 - ix0 + 1, iz1 - iz0 + 1
    local_road = road_mask[iz0:iz1 + 1, ix0:ix1 + 1].copy()
    zz, xx = np.mgrid[iz0:iz1 + 1, ix0:ix1 + 1]
    local_road &= np.hypot(xx / fs - cx, zz / fs - cz) <= 4.0 + 1e-9

    # Local 0.25-map-unit height variables plus the minimax step t.
    count = width * height
    t_index = count
    row_ids: list[int] = []
    col_ids: list[int] = []
    values: list[float] = []
    upper: list[float] = []
    pairs: list[tuple[int, int]] = []

    def add(entries: dict[int, float], bound: float) -> None:
        row = len(upper)
        for col, value in entries.items():
            if abs(value) > 1e-13:
                row_ids.append(row)
                col_ids.append(int(col))
                values.append(float(value))
        upper.append(float(bound))

    # Every checker-measured adjacent road pair is constrained by the same t.
    pair_count = 0
    for axis in (0, 1):
        ys, xs = np.nonzero(local_road)
        if axis == 0:
            keep = (ys + 1 < height) & local_road[np.minimum(ys + 1, height - 1), xs]
            aa, bb = ys[keep] * width + xs[keep], (ys[keep] + 1) * width + xs[keep]
        else:
            keep = (xs + 1 < width) & local_road[ys, np.minimum(xs + 1, width - 1)]
            aa, bb = ys[keep] * width + xs[keep], ys[keep] * width + xs[keep] + 1
        for a, b in zip(aa, bb):
            add({int(a): 1.0, int(b): -1.0, t_index: -1.0}, 0.0)
            add({int(a): -1.0, int(b): 1.0, t_index: -1.0}, 0.0)
            pair_count += 1
            pairs.append((int(a), int(b)))

    # Hard axis supports from the g=0.45 MILP, restricted to the R8 neighborhood.
    axis_rows = 0
    for name in ("rampe_2", "rampe_11"):
        route = solution["routes"][name]
        coords = np.asarray(route["coords"], dtype=np.float64)
        targets = np.asarray(route["h_solution"], dtype=np.float64)
        inside = (
            (coords[:, 0] >= x0 - 1e-9) & (coords[:, 0] <= x0 + (width - 1) / fs + 1e-9)
            & (coords[:, 1] >= z0 - 1e-9) & (coords[:, 1] <= z0 + (height - 1) / fs + 1e-9)
        )
        for point, target in zip(coords[inside], targets[inside]):
            row = bilinear_row(float(point[0]), float(point[1]), x0, z0, fs, width)
            add(row, float(target) + args.axis_tolerance)
            add({key: -value for key, value in row.items()}, -float(target) + args.axis_tolerance)
            axis_rows += 1

    # The plane core is held at the MILP plane to +/- 2 cm at every fine support.
    plane_rows = 0
    h0 = float(solution["Hc_m"])
    gx, gz = float(solution["plane_gradient_x"]), float(solution["plane_gradient_z"])
    for iz in range(height):
        for ix in range(width):
            x, z = x0 + ix / fs, z0 + iz / fs
            dx, dz = (x - cx) * CELL_M, (z - cz) * CELL_M
            if np.hypot(dx, dz) > args.plane_radius_m + 1e-9:
                continue
            target = h0 + gx * dx + gz * dz
            index = iz * width + ix
            add({index: 1.0}, target + args.plane_tolerance)
            add({index: -1.0}, -target + args.plane_tolerance)
            plane_rows += 1

    matrix = coo_matrix(
        (values, (row_ids, col_ids)), shape=(len(upper), count + 1),
    ).tocsr()
    objective = np.zeros(count + 1, dtype=np.float64)
    objective[t_index] = 1.0
    bounds = [(None, None)] * count + [(0.0, None)]
    result = linprog(
        objective, A_ub=matrix, b_ub=np.asarray(upper), bounds=bounds, method="highs",
    )
    worst_pair = None
    if result.success and pairs:
        surface = result.x[:count]
        pair_steps = np.asarray([abs(surface[a] - surface[b]) for a, b in pairs])
        worst_index = int(np.argmax(pair_steps))
        a, b = pairs[worst_index]

        def point_detail(index: int) -> dict:
            iz, ix = divmod(index, width)
            x, z = x0 + ix / fs, z0 + iz / fs
            nearest = []
            for route_index in (2, 11):
                path = ramp_samples[route_index]
                distance = np.linalg.norm(path - np.asarray([x, z]), axis=1)
                j = int(np.argmin(distance))
                nearest.append({
                    "route": f"rampe_{route_index}",
                    "station_m": round(j * 0.25 * CELL_M, 4),
                    "distance_m": round(float(distance[j] * CELL_M), 4),
                })
            nearest.sort(key=lambda item: (item["distance_m"], item["route"]))
            return {"x": round(x, 4), "z": round(z, 4), "height_m": round(float(surface[index]), 6), "nearest_routes": nearest}

        worst_pair = {
            "step_m": round(float(pair_steps[worst_index]), 9),
            "a": point_detail(a),
            "b": point_detail(b),
        }
    output = {
        "status": str(result.message),
        "success": bool(result.success),
        "center": list(CENTER),
        "local_fine_shape": [height, width],
        "checker_neighbor_pairs": int(pair_count),
        "axis_supports": int(axis_rows),
        "plane_core_supports": int(plane_rows),
        "plane_radius_m": args.plane_radius_m,
        "axis_tolerance_m": args.axis_tolerance,
        "plane_tolerance_m": args.plane_tolerance,
        "milp_pair_grade": 0.45,
        "r3_sections_D1": solution.get("r3_sections_D1"),
        "minimum_neighbor_step_m": float(result.fun) if result.success else None,
        "minimum_neighbor_grade_pct": float(result.fun / (CELL_M / fs) * 100.0) if result.success else None,
        "minimum_surface_worst_pair": worst_pair,
        "mesh_relaxation": "independent 0.25-map-unit raster; more degrees of freedom than the delivered 0.5-map-unit mesh",
    }
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))
    if not result.success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
