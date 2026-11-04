import base64
import csv
import gzip
import hashlib
import json
import struct
from pathlib import Path

from neu.gen_relief import SOURCE_COLUMNS, build


RELIEF3D = Path(__file__).resolve().parents[2]
MAP_ROOT = RELIEF3D.parent
SOURCE = MAP_ROOT / "raster_c20_z25_zellen.csv"
LEGACY = RELIEF3D / "relief_daten.json.gz"


def _expected_source_rows(tile="D2"):
    ix, iz = "ABCDEFGH".index(tile[0]), int(tile[1]) - 1
    x0, x1, z0, z1 = ix * 42, ix * 42 + 42, iz * 43, iz * 43 + 43
    with SOURCE.open(newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if x0 <= int(r["cx"]) < x1 and z0 <= int(r["cy"]) < z1]
    rows.sort(key=lambda r: (int(r["cy"]), int(r["cx"])))
    return rows


def _crop_f32(raw, nx, ny, rs, x0, x1, z0, z1):
    width = nx * rs + 1
    grid = memoryview(raw)
    chunks = []
    stride = width * 4
    for y in range(z0 * rs, z1 * rs + 1):
        start = y * stride + x0 * rs * 4
        chunks.append(bytes(grid[start : start + ((x1 - x0) * rs + 1) * 4]))
    return b"".join(chunks)


def test_build_is_deterministic_and_keeps_d2_source_and_display_bytes(tmp_path):
    first, second = tmp_path / "a.json", tmp_path / "b.json"
    d = build(SOURCE, LEGACY, first)
    build(SOURCE, LEGACY, second)
    assert first.read_bytes() == second.read_bytes()
    assert [t["tile"] for t in d["tiles"]] == ["D1", "D2", "G1"]
    assert d["lod1_triangle_estimate"] < 1_300_000

    d2 = d["tiles"][1]
    source_rows = _expected_source_rows()
    assert len(source_rows) == len(d2["cells"]) == 42 * 43
    for src, cell in zip(source_rows, d2["cells"]):
        assert all(src[k] == cell[k] for k in SOURCE_COLUMNS)

    legacy = json.load(gzip.open(LEGACY, "rt", encoding="utf-8"))
    expected = _crop_f32(base64.b64decode(legacy["GB"]), legacy["nx"], legacy["ny"], legacy["rs"], 126, 168, 43, 86)
    actual = base64.b64decode(d2["display_fields"]["GB"]["bytes_b64"])
    assert actual == expected
    assert hashlib.sha256(actual).hexdigest() == d2["display_fields"]["GB"]["sha256"]

    colors = base64.b64decode(legacy["VC"])
    width, height = legacy["nx"] * legacy["rs"] + 1, legacy["ny"] * legacy["rs"] + 1
    expected_colors = b"".join(
        colors[(y * width + 252) * 3 : (y * width + 337) * 3]
        for y in range(86, 173)
    )
    actual_colors = base64.b64decode(d2["display_fields"]["VC"]["bytes_b64"])
    assert actual_colors == expected_colors
    assert len(struct.unpack("<" + "f" * 43 * 44, base64.b64decode(d["tiles"][0]["height_f32_le_b64"]))) == 43 * 44
