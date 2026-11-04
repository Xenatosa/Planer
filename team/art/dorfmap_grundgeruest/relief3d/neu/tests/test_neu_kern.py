from __future__ import annotations

import gzip
import json
import shutil
from pathlib import Path

from neu.mesh import (
    SOURCE_COLUMNS,
    load_relief,
    mesh_height_bytes,
    source_column_hashes,
    tile_mesh,
)
from neu.pipeline import build


RELIEF3D = Path(__file__).resolve().parents[2]


def test_mesh_tiles_are_deterministic_and_below_triangle_budget(tmp_path: Path) -> None:
    source = load_relief(RELIEF3D / "relief_daten.json.gz")
    expected_triangles = {"D2": 14_448, "G1": 14_448, "D1": 14_448}
    for tile, count in expected_triangles.items():
        p0, i0 = tile_mesh(source, tile)
        p1, i1 = tile_mesh(source, tile)
        assert p0.tobytes() == p1.tobytes()
        assert i0.tobytes() == i1.tobytes()
        assert len(i0) // 3 == count
    assert sum(expected_triangles.values()) < 1_300_000


def test_d2_height_vertices_are_the_unmodified_source_bytes() -> None:
    source = load_relief(RELIEF3D / "relief_daten.json.gz")
    x0, z0, x1, z1 = 126, 43, 168, 86
    rs = int(source.data["rs"])
    expected = source.heights[z0 * rs : z1 * rs + 1, x0 * rs : x1 * rs + 1].ravel().tobytes()
    assert mesh_height_bytes(source, "D2") == expected
    assert len(expected) == (42 * rs + 1) * (43 * rs + 1) * 4


def test_source_cell_columns_have_stable_byte_hashes() -> None:
    hashes = source_column_hashes(RELIEF3D / "zellen_relief.csv")
    assert tuple(hashes) == SOURCE_COLUMNS
    assert len(hashes) == 9
    assert all(len(value) == 64 for value in hashes.values())


def test_opt_in_pipeline_writes_a_deterministic_read_only_package(tmp_path: Path, monkeypatch) -> None:
    import neu.pipeline as pipeline

    fixture_root = tmp_path / "relief3d"
    (fixture_root / "neu").mkdir(parents=True)
    shutil.copyfile(RELIEF3D / "relief_daten.json.gz", fixture_root / "relief_daten.json.gz")
    shutil.copyfile(RELIEF3D / "zellen_relief.csv", fixture_root / "zellen_relief.csv")
    before = (fixture_root / "zellen_relief.csv").read_bytes()
    monkeypatch.setattr(pipeline, "ROOT", fixture_root)
    pipeline.build()
    out = fixture_root / "neu" / "relief_neu.json.gz"
    run_a = out.read_bytes()
    package = json.loads(gzip.decompress(run_a))
    original = json.loads(gzip.decompress((fixture_root / "relief_daten.json.gz").read_bytes()))
    pipeline.build()
    assert out.read_bytes() == run_a
    assert (fixture_root / "zellen_relief.csv").read_bytes() == before
    assert {key: value for key, value in package.items() if key != "neu_mesh_tiles"} == original
    assert package["neu_mesh_tiles"]["tiles"]["D2"]["height_sha256"]
    assert build is pipeline.build
