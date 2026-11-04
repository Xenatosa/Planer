"""Opt-in entry point for the new tiled mesh prototype."""

from pathlib import Path
import gzip
import json

from .mesh import build_manifest, load_relief


ROOT = Path(__file__).resolve().parent.parent


def build() -> None:
    input_path = ROOT / "relief_daten.json.gz"
    csv_path = ROOT / "zellen_relief.csv"
    output = ROOT / "neu" / "relief_neu.json.gz"
    source = load_relief(input_path)
    manifest = build_manifest(input_path, csv_path)
    # The viewer receives the exact original scene payload plus an opt-in,
    # independently triangulated tile set. It ignores the extra key until a
    # later renderer consumes it, so the shared scene (and D2) stays byte exact.
    package = dict(source.data)
    package["neu_mesh_tiles"] = manifest
    payload = json.dumps(package, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(gzip.compress(payload, compresslevel=9, mtime=0))
    report = {
        "output": str(output.relative_to(ROOT)),
        "tiles": {
            name: {"vertices": tile["vertices"], "triangles": tile["triangles"], "height_sha256": tile["height_sha256"]}
            for name, tile in manifest["tiles"].items()
        },
        "source_columns": list(manifest["source_cell_columns"]),
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
