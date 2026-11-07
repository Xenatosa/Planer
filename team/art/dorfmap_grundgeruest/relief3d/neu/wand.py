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
FOOT_VARIANTS = {
    0: "profil_unveraendert",
    1: "terrain_gebundener_fuss_0_15m",
    2: "terrain_gebundener_fuss_0_05m",
}


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


def _chaikin(
    points: np.ndarray, top: np.ndarray, bottom: np.ndarray, iterations: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Round raster-like bends while keeping endpoints and height profiles fixed."""
    for _ in range(iterations):
        if len(points) < 3:
            break
        q = points[:-1] * 0.75 + points[1:] * 0.25
        r = points[:-1] * 0.25 + points[1:] * 0.75
        qt = top[:-1] * 0.75 + top[1:] * 0.25
        rt = top[:-1] * 0.25 + top[1:] * 0.75
        qb = bottom[:-1] * 0.75 + bottom[1:] * 0.25
        rb = bottom[:-1] * 0.25 + bottom[1:] * 0.75
        points = np.vstack((points[0], np.column_stack((q, r)).reshape(-1, 2), points[-1]))
        top = np.r_[top[0], np.column_stack((qt, rt)).ravel(), top[-1]]
        bottom = np.r_[bottom[0], np.column_stack((qb, rb)).ravel(), bottom[-1]]
    return points, top, bottom


def _chunks(wall: dict[str, Any], bounds: tuple[int, int, int, int], width: float, variant: int):
    points = np.asarray(wall["mittellinie_m"], dtype=np.float64)
    top = np.asarray(wall["hoehe_oben_m"], dtype=np.float64)
    bottom = np.asarray(wall["hoehe_unten_m"], dtype=np.float64)
    if len(points) != len(top) or len(points) != len(bottom):
        raise ValueError(f"Profil-Laenge stimmt nicht bei Wand {wall.get('name')}:{wall.get('teil')}")
    # Both supported variants smooth the contour; the wider variant keeps one
    # round of the source corners, while the default profile uses two.
    points, top, bottom = _chaikin(points, top, bottom, 1 if variant == 0 else 2)
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
    half = width * 0.5
    ring_size = 12
    positions = np.empty((len(points) * ring_size + 2, 3), dtype="<f4")
    indices: list[int] = []
    for i, (point, normal) in enumerate(zip(points, offsets / max(half, 1e-12))):
        low, high = float(bottom[i]), float(top[i])
        height = max(high - low, 0.01)
        radius = min(0.12, half * 0.18, height * 0.18)
        arcs = (
            (-half + radius, low + radius, (np.pi, 1.25 * np.pi, 1.5 * np.pi)),
            (half - radius, low + radius, (1.5 * np.pi, 1.75 * np.pi, 2.0 * np.pi)),
            (half - radius, high - radius, (0.0, 0.25 * np.pi, 0.5 * np.pi)),
            (-half + radius, high - radius, (0.5 * np.pi, 0.75 * np.pi, np.pi)),
        )
        ring = []
        for center_s, center_y, angles in arcs:
            ring.extend((center_s + radius * np.cos(a), center_y + radius * np.sin(a)) for a in angles)
        base = i * ring_size
        for j, (side, y) in enumerate(ring):
            positions[base + j] = (point[0] + normal[0] * side, y, point[1] + normal[1] * side)
    start_cap = len(points) * ring_size
    end_cap = start_cap + 1
    for cap, i in ((start_cap, 0), (end_cap, len(points) - 1)):
        positions[cap] = (points[i, 0], (top[i] + bottom[i]) * 0.5, points[i, 1])
    for i in range(len(points) - 1):
        for j in range(ring_size):
            k = (j + 1) % ring_size
            a, b, c, d = i * ring_size + j, i * ring_size + k, (i + 1) * ring_size + k, (i + 1) * ring_size + j
            indices.extend((a, b, c, a, c, d))
    for j in range(ring_size):
        k = (j + 1) % ring_size
        indices.extend((start_cap, k, j))
        a, b = (len(points) - 1) * ring_size + j, (len(points) - 1) * ring_size + k
        indices.extend((end_cap, a, b))
    return positions, np.asarray(indices, dtype="<u4")


def _terrain_heights(terrain_tiles: dict[str, Any], tile: str) -> tuple[np.ndarray, int] | None:
    item = terrain_tiles.get(tile)
    if not item:
        return None
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    rs = int(item["samples_per_m"])
    cols, rows = (x1 - x0) * rs + 1, (z1 - z0) * rs + 1
    positions = np.frombuffer(base64.b64decode(item["vertices_xyz_f32"]), dtype="<f4").reshape(-1, 3)
    if len(positions) != cols * rows:
        raise ValueError(f"Terrainmesh {tile} hat unerwartete Vertexzahl")
    return positions[:, 1].reshape(rows, cols), rs


def _sample_grid(heights: np.ndarray, rs: int, tile: str, x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Sample the rendered terrain triangles, including their a-to-d diagonal."""
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    u = np.clip((x - x0) * rs, 0, heights.shape[1] - 1.001)
    v = np.clip((z - z0) * rs, 0, heights.shape[0] - 1.001)
    ix, iz = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
    du, dv = u - ix, v - iz
    a = heights[iz, ix]
    b = heights[iz, ix + 1]
    c = heights[iz + 1, ix]
    d = heights[iz + 1, ix + 1]
    # tile_mesh uses triangles (a,c,d) and (a,d,b), split along a--d.
    first = a * (1.0 - dv) + c * (dv - du) + d * du
    second = a * (1.0 - du) + b * (du - dv) + d * dv
    return np.where(du <= dv, first, second)


def _bind_wall_foot(
    points: np.ndarray,
    bottom: np.ndarray,
    width: float,
    heights: np.ndarray,
    rs: int,
    tile: str,
    embed_m: float = 0.15,
) -> tuple[np.ndarray, int]:
    """Lower each wall-foot station below the visible terrain under its strip."""
    edges = np.diff(points, axis=0)
    lengths = np.linalg.norm(edges, axis=1)
    tangents = edges / np.maximum(lengths[:, None], 1e-12)
    normals = np.column_stack((-tangents[:, 1], tangents[:, 0]))
    local_bottom = bottom.copy()
    lowered = 0
    for i, point in enumerate(points):
        if i == 0:
            normal = normals[0]
        elif i == len(points) - 1:
            normal = normals[-1]
        else:
            normal = normals[i - 1] + normals[i]
            normal /= max(float(np.linalg.norm(normal)), 1e-12)
        # ``_solid`` spans half of the nominal width on each side. Sample that
        # same strip here; looking twice as wide lowered the foot to unrelated
        # terrain outside the wall and introduced avoidable bottom facets.
        offsets = np.linspace(-width * 0.5, width * 0.5, 9)
        sx = point[0] + normal[0] * offsets
        sz = point[1] + normal[1] * offsets
        ground = _sample_grid(heights, rs, tile, sx, sz)
        buried = float(np.min(ground)) - embed_m
        if buried < local_bottom[i]:
            local_bottom[i] = buried
            lowered += 1
    return local_bottom, lowered


def _b64(array: np.ndarray) -> str:
    return base64.b64encode(array.tobytes(order="C")).decode("ascii")


def build_wall_manifest(
    vector_path: Path,
    variant: int | None = None,
    terrain_tiles: dict[str, Any] | None = None,
    foot_variant: int | None = None,
) -> dict[str, Any]:
    """Build wall solids from the generated ``neu/vektor.json`` profiles."""
    if variant is None:
        import os
        variant = int(os.environ.get("WANDVAR", str(DEFAULT_VARIANT)))
    if foot_variant is None:
        import os
        foot_variant = int(os.environ.get("RELIEF_WANDFUSS_VAR", "1"))
    if variant not in VARIANTS:
        raise ValueError(f"WANDVAR muss eine der Varianten {sorted(VARIANTS)} sein")
    if foot_variant not in FOOT_VARIANTS:
        raise ValueError(f"RELIEF_WANDFUSS_VAR muss eine der Varianten {sorted(FOOT_VARIANTS)} sein")
    vector = json.loads(vector_path.read_text(encoding="utf-8"))
    tile_data: dict[str, Any] = {}
    lowered_total = 0
    for tile in ("D1", "G1", "D2"):
        bounds = TILE_BOUNDS[tile]
        terrain = _terrain_heights(terrain_tiles or {}, tile) if foot_variant in (1, 2) else None
        pieces: list[tuple[np.ndarray, np.ndarray]] = []
        features = 0
        used_widths: list[float] = []
        for wall in vector.get("waende", []):
            nominal = float(wall.get("breite_min_m", 0.0))
            if nominal <= 0:
                raise ValueError(f"Wand ohne positive Mindestbreite: {wall.get('name')}:{wall.get('teil')}")
            width = max(nominal, 2.4 if variant == 0 else nominal)
            for points, top, bottom in _chunks(wall, bounds, width, variant):
                if terrain is not None:
                    bottom, lowered = _bind_wall_foot(
                        points, bottom, width, terrain[0], terrain[1], tile,
                        embed_m=0.15 if foot_variant == 1 else 0.05,
                    )
                    lowered_total += lowered
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
            "foot_variant": foot_variant, "foot_variant_name": FOOT_VARIANTS[foot_variant],
            "foot_embed_m": (0.15 if foot_variant == 1 else 0.05)
            if foot_variant in (1, 2) and terrain_tiles else 0.0,
            "foot_vertices_lowered": int(lowered_total),
            "tiles": tile_data}
