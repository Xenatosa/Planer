"""Small immutable tiled mesh core, sourced from the exported relief field."""

from __future__ import annotations

from dataclasses import dataclass
import base64
import gzip
import hashlib
import json
from pathlib import Path
import struct
from typing import Any

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from shapely.geometry import LineString, Point, Polygon


SOURCE_COLUMNS = (
    "untergrund",
    "hindernis_id",
    "hindernis_art",
    "wasser_eis",
    "ebene",
    "bauzone_bestand",
    "bauzone_plan",
    "begehbar",
    "bebaubar",
)
TILE_BOUNDS = {
    "D2": (126, 43, 168, 86),
    "G1": (252, 0, 294, 43),
    "D1": (126, 0, 168, 43),
}
CELL_M = 1.2
TERRAIN_VARIANTS = {"0", "1", "2"}
RAMP_PROFILE_SETTINGS = {
    # Variant 1 profiles full ramp lengths; variant 2 is the targeted default.
    # Neither variant globally damps its result.
    "1": {"sigma_m": 3.0, "half_width_m": 1.5, "runout_m": 6.0, "endpoint_only": False, "cross_inner_m": 4.5, "cross_outer_m": 8.5},
    "2": {
        "sigma_m": 4.0, "half_width_m": 1.8, "runout_m": 8.0, "endpoint_only": True,
        "cross_inner_m": 4.5, "cross_outer_m": 9.5,
        "cross_half_width_m": 1.8, "cross_width_fade_m": 4.5,
        "cross_core_runout_m": 5.0, "cross_runout_m": 7.0,
    },
}


@dataclass(frozen=True)
class ReliefSource:
    data: dict[str, Any]
    heights: np.ndarray
    source_file_sha256: str


def load_relief(path: Path) -> ReliefSource:
    raw = path.read_bytes()
    data = json.loads(gzip.decompress(raw))
    nx, ny, rs = int(data["nx"]), int(data["ny"]), int(data["rs"])
    # main.js renders GB when present; prototype vertices must use that exact
    # field so D2 follows the same visible surface without a reset or patch.
    visible_field = data.get("GB") or data["G"]
    heights = np.frombuffer(base64.b64decode(visible_field), dtype=np.float32)
    expected = (ny * rs + 1) * (nx * rs + 1)
    if heights.size != expected:
        raise ValueError(f"G hat {heights.size} Werte; erwartet {expected}")
    return ReliefSource(data, heights.reshape(ny * rs + 1, nx * rs + 1), hashlib.sha256(raw).hexdigest())


def source_column_hashes(path: Path) -> dict[str, str]:
    """Hash each source column's UTF-8 values, preserving CSV row order."""
    import csv

    hashes = {name: hashlib.sha256() for name in SOURCE_COLUMNS}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(SOURCE_COLUMNS) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"Fehlende Zellquellspalten: {sorted(missing)}")
        for row in reader:
            for name, digest in hashes.items():
                digest.update((row[name] or "").encode("utf-8"))
                digest.update(b"\n")
    return {name: digest.hexdigest() for name, digest in hashes.items()}


def tile_mesh(
    source: ReliefSource, tile: str, tile_heights: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Triangulate one tile on the source grid; no height is resampled or edited."""
    if tile not in TILE_BOUNDS:
        raise KeyError(tile)
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    d = source.data
    rs = int(d["rs"])
    nx, ny = int(d["nx"]), int(d["ny"])
    if x1 > nx or z1 > ny:
        raise ValueError(f"Kachel {tile} liegt ausserhalb des Reliefgitters")

    sx0, sz0, sx1, sz1 = x0 * rs, z0 * rs, x1 * rs, z1 * rs
    slab = tile_heights if tile_heights is not None else source.heights[sz0 : sz1 + 1, sx0 : sx1 + 1]
    if slab.shape != (sz1 - sz0 + 1, sx1 - sx0 + 1):
        raise ValueError(f"Hoehenfeld fuer {tile} hat unerwartete Form {slab.shape}")
    zz, xx = np.mgrid[sz0 : sz1 + 1, sx0 : sx1 + 1]
    positions = np.empty((slab.size, 3), dtype="<f4")
    positions[:, 0] = (xx.ravel() / rs).astype(np.float32)
    positions[:, 1] = slab.ravel()
    positions[:, 2] = (zz.ravel() / rs).astype(np.float32)

    width = sx1 - sx0 + 1
    rows = sz1 - sz0
    cols = sx1 - sx0
    indices = np.empty((rows * cols * 6,), dtype="<u4")
    out = 0
    for row in range(rows):
        for col in range(cols):
            a = row * width + col
            b, c, d0 = a + 1, a + width, a + width + 1
            # Same diagonal and triangle order as the current 0.5 m surface.
            indices[out : out + 6] = (a, c, d0, a, d0, b)
            out += 6
    return positions, indices


def source_tile_mesh(cells_csv: Path, tile: str) -> tuple[np.ndarray, np.ndarray]:
    """Build D1/G1 from source cell-center heights at a 1 m vertex grid."""
    import csv

    if tile not in ("D1", "G1"):
        raise KeyError(tile)
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    cell_h = np.full((z1 - z0, x1 - x0), np.nan, dtype=np.float64)
    with cells_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"cx", "cy", "hoehe_m"}
        if not required.issubset(reader.fieldnames or ()):
            raise ValueError(f"Quell-CSV benoetigt Spalten {sorted(required)}")
        for row in reader:
            x, z = int(row["cx"]), int(row["cy"])
            if x0 <= x < x1 and z0 <= z < z1:
                cell_h[z - z0, x - x0] = float(row["hoehe_m"])
    if not np.isfinite(cell_h).all():
        raise ValueError(f"Unvollstaendige Zellhoehen in {tile}")
    heights = np.empty((z1 - z0 + 1, x1 - x0 + 1), dtype="<f4")
    for vz in range(heights.shape[0]):
        for vx in range(heights.shape[1]):
            samples = [cell_h[cz, cx] for cz in (vz - 1, vz) for cx in (vx - 1, vx)
                       if 0 <= cz < cell_h.shape[0] and 0 <= cx < cell_h.shape[1]]
            heights[vz, vx] = np.float32(sum(samples) / len(samples))
    rows, cols = heights.shape[0] - 1, heights.shape[1] - 1
    zz, xx = np.mgrid[0 : rows + 1, 0 : cols + 1]
    positions = np.empty((heights.size, 3), dtype="<f4")
    positions[:, 0] = (x0 + xx.ravel()).astype(np.float32)
    positions[:, 1] = heights.ravel()
    positions[:, 2] = (z0 + zz.ravel()).astype(np.float32)
    width = cols + 1
    indices = np.empty((rows * cols * 6,), dtype="<u4")
    out = 0
    for row in range(rows):
        for col in range(cols):
            a = row * width + col
            b, c, d0 = a + 1, a + width, a + width + 1
            indices[out : out + 6] = (a, c, d0, a, d0, b)
            out += 6
    return positions, indices


def _b64(array: np.ndarray) -> str:
    return base64.b64encode(array.tobytes(order="C")).decode("ascii")


def build_manifest(
    relief_path: Path,
    cells_csv: Path,
    vector_path: Path | None = None,
    fields_path: Path | None = None,
    variant: str | None = None,
) -> dict[str, Any]:
    source = load_relief(relief_path)
    directory = relief_path.parent / "neu"
    vector_path = vector_path or directory / "vektor.json"
    fields_path = fields_path or directory / "felder.npz"
    if variant is None:
        import os
        variant = os.environ.get("RELIEF_GELAENDE_VAR", "2")
    vector = json.loads(vector_path.read_text(encoding="utf-8"))
    with np.load(fields_path, allow_pickle=False) as archive:
        fields = {name: archive[name] for name in archive.files}
    tiles: dict[str, Any] = {}
    terrain: dict[str, Any] = {}
    for tile in ("D2", "G1", "D1"):
        heights, info = terrain_heights(source, tile, vector, fields, variant)
        positions, indices = tile_mesh(source, tile, heights)
        terrain[tile] = info
        samples_per_m = int(source.data["rs"])
        surface_mode = "locked_visible_GB_bytes" if tile == "D2" else "GB_with_local_profiles"
        tiles[tile] = {
            "bounds": list(TILE_BOUNDS[tile]),
            "samples_per_m": samples_per_m,
            "sampling_m": 1.0 / samples_per_m,
            "surface_mode": surface_mode,
            "vertices_xyz_f32": _b64(positions),
            "indices_u32": _b64(indices),
            "vertices": int(len(positions)),
            "triangles": int(len(indices) // 3),
            "height_sha256": hashlib.sha256(positions[:, 1].tobytes()).hexdigest(),
            "mesh_sha256": hashlib.sha256(positions.tobytes() + indices.tobytes()).hexdigest(),
        }
    return {
        "format": "relief-neu-tile-mesh-v2",
        "sampling_m": 1.0 / int(source.data["rs"]),
        "source_relief_sha256": source.source_file_sha256,
        "source_vector_sha256": hashlib.sha256(vector_path.read_bytes()).hexdigest(),
        "source_fields_sha256": hashlib.sha256(fields_path.read_bytes()).hexdigest(),
        "source_cell_columns": list(SOURCE_COLUMNS),
        "source_cell_column_sha256": source_column_hashes(cells_csv),
        "terrain_variant": variant,
        "terrain": terrain,
        "tiles": tiles,
    }


def write_manifest(relief_path: Path, cells_csv: Path, output: Path) -> dict[str, Any]:
    manifest = build_manifest(relief_path, cells_csv)
    raw = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    return manifest


def mesh_height_bytes(source: ReliefSource, tile: str) -> bytes:
    """Expose the exact per-tile y samples for byte-level D2 comparisons."""
    positions, _ = tile_mesh(source, tile)
    return b"".join(struct.pack("<f", float(v)) for v in positions[:, 1])


def _smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    t = np.clip((value - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _sample_field(field: np.ndarray, x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Sample a cell-centred global field at the mesh's world coordinates."""
    return ndi.map_coordinates(
        field,
        [z / CELL_M - 0.5, x / CELL_M - 0.5],
        order=1,
        mode="nearest",
        prefilter=False,
    )


def _sample_height(source: ReliefSource, x: np.ndarray, z: np.ndarray) -> np.ndarray:
    rs = int(source.data["rs"])
    return ndi.map_coordinates(
        source.heights,
        [z * rs, x * rs],
        order=1,
        mode="nearest",
        prefilter=False,
    )


def _polygon_from_feature(feature: dict[str, Any]) -> Polygon | None:
    rings = feature.get("polygon_m") or []
    if not rings:
        return None
    # Crossings store one ring directly; area features store a ring list.
    ring_list = rings if rings and isinstance(rings[0][0], (int, float)) else rings[0]
    exterior = [(float(x) / CELL_M, float(z) / CELL_M) for x, z in ring_list]
    holes = [
        [(float(x) / CELL_M, float(z) / CELL_M) for x, z in ring]
        for ring in (feature.get("innenringe_m") or [[]])[0]
    ]
    polygon = Polygon(exterior, holes)
    return polygon if not polygon.is_empty and polygon.is_valid else None


def _local_polygon_mask(
    polygon: Polygon, x: np.ndarray, z: np.ndarray, padding_world: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return candidate grid indices and distances for a feature near a tile."""
    min_x, min_z, max_x, max_z = polygon.bounds
    rs = int(round(1.0 / (x[0, 1] - x[0, 0]))) if x.shape[1] > 1 else 2
    pad = padding_world + 1.0 / rs
    where = np.where(
        (x >= min_x - pad) & (x <= max_x + pad)
        & (z >= min_z - pad) & (z <= max_z + pad)
    )
    if not len(where[0]):
        return where, np.empty(0, dtype=np.float64)
    coords = zip(x[where].ravel(), z[where].ravel())
    distances = np.fromiter(
        (polygon.distance(Point(float(px), float(pz))) * CELL_M for px, pz in coords),
        dtype=np.float64,
        count=len(where[0]),
    )
    return where, distances


def _road_profile_grid(
    source: ReliefSource,
    vector: dict[str, Any],
    x: np.ndarray,
    z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Create the road-spline target and width mask from the vector layer."""
    points: list[tuple[float, float]] = []
    target_heights: list[float] = []
    radii: list[float] = []
    for road in vector.get("wege", []):
        line = np.asarray(road.get("mittellinie_m", []), dtype=np.float64)
        if len(line) < 2:
            continue
        line /= CELL_M
        x0, z0 = x.min(), z.min()
        x1, z1 = x.max(), z.max()
        pad = float(road.get("breite_m", 2.4)) / CELL_M + 2.0
        if line[:, 0].max() < x0 - pad or line[:, 0].min() > x1 + pad or line[:, 1].max() < z0 - pad or line[:, 1].min() > z1 + pad:
            continue

        profile = _sample_height(source, line[:, 0], line[:, 1]).astype(np.float64)
        # Preserve the vector's explicit longitudinal shape where one exists;
        # its current source values are often flat, so GB remains the anchor.
        supplied = np.asarray(road.get("laengsprofil_m", []), dtype=np.float64)
        if len(supplied) == len(profile) and np.ptp(supplied) > 0.02:
            profile += supplied - ndi.gaussian_filter1d(supplied, sigma=4.0, mode="nearest")
        profile = ndi.gaussian_filter1d(profile, sigma=4.0, mode="nearest")
        points.extend(map(tuple, line.tolist()))
        target_heights.extend(profile.tolist())
        radii.extend([float(road.get("breite_m", 2.4)) * 0.5] * len(line))

    if not points:
        return np.zeros(x.shape, dtype=np.float64), np.zeros(x.shape, dtype=np.float64)
    tree = cKDTree(np.asarray(points, dtype=np.float64))
    q = np.column_stack((x.ravel(), z.ravel()))
    distance_world, nearest = tree.query(q, k=1, workers=1)
    distance_m = distance_world * CELL_M
    radius_m = np.asarray(radii, dtype=np.float64)[nearest].reshape(x.shape)
    target = np.asarray(target_heights, dtype=np.float64)[nearest].reshape(x.shape)
    # A path may pass close to a cliff or a steep cell transition. Keep its
    # longitudinal profile anchored to GB instead of dragging the whole slope.
    base = _sample_height(source, x, z)
    target = base + np.clip(target - base, -0.55, 0.55)
    weight = 1.0 - _smoothstep(radius_m, radius_m + 1.35, distance_m.reshape(x.shape))
    return target, weight


def _ramp_profile_grid(
    source: ReliefSource,
    x: np.ndarray,
    z: np.ndarray,
    variant: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Build longitudinal ramp profiles with at least 4 m of shoulder at both ends."""
    settings = RAMP_PROFILE_SETTINGS[variant]
    q = np.column_stack((x.ravel(), z.ravel()))
    weighted_target = np.zeros(len(q), dtype=np.float64)
    weight_sum = np.zeros(len(q), dtype=np.float64)
    weight_product = np.ones(len(q), dtype=np.float64)
    for raw in source.data.get("rampenwege", []):
        line = np.asarray(raw, dtype=np.float64)
        if len(line) < 2:
            continue
        lengths = np.r_[0.0, np.cumsum(np.hypot(*np.diff(line, axis=0).T) * CELL_M)]
        total_m = float(lengths[-1])
        x0, z0, x1, z1 = x.min(), z.min(), x.max(), z.max()
        pad = 9.0 / CELL_M
        if line[:, 0].max() < x0 - pad or line[:, 0].min() > x1 + pad or line[:, 1].max() < z0 - pad or line[:, 1].min() > z1 + pad:
            continue

        runout_m = settings["runout_m"]
        station = np.arange(-runout_m, total_m + runout_m + 0.001, 0.25, dtype=np.float64)
        clipped = np.clip(station, 0.0, total_m)
        px = np.interp(clipped, lengths, line[:, 0])
        pz = np.interp(clipped, lengths, line[:, 1])
        direction_start = (line[1] - line[0]) / max(lengths[1] / CELL_M, 1e-9)
        direction_end = (line[-1] - line[-2]) / max((lengths[-1] - lengths[-2]) / CELL_M, 1e-9)
        before = station < 0.0
        after = station > total_m
        px[before] += direction_start[0] * station[before] / CELL_M
        pz[before] += direction_start[1] * station[before] / CELL_M
        px[after] += direction_end[0] * (station[after] - total_m) / CELL_M
        pz[after] += direction_end[1] * (station[after] - total_m) / CELL_M
        source_profile = _sample_height(source, px, pz).astype(np.float64)
        profile = ndi.gaussian_filter1d(
            source_profile, sigma=max(1.0, settings["sigma_m"] / 0.25), mode="nearest",
        )
        start_blend = _smoothstep(0.0, runout_m, np.maximum(station + runout_m, 0.0))
        end_blend = _smoothstep(0.0, runout_m, np.maximum(total_m + runout_m - station, 0.0))
        blend = np.minimum(start_blend, end_blend)
        profile = source_profile + blend * (profile - source_profile)
        coords = np.column_stack((px, pz))
        tree = cKDTree(coords)
        _, nearest = tree.query(q, k=1, workers=1)
        segment_a = np.clip(nearest - 1, 0, len(coords) - 2)
        best_d2 = np.full(len(q), np.inf, dtype=np.float64)
        best_height = np.zeros(len(q), dtype=np.float64)
        best_station = np.zeros(len(q), dtype=np.float64)
        for segment in (segment_a, nearest.clip(0, len(coords) - 2)):
            a = coords[segment]
            vector = coords[segment + 1] - a
            norm2 = np.maximum(np.einsum("ij,ij->i", vector, vector), 1e-15)
            t = np.clip(np.einsum("ij,ij->i", q - a, vector) / norm2, 0.0, 1.0)
            projected = a + vector * t[:, None]
            delta = q - projected
            distance2 = np.einsum("ij,ij->i", delta, delta)
            better = distance2 < best_d2
            best_d2[better] = distance2[better]
            best_height[better] = profile[segment[better]] * (1.0 - t[better]) + profile[segment[better] + 1] * t[better]
            best_station[better] = station[segment[better]] * (1.0 - t[better]) + station[segment[better] + 1] * t[better]
        distance_m = np.sqrt(best_d2) * CELL_M
        path_weight = 1.0 - _smoothstep(
            settings["half_width_m"], settings["half_width_m"] + 1.5, distance_m,
        )
        if settings["endpoint_only"]:
            from_start = 1.0 - _smoothstep(4.0, 8.0, np.abs(best_station))
            from_end = 1.0 - _smoothstep(4.0, 8.0, np.abs(total_m - best_station))
            path_weight *= np.maximum(from_start, from_end)
        weighted_target += path_weight * best_height
        weight_sum += path_weight
        weight_product *= 1.0 - path_weight

    if not np.any(weight_sum):
        return np.zeros(x.shape, dtype=np.float64), np.zeros(x.shape, dtype=np.float64)
    target = np.divide(weighted_target, weight_sum, out=np.zeros_like(weighted_target), where=weight_sum > 0)
    weight = 1.0 - weight_product
    return target.reshape(x.shape), weight.reshape(x.shape)


def _ramp_intersections(source: ReliefSource, tile: str) -> list[tuple[float, float]]:
    """Return deterministic point intersections between distinct ramp paths."""
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    paths = [
        np.asarray(path, dtype=np.float64)
        for path in source.data.get("rampenwege", [])
        if len(path) >= 2
    ]
    lines = [LineString(path) for path in paths]
    points: list[tuple[float, float]] = []
    for i, a in enumerate(lines):
        if not a.intersects(Polygon([(x0, z0), (x1, z0), (x1, z1), (x0, z1)])):
            continue
        for b in lines[i + 1 :]:
            intersection = a.intersection(b)
            if intersection.is_empty:
                continue
            candidates = list(intersection.geoms) if hasattr(intersection, "geoms") else [intersection]
            for item in candidates:
                if item.geom_type == "Point" and x0 <= item.x <= x1 and z0 <= item.y <= z1:
                    points.append((float(item.x), float(item.y)))
    # Repeated/near-duplicate vertices at a shared polyline segment count as
    # one crossing patch.
    unique: list[tuple[float, float]] = []
    for point in sorted(points, key=lambda p: (round(p[1], 5), round(p[0], 5))):
        if all(np.hypot(point[0] - other[0], point[1] - other[1]) > 0.5 for other in unique):
            unique.append(point)
    return unique


def _ramp_intersection_pairs(source: ReliefSource, tile: str) -> list[tuple[float, float, int, int]]:
    """Return unique ramp crossing points with the two source path indices."""
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    bounds = Polygon([(x0, z0), (x1, z0), (x1, z1), (x0, z1)])
    paths = [
        np.asarray(path, dtype=np.float64)
        for path in source.data.get("rampenwege", [])
        if len(path) >= 2
    ]
    lines = [LineString(path) for path in paths]
    found: list[tuple[float, float, int, int]] = []
    for i, a in enumerate(lines):
        if not a.intersects(bounds):
            continue
        for j in range(i + 1, len(lines)):
            intersection = a.intersection(lines[j])
            if intersection.is_empty:
                continue
            candidates = list(intersection.geoms) if hasattr(intersection, "geoms") else [intersection]
            for item in candidates:
                if item.geom_type != "Point" or not (x0 <= item.x <= x1 and z0 <= item.y <= z1):
                    continue
                if all(np.hypot(item.x - px, item.y - pz) > 0.5 for px, pz, _, _ in found):
                    found.append((float(item.x), float(item.y), i, j))
    return sorted(found, key=lambda item: (round(item[1], 5), round(item[0], 5), item[2], item[3]))


def _apply_ramp_crossing_planes(
    base: np.ndarray,
    x: np.ndarray,
    z: np.ndarray,
    result: np.ndarray,
    source: ReliefSource,
    tile: str,
    variant: str,
) -> tuple[np.ndarray, int]:
    settings = RAMP_PROFILE_SETTINGS[variant]
    if variant == "2":
        # A circular constant-height patch made a visible plate and introduced
        # short contour teeth at its rim. Grade only the two intersecting road
        # corridors: keep a shared level through the measured crossing, then
        # feather sideways and along each approach with smoothstep weights.
        paths = [
            np.asarray(raw, dtype=np.float64) * CELL_M
            for raw in source.data.get("rampenwege", [])
            if len(raw) >= 2
        ]
        lines = [LineString(path) for path in paths]
        q = np.column_stack((x.ravel() * CELL_M, z.ravel() * CELL_M))
        correction_weight = np.zeros(len(q), dtype=np.float64)
        target_sum = np.zeros(len(q), dtype=np.float64)
        target_weight = np.zeros(len(q), dtype=np.float64)
        count = 0
        inner = float(settings["cross_inner_m"])
        half_width = float(settings["cross_half_width_m"])
        width_fade = float(settings["cross_width_fade_m"])
        core_runout = float(settings["cross_core_runout_m"])
        runout = float(settings["cross_runout_m"])

        for cx, cz, first, second in _ramp_intersection_pairs(source, tile):
            radial = np.hypot((x - cx) * CELL_M, (z - cz) * CELL_M)
            inside = radial <= inner
            if not inside.any():
                continue
            plane = float(np.median(base[inside]))
            crossing_weight = np.zeros(len(q), dtype=np.float64)
            point = Point(cx * CELL_M, cz * CELL_M)
            for path_index in (first, second):
                line = lines[path_index]
                center_station = line.project(point)
                lo = max(0.0, center_station - runout)
                hi = min(line.length, center_station + runout)
                stations = np.arange(lo, hi + 0.125, 0.25, dtype=np.float64)
                if len(stations) < 2:
                    continue
                coords = np.asarray([
                    (line.interpolate(float(station)).x, line.interpolate(float(station)).y)
                    for station in stations
                ], dtype=np.float64)
                tree = cKDTree(coords)
                _, nearest = tree.query(q, k=1, workers=1)
                segments = np.clip(nearest - 1, 0, len(coords) - 2)
                best_d2 = np.full(len(q), np.inf, dtype=np.float64)
                best_station = np.zeros(len(q), dtype=np.float64)
                for segment in (segments, np.clip(nearest, 0, len(coords) - 2)):
                    vector = coords[segment + 1] - coords[segment]
                    norm2 = np.maximum(np.einsum("ij,ij->i", vector, vector), 1e-15)
                    t = np.clip(np.einsum("ij,ij->i", q - coords[segment], vector) / norm2, 0.0, 1.0)
                    projected = coords[segment] + vector * t[:, None]
                    delta = q - projected
                    distance2 = np.einsum("ij,ij->i", delta, delta)
                    better = distance2 < best_d2
                    best_d2[better] = distance2[better]
                    best_station[better] = (
                        stations[segment[better]] * (1.0 - t[better])
                        + stations[segment[better] + 1] * t[better]
                    )
                distance = np.sqrt(best_d2)
                along = np.abs(best_station - center_station)
                lateral_weight = 1.0 - _smoothstep(half_width, half_width + width_fade, distance)
                along_weight = 1.0 - _smoothstep(core_runout, runout, along)
                crossing_weight = np.maximum(crossing_weight, lateral_weight * along_weight)

            # The corridor falloff alone left the outer edge of the measured
            # 4 m crossing footprint partly ungraded where the two approaches
            # curve away from one another. A broad radial feather fills that
            # footprint and eases the shared plane back into the source surface.
            radial_weight = 1.0 - _smoothstep(inner, inner + 4.0, radial.ravel())
            crossing_weight = np.maximum(crossing_weight, radial_weight)

            # The returned weight applies once in terrain_heights. Assigning the
            # shared target here keeps the feather continuous instead of
            # squaring its falloff at the corridor edge.
            target_sum += crossing_weight * plane
            target_weight += crossing_weight
            correction_weight = np.maximum(correction_weight, crossing_weight)
            count += int(np.count_nonzero(crossing_weight >= 0.999))

        target = np.divide(
            target_sum, target_weight,
            out=np.zeros_like(target_sum), where=target_weight > 0,
        ).reshape(x.shape)
        affected = target_weight.reshape(x.shape) > 0
        result[affected] = target[affected]
        return correction_weight.reshape(x.shape), count

    crossing_weight = np.zeros(x.shape, dtype=np.float64)
    count = 0
    for cx, cz in _ramp_intersections(source, tile):
        distance = np.hypot((x - cx) * CELL_M, (z - cz) * CELL_M)
        inside = distance <= settings["cross_inner_m"]
        if not inside.any():
            continue
        plane = float(np.median(base[inside]))
        weight = 1.0 - _smoothstep(
            settings["cross_inner_m"], settings["cross_outer_m"], distance,
        )
        weight[inside] = 1.0
        result += weight * (plane - result)
        crossing_weight = np.maximum(crossing_weight, weight)
        count += int(inside.sum())
    return crossing_weight, count


def _apply_feature_planes(
    base: np.ndarray,
    x: np.ndarray,
    z: np.ndarray,
    result: np.ndarray,
    features: list[dict[str, Any]],
    transition_default_m: float,
    kind: str,
) -> int:
    """Blend a crossing or zone to one shared plane with a soft outside edge."""
    count = 0
    for feature in features:
        polygon = _polygon_from_feature(feature)
        if polygon is None:
            continue
        where, distance_m = _local_polygon_mask(
            polygon, x, z, transition_default_m / CELL_M,
        )
        if not len(where[0]):
            continue
        # Build the plane from unmodified visible-height samples inside the polygon.
        inside = np.fromiter(
            (polygon.covers(Point(float(px), float(pz))) for px, pz in zip(x[where].ravel(), z[where].ravel())),
            dtype=bool,
            count=len(where[0]),
        )
        if not inside.any():
            continue
        ix, iz = where[1][inside], where[0][inside]
        # Use only the local tile samples in the polygon, avoiding a global fallback.
        plane = float(np.median(base[iz, ix]))
        if kind == "kreuzung":
            transition_m = max(float(feature.get("uebergang_m", transition_default_m)), 0.1)
        else:
            transition_m = transition_default_m
        weights = 1.0 - _smoothstep(0.0, transition_m, distance_m)
        weights[inside] = 1.0
        current = result[where]
        correction = np.clip(plane - current, -0.6, 0.6)
        result[where] = current + weights * correction
        count += int(inside.sum())
    return count


def _apply_zone_profile(
    fields: dict[str, np.ndarray], x: np.ndarray, z: np.ndarray, result: np.ndarray,
) -> int:
    distances = [
        _sample_field(fields[name], x, z)
        for name in ("bauzone_bestand", "bauzone_plan")
        if name in fields
    ]
    if not distances:
        return 0
    distance = np.minimum.reduce(distances)
    mask = distance <= 3.0
    if not mask.any():
        return 0
    # The extracted polygons can span several elevations. Shape a local pad
    # profile without forcing unrelated parts of a large polygon onto one plane.
    sample_step_m = CELL_M * (x[0, 1] - x[0, 0])
    local = ndi.gaussian_filter(result, sigma=max(1.0, 2.4 / sample_step_m), mode="nearest")
    weight = (1.0 - _smoothstep(0.0, 3.0, np.maximum(distance, 0.0))) * 0.45
    weight[distance <= 0.0] = 0.45
    result += weight * np.clip(local - result, -0.35, 0.35)
    return int(np.count_nonzero(mask))


def terrain_heights(
    source: ReliefSource,
    tile: str,
    vector: dict[str, Any],
    fields: dict[str, np.ndarray],
    variant: str = "2",
) -> tuple[np.ndarray, dict[str, Any]]:
    """Build a deterministic per-tile terrain surface from GB and feature layers."""
    if variant not in TERRAIN_VARIANTS:
        raise ValueError(f"RELIEF_GELAENDE_VAR muss einer von {sorted(TERRAIN_VARIANTS)} sein")
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    rs = int(source.data["rs"])
    sx0, sz0, sx1, sz1 = x0 * rs, z0 * rs, x1 * rs, z1 * rs
    base = source.heights[sz0 : sz1 + 1, sx0 : sx1 + 1].copy()
    if tile == "D2" or variant == "0":
        return base, {"variant": variant, "changed_vertices": 0, "max_abs_delta_m": 0.0, "layers": []}

    xx, zz = np.meshgrid(
        np.arange(sx0, sx1 + 1, dtype=np.float64) / rs,
        np.arange(sz0, sz1 + 1, dtype=np.float64) / rs,
    )
    result = base.astype(np.float64, copy=True)
    layers: list[str] = ["basishoehe_GB"]

    if variant == "2":
        road_weight = np.zeros(xx.shape, dtype=np.float64)
        ramp_weight = np.zeros(xx.shape, dtype=np.float64)
        cross_count = 0
    else:
        road_target, road_weight = _road_profile_grid(source, vector, xx, zz)
        if road_weight.any():
            result += road_weight * (road_target - result)
            layers.append("wege_spline_breite_laengsprofil")

        ramp_target, ramp_weight = _ramp_profile_grid(source, xx, zz, variant)
        if ramp_weight.any():
            result += ramp_weight * (ramp_target - result)
            layers.append("rampen_laengsprofil_weicher_querschnitt_auslauf_ge4m")

        cross_features = [
            item for item in vector.get("kreuzungen", [])
            if item.get("polygon_m")
        ]
        cross_count = _apply_feature_planes(
            base, xx, zz, result, cross_features, 2.4, "kreuzung",
        )
        if cross_count:
            layers.append("kreuzung_gemeinsame_ebene_weicher_rand")

    crossing_weight, ramp_crossings = _apply_ramp_crossing_planes(
        base, xx, zz, result, source, tile, variant,
    )
    if ramp_crossings:
        layers.append("rampenkreuzung_gemeinsame_ebene_weicher_rand")

    zone_count = _apply_zone_profile(fields, xx, zz, result) if variant == "1" else 0
    if zone_count:
        layers.append("bauzonen_lokales_profil_weicher_rand")

    # Water remains below the existing WV surface and eases back to the terrain
    # over 2.4 m; it is restricted to the selected tile using the global field.
    if variant == "1" and "wasser" in fields:
        water_distance = _sample_field(fields["wasser"], xx, zz)
        wv = source.data.get("WV")
        if wv:
            water = np.frombuffer(base64.b64decode(wv), dtype=np.float32).reshape(source.heights.shape)
            water_surface = water[sz0 : sz1 + 1, sx0 : sx1 + 1]
            valid = water_surface > -900.0
            water_weight = 1.0 - _smoothstep(0.0, 2.4, np.maximum(water_distance, 0.0))
            water_weight[water_distance <= 0.0] = 1.0
            water_weight *= valid
            water_target = result + np.clip(water_surface.astype(np.float64) - 0.20 - result, -0.35, 0.35)
            result += water_weight * (water_target - result)
            if water_weight.any():
                layers.append("wasser_spiegel_uferprofil")

    # Keep the emitted replacement surface pinned to GB at tile joins and at
    # wall bands. This preserves D1's measured cliff silhouette and all borders.
    edge_m = np.minimum.reduce((xx - x0, x1 - xx, zz - z0, z1 - zz)) * CELL_M
    tile_weight = _smoothstep(0.0, 3.0, edge_m)
    wall_distance = _sample_field(fields["wand"], xx, zz) if "wand" in fields else np.full(xx.shape, 99.0)
    wall_weight = _smoothstep(1.2, 4.8, wall_distance)
    # Explicit route profiles are allowed to meet the wall-foot surface; all
    # unrelated cliff geometry keeps the original wall-distance protection.
    weight = tile_weight * np.maximum.reduce((wall_weight, ramp_weight, crossing_weight))
    if tile == "D1":
        # Preserve the surveyed cliff control point and a local collar around it.
        d_cliff = np.hypot((xx - 140.0) * CELL_M, (zz - 35.0) * CELL_M)
        weight[d_cliff <= 1.0] = 0.0
    result = base + (result - base) * weight

    delta = result - base
    info = {
        "variant": variant,
        "changed_vertices": int(np.count_nonzero(np.abs(delta) > 1e-5)),
        "max_abs_delta_m": round(float(np.max(np.abs(delta))), 6),
        "mean_abs_delta_m": round(float(np.mean(np.abs(delta))), 6),
        "layers": layers + ["wand_abstandsschutz", "kachelrand_fade_3m"],
        "wand_protected_vertices": int(np.count_nonzero(wall_distance <= 1.2)),
        "crossing_flat_vertices": cross_count,
        "ramp_crossing_flat_vertices": ramp_crossings,
        "zone_flat_vertices": zone_count,
    }
    return result.astype("<f4"), info
