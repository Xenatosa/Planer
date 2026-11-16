"""L1: one deterministic, edge-masked finish pass over the full display field."""
from __future__ import annotations

import base64
import math

import numpy as np
import scipy.ndimage as nd


# The default is selected only after the full unchanged gate has been compared.
DEFAULT_VARIANT = 2

_VARIANTS = {
    # sigma in metres, blend fraction, maximum per-pass displacement in metres
    1: (0.75, 0.75, 0.35),
    2: (1.00, 0.80, 0.50),
    3: (2.00, 0.90, 0.90),
}


def _route_mask(shape, rs, wega, wege, rampenwege):
    road = np.asarray(wega).reshape(shape) > 20
    for x, z in wege:
        ix, iz = int(x * rs), int(z * rs)
        road[max(0, iz):min(shape[0], iz + rs + 1),
             max(0, ix):min(shape[1], ix + rs + 1)] = True
    for route in rampenwege:
        points = np.asarray(route, dtype=float)
        if len(points) == 0:
            continue
        lengths = np.r_[0.0, np.cumsum(np.hypot(*np.diff(points, axis=0).T))]
        samples = np.arange(0.0, lengths[-1] + 1e-6, 0.25)
        xs = np.clip(np.rint(np.interp(samples, lengths, points[:, 0]) * rs).astype(int), 0, shape[1] - 1)
        zs = np.clip(np.rint(np.interp(samples, lengths, points[:, 1]) * rs).astype(int), 0, shape[0] - 1)
        road[zs, xs] = True
    return road


def apply_global_finish(gb, fw, water, wega, wege, rampenwege, band, nx, ny, rs, fs, variant):
    """Smooth visible terrain globally while holding protected geometry fixed.

    Variant 0 returns the original objects without decoding or re-encoding data.
    Nonzero variants apply one low-pass correction to GB and transfer the same
    correction to the sparse fine mesh, leaving source G and all overlays alone.
    """
    variant = int(variant)
    if variant not in (0, 1, 2, 3):
        raise ValueError("RELIEF_L1_VAR muss 0, 1, 2 oder 3 sein")
    if variant == 0:
        return gb, fw, {"variante": 0, "geaendert_grob": 0, "geaendert_fein": 0}

    sigma_m, blend, max_delta_m = _VARIANTS[variant]
    original = np.asarray(gb)
    grid = original.reshape(np.shape(water)).astype(np.float64)
    height, width = grid.shape
    land = np.asarray(water).reshape(grid.shape) <= -900

    # Hold cliff bands and their immediate contour neighborhood.
    gy, gx = np.gradient(grid, 1.0 / rs)
    steep = np.hypot(gx, gy) > 1.0
    protected = nd.binary_dilation(steep, iterations=math.ceil(1.5 * rs))
    if band is not None:
        source_band = np.asarray(band, dtype=bool)
        by = np.minimum((np.arange(height) / rs).astype(int), source_band.shape[0] - 1)
        bx = np.minimum((np.arange(width) / rs).astype(int), source_band.shape[1] - 1)
        protected |= source_band[by[:, None], bx[None, :]]
        protected = nd.binary_dilation(protected, iterations=math.ceil(1.0 * rs))

    # Preserve water, road profiles and intersections with a feathered margin.
    water_or_bank = nd.binary_dilation(~land, iterations=math.ceil(2.0 * rs))
    road = _route_mask(grid.shape, rs, wega, wege, rampenwege)
    road_or_margin = nd.binary_dilation(road, iterations=math.ceil(3.5 * rs))

    # Internal and outer tile borders remain exact source anchors.
    x_m = np.arange(width, dtype=np.float64) / rs
    z_m = np.arange(height, dtype=np.float64) / rs
    x_phase = np.mod(x_m, 42.0)
    z_phase = np.mod(z_m, 43.0)
    x_border_dist = np.minimum(x_phase, 42.0 - x_phase)
    z_border_dist = np.minimum(z_phase, 43.0 - z_phase)
    tile_interior = (
        (x_border_dist[None, :] > 1.0)
        & (z_border_dist[:, None] > 1.0)
        & (x_m[None, :] > 1.0)
        & (x_m[None, :] < nx - 1.0)
        & (z_m[:, None] > 1.0)
        & (z_m[:, None] < ny - 1.0)
    )

    allowed = land & tile_interior & ~protected & ~water_or_bank & ~road_or_margin
    # D2 is a fixed regression tile, including every shared boundary sample.
    d2 = np.zeros(grid.shape, dtype=bool)
    d2[43 * rs:min(height, 86 * rs + 1), 126 * rs:min(width, 168 * rs + 1)] = True
    allowed &= ~d2

    # Fade the correction in from every fixed band to avoid a new sharp seam.
    fade = np.clip(nd.distance_transform_edt(allowed) / (2.0 * rs), 0.0, 1.0)
    fade = fade * fade * (3.0 - 2.0 * fade)
    smoothed = nd.gaussian_filter(grid, sigma_m * rs, mode="nearest")
    delta = np.clip(smoothed - grid, -max_delta_m, max_delta_m) * blend * fade
    delta[~allowed] = 0.0

    updated = (grid + delta).astype(original.dtype).reshape(original.shape)
    changed = int(np.count_nonzero(updated != original))

    # Apply the same continuous correction to the sparse fine terrain mesh.
    fw_out = dict(fw)
    vertices = np.frombuffer(base64.b64decode(fw["vid"]), dtype=np.uint32)
    fy, fx = vertices // (nx * fs + 1), vertices % (nx * fs + 1)
    h = np.frombuffer(base64.b64decode(fw["h"]), dtype=np.float32).copy()
    sample_y, sample_x = fy / fs * rs, fx / fs * rs
    fine_delta = nd.map_coordinates(delta, [sample_y, sample_x], order=1, mode="nearest")
    fine_allowed = nd.map_coordinates(allowed.astype(np.uint8), [sample_y, sample_x], order=0, mode="nearest") > 0
    fine_delta[~fine_allowed] = 0.0
    fine_x, fine_z = fx / fs, fy / fs
    fine_d2 = (fine_x >= 126) & (fine_x <= 168) & (fine_z >= 43) & (fine_z <= 86)
    fine_delta[fine_d2] = 0.0
    h_after = (h.astype(np.float64) + fine_delta).astype(np.float32)
    fw_out["h"] = base64.b64encode(h_after.tobytes()).decode("ascii")

    return updated, fw_out, {
        "variante": variant,
        "sigma_m": sigma_m,
        "blend": blend,
        "max_delta_m": max_delta_m,
        "geaendert_grob": changed,
        "geaendert_fein": int(np.count_nonzero(h_after != h)),
        "sperrmaske_punkte": int((~allowed).sum()),
        "max_aenderung_m": round(float(np.max(np.abs(delta))), 6),
        "rms_aenderung_m": round(float(np.sqrt(np.mean(delta * delta))), 6),
    }
