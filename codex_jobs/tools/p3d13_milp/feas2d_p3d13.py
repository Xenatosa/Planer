#!/usr/bin/env python3
"""Measure joint ramp-profile feasibility with 2D grade and exact R3 gates.

Run from the worktree root:
    python3 codex_jobs/tools/p3d13_milp/feas2d_p3d13.py

The profiles are sampled from the read-only GB source at the same 0.25 map-
unit intervals used by pruefe_regeln.py.  Outputs are deterministic JSON files
beside this script, one per requested cross-slope limit.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point, box


ROOT = Path(__file__).resolve().parents[3]
RELIEF_DIR = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
RELIEF_PATH = RELIEF_DIR / "relief_daten.json.gz"
VECTOR_PATH = RELIEF_DIR / "neu/vektor.json"
CELL_M = 1.2
SAMPLE_STEP = 0.25
R3_SIGMA = 8.0
R3_TOL = 0.075
R3_SECTION_SAMPLES = 16
SLOPE_MAX = 0.60
PLANE_RADIUS_M = 2.25
PLANE_DEVIATION_M = 0.05
PLANE_SLOPE_MAX = 0.03
PAIR_RADIUS_M = 4.5
END_PIN_COORD = 1.0
WALL_TAIL_START = 40.0
WALL_TAIL_TOL = 0.25
CROSSING = np.array([152.5, 28.5], dtype=np.float64)
D1_BOUNDS = (126.0, 0.0, 168.0, 43.0)


def interp_height(heights: np.ndarray, coords: np.ndarray, rs: int) -> np.ndarray:
    # Matches pruefe_regeln.py's hf() order, coordinates and nearest boundary.
    return ndi.map_coordinates(
        heights,
        [coords[:, 1] * rs, coords[:, 0] * rs],
        order=1,
        mode="nearest",
    ).astype(np.float64)


def profile_path(path: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    cumulative = np.r_[0.0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))]
    station = np.arange(0.0, cumulative[-1] + 1e-7, SAMPLE_STEP, dtype=np.float64)
    coords = np.column_stack((
        np.interp(station, cumulative, path[:, 0]),
        np.interp(station, cumulative, path[:, 1]),
    ))
    return station, coords


def close_pairs(
    profiles: list[dict], max_distance_m: float, same_route_arc_distance_factor: float,
) -> list[tuple[int, int, int, int, float]]:
    """Return every eligible (route, sample, route, sample, distance_m) pair."""
    pairs: list[tuple[int, int, int, int, float]] = []
    trees = [cKDTree(np.asarray(p["coords"]) * CELL_M) for p in profiles]
    coords_m = [np.asarray(p["coords"]) * CELL_M for p in profiles]
    stations_m = [np.asarray(p["station"]) * CELL_M for p in profiles]
    for a in range(len(profiles)):
        for b in range(a, len(profiles)):
            neighbors = trees[b].query_ball_tree(trees[a], max_distance_m) if a != b else None
            if a == b:
                neighbor_lists = trees[a].query_ball_point(coords_m[a], max_distance_m)
                candidates = (
                    (i, j)
                    for i, js in enumerate(neighbor_lists)
                    for j in sorted(js)
                    if j > i
                )
            else:
                # query_ball_tree returns one sorted-by-index neighbor list per
                # point in tree b, listing matches in tree a.
                candidates = (
                    (i, j)
                    for j, is_ in enumerate(neighbors)
                    for i in sorted(is_)
                )
            for i, j in candidates:
                distance = float(np.linalg.norm(coords_m[a][i] - coords_m[b][j]))
                if distance <= max_distance_m + 1e-9:
                    if (
                        a == b
                        and stations_m[a][j] - stations_m[a][i]
                        <= same_route_arc_distance_factor * distance + 1e-9
                    ):
                        continue
                    pairs.append((a, i, b, j, distance))
    return pairs


def add_pair_rows(
    pairs: list[tuple[int, int, int, int, float]],
    offsets: list[int],
    variables: int,
    gradient_limit: float,
) -> list[tuple[dict[int, float], float]]:
    rows: list[tuple[dict[int, float], float]] = []
    for ra, ia, rb, ib, distance in pairs:
        va, vb = offsets[ra] + ia, offsets[rb] + ib
        bound = gradient_limit * distance
        if va == vb:
            continue
        rows.append(({va: 1.0, vb: -1.0}, bound))
        rows.append(({va: -1.0, vb: 1.0}, bound))
    return rows


def solve_for_gradient(profiles: list[dict], slope: float, output_path: Path) -> dict:
    lengths = [len(p["h0"]) for p in profiles]
    h_offsets = np.cumsum([0, *lengths[:-1]]).astype(int).tolist()
    total_h = sum(lengths)
    deviation_start = total_h
    section_offsets = np.cumsum([0, *[(n + 15) // 16 for n in lengths[:-1]]]).astype(int).tolist()
    section_counts = [(n + 15) // 16 for n in lengths]
    binary_start = total_h * 2
    total_sections = sum(section_counts)
    plane_height_index = binary_start + total_sections
    plane_gx_index = plane_height_index + 1
    plane_gz_index = plane_height_index + 2
    variable_count = plane_height_index + 3

    lower = np.empty(variable_count, dtype=np.float64)
    upper = np.empty(variable_count, dtype=np.float64)
    h0_flat = np.empty(total_h, dtype=np.float64)
    for route, profile in enumerate(profiles):
        h0 = np.asarray(profile["h0"], dtype=np.float64)
        station = np.asarray(profile["station"], dtype=np.float64)
        coords = np.asarray(profile["coords"], dtype=np.float64)
        start = h_offsets[route]
        h0_flat[start:start + len(h0)] = h0
        lo, hi = h0 - 2.0, h0 + 2.0
        x0, z0, x1, z1 = D1_BOUNDS
        edge_distance_m = np.minimum.reduce((
            coords[:, 0] - x0,
            x1 - coords[:, 0],
            coords[:, 1] - z0,
            z1 - coords[:, 1],
        )) * CELL_M
        fixed = (station <= END_PIN_COORD + 1e-9) | (station >= station[-1] - END_PIN_COORD - 1e-9)
        fixed |= edge_distance_m < 3.0 - 1e-8
        if profile["index"] == 11:
            tail = station >= WALL_TAIL_START - 1e-9
            lo[tail] = np.maximum(lo[tail], h0[tail] - WALL_TAIL_TOL)
            hi[tail] = np.minimum(hi[tail], h0[tail] + WALL_TAIL_TOL)
        lo[fixed] = h0[fixed]
        hi[fixed] = h0[fixed]
        lower[start:start + len(h0)] = lo
        upper[start:start + len(h0)] = hi
        profile["bounds_lo"] = lo
        profile["bounds_hi"] = hi

    lower[deviation_start:binary_start] = 0.0
    upper[deviation_start:binary_start] = 2.0
    lower[binary_start:plane_height_index] = 0.0
    upper[binary_start:plane_height_index] = 1.0
    plane_mask_heights = [
        p["h0"][np.flatnonzero(np.linalg.norm((p["coords"] - CROSSING) * CELL_M, axis=1) <= PLANE_RADIUS_M + 1e-9)]
        for p in profiles
    ]
    plane_values = np.concatenate([a for a in plane_mask_heights if len(a)])
    lower[plane_height_index] = float(plane_values.min() - 2.0)
    upper[plane_height_index] = float(plane_values.max() + 2.0)
    lower[plane_gx_index:plane_gz_index + 1] = -PLANE_SLOPE_MAX
    upper[plane_gx_index:plane_gz_index + 1] = PLANE_SLOPE_MAX

    integrality = np.zeros(variable_count, dtype=np.uint8)
    integrality[binary_start:plane_height_index] = 1
    row_indices: list[int] = []
    col_indices: list[int] = []
    values: list[float] = []
    row_upper: list[float] = []

    def add_row(entries: dict[int, float], hi: float) -> None:
        row = len(row_upper)
        for col, value in entries.items():
            if abs(value) > 1e-13:
                row_indices.append(row)
                col_indices.append(int(col))
                values.append(float(value))
        row_upper.append(float(hi))

    # L1 movement from the unchanged GB source surface (p3d10 objective).
    for route, profile in enumerate(profiles):
        start = h_offsets[route]
        for k, h0 in enumerate(profile["h0"]):
            d = deviation_start + start + k
            add_row({start + k: 1.0, d: -1.0}, float(h0))
            add_row({start + k: -1.0, d: -1.0}, float(-h0))

    section_descriptions = []
    for route, profile in enumerate(profiles):
        h0 = np.asarray(profile["h0"], dtype=np.float64)
        station = np.asarray(profile["station"], dtype=np.float64)
        start = h_offsets[route]
        section_start = section_offsets[route]
        operator = np.eye(len(h0), dtype=np.float64) - ndi.gaussian_filter1d(
            np.eye(len(h0), dtype=np.float64), sigma=R3_SIGMA, axis=0, mode="nearest",
        )
        lo_h, hi_h = profile["bounds_lo"], profile["bounds_hi"]
        for k, op_row in enumerate(operator):
            active = np.flatnonzero(np.abs(op_row) > 1e-12)
            binary = binary_start + section_start + k // R3_SECTION_SAMPLES
            row = {start + int(j): float(op_row[j]) for j in active}
            max_value = sum(float(op_row[j]) * (hi_h[j] if op_row[j] >= 0 else lo_h[j]) for j in active)
            min_value = sum(float(op_row[j]) * (lo_h[j] if op_row[j] >= 0 else hi_h[j]) for j in active)
            upper_relaxation = max(0.0, max_value - R3_TOL)
            lower_relaxation = max(0.0, -min_value - R3_TOL)
            add_row({**row, binary: -upper_relaxation}, R3_TOL)
            add_row({**{j: -v for j, v in row.items()}, binary: -lower_relaxation}, R3_TOL)
            if k % R3_SECTION_SAMPLES == 0:
                x, z = profile["coords"][k]
                in_d1 = D1_BOUNDS[0] <= x <= D1_BOUNDS[2] and D1_BOUNDS[1] <= z <= D1_BOUNDS[3]
                section_descriptions.append({
                    "route": profile["index"],
                    "section": k // R3_SECTION_SAMPLES,
                    "start_station": round(float(station[k]), 6),
                    "x": round(float(x), 6),
                    "z": round(float(z), 6),
                    "in_D1": bool(in_d1),
                    "binary": binary,
                })
            if k + 1 < len(h0):
                add_row({start + k + 1: 1.0, start + k: -1.0}, SLOPE_MAX * SAMPLE_STEP)
                add_row({start + k: 1.0, start + k + 1: -1.0}, SLOPE_MAX * SAMPLE_STEP)

        coords = np.asarray(profile["coords"], dtype=np.float64)
        in_plane = np.flatnonzero(np.linalg.norm((coords - CROSSING) * CELL_M, axis=1) <= PLANE_RADIUS_M + 1e-9)
        for k in in_plane:
            dx_m, dz_m = (coords[k] - CROSSING) * CELL_M
            # |h - (Hc + gx*dx + gz*dz)| <= 5 cm.
            add_row({start + int(k): 1.0, plane_height_index: -1.0,
                     plane_gx_index: -float(dx_m), plane_gz_index: -float(dz_m)}, PLANE_DEVIATION_M)
            add_row({start + int(k): -1.0, plane_height_index: 1.0,
                     plane_gx_index: float(dx_m), plane_gz_index: float(dz_m)}, PLANE_DEVIATION_M)

    # A 32-sided inscribed polygon conservatively enforces a 3% vector slope.
    polygon_bound = PLANE_SLOPE_MAX * np.cos(np.pi / 32.0)
    for angle in np.arange(32, dtype=np.float64) * (2.0 * np.pi / 32.0):
        add_row({plane_gx_index: float(np.cos(angle)), plane_gz_index: float(np.sin(angle))}, float(polygon_bound))

    pairs = close_pairs(
        profiles, PAIR_RADIUS_M, same_route_arc_distance_factor=1.5,
    )
    same_route_pair_count = sum(1 for a, _, b, _, _ in pairs if a == b)
    cross_route_pair_count = len(pairs) - same_route_pair_count
    pair_rows = add_pair_rows(pairs, h_offsets, variable_count, slope)
    for entries, limit in pair_rows:
        add_row(entries, limit)

    def constraints() -> LinearConstraint:
        matrix = coo_matrix(
            (values, (row_indices, col_indices)),
            shape=(len(row_upper), variable_count),
        ).tocsr()
        return LinearConstraint(matrix, np.full(len(row_upper), -np.inf), np.asarray(row_upper))

    bounds = Bounds(lower, upper)
    section_objective = np.zeros(variable_count, dtype=np.float64)
    section_objective[binary_start:plane_height_index] = 1.0
    first = milp(
        section_objective, integrality=integrality, bounds=bounds,
        constraints=constraints(), options={"presolve": True, "mip_rel_gap": 0.0, "time_limit": 600},
    )
    result = {
        "g_m_per_m": slope,
        "status_code": int(first.status),
        "solver_status": str(first.message),
        "eligible_pair_count": len(pairs),
        "same_route_eligible_pair_count": same_route_pair_count,
        "cross_route_eligible_pair_count": cross_route_pair_count,
        "pair_constraints": len(pair_rows),
        "station_count": {f"rampe_{p['index']}": len(p["h0"]) for p in profiles},
        "r3_sections_total": None,
        "r3_sections_D1": None,
    }
    if first.x is None:
        result["status"] = "infeasible_or_no_incumbent"
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return result

    minimum_sections = int(round(float(first.fun)))
    result["r3_sections_total"] = minimum_sections
    section_values = first.x[binary_start:plane_height_index]
    result["r3_sections_D1"] = int(sum(
        section_values[item["binary"] - binary_start] > 0.5
        for item in section_descriptions if item["in_D1"]
    ))
    result["minimum_section_solution_is_within_six"] = minimum_sections <= 6
    result["r3_sections_over_threshold"] = [
        {k: v for k, v in item.items() if k != "binary"}
        for item in section_descriptions
        if section_values[item["binary"] - binary_start] > 0.5
    ]
    result["status"] = "optimal_minimum_sections"
    second = None
    if minimum_sections <= 6:
        # Freeze the optimal R3 count, then use p3d10's source L1 movement goal.
        add_row({j: 1.0 for j in range(binary_start, plane_height_index)}, float(minimum_sections))
        movement_objective = np.zeros(variable_count, dtype=np.float64)
        movement_objective[deviation_start:binary_start] = 1.0
        second = milp(
            movement_objective, integrality=integrality, bounds=bounds,
            constraints=constraints(), options={"presolve": True, "mip_rel_gap": 0.0, "time_limit": 600},
        )
        if second.x is not None:
            xsol = second.x
            result["source_l1_delta_m"] = round(float(xsol[deviation_start:binary_start].sum()), 6)
            result["max_abs_delta_m"] = round(float(np.max(np.abs(xsol[:total_h] - h0_flat))), 6)
            result["Hc_m"] = round(float(xsol[plane_height_index]), 6)
            result["plane_gradient_x"] = round(float(xsol[plane_gx_index]), 9)
            result["plane_gradient_z"] = round(float(xsol[plane_gz_index]), 9)
            result["plane_slope_pct"] = round(float(np.hypot(xsol[plane_gx_index], xsol[plane_gz_index]) * 100.0), 6)
            result["max_abs_pair_grade"] = round(max(
                (abs(xsol[h_offsets[ra] + ia] - xsol[h_offsets[rb] + ib]) / max(d, 1e-12)
                 for ra, ia, rb, ib, d in pairs), default=0.0,
            ), 6)
            result["second_solver_status"] = str(second.message)
            result["routes"] = {}
            for route, profile in enumerate(profiles):
                start = h_offsets[route]
                h = xsol[start:start + lengths[route]]
                residual = h - ndi.gaussian_filter1d(h, sigma=R3_SIGMA, mode="nearest")
                sections = []
                for k in range(0, len(h), R3_SECTION_SAMPLES):
                    stop = min(k + R3_SECTION_SAMPLES, len(h))
                    x, z = profile["coords"][k]
                    in_d1 = D1_BOUNDS[0] <= x <= D1_BOUNDS[2] and D1_BOUNDS[1] <= z <= D1_BOUNDS[3]
                    sections.append({
                        "start_station": round(float(profile["station"][k]), 6),
                        "stop_station": round(float(profile["station"][stop - 1]), 6),
                        "max_abs_R3_m": round(float(np.max(np.abs(residual[k:stop]))), 6),
                        "in_D1": bool(in_d1),
                    })
                result["routes"][f"rampe_{profile['index']}"] = {
                    "station": profile["station"].tolist(),
                    "coords": profile["coords"].tolist(),
                    "h0_source": profile["h0"].tolist(),
                    "h_solution": h.tolist(),
                    "R3_residual": residual.tolist(),
                    "max_abs_delta_m": round(float(np.max(np.abs(h - profile["h0"]))), 6),
                    "max_slope": round(float(np.max(np.abs(np.diff(h) / (SAMPLE_STEP * CELL_M)))), 6),
                    "sections": sections,
                }
            result["status"] = "optimal_and_within_six" if result["r3_sections_D1"] <= 6 else "optimal_total_but_D1_over_six"
        else:
            result["status"] = "minimum_sections_found_but_L1_tiebreak_failed"
            result["second_solver_status"] = str(second.message)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    with gzip.open(RELIEF_PATH, "rt", encoding="utf-8") as handle:
        data = json.load(handle)
    heights = np.frombuffer(__import__("base64").b64decode(data["GB"]), dtype=np.float32).reshape(
        int(data["ny"]) * int(data["rs"]) + 1,
        int(data["nx"]) * int(data["rs"]) + 1,
    )
    rs = int(data["rs"])
    tile = box(*D1_BOUNDS)
    paths = data["rampenwege"]
    crossing = Point(*CROSSING)
    selected = []
    for index, raw_path in enumerate(paths):
        path = np.asarray(raw_path, dtype=np.float64)
        line = LineString(path)
        if not line.intersects(tile):
            continue
        station, coords = profile_path(path)
        h0 = interp_height(heights, coords, rs)
        selected.append({"index": index, "station": station, "coords": coords, "h0": h0})
    selected.sort(key=lambda p: p["index"])

    vector = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
    nearby_ways = []
    for way in vector.get("wege", []):
        points = way.get("mittellinie_m", [])
        if len(points) < 2:
            continue
        line = LineString(points)
        surface_distance_m = max(0.0, line.distance(crossing) * CELL_M - float(way.get("breite_m", 0.0)) / 2)
        if surface_distance_m <= 6.0 + 1e-9:
            nearby_ways.append({"id": way.get("id"), "klasse": way.get("klasse"), "distance_m": round(surface_distance_m, 6)})

    if [p["index"] for p in selected] != [2, 11]:
        raise RuntimeError(f"D1-Rampen unerwartet: {[p['index'] for p in selected]}")
    if nearby_ways:
        raise RuntimeError(f"Weitere Wegflaechen innerhalb 6 m erfordern Profilaufnahme: {nearby_ways}")

    all_results = []
    for gradient in (0.60, 0.45):
        output = Path(__file__).resolve().parent / f"machbarkeit_g{int(gradient * 100):02d}.json"
        result = solve_for_gradient(selected, gradient, output)
        all_results.append({
            "g": gradient,
            "status": result["status"],
            "r3_sections_total": result["r3_sections_total"],
            "r3_sections_D1": result["r3_sections_D1"],
            "Hc_m": result.get("Hc_m"),
            "max_abs_delta_m": result.get("max_abs_delta_m"),
            "max_abs_pair_grade": result.get("max_abs_pair_grade"),
            "eligible_pair_count": result["eligible_pair_count"],
            "same_route_eligible_pair_count": result["same_route_eligible_pair_count"],
            "cross_route_eligible_pair_count": result["cross_route_eligible_pair_count"],
        })
    summary = {
        "source": str(RELIEF_PATH.relative_to(ROOT)),
        "ramp_indices_in_D1": [p["index"] for p in selected],
        "additional_ways_within_6m": nearby_ways,
        "station_step_coordinate_units": SAMPLE_STEP,
        "station_step_m": SAMPLE_STEP * CELL_M,
        "plane_center": CROSSING.tolist(),
        "plane_radius_m": PLANE_RADIUS_M,
        "results": all_results,
    }
    out = Path(__file__).resolve().parent / "machbarkeit.json"
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
