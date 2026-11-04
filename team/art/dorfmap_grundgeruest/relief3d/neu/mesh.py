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


def tile_mesh(source: ReliefSource, tile: str) -> tuple[np.ndarray, np.ndarray]:
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
    slab = source.heights[sz0 : sz1 + 1, sx0 : sx1 + 1]
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


def _b64(array: np.ndarray) -> str:
    return base64.b64encode(array.tobytes(order="C")).decode("ascii")


def build_manifest(relief_path: Path, cells_csv: Path) -> dict[str, Any]:
    source = load_relief(relief_path)
    tiles: dict[str, Any] = {}
    for tile in ("D2", "G1", "D1"):
        positions, indices = tile_mesh(source, tile)
        tiles[tile] = {
            "bounds": list(TILE_BOUNDS[tile]),
            "vertices_xyz_f32": _b64(positions),
            "indices_u32": _b64(indices),
            "vertices": int(len(positions)),
            "triangles": int(len(indices) // 3),
            "height_sha256": hashlib.sha256(positions[:, 1].tobytes()).hexdigest(),
            "mesh_sha256": hashlib.sha256(positions.tobytes() + indices.tobytes()).hexdigest(),
        }
    return {
        "format": "relief-neu-tile-mesh-v1",
        "sampling_m": 1.0 / int(source.data["rs"]),
        "source_relief_sha256": source.source_file_sha256,
        "source_cell_columns": list(SOURCE_COLUMNS),
        "source_cell_column_sha256": source_column_hashes(cells_csv),
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
