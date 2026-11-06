"""Deterministic, profile-driven wall solids for the opt-in tile viewer."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from .mesh import TILE_BOUNDS


DEFAULT_VARIANT = 1
VARIANTS = {0: "breit_2m4", 1: "profil_minimal"}


def _clip(a: np.ndarray, b: np.ndarray, bounds: tuple[float, float, float, float]):
    """Liang-Barsky clipping with profile interpolation parameters."""
    x0, z0, x1, z1 = bounds
    dx, dz = b[0] - a[0], b[1] - a[1]
    lo, hi = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dz, a[1] - z0), (dz, z1 - a[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            if r > hi:
                return None
            lo = max(lo, r)
        else:
            if r < lo:
                return None
            hi = min(hi, r)
    if hi - lo < 1e-9:
        return None
    return lo, hi


def _chunks(wall: dict[str, Any], bounds: tuple[int, int, int, int], width: float):
    points = np.asarray(wall["mittellinie_m"], dtype=np.float64)
    top = np.asarray(wall["hoehe_oben_m"], dtype=np.float64)
    bottom = np.asarray(wall["hoehe_unten_m"], dtype=np.float64)
    if len(points) != len(top) or len(points) != len(bottom):
        raise ValueError(f"Profil-Laenge stimmt nicht bei Wand {wall.get('name')}:{wall.get('teil')}")
    # Keep the complete minimum-width solid inside its prototype tile.
    margin = width * 1.05
    x0, z0, x1, z1 = bounds
    clipbox = (x0 + margin, z0 + margin, x1 - margin, z1 - margin)
    result: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
    run_p: list[np.ndarray] = []
    run_t: list[float] = []
    run_b: list[float] = []

    def flush() -> None:
        nonlocal run_p, run_t, run_b
        if len(run_p) >= 2:
            result.append((np.asarray(run_p), np.asarray(run_t), np.asarray(run_b)))
        run_p, run_t, run_b = [], [], []

    for i in range(len(points) - 1):
        clipped = _clip(points[i], points[i + 1], clipbox)
        if clipped is None:
            flush()
            continue
        t0, t1 = clipped
        p0 = points[i] + (points[i + 1] - points[i]) * t0
        p1 = points[i] + (points[i + 1] - points[i]) * t1
        top0, top1 = top[i] + (top[i + 1] - top[i]) * t0, top[i] + (top[i + 1] - top[i]) * t1
        bot0, bot1 = bottom[i] + (bottom[i + 1] - bottom[i]) * t0, bottom[i] + (bottom[i + 1] - bottom[i]) * t1
        if not run_p or np.linalg.norm(run_p[-1] - p0) > 1e-6:
            flush()
            run_p, run_t, run_b = [p0], [top0], [bot0]
        if np.linalg.norm(run_p[-1] - p1) > 1e-8:
            run_p.append(p1)
            run_t.append(top1)
            run_b.append(bot1)
        if t1 < 1.0 - 1e-8:
            flush()
    flush()
    return result


def _offsets(points: np.ndarray, width: float, variant: int) -> np.ndarray:
    half = width * 0.5
    edges = np.diff(points, axis=0)
    lengths = np.linalg.norm(edges, axis=1)
    tangents = edges / np.maximum(lengths[:, None], 1e-12)
    normals = np.column_stack((-tangents[:, 1], tangents[:, 0]))
    out = np.empty_like(points)
    out[0] = normals[0] * half
    out[-1] = normals[-1] * half
    for i in range(1, len(points) - 1):
        n = normals[i - 1] + normals[i]
        ln = np.linalg.norm(n)
        if ln < 1e-8:
            out[i] = normals[i] * half
            continue
        miter = n / ln
        denom = abs(float(miter @ normals[i]))
        scale = half / max(denom, 0.5)
        if variant == 0:
            # Keep the same minimum strip width while making bends wider and
            # easier to read in the close-up renders.
            scale = max(half, min(scale, width))
        else:
            scale = min(scale, width)
        out[i] = miter * scale
    return out


def _solid(points: np.ndarray, top: np.ndarray, bottom: np.ndarray, width: float, variant: int):
    offsets = _offsets(points, width, variant)
    left = points + offsets
    right = points - offsets
    positions: list[tuple[float, float, float]] = []
    indices: list[int] = []

    def quad(a, b, c, d):
        base = len(positions)
        positions.extend((a, b, c, d))
        indices.extend((base, base + 1, base + 2, base, base + 2, base + 3))

    for i in range(len(points) - 1):
        lb0, lt0 = (left[i, 0], bottom[i], left[i, 1]), (left[i, 0], top[i], left[i, 1])
        rb0, rt0 = (right[i, 0], bottom[i], right[i, 1]), (right[i, 0], top[i], right[i, 1])
        lb1, lt1 = (left[i + 1, 0], bottom[i + 1], left[i + 1, 1]), (left[i + 1, 0], top[i + 1], left[i + 1, 1])
        rb1, rt1 = (right[i + 1, 0], bottom[i + 1], right[i + 1, 1]), (right[i + 1, 0], top[i + 1], right[i + 1, 1])
        # The duplicated face vertices leave the crown, foot and side facets
        # hard-edged in the renderer; there is no height-field smoothing here.
        quad(lb0, lt0, lt1, lb1)
        quad(rb1, rt1, rt0, rb0)
        quad(lt0, rt0, rt1, lt1)
        quad(rb0, lb0, lb1, rb1)
    quad((left[0, 0], bottom[0], left[0, 1]), (right[0, 0], bottom[0], right[0, 1]),
         (right[0, 0], top[0], right[0, 1]), (left[0, 0], top[0], left[0, 1]))
    k = len(points) - 1
    quad((right[k, 0], bottom[k], right[k, 1]), (left[k, 0], bottom[k], left[k, 1]),
         (left[k, 0], top[k], left[k, 1]), (right[k, 0], top[k], right[k, 1]))
    return np.asarray(positions, dtype="<f4"), np.asarray(indices, dtype="<u4")


def _b64(array: np.ndarray) -> str:
    return base64.b64encode(array.tobytes(order="C")).decode("ascii")


def build_wall_manifest(vector_path: Path, variant: int | None = None) -> dict[str, Any]:
    """Build wall solids from the generated ``neu/vektor.json`` profiles."""
    if variant is None:
        import os
        variant = int(os.environ.get("WANDVAR", str(DEFAULT_VARIANT)))
    if variant not in VARIANTS:
        raise ValueError(f"WANDVAR muss eine der Varianten {sorted(VARIANTS)} sein")
    vector = json.loads(vector_path.read_text(encoding="utf-8"))
    tile_data: dict[str, Any] = {}
    for tile in ("D1", "G1", "D2"):
        bounds = TILE_BOUNDS[tile]
        pieces: list[tuple[np.ndarray, np.ndarray]] = []
        features = 0
        used_widths: list[float] = []
        for wall in vector.get("waende", []):
            nominal = float(wall.get("breite_min_m", 0.0))
            if nominal <= 0:
                raise ValueError(f"Wand ohne positive Mindestbreite: {wall.get('name')}:{wall.get('teil')}")
            width = max(nominal, 2.4 if variant == 0 else nominal)
            for points, top, bottom in _chunks(wall, bounds, width):
                positions, indices = _solid(points, np.maximum(top, bottom), np.minimum(top, bottom), width, variant)
                if len(indices):
                    pieces.append((positions, indices))
                    features += 1
                    used_widths.append(width)
        if tile == "D2":
            pieces, features, used_widths = [], 0, []
        if pieces:
            positions = np.concatenate([p for p, _ in pieces]).astype("<f4", copy=False)
            indices_parts, offset = [], 0
            for p, ix in pieces:
                indices_parts.append(ix + offset)
                offset += len(p)
            indices = np.concatenate(indices_parts).astype("<u4", copy=False)
        else:
            positions = np.empty((0, 3), dtype="<f4")
            indices = np.empty((0,), dtype="<u4")
        tile_data[tile] = {
            "vertices_xyz_f32": _b64(positions.reshape(-1)), "indices_u32": _b64(indices),
            "vertices": int(len(positions)), "triangles": int(len(indices) // 3),
            "features": int(features), "min_width_m": min(used_widths) if used_widths else None,
            "max_width_m": max(used_widths) if used_widths else None,
            "mesh_sha256": hashlib.sha256(positions.tobytes() + indices.tobytes()).hexdigest(),
        }
    return {"format": "relief-neu-wall-mesh-v1", "variant": variant,
            "variant_name": VARIANTS[variant], "source_vector_sha256": hashlib.sha256(vector_path.read_bytes()).hexdigest(),
            "tiles": tile_data}
