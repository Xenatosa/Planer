#!/usr/bin/env python3
"""Capture p3d14's D1 crossing transfer terms and resample at 0.25 map units."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[3]
RELIEF = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
if str(RELIEF) not in sys.path:
    sys.path.insert(0, str(RELIEF))

from neu import mesh


def bilinear(field: np.ndarray, x: float, z: float, x0: float, z0: float, step: float) -> float:
    u = (x - x0) / step
    v = (z - z0) / step
    ix, iz = int(np.floor(u)), int(np.floor(v))
    fu, fv = u - ix, v - iz
    ix = min(max(ix, 0), field.shape[1] - 2)
    iz = min(max(iz, 0), field.shape[0] - 2)
    return float(
        field[iz, ix] * (1.0 - fu) * (1.0 - fv)
        + field[iz, ix + 1] * fu * (1.0 - fv)
        + field[iz + 1, ix] * (1.0 - fu) * fv
        + field[iz + 1, ix + 1] * fu * fv
    )


def capture(
    result: np.ndarray, background: np.ndarray, x: np.ndarray, z: np.ndarray,
    profiles: list[dict], solved: list[np.ndarray], info: dict,
    crossing_m: np.ndarray, settings: dict,
) -> dict[str, np.ndarray]:
    """Mirror the production spatial transfer, retaining its weighted terms."""
    query = np.column_stack((x.ravel() * mesh.CELL_M, z.ravel() * mesh.CELL_M))
    selector_sum = np.zeros(len(query), dtype=np.float64)
    target_sum = np.zeros(len(query), dtype=np.float64)
    uncovered = np.ones(len(query), dtype=np.float64)
    selector_sigma = float(settings["selection_sigma_m"])
    midpoints = np.asarray(info.get("same_route_pair_midpoints_m", []), dtype=np.float64).reshape(-1, 2)
    sigma_by_query = np.full(len(query), selector_sigma, dtype=np.float64)
    if len(midpoints):
        midpoints = midpoints[np.linalg.norm(midpoints - crossing_m[None, :], axis=1) <= 7.0]
    if len(midpoints):
        dmid, _ = cKDTree(midpoints).query(query, k=1, workers=1)
        support = 1.0 - mesh._smoothstep(4.5, 7.0, dmid)
        radius = np.linalg.norm(query - crossing_m[None, :], axis=1)
        support = np.maximum(support, 1.0 - mesh._smoothstep(2.0, 6.0, radius))
        axis_distance = np.full(len(query), np.inf, dtype=np.float64)
        for profile in profiles:
            coords_m = np.asarray(profile["coords"], dtype=np.float64) * mesh.CELL_M
            distance, _ = cKDTree(coords_m).query(query, k=1, workers=1)
            axis_distance = np.minimum(axis_distance, distance)
        off_axis = mesh._smoothstep(0.3, 1.2, axis_distance)
        sigma_by_query += (max(selector_sigma, 1.5) - selector_sigma) * support * off_axis

    band = float(settings["band_m"])
    fade = float(settings["fade_m"])
    softmin_m = 0.02
    route_covers = []
    for profile, height in zip(profiles, solved):
        coords_m = np.asarray(profile["coords"], dtype=np.float64) * mesh.CELL_M
        start_tangent = coords_m[1] - coords_m[0]
        start_tangent /= max(float(np.hypot(*start_tangent)), 1e-12)
        end_tangent = coords_m[-1] - coords_m[-2]
        end_tangent /= max(float(np.hypot(*end_tangent)), 1e-12)
        valid = ~(((query - coords_m[0]) @ start_tangent) < -1e-8)
        valid &= ~(((query - coords_m[-1]) @ end_tangent) > 1e-8)
        min_distance = np.full(len(query), np.inf, dtype=np.float64)
        softmin_sum = np.zeros(len(query), dtype=np.float64)
        for segment in range(len(coords_m) - 1):
            vector = coords_m[segment + 1] - coords_m[segment]
            norm2 = max(float(vector @ vector), 1e-15)
            t = np.clip(((query - coords_m[segment]) @ vector) / norm2, 0.0, 1.0)
            projected = coords_m[segment] + t[:, None] * vector
            distance = np.sqrt(np.einsum("ij,ij->i", query - projected, query - projected))
            next_minimum = np.minimum(min_distance, distance)
            softmin_sum *= np.exp(-(min_distance - next_minimum) / softmin_m)
            softmin_sum += np.exp(-(distance - next_minimum) / softmin_m)
            min_distance = next_minimum
            route_weight = (1.0 - mesh._smoothstep(band, band + fade, distance)) * valid
            selector = route_weight * np.exp(-0.5 * (distance / sigma_by_query) ** 2)
            segment_target = height[segment] * (1.0 - t) + height[segment + 1] * t
            selector_sum += selector
            target_sum += selector * segment_target
        soft_distance = min_distance - softmin_m * np.log(np.maximum(softmin_sum, 1e-300))
        cover = (1.0 - mesh._smoothstep(band, band + fade, soft_distance)) * valid
        route_covers.append(cover)

    profile_cover = 1.0 - np.prod(1.0 - np.asarray(route_covers), axis=0)
    profile_target = np.divide(target_sum, selector_sum, out=np.zeros_like(target_sum), where=selector_sum > 0.0)
    radius = np.hypot(query[:, 0] - crossing_m[0], query[:, 1] - crossing_m[1])
    plane_mix = 1.0 - mesh._smoothstep(float(settings["plane_inner_m"]), float(settings["plane_outer_m"]), radius)
    plane_target = float(info["crossing_plane_height_m"])
    plane_target += float(info["crossing_plane_gradient_x"]) * (query[:, 0] - crossing_m[0])
    plane_target += float(info["crossing_plane_gradient_z"]) * (query[:, 1] - crossing_m[1])
    background_weight = (1.0 - profile_cover) * (1.0 - plane_mix)
    band_weight = profile_cover * (1.0 - plane_mix)
    plane_weight = plane_mix
    background_term = background.ravel() * background_weight
    band_term = profile_target * band_weight
    plane_term = plane_target * plane_weight
    reconstructed = background_term + band_term + plane_term
    return {
        "background": background.ravel(), "profile_target": profile_target,
        "plane_target": plane_target, "profile_cover": profile_cover,
        "plane_mix": plane_mix, "background_weight": background_weight,
        "band_weight": band_weight, "plane_weight": plane_weight,
        "background_term": background_term, "band_term": band_term,
        "plane_term": plane_term, "reconstructed": reconstructed,
        "result": result.ravel().copy(),
    }


def main() -> None:
    source = mesh.load_relief(RELIEF / "relief_daten.json.gz")
    vector = json.loads((RELIEF / "neu/vektor.json").read_text(encoding="utf-8"))
    with np.load(RELIEF / "neu/felder.npz", allow_pickle=False) as archive:
        fields = {name: archive[name] for name in archive.files}
    output: dict[str, dict[str, np.ndarray]] = {}
    original = mesh._apply_d1_spatial_transfer

    def wrapped(result, background, x, z, profiles, solved, info, crossing_m, old_weight, settings):
        captured = capture(result, background, x, z, profiles, solved, info, crossing_m, settings)
        value = original(result, background, x, z, profiles, solved, info, crossing_m, old_weight, settings)
        captured["result"] = result.ravel().copy()
        output["terms"] = {key: val.reshape(result.shape) for key, val in captured.items()}
        output["solver"] = {
            key: info[key] for key in (
                "crossing_plane_height_m", "crossing_plane_gradient_x", "crossing_plane_gradient_z",
                "crossing_plane_slope_pct", "crossing_plane_max_deviation_m",
                "same_route_pair_midpoints_m", "r3_sections_D1", "r3_sections_total",
            ) if key in info
        }
        output["solver"]["same_route_pair_midpoints_m"] = len(info.get("same_route_pair_midpoints_m", []))
        return value

    mesh._apply_d1_spatial_transfer = wrapped
    try:
        heights, build_info = mesh.terrain_heights(source, "D1", vector, fields, "2")
    finally:
        mesh._apply_d1_spatial_transfer = original

    term = output["terms"]
    x0, z0, _, _ = mesh.TILE_BOUNDS["D1"]
    step = 1.0 / int(source.data["rs"])
    # The gate's profile station spacing is 0.25 map units. Rasterize all
    # requested points directly from each mesh term using the same bilinear
    # interpolation used by the gate over the 0.5-unit source mesh.
    rows = []
    xs = np.round(np.arange(149.0, 154.0 + 1e-9, 0.25), 8)
    zs = np.round(np.arange(29.0, 34.0 + 1e-9, 0.25), 8)
    keys = (
        "background", "profile_target", "plane_target", "profile_cover", "plane_mix",
        "background_weight", "band_weight", "plane_weight", "background_term",
        "band_term", "plane_term", "reconstructed", "result",
    )
    sampled = {}
    for key in keys:
        grid = term[key]
        sampled[key] = np.asarray([
            [bilinear(grid, x, z, x0, z0, step) for x in xs] for z in zs
        ], dtype=np.float64)
    out_csv = Path(__file__).resolve().parent / "transfer_raster_p3d15.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["x", "z", *keys, "reconstruction_minus_mesh_m"])
        for zi, z in enumerate(zs):
            for xi, x in enumerate(xs):
                values = [sampled[key][zi, xi] for key in keys]
                rows.append((float(x), float(z), *values))
                writer.writerow([
                    f"{x:.2f}", f"{z:.2f}", *(f"{v:.9f}" for v in values),
                    f"{sampled['reconstructed'][zi, xi] - sampled['result'][zi, xi]:.12f}",
                ])

    # Focus comparison from the p3d14 report, with componentwise contribution
    # differences proving which terms cause the observed jump.
    focus = []
    for x, z in ((152.25, 31.75), (152.25, 32.0)):
        ix, iz = int(round((x - 149.0) / 0.25)), int(round((z - 29.0) / 0.25))
        focus.append({"x": x, "z": z, **{key: float(sampled[key][iz, ix]) for key in keys}})
    differences = {
        key: round(focus[1][key] - focus[0][key], 9)
        for key in ("background_term", "band_term", "plane_term", "result")
    }
    report = {
        "source": "p3d14 production transfer variant 17, sampled from its 0.5-map-unit mesh at 0.25-map-unit intervals",
        "physical_step_m": round(0.25 * mesh.CELL_M, 6),
        "grid": {"x_min": float(xs.min()), "x_max": float(xs.max()), "z_min": float(zs.min()), "z_max": float(zs.max()), "points": len(xs) * len(zs)},
        "production_build_info": build_info,
        "solver": output["solver"],
        "max_abs_component_reconstruction_error_m": float(np.max(np.abs(term["reconstructed"] - term["result"]))),
        "focus": focus,
        "component_delta_second_minus_first_m": differences,
        "csv": out_csv.name,
    }
    out_json = Path(__file__).resolve().parent / "transfer_raster_p3d15.json"
    out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
