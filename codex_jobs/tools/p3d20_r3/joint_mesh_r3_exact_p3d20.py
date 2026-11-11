#!/usr/bin/env python3
"""p3d20: p3d18 transfer plus official-counter-directed G5/R5/R4 cuts.

The p3d19 R8/R3/axis safety constraints are inherited. Local height pins and
R9w locks are omitted. Exact checker measurements on float32 direct-transfer
candidates add local event cuts for G5, R5-loch and R4.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace

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
R3_TOL = 0.08
R3_SECTION_SAMPLES = 16
R3_FLOAT32_GUARD_M = 1e-5
R3_FLOAT32_GUARD_PCT = 3e-4
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
R8_GITTER_LIMIT_M = float(os.environ.get("P3D20_MODEL_GITTER_LIMIT", "0.019"))
R8_QUER_LIMIT_PCT = float(os.environ.get("P3D20_MODEL_QUER_LIMIT", "2.95"))
R3_SINGLE_QUER_LIMIT_PCT = float(os.environ.get("P3D20_MODEL_SINGLE_QUER_LIMIT", "19.5"))
D1_BOUNDS = (126.0, 0.0, 168.0, 43.0)
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
OFFICIAL_RULES = RELIEF3D / "pruefung/pruefe_regeln.py"


def p3d17_transfer_context() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """Capture the unchanged p3d17 transfer's fixed background and support."""
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    from neu import mesh as neu_mesh

    source = neu_mesh.load_relief(RELIEF)
    vector = json.loads((RELIEF3D / "neu/vektor.json").read_text(encoding="utf-8"))
    with np.load(RELIEF3D / "neu/felder.npz", allow_pickle=False) as archive:
        fields = {name: archive[name] for name in archive.files}

    captured: dict = {}
    original = neu_mesh._apply_d1_joint_solution_transfer
    original_endpoint = neu_mesh._apply_ramp_endpoint_runouts

    def capture_endpoint(*args, **kwargs):
        result = original_endpoint(*args, **kwargs)
        captured["endpoint_weight"] = np.asarray(result[1], dtype=np.float64).copy()
        return result

    def capture(result, background, profiles, solved, solver_info, crossing_m, settings, x, z):
        captured["background"] = np.asarray(background, dtype=np.float64).copy()
        captured["target"] = np.asarray(solver_info["surface_grid"]["heights_m"], dtype=np.float64)
        captured["profiles"] = profiles
        captured["crossing_m"] = np.asarray(crossing_m, dtype=np.float64).copy()
        captured["settings"] = dict(settings)
        captured["x"] = np.asarray(x, dtype=np.float64).copy()
        captured["z"] = np.asarray(z, dtype=np.float64).copy()
        returned = original(result, background, profiles, solved, solver_info, crossing_m, settings, x, z)
        captured["inner_coverage"] = np.asarray(returned[0], dtype=np.float64).reshape(result.shape)
        return returned

    old_crossing = os.environ.get("RELIEF_KREUZUNG_VAR")
    old_endpoint = os.environ.get("RELIEF_WEGEND_VAR")
    os.environ["RELIEF_KREUZUNG_VAR"] = "22"
    os.environ["RELIEF_WEGEND_VAR"] = "1"
    neu_mesh._apply_d1_joint_solution_transfer = capture
    neu_mesh._apply_ramp_endpoint_runouts = capture_endpoint
    try:
        delivered, _ = neu_mesh.terrain_heights(source, "D1", vector, fields, variant="2")
    finally:
        neu_mesh._apply_d1_joint_solution_transfer = original
        neu_mesh._apply_ramp_endpoint_runouts = original_endpoint
        if old_crossing is None:
            os.environ.pop("RELIEF_KREUZUNG_VAR", None)
        else:
            os.environ["RELIEF_KREUZUNG_VAR"] = old_crossing
        if old_endpoint is None:
            os.environ.pop("RELIEF_WEGEND_VAR", None)
        else:
            os.environ["RELIEF_WEGEND_VAR"] = old_endpoint

    if not captured or [int(p["index"]) for p in captured["profiles"]] != [2, 11]:
        raise RuntimeError("Konnte den unveraenderten p3d17-Transfer nicht kalibrieren")
    inner_coverage = d1_transfer_coverage(
        captured["profiles"], captured["x"], captured["z"],
        captured["crossing_m"], captured["settings"],
    )
    if not np.allclose(inner_coverage, captured["inner_coverage"], atol=1e-12, rtol=0.0):
        raise RuntimeError("Die nachgebildete p3d17-Deckung weicht vom Transferoperator ab")
    x, z = captured["x"], captured["z"]
    x0, z0, x1, z1 = D1_BOUNDS
    edge_m = np.minimum.reduce((x - x0, x1 - x, z - z0, z1 - z)) * 1.2
    tile_weight = neu_mesh._smoothstep(0.0, 3.0, edge_m)
    wall_distance = neu_mesh._sample_field(fields["wand"], x, z)
    wall_weight = neu_mesh._smoothstep(1.2, 4.8, wall_distance)
    endpoint_weight = captured.get("endpoint_weight", np.zeros_like(tile_weight))
    outer_weight = tile_weight * np.maximum.reduce((
        wall_weight, np.zeros_like(wall_weight), inner_coverage, endpoint_weight,
    ))
    cliff_distance = np.hypot((x - 140.0) * 1.2, (z - 35.0) * 1.2)
    outer_weight[cliff_distance <= 1.0] = 0.0
    rs = int(source.data["rs"])
    sx0, sz0, sx1, sz1 = [int(v * rs) for v in (x0, z0, x1, z1)]
    source_base = source.heights[sz0:sz1 + 1, sx0:sx1 + 1].astype(np.float64)
    coverage = outer_weight * inner_coverage
    transfer_fixed = source_base + outer_weight * (
        captured["background"] * (1.0 - inner_coverage) - source_base
    )
    reconstructed = (transfer_fixed + coverage * captured["target"]).astype("<f4")
    if not np.array_equal(reconstructed, delivered):
        raise RuntimeError(
            "P3D17-Transferkoeffizienten reproduzieren das ausgegebene Raster nicht: "
            f"max_delta={float(np.max(np.abs(reconstructed - delivered))):.9g} m"
        )
    return transfer_fixed, coverage, delivered, captured


def d1_transfer_coverage(profiles, x, z, crossing_m, settings) -> np.ndarray:
    """Return the unchanged p3d17 blend weight at each D1 mesh vertex."""
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    from neu.mesh import CELL_M, _project_to_ramp_strip, _smoothstep

    query = np.column_stack((x.ravel() * CELL_M, z.ravel() * CELL_M))
    uncovered = np.ones(len(query), dtype=np.float64)
    band = float(settings["band_m"])
    fade = float(settings["fade_m"])
    for profile in profiles:
        coords = np.asarray(profile["coords"], dtype=np.float64)
        direction = np.gradient(coords, axis=0)
        direction /= np.maximum(np.linalg.norm(direction, axis=1, keepdims=True), 1e-9)
        normals = np.column_stack((-direction[:, 1], direction[:, 0]))
        _, lateral, _ = _project_to_ramp_strip(
            query, coords, np.asarray(profile["stations"], dtype=np.float64), normals, band,
        )
        path_m = coords * CELL_M
        start_tangent = path_m[1] - path_m[0]
        start_tangent /= max(float(np.hypot(*start_tangent)), 1e-12)
        end_tangent = path_m[-1] - path_m[-2]
        end_tangent /= max(float(np.hypot(*end_tangent)), 1e-12)
        valid = ~(((query - path_m[0]) @ start_tangent) < -1e-8)
        valid &= ~(((query - path_m[-1]) @ end_tangent) > 1e-8)
        route_cover = (1.0 - _smoothstep(band, band + fade, lateral)) * valid
        uncovered *= 1.0 - np.clip(route_cover, 0.0, 1.0)
    profile_cover = 1.0 - uncovered
    radius = np.linalg.norm(query - crossing_m[None, :], axis=1)
    plane_cover = 1.0 - _smoothstep(
        float(settings["plane_radius_m"]), float(settings["plane_outer_m"]), radius,
    )
    coverage = 1.0 - (1.0 - profile_cover) * (1.0 - plane_cover)
    gate_radius_map = float(settings.get("r8_transfer_radius_map", 0.0))
    if gate_radius_map > 0.0:
        gate_center_map = R8_GATE_CENTER
        gate_radius = np.linalg.norm(query / CELL_M - gate_center_map[None, :], axis=1)
        gate_cover = 1.0 - _smoothstep(
            gate_radius_map,
            gate_radius_map + float(settings.get("r8_fade_m", 0.0)) / CELL_M,
            gate_radius,
        )
        coverage = 1.0 - (1.0 - coverage) * (1.0 - gate_cover)
    return coverage.reshape(x.shape)


def highs_mip_solve(matrix, rhs, objective, integrality, lower, upper, start, time_limit=600.0):
    """Solve with a full incumbent start using the free HiGHS Python binding."""
    highspy_dir = Path("/tmp/p3d18_highspy")
    if str(highspy_dir) not in sys.path and highspy_dir.exists():
        sys.path.insert(0, str(highspy_dir))
    import highspy

    lp = highspy.HighsLp()
    lp.num_col_ = int(matrix.shape[1])
    lp.num_row_ = int(matrix.shape[0])
    lp.col_cost_ = np.asarray(objective, dtype=np.float64)
    lp.col_lower_ = np.asarray(lower, dtype=np.float64)
    lp.col_upper_ = np.asarray(upper, dtype=np.float64)
    lp.row_lower_ = np.full(matrix.shape[0], -np.inf, dtype=np.float64)
    lp.row_upper_ = np.asarray(rhs, dtype=np.float64)
    lp.sense_ = highspy.ObjSense.kMinimize
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_ = matrix.indptr.astype(np.int32, copy=False)
    lp.a_matrix_.index_ = matrix.indices.astype(np.int32, copy=False)
    lp.a_matrix_.value_ = matrix.data.astype(np.float64, copy=False)
    lp.integrality_ = [
        highspy.HighsVarType.kInteger if value else highspy.HighsVarType.kContinuous
        for value in np.asarray(integrality, dtype=np.uint8)
    ]

    highs = highspy.Highs()
    highs.setOptionValue("output_flag", False)
    highs.setOptionValue("presolve", "on")
    highs.setOptionValue("threads", 1)
    highs.setOptionValue("mip_rel_gap", 0.0)
    highs.setOptionValue("time_limit", float(time_limit))
    status = highs.passModel(lp)
    if status not in (highspy.HighsStatus.kOk, highspy.HighsStatus.kWarning):
        raise RuntimeError(f"HiGHS Modellannahme fehlgeschlagen: {status}")
    start = np.asarray(start, dtype=np.float64)
    if len(start) != matrix.shape[1]:
        raise ValueError(f"MIP-Start hat {len(start)} statt {matrix.shape[1]} Werte")
    start_status = highs.setSolution(
        matrix.shape[1], np.arange(matrix.shape[1], dtype=np.int32), start,
    )
    if start_status not in (highspy.HighsStatus.kOk, highspy.HighsStatus.kWarning):
        raise RuntimeError(f"HiGHS MIP-Start wurde abgelehnt: {start_status}")
    highs.run()
    model_status = highs.getModelStatus()
    solution = highs.getSolution()
    info = highs.getInfo()
    success = model_status == highspy.HighsModelStatus.kOptimal
    status_code = 0 if success else 1 if model_status == highspy.HighsModelStatus.kTimeLimit else 2
    return SimpleNamespace(
        success=success,
        status=status_code,
        message=highs.modelStatusToString(model_status),
        x=np.asarray(solution.col_value, dtype=np.float64) if solution.value_valid else None,
        fun=float(info.objective_function_value),
        mip_dual_bound=float(info.mip_dual_bound),
        mip_gap=float(info.mip_gap),
    )


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


def solve(
    data: dict,
    grade: float,
    r3_limit: int | None,
    out: Path,
    reference_mesh_path: Path | None,
    axis_tolerance: float,
    plane_tolerance: float,
    stage_limit: float | None = None,
    quer_limit: int | None = 7,
    wob_limit: int | None = 7,
    objective_mode: str = "step",
    relax_integrality: bool = False,
    mip_start_path: Path | None = None,
    mip_start_out: Path | None = None,
    time_limit_s: float = 600.0,
    event_cuts_path: Path | None = None,
    reference_solution_path: Path | None = None,
) -> dict:
    if objective_mode not in {"feasibility", "step", "quer", "wob"}:
        raise ValueError(f"Unbekannter Ziellauf: {objective_mode}")
    event_cuts = json.loads(event_cuts_path.read_text(encoding="utf-8")) if event_cuts_path else []
    event_cuts = list(event_cuts)
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

    transfer_background, transfer_coverage, p3d17_output, transfer_context = p3d17_transfer_context()

    # Recompute the exact p3d18 variant-24 reference for official-counter
    # comparisons; it is never used as a local height pin.
    from neu import mesh as neu_mesh
    source = neu_mesh.load_relief(RELIEF)
    vector = json.loads((RELIEF3D / "neu/vektor.json").read_text(encoding="utf-8"))
    with np.load(RELIEF3D / "neu/felder.npz", allow_pickle=False) as archive:
        fields = {name: archive[name] for name in archive.files}
    old_crossing = os.environ.get("RELIEF_KREUZUNG_VAR")
    old_endpoint = os.environ.get("RELIEF_WEGEND_VAR")
    os.environ["RELIEF_KREUZUNG_VAR"] = "24"
    os.environ["RELIEF_WEGEND_VAR"] = "1"
    try:
        p3d18_output, _ = neu_mesh.terrain_heights(source, "D1", vector, fields, variant="2")
    finally:
        if old_crossing is None:
            os.environ.pop("RELIEF_KREUZUNG_VAR", None)
        else:
            os.environ["RELIEF_KREUZUNG_VAR"] = old_crossing
        if old_endpoint is None:
            os.environ.pop("RELIEF_WEGEND_VAR", None)
        else:
            os.environ["RELIEF_WEGEND_VAR"] = old_endpoint
    p3d18_reference_hash = hashlib.sha256(p3d18_output.astype("<f4", copy=False).tobytes()).hexdigest()
    if p3d18_reference_hash != "9619da5083720eb43f736043452b28f87dd2f9aa946dc2cb453b5ed972d02c6c":
        raise RuntimeError("Die unveraenderte p3d18-Variante-24 Referenz passt nicht zum Bericht")

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
        quer_binary_index = {}
        wob_binary_index = {}
    else:
        binary_index = {item: binary_start + i for i, item in enumerate(r3_sections)}
        d1_sections = list(dict.fromkeys(
            (route, k // R3_SECTION_SAMPLES)
            for route, k, inside in section_lookup if inside
        ))
        quer_start = binary_start + len(binary_index)
        quer_binary_index = {item: quer_start + i for i, item in enumerate(d1_sections)}
        wob_start = quer_start + len(quer_binary_index)
        wob_binary_index = {item: wob_start + i for i, item in enumerate(d1_sections)}
    nvars = binary_start + len(binary_index) + len(quer_binary_index) + len(wob_binary_index)

    event_selector_indices: dict[tuple[int, int], int] = {}
    next_event_column = nvars
    for cut_i, cut in enumerate(event_cuts):
        choices = (4 if cut["kind"] == "G5" else 2 if cut["kind"] == "R4"
                   else 9 if cut["kind"] == "R5sp" else 0)
        for choice_i in range(choices):
            event_selector_indices[(cut_i, choice_i)] = next_event_column
            next_event_column += 1
    event_selector_count = next_event_column - nvars
    nvars = next_event_column

    lower = np.full(nvars, -np.inf, dtype=np.float64)
    upper = np.full(nvars, np.inf, dtype=np.float64)
    lower[:total_h], upper[:total_h] = lo_h, hi_h
    source_tile = gb[
        int(grid_z0 * rs):int(grid_z1 * rs) + 1,
        int(grid_x0 * rs):int(grid_x1 * rs) + 1,
    ].astype(np.float64)
    source_delta_limit = 4.0
    for index, cover in enumerate(transfer_coverage.ravel()):
        if cover <= 1e-12:
            continue
        fixed = float(transfer_background.ravel()[index])
        source_height = float(source_tile.ravel()[index])
        lower[surface_start + index] = (
            source_height - source_delta_limit - fixed
        ) / float(cover)
        upper[surface_start + index] = (
            source_height + source_delta_limit - fixed
        ) / float(cover)
    lower[t_index] = 0.0
    if stage_limit is not None:
        upper[t_index] = float(stage_limit)
    lower[plane_h] = float(min(np.min(p["h0"]) for p in profiles) - 2.0)
    upper[plane_h] = float(max(np.max(p["h0"]) for p in profiles) + 2.0)
    lower[plane_gx:plane_gz + 1], upper[plane_gx:plane_gz + 1] = -PLANE_SLOPE_MAX, PLANE_SLOPE_MAX
    integrality = np.zeros(nvars, dtype=np.uint8)
    for j in (*binary_index.values(), *quer_binary_index.values(), *wob_binary_index.values()):
        lower[j], upper[j], integrality[j] = 0.0, 1.0, 1
    for j in event_selector_indices.values():
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

    # p3d20 does not use local height pins or an R9w equality lock.
    hp_lock_count = 0
    regression_locks: dict[str, int] = {}

    # Bilinear evaluation at every checker sample on the emitted mesh raster.
    def mesh_row(px: float, pz: float) -> dict[int, float]:
        return bilinear_row(px, pz, grid_x0, grid_z0, fs, width)

    def route_field_row(px: float, pz: float) -> tuple[dict[int, float], float]:
        if (grid_x0 - 1e-9 <= px <= grid_x1 + 1e-9
                and grid_z0 - 1e-9 <= pz <= grid_z1 + 1e-9):
            raw = mesh_row(px, pz)
            entries: dict[int, float] = {}
            fixed = 0.0
            for index, weight in raw.items():
                iz, ix = divmod(index, width)
                support = float(transfer_coverage[iz, ix])
                coefficient = weight * support
                if abs(coefficient) > 1e-13:
                    entries[surface_start + index] = coefficient
                # `transfer_background` is the affine intercept of the actual
                # final transfer, not an unmodified terrain background.
                fixed += weight * float(transfer_background[iz, ix])
            return entries, fixed
        fixed = float(ndi.map_coordinates(
            gb, [[pz * rs], [px * rs]], order=1, mode="nearest",
        )[0])
        return {}, fixed

    def subtract_rows(left: dict[int, float], right: dict[int, float]) -> dict[int, float]:
        result = dict(left)
        for column, value in right.items():
            result[column] = result.get(column, 0.0) - value
        return {column: value for column, value in result.items() if abs(value) > 1e-13}

    def event_big_m(row: dict[int, float], fixed: float, threshold: float) -> float:
        maximum = fixed + sum(
            value * (upper[column] if value >= 0.0 else lower[column])
            for column, value in row.items()
        )
        return max(1e-6, maximum - threshold + 1e-5)

    # G5 and R4 cuts encode the checker's local comparison as a four-way or
    # two-way disjunction. R5 cuts compare a detected pit with its flood saddle.
    # The outer loop reruns the unchanged component counters after each solve.
    for cut_i, cut in enumerate(event_cuts):
        if cut["kind"] == "G5":
            point_row, point_fixed = route_field_row(*cut["point"])
            selectors = [event_selector_indices[(cut_i, i)] for i in range(4)]
            add({column: 1.0 for column in selectors}, 1.0)
            add({column: -1.0 for column in selectors}, -1.0)
            for choice_i, ref in enumerate(cut["references"]):
                ref_row, ref_fixed = route_field_row(*ref)
                row = subtract_rows(point_row, ref_row)
                fixed = point_fixed - ref_fixed
                threshold = 0.6 - 1e-5
                big_m = event_big_m(row, fixed, threshold)
                row[event_selector_indices[(cut_i, choice_i)]] = big_m
                add(row, threshold + big_m - fixed)
        elif cut["kind"] == "R4":
            center_row, center_fixed = route_field_row(*cut["center"])
            selectors = [event_selector_indices[(cut_i, i)] for i in range(2)]
            add({column: 1.0 for column in selectors}, 1.0)
            add({column: -1.0 for column in selectors}, -1.0)
            for choice_i, side in enumerate(cut["sides"]):
                side_row, side_fixed = route_field_row(*side)
                row = subtract_rows(side_row, center_row)
                fixed = side_fixed - center_fixed
                threshold = 1.5 - 1e-5
                big_m = event_big_m(row, fixed, threshold)
                row[event_selector_indices[(cut_i, choice_i)]] = big_m
                add(row, threshold + big_m - fixed)
        elif cut["kind"] == "R5":
            saddle_row, saddle_fixed = route_field_row(*cut["saddle"])
            for pit in cut.get("pits", [cut["pit"]]):
                pit_row, pit_fixed = route_field_row(*pit)
                row = subtract_rows(saddle_row, pit_row)
                add(row, 1.0 - 1e-5 - (saddle_fixed - pit_fixed))
        elif cut["kind"] == "G6":
            x, z = cut["point"]
            spacing = 1.0 / rs
            gx_terms = [
                (float(x + 2.0 * spacing), float(z), 1.0 / (2.0 * spacing)),
                (float(x), float(z), -1.0 / (2.0 * spacing)),
                (float(x + spacing), float(z), -1.0 / (2.0 * spacing)),
                (float(x - spacing), float(z), 1.0 / (2.0 * spacing)),
            ]
            gy_terms = [
                (float(x + spacing), float(z + spacing), 1.0 / (2.0 * spacing)),
                (float(x + spacing), float(z - spacing), -1.0 / (2.0 * spacing)),
                (float(x), float(z + spacing), -1.0 / (2.0 * spacing)),
                (float(x), float(z - spacing), 1.0 / (2.0 * spacing)),
            ]
            for terms in (gx_terms, gy_terms):
                row: dict[int, float] = {}
                fixed = 0.0
                for px, pz, weight in terms:
                    field_row, field_fixed = route_field_row(px, pz)
                    for column, value in field_row.items():
                        row[column] = row.get(column, 0.0) + weight * value
                    fixed += weight * field_fixed
                # The unit normal map n(g)=(-gx,-gz,1)/sqrt(1+|g|^2)
                # is 1-Lipschitz in L2. Bounding each gradient-component
                # change by 0.10 keeps the checker L1 normal difference below
                # 0.25 at this detected facette pixel.
                add(row, 0.10 - fixed)
                add({column: -value for column, value in row.items()}, 0.10 + fixed)
        elif cut["kind"] == "R5sp":
            point_row, point_fixed = route_field_row(*cut["point"])
            selectors = [event_selector_indices[(cut_i, i)] for i in range(9)]
            add({column: 1.0 for column in selectors}, 1.0)
            add({column: -1.0 for column in selectors}, -1.0)
            threshold = 0.5 - 1e-5
            for choice_i, window in enumerate(cut["windows"]):
                selector = event_selector_indices[(cut_i, choice_i)]
                for node in window:
                    node_row, node_fixed = route_field_row(*node)
                    row = subtract_rows(point_row, node_row)
                    fixed = point_fixed - node_fixed
                    big_m = event_big_m(row, fixed, threshold)
                    row[selector] = big_m
                    add(row, threshold + big_m - fixed)
        elif cut["kind"] == "R8G":
            row: dict[int, float] = {}
            fixed = 0.0
            for item in cut["weights"]:
                point_row, point_fixed = route_field_row(*item["point"])
                weight = float(item["weight"])
                for column, value in point_row.items():
                    row[column] = row.get(column, 0.0) + weight * value
                fixed += weight * point_fixed
            threshold = 0.15 - 1e-5
            add(row, threshold - fixed)
            add({column: -value for column, value in row.items()}, threshold + fixed)
        elif cut["kind"] == "R9w":
            # Match r9_form.py's linear Gaussian bandpass at a checker pixel.
            # This is an event cut at a detected component maximum, not a
            # pointwise equality lock on the old R9w field.
            x, z = map(float, cut["point"])

            def gaussian_kernel(sigma: float) -> np.ndarray:
                radius = int(4.0 * sigma + 0.5)
                offsets = np.arange(-radius, radius + 1, dtype=np.float64)
                kernel = np.exp(-0.5 * (offsets / sigma) ** 2)
                return kernel / kernel.sum()

            small = gaussian_kernel(rs * 0.25)
            large = gaussian_kernel(rs * 1.5)
            small_radius, large_radius = len(small) // 2, len(large) // 2
            row: dict[int, float] = {}
            fixed = 0.0
            sign = int(cut["sign"])
            for dy in range(-large_radius, large_radius + 1):
                ky_large = large[dy + large_radius]
                ky_small = (small[dy + small_radius]
                            if abs(dy) <= small_radius else 0.0)
                for dx in range(-large_radius, large_radius + 1):
                    weight = sign * (ky_small * (
                        small[dx + small_radius] if abs(dx) <= small_radius else 0.0
                    ) - ky_large * large[dx + large_radius])
                    if abs(weight) <= 1e-14:
                        continue
                    field_row, field_fixed = route_field_row(
                        x + dx / rs, z + dy / rs,
                    )
                    for column, value in field_row.items():
                        row[column] = row.get(column, 0.0) + weight * value
                    fixed += weight * field_fixed
            threshold = 0.10 - 1e-5
            add(row, threshold - fixed)
            add({column: -value for column, value in row.items()}, threshold + fixed)
        else:
            raise ValueError(f"Unbekannter Ereignisschnitt: {cut['kind']}")

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

    # Hard p3d19 endpoint constraints use the same 0.25-map checker lattice
    # as r8_kreuzung.py. The 5.4 cm cap applies to the ramp-end crossing
    # footprint; the 10 cm runout cap prevents every possible R8a hit there.
    endpoint = next(p for p in profiles if p["index"] == 11)
    q0 = np.asarray(endpoint["coords"][-1], dtype=np.float64)
    q1 = np.asarray(endpoint["coords"][max(0, len(endpoint["coords"]) - 9)], dtype=np.float64)
    tangent = q0 - q1
    tangent /= max(float(np.hypot(*tangent)), 1e-12)
    normal = np.array([-tangent[1], tangent[0]], dtype=np.float64)
    end_fs = checker_fs
    end_ix0 = max(0, int(np.floor((q0[0] - 6.0) * end_fs)))
    end_ix1 = min(nx * end_fs, int(np.ceil((q0[0] + 6.0) * end_fs)))
    end_iz0 = max(0, int(np.floor((q0[1] - 6.0) * end_fs)))
    end_iz1 = min(ny * end_fs, int(np.ceil((q0[1] + 6.0) * end_fs)))
    ez, ex = np.mgrid[end_iz0:end_iz1 + 1, end_ix0:end_ix1 + 1]
    exm, ezm = ex / end_fs, ez / end_fs
    ramp_mask = np.zeros((end_iz1 - end_iz0 + 1, end_ix1 - end_ix0 + 1), dtype=bool)
    for px, pz in endpoint["coords"]:
        ix = int(np.rint(px * end_fs)) - end_ix0
        iz = int(np.rint(pz * end_fs)) - end_iz0
        if 0 <= iz < ramp_mask.shape[0] and 0 <= ix < ramp_mask.shape[1]:
            ramp_mask[iz, ix] = True
    end_road = ndi.distance_transform_edt(~ramp_mask) / end_fs <= 1.5
    road_cells = np.zeros((ny, nx), dtype=bool)
    for rx, rz in data["wege"]:
        road_cells[int(rz), int(rx)] = True
    road_cells |= np.frombuffer(base64.b64decode(data["WEGA"]), dtype=np.uint8).reshape(
        ny * rs + 1, nx * rs + 1,
    )[:-1:rs, :-1:rs] > 20
    tiled_road = np.kron(road_cells, np.ones((end_fs, end_fs), dtype=bool))
    end_road[:-1, :-1] |= tiled_road[
        end_iz0:end_iz1, end_ix0:end_ix1
    ]
    end_distance = np.hypot(exm - q0[0], ezm - q0[1])
    end_stage_mask = end_road & (end_distance <= 4.0 + 1e-9)
    dx, dz = exm - q0[0], ezm - q0[1]
    along = dx * tangent[0] + dz * tangent[1]
    across = dx * normal[0] + dz * normal[1]
    end_runout_mask = (
        (along >= -1.0 - 1e-9) & (along <= 4.0 + 1e-9)
        & (np.abs(across) <= 2.5 + 1e-9)
        & (exm > 0.0) & (ezm > 0.0)
        & (exm < nx) & (ezm < ny)
    )

    def adjacent_pairs(
        mask: np.ndarray, xcoords: np.ndarray, zcoords: np.ndarray,
    ) -> list[tuple[float, float, float, float]]:
        pairs: list[tuple[float, float, float, float]] = []
        for iy, ix in zip(*np.nonzero(mask)):
            if iy + 1 < mask.shape[0] and mask[iy + 1, ix]:
                pairs.append((float(xcoords[iy, ix]), float(zcoords[iy, ix]),
                              float(xcoords[iy + 1, ix]), float(zcoords[iy + 1, ix])))
            if ix + 1 < mask.shape[1] and mask[iy, ix + 1]:
                pairs.append((float(xcoords[iy, ix]), float(zcoords[iy, ix]),
                              float(xcoords[iy, ix + 1]), float(zcoords[iy, ix + 1])))
        return pairs

    def endpoint_runout_pairs_for(profile: dict, at_start: bool) -> list[tuple[float, float, float, float]]:
        coords = np.asarray(profile["coords"], dtype=np.float64)
        if at_start:
            q_start = coords[0]
            q_inside = coords[min(8, len(coords) - 1)]
        else:
            q_start = coords[-1]
            q_inside = coords[max(0, len(coords) - 9)]
        direction = q_start - q_inside
        direction /= max(float(np.hypot(*direction)), 1e-12)
        side = np.array([-direction[1], direction[0]], dtype=np.float64)
        ix0 = max(0, int(np.floor((q_start[0] - 6.0) * end_fs)))
        ix1 = min(nx * end_fs, int(np.ceil((q_start[0] + 6.0) * end_fs)))
        iz0 = max(0, int(np.floor((q_start[1] - 6.0) * end_fs)))
        iz1 = min(ny * end_fs, int(np.ceil((q_start[1] + 6.0) * end_fs)))
        zz, xx = np.mgrid[iz0:iz1 + 1, ix0:ix1 + 1]
        map_x, map_z = xx / end_fs, zz / end_fs
        rx, rz = map_x - q_start[0], map_z - q_start[1]
        along = rx * direction[0] + rz * direction[1]
        across = rx * side[0] + rz * side[1]
        mask = (
            (along >= -1.0 - 1e-9) & (along <= 4.0 + 1e-9)
            & (np.abs(across) <= 2.5 + 1e-9)
            & (map_x > 0.0) & (map_z > 0.0)
            & (map_x < nx) & (map_z < ny)
        )
        return adjacent_pairs(mask, map_x, map_z)

    endpoint_stage_pairs = adjacent_pairs(end_stage_mask, exm, ezm)
    endpoint_runout_pairs = adjacent_pairs(end_runout_mask, exm, ezm)
    extra_endpoint_runout_pairs = [
        pair
        for profile in profiles
        for pair in (endpoint_runout_pairs_for(profile, True)
                     if profile["index"] in (2, 11) else [])
    ]

    # R8 checker local road-neighbor pairs, evaluated bilinearly on the 0.5 grid.
    for a, b in neighbor_pairs:
        entries = {surface_start + j: v for j, v in pair_row(a, b).items()}
        add({**entries, t_index: -1.0}, 0.0)
        add({**{j: -v for j, v in entries.items()}, t_index: -1.0}, 0.0)

    def add_pair_cap(px0: float, pz0: float, px1: float, pz1: float, cap: float) -> None:
        row0, fixed0 = route_field_row(px0, pz0)
        row1, fixed1 = route_field_row(px1, pz1)
        entries = dict(row0)
        for index, value in row1.items():
            entries[index] = entries.get(index, 0.0) - value
        add(entries, cap - (fixed0 - fixed1))
        add({index: -value for index, value in entries.items()}, cap + (fixed0 - fixed1))

    endpoint_stage_enabled = os.environ.get("P3D20_ENDPOINT_STAGE_LOCK", "1") != "0"
    endpoint_r8a_enabled = os.environ.get("P3D20_ENDPOINT_R8A_LOCK", "1") != "0"
    if endpoint_stage_enabled:
        for pair in endpoint_stage_pairs:
            add_pair_cap(*pair, 0.054)
    if endpoint_r8a_enabled:
        for pair in [*endpoint_runout_pairs, *extra_endpoint_runout_pairs]:
            add_pair_cap(*pair, 0.10)

    # Mesh axis samples agree with the exact ramp variables within 2 cm.
    axis_count = 0
    for route, p in enumerate(profiles):
        for k, (x, z) in enumerate(p["coords"]):
            if not (grid_x0 - 1e-9 <= x <= grid_x1 + 1e-9 and grid_z0 - 1e-9 <= z <= grid_z1 + 1e-9):
                continue
            row, fixed = route_field_row(float(x), float(z))
            hidx = h_offsets[route] + k
            add({**row, hidx: -1.0}, axis_tolerance - fixed)
            add({**{j: -v for j, v in row.items()}, hidx: 1.0}, axis_tolerance + fixed)
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

    # Official R3 operator over the field that the unchanged p3d17 transfer
    # actually emits. The checker samples at 0.25 map units and counts the
    # maximum over each 16-sample (4.8 m) section.
    r3_d1_terms = []
    if r3_limit is not None:
        for route, p in enumerate(profiles):
            coords = np.asarray(p["coords"], dtype=np.float64)
            center_rows, center_fixed = [], []
            for px, pz in coords:
                row, fixed = route_field_row(float(px), float(pz))
                center_rows.append(row)
                center_fixed.append(fixed)
            operator = np.eye(len(coords), dtype=np.float64) - ndi.gaussian_filter1d(
                np.eye(len(coords), dtype=np.float64), sigma=R3_SIGMA, axis=0, mode="nearest",
            )
            for k, op_row in enumerate(operator):
                active = np.flatnonzero(np.abs(op_row) > 1e-12)
                sec = k // R3_SECTION_SAMPLES
                bidx = binary_index[(route, sec)]
                row: dict[int, float] = {}
                fixed = 0.0
                for sample in active:
                    weight = float(op_row[sample])
                    for column, value in center_rows[int(sample)].items():
                        row[column] = row.get(column, 0.0) + weight * value
                    fixed += weight * center_fixed[int(sample)]
                threshold = R3_TOL - R3_FLOAT32_GUARD_M
                max_value = fixed + sum(
                    value * (upper[column] if value >= 0.0 else lower[column])
                    for column, value in row.items()
                )
                min_value = fixed + sum(
                    value * (lower[column] if value >= 0.0 else upper[column])
                    for column, value in row.items()
                )
                upper_relax = max(0.0, max_value - threshold)
                lower_relax = max(0.0, -min_value - threshold)
                add({**row, bidx: -upper_relax}, threshold - fixed)
                add({**{j: -v for j, v in row.items()}, bidx: -lower_relax}, threshold + fixed)
        for route, k, inside in section_lookup:
            if inside:
                r3_d1_terms.append(binary_index[(route, k // R3_SECTION_SAMPLES)])
        add({j: 1.0 for j in sorted(set(r3_d1_terms))}, float(r3_limit))

    # The official cross-section formulas sample +/-1.5 map units. The fixed
    # numerical guards cover float32 mesh emission; the reported checker and
    # its 3.5%, 20%, and 0.08 m thresholds remain unchanged.
    if r3_limit is not None:
        quer_section_terms: list[int] = []
        wob_section_terms: list[int] = []
        for route, p in enumerate(profiles):
            coords = np.asarray(p["coords"], dtype=np.float64)
            direction = np.gradient(coords, axis=0)
            direction /= np.maximum(np.linalg.norm(direction, axis=1, keepdims=True), 1e-9)
            normals = np.column_stack((-direction[:, 1], direction[:, 0]))
            center_rows, center_fixed = [], []
            plus_rows, plus_fixeds, minus_rows, minus_fixeds = [], [], [], []
            for (px, pz), normal in zip(coords, normals):
                axis_row, axis_fixed = route_field_row(float(px), float(pz))
                plus_row, plus_fixed = route_field_row(float(px + normal[0] * 1.5), float(pz + normal[1] * 1.5))
                minus_row, minus_fixed = route_field_row(float(px - normal[0] * 1.5), float(pz - normal[1] * 1.5))
                center_rows.append(axis_row)
                center_fixed.append(axis_fixed)
                plus_rows.append(plus_row)
                plus_fixeds.append(plus_fixed)
                minus_rows.append(minus_row)
                minus_fixeds.append(minus_fixed)
            for k, (px, pz) in enumerate(coords):
                section = (route, k // R3_SECTION_SAMPLES)
                if section not in quer_binary_index:
                    continue
                plus_row, minus_row = plus_rows[k], minus_rows[k]
                plus_fixed, minus_fixed = plus_fixeds[k], minus_fixeds[k]
                axis_row, axis_fixed = center_rows[k], center_fixed[k]

                q_row: dict[int, float] = {}
                for column, value in plus_row.items():
                    q_row[column] = q_row.get(column, 0.0) + value * (100.0 / 3.0)
                for column, value in minus_row.items():
                    q_row[column] = q_row.get(column, 0.0) - value * (100.0 / 3.0)
                q_fixed = (plus_fixed - minus_fixed) * (100.0 / 3.0)
                q_binary = quer_binary_index[section]
                add(q_row, R3_SINGLE_QUER_LIMIT_PCT - R3_FLOAT32_GUARD_PCT - q_fixed)
                add({column: -value for column, value in q_row.items()}, R3_SINGLE_QUER_LIMIT_PCT - R3_FLOAT32_GUARD_PCT + q_fixed)
                quer_big_m = R3_SINGLE_QUER_LIMIT_PCT - 3.5
                add({**q_row, q_binary: -quer_big_m}, 3.5 - R3_FLOAT32_GUARD_PCT - q_fixed)
                add({**{column: -value for column, value in q_row.items()}, q_binary: -quer_big_m}, 3.5 - R3_FLOAT32_GUARD_PCT + q_fixed)

                wob_row: dict[int, float] = {}
                for column, value in axis_row.items():
                    wob_row[column] = wob_row.get(column, 0.0) + value
                for column, value in plus_row.items():
                    wob_row[column] = wob_row.get(column, 0.0) - 0.5 * value
                for column, value in minus_row.items():
                    wob_row[column] = wob_row.get(column, 0.0) - 0.5 * value
                wob_fixed = axis_fixed - 0.5 * (plus_fixed + minus_fixed)
                wob_binary = wob_binary_index[section]
                wob_threshold = 0.08 - R3_FLOAT32_GUARD_M
                wob_max = wob_fixed + sum(
                    value * (upper[column] if value >= 0.0 else lower[column])
                    for column, value in wob_row.items()
                )
                wob_min = wob_fixed + sum(
                    value * (lower[column] if value >= 0.0 else upper[column])
                    for column, value in wob_row.items()
                )
                wob_upper_relax = max(0.0, wob_max - wob_threshold)
                wob_lower_relax = max(0.0, -wob_min - wob_threshold)
                add({**wob_row, wob_binary: -wob_upper_relax}, wob_threshold - wob_fixed)
                add({**{column: -value for column, value in wob_row.items()}, wob_binary: -wob_lower_relax}, wob_threshold + wob_fixed)
            quer_section_terms.extend(quer_binary_index[(route, k // R3_SECTION_SAMPLES)]
                                      for r, k, inside in section_lookup if r == route and inside)
            wob_section_terms.extend(wob_binary_index[(route, k // R3_SECTION_SAMPLES)]
                                     for r, k, inside in section_lookup if r == route and inside)
        if quer_limit is not None:
            add({j: 1.0 for j in sorted(set(quer_section_terms))}, float(quer_limit))
        if wob_limit is not None:
            add({j: 1.0 for j in sorted(set(wob_section_terms))}, float(wob_limit))

    # Same-route and cross-route pairs from p3d15, with the selected physical grade.
    pairs = route_pairs(profiles)
    for ra, ia, rb, ib, distance in pairs:
        va, vb = h_offsets[ra] + ia, h_offsets[rb] + ib
        bound = grade * distance
        add({va: 1.0, vb: -1.0}, bound)
        add({va: -1.0, vb: 1.0}, bound)

    matrix = coo_matrix((vals, (row_i, col_i)), shape=(len(rhs), nvars)).tocsr()
    objective = np.zeros(nvars, dtype=np.float64)
    if objective_mode == "feasibility":
        feasibility_counts = set(r3_d1_terms)
        feasibility_counts.update(quer_binary_index.values())
        feasibility_counts.update(wob_binary_index.values())
        for index in feasibility_counts:
            objective[index] = 1.0
        objective[t_index] = 1e-3
    elif objective_mode == "step":
        objective[t_index] = 1.0
    elif objective_mode == "quer":
        for index in quer_binary_index.values():
            objective[index] = 1.0
    elif objective_mode == "wob":
        for index in wob_binary_index.values():
            objective[index] = 1.0
    if mip_start_path is not None:
        mip_start = np.asarray(json.loads(mip_start_path.read_text(encoding="utf-8"))["x"], dtype=np.float64)
        result = highs_mip_solve(
            matrix, rhs, objective,
            np.zeros_like(integrality) if relax_integrality else integrality,
            lower, upper, mip_start, time_limit=time_limit_s,
        )
    else:
        result = milp(
            objective,
            integrality=(np.zeros_like(integrality) if relax_integrality else integrality),
            bounds=Bounds(lower, upper),
            constraints=LinearConstraint(matrix, np.full(len(rhs), -np.inf), np.asarray(rhs)),
            options={"presolve": True, "mip_rel_gap": 0.0, "time_limit": time_limit_s},
        )
    primal_feasible = False
    if result.x is not None:
        activity = matrix @ result.x
        primal_feasible = bool(
            np.all(activity <= np.asarray(rhs) + 2e-6)
            and np.all(result.x >= lower - 2e-6)
            and np.all(result.x <= upper + 2e-6)
            and (relax_integrality or np.all(np.abs(
                result.x[integrality.astype(bool)] - np.rint(result.x[integrality.astype(bool)])
            ) <= 2e-6))
        )
    if (not result.success and not primal_feasible) or result.x is None:
        summary = {
            "status": str(result.message),
            "status_code": int(result.status),
            "success": False,
            "primal_feasible": primal_feasible,
            "optimality_proven": bool(result.success),
            "objective_mode": objective_mode,
            "stage_limit_m": stage_limit,
            "r3_long_limit": r3_limit,
            "r3_quer_limit": quer_limit,
            "r3_wob_limit": wob_limit,
            "variables": nvars,
            "constraints": len(rhs),
        }
        out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return summary

    # Among exact minimax solutions, preserve the selected reference profile
    # and emitted mesh as closely as possible. A reference mesh contains final
    # heights, while `surface_start` stores pre-transfer target heights, so
    # invert the affine transfer before using it in the tie-break.
    primary_objective = float(result.fun)
    primary_step = float(result.x[t_index])
    primary_x = result.x.copy()
    add({t_index: 1.0}, primary_step + 1e-8)
    base_matrix = coo_matrix((vals, (row_i, col_i)), shape=(len(rhs), nvars)).tocsr()
    if reference_solution_path is not None:
        reference_solution = json.loads(reference_solution_path.read_text(encoding="utf-8"))
        reference_profiles = reference_solution["routes"]
        profile_reference = np.concatenate([
            np.asarray(reference_profiles[f"rampe_{p['index']}"]["solution_h_m"], dtype=np.float64)
            for p in profiles
        ])
        surface_reference = np.asarray(reference_solution["surface_grid"]["heights_m"], dtype=np.float64).ravel()
    else:
        reference_profiles = json.loads((Path(__file__).resolve().parents[1] / "p3d16_milp/machbarkeit_g45.json").read_text(encoding="utf-8"))["routes"]
        profile_reference = np.concatenate([
            np.asarray(reference_profiles[f"rampe_{p['index']}"]["h_solution"], dtype=np.float64)
            for p in profiles
        ])
    if reference_solution_path is not None:
        pass
    elif reference_mesh_path is None:
        reference_g = np.frombuffer(base64.b64decode(data["GB"]), dtype=np.float32).reshape(ny * rs + 1, nx * rs + 1).astype(np.float64)
    else:
        ref_data = json.loads(gzip.decompress(reference_mesh_path.read_bytes()))
        reference_g = np.frombuffer(base64.b64decode(ref_data["GB"]), dtype=np.float32).reshape(ny * rs + 1, nx * rs + 1).astype(np.float64)
    if reference_solution_path is None:
        mesh_x = grid_x0 + np.arange(width, dtype=np.float64) / fs
        mesh_z = grid_z0 + np.arange(height, dtype=np.float64) / fs
        mz, mx = np.meshgrid(mesh_z, mesh_x, indexing="ij")
        emitted_reference = ndi.map_coordinates(
            reference_g, [mz.ravel() * rs, mx.ravel() * rs], order=1, mode="nearest",
        )
        coverage_flat = transfer_coverage.ravel()
        background_flat = transfer_background.ravel()
        surface_reference = np.zeros(surface_count, dtype=np.float64)
        covered = coverage_flat > 1e-12
        surface_reference[covered] = (
            emitted_reference[covered] - background_flat[covered]
        ) / coverage_flat[covered]
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
    if not relax_integrality:
        for index in (*binary_index.values(), *quer_binary_index.values(), *wob_binary_index.values(), *event_selector_indices.values()):
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
    if mip_start_out is not None:
        mip_start_out.parent.mkdir(parents=True, exist_ok=True)
        mip_start_out.write_text(
            json.dumps({"x": result_x.tolist()}, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

    summary = {
        "status": str(result.message), "status_code": int(result.status),
        "success": bool(result.success or primal_feasible),
        "primal_feasible": primal_feasible,
        "optimality_proven": bool(result.success),
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
        "R3_single_cross_slope_limit_pct": R3_SINGLE_QUER_LIMIT_PCT,
        "endpoint_stage_limit_m": 0.054,
        "endpoint_R8a_pair_limit_m": 0.10,
        "endpoint_stage_pair_count": len(endpoint_stage_pairs),
        "endpoint_R8a_pair_count": len(endpoint_runout_pairs) + len(extra_endpoint_runout_pairs),
        "R9w_exact_bandpass_lock_points": hp_lock_count,
        "D1_regression_fence_vertex_counts": regression_locks,
        "exact_event_cut_count": len(event_cuts),
        "exact_event_selector_count": event_selector_count,
        "p3d18_variant24_reference_D1_sha256": p3d18_reference_hash,
        "variables": nvars, "constraints": len(rhs),
        "objective_mode": objective_mode,
        "relaxed_integrality": relax_integrality,
        "primary_objective_value": primary_objective,
        "primary_r3_long_indicator_sum": float(sum(primary_x[j] for j in set(r3_d1_terms))),
        "primary_r3_quer_indicator_sum": float(sum(primary_x[j] for j in set(quer_binary_index.values()))),
        "primary_r3_wob_indicator_sum": float(sum(primary_x[j] for j in set(wob_binary_index.values()))),
        "stage_limit_m": stage_limit,
        "r3_long_limit": r3_limit,
        "r3_quer_limit": quer_limit,
        "r3_wob_limit": wob_limit,
        "minimum_neighbor_step_m": float(result.x[t_index]),
        "tie_break_movement_l1_m": tie_break_movement,
        "tie_break_reference_mesh": reference_mesh_path.name if reference_mesh_path else "GB source field",
        "tie_break_reference_solution": reference_solution_path.name if reference_solution_path else None,
        "mip_dual_bound_m": (None if getattr(result, "mip_dual_bound", None) is None else float(result.mip_dual_bound)),
        "mip_gap": (None if getattr(result, "mip_gap", None) is None else float(result.mip_gap)),
    }
    if result.x is not None:
        xsol = result.x
        section_count = int(sum(xsol[j] > 0.5 for j in set(r3_d1_terms))) if r3_limit is not None else None
        summary["r3_sections_D1_solution"] = section_count
        summary["r3_quer_sections_D1_solution"] = int(
            sum(xsol[j] > 0.5 for j in set(quer_binary_index.values()))
        ) if r3_limit is not None else None
        summary["r3_wob_sections_D1_solution"] = int(
            sum(xsol[j] > 0.5 for j in set(wob_binary_index.values()))
        ) if r3_limit is not None else None
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
    ap.add_argument("--grade", type=float, choices=(0.45, 0.60), default=0.45)
    ap.add_argument("--mode", choices=("feasibility", "step", "quer", "wob"), default="feasibility")
    ap.add_argument("--r3-limit", type=int, default=6, help="official R3 longitudinal section limit")
    ap.add_argument("--r3-quer-limit", type=int, default=7)
    ap.add_argument("--r3-wob-limit", type=int, default=7)
    ap.add_argument("--stage-limit", type=float, default=None)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--reference-mesh", type=Path, help="p3d16 relief JSON gzip; its GB field is used only for the deterministic minimax tie-break")
    ap.add_argument("--mip-start", type=Path, help="full feasible HiGHS start vector from an earlier identical model")
    ap.add_argument("--mip-start-out", type=Path, help="write the final feasible model vector for a later warm start")
    ap.add_argument("--time-limit", type=float, default=600.0, help="MILP time limit in seconds")
    ap.add_argument("--event-cuts", type=Path, help="checker-derived local event cuts JSON")
    ap.add_argument("--reference-solution", type=Path, help="solution JSON used only as the L1 tie-break target")
    ap.add_argument("--axis-tolerance", type=float, default=0.02)
    ap.add_argument("--plane-tolerance", type=float, default=0.02)
    ap.add_argument("--relax-integrality", action="store_true")
    args = ap.parse_args()
    with gzip.open(RELIEF, "rt", encoding="utf-8") as f:
        data = json.load(f)
    stage_limit = args.stage_limit
    if stage_limit is None and args.mode in {"feasibility", "quer", "wob"}:
        stage_limit = 0.116
    summary = solve(
        data,
        args.grade,
        args.r3_limit,
        args.out,
        args.reference_mesh,
        args.axis_tolerance,
        args.plane_tolerance,
        stage_limit,
        args.r3_quer_limit,
        args.r3_wob_limit,
        args.mode,
        args.relax_integrality,
        args.mip_start,
        args.mip_start_out,
        args.time_limit,
        args.event_cuts,
        args.reference_solution,
    )
    summary["source_relief_sha256"] = hashlib.sha256(RELIEF.read_bytes()).hexdigest()
    summary["tie_break_reference_sha256"] = (
        hashlib.sha256(args.reference_mesh.read_bytes()).hexdigest()
        if args.reference_mesh else None
    )
    args.out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
