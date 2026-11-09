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
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import coo_matrix
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
WEGENDE_VARIANTS = {"0", "1", "2"}
KREUZUNG_VARIANTS = {"0", "1", "2", "3", "4", "5", "8", "9", "10"}
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

# The endpoint and crossing switches are deliberately independent from the
# broad legacy terrain variants. Variant 1 only shapes the named local feature.
WEGENDE_SETTINGS = {
    "1": {"runin_m": 4.0, "runout_m": 8.0, "smooth_sigma_m": 6.0,
          "max_grade": 0.10, "full_runout_m": 4.0, "lateral_core_m": 3.0,
          "lateral_fade_m": 4.5,
          # These are the three D1/G1 sites that fail the absolute R8a gate.
          "eligible_endpoints": {(1, True), (2, True), (11, True)}},
    "2": {"runin_m": 4.0, "runout_m": 6.0, "smooth_sigma_m": 8.0,
          "max_grade": 0.10, "full_runout_m": 4.0, "lateral_core_m": 2.5,
          "lateral_fade_m": 1.5,
          # The four endpoints are the measured D1/G1 R8a sites, including
          # the D1 endpoint at 156.5|37.5. This variant keeps the R8a strip
          # inside its full-weight lateral core and shortens the outer collar.
          "eligible_endpoints": {(1, True), (2, True), (11, True), (11, False)}},
}
KREUZUNG_SETTINGS = {
    "0": {"inner_m": 4.5, "radial_fade_m": 4.0},
    # Keep the measured crossing core and spread the height transition over a
    # wider shoulder so longitudinal grades return gradually to each approach.
    "1": {"inner_m": 4.5, "radial_fade_m": 8.0},
    # Radial-only correction leaves distant ramp ends on their source profile.
    "2": {"inner_m": 4.5, "radial_fade_m": 3.0,
          "core_runout_m": 2.8, "runout_m": 5.8, "radial_only": True},
    # Variant 3 solves the two D1 approach profiles together. The 2D transfer
    # applies the lateral and longitudinal weights as an actual height blend.
    "3": {"window_m": 18.0, "half_width_m": 1.8,
          "width_fade_m": 8.0, "along_fade_m": 2.0,
          "radial_inner_m": 5.0, "radial_outer_m": 12.0,
          "forward_window_m": 5.5,
          "plane_inner_m": 4.2,
          "plane_outer_m": 6.5},
    "4": {"window_m": 18.0, "half_width_m": 1.8,
          "width_fade_m": 8.0, "along_fade_m": 2.0,
          "radial_inner_m": 4.5, "radial_outer_m": 12.0,
          "forward_window_m": 6.5,
          "plane_inner_m": 4.8,
          "plane_outer_m": 7.0},
    "5": {"window_m": 18.0, "half_width_m": 1.8,
          "width_fade_m": 8.0, "along_fade_m": 2.0,
          "radial_inner_m": 5.0, "radial_outer_m": 14.0,
          "forward_window_m": 7.5,
          "plane_inner_m": 4.8,
          "plane_outer_m": 8.0},
    # p3d10 solves both D1 ramps over their complete polylines. The path band
    # is copied at full weight; only terrain outside that band is feathered.
    "8": {"mode": "free", "band_m": 1.81, "fade_m": 10.0, "plane_radius_m": 2.0, "plane_inner_m": 1.0, "plane_outer_m": 2.0},
    "9": {"mode": "wand40", "band_m": 1.81, "fade_m": 10.0, "plane_radius_m": 2.0, "plane_inner_m": 1.0, "plane_outer_m": 2.0},
    "10": {"mode": "mixed_wand", "band_m": 1.81, "fade_m": 10.0, "plane_radius_m": 2.0, "plane_inner_m": 1.0, "plane_outer_m": 2.0},
}

_FULL_CROSSING_CACHE: dict[tuple[str, str, str], tuple[list[np.ndarray], dict[str, Any]]] = {}


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
    rs = int(source.data["rs"])
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

    extensions: dict[str, Any] = {
        "format": "relief-neu-local-terrain-extension-v1",
        "vertices_xyz_f32": _b64(np.empty((0, 3), dtype="<f4")),
        "vertices": 0,
        "fine_vid_u32": _b64(np.empty(0, dtype="<u4")),
        "fine_h_f32": _b64(np.empty(0, dtype="<f4")),
        "fine_vertices": 0,
    }
    import os
    endpoint_variant = os.environ.get("RELIEF_WEGEND_VAR", "1")
    if variant == "2" and endpoint_variant != "0":
        all_z, all_x = np.mgrid[0 : source.heights.shape[0], 0 : source.heights.shape[1]]
        world_x, world_z = all_x.astype(np.float64) / rs, all_z.astype(np.float64) / rs
        extension_heights = source.heights.astype(np.float64, copy=True)
        extension_weight = np.zeros(source.heights.shape, dtype=np.float64)
        for tile in ("D1", "G1"):
            extension_heights, tile_weight, _ = _apply_ramp_endpoint_runouts(
                source, tile, world_x, world_z, extension_heights,
                endpoint_variant, outside_tile_only=True,
            )
            extension_weight = np.maximum(extension_weight, tile_weight)
        changed = np.abs(extension_heights - source.heights) > 1e-5
        if changed.any():
            iz, ix = np.nonzero(changed)
            vertices = np.column_stack((ix / rs, extension_heights[iz, ix], iz / rs)).astype("<f4")
            extensions["vertices_xyz_f32"] = _b64(vertices.reshape(-1))
            extensions["vertices"] = int(len(vertices))
            extensions["height_sha256"] = hashlib.sha256(vertices[:, 1].tobytes()).hexdigest()

            fine = source.data.get("FW") or {}
            fine_ids = np.frombuffer(base64.b64decode(fine.get("vid", "")), dtype=np.uint32)
            fine_h = np.frombuffer(base64.b64decode(fine.get("h", "")), dtype=np.float32)
            fs = int(fine.get("fs", 0))
            if fs and len(fine_ids) == len(fine_h):
                fw_width = int(source.data["nx"]) * fs + 1
                fx = (fine_ids % fw_width).astype(np.float64) / fs
                fz = (fine_ids // fw_width).astype(np.float64) / fs
                fine_weight = ndi.map_coordinates(
                    extension_weight, [fz * rs, fx * rs], order=1,
                    mode="nearest", prefilter=False,
                )
                fine_mask = fine_weight > 1e-5
                if fine_mask.any():
                    fine_values = ndi.map_coordinates(
                        extension_heights, [fz[fine_mask] * rs, fx[fine_mask] * rs],
                        order=1, mode="nearest", prefilter=False,
                    ).astype("<f4")
                    extensions["fine_vid_u32"] = _b64(fine_ids[fine_mask].astype("<u4"))
                    extensions["fine_h_f32"] = _b64(fine_values)
                    extensions["fine_vertices"] = int(len(fine_values))

    return {
        "format": "relief-neu-tile-mesh-v2",
        "sampling_m": 1.0 / int(source.data["rs"]),
        "source_relief_sha256": source.source_file_sha256,
        "source_vector_sha256": hashlib.sha256(vector_path.read_bytes()).hexdigest(),
        "source_fields_sha256": hashlib.sha256(fields_path.read_bytes()).hexdigest(),
        "source_cell_columns": list(SOURCE_COLUMNS),
        "source_cell_column_sha256": source_column_hashes(cells_csv),
        "terrain_variant": variant,
        "terrain_extensions": extensions,
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


def _apply_ramp_endpoint_runouts(
    source: ReliefSource,
    tile: str,
    x: np.ndarray,
    z: np.ndarray,
    result: np.ndarray,
    variant: str,
    *,
    outside_tile_only: bool = False,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Soften only ramp endpoints; keep each correction local and grade-limited."""
    weight_out = np.zeros(x.shape, dtype=np.float64)
    if variant == "0" or tile not in ("D1", "G1"):
        return result, weight_out, 0
    settings = WEGENDE_SETTINGS[variant]
    x0, z0, x1, z1 = TILE_BOUNDS[tile]
    d2x0, d2z0, d2x1, d2z1 = TILE_BOUNDS["D2"]
    q = np.column_stack((x.ravel() * CELL_M, z.ravel() * CELL_M))
    tile_mask = (x >= x0) & (x <= x1) & (z >= z0) & (z <= z1)
    outside_d2 = ~((x >= d2x0) & (x <= d2x1) & (z >= d2z0) & (z <= d2z1))
    total_changed = 0
    sample_step_m = 0.25

    for ramp_index, raw in enumerate(source.data.get("rampenwege", [])):
        line = np.asarray(raw, dtype=np.float64)
        if len(line) < 2:
            continue
        for is_start, endpoint, adjacent in (
            (True, line[0], line[1]), (False, line[-1], line[-2]),
        ):
            eligible = settings.get("eligible_endpoints")
            if eligible is not None and (ramp_index, is_start) not in eligible:
                continue
            if not (x0 <= endpoint[0] <= x1 and z0 <= endpoint[1] <= z1):
                continue
            direction = endpoint - adjacent if is_start else endpoint - adjacent
            length = float(np.hypot(*direction))
            if length <= 1e-9:
                continue
            direction = direction / length
            tangent = direction * (1.0 if is_start else 1.0)
            tangent_m = tangent.copy()
            tangent_m /= max(float(np.hypot(*tangent_m)), 1e-12)
            endpoint_m = endpoint * CELL_M
            rel = q - endpoint_m
            station = rel @ tangent_m
            lateral = np.abs(rel[:, 0] * tangent_m[1] - rel[:, 1] * tangent_m[0])

            # The profile is sampled on a 0.25 m line through the endpoint,
            # then its derivative is bounded before reintegration around the
            # unchanged endpoint height. This avoids a flat pad or hard edge.
            stations = np.arange(
                -settings["runin_m"], settings["runout_m"] + sample_step_m * 0.5,
                sample_step_m, dtype=np.float64,
            )
            coords = endpoint_m[None, :] + stations[:, None] * tangent_m[None, :]
            raw_profile = _sample_height(
                source, coords[:, 0] / CELL_M, coords[:, 1] / CELL_M,
            ).astype(np.float64)
            smoothed = ndi.gaussian_filter1d(
                raw_profile, sigma=settings["smooth_sigma_m"] / sample_step_m,
                mode="nearest",
            )
            grade = np.clip(
                np.gradient(smoothed, sample_step_m),
                -settings["max_grade"], settings["max_grade"],
            )
            grade = ndi.gaussian_filter1d(grade, sigma=0.5 / sample_step_m, mode="nearest")
            zero = int(round(settings["runin_m"] / sample_step_m))
            profile = np.empty_like(stations)
            profile[zero] = float(_sample_height(
                source, np.asarray([endpoint[0]]), np.asarray([endpoint[1]]),
            )[0])
            for i in range(zero + 1, len(profile)):
                profile[i] = profile[i - 1] + 0.5 * (grade[i - 1] + grade[i]) * sample_step_m
            for i in range(zero - 1, -1, -1):
                profile[i] = profile[i + 1] - 0.5 * (grade[i] + grade[i + 1]) * sample_step_m

            station_weight = _smoothstep(-settings["runin_m"], -1.5, station)
            station_weight *= 1.0 - _smoothstep(
                settings["full_runout_m"], settings["runout_m"], station,
            )
            lateral_weight = 1.0 - _smoothstep(
                settings["lateral_core_m"],
                settings["lateral_core_m"] + settings["lateral_fade_m"],
                lateral,
            )
            local_weight = station_weight * lateral_weight
            if outside_tile_only:
                dx = np.maximum.reduce((x0 - x, np.zeros(x.shape), x - x1)) * CELL_M
                dz = np.maximum.reduce((z0 - z, np.zeros(z.shape), z - z1)) * CELL_M
                outside_distance = np.hypot(dx, dz)
                edge_weight = _smoothstep(0.0, 3.0, outside_distance)
                local_weight = local_weight.reshape(x.shape) * (~tile_mask) * outside_d2 * edge_weight
                local_weight = local_weight.ravel()
            else:
                local_weight = local_weight.reshape(x.shape) * tile_mask
                local_weight = local_weight.ravel()

            eligible = local_weight > 1e-6
            if not eligible.any():
                continue
            target = np.interp(station, stations, profile)
            flat = result.ravel()
            delta = local_weight * (target - flat)
            flat += delta
            result = flat.reshape(x.shape)
            weight_out = np.maximum(weight_out, local_weight.reshape(x.shape))
            total_changed += int(np.count_nonzero(np.abs(delta) > 1e-5))

    return result, weight_out, total_changed


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


def _profile_path(path: np.ndarray, step_m: float = 0.25) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample the route using the same 0.25-coordinate-unit stations as R3."""
    points = np.asarray(path, dtype=np.float64)
    cumulative = np.r_[0.0, np.cumsum(np.hypot(*np.diff(points, axis=0).T))]
    stations = np.arange(0.0, cumulative[-1] + 1e-7, step_m, dtype=np.float64)
    coords = np.column_stack((
        np.interp(stations, cumulative, points[:, 0]),
        np.interp(stations, cumulative, points[:, 1]),
    ))
    return stations, coords, cumulative


def _solve_crossing_profiles(
    profiles: list[dict[str, Any]], crossing_m: np.ndarray,
) -> list[np.ndarray]:
    """Minimise the exact R3 residual around the crossing with a shared plane."""
    matrices: list[np.ndarray] = []
    free_indices: list[np.ndarray] = []
    offsets: list[int] = []
    variable_count = 0
    slack_segments: list[list[int]] = []
    for profile in profiles:
        h0 = profile["height"]
        stations = profile["stations"]
        center = profile["center"]
        in_window = (
            (stations >= center - profile["window_before"] - 1e-8)
            & (stations <= center + profile["window_after"] + 1e-8)
        )
        free = np.flatnonzero(in_window)
        if len(free) < 8:
            raise RuntimeError("LP-Fenster der Kreuzungsrampe ist zu kurz")
        # Pin both window boundaries to the original p3d6 profile.
        free = free[1:-1]
        operator = np.eye(len(h0)) - ndi.gaussian_filter1d(
            np.eye(len(h0)), sigma=8.0, axis=0, mode="nearest",
        )
        matrices.append(operator)
        free_indices.append(free)
        offsets.append(variable_count)
        variable_count += len(free)
        slack_segments.append(sorted({
            k // 16 for k in range(len(h0))
            if np.any(np.abs(operator[k, free]) > 1e-9)
        }))

    t_index = variable_count
    hc_index, gx_index, gz_index = t_index + 1, t_index + 2, t_index + 3
    slack_start = variable_count + 4
    slack_offsets: list[dict[int, int]] = []
    next_slack = slack_start
    for segments in slack_segments:
        slack_offsets.append({segment: next_slack + i for i, segment in enumerate(segments)})
        next_slack += len(segments)
    nvars = next_slack
    aub: list[np.ndarray] = []
    bub: list[float] = []

    for route, profile in enumerate(profiles):
        h0 = profile["height"]
        stations = profile["stations"]
        coords = profile["coords"]
        center = profile["center"]
        free = free_indices[route]
        offset = offsets[route]
        index_to_var = np.full(len(h0), -1, dtype=np.int64)
        index_to_var[free] = offset + np.arange(len(free))
        operator = matrices[route]
        fixed_profile = h0.copy()
        fixed_profile[free] = 0.0
        fixed_residual = operator @ fixed_profile

        # Match h - gaussian_filter1d(h, sigma=8), in the same 16-sample
        # groups used by pruefe_regeln.py. The small slack keeps infeasible
        # source sections solvable while the objective minimizes total excess.
        for k in range(len(h0)):
            coeff = operator[k, free]
            if not np.any(np.abs(coeff) > 1e-9):
                continue
            segment = k // 16
            row = np.zeros(nvars, dtype=np.float64)
            row[offset:offset + len(free)] = coeff
            row[slack_offsets[route][segment]] = -1.0
            aub.append(row)
            bub.append(0.075 - fixed_residual[k])
            opposite = -row
            opposite[slack_offsets[route][segment]] = -1.0
            aub.append(opposite)
            bub.append(0.075 + fixed_residual[k])

        # Minimise the largest profile movement after the residual objective.
        for local, k in enumerate(free):
            row = np.zeros(nvars, dtype=np.float64)
            row[offset + local] = 1.0
            row[t_index] = -1.0
            aub.append(row)
            bub.append(float(h0[k]))
            row = np.zeros(nvars, dtype=np.float64)
            row[offset + local] = -1.0
            row[t_index] = -1.0
            aub.append(row)
            bub.append(float(-h0[k]))

        # Preserve the 0.6 m/m maximum change between adjacent stations.
        for k in range(1, len(h0)):
            if index_to_var[k] < 0 and index_to_var[k - 1] < 0:
                continue
            row = np.zeros(nvars, dtype=np.float64)
            constant = 0.0
            for idx, sign in ((k, 1.0), (k - 1, -1.0)):
                var = index_to_var[idx]
                if var >= 0:
                    row[var] += sign
                else:
                    constant += sign * float(h0[idx])
            aub.append(row)
            bub.append(0.15 - constant)
            aub.append(-row)
            bub.append(0.15 + constant)

        # Keep both 4 m crossing sections close to one shared, nearly level plane.
        for k in np.flatnonzero(np.abs(stations - center) <= 4.0 + 1e-8):
            var = index_to_var[k]
            if var < 0:
                continue
            dx, dz = (coords[k] * CELL_M) - crossing_m
            row = np.zeros(nvars, dtype=np.float64)
            row[var] = 1.0
            row[hc_index] = -1.0
            row[gx_index] = -dx
            row[gz_index] = -dz
            aub.append(row)
            bub.append(0.04)
            aub.append(-row)
            bub.append(0.04)

    # Polygonal outer approximation of hypot(gx, gz) <= 0.03.
    for angle in np.arange(0.0, 2.0 * np.pi, np.pi / 16.0):
        row = np.zeros(nvars, dtype=np.float64)
        row[gx_index] = np.cos(angle)
        row[gz_index] = np.sin(angle)
        aub.append(row)
        bub.append(0.03)

    objective = np.zeros(nvars, dtype=np.float64)
    objective[t_index] = 1e-3
    objective[slack_start:] = 1.0
    bounds = [(None, None)] * variable_count + [
        (0.0, None), (None, None), (-0.03, 0.03), (-0.03, 0.03),
    ]
    bounds.extend([(0.0, 0.225)] * (nvars - len(bounds)))
    solution = linprog(
        objective, A_ub=np.asarray(aub), b_ub=np.asarray(bub), bounds=bounds,
        method="highs",
    )
    if not solution.success:
        raise RuntimeError(f"D1-Kreuzungs-LP nicht lösbar: {solution.message}")

    solved: list[np.ndarray] = []
    for route, profile in enumerate(profiles):
        height = profile["height"].copy()
        free = free_indices[route]
        offset = offsets[route]
        height[free] = solution.x[offset:offset + len(free)]
        solved.append(height)
    return solved


def _solve_full_ramp_profiles(
    profiles: list[dict[str, Any]], crossing_m: np.ndarray, variant: str,
    cache_key: tuple[str, str, str],
) -> tuple[list[np.ndarray], dict[str, Any]]:
    """Solve the two complete D1 profiles with the gate's sampled R3 operator.

    A binary variable represents one 16-sample section (the exact grouping in
    pruefe_regeln.py). The first MILP minimizes the count of sections that may
    exceed 0.075 m; a second solve fixes that count and minimizes total L1
    movement from the p3d6 crossing surface. End caps remain pinned, and the
    wall40 alternatives constrain the wall-side tail of rampe_11.
    """
    cached = _FULL_CROSSING_CACHE.get(cache_key)
    if cached is not None:
        return [item.copy() for item in cached[0]], dict(cached[1])

    profile_count = len(profiles)
    if profile_count != 2:
        raise ValueError("Die D1-Ganzrampenloesung benoetigt genau zwei Rampen")
    lengths = [len(profile["height"]) for profile in profiles]
    h_offsets = np.cumsum([0, *lengths[:-1]]).astype(int).tolist()
    total_h = sum(lengths)
    sections_per_route = [(length + 15) // 16 for length in lengths]
    section_offsets = np.cumsum([0, *sections_per_route[:-1]]).astype(int).tolist()
    total_sections = sum(sections_per_route)
    deviation_start = total_h
    binary_start = total_h * 2
    plane_index = binary_start + total_sections
    variable_count = plane_index + 1

    lower = np.empty(variable_count, dtype=np.float64)
    upper = np.empty(variable_count, dtype=np.float64)
    h0_flat = np.empty(total_h, dtype=np.float64)
    route_bounds: list[tuple[np.ndarray, np.ndarray]] = []
    mode = KREUZUNG_SETTINGS[variant]["mode"]
    for route, profile in enumerate(profiles):
        h0 = np.asarray(profile["height"], dtype=np.float64)
        stations = np.asarray(profile["stations"], dtype=np.float64)
        offset = h_offsets[route]
        h0_flat[offset:offset + len(h0)] = h0
        lo, hi = h0 - 2.0, h0 + 2.0
        # Match the measurement scripts' one-coordinate-unit fixed end caps.
        fixed = (stations <= 1.0 + 1e-9) | (stations >= stations[-1] - 1.0 - 1e-9)
        # Preserve the tile join wherever a route enters or leaves within the
        # 3 m tile fade. The axis proof is otherwise diluted by the edge mask.
        tile_x0, tile_z0, tile_x1, tile_z1 = TILE_BOUNDS["D1"]
        px, pz = np.asarray(profile["coords"], dtype=np.float64).T
        tile_edge_distance = np.minimum.reduce((px - tile_x0, tile_x1 - px, pz - tile_z0, tile_z1 - pz)) * CELL_M
        fixed |= tile_edge_distance < 3.0 - 1e-8
        if int(profile["index"]) == 11 and mode == "wand40":
            fixed |= stations >= 40.0 - 1e-9
        elif int(profile["index"]) == 11 and mode == "mixed_wand":
            lo[stations >= 40.0 - 1e-9] = np.maximum(
                lo[stations >= 40.0 - 1e-9], h0[stations >= 40.0 - 1e-9] - 0.25,
            )
            hi[stations >= 40.0 - 1e-9] = np.minimum(
                hi[stations >= 40.0 - 1e-9], h0[stations >= 40.0 - 1e-9] + 0.25,
            )
        lo[fixed] = h0[fixed]
        hi[fixed] = h0[fixed]
        route_bounds.append((lo, hi))
        lower[offset:offset + len(h0)] = lo
        upper[offset:offset + len(h0)] = hi

    lower[deviation_start:binary_start] = 0.0
    upper[deviation_start:binary_start] = 2.0
    lower[binary_start:plane_index] = 0.0
    upper[binary_start:plane_index] = 1.0
    for route, profile in enumerate(profiles):
        stations = np.asarray(profile["stations"], dtype=np.float64)
        center = float(profile["center"])
    plane_heights = np.concatenate([
        np.asarray(profile["height"], dtype=np.float64)[
            np.flatnonzero(
                np.abs(np.asarray(profile["stations"]) - float(profile["center"])) * CELL_M
                <= float(KREUZUNG_SETTINGS[variant]["plane_radius_m"]) + 1e-8
            )
        ]
        for profile in profiles
    ])
    lower[plane_index] = float(plane_heights.min() - 2.0)
    upper[plane_index] = float(plane_heights.max() + 2.0)

    integrality = np.zeros(variable_count, dtype=np.uint8)
    integrality[binary_start:plane_index] = 1
    row_indices: list[int] = []
    column_indices: list[int] = []
    values: list[float] = []
    row_lower: list[float] = []
    row_upper: list[float] = []

    def add_constraint(entries: dict[int, float], lo: float = -np.inf, hi: float = np.inf) -> None:
        row = len(row_lower)
        for column, value in entries.items():
            if abs(value) > 1e-13:
                row_indices.append(row)
                column_indices.append(int(column))
                values.append(float(value))
        row_lower.append(float(lo))
        row_upper.append(float(hi))

    # Absolute movement from the p3d6 surface, used only by the second solve.
    for k, h0 in enumerate(h0_flat):
        d = deviation_start + k
        add_constraint({k: 1.0, d: -1.0}, hi=float(h0))
        add_constraint({k: -1.0, d: -1.0}, hi=float(-h0))

    for route, profile in enumerate(profiles):
        h0 = np.asarray(profile["height"], dtype=np.float64)
        stations = np.asarray(profile["stations"], dtype=np.float64)
        offset = h_offsets[route]
        section_offset = section_offsets[route]
        operator = np.eye(len(h0), dtype=np.float64) - ndi.gaussian_filter1d(
            np.eye(len(h0), dtype=np.float64), sigma=8.0, axis=0, mode="nearest",
        )

        # Exact R3 residual rows, relaxed by one binary for each checker section.
        lo_h, hi_h = route_bounds[route]
        for k in range(len(h0)):
            op_row = operator[k]
            active = np.flatnonzero(np.abs(op_row) > 1e-12)
            section = binary_start + section_offset + k // 16
            row = {offset + int(j): float(op_row[j]) for j in active}
            max_value = sum(
                float(op_row[j]) * (hi_h[j] if op_row[j] >= 0.0 else lo_h[j])
                for j in active
            )
            min_value = sum(
                float(op_row[j]) * (lo_h[j] if op_row[j] >= 0.0 else hi_h[j])
                for j in active
            )
            upper_relaxation = max(0.0, max_value - 0.075)
            lower_relaxation = max(0.0, -min_value - 0.075)
            add_constraint({**row, section: -upper_relaxation}, hi=0.075)
            add_constraint({**{j: -v for j, v in row.items()}, section: -lower_relaxation}, hi=0.075)

        # Physical grade <= 0.6 m/m: 0.18 m over each 0.30 m station step.
        for k in range(1, len(h0)):
            add_constraint({offset + k: 1.0, offset + k - 1: -1.0}, hi=0.18)
            add_constraint({offset + k: -1.0, offset + k - 1: 1.0}, hi=0.18)

        # Both complete bands share one constant plane inside the 2 m crossing disk.
        center = float(profile["center"])
        for k in np.flatnonzero(
            np.abs(stations - center) * CELL_M
            <= float(KREUZUNG_SETTINGS[variant]["plane_radius_m"]) + 1e-8
        ):
            h = offset + int(k)
            add_constraint({h: 1.0, plane_index: -1.0}, hi=0.01)
            add_constraint({h: -1.0, plane_index: 1.0}, hi=0.01)

    # The first solve minimizes the exact number of sections with any residual
    # above 0.075 m. The second solve fixes that count before minimizing L1 movement.
    def make_linear_constraint() -> LinearConstraint:
        matrix = coo_matrix(
            (values, (row_indices, column_indices)),
            shape=(len(row_lower), variable_count),
        ).tocsr()
        return LinearConstraint(matrix, np.asarray(row_lower), np.asarray(row_upper))

    bounds = Bounds(lower, upper)
    objective = np.zeros(variable_count, dtype=np.float64)
    objective[binary_start:plane_index] = 1.0
    first = milp(
        objective, integrality=integrality, bounds=bounds,
        constraints=make_linear_constraint(),
        options={"presolve": True, "mip_rel_gap": 0.0},
    )
    if not first.success:
        raise RuntimeError(f"D1-Ganzrampen-MILP unloesbar: {first.message}")
    optimal_sections = int(round(float(first.fun)))
    add_constraint(
        {j: 1.0 for j in range(binary_start, plane_index)},
        hi=float(optimal_sections),
    )
    movement_objective = np.zeros(variable_count, dtype=np.float64)
    movement_objective[deviation_start:binary_start] = 1.0
    second = milp(
        movement_objective, integrality=integrality, bounds=bounds,
        constraints=make_linear_constraint(),
        options={"presolve": True, "mip_rel_gap": 0.0},
    )
    if not second.success:
        raise RuntimeError(f"D1-Ganzrampen-Zweitlauf unloesbar: {second.message}")

    solved: list[np.ndarray] = []
    section_report: list[dict[str, Any]] = []
    for route, profile in enumerate(profiles):
        length = lengths[route]
        offset = h_offsets[route]
        height = second.x[offset:offset + length].copy()
        residual = height - ndi.gaussian_filter1d(height, sigma=8.0, mode="nearest")
        solved.append(height)
        for start in range(0, length, 16):
            stop = min(start + 16, length)
            maximum = float(np.max(np.abs(residual[start:stop])))
            if maximum > 0.075 + 1e-6:
                section_report.append({
                    "rampe": f"rampe_{profile['index']}",
                    "station_start": round(float(profile["stations"][start]), 3),
                    "station_stop": round(float(profile["stations"][stop - 1]), 3),
                    "max_abs_lr_m": round(maximum, 6),
                })
    diagnostics = {
        "variant": variant,
        "mode": mode,
        "status": "optimal",
        "optimal_sections_over_0_075_m": optimal_sections,
        "actual_sections_over_0_075_m": len(section_report),
        "total_abs_delta_m": round(float(np.abs(second.x[:total_h] - h0_flat).sum()), 6),
        "max_abs_delta_m": round(float(np.abs(second.x[:total_h] - h0_flat).max()), 6),
        "crossing_plane_height_m": round(float(second.x[plane_index]), 6),
        "crossing_plane_slope_pct": 0.0,
        "crossing_plane_max_deviation_m": round(float(np.max(np.abs(np.concatenate([
            solved[route][
                np.flatnonzero(
                    np.abs(np.asarray(profile["stations"]) - float(profile["center"])) * CELL_M
                    <= float(KREUZUNG_SETTINGS[variant]["plane_radius_m"]) + 1e-8
                )
            ]
            for route, profile in enumerate(profiles)
        ]) - second.x[plane_index]))), 6),
        "sections": section_report,
    }
    _FULL_CROSSING_CACHE[cache_key] = ([item.copy() for item in solved], dict(diagnostics))
    return solved, diagnostics


def _project_to_path(
    query_m: np.ndarray,
    path_m: np.ndarray,
    cumulative: np.ndarray,
    station_lo: float,
    station_hi: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return nearest path station and lateral distance for local grid points."""
    starts, ends = path_m[:-1], path_m[1:]
    lengths = np.diff(cumulative)
    keep = (cumulative[:-1] <= station_hi) & (cumulative[1:] >= station_lo)
    starts, ends = starts[keep], ends[keep]
    seg_start, seg_length = cumulative[:-1][keep], lengths[keep]
    vector = ends - starts
    norm2 = np.maximum(np.einsum("ij,ij->i", vector, vector), 1e-15)
    delta = query_m[:, None, :] - starts[None, :, :]
    t = np.clip(np.einsum("qsi,si->qs", delta, vector) / norm2[None, :], 0.0, 1.0)
    projected = starts[None, :, :] + t[:, :, None] * vector[None, :, :]
    residual = query_m[:, None, :] - projected
    d2 = np.einsum("qsi,qsi->qs", residual, residual)
    station = seg_start[None, :] + t * seg_length[None, :]
    chosen = np.argmin(d2, axis=1)
    rows = np.arange(len(query_m))
    return station[rows, chosen], np.sqrt(d2[rows, chosen])


def _project_to_ramp_strip(
    query_m: np.ndarray,
    coords: np.ndarray,
    stations: np.ndarray,
    normals: np.ndarray,
    band_m: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Map grid points into the checker-sampled, constant-height ramp ribbon.

    The R3 checker offsets the sampled centerline by its central-difference
    normals. At a polyline corner those normals differ from the nearest raw
    segment normal, so ordinary closest-segment projection creates false cross
    slopes. This inverse map uses the same sampled cross sections inside the
    full-weight road band, then falls back to nearest-path coordinates outside.
    """
    path_m = np.asarray(coords, dtype=np.float64) * CELL_M
    station_m = np.asarray(stations, dtype=np.float64) * CELL_M
    fallback_station, fallback_lateral = _project_to_path(
        query_m, path_m, station_m, float(station_m[0]), float(station_m[-1]),
    )
    output_station = fallback_station.copy()
    output_lateral = fallback_lateral.copy()
    inside_strip = np.zeros(len(query_m), dtype=bool)
    best_center_d2 = np.full(len(query_m), np.inf, dtype=np.float64)

    left = path_m + normals * band_m
    right = path_m - normals * band_m
    for k in range(len(path_m) - 1):
        center_start = path_m[k]
        center_vector = path_m[k + 1] - center_start
        center_norm2 = max(float(np.dot(center_vector, center_vector)), 1e-15)
        center_t = np.clip(
            ((query_m - center_start) @ center_vector) / center_norm2, 0.0, 1.0,
        )
        center_delta = query_m - (center_start + center_t[:, None] * center_vector)
        center_d2 = np.einsum("ij,ij->i", center_delta, center_delta)
        triangles = (
            (left[k], right[k], right[k + 1], (station_m[k], station_m[k], station_m[k + 1]), (band_m, -band_m, -band_m)),
            (left[k], right[k + 1], left[k + 1], (station_m[k], station_m[k + 1], station_m[k + 1]), (band_m, -band_m, band_m)),
        )
        for a, b, c, triangle_stations, triangle_lateral in triangles:
            v0, v1 = b - a, c - a
            d00, d01, d11 = float(v0 @ v0), float(v0 @ v1), float(v1 @ v1)
            denom = d00 * d11 - d01 * d01
            if abs(denom) < 1e-12:
                continue
            v2 = query_m - a
            d20 = v2 @ v0
            d21 = v2 @ v1
            wb = (d11 * d20 - d01 * d21) / denom
            wc = (d00 * d21 - d01 * d20) / denom
            wa = 1.0 - wb - wc
            inside = (wa >= -1e-9) & (wb >= -1e-9) & (wc >= -1e-9)
            better = inside & (center_d2 < best_center_d2)
            if not better.any():
                continue
            output_station[better] = (
                wa[better] * triangle_stations[0]
                + wb[better] * triangle_stations[1]
                + wc[better] * triangle_stations[2]
            )
            output_lateral[better] = (
                wa[better] * triangle_lateral[0]
                + wb[better] * triangle_lateral[1]
                + wc[better] * triangle_lateral[2]
            )
            best_center_d2[better] = center_d2[better]
            inside_strip[better] = True
    return output_station, output_lateral, inside_strip


def _apply_d1_optimized_crossing(
    base: np.ndarray,
    x: np.ndarray,
    z: np.ndarray,
    result: np.ndarray,
    source: ReliefSource,
    variant: str,
    endpoint_weight: np.ndarray,
) -> tuple[np.ndarray, int]:
    """Blend jointly solved profiles into the p3d6 surface at the D1 crossing."""
    settings = KREUZUNG_SETTINGS[variant]
    crossings = _ramp_intersection_pairs(source, "D1")
    if not crossings or (crossings[0][2], crossings[0][3]) != (2, 11):
        raise RuntimeError("Erwartete D1-Kreuzung rampe_2/rampe_11 fehlt")
    cx, cz, _, _ = crossings[0]
    crossing_m = np.array([cx, cz], dtype=np.float64) * CELL_M

    # Recreate the selected p3d6 crossing as the local terrain background.
    # The old radial mask is blended once here; it is not used as a hard write.
    p3d6_surface = result.copy()
    crossed_surface = p3d6_surface.copy()
    old_weight, _ = _apply_ramp_crossing_planes(
        base, x, z, crossed_surface, source, "D1", "2", "2",
    )
    p3d6_surface += old_weight * (crossed_surface - p3d6_surface)
    # Keep the complete p3d6 crossing and its radial shoulder as the terrain
    # background; only the weighted LP corridor below may replace its height.
    result[:] = p3d6_surface

    raw_paths = source.data.get("rampenwege", [])
    x0, z0, _, _ = TILE_BOUNDS["D1"]
    rs = int(source.data["rs"])
    profiles: list[dict[str, Any]] = []
    for path_index in (2, 11):
        path = np.asarray(raw_paths[path_index], dtype=np.float64)
        stations, coords, cumulative = _profile_path(path)
        center = float(LineString(path).project(Point(cx, cz)))
        window_before = float(settings["window_m"])
        window_after = window_before
        if path_index == 11:
            window_after = min(
                window_after,
                float(cumulative[-1]) - center - 1.0 / CELL_M,
            )
        apply_window_after = window_after
        if path_index == 11:
            apply_window_after = min(
                float(settings.get("forward_window_m", window_after)),
                window_after,
            )
        row = (coords[:, 1] - z0) * rs
        col = (coords[:, 0] - x0) * rs
        height = ndi.map_coordinates(p3d6_surface, [row, col], order=1, mode="nearest")
        profiles.append({
            "index": path_index,
            "stations": stations,
            "coords": coords,
            "path_m": path * CELL_M,
            "cumulative": cumulative * CELL_M,
            "center": center,
            "center_phys": center * CELL_M,
            "window_before": window_before,
            "window_after": window_after,
            "window_before_phys": window_before * CELL_M,
            "window_after_phys": window_after * CELL_M,
            "apply_window_after_phys": apply_window_after * CELL_M,
            "height": height,
        })

    solved = _solve_crossing_profiles(profiles, crossing_m)
    plane_height = float(np.mean([
        np.interp(profile["center"], profile["stations"], height)
        for profile, height in zip(profiles, solved)
    ]))

    # Restrict the expensive path projection to the local crossing region.
    margin_m = float(settings["window_m"]) * CELL_M + float(settings["width_fade_m"]) + 8.0
    local = np.hypot((x - cx) * CELL_M, (z - cz) * CELL_M) <= margin_m
    flat_index = np.flatnonzero(local.ravel())
    query = np.column_stack((x.ravel()[flat_index] * CELL_M, z.ravel()[flat_index] * CELL_M))
    target_sum = np.zeros(len(flat_index), dtype=np.float64)
    target_weight = np.zeros(len(flat_index), dtype=np.float64)
    profile_weight = np.zeros(len(flat_index), dtype=np.float64)
    crossing_weight = old_weight.ravel().copy()

    for profile, height in zip(profiles, solved):
        station, lateral = _project_to_path(
            query, profile["path_m"], profile["cumulative"],
            max(0.0, profile["center_phys"] - profile["window_before_phys"]),
            min(float(profile["cumulative"][-1]), profile["center_phys"] + profile["apply_window_after_phys"]),
        )
        lateral_weight = 1.0 - _smoothstep(
            float(settings["half_width_m"]),
            float(settings["half_width_m"] + settings["width_fade_m"]),
            lateral,
        )
        station_delta = station - profile["center_phys"]
        station_window = np.where(
            station_delta < 0.0,
            profile["window_before_phys"],
            profile["apply_window_after_phys"],
        )
        along_weight = 1.0 - _smoothstep(
            np.maximum(0.0, station_window - settings["along_fade_m"]),
            station_window,
            np.abs(station_delta),
        )
        radius = np.hypot(query[:, 0] - crossing_m[0], query[:, 1] - crossing_m[1])
        radial_weight = 1.0 - _smoothstep(
            float(settings["radial_inner_m"]), float(settings["radial_outer_m"]), radius,
        )
        weight = lateral_weight * along_weight * radial_weight
        target = np.interp(station / CELL_M, profile["stations"], height)
        target_sum += weight * target
        target_weight += weight
        profile_weight = np.maximum(profile_weight, weight)
        crossing_weight[flat_index] = np.maximum(crossing_weight[flat_index], weight)

    affected = target_weight > 0.0
    if affected.any():
        radius = np.hypot(
            query[affected, 0] - crossing_m[0], query[affected, 1] - crossing_m[1],
        )
        plane_mix = 1.0 - _smoothstep(
            float(settings["plane_inner_m"]), float(settings["plane_outer_m"]), radius,
        )
        profile_target = target_sum[affected] / target_weight[affected]
        target = profile_target * (1.0 - plane_mix) + plane_height * plane_mix
        weight = np.maximum(profile_weight[affected], plane_mix)
        background = p3d6_surface.ravel()[flat_index[affected]]
        result_flat = result.ravel()
        result_flat[flat_index[affected]] = target * weight + background * (1.0 - weight)

    weight_grid = crossing_weight.reshape(x.shape)
    return weight_grid, int(np.count_nonzero(weight_grid >= 0.999))


def _apply_d1_full_crossing(
    base: np.ndarray,
    x: np.ndarray,
    z: np.ndarray,
    result: np.ndarray,
    source: ReliefSource,
    variant: str,
) -> tuple[np.ndarray, int]:
    """Apply the p3d10 whole-ramp profiles with a full-weight road band."""
    settings = KREUZUNG_SETTINGS[variant]
    crossings = _ramp_intersection_pairs(source, "D1")
    if not crossings or (crossings[0][2], crossings[0][3]) != (2, 11):
        raise RuntimeError("Erwartete D1-Kreuzung rampe_2/rampe_11 fehlt")
    cx, cz, _, _ = crossings[0]
    crossing_m = np.array([cx, cz], dtype=np.float64) * CELL_M

    # Start from the established p3d6 surface, including its unchanged local
    # endpoint work and its old radial crossing, then transfer only the two
    # solved route profiles into it.
    p3d6_surface = result.copy()
    crossed_surface = p3d6_surface.copy()
    old_weight, _ = _apply_ramp_crossing_planes(
        base, x, z, crossed_surface, source, "D1", "2", "2",
    )
    p3d6_surface += old_weight * (crossed_surface - p3d6_surface)
    result[:] = p3d6_surface

    # The ramp polylines extend beyond D1. Those samples remain on the source
    # surface because this prototype only replaces D1/G1; use the global source
    # field there instead of clamping to D1's last mesh column/row.
    sx0, sz0, sx1, sz1 = TILE_BOUNDS["D1"]
    global_p3d6 = source.heights.astype(np.float64, copy=True)
    tile_x0, tile_z0, tile_x1, tile_z1 = sx0 * int(source.data["rs"]), sz0 * int(source.data["rs"]), sx1 * int(source.data["rs"]), sz1 * int(source.data["rs"])
    global_p3d6[tile_z0:tile_z1 + 1, tile_x0:tile_x1 + 1] = p3d6_surface

    raw_paths = source.data.get("rampenwege", [])
    rs = int(source.data["rs"])
    profiles: list[dict[str, Any]] = []
    for path_index in (2, 11):
        path = np.asarray(raw_paths[path_index], dtype=np.float64)
        stations, coords, cumulative = _profile_path(path)
        center = float(LineString(path).project(Point(cx, cz)))
        row = coords[:, 1] * rs
        col = coords[:, 0] * rs
        height = ndi.map_coordinates(global_p3d6, [row, col], order=1, mode="nearest")
        profiles.append({
            "index": path_index,
            "stations": stations,
            "coords": coords,
            "path_m": path * CELL_M,
            "cumulative": cumulative * CELL_M,
            "center": center,
            "height": height,
        })

    import os
    cache_key = (
        source.source_file_sha256,
        variant,
        os.environ.get("RELIEF_WEGEND_VAR", "1"),
    )
    solved, solver_info = _solve_full_ramp_profiles(profiles, crossing_m, variant, cache_key)

    # Rasterize a profile target on every mesh vertex in each complete corridor.
    # Its blend is exactly one through +/-1.81 m (R3 samples +/-1.5 coordinate
    # units = 1.8 m at CELL_M=1.2) and then eases into p3d6 over
    # the selected 10 m collar. The final tile mask is set to one wherever this
    # already blended value exists, avoiding a second fade in terrain_heights.
    query = np.column_stack((x.ravel() * CELL_M, z.ravel() * CELL_M))
    best_lateral = np.full(len(query), np.inf, dtype=np.float64)
    best_target = np.zeros(len(query), dtype=np.float64)
    transfer_weight = np.zeros(len(query), dtype=np.float64)
    for profile, height in zip(profiles, solved):
        coords = np.asarray(profile["coords"], dtype=np.float64)
        direction = np.gradient(coords, axis=0)
        direction /= np.maximum(np.linalg.norm(direction, axis=1, keepdims=True), 1e-9)
        normals = np.column_stack((-direction[:, 1], direction[:, 0]))
        station, lateral, inside_strip = _project_to_ramp_strip(
            query, coords, profile["stations"], normals, float(settings["band_m"]),
        )
        path_m = coords * CELL_M
        start_tangent = path_m[1] - path_m[0]
        start_tangent /= max(float(np.hypot(*start_tangent)), 1e-12)
        end_tangent = path_m[-1] - path_m[-2]
        end_tangent /= max(float(np.hypot(*end_tangent)), 1e-12)
        beyond_start = ((query - path_m[0]) @ start_tangent) < -1e-8
        beyond_end = ((query - path_m[-1]) @ end_tangent) > 1e-8
        valid_station = ~beyond_start & ~beyond_end
        road_weight = 1.0 - _smoothstep(
            float(settings["band_m"]),
            float(settings["band_m"] + settings["fade_m"]),
            np.abs(lateral),
        )
        road_weight[inside_strip] = 1.0
        road_weight *= valid_station
        target = np.interp(station / CELL_M, profile["stations"], height)
        abs_lateral = np.abs(lateral)
        # Where the two broad collars overlap, use the nearest route. Averaging
        # them would leak longitudinal slope across a road axis even though the
        # profiles agree on the shared crossing plane.
        nearest = valid_station & (abs_lateral < best_lateral)
        best_lateral[nearest] = abs_lateral[nearest]
        best_target[nearest] = target[nearest]
        transfer_weight[nearest] = road_weight[nearest]

    affected = transfer_weight > 1e-12
    radius = np.hypot(query[:, 0] - crossing_m[0], query[:, 1] - crossing_m[1])
    plane_mix = 1.0 - _smoothstep(
        float(settings["plane_inner_m"]), float(settings["plane_outer_m"]), radius,
    )
    plane_affected = plane_mix > 1e-12
    blended = affected | plane_affected
    if blended.any():
        background = p3d6_surface.ravel()
        profile_surface = background.copy()
        profile_surface[affected] = (
            background[affected] * (1.0 - transfer_weight[affected])
            + best_target[affected] * transfer_weight[affected]
        )
        plane_height = float(solver_info["crossing_plane_height_m"])
        result.ravel()[blended] = (
            profile_surface[blended] * (1.0 - plane_mix[blended])
            + plane_height * plane_mix[blended]
        )

    crossing_weight = old_weight.copy()
    crossing_weight.ravel()[blended] = 1.0
    return crossing_weight, int(np.count_nonzero(transfer_weight >= 0.999))


def _apply_ramp_crossing_planes(
    base: np.ndarray,
    x: np.ndarray,
    z: np.ndarray,
    result: np.ndarray,
    source: ReliefSource,
    tile: str,
    variant: str,
    crossing_variant: str,
    endpoint_weight: np.ndarray | None = None,
) -> tuple[np.ndarray, int]:
    settings = RAMP_PROFILE_SETTINGS[variant]
    if variant == "2" and crossing_variant in {"3", "4", "5", "8", "9", "10"}:
        if tile == "D1":
            if endpoint_weight is None:
                endpoint_weight = np.zeros(x.shape, dtype=np.float64)
            if crossing_variant in {"8", "9", "10"}:
                return _apply_d1_full_crossing(
                    base, x, z, result, source, crossing_variant,
                )
            return _apply_d1_optimized_crossing(
                base, x, z, result, source, crossing_variant, endpoint_weight,
            )
        # The new solver is scoped to D1; preserve the p3d6 G1 crossing.
        crossing_variant = "2"
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
        cross_settings = KREUZUNG_SETTINGS[crossing_variant]
        inner = float(cross_settings["inner_m"])
        half_width = float(settings["cross_half_width_m"])
        width_fade = float(settings["cross_width_fade_m"])
        core_runout = float(cross_settings.get("core_runout_m", settings["cross_core_runout_m"]))
        runout = float(cross_settings.get("runout_m", settings["cross_runout_m"]))

        for cx, cz, first, second in _ramp_intersection_pairs(source, tile):
            radial = np.hypot((x - cx) * CELL_M, (z - cz) * CELL_M)
            inside = radial <= inner
            if not inside.any():
                continue
            plane = float(np.median(base[inside]))
            plane_values = None
            crossing_weight = np.zeros(len(q), dtype=np.float64)
            point = Point(cx * CELL_M, cz * CELL_M)
            path_indices = () if cross_settings.get("radial_only", False) else (first, second)
            for path_index in path_indices:
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
            radial_weight = 1.0 - _smoothstep(
                inner, inner + float(cross_settings["radial_fade_m"]), radial.ravel(),
            )
            crossing_weight = np.maximum(crossing_weight, radial_weight)

            # The returned weight applies once in terrain_heights. Assigning the
            # shared target here keeps the feather continuous instead of
            # squaring its falloff at the corridor edge.
            target_sum += crossing_weight * (plane if plane_values is None else plane_values)
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
    import os
    endpoint_variant = os.environ.get("RELIEF_WEGEND_VAR", "1")
    crossing_variant = os.environ.get("RELIEF_KREUZUNG_VAR", "10")
    if endpoint_variant not in WEGENDE_VARIANTS:
        raise ValueError(f"RELIEF_WEGEND_VAR muss einer von {sorted(WEGENDE_VARIANTS)} sein")
    if crossing_variant not in KREUZUNG_VARIANTS:
        raise ValueError(f"RELIEF_KREUZUNG_VAR muss einer von {sorted(KREUZUNG_VARIANTS)} sein")
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

    endpoint_weight = np.zeros(xx.shape, dtype=np.float64)
    endpoint_count = 0
    if variant == "2" and endpoint_variant != "0":
        result, endpoint_weight, endpoint_count = _apply_ramp_endpoint_runouts(
            source, tile, xx, zz, result, endpoint_variant,
        )
        if endpoint_count:
            layers.append("rampenenden_lokaler_auslauf_ge4m_weich")

    crossing_weight, ramp_crossings = _apply_ramp_crossing_planes(
        base, xx, zz, result, source, tile, variant, crossing_variant,
        endpoint_weight=endpoint_weight,
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
    weight = tile_weight * np.maximum.reduce((wall_weight, ramp_weight, crossing_weight, endpoint_weight))
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
        "endpoint_variant": endpoint_variant,
        "endpoint_runout_vertices": endpoint_count,
        "crossing_variant": crossing_variant,
        "zone_flat_vertices": zone_count,
    }
    if tile == "D1" and crossing_variant in {"8", "9", "10"}:
        cache_key = (
            source.source_file_sha256,
            crossing_variant,
            endpoint_variant,
        )
        if cache_key in _FULL_CROSSING_CACHE:
            info["profile_solver"] = dict(_FULL_CROSSING_CACHE[cache_key][1])
    return result.astype("<f4"), info
