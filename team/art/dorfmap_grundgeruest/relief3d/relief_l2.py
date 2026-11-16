"""Gezielte, weltkoordinatenbasierte L2-Korrekturen des sichtbaren Hoehenfelds."""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from scipy import ndimage as nd


STELLEN = Path(__file__).with_name("pruefung") / "l2_stellen.json"


def _vertices(a: np.ndarray, rs: int, shape: tuple[int, int]) -> np.ndarray:
    """Zellmaske auf die 0,5-m-Vertexmaske abbilden; Rand folgt der letzten Zelle."""
    a = np.asarray(a, dtype=bool)
    b = np.repeat(np.repeat(a, rs, axis=0), rs, axis=1)
    return np.pad(b, ((0, 1), (0, 1)), mode="edge")[: shape[0], : shape[1]]


def _smoothstep(a: np.ndarray, edge0: float, edge1: float) -> np.ndarray:
    t = np.clip((a - edge0) / max(edge1 - edge0, 1e-9), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _line_mask(shape: tuple[int, int], rs: int, paths: list, ways: list) -> np.ndarray:
    out = np.zeros(shape, dtype=bool)
    for z, x in ways:
        y0, x0 = int(z) * rs, int(x) * rs
        out[y0 : min(y0 + rs + 1, shape[0]), x0 : min(x0 + rs + 1, shape[1])] = True
    for path in paths:
        p = np.asarray(path, dtype=float)
        if len(p) < 2:
            continue
        length = np.r_[0.0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
        t = np.arange(0.0, length[-1] + 1e-9, 0.25)
        x = np.interp(t, length, p[:, 0])
        z = np.interp(t, length, p[:, 1])
        ix = np.clip(np.rint(x * rs).astype(int), 0, shape[1] - 1)
        iz = np.clip(np.rint(z * rs).astype(int), 0, shape[0] - 1)
        out[iz, ix] = True
    return out


def _protection(meta: dict, shape: tuple[int, int], lock_render_band: bool) -> tuple[np.ndarray, np.ndarray]:
    nx, ny, rs = int(meta["nx"]), int(meta["ny"]), int(meta["rs"])
    band = _vertices(meta["band"], rs, shape)
    wall = _vertices(meta["wall"], rs, shape)
    names = _vertices(np.asarray(meta["wall_names"]) != "", rs, shape)
    contour = _vertices(np.asarray(meta["klippe"]) != "", rs, shape)
    built = _vertices(meta["built"], rs, shape)

    water = _vertices(meta["water_cells"], rs, shape)
    water |= np.asarray(meta["water_vertices"], dtype=bool)
    water_distance = nd.distance_transform_edt(~water, sampling=1.0 / rs)
    water_keep = water_distance <= 2.0

    road = _vertices(meta["road_cells"], rs, shape)
    road |= np.asarray(meta["road_vertices"], dtype=bool)
    road |= _line_mask(shape, rs, meta["ramps"], meta["ways"])
    road_distance = nd.distance_transform_edt(~road, sampling=1.0 / rs)
    road_keep = road_distance <= 2.5

    # Kachel D2 bleibt vollstaendig bytegleich; ein 3-m-Fade liegt ausserhalb.
    d2 = np.zeros(shape, dtype=bool)
    x0, x1 = 126 * rs, 168 * rs
    z0, z1 = 43 * rs, 86 * rs
    d2[z0 : z1 + 1, x0 : x1 + 1] = True
    d2_distance = nd.distance_transform_edt(~d2, sampling=1.0 / rs)
    d2_weight = _smoothstep(d2_distance, 0.0, 3.0)

    fixed = wall | names | contour | built | water_keep | road_keep | d2
    if lock_render_band:
        fixed |= band
    clearance = nd.distance_transform_edt(~fixed, sampling=1.0 / rs)
    # C1-Auslauf von mindestens 3 Vertices (1,5 m) an jedem festen Band.
    safe_weight = _smoothstep(clearance, 0.0, 1.5) * d2_weight
    return fixed, safe_weight


def _region_weight(shape: tuple[int, int], rs: int, point: dict) -> np.ndarray:
    x = np.arange(shape[1], dtype=float)[None, :] / rs
    z = np.arange(shape[0], dtype=float)[:, None] / rs
    rx, rz = float(point["rx_m"]), float(point["rz_m"])
    norm = np.sqrt(((x - float(point["x_m"])) / rx) ** 2 + ((z - float(point["z_m"])) / rz) ** 2)
    physical = np.minimum(rx, rz) * np.maximum(norm - 1.0, 0.0)
    # Flat core plus smooth 3-m falloff into the untouched neighbourhood.
    return 1.0 - _smoothstep(physical, 0.0, float(point.get("fade_m", 3.0)))


def _apply_one(field: np.ndarray, regions: list[dict], safe: np.ndarray, rs: int) -> tuple[np.ndarray, dict[str, float]]:
    source = np.asarray(field)
    original = source.astype(np.float64, copy=True).reshape(safe.shape)
    total = np.zeros_like(original)
    kernels: dict[tuple, np.ndarray] = {}
    maxima: dict[str, float] = {}
    for region in regions:
        method = region.get("method", "median")
        if method == "line" and _VARIANTE in (2, 3):
            angle = round(float(region["richtung_grad"]), 3)
            key = ("line", angle)
            if key not in kernels:
                kernels[key] = _line_filter(original, np.radians(angle), rs)
        else:
            kernel = int(region.get("median_kernel", 5))
            key = ("median", kernel)
            if key not in kernels:
                kernels[key] = nd.median_filter(original, size=kernel, mode="nearest")
        difference = np.clip(
            kernels[key] - original,
            -float(region["max_correction_m"]),
            float(region["max_correction_m"]),
        )
        weight = np.zeros_like(safe)
        for point in region["masken"]:
            weight = np.maximum(weight, _region_weight(safe.shape, rs, point))
        weight *= safe
        contribution = difference * weight
        total += contribution
        region_mask = weight > 1e-6
        maxima[region["id"]] = float(np.max(np.abs(contribution[region_mask]))) if region_mask.any() else 0.0
    result = (original + total).astype(source.dtype, copy=False)
    return result.reshape(source.shape), maxima


def _line_filter(field: np.ndarray, angle: float, rs: int) -> np.ndarray:
    """Symmetrische 1D-Mittelung entlang der Gratachse, ohne Querprofil zu glaetten."""
    h, w = field.shape
    y, x = np.mgrid[0:h, 0:w].astype(np.float64)
    dx, dy = np.cos(angle), np.sin(angle)
    out = 0.25 * field
    for offset, weight in ((0.5, 0.20), (1.0, 0.125), (1.5, 0.05)):
        sx, sy = offset * rs * dx, offset * rs * dy
        out += weight * nd.map_coordinates(field, [y + sy, x + sx], order=1, mode="nearest")
        out += weight * nd.map_coordinates(field, [y - sy, x - sx], order=1, mode="nearest")
    return out


def apply_pair(g: np.ndarray, gb: np.ndarray, meta: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    """Apply one local variant to visible GB; keep source field G byte-identical."""
    shape = (int(meta["ny"]) * int(meta["rs"]) + 1, int(meta["nx"]) * int(meta["rs"]) + 1)
    global _VARIANTE
    _VARIANTE = int(os.environ.get("RELIEF_L2_VAR", "2"))
    if _VARIANTE not in (1, 2, 3):
        raise ValueError("RELIEF_L2_VAR muss 1 (Median), 2 (1D-Grat mit Renderband-Sperre) oder 3 (1D-Grat mit expliziten Wand-/Klippen-Sperren) sein")
    settings = json.loads(STELLEN.read_text(encoding="utf-8"))
    fixed, safe = _protection(meta, shape, lock_render_band=_VARIANTE != 3)
    gb_after, gb_max = _apply_one(gb, settings["stellen"], safe, int(meta["rs"]))
    rows = []
    for row in settings["stellen"]:
        key = row["id"]
        rows.append({
            "id": key,
            "muster": row["muster"],
            "max_g_m": 0.0,
            "max_gb_m": round(gb_max[key], 4),
            "beruehrbare_flaeche_vertices": int(((
                np.maximum.reduce([_region_weight(shape, int(meta["rs"]), p) for p in row["masken"]]) * safe
            ) > 1e-3).sum()),
        })
    report = {
        "aktiv": True,
        "variante": _VARIANTE,
        "verfahren": "Medianfilter lokal" if _VARIANTE == 1 else "1D-Mittelung entlang Gratachse lokal",
        "band_sperre": _VARIANTE != 3,
        "auslauf_m": 3.0,
        "fixierte_vertices": int(fixed.sum()),
        "gewaehlte_stellen": rows,
        "max_abs_g_m": 0.0,
        "max_abs_gb_m": round(float(np.max(np.abs(gb_after.astype(float) - np.asarray(gb).reshape(shape).astype(float)))), 4),
    }
    return g, gb_after, report
