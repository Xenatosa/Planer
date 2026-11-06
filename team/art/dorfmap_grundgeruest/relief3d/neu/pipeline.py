"""Opt-in entry point for the new tiled mesh prototype."""

from pathlib import Path
import gzip
import json

from .mesh import TILE_BOUNDS, build_manifest, load_relief
from .wand import build_wall_manifest


ROOT = Path(__file__).resolve().parent.parent


def build() -> dict:
    input_path = ROOT / "relief_daten.json.gz"
    # The neu/ sidecar is copied byte-for-byte from raster_c20_z25_zellen.csv
    # by gen_relief.py; use it for both source-column hashes and D1/G1 heights.
    csv_path = ROOT / "neu" / "zellen_relief.csv"
    output = ROOT / "neu" / "relief_neu.json.gz"
    source = load_relief(input_path)
    manifest = build_manifest(input_path, csv_path)
    manifest["waende"] = build_wall_manifest(ROOT / "neu" / "vektor.json")
    # LOD1 currently uses the deterministic 0.5 m tile samples. Each tile is a
    # closed solid in the viewer (top, sides, bottom); wall solids are additional.
    terrain_triangles = 0
    for tile, (x0, z0, x1, z1) in TILE_BOUNDS.items():
        tile_rs = manifest["tiles"][tile]["samples_per_m"]
        cols, rows = (x1 - x0) * tile_rs, (z1 - z0) * tile_rs
        top = manifest["tiles"][tile]["triangles"]
        side = 2 * 2 * (cols + rows)
        closed = top * 2 + side
        manifest["tiles"][tile]["closed_triangles"] = closed
        terrain_triangles += closed
    wall_triangles = sum(t["triangles"] for t in manifest["waende"]["tiles"].values())
    manifest["lod1"] = {
        "sampling_m": min(tile["sampling_m"] for tile in manifest["tiles"].values()),
        "sampling_m_by_tile": {name: tile["sampling_m"] for name, tile in manifest["tiles"].items()},
        "terrain_closed_triangles": terrain_triangles,
        "wall_triangles": wall_triangles,
        "total_triangles": terrain_triangles + wall_triangles,
        "budget_triangles": 1_300_000,
    }
    if manifest["lod1"]["total_triangles"] >= manifest["lod1"]["budget_triangles"]:
        raise ValueError(f"LOD1-Dreiecksbudget ueberschritten: {manifest['lod1']['total_triangles']}")
    # Keep the original relief payload unchanged and attach the opt-in mesh
    # manifest for the new standalone viewer.
    package = dict(source.data)
    package["neu_mesh_tiles"] = manifest
    payload = json.dumps(package, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(gzip.compress(payload, compresslevel=9, mtime=0))
    report = {
        "output": str(output.relative_to(ROOT)),
        "tiles": {
            name: {"vertices": tile["vertices"], "triangles": tile["triangles"],
                   "closed_triangles": tile["closed_triangles"], "height_sha256": tile["height_sha256"]}
            for name, tile in manifest["tiles"].items()
        },
        "waende": {
            "variant": manifest["waende"]["variant"],
            "tiles": {name: {"vertices": tile["vertices"], "triangles": tile["triangles"],
                             "features": tile["features"], "min_width_m": tile["min_width_m"]}
                      for name, tile in manifest["waende"]["tiles"].items()},
        },
        "lod1": manifest["lod1"],
        "source_columns": list(manifest["source_cell_columns"]),
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return report
