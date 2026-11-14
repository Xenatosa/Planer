#!/usr/bin/env python3
"""p3d32: continuous V3 LP with fixed crossing/ramp anchors and local flood cuts.

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

from construction_p3d31 import build as build_p3d31_construction

ROOT = Path(__file__).resolve().parents[3]
RELIEF = Path(os.environ.get(
    "P3D23_SOURCE_RELIEF",
    str(ROOT / "team/art/dorfmap_grundgeruest/relief3d/relief_daten.json.gz"),
))
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
R8A_POLICY_DIR = RELIEF3D / "pruefung"
if str(R8A_POLICY_DIR) not in sys.path:
    sys.path.insert(0, str(R8A_POLICY_DIR))
from r8a_policy import (  # noqa: E402
    R8A_DEFAULT_LIMIT_M,
    R8A_RAMPE2_START_EXCEPTION,
    R8A_RAMPE2_START_ENDPOINT_ID,
    R8A_RAMPE2_START_LIMIT_M,
    R8A_RAMPE2_START_XZ,
    r8a_exception_for_endpoint,
    r8a_pair_limit_m,
)

# Keep the unchanged strict official caps clear of Float32/solver roundoff.
# These are internal model guards, not changes to the checker policy.
R8A_FLOAT32_GUARD_M = 1e-5
ENDPOINT_STAGE_FLOAT32_GUARD_M = 1e-5
P3D29_CURVATURE_TOL_M = 0.02
P3D29_TREE_GROUND_TOL_M = 0.001
P3D31_DRAINAGE_L1_SCALE_M = 0.0001
P3D26_MODEL_SOLUTION = ROOT / "codex_jobs/tools/p3d26/results/p3d26_V3_all_hard_with_rampe2_exception.json"
P3D26_MODEL_SOLUTION_SHA256 = "0b03648f7d71a25783d111b81d7d8b4980e3a5ad9c6760d76209cebae241245e"
P3D32_VARIANTS = {"1": 0.015, "2": 0.020}
P3D32_CROSSING_ANCHOR = (152.5, 28.5)
P3D32_RAMP2_START = (126.51, 31.62)
P3D31_V3_REFERENCE = ROOT / "codex_jobs/tools/p3d31/results/p3d31_V3_round03_model.json"


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


def p3d17_reference_output() -> np.ndarray:
    """Rebuild the checked p3d17 reference from its immutable base inputs."""
    if str(RELIEF3D) not in sys.path:
        sys.path.insert(0, str(RELIEF3D))
    from neu import mesh as neu_mesh

    base_path = RELIEF3D / "relief_daten.json.gz"
    base_sha256 = hashlib.sha256(base_path.read_bytes()).hexdigest()
    expected_base = "5e8fdb51c3f3dff9ad2c03c32c7a39ee1a4f97a3bc0942d47a352b1d0b4f0e88"
    if base_sha256 != expected_base:
        raise RuntimeError(f"p3d17-Basisrelief hat unerwarteten Hash {base_sha256}")
    source = neu_mesh.load_relief(base_path)
    vector = json.loads((RELIEF3D / "neu/vektor.json").read_text(encoding="utf-8"))
    with np.load(RELIEF3D / "neu/felder.npz", allow_pickle=False) as archive:
        fields = {name: archive[name] for name in archive.files}

    settings = neu_mesh.KREUZUNG_SETTINGS["22"]
    old_solution = settings.get("solution_file")
    old_center = settings.get("crossing_center_map")
    old_crossing = os.environ.get("RELIEF_KREUZUNG_VAR")
    old_endpoint = os.environ.get("RELIEF_WEGEND_VAR")
    settings["solution_file"] = "p3d17_joint_mesh_v22.json"
    settings["crossing_center_map"] = [152.54985704503775, 28.48954534572434]
    os.environ["RELIEF_KREUZUNG_VAR"] = "22"
    os.environ["RELIEF_WEGEND_VAR"] = "1"
    try:
        result, _ = neu_mesh.terrain_heights(source, "D1", vector, fields, variant="2")
    finally:
        if old_solution is None:
            settings.pop("solution_file", None)
        else:
            settings["solution_file"] = old_solution
        if old_center is None:
            settings.pop("crossing_center_map", None)
        else:
            settings["crossing_center_map"] = old_center
        if old_crossing is None:
            os.environ.pop("RELIEF_KREUZUNG_VAR", None)
        else:
            os.environ["RELIEF_KREUZUNG_VAR"] = old_crossing
        if old_endpoint is None:
            os.environ.pop("RELIEF_WEGEND_VAR", None)
        else:
            os.environ["RELIEF_WEGEND_VAR"] = old_endpoint

    result_hash = hashlib.sha256(result.astype("<f4", copy=False).tobytes()).hexdigest()
    expected_result = "26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29"
    if result_hash != expected_result:
        raise RuntimeError(f"Reproduziertes p3d17-D1 hat unerwarteten Hash {result_hash}")
    return result


def p3d26_v3_surface() -> tuple[np.ndarray, dict]:
    """Load the recorded all-hard V3 p3d26 D1 mesh target for flood seeding."""
    payload = P3D26_MODEL_SOLUTION.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != P3D26_MODEL_SOLUTION_SHA256:
        raise RuntimeError(f"p3d26-V3-Loesung hat unerwarteten SHA-256: {digest}")
    solution = json.loads(payload)
    grid = solution["surface_grid"]
    if (int(grid["x0"]) != D1_BOUNDS[0] or int(grid["z0"]) != D1_BOUNDS[1]
            or abs(float(grid["spacing"]) - 0.5) > 1e-12
            or int(grid["width"]) != int((D1_BOUNDS[2] - D1_BOUNDS[0]) * 2) + 1
            or int(grid["height"]) != int((D1_BOUNDS[3] - D1_BOUNDS[1]) * 2) + 1):
        raise RuntimeError("p3d26-V3-Loesung hat ein unerwartetes D1-Gitter")
    heights = np.asarray(grid["heights_m"], dtype=np.float64)
    if heights.shape != (int(grid["height"]), int(grid["width"])):
        raise RuntimeError("p3d26-V3-Hoehenraster hat unerwartete Abmessungen")
    return heights, {
        "file": str(P3D26_MODEL_SOLUTION.relative_to(ROOT)),
        "sha256": digest,
        "status": solution.get("status"),
        "primal_feasible": bool(solution.get("primal_feasible")),
        "grid": {key: grid[key] for key in ("x0", "z0", "spacing", "width", "height")},
    }


def p3d32_fixed_anchors(variant: str) -> dict:
    """Derive crossing plane and ramp-2 start anchors from the recorded V3 LP."""
    if not P3D31_V3_REFERENCE.exists():
        raise RuntimeError(f"V3-Referenz für feste p3d32-Anker fehlt: {P3D31_V3_REFERENCE}")
    v3 = json.loads(P3D31_V3_REFERENCE.read_text(encoding="utf-8"))
    grid = v3["surface_grid"]
    heights = np.asarray(grid["heights_m"], dtype=np.float64)
    spacing = float(grid["spacing"])
    x0, z0 = float(grid["x0"]), float(grid["z0"])

    def sample(x: float, z: float) -> float:
        u, v = (x - x0) / spacing, (z - z0) / spacing
        ix, iz = int(np.floor(u)), int(np.floor(v))
        ix = min(max(ix, 0), heights.shape[1] - 2)
        iz = min(max(iz, 0), heights.shape[0] - 2)
        fu, fv = u - ix, v - iz
        return float((1.0 - fu) * (1.0 - fv) * heights[iz, ix]
                     + fu * (1.0 - fv) * heights[iz, ix + 1]
                     + (1.0 - fu) * fv * heights[iz + 1, ix]
                     + fu * fv * heights[iz + 1, ix + 1])

    anchor_x, anchor_z = P3D32_CROSSING_ANCHOR
    anchor_height = sample(anchor_x, anchor_z)
    grad_x = (sample(anchor_x + 0.5, anchor_z)
              - sample(anchor_x - 0.5, anchor_z)) / 1.2
    grad_z = (sample(anchor_x, anchor_z + 0.5)
              - sample(anchor_x, anchor_z - 0.5)) / 1.2
    slope = float(np.hypot(grad_x, grad_z))
    if slope <= 1e-9:
        raise RuntimeError("V3-Kreuzungshöhe hat keinen definierten Auslaufgradienten")
    downhill = np.array([-grad_x, -grad_z], dtype=np.float64) / slope
    crossfall = P3D32_VARIANTS[variant]
    # The height gradient points uphill, opposite the named outlet direction.
    platform_gx, platform_gz = (-crossfall * downhill).tolist()
    target_raw = np.array([anchor_x, anchor_z], dtype=np.float64) + downhill * (2.0 / 1.2)
    target = [float(126.0 + round((target_raw[0] - 126.0) / 0.5) * 0.5),
              float(round(target_raw[1] / 0.5) * 0.5)]
    gate_center_height = (anchor_height
                          + platform_gx * (float(R8_GATE_CENTER[0]) - anchor_x) * CELL_M
                          + platform_gz * (float(R8_GATE_CENTER[1]) - anchor_z) * CELL_M)
    ramp_height = float(v3["routes"]["rampe_2"]["solution_h_m"][0])
    return {
        "variant": variant,
        "crossing_anchor_xz": [float(anchor_x), float(anchor_z)],
        "crossing_anchor_height_m": anchor_height,
        "crossfall_percent": crossfall * 100.0,
        "outlet_direction_physical_unit": downhill.tolist(),
        "outlet_target_cell_xz": target,
        "outlet_target_height_m": float(anchor_height
                                          + platform_gx * (target[0] - anchor_x) * CELL_M
                                          + platform_gz * (target[1] - anchor_z) * CELL_M),
        "platform_radius_physical_m": PLANE_RADIUS_M,
        "platform_gradient_physical": [platform_gx, platform_gz],
        "plane_height_at_R8_center_m": gate_center_height,
        "rampe_2_start_xz": list(P3D32_RAMP2_START),
        "rampe_2_start_height_m": ramp_height,
        "anchor_source": str(P3D31_V3_REFERENCE.relative_to(ROOT)),
        "anchor_source_sha256": hashlib.sha256(P3D31_V3_REFERENCE.read_bytes()).hexdigest(),
        "outlet_direction_basis": "negative bilinear central-difference gradient of p3d31 V3 round03 at 152.5|28.5",
    }


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


def highs_mip_solve(matrix, rhs, objective, integrality, lower, upper, start=None, time_limit=600.0):
    """Solve single-threaded with the free HiGHS Python binding."""
    highspy_dir = Path("/tmp/p3d18_highspy")
    if str(highspy_dir) not in sys.path and highspy_dir.exists():
        sys.path.insert(0, str(highspy_dir))
    import highspy

    lp = highspy.HighsLp()
    lp.num_col_ = int(matrix.shape[1])
    lp.num_row_ = int(matrix.shape[0])
    # Highs may take ownership of passModel arrays. Keep independent copies so
    # the post-solve residual check still uses the original SciPy matrix/bounds.
    lp.col_cost_ = np.array(objective, dtype=np.float64, copy=True)
    lp.col_lower_ = np.array(lower, dtype=np.float64, copy=True)
    lp.col_upper_ = np.array(upper, dtype=np.float64, copy=True)
    lp.row_lower_ = np.full(matrix.shape[0], -np.inf, dtype=np.float64)
    lp.row_upper_ = np.array(rhs, dtype=np.float64, copy=True)
    lp.sense_ = highspy.ObjSense.kMinimize
    column_matrix = matrix.tocsc()
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = column_matrix.indptr.astype(np.int32, copy=True)
    lp.a_matrix_.index_ = column_matrix.indices.astype(np.int32, copy=True)
    lp.a_matrix_.value_ = column_matrix.data.astype(np.float64, copy=True)
    lp.integrality_ = [
        highspy.HighsVarType.kInteger if value else highspy.HighsVarType.kContinuous
        for value in np.asarray(integrality, dtype=np.uint8)
    ]

    highs = highspy.Highs()
    highs.setOptionValue("output_flag", False)
    highs.setOptionValue("presolve", "off" if not np.any(integrality) else "on")
    highs.setOptionValue("threads", 1)
    highs.setOptionValue("mip_rel_gap", 0.0)
    highs.setOptionValue("time_limit", float(time_limit))
    # Preserve small affine-transfer coefficients at the fade edge; the
    # default 1e-9 can drop them while their pre-transfer target is large.
    highs.setOptionValue("small_matrix_value", 1e-12)
    status = highs.passModel(lp)
    if status not in (highspy.HighsStatus.kOk, highspy.HighsStatus.kWarning):
        raise RuntimeError(f"HiGHS Modellannahme fehlgeschlagen: {status}")
    loaded_lp = highs.getLp()
    loaded_matrix_data = np.asarray(loaded_lp.a_matrix_.value_, dtype=np.float64)
    loaded_matrix_index = np.asarray(loaded_lp.a_matrix_.index_, dtype=np.int32)
    loaded_matrix_start = np.asarray(loaded_lp.a_matrix_.start_, dtype=np.int32)
    if loaded_lp.a_matrix_.format_ == highspy.MatrixFormat.kColwise:
        loaded_matrix = csr_matrix((
            loaded_matrix_data, loaded_matrix_index, loaded_matrix_start,
        ), shape=(lp.num_col_, lp.num_row_)).T.tocsr()
    else:
        loaded_matrix = csr_matrix((
            loaded_matrix_data, loaded_matrix_index, loaded_matrix_start,
        ), shape=(lp.num_row_, lp.num_col_))
    loaded_delta = (loaded_matrix - matrix).tocsr()
    loaded_matrix_delta = float(np.max(np.abs(loaded_delta.data))) if loaded_delta.nnz else 0.0
    loaded_row_upper = np.asarray(loaded_lp.row_upper_, dtype=np.float64).copy()
    loaded_row_lower = np.asarray(loaded_lp.row_lower_, dtype=np.float64).copy()
    upper_delta = float(np.max(np.abs(
        loaded_row_upper - np.asarray(rhs, dtype=np.float64),
    )))
    lower_matches = np.array_equal(loaded_row_lower, np.full(len(rhs), -np.inf))
    loaded_row_bound_delta = upper_delta if lower_matches else float("inf")
    if loaded_matrix_delta > 1e-9:
        raise RuntimeError(
            f"HiGHS hat eine andere Nebenbedingungsmatrix geladen (max_delta={loaded_matrix_delta:.9g})"
        )
    if start is not None:
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
    status_code = (model_status.value if hasattr(model_status, "value")
                   else int(model_status))
    return SimpleNamespace(
        success=success,
        status=status_code,
        message=highs.modelStatusToString(model_status),
        x=np.asarray(solution.col_value, dtype=np.float64) if solution.value_valid else None,
        row_value=np.asarray(solution.row_value, dtype=np.float64) if solution.value_valid else None,
        loaded_row_upper=loaded_row_upper,
        fun=float(info.objective_function_value),
        mip_dual_bound=float(info.mip_dual_bound),
        mip_gap=float(info.mip_gap),
        max_primal_infeasibility=float(getattr(info, "max_primal_infeasibility", 0.0)),
        loaded_matrix_delta=loaded_matrix_delta,
        loaded_row_bound_delta=loaded_row_bound_delta,
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


def bilinear_row(x: float, z: float, x0: float, z0: float, fs: int,
                 width: int, height: int) -> dict[int, float]:
    u, v = (x - x0) * fs, (z - z0) * fs
    ix, iz = int(np.floor(u)), int(np.floor(v))
    ix = min(max(ix, 0), width - 2)
    iz = min(max(iz, 0), height - 2)
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
    flood_cuts_path: Path | None = None,
    reference_solution_path: Path | None = None,
    diagnostic_groups: set[str] | None = None,
) -> dict:
    if objective_mode not in {"feasibility", "step", "quer", "wob", "diagnostic"}:
        raise ValueError(f"Unbekannter Ziellauf: {objective_mode}")
    diagnostic_groups = set(diagnostic_groups or ())
    p3d32_variant = os.environ.get("P3D32_VARIANT", "1")
    if p3d32_variant not in P3D32_VARIANTS:
        raise ValueError("P3D32_VARIANT muss 1 oder 2 sein")
    # The p3d31 model's drainage MIP is intentionally disabled in p3d32.
    # Priority-Flood is post-LP and any needed lift returns as a linear floor cut.
    variant = "1"
    drainage_mode = "off"
    event_cuts = json.loads(event_cuts_path.read_text(encoding="utf-8")) if event_cuts_path else []
    event_cuts = list(event_cuts)
    flood_cuts = json.loads(flood_cuts_path.read_text(encoding="utf-8")) if flood_cuts_path else []
    event_cuts.extend(flood_cuts)
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

    transfer_background, transfer_coverage, _candidate_transfer_output, transfer_context = p3d17_transfer_context()
    p3d17_output = p3d17_reference_output()

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
    expected_reference_hash = os.environ.get("P3D22_EXPECT_REFERENCE_SHA256")
    if expected_reference_hash and p3d18_reference_hash != expected_reference_hash:
        raise RuntimeError("Die p3d18-Transferreferenz weicht vom dokumentierten Hash ab")

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
    construction_variant = os.environ.get("P3D31_CONSTRUCTION_VARIANT", "3")
    if construction_variant != "3":
        raise ValueError("p3d31 verwendet verbindlich den Lokalitaetsring 7,5 m (Variante 3)")
    drainage_eps_m = 0.001
    p3d26_surface, p3d26_meta = p3d26_v3_surface()
    reference_full = gb.astype(np.float64, copy=True)
    ref_ix0, ref_iz0 = int(grid_x0 * rs), int(grid_z0 * rs)
    reference_full[ref_iz0:ref_iz0 + height, ref_ix0:ref_ix0 + width] = p3d17_output
    construction = build_p3d31_construction(
        data, profiles, p3d17_output, reference_full,
        drainage_surface=p3d26_surface,
        transfer_support=transfer_coverage,
        endpoint_support=np.asarray(
            transfer_context.get("endpoint_weight", np.zeros_like(transfer_coverage)),
            dtype=np.float64,
        ),
        x0=grid_x0, z0=grid_z0, x1=grid_x1, z1=grid_z1, fs=fs,
        ring_variant=construction_variant, drainage_eps_m=drainage_eps_m,
    )
    platform_meta = p3d32_fixed_anchors(p3d32_variant)
    active_mask = np.asarray(construction["active_mask"], dtype=bool)
    ring_mask = np.asarray(construction["ring_mask"], dtype=bool)
    ring_distance_m = np.asarray(construction["ring_distance_m"], dtype=np.float64)
    ring_tolerance_m = np.asarray(construction["ring_tolerance_m"], dtype=np.float64)
    cliff_zone = np.asarray(construction["wall_cliff_gorge_mask"], dtype=bool)
    curvature_l1_mask = np.asarray(construction["curvature_l1_mask"], dtype=bool)
    curvature_directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    ref_grid = p3d17_output.astype(np.float64)
    curvature_specs = []
    for iz, ix in zip(*np.nonzero(cliff_zone)):
        for dz, dx in curvature_directions:
            az, ax = iz - dz, ix - dx
            bz, bx = iz + dz, ix + dx
            if not (0 <= az < height and 0 <= ax < width
                    and 0 <= bz < height and 0 <= bx < width):
                continue
            ref_second = float(ref_grid[az, ax] - 2.0 * ref_grid[iz, ix]
                               + ref_grid[bz, bx])
            # Any stencil touching a road, crossing, runout or ramp-end cell
            # receives only the weighted L1 reference-form penalty.
            soft_form = bool(curvature_l1_mask[az, ax]
                             or curvature_l1_mask[iz, ix]
                             or curvature_l1_mask[bz, bx])
            tolerance = max(P3D29_CURVATURE_TOL_M, 0.25 * abs(ref_second))
            curvature_specs.append({
                "indices": (az, ax, iz, ix, bz, bx),
                "reference_second_difference_m": ref_second,
                "soft_l1": soft_form,
                "hard_tolerance_m": tolerance,
                "l1_weight": 1.0 / tolerance,
            })
    ref_gy, ref_gx = np.gradient(ref_grid, 1.0 / fs)
    ref_slope = np.hypot(ref_gx, ref_gy)
    smooth_centers = (active_mask & ~cliff_zone & ~curvature_l1_mask
                      & (ref_slope >= 0.15) & (ref_slope <= 0.80))
    smoothness_specs = []
    for iz, ix in zip(*np.nonzero(smooth_centers)):
        for dz, dx in curvature_directions:
            az, ax = int(iz - dz), int(ix - dx)
            bz, bx = int(iz + dz), int(ix + dx)
            if not (0 <= az < height and 0 <= ax < width
                    and 0 <= bz < height and 0 <= bx < width
                    and active_mask[az, ax] and active_mask[bz, bx]):
                continue
            ref_second = float(ref_grid[az, ax] - 2.0 * ref_grid[iz, ix]
                               + ref_grid[bz, bx])
            tolerance = max(P3D29_CURVATURE_TOL_M, 0.25 * abs(ref_second))
            smoothness_specs.append({
                "indices": (az, ax, int(iz), int(ix), bz, bx),
                "reference_second_difference_m": ref_second,
                "l1_weight": 1.0 / tolerance,
            })
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
    drainage_candidates = construction["drainage_candidate_edges_child_parent_eps"]
    if variant == "1":
        # V1 implements the official-counter policy: sinks are allowed and
        # evaluated only by fresh official G5/R5_loch/G6 component cuts.
        drainage_candidates = []
    construction["modeled_drainage_candidate_count"] = len(drainage_candidates)
    construction["official_sink_policy"] = (
        "V1: no successor-choice or reachability constraints; only official G5/R5_loch/G6 event cuts and checker budgets"
        if variant == "1" else
        "V2 unavailable: legacy soft drainage is not the requested LP/Priority-Flood construction"
    )
    drainage_choice_indices = {
        edge_index: binary_start + len(binary_index) + len(quer_binary_index)
        + len(wob_binary_index) + edge_index
        for edge_index in range(len(drainage_candidates))
    }
    drainage_flow_start = (binary_start + len(binary_index) + len(quer_binary_index)
                           + len(wob_binary_index) + len(drainage_candidates))
    drainage_flow_indices = {
        edge_index: drainage_flow_start + edge_index
        for edge_index in range(len(drainage_candidates))
    }
    nvars = drainage_flow_start + len(drainage_candidates)

    event_selector_indices: dict[tuple[int, int], int] = {}
    next_event_column = nvars
    for cut_i, cut in enumerate(event_cuts):
        # p3d32 converts checker events to direct continuous inequalities.
        # It has no disjunctive selectors or hit-count indicator variables.
        if cut["kind"] not in {"G5", "R4", "R5", "R8b", "G11", "G6", "R5sp", "R8G", "R9w", "FLOOR"}:
            raise ValueError(f"Unbekannter p3d32-Lazy-Cut: {cut['kind']}")
    event_selector_count = next_event_column - nvars
    event_hit_indices: dict[int, int] = {}

    # Every slack is zero unless its named group is enabled for this solve.
    # Scales are the normalization units used by the joint weighted L1.
    slack_spec = {
        "r3_long_extra_hits": ("r3_long", 1.0, None),
        "r3_long_residual_m": ("r3_long", 0.08, None),
        "r3_quer_extra_hits": ("r3_quer", 1.0, None),
        "r3_quer_residual_pp": ("r3_quer", 3.5, None),
        "r3_wob_extra_hits": ("r3_wob", 1.0, None),
        "r3_wob_residual_m": ("r3_wob", 0.08, None),
        "crossing_stage_extra_m": ("crossing_stage", 0.116, None),
        "axis_tolerance_extra_m": ("axis_supports", 0.02, None),
        "plane_tolerance_extra_m": ("plane_core", 0.02, None),
        "endpoint_stage_extra_m": ("endpoint_stage", 0.054, None),
        "safety_gitter_extra_m": ("safety_gitter", 0.019, None),
        "safety_quer_extra_pp": ("safety_quer", 2.95, None),
        "safety_single_quer_extra_pp": ("safety_single_quer", 19.5, None),
        "g5_total_extra_hits": ("g5", 1.0, None),
        "g5_d1_extra_hits": ("g5", 1.0, None),
        "r5_total_extra_hits": ("r5_hole", 1.0, None),
        "r5_d1_extra_hits": ("r5_hole", 1.0, None),
        "r4_d1_extra_hits": ("r4", 1.0, None),
        "g11_d1_extra_hits": ("g11", 1.0, None),
        "r8b_d1_extra_hits": ("r8b", 1.0, None),
        # Families that were hard in p3d22. Route grades and the two route
        # classes use a shared maximum relaxation per family.
        "grade_cross_extra_m": ("grade_cross", 0.45, None),
        "grade_same_extra_m": ("grade_same", 0.45, None),
        "endpoint_r8a_extra_m": ("endpoint_r8a", 0.10, None),
        "plane_slope_polygon_extra_pp": ("plane_slope_polygon", 1.0, None),
        "plane_slope_box_extra_pp": ("plane_slope_box", 1.0, None),
        "variable_bounds_extra_m": ("variable_bounds", 1.0, None),
        "route_profile_slope_extra_m": ("route_profile_slope", 0.60, None),
        "source_monotone_extra_m": ("source_monotone", 1.0, None),
        "p3d29_locality_extra_m": ("p3d29_locality", 0.02, None),
        "p3d29_cliff_form_extra_m": ("p3d29_cliff_form", 0.02, None),
        "p3d29_tree_ground_extra_m": ("p3d29_tree_ground", 0.001, None),
    }
    slack_indices = {}
    for name in slack_spec:
        slack_indices[name] = next_event_column
        next_event_column += 1
    curvature_l1_indices = {}
    for spec_index, item in enumerate(curvature_specs):
        if item["soft_l1"]:
            curvature_l1_indices[spec_index] = next_event_column
            next_event_column += 1
    smoothness_l1_indices = {}
    for spec_index in range(len(smoothness_specs)):
        smoothness_l1_indices[spec_index] = next_event_column
        next_event_column += 1
    drainage_slack_indices = {}
    drainage_slack_enabled = (
        drainage_mode == "soft" or "p3d31_drainage" in diagnostic_groups
    )
    if drainage_slack_enabled:
        for edge_index in range(len(drainage_candidates)):
            drainage_slack_indices[edge_index] = next_event_column
            next_event_column += 1
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
        upper[t_index] = np.inf
    lower[plane_h] = float(min(np.min(p["h0"]) for p in profiles) - 2.0)
    upper[plane_h] = float(max(np.max(p["h0"]) for p in profiles) + 2.0)
    lower[plane_gx:plane_gz + 1], upper[plane_gx:plane_gz + 1] = -PLANE_SLOPE_MAX, PLANE_SLOPE_MAX
    lower[plane_h] = upper[plane_h] = float(platform_meta["plane_height_at_R8_center_m"])
    lower[plane_gx] = upper[plane_gx] = float(platform_meta["platform_gradient_physical"][0])
    lower[plane_gz] = upper[plane_gz] = float(platform_meta["platform_gradient_physical"][1])
    integrality = np.zeros(nvars, dtype=np.uint8)
    for j in (*binary_index.values(), *quer_binary_index.values(), *wob_binary_index.values()):
        lower[j], upper[j], integrality[j] = 0.0, 1.0, 1
    for j in drainage_choice_indices.values():
        lower[j], upper[j], integrality[j] = 0.0, 1.0, 1
    flow_capacity = int(construction["drainage_candidate_meta"]["non_outlet_vertices"])
    for j in drainage_flow_indices.values():
        lower[j], upper[j] = 0.0, float(flow_capacity)
    for j in event_selector_indices.values():
        lower[j], upper[j], integrality[j] = 0.0, 1.0, 1
    for j in event_hit_indices.values():
        lower[j], upper[j], integrality[j] = 0.0, 1.0, 1
    for name, index in slack_indices.items():
        group = slack_spec[name][0]
        lower[index] = 0.0
        upper[index] = np.inf if group in diagnostic_groups else 0.0
    for index in curvature_l1_indices.values():
        lower[index] = 0.0
        upper[index] = np.inf
    for index in smoothness_l1_indices.values():
        lower[index] = 0.0
        upper[index] = np.inf
    for index in drainage_slack_indices.values():
        lower[index] = 0.0
        upper[index] = 10.0 if drainage_mode == "soft" or "p3d31_drainage" in diagnostic_groups else 0.0
    # Cap only the new generic relaxations. These finite caps make the event
    # disjunction big-M values valid after variable-bound relaxation as well.
    slack_caps = {
        "grade_cross_extra_m": 10.0, "grade_same_extra_m": 10.0,
        "endpoint_r8a_extra_m": 10.0,
        "plane_slope_polygon_extra_pp": 100.0,
        "plane_slope_box_extra_pp": 100.0,
        "variable_bounds_extra_m": 10.0,
        "route_profile_slope_extra_m": 10.0,
        "source_monotone_extra_m": 10.0,
        # Diagnostic caps exceed the largest ±4 m surface bounds and keep
        # the reported elastic minimum from being clipped by an arbitrary
        # small cap. Official hard solves set these four slacks to exactly 0.
        "p3d29_locality_extra_m": 10.0,
        "p3d29_cliff_form_extra_m": 10.0,
        "p3d29_tree_ground_extra_m": 10.0,
    }
    for name, cap in slack_caps.items():
        upper[slack_indices[name]] = cap if slack_spec[name][0] in diagnostic_groups else 0.0

    # Preserve the original finite bounds as rows for the height, mesh-target,
    # stage and plane-height variables. Their solver bounds are expanded by
    # the maximum diagnostic slack; binary bounds remain exact.
    base_lower, base_upper = lower.copy(), upper.copy()
    generic_bound_indices = [*range(total_h), *range(surface_start, surface_start + surface_count),
                             t_index, plane_h]
    bound_cap = slack_caps["variable_bounds_extra_m"]
    for j in generic_bound_indices:
        if np.isfinite(base_lower[j]):
            lower[j] = base_lower[j] - bound_cap
        if np.isfinite(base_upper[j]):
            upper[j] = base_upper[j] + bound_cap
    # Slope box bounds are represented as rows, with a percentage-point slack.
    slope_box_cap = slack_caps["plane_slope_box_extra_pp"] / 100.0
    lower[plane_gx:plane_gz + 1] = -PLANE_SLOPE_MAX - slope_box_cap
    upper[plane_gx:plane_gz + 1] = PLANE_SLOPE_MAX + slope_box_cap

    row_i: list[int] = []
    col_i: list[int] = []
    vals: list[float] = []
    rhs: list[float] = []
    family_counts: dict[str, int] = {}
    row_families: list[str] = []
    current_family = "unclassified"

    def add(row: dict[int, float], bound: float) -> None:
        family_counts[current_family] = family_counts.get(current_family, 0) + 1
        rid = len(rhs)
        row_families.append(current_family)
        for col, value in row.items():
            if abs(value) > 1e-13:
                row_i.append(rid)
                col_i.append(int(col))
                vals.append(float(value))
        rhs.append(float(bound))

    current_family = "crossing_stage_cap"
    if stage_limit is not None:
        add({t_index: 1.0, slack_indices["crossing_stage_extra_m"]: -1.0}, float(stage_limit))

    # Explicitly encode finite original variable bounds with the dedicated
    # family slack. This is a diagnostic bound relaxation, not a model change.
    current_family = "variable_bounds"
    bound_slack = slack_indices["variable_bounds_extra_m"]
    for j in generic_bound_indices:
        if np.isfinite(base_upper[j]):
            add({j: 1.0, bound_slack: -1.0}, float(base_upper[j]))
        if np.isfinite(base_lower[j]):
            add({j: -1.0, bound_slack: -1.0}, -float(base_lower[j]))
    current_family = "plane_slope_box"
    for j in (plane_gx, plane_gz):
        add({j: 1.0, slack_indices["plane_slope_box_extra_pp"]: -0.01}, PLANE_SLOPE_MAX)
        add({j: -1.0, slack_indices["plane_slope_box_extra_pp"]: -0.01}, PLANE_SLOPE_MAX)

    # p3d20 does not use local height pins or an R9w equality lock.
    hp_lock_count = 0
    regression_locks: dict[str, int] = {}

    # Bilinear evaluation at every checker sample on the emitted mesh raster.
    def mesh_row(px: float, pz: float) -> dict[int, float]:
        return bilinear_row(px, pz, grid_x0, grid_z0, fs, width, height)

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

    def add_final_height_equality(row: dict[int, float], fixed: float,
                                  target: float) -> None:
        add(row, float(target) - fixed)
        add({column: -value for column, value in row.items()},
            -float(target) + fixed)

    current_family = "p3d32_fixed_anchors"
    for index, target in zip(
        (plane_gx, plane_gz), platform_meta["platform_gradient_physical"],
    ):
        add({index: 1.0}, float(target))
        add({index: -1.0}, -float(target))
    crossing_row, crossing_fixed = route_field_row(*P3D32_CROSSING_ANCHOR)
    add_final_height_equality(
        crossing_row, crossing_fixed, float(platform_meta["crossing_anchor_height_m"]),
    )
    ramp2_row, ramp2_fixed = route_field_row(*P3D32_RAMP2_START)
    add_final_height_equality(
        ramp2_row, ramp2_fixed, float(platform_meta["rampe_2_start_height_m"]),
    )

    def subtract_rows(left: dict[int, float], right: dict[int, float]) -> dict[int, float]:
        result = dict(left)
        for column, value in right.items():
            result[column] = result.get(column, 0.0) - value
        return {column: value for column, value in result.items() if abs(value) > 1e-13}

    # p3d29 retains the fixed 7.5 m locality ring and replaces the two
    # conflicting construction helpers: the flood is seeded from the p3d26
    # V3 surface, while road/crossing/runout curvature uses an L1 penalty.
    construction_rows = {
        "locality_outside": 0, "locality_ring": 0,
        "cliff_curvature_hard": 0, "cliff_curvature_l1": 0, "tree_ground": 0,
    }
    construction_meta = {
        "variant": construction_variant,
        "p3d31_variant": variant,
        "official_sink_policy": construction["official_sink_policy"],
        "modeled_drainage_candidate_count": construction["modeled_drainage_candidate_count"],
        "ring_width_m": float(construction["ring_width_m"]),
        "ring_tolerance_inner_m": 0.02, "outside_tolerance_m": 0.001,
        "drainage_eps_m": drainage_eps_m,
        "drainage_l1_mode": ("off" if variant == "1" else
                             "soft" if drainage_slack_enabled else "hard"),
        "drainage_l1_scale_m": P3D31_DRAINAGE_L1_SCALE_M,
        "drainage_formulation": (
            "official checker event cuts only; no per-cell successor or outlet reachability constraint"
            if variant == "1" else
            "one selected successor per non-outlet; conditional height drop; single-commodity flow"
        ),
        "drainage_candidates": construction["drainage_candidate_meta"],
        "drainage_binary_variables": len(drainage_choice_indices),
        "drainage_flow_variables": len(drainage_flow_indices),
        "drainage_slack_variables": len(drainage_slack_indices),
        "priority_flood_seed": p3d26_meta,
        "p3d23_route_pair_radius_m": 4.5, "crossing_radius_map": 4.0,
        "exact_v3_transfer_support_vertices": construction["transfer_support_vertices"],
        "endpoint_runout_support_vertices": construction["endpoint_support_vertices"],
        "runout_along_map": construction["runout_along_map"],
        "runout_across_map": construction["runout_across_map"],
        "hard_curvature_tolerance_rule": "max(0.02 m, 0.25 * abs(p3d17 reference second difference))",
        "curvature_hard_stencils": sum(not item["soft_l1"] for item in curvature_specs),
        "curvature_l1_stencils": sum(item["soft_l1"] for item in curvature_specs),
        "curvature_l1_weight_rule": "1 / max(0.02 m, 0.25 * abs(reference second difference))",
        "tree_ground_tolerance_m": P3D29_TREE_GROUND_TOL_M,
        "counts": construction["counts"],
        "routes": construction["routes"],
    }
    construction_meta["p3d32_window_bounds"] = {
        "x_map": [grid_x0, grid_x1], "z_map": [grid_z0, grid_z1],
        "active_vertices_core_plus_ring": int(active_mask.sum()),
        "ring_width_m": float(construction["ring_width_m"]),
        "outside_window_transfer_support_vertices": int(
            construction["transfer_support_outside_active_vertices"]
        ),
    }
    construction_meta["p3d32_smoothness"] = {
        "rule": "L1 deviation of second differences from p3d17 in active non-cliff gentle-slope stencils",
        "reference_slope_range": [0.15, 0.80],
        "stencils": len(smoothness_specs),
        "terms": len(smoothness_specs),
    }
    construction_spec = {
        "tag": "p3d31", "source_relief_sha256": hashlib.sha256(RELIEF.read_bytes()).hexdigest(),
        "p3d17_D1_reference_sha256": hashlib.sha256(
            p3d17_output.astype("<f4", copy=False).tobytes()).hexdigest(),
        "construction": construction,
    }
    construction_spec_path = out.with_name(out.stem + "_construction.json")
    construction_spec_path.parent.mkdir(parents=True, exist_ok=True)
    construction_spec_bytes = (json.dumps(
        construction_spec, indent=2, sort_keys=True, separators=(",", ": "),
    ) + "\n").encode("utf-8")
    construction_spec_path.write_bytes(construction_spec_bytes)
    construction_meta["spec_file"] = construction_spec_path.name
    construction_meta["spec_sha256"] = hashlib.sha256(construction_spec_bytes).hexdigest()

    def add_final_height_band(row: dict[int, float], fixed: float,
                              ref_height: float, tolerance: float,
                              slack_index: int) -> None:
        upper_row = dict(row)
        lower_row = {column: -value for column, value in row.items()}
        upper_row[slack_index] = -1.0
        lower_row[slack_index] = -1.0
        add(upper_row, ref_height + tolerance - fixed)
        add(lower_row,
            -ref_height + tolerance + fixed)

    locality_row_debug = {}
    locality_debug_points = {(150.5, 42.5), (152.5, 42.5)}

    def add_locality_band(ix: int, iz: int, tolerance: float) -> None:
        px, pz = grid_x0 + ix / fs, grid_z0 + iz / fs
        row, fixed = route_field_row(px, pz)
        reference_height = float(p3d17_output[iz, ix])
        upper_row = dict(row)
        lower_row = {column: -value for column, value in row.items()}
        slack_index = slack_indices["p3d29_locality_extra_m"]
        upper_row[slack_index] = -1.0
        lower_row[slack_index] = -1.0
        upper_index = len(rhs)
        add(upper_row, reference_height + tolerance - fixed)
        lower_index = len(rhs)
        add(lower_row, -reference_height + tolerance + fixed)
        if (round(px, 6), round(pz, 6)) in locality_debug_points:
            locality_row_debug[(px, pz)] = {
                "upper_row": upper_index, "lower_row": lower_index,
                "upper_rhs": float(rhs[upper_index]), "lower_rhs": float(rhs[lower_index]),
                "target_coefficients": {str(k): float(v) for k, v in row.items()},
                "fixed": fixed, "reference": reference_height,
                "tolerance": float(tolerance),
            }

    current_family = "p3d29_locality_outside"
    for iz, ix in zip(*np.nonzero(~active_mask)):
        add_locality_band(int(ix), int(iz), 0.001)
        construction_rows["locality_outside"] += 2
    current_family = "p3d29_locality_ring"
    for iz, ix in zip(*np.nonzero(ring_mask)):
        add_locality_band(int(ix), int(iz), float(ring_tolerance_m[iz, ix]))
        construction_rows["locality_ring"] += 2

    drainage_edges_by_child: dict[int, list[int]] = {}
    drainage_incoming: dict[int, list[int]] = {}
    for edge_index, (child, parent, _eps_m) in enumerate(drainage_candidates):
        drainage_edges_by_child.setdefault(int(child), []).append(edge_index)
        drainage_incoming.setdefault(int(parent), []).append(edge_index)
    active_flat = active_mask.ravel()
    outlets = set(int(v) for v in construction["outlet_flat_indices"])
    drainage_nodes = [int(v) for v in np.flatnonzero(active_flat) if int(v) not in outlets]
    if variant == "1":
        drainage_nodes = []
    drainage_node_rows: dict[int, tuple[dict[int, float], float]] = {}
    for node in np.flatnonzero(active_flat):
        iz, ix = divmod(int(node), width)
        drainage_node_rows[int(node)] = route_field_row(
            grid_x0 + ix / fs, grid_z0 + iz / fs,
        )

    current_family = "p3d31_drainage_successor_choice"
    for child in drainage_nodes:
        edge_ids = drainage_edges_by_child.get(child, [])
        if not edge_ids:
            raise RuntimeError(f"p3d31 flow node {child} has no successor candidates")
        degree = {drainage_choice_indices[i]: 1.0 for i in edge_ids}
        add(degree, 1.0)
        add({column: -value for column, value in degree.items()}, -1.0)
        construction_rows["drainage_successor_choice"] = (
            construction_rows.get("drainage_successor_choice", 0) + 2
        )

    current_family = "p3d31_drainage_single_commodity_flow"
    for edge_index, (child, parent, _eps_m) in enumerate(drainage_candidates):
        choice = drainage_choice_indices[edge_index]
        flow = drainage_flow_indices[edge_index]
        add({flow: 1.0, choice: -float(flow_capacity)}, 0.0)
        construction_rows["drainage_flow_capacity"] = (
            construction_rows.get("drainage_flow_capacity", 0) + 1
        )
        slack_index = drainage_slack_indices.get(edge_index)
        if slack_index is not None:
            current_family = "p3d31_drainage_slack_activation"
            add({slack_index: 1.0, choice: -10.0}, 0.0)
            construction_rows["drainage_slack_activation"] = (
                construction_rows.get("drainage_slack_activation", 0) + 1
            )
            current_family = "p3d31_drainage_single_commodity_flow"
    for node in drainage_nodes:
        balance: dict[int, float] = {}
        for edge_index in drainage_edges_by_child.get(node, []):
            balance[drainage_flow_indices[edge_index]] = 1.0
        for edge_index in drainage_incoming.get(node, []):
            balance[drainage_flow_indices[edge_index]] = -1.0
        add(balance, 1.0)
        add({column: -value for column, value in balance.items()}, -1.0)
        construction_rows["drainage_flow_conservation"] = (
            construction_rows.get("drainage_flow_conservation", 0) + 2
        )

    current_family = "p3d31_drainage_selected_edge_height"
    for edge_index, (child, parent, eps_m) in enumerate(drainage_candidates):
        child_row, child_fixed = drainage_node_rows[int(child)]
        parent_row, parent_fixed = drainage_node_rows[int(parent)]
        drain_row = subtract_rows(parent_row, child_row)
        choice = drainage_choice_indices[edge_index]
        slack_index = drainage_slack_indices.get(edge_index)
        if slack_index is not None:
            drain_row[slack_index] = -1.0
        fixed = parent_fixed - child_fixed
        max_unselected = fixed + sum(
            value * (upper[column] if value >= 0.0 else lower[column])
            for column, value in drain_row.items()
            if column != choice and column != slack_index
        )
        big_m = max(1e-6, max_unselected + float(eps_m) + 1e-5)
        drain_row[choice] = big_m
        add(drain_row, big_m - float(eps_m) - fixed)
        construction_rows["drainage_selected_edge_height"] = (
            construction_rows.get("drainage_selected_edge_height", 0) + 1
        )

    def reference_sample(px: float, pz: float) -> float:
        return float(ndi.map_coordinates(
            reference_full, [[pz * rs], [px * rs]], order=1, mode="nearest",
        )[0])

    def add_final_second_difference(spec_index: int, spec: dict) -> None:
        az, ax, iz, ix, bz, bx = spec["indices"]
        points = [
            (grid_x0 + ax / fs, grid_z0 + az / fs),
            (grid_x0 + ix / fs, grid_z0 + iz / fs),
            (grid_x0 + bx / fs, grid_z0 + bz / fs),
        ]
        expression: dict[int, float] = {}
        fixed_value = 0.0
        for (px, pz), coefficient in zip(points, (1.0, -2.0, 1.0)):
            row, fixed = route_field_row(px, pz)
            for column, value in row.items():
                expression[column] = expression.get(column, 0.0) + coefficient * value
            fixed_value += coefficient * fixed
        expression = {column: value for column, value in expression.items()
                      if abs(value) > 1e-13}
        reference_second = float(spec["reference_second_difference_m"])
        if spec["soft_l1"]:
            absolute_deviation = curvature_l1_indices[spec_index]
            positive = dict(expression)
            negative = {column: -value for column, value in expression.items()}
            positive[absolute_deviation] = -1.0
            negative[absolute_deviation] = -1.0
            add(positive, reference_second - fixed_value)
            add(negative, -reference_second + fixed_value)
            construction_rows["cliff_curvature_l1"] += 2
        else:
            tolerance = float(spec["hard_tolerance_m"])
            upper_expression = dict(expression)
            lower_expression = {column: -value for column, value in expression.items()}
            upper_expression[slack_indices["p3d29_cliff_form_extra_m"]] = -1.0
            lower_expression[slack_indices["p3d29_cliff_form_extra_m"]] = -1.0
            add(upper_expression, reference_second + tolerance - fixed_value)
            add(lower_expression, -reference_second + tolerance + fixed_value)
            construction_rows["cliff_curvature_hard"] += 2

    current_family = "p3d29_cliff_gorge_curvature"
    for spec_index, spec in enumerate(curvature_specs):
        add_final_second_difference(spec_index, spec)

    current_family = "p3d32_slope_smoothness_l1"
    for spec_index, spec in enumerate(smoothness_specs):
        az, ax, iz, ix, bz, bx = spec["indices"]
        expression: dict[int, float] = {}
        fixed_value = 0.0
        for px, pz, coefficient in (
            (grid_x0 + ax / fs, grid_z0 + az / fs, 1.0),
            (grid_x0 + ix / fs, grid_z0 + iz / fs, -2.0),
            (grid_x0 + bx / fs, grid_z0 + bz / fs, 1.0),
        ):
            row, fixed = route_field_row(px, pz)
            for column, value in row.items():
                expression[column] = expression.get(column, 0.0) + coefficient * value
            fixed_value += coefficient * fixed
        smooth_slack = smoothness_l1_indices[spec_index]
        positive = dict(expression)
        negative = {column: -value for column, value in expression.items()}
        positive[smooth_slack] = -1.0
        negative[smooth_slack] = -1.0
        reference_second = float(spec["reference_second_difference_m"])
        add(positive, reference_second - fixed_value)
        add(negative, -reference_second + fixed_value)

    # Tree sites remain source-identical. A 3x3 D1 mesh stencil around every
    # tree in the work area holds the reference ground within 1 mm, preserving
    # the local slope used by G11 as well as the soil height beneath the tree.
    current_family = "p3d29_tree_ground_reference"
    for tree_index, tree_object in enumerate(data.get("baeume", [])):
        try:
            tx, tz = float(tree_object[0]), float(tree_object[2])
        except (TypeError, ValueError, IndexError):
            continue
        if not (grid_x0 <= tx <= grid_x1 and grid_z0 <= tz <= grid_z1):
            continue
        tix = int(round((tx - grid_x0) * fs))
        tiz = int(round((tz - grid_z0) * fs))
        if not (0 <= tix < width and 0 <= tiz < height and active_mask[tiz, tix]):
            continue
        for dz in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ix, iz = tix + dx, tiz + dz
                if not (0 <= ix < width and 0 <= iz < height):
                    continue
                px, pz = grid_x0 + ix / fs, grid_z0 + iz / fs
                row, fixed = route_field_row(px, pz)
                add_final_height_band(row, fixed, reference_sample(px, pz),
                                      P3D29_TREE_GROUND_TOL_M,
                                      slack_indices["p3d29_tree_ground_extra_m"])
                construction_rows["tree_ground"] += 2

    construction_meta["linear_constraint_rows"] = construction_rows
    construction_meta["outlet_note"] = (
        "All active work-area boundary cells are outlets. Each active non-outlet selects exactly "
        "one local successor; single-commodity unit supply at every non-outlet forces all selected "
        "paths to outlets and excludes directed cycles. The p3d29 Priority-Flood tree remains in "
        "the construction record for comparison but does not constrain the p3d31 active area."
    )

    def event_big_m(row: dict[int, float], fixed: float, threshold: float) -> float:
        maximum = fixed + sum(
            value * (upper[column] if value >= 0.0 else lower[column])
            for column, value in row.items()
        )
        return max(1e-6, maximum - threshold + 1e-5)

    # Checker-triggered local LP cuts. Disjunctions are replaced by conservative
    # direct inequalities so the model passed to HiGHS remains a pure LP.
    for cut_i, cut in enumerate(event_cuts):
        current_family = "event_cut_" + cut["kind"]
        if cut["kind"] == "G5":
            point_row, point_fixed = route_field_row(*cut["point"])
            references = cut["references"]
            if not references:
                raise ValueError("G5-Lazy-Cut ohne Vergleichspunkte")
            row = dict(point_row)
            fixed = point_fixed
            for ref in references:
                ref_row, ref_fixed = route_field_row(*ref)
                for column, value in ref_row.items():
                    row[column] = row.get(column, 0.0) - value / len(references)
                fixed -= ref_fixed / len(references)
            add(row, (0.6 - 1e-5) - fixed)
        elif cut["kind"] == "R4":
            center_row, center_fixed = route_field_row(*cut["center"])
            sides = cut["sides"]
            if not sides:
                raise ValueError("R4-Lazy-Cut ohne Seiten")
            row = {column: -value for column, value in center_row.items()}
            fixed = -center_fixed
            for side in sides:
                side_row, side_fixed = route_field_row(*side)
                for column, value in side_row.items():
                    row[column] = row.get(column, 0.0) + value / len(sides)
                fixed += side_fixed / len(sides)
            add(row, (1.5 - 1e-5) - fixed)
        elif cut["kind"] == "R5":
            saddle_row, saddle_fixed = route_field_row(*cut["saddle"])
            for pit in cut.get("pits", [cut["pit"]]):
                pit_row, pit_fixed = route_field_row(*pit)
                row = subtract_rows(saddle_row, pit_row)
                fixed = saddle_fixed - pit_fixed
                threshold = 1.0 - 1e-5
                add(row, threshold - fixed)
        elif cut["kind"] == "R8b":
            saddle_row, saddle_fixed = route_field_row(*cut["saddle"])
            for pit in cut.get("pits", [cut["pit"]]):
                pit_row, pit_fixed = route_field_row(*pit)
                row = subtract_rows(saddle_row, pit_row)
                fixed = saddle_fixed - pit_fixed
                threshold = 0.30 - 1e-5
                add(row, threshold - fixed)
        elif cut["kind"] == "G11":
            point_row, point_fixed = route_field_row(*cut["point"])
            y = float(cut["object_height_m"])
            clearance = 0.6 - 1e-5
            negative_row = {column: -value for column, value in point_row.items()}
            add(point_row, y + clearance - point_fixed)
            add(negative_row, -y + clearance + point_fixed)
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
            window = cut.get("selected_window")
            if not window:
                raise ValueError("R5-Spitzen-Lazy-Cut benötigt das offizielle lokale Minimum")
            for node in window:
                node_row, node_fixed = route_field_row(*node)
                row = subtract_rows(point_row, node_row)
                fixed = point_fixed - node_fixed
                add(row, (0.5 - 1e-5) - fixed)
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
        elif cut["kind"] == "FLOOR":
            point_row, point_fixed = route_field_row(*cut["point"])
            minimum = float(cut["minimum_final_height_m"])
            add({column: -value for column, value in point_row.items()},
                point_fixed - minimum)
        else:
            raise ValueError(f"Unbekannter Ereignisschnitt: {cut['kind']}")

    # The event catalogue is D1-local. Fixed non-D1 components are taken from
    # the official round-05 probe (G5=67, R5-hole=17); total and D1 allowances
    # are both kept explicit so their measured excesses can be reported.
    g5_hits = [event_hit_indices[i] for i, cut in enumerate(event_cuts) if cut["kind"] == "G5"]
    r5_hits = [event_hit_indices[i] for i, cut in enumerate(event_cuts) if cut["kind"] == "R5"]
    r8b_hits = [event_hit_indices[i] for i, cut in enumerate(event_cuts) if cut["kind"] == "R8b"]
    r4_hits = [event_hit_indices[i] for i, cut in enumerate(event_cuts) if cut["kind"] == "R4"]
    current_family = "event_counter_caps"
    if g5_hits:
        add({**{j: 1.0 for j in g5_hits}, slack_indices["g5_total_extra_hits"]: -1.0}, 69.0 - 67.0)
        add({**{j: 1.0 for j in g5_hits}, slack_indices["g5_d1_extra_hits"]: -1.0}, 2.0)
    if r5_hits:
        add({**{j: 1.0 for j in r5_hits}, slack_indices["r5_total_extra_hits"]: -1.0}, 22.0 - 17.0)
        add({**{j: 1.0 for j in r5_hits}, slack_indices["r5_d1_extra_hits"]: -1.0}, 5.0)
    if r8b_hits:
        add({**{j: 1.0 for j in r8b_hits}, slack_indices["r8b_d1_extra_hits"]: -1.0}, 1.0)
    if r4_hits:
        add({**{j: 1.0 for j in r4_hits}, slack_indices["r4_d1_extra_hits"]: -1.0}, 0.0)
    g11_hits = [event_hit_indices[i] for i, cut in enumerate(event_cuts) if cut["kind"] == "G11"]
    if g11_hits:
        current_family = "event_counter_caps"
        # Only newly observed D1 G11 events enter this cut list. The two
        # baseline D1 events already consume the allowance, so the counter
        # slack measures the number of new events retained by the model.
        add({**{j: 1.0 for j in g11_hits},
             slack_indices["g11_d1_extra_hits"]: -1.0}, 0.0)

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
    endpoint_id = f"rampe_{endpoint['index']}_ende"
    endpoint_anchor = q0.tolist()
    endpoint_limit = r8a_pair_limit_m(endpoint_id, endpoint_anchor)
    endpoint_runout_pair_specs = [
        (pair, endpoint_limit, endpoint_id, endpoint_anchor)
        for pair in adjacent_pairs(end_runout_mask, exm, ezm)
    ]
    extra_endpoint_runout_pair_specs = []
    for profile in profiles:
        if profile["index"] not in (2, 11):
            continue
        endpoint_id = f"rampe_{profile['index']}_anfang"
        endpoint_anchor = np.asarray(profile["coords"][0], dtype=np.float64)
        endpoint_limit = r8a_pair_limit_m(endpoint_id, endpoint_anchor)
        extra_endpoint_runout_pair_specs.extend(
            (pair, endpoint_limit, endpoint_id, endpoint_anchor.tolist())
            for pair in endpoint_runout_pairs_for(profile, True)
        )
    endpoint_runout_pair_specs = [
        *endpoint_runout_pair_specs, *extra_endpoint_runout_pair_specs,
    ]

    # R8 checker local road-neighbor pairs, evaluated bilinearly on the 0.5 grid.
    current_family = "r8_neighbor_stage"
    for a, b in neighbor_pairs:
        entries = {surface_start + j: v for j, v in pair_row(a, b).items()}
        add({**entries, t_index: -1.0}, 0.0)
        add({**{j: -v for j, v in entries.items()}, t_index: -1.0}, 0.0)

    def add_pair_cap(px0: float, pz0: float, px1: float, pz1: float, cap: float,
                     slack_index: int | None = None) -> None:
        row0, fixed0 = route_field_row(px0, pz0)
        row1, fixed1 = route_field_row(px1, pz1)
        entries = dict(row0)
        for index, value in row1.items():
            entries[index] = entries.get(index, 0.0) - value
        forward = dict(entries)
        backward = {index: -value for index, value in entries.items()}
        if slack_index is not None:
            forward[slack_index] = -1.0
            backward[slack_index] = -1.0
        add(forward, cap - (fixed0 - fixed1))
        add(backward, cap + (fixed0 - fixed1))

    endpoint_stage_enabled = os.environ.get("P3D20_ENDPOINT_STAGE_LOCK", "1") != "0"
    endpoint_r8a_enabled = os.environ.get("P3D20_ENDPOINT_R8A_LOCK", "1") != "0"
    if endpoint_stage_enabled:
        current_family = "endpoint_stage_pairs"
        for pair in endpoint_stage_pairs:
            add_pair_cap(*pair, 0.054 - ENDPOINT_STAGE_FLOAT32_GUARD_M,
                         slack_indices["endpoint_stage_extra_m"])
    if endpoint_r8a_enabled:
        current_family = "endpoint_r8a_runout_pairs"
        for pair, pair_limit, _endpoint_id, _anchor in endpoint_runout_pair_specs:
            add_pair_cap(*pair, pair_limit - R8A_FLOAT32_GUARD_M,
                         slack_indices["endpoint_r8a_extra_m"])

    # Mesh axis samples agree with the exact ramp variables within 2 cm.
    axis_count = 0
    current_family = "axis_supports"
    for route, p in enumerate(profiles):
        for k, (x, z) in enumerate(p["coords"]):
            if not (grid_x0 - 1e-9 <= x <= grid_x1 + 1e-9 and grid_z0 - 1e-9 <= z <= grid_z1 + 1e-9):
                continue
            row, fixed = route_field_row(float(x), float(z))
            hidx = h_offsets[route] + k
            plus = {**row, hidx: -1.0, slack_indices["axis_tolerance_extra_m"]: -1.0}
            minus = {**{j: -v for j, v in row.items()}, hidx: 1.0,
                     slack_indices["axis_tolerance_extra_m"]: -1.0}
            add(plus, axis_tolerance - fixed)
            add(minus, axis_tolerance + fixed)
            axis_count += 1

    # Hold the complete plane core at checker resolution, using bilinear mesh values.
    plane_count = 0
    checker_height, checker_width = local.shape
    current_family = "plane_core_supports"
    for iz in range(checker_height):
        for ix in range(checker_width):
            x, z = local_x0 + ix / checker_fs, local_z0 + iz / checker_fs
            dx, dz = (x - CROSSING[0]) * CELL_M, (z - CROSSING[1]) * CELL_M
            if np.hypot(dx, dz) > PLANE_RADIUS_M + 1e-9:
                continue
            entries, final_fixed = route_field_row(x, z)
            entries.update({plane_h: -1.0, plane_gx: -dx, plane_gz: -dz})
            positive = dict(entries)
            negative = {j: -v for j, v in entries.items()}
            positive[slack_indices["plane_tolerance_extra_m"]] = -1.0
            negative[slack_indices["plane_tolerance_extra_m"]] = -1.0
            add(positive, plane_tolerance - final_fixed)
            add(negative, plane_tolerance + final_fixed)
            # The p3d32 crossing platform is an exact plane on the unchanged
            # 2 m physical kernel. The existing 2 cm hard support remains too.
            add(entries, -final_fixed)
            add({j: -v for j, v in entries.items()}, final_fixed)
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
    current_family = "R8_gitter_safety"
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
            positive = dict(entries)
            negative = {column: -value for column, value in entries.items()}
            positive[slack_indices["safety_gitter_extra_m"]] = -1.0
            negative[slack_indices["safety_gitter_extra_m"]] = -1.0
            add(positive, R8_GITTER_LIMIT_M)
            add(negative, R8_GITTER_LIMIT_M)
            gitter_pairs.append((i, j))
            gitter_pair_count += 1

    quer_ids, quer_supports, quer_design = gate_support_rows(quer_mask)
    quer_inverse = np.linalg.pinv(quer_design)
    quer_row_count = 0
    quer_bound = (R8_QUER_LIMIT_PCT / 100.0) * np.cos(np.pi / 32.0)
    current_family = "R8_quer_safety"
    for angle in np.arange(32, dtype=np.float64) * (2.0 * np.pi / 32.0):
        weights = np.cos(angle) * quer_inverse[0] + np.sin(angle) * quer_inverse[1]
        entries = combine_support_rows(weights, quer_supports)
        entries[slack_indices["safety_quer_extra_pp"]] = -np.cos(np.pi / 32.0) / 100.0
        add(entries, quer_bound)
        quer_row_count += 1

    current_family = "plane_slope_polygon"
    polygon_bound = PLANE_SLOPE_MAX * np.cos(np.pi / 32.0)
    for angle in np.arange(32) * (2.0 * np.pi / 32.0):
        add({plane_gx: float(np.cos(angle)), plane_gz: float(np.sin(angle)),
             slack_indices["plane_slope_polygon_extra_pp"]: -0.01}, polygon_bound)

    # The profile section gradient and p3d15 monotonic source-descending rows.
    current_family = "route_profile_slope"
    for route, p in enumerate(profiles):
        start = h_offsets[route]
        for k in range(len(p["h0"]) - 1):
            add({start + k + 1: 1.0, start + k: -1.0,
                 slack_indices["route_profile_slope_extra_m"]: -1.0}, SLOPE_MAX * SAMPLE_STEP)
            add({start + k: 1.0, start + k + 1: -1.0,
                 slack_indices["route_profile_slope_extra_m"]: -1.0}, SLOPE_MAX * SAMPLE_STEP)
            current_family = "source_monotonicity"
            if p["h0"][k + 1] <= p["h0"][k] + 1e-9:
                add({start + k + 1: 1.0, start + k: -1.0,
                     slack_indices["source_monotone_extra_m"]: -1.0}, 0.0)
            current_family = "route_profile_slope"

    # Official R3 operator over the field that the unchanged p3d17 transfer
    # actually emits. The checker samples at 0.25 map units and counts the
    # maximum over each 16-sample (4.8 m) section.
    r3_d1_terms = []
    current_family = "r3_long_constraints"
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
                upper_row = {**row, bidx: -upper_relax,
                             slack_indices["r3_long_residual_m"]: -1.0}
                lower_row = {**{j: -v for j, v in row.items()}, bidx: -lower_relax,
                             slack_indices["r3_long_residual_m"]: -1.0}
                add(upper_row, threshold - fixed)
                add(lower_row, threshold + fixed)
        for route, k, inside in section_lookup:
            if inside:
                r3_d1_terms.append(binary_index[(route, k // R3_SECTION_SAMPLES)])
        r3_count_row = {j: 1.0 for j in sorted(set(r3_d1_terms))}
        r3_count_row[slack_indices["r3_long_extra_hits"]] = -1.0
        add(r3_count_row, float(r3_limit))

    # The official cross-section formulas sample +/-1.5 map units. The fixed
    # numerical guards cover float32 mesh emission; the reported checker and
    # its 3.5%, 20%, and 0.08 m thresholds remain unchanged.
    current_family = "r3_cross_constraints"
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
                q_positive = dict(q_row)
                q_negative = {column: -value for column, value in q_row.items()}
                q_positive[slack_indices["safety_single_quer_extra_pp"]] = -1.0
                q_negative[slack_indices["safety_single_quer_extra_pp"]] = -1.0
                add(q_positive, R3_SINGLE_QUER_LIMIT_PCT - R3_FLOAT32_GUARD_PCT - q_fixed)
                add(q_negative, R3_SINGLE_QUER_LIMIT_PCT - R3_FLOAT32_GUARD_PCT + q_fixed)
                quer_big_m = 1000.0
                q_count_positive = {**q_row, q_binary: -quer_big_m,
                                    slack_indices["r3_quer_residual_pp"]: -1.0}
                q_count_negative = {**{column: -value for column, value in q_row.items()},
                                    q_binary: -quer_big_m,
                                    slack_indices["r3_quer_residual_pp"]: -1.0}
                add(q_count_positive, 3.5 - R3_FLOAT32_GUARD_PCT - q_fixed)
                add(q_count_negative, 3.5 - R3_FLOAT32_GUARD_PCT + q_fixed)

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
                wob_upper_relax = max(0.0, wob_max + 10.0 - wob_threshold)
                wob_lower_relax = max(0.0, -wob_min + 10.0 - wob_threshold)
                wob_positive = {**wob_row, wob_binary: -wob_upper_relax,
                                slack_indices["r3_wob_residual_m"]: -1.0}
                wob_negative = {**{column: -value for column, value in wob_row.items()},
                                wob_binary: -wob_lower_relax,
                                slack_indices["r3_wob_residual_m"]: -1.0}
                add(wob_positive, wob_threshold - wob_fixed)
                add(wob_negative, wob_threshold + wob_fixed)
            quer_section_terms.extend(quer_binary_index[(route, k // R3_SECTION_SAMPLES)]
                                      for r, k, inside in section_lookup if r == route and inside)
            wob_section_terms.extend(wob_binary_index[(route, k // R3_SECTION_SAMPLES)]
                                     for r, k, inside in section_lookup if r == route and inside)
        if quer_limit is not None:
            quer_count_row = {j: 1.0 for j in sorted(set(quer_section_terms))}
            quer_count_row[slack_indices["r3_quer_extra_hits"]] = -1.0
            add(quer_count_row, float(quer_limit))
        if wob_limit is not None:
            wob_count_row = {j: 1.0 for j in sorted(set(wob_section_terms))}
            wob_count_row[slack_indices["r3_wob_extra_hits"]] = -1.0
            add(wob_count_row, float(wob_limit))

    # Same-route and cross-route pairs from p3d15, with the selected physical grade.
    pairs = route_pairs(profiles)
    current_family = "route_pair_grade"
    for ra, ia, rb, ib, distance in pairs:
        va, vb = h_offsets[ra] + ia, h_offsets[rb] + ib
        bound = grade * distance
        slack_name = "grade_same_extra_m" if ra == rb else "grade_cross_extra_m"
        slack = slack_indices[slack_name]
        add({va: 1.0, vb: -1.0, slack: -1.0}, bound)
        add({va: -1.0, vb: 1.0, slack: -1.0}, bound)

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
    elif objective_mode == "diagnostic":
        for name, index in slack_indices.items():
            group, scale, _ = slack_spec[name]
            if group in diagnostic_groups:
                objective[index] = 1.0 / scale
        if "p3d31_drainage" in diagnostic_groups:
            for index in drainage_slack_indices.values():
                objective[index] = 1.0 / P3D31_DRAINAGE_L1_SCALE_M
    mip_start = None
    if mip_start_path is not None:
        mip_start = np.asarray(json.loads(mip_start_path.read_text(encoding="utf-8"))["x"], dtype=np.float64)
    # Use the same explicit single-thread HiGHS interface for every mode.
    result = highs_mip_solve(
        matrix, rhs, objective,
        np.zeros_like(integrality) if relax_integrality else integrality,
        lower, upper, mip_start, time_limit=time_limit_s,
    )
    primal_feasible = False
    feasibility_residuals = None
    if result.x is not None:
        activity = matrix @ result.x
        row_violation = activity - np.asarray(rhs)
        bound_violation = np.maximum(
            np.maximum(lower - result.x, result.x - upper), 0.0,
        )
        worst_row = int(np.argmax(row_violation)) if len(row_violation) else 0
        worst_bound = int(np.argmax(bound_violation)) if len(bound_violation) else 0
        feasibility_residuals = {
            "maximum_row_violation": float(max(0.0, row_violation[worst_row])) if len(row_violation) else 0.0,
            "worst_row_index": worst_row if len(row_violation) else None,
            "worst_row_family": row_families[worst_row] if len(row_families) else None,
            "solver_max_primal_infeasibility": float(result.max_primal_infeasibility),
            "loaded_matrix_delta": float(result.loaded_matrix_delta),
            "loaded_row_bound_delta": float(result.loaded_row_bound_delta),
            "maximum_solver_row_upper_violation": (
                float(max(0.0, np.max(result.row_value - result.loaded_row_upper)))
                if result.row_value is not None and len(result.row_value) else None
            ),
            "maximum_solver_matrix_activity_delta": (
                float(np.max(np.abs(activity - result.row_value)))
                if result.row_value is not None and len(activity) else None
            ),
            "maximum_variable_bound_violation": float(bound_violation[worst_bound]) if len(bound_violation) else 0.0,
            "worst_variable_index": worst_bound if len(bound_violation) else None,
        }
        primal_feasible = bool(
            feasibility_residuals["maximum_row_violation"] <= 2e-6
            and feasibility_residuals["maximum_variable_bound_violation"] <= 2e-6
            and (relax_integrality or np.all(np.abs(
                result.x[integrality.astype(bool)] - np.rint(result.x[integrality.astype(bool)])
            ) <= 2e-6))
        )
    if not primal_feasible or result.x is None:
        invalid_point = None
        if result.x is not None and feasibility_residuals is not None:
            row_id = feasibility_residuals["worst_row_index"]
            row_slice = matrix.getrow(int(row_id))
            invalid_point = {
                "worst_row": {
                    "index": int(row_id), "family": row_families[int(row_id)],
                    "rhs": float(rhs[int(row_id)]),
                    "matrix_activity": float(activity[int(row_id)]),
                    "solver_activity": (float(result.row_value[int(row_id)])
                                        if result.row_value is not None else None),
                    "terms": [[int(column), float(coefficient), float(result.x[int(column)])]
                              for column, coefficient in zip(row_slice.indices, row_slice.data)],
                },
                "diagnostic_slacks": {name: float(result.x[index])
                                      for name, index in slack_indices.items()},
            }
        for name in ("event_cut_G5", "event_cut_R4", "event_cut_R5", "event_cut_R8b", "event_cut_G11",
                     "event_cut_G6", "event_cut_R5sp", "event_cut_R8G", "event_cut_R9w",
                     "event_counter_caps", "regression_locks"):
            family_counts.setdefault(name, 0)
        summary = {
            "status": str(result.message),
            "status_code": int(result.status),
            "success": False,
            "primal_feasible": primal_feasible,
            "optimality_proven": bool(result.success),
            "objective_mode": objective_mode,
            "relaxed_integrality": relax_integrality,
            "primal_feasibility_residuals": feasibility_residuals,
            "invalid_solver_point_diagnostic": invalid_point,
            "stage_limit_m": stage_limit,
            "r3_long_limit": r3_limit,
            "r3_quer_limit": quer_limit,
            "r3_wob_limit": wob_limit,
            "variables": nvars,
            "constraints": len(rhs),
            "family_row_counts": dict(sorted(family_counts.items())),
            "p3d31_construction": construction_meta,
            "p3d26_priority_flood_seed": p3d26_meta,
            "curvature_l1_variable_count": len(curvature_l1_indices),
            "diagnostic_groups_enabled": sorted(diagnostic_groups),
            "slack_values": {**{name: None for name in slack_indices},
                             "p3d31_drainage_extra_m": None},
            "slack_units": {name: ("hits" if "hits" in name else "percentage_points" if "pp" in name else "m")
                            for name in slack_indices},
            "event_cut_count_by_kind": {
                kind: sum(cut["kind"] == kind for cut in event_cuts)
                for kind in sorted({cut["kind"] for cut in event_cuts})
            },
            "weighted_l1_scales": {name: scale for name, (_, scale, _) in slack_spec.items()},
        }
        summary["p3d32_variant"] = p3d32_variant
        summary["p3d32_platform"] = platform_meta
        summary["p3d32_linear_lazy_cuts"] = True
        summary["integer_variable_count"] = 0
        summary["all_solver_variables_continuous"] = bool(relax_integrality)
        summary["flood_cut_count"] = len(flood_cuts)
        out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return summary

    if objective_mode == "diagnostic":
        primary_objective = float(result.fun)
        primary_step = float(result.x[t_index])
        primary_x = result.x.copy()
        result_x = result.x
        tie_break_movement = 0.0
    else:
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
            for index in (*binary_index.values(), *quer_binary_index.values(), *wob_binary_index.values(),
                          *drainage_choice_indices.values(), *event_selector_indices.values()):
                fixed_value = float(round(result.x[index]))
                lower2[index] = upper2[index] = fixed_value
        c2 = np.zeros(nvars_secondary, dtype=np.float64)
        c2[nvars:nvars + total_h] = 1.0
        c2[nvars + total_h:] = 1.0
        for spec_index, column in curvature_l1_indices.items():
            c2[column] = float(curvature_specs[spec_index]["l1_weight"])
        for spec_index, column in smoothness_l1_indices.items():
            c2[column] = float(smoothness_specs[spec_index]["l1_weight"])
        for name, column in slack_indices.items():
            group, scale, _ = slack_spec[name]
            if group in diagnostic_groups:
                c2[column] = 1.0 / float(scale)
        if "p3d31_drainage" in diagnostic_groups:
            for column in drainage_slack_indices.values():
                c2[column] = 1.0 / P3D31_DRAINAGE_L1_SCALE_M
        secondary = linprog(c2, A_ub=A2, b_ub=b2, bounds=list(zip(lower2, upper2)), method="highs")
        if not secondary.success or secondary.x is None:
            raise RuntimeError(f"Minimax tie-break LP failed: {secondary.message}")
        result_x = secondary.x[:nvars]
        result.fun = primary_step
        result.x = result_x
        tie_break_movement = float(np.sum(secondary.x[nvars:nvars + slack_count]))
        tie_break_weighted_l1 = float(secondary.fun)
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
        "endpoint_stage_float32_guard_m": ENDPOINT_STAGE_FLOAT32_GUARD_M,
        "endpoint_R8a_pair_limit_m": R8A_DEFAULT_LIMIT_M,
        "endpoint_R8a_float32_guard_m": R8A_FLOAT32_GUARD_M,
        "endpoint_R8a_named_exception": {
            "name": R8A_RAMPE2_START_EXCEPTION,
            "limit_m": R8A_RAMPE2_START_LIMIT_M,
            "endpoint_id": R8A_RAMPE2_START_ENDPOINT_ID,
            "coordinate_map": list(R8A_RAMPE2_START_XZ),
            "source": "[F] Fabian widget t166s961, 2026-11-13",
        },
        "endpoint_stage_pair_count": len(endpoint_stage_pairs),
        "endpoint_R8a_pair_count": len(endpoint_runout_pair_specs),
        "R9w_exact_bandpass_lock_points": hp_lock_count,
        "D1_regression_fence_vertex_counts": regression_locks,
        "exact_event_cut_count": len(event_cuts),
        "exact_event_selector_count": event_selector_count,
        "p3d18_variant24_reference_D1_sha256": p3d18_reference_hash,
        "variables": nvars, "constraints": len(rhs),
        "objective_mode": objective_mode,
        "relaxed_integrality": relax_integrality,
        "p3d31_variant": variant,
        "official_sink_policy": construction["official_sink_policy"],
        "p3d26_priority_flood_seed": p3d26_meta,
        "curvature_l1_variable_count": len(curvature_l1_indices),
        "primal_feasibility_residuals": feasibility_residuals,
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
        "tie_break_weighted_l1_objective": float(
            tie_break_weighted_l1 if objective_mode != "diagnostic" else 0.0
        ),
        "tie_break_reference_mesh": reference_mesh_path.name if reference_mesh_path else "GB source field",
        "tie_break_reference_solution": reference_solution_path.name if reference_solution_path else None,
        "mip_dual_bound_m": (None if getattr(result, "mip_dual_bound", None) is None else float(result.mip_dual_bound)),
        "mip_gap": (None if getattr(result, "mip_gap", None) is None else float(result.mip_gap)),
    }
    summary["diagnostic_groups_enabled"] = sorted(diagnostic_groups)
    for name in ("event_cut_G5", "event_cut_R4", "event_cut_R5", "event_cut_R8b", "event_cut_G11",
                 "event_cut_G6", "event_cut_R5sp", "event_cut_R8G", "event_cut_R9w",
                 "event_counter_caps", "regression_locks"):
        family_counts.setdefault(name, 0)
    summary["family_row_counts"] = dict(sorted(family_counts.items()))
    summary["p3d31_construction"] = construction_meta
    summary["slack_values"] = {
        name: float(result.x[index]) for name, index in slack_indices.items()
    }
    summary["normalized_slack_values"] = {
        name: float(result.x[index]) / float(slack_spec[name][1])
        for name, index in slack_indices.items()
    }
    drainage_slack_values = np.asarray(
        [result.x[index] for index in drainage_slack_indices.values()], dtype=np.float64,
    )
    summary["slack_values"]["p3d31_drainage_extra_m"] = float(
        drainage_slack_values.max(initial=0.0)
    )
    summary["normalized_slack_values"]["p3d31_drainage_extra_m"] = float(
        drainage_slack_values.sum() / P3D31_DRAINAGE_L1_SCALE_M
    )
    summary["maximum_normalized_slack"] = max(
        summary["normalized_slack_values"].values(), default=0.0,
    )
    summary["slack_units"] = {
        name: ("hits" if "hits" in name else "percentage_points" if "pp" in name else "m")
        for name in slack_indices
    }
    summary["slack_units"]["p3d31_drainage_extra_m"] = "max_edge_m; L1 is reported separately"
    summary["weighted_l1_scales"] = {
        name: scale for name, (_, scale, _) in slack_spec.items()
    }
    summary["weighted_l1_scales"]["p3d31_drainage_extra_m"] = P3D31_DRAINAGE_L1_SCALE_M
    summary["weighted_l1_value"] = float(result.fun)
    summary["cliff_form_weighted_l1_value"] = float(sum(
        float(spec["l1_weight"]) * float(result.x[column])
        for spec_index, column in curvature_l1_indices.items()
        for spec in [curvature_specs[spec_index]]
    ))
    summary["drainage_l1_sum_m"] = float(drainage_slack_values.sum())
    summary["drainage_weighted_l1_value"] = float(
        drainage_slack_values.sum() / P3D31_DRAINAGE_L1_SCALE_M
    )
    if drainage_slack_indices:
        edge_slacks = [
            (float(result.x[column]), edge_index)
            for edge_index, column in drainage_slack_indices.items()
        ]
        max_slack_m, max_slack_edge = max(edge_slacks, default=(0.0, -1))
        if max_slack_edge >= 0:
            child, parent, eps_m = drainage_candidates[max_slack_edge]
            child_z, child_x = divmod(int(child), width)
            parent_z, parent_x = divmod(int(parent), width)
            max_slack_location = {
                "maximum_edge_slack_m": max_slack_m,
                "child_xz": [float(grid_x0 + child_x / fs), float(grid_z0 + child_z / fs)],
                "successor_xz": [float(grid_x0 + parent_x / fs), float(grid_z0 + parent_z / fs)],
                "required_eps_m": float(eps_m),
                "successor_choice_value": float(result.x[drainage_choice_indices[max_slack_edge]]),
            }
        else:
            max_slack_location = None
        summary["p3d31_drainage_slack_diagnostic"] = {
            "positive_edge_slack_count": int(np.count_nonzero(drainage_slack_values > 1e-8)),
            "sum_edge_slack_m": float(drainage_slack_values.sum()),
            "maximum_edge_slack": max_slack_location,
            "integrality_relaxed": bool(relax_integrality),
        }
    summary["cliff_form_l1_absolute_deviation_sum_m"] = float(sum(
        float(result.x[column]) for column in curvature_l1_indices.values()
    ))
    summary["p3d32_smoothness_l1_absolute_deviation_sum_m"] = float(sum(
        float(result.x[column]) for column in smoothness_l1_indices.values()
    ))
    summary["event_cut_count_by_kind"] = {
        kind: sum(cut["kind"] == kind for cut in event_cuts)
        for kind in sorted({cut["kind"] for cut in event_cuts})
    }
    summary["selected_soft_event_cut_relaxations_by_kind"] = {
        kind: int(sum(result.x[event_hit_indices[i]] > 0.5
                      for i, cut in enumerate(event_cuts) if cut["kind"] == kind))
        for kind in ("G5", "R5", "R8b", "R4", "G11")
    }
    summary["p3d32_variant"] = p3d32_variant
    summary["p3d32_platform"] = platform_meta
    summary["p3d32_linear_lazy_cuts"] = True
    summary["integer_variable_count"] = 0
    summary["all_solver_variables_continuous"] = bool(relax_integrality)
    summary["flood_cut_count"] = len(flood_cuts)
    summary["p3d32_smoothness_l1_variable_count"] = len(smoothness_l1_indices)
    summary["p3d32_smoothness_l1_row_count"] = 2 * len(smoothness_l1_indices)
    if result.x is not None:
        xsol = result.x
        def field_value(px: float, pz: float) -> float:
            row, fixed = route_field_row(px, pz)
            return fixed + sum(value * xsol[column] for column, value in row.items())

        final_grid = transfer_background + transfer_coverage * xsol[
            surface_start:surface_start + surface_count
        ].reshape(height, width)
        locality_violations = {}
        for label, mask, allowance in (
            ("outside", ~active_mask, np.full((height, width), 0.001)),
            ("transition_ring", ring_mask, ring_tolerance_m),
        ):
            amount = np.abs(final_grid - p3d17_output) - allowance
            amount = np.where(mask, amount, -np.inf)
            flat = int(np.argmax(amount))
            iz, ix = divmod(flat, width)
            locality_violations[label] = {
                "maximum_violation_m": float(max(0.0, amount[iz, ix])),
                "xz": [float(grid_x0 + ix / fs), float(grid_z0 + iz / fs)],
                "delta_m": float(final_grid[iz, ix] - p3d17_output[iz, ix]),
                "allowed_abs_delta_m": float(allowance[iz, ix]),
            }

        drainage_worst = (0.0, None)
        final_flat = final_grid.ravel()
        selected_drainage_edges = []
        for edge_index, (child, parent, eps_m) in enumerate(drainage_candidates):
            if float(xsol[drainage_choice_indices[edge_index]]) <= 0.5:
                continue
            slack_index = drainage_slack_indices.get(edge_index)
            slack_value = float(xsol[slack_index]) if slack_index is not None else 0.0
            violation = float(
                final_flat[int(parent)] + float(eps_m) - final_flat[int(child)] - slack_value
            )
            cz, cx = divmod(int(child), width)
            pz_, px_ = divmod(int(parent), width)
            selected = {
                "child_flat": int(child), "successor_flat": int(parent),
                "child_xz": [float(grid_x0 + cx / fs), float(grid_z0 + cz / fs)],
                "successor_xz": [float(grid_x0 + px_ / fs), float(grid_z0 + pz_ / fs)],
                "required_eps_m": float(eps_m), "slack_m": slack_value,
                "height_margin_after_eps_and_slack_m": float(-violation),
            }
            selected_drainage_edges.append(selected)
            if violation > drainage_worst[0]:
                drainage_worst = (violation, selected)
        summary["p3d31_drainage_selection"] = {
            "selected_edge_count": len(selected_drainage_edges),
            "non_outlet_vertex_count": len(drainage_nodes),
            "single_commodity_flow_capacity_per_edge": flow_capacity,
            "integrality_relaxed": bool(relax_integrality),
            "selected_edges": [] if relax_integrality else selected_drainage_edges,
        }

        curvature_hard_worst = (0.0, None)
        curvature_soft_abs_max = (0.0, None)
        curvature_soft_weighted_sum = 0.0
        for spec_index, spec in enumerate(curvature_specs):
            az, ax, iz, ix, bz, bx = spec["indices"]
            value = float(final_grid[az, ax] - 2.0 * final_grid[iz, ix]
                          + final_grid[bz, bx])
            ref_value = float(spec["reference_second_difference_m"])
            delta = abs(value - ref_value)
            if spec["soft_l1"]:
                curvature_soft_weighted_sum += float(spec["l1_weight"]) * delta
                if delta > curvature_soft_abs_max[0]:
                    curvature_soft_abs_max = (delta, {
                        "center_xz": [float(grid_x0 + ix / fs), float(grid_z0 + iz / fs)],
                        "second_difference_m": value,
                        "reference_second_difference_m": ref_value,
                    })
            else:
                violation = max(0.0, delta - float(spec["hard_tolerance_m"]))
                if violation > curvature_hard_worst[0]:
                    curvature_hard_worst = (violation, {
                        "center_xz": [float(grid_x0 + ix / fs), float(grid_z0 + iz / fs)],
                        "second_difference_m": value,
                        "reference_second_difference_m": ref_value,
                        "tolerance_m": float(spec["hard_tolerance_m"]),
                    })

        r4_worst = (0.0, None)
        for profile in profiles:
            coords = np.asarray(profile["coords"], dtype=np.float64)
            direction = np.gradient(coords, axis=0)
            direction /= np.maximum(np.linalg.norm(direction, axis=1, keepdims=True), 1e-9)
            normal = np.column_stack((-direction[:, 1], direction[:, 0]))
            for sample_index in range(0, len(coords), 16):
                center = coords[sample_index]
                cix = int(round((center[0] - grid_x0) * fs))
                ciz = int(round((center[1] - grid_z0) * fs))
                if not (0 <= cix < width and 0 <= ciz < height and active_mask[ciz, cix]):
                    continue
                center_height = field_value(float(center[0]), float(center[1]))
                side_deltas = []
                for side in (center + normal[sample_index] * 4.0,
                             center - normal[sample_index] * 4.0):
                    sx, sz = float(side[0]), float(side[1])
                    if not (0.0 <= sx <= nx and 0.0 <= sz <= ny):
                        continue
                    side_height = field_value(sx, sz)
                    side_deltas.append(float(side_height - center_height))
                if len(side_deltas) != 2:
                    continue
                indicator = min(side_deltas)
                violation = max(0.0, indicator - (1.5 - 1e-5))
                if violation > r4_worst[0]:
                    r4_worst = (violation, {
                        "center_xz": [float(center[0]), float(center[1])],
                        "side_minus_center_m": side_deltas,
                        "indicator_m": indicator,
                        "official_limit_m": 1.5,
                    })

        tree_worst = (0.0, None)
        tree_points_seen = set()
        for tree_index, tree_object in enumerate(data.get("baeume", [])):
            try:
                tx, tz = float(tree_object[0]), float(tree_object[2])
            except (TypeError, ValueError, IndexError):
                continue
            if not (grid_x0 <= tx <= grid_x1 and grid_z0 <= tz <= grid_z1):
                continue
            tix = int(round((tx - grid_x0) * fs))
            tiz = int(round((tz - grid_z0) * fs))
            if not (0 <= tix < width and 0 <= tiz < height and active_mask[tiz, tix]):
                continue
            for dz in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ix, iz = tix + dx, tiz + dz
                    if not (0 <= ix < width and 0 <= iz < height):
                        continue
                    px, pz = grid_x0 + ix / fs, grid_z0 + iz / fs
                    key = (tree_index, ix, iz)
                    if key in tree_points_seen:
                        continue
                    tree_points_seen.add(key)
                    delta = field_value(px, pz) - reference_sample(px, pz)
                    violation = max(0.0, abs(delta) - P3D29_TREE_GROUND_TOL_M)
                    if violation > tree_worst[0]:
                        tree_worst = (violation, {
                            "tree_index": int(tree_index), "tree_xz": [tx, tz],
                            "ground_sample_xz": [px, pz], "delta_m": float(delta),
                        })
        summary["p3d31_construction_max_violations"] = {
            "locality": locality_violations,
            "locality_row_debug": {
                f"{point[0]}|{point[1]}": {
                    **details,
                    "upper_activity": float(activity[details["upper_row"]]),
                    "lower_activity": float(activity[details["lower_row"]]),
                }
                for point, details in locality_row_debug.items()
            },
            "drainage": {"maximum_violation_m": float(max(0.0, drainage_worst[0])),
                         "edge": drainage_worst[1]},
            "cliff_curvature_hard": {"maximum_violation_m": float(curvature_hard_worst[0]),
                                      "stencil": curvature_hard_worst[1]},
            "cliff_curvature_l1": {"maximum_abs_deviation_m": float(curvature_soft_abs_max[0]),
                                   "largest_stencil": curvature_soft_abs_max[1],
                                   "weighted_l1_sum": float(curvature_soft_weighted_sum)},
            "r4_official_indicator": {"maximum_violation_m": float(r4_worst[0]),
                                      "section": r4_worst[1]},
            "tree_ground": {"maximum_violation_m": float(tree_worst[0]),
                            "sample": tree_worst[1],
                            "stencil_samples": int(len(tree_points_seen))},
        }

        def endpoint_pair_max(pairs_for_family, cap: float) -> dict:
            best = (0.0, None)
            for px0, pz0, px1, pz1 in pairs_for_family:
                delta = abs(field_value(px0, pz0) - field_value(px1, pz1))
                violation = max(0.0, delta - cap)
                if violation > best[0]:
                    best = (violation, {"a": [px0, pz0], "b": [px1, pz1],
                                        "delta_m": delta, "limit_m": cap})
            return {"maximum_violation_m": float(best[0]), "pair": best[1]}

        def endpoint_pair_specs_max(pair_specs) -> dict:
            best = (0.0, None)
            for pair, cap, endpoint_id, anchor in pair_specs:
                px0, pz0, px1, pz1 = pair
                delta = abs(field_value(px0, pz0) - field_value(px1, pz1))
                violation = max(0.0, delta - cap)
                if violation > best[0]:
                    best = (violation, {
                        "a": [px0, pz0], "b": [px1, pz1],
                        "delta_m": delta, "limit_m": cap,
                        "wegend_id": endpoint_id, "anchor_xz": anchor,
                        "ausnahme": r8a_exception_for_endpoint(endpoint_id, anchor),
                    })
            return {"maximum_violation_m": float(best[0]), "pair": best[1]}

        pair_grade_max = {"cross_route": (0.0, None), "same_route": (0.0, None)}
        for ra, ia, rb, ib, distance in pairs:
            va, vb = h_offsets[ra] + ia, h_offsets[rb] + ib
            violation = max(0.0, abs(float(xsol[va] - xsol[vb])) - grade * distance)
            key = "same_route" if ra == rb else "cross_route"
            if violation > pair_grade_max[key][0]:
                ca, cb = profiles[ra]["coords"][ia], profiles[rb]["coords"][ib]
                pair_grade_max[key] = (violation, {
                    "route_a": int(profiles[ra]["index"]), "station_a_m": float(profiles[ra]["station"][ia] * CELL_M),
                    "route_b": int(profiles[rb]["index"]), "station_b_m": float(profiles[rb]["station"][ib] * CELL_M),
                    "a_map": ca.tolist(), "b_map": cb.tolist(),
                    "height_delta_m": float(abs(xsol[va] - xsol[vb])),
                    "grade_limit_m": float(grade * distance), "pair_distance_m": float(distance),
                })
        endpoint_max = endpoint_pair_specs_max(endpoint_runout_pair_specs)
        if endpoint_max["pair"] is not None:
            midpoint = np.mean([endpoint_max["pair"]["a"], endpoint_max["pair"]["b"]], axis=0)
            endpoints = []
            for p in profiles:
                for label, k in (("start", 0), ("end", len(p["coords"]) - 1)):
                    coord = p["coords"][k]
                    endpoints.append((float(np.linalg.norm(coord - midpoint)), int(p["index"]), label, coord.tolist()))
            _, route_id, endpoint_label, endpoint_xy = min(endpoints)
            endpoint_max["nearest_route_endpoint"] = {
                "route": route_id, "endpoint": endpoint_label, "map": endpoint_xy,
            }
        summary["family_max_relaxation_locations"] = {
            "grade_cross": {"maximum_violation_m": pair_grade_max["cross_route"][0],
                            "pair": pair_grade_max["cross_route"][1]},
            "grade_same": {"maximum_violation_m": pair_grade_max["same_route"][0],
                            "pair": pair_grade_max["same_route"][1]},
            "endpoint_r8a": endpoint_max,
            "endpoint_stage": endpoint_pair_max(endpoint_stage_pairs, 0.054),
        }
        # Find the largest lower/upper-bound violation before applying its
        # family slack, with a map coordinate or route station for context.
        worst_bound = (0.0, None)
        for route, p in enumerate(profiles):
            start = h_offsets[route]
            for k, xy in enumerate(p["coords"]):
                j = start + k
                violation = max(float(base_lower[j] - xsol[j]) if np.isfinite(base_lower[j]) else 0.0,
                                float(xsol[j] - base_upper[j]) if np.isfinite(base_upper[j]) else 0.0,
                                0.0)
                if violation > worst_bound[0]:
                    worst_bound = (violation, {"kind": "route_height", "route": int(p["index"]),
                                               "station_m": float(p["station"][k] * CELL_M),
                                               "map": xy.tolist(), "height_m": float(xsol[j]),
                                               "lower_m": float(base_lower[j]), "upper_m": float(base_upper[j])})
        summary["family_max_relaxation_locations"]["variable_bounds"] = {
            "maximum_violation_m": worst_bound[0], "variable": worst_bound[1],
        }
        poly = [float(xsol[plane_gx] * np.cos(a) + xsol[plane_gz] * np.sin(a))
                for a in np.arange(32) * (2.0 * np.pi / 32.0)]
        summary["family_max_relaxation_locations"]["plane_slope_polygon"] = {
            "maximum_violation_pp": max(0.0, (max(poly) - PLANE_SLOPE_MAX * np.cos(np.pi / 32.0)) * 100.0),
            "map": R8_GATE_CENTER.tolist(),
        }
        summary["family_max_relaxation_locations"]["plane_slope_box"] = {
            "maximum_violation_pp": max(0.0, (max(abs(xsol[plane_gx]), abs(xsol[plane_gz])) - PLANE_SLOPE_MAX) * 100.0),
            "map": R8_GATE_CENTER.tolist(),
        }
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
