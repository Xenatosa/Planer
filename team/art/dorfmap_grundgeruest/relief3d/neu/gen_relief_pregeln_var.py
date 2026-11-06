#!/usr/bin/env python3
"""Build a source-driven D1/G1 prototype and a read-only D2 reference payload.

The legacy files are inputs only. This prototype writes to RELIEF_NEU_DIR (by
default /tmp/relief_neu_pregeln), never to relief_daten.json.gz or zellen_relief.csv.
"""
from __future__ import annotations

import base64
import csv
import gzip
import hashlib
import json
import os
import struct
from pathlib import Path


HERE = Path(__file__).resolve().parent
RELIEF3D = HERE.parent
MAP_ROOT = RELIEF3D.parent
SOURCE = MAP_ROOT / "raster_c20_z25_zellen.csv"
LEGACY = RELIEF3D / "relief_daten.json.gz"
SOURCE_COLUMNS = (
    "untergrund", "hindernis_id", "hindernis_art", "wasser_eis", "ebene",
    "bauzone_bestand", "bauzone_plan", "begehbar", "bebaubar",
)
TILES = ("D1", "D2", "G1")
TILE_LETTERS = "ABCDEFGH"


def bounds(tile: str, nx: int, ny: int) -> tuple[int, int, int, int]:
    ix, iz = TILE_LETTERS.index(tile[0]), int(tile[1]) - 1
    x0, z0 = ix * 42, iz * 43
    return x0, min(nx, x0 + 42), z0, min(ny, z0 + 43)


def source_cells(path: Path) -> tuple[list[dict[str, str]], int, int]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"leere Kartenquelle: {path}")
    nx = max(int(r["cx"]) for r in rows) + 1
    ny = max(int(r["cy"]) for r in rows) + 1
    if len(rows) != nx * ny or len({(r["cx"], r["cy"]) for r in rows}) != len(rows):
        raise ValueError("Kartenquelle muss ein lueckenloses, eindeutiges Zellraster enthalten")
    return rows, nx, ny


def crop_bytes(raw: bytes, nx: int, ny: int, rs: int, tile: str, channels: int, itemsize: int) -> tuple[bytes, int, int]:
    x0, x1, z0, z1 = bounds(tile, nx, ny)
    source_width, source_height = nx * rs + 1, ny * rs + 1
    expected = source_width * source_height * channels * itemsize
    if len(raw) != expected:
        raise ValueError(f"Feldlaenge unerwartet: {len(raw)} statt {expected}")
    stride = source_width * channels * itemsize
    row_size = (x1 - x0) * rs * channels * itemsize
    chunks = []
    for y in range(z0 * rs, z1 * rs + 1):
        start = y * stride + x0 * rs * channels * itemsize
        chunks.append(raw[start : start + row_size + channels * itemsize])
    return b"".join(chunks), (x1 - x0) * rs + 1, (z1 - z0) * rs + 1


def source_tile(rows: list[dict[str, str]], tile: str, nx: int, ny: int) -> list[dict[str, str]]:
    x0, x1, z0, z1 = bounds(tile, nx, ny)
    selected = [r for r in rows if x0 <= int(r["cx"]) < x1 and z0 <= int(r["cy"]) < z1]
    selected.sort(key=lambda r: (int(r["cy"]), int(r["cx"])))
    cells = [{
        "cx": r["cx"], "cy": r["cy"],
        **{k: r[k] for k in SOURCE_COLUMNS},
        "hoehe_m": r["hoehe_m"],
        "skin_slot": r["skin_slot"],
    } for r in selected]
    return cells


def canonical_hash(value: object) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def source_height_grid(cells: list[dict[str, str]], tile: str, nx: int, ny: int) -> tuple[bytes, int, int]:
    x0, x1, z0, z1 = bounds(tile, nx, ny)
    width, height = x1 - x0, z1 - z0
    heights = {(int(c["cx"]) - x0, int(c["cy"]) - z0): float(c["hoehe_m"]) for c in cells}
    values = []
    for vz in range(height + 1):
        for vx in range(width + 1):
            samples = [
                heights[(cx, cz)]
                for cz in (vz - 1, vz)
                for cx in (vx - 1, vx)
                if 0 <= cx < width and 0 <= cz < height
            ]
            values.append(sum(samples) / len(samples))
    return struct.pack(f"<{len(values)}f", *values), width + 1, height + 1


def build(source_path: Path, legacy_path: Path, output_path: Path) -> dict:
    rows, nx, ny = source_cells(source_path)
    if nx != 336 or ny != 303:
        raise ValueError(f"unerwartete Kartenabmessung {nx}x{ny}")
    with gzip.open(legacy_path, "rt", encoding="utf-8") as f:
        legacy = json.load(f)
    if (int(legacy["nx"]), int(legacy["ny"])) != (nx, ny):
        raise ValueError("Relief-Referenz und Kartenquelle haben verschiedene Abmessungen")
    rs = int(legacy["rs"])

    legacy_specs = {
        "GB": (1, 4, "float32-le"),
        "VC": (3, 1, "uint8"),
        "WV": (1, 4, "float32-le"),
        "WEGA": (1, 1, "uint8"),
    }
    legacy_raw = {key: base64.b64decode(legacy[key]) for key in legacy_specs}
    tiles = []
    for name in TILES:
        x0, x1, z0, z1 = bounds(name, nx, ny)
        cells = source_tile(rows, name, nx, ny)
        if len(cells) != (x1 - x0) * (z1 - z0):
            raise ValueError(f"unvollstaendige Quellzellen in {name}")
        entry = {
            "tile": name,
            "cell_bounds_xyxy_inclusive_exclusive": [x0, z0, x1, z1],
            "cells": cells,
            "source_cells_sha256": canonical_hash(cells),
        }
        if name == "D2":
            fields = {}
            for key, (channels, itemsize, dtype) in legacy_specs.items():
                raw, width, height = crop_bytes(legacy_raw[key], nx, ny, rs, name, channels, itemsize)
                fields[key] = {
                    "dtype": dtype,
                    "channels": channels,
                    "width": width,
                    "height": height,
                    "bytes_b64": base64.b64encode(raw).decode("ascii"),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                }
            entry.update({
                "mode": "locked_legacy_reference",
                "grid_spacing_m": 1 / rs,
                "display_fields": fields,
                "lod1_triangles": sum((v["width"] - 1) * (v["height"] - 1) * 2 for v in [fields["GB"]]),
            })
        else:
            raw, width, height = source_height_grid(cells, name, nx, ny)
            entry.update({
                "mode": "source_cell_centres_mean_at_vertices",
                "grid_spacing_m": 1.0,
                "height_dtype": "float32-le",
                "height_width": width,
                "height_height": height,
                "height_f32_le_b64": base64.b64encode(raw).decode("ascii"),
                "height_sha256": hashlib.sha256(raw).hexdigest(),
                "lod1_triangles": (width - 1) * (height - 1) * 2,
            })
        tiles.append(entry)

    result = {
        "schema": "relief-neu-prototyp-v1",
        "source": {
            "cells": "../raster_c20_z25_zellen.csv",
            "source_columns": list(SOURCE_COLUMNS),
            "source_rows": len(rows),
            "source_file_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "tile_formula": "ABCDEFGH[cx//42] + str(cy//43+1)",
        },
        "tiles": tiles,
        "lod1_triangle_estimate": sum(t["lod1_triangles"] for t in tiles),
        "scope": "D1/G1 are new source-derived terrain-only tiles; D2 is a frozen GB/VC/WV/WEGA reference payload. No legacy output is rewritten.",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return result


def main() -> int:
    out_dir = Path(os.environ.get("RELIEF_NEU_DIR", "/tmp/relief_neu_pregeln"))
    source = Path(os.environ.get("RELIEF_NEU_SOURCE", str(SOURCE)))
    legacy = Path(os.environ.get("RELIEF_NEU_D2_REFERENCE", str(LEGACY)))
    result = build(source, legacy, out_dir / "prototyp.json")
    print(json.dumps({"output": str(out_dir / "prototyp.json"), "tiles": [t["tile"] for t in result["tiles"]],
                      "lod1_triangles_estimate": result["lod1_triangle_estimate"]}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
