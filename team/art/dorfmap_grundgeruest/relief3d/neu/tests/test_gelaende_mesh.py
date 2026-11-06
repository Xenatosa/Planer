from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from neu.mesh import TILE_BOUNDS, build_manifest, load_relief, terrain_heights


RELIEF3D = Path(__file__).resolve().parents[2]


def _inputs():
    source = load_relief(RELIEF3D / "relief_daten.json.gz")
    vector = json.loads((RELIEF3D / "neu" / "vektor.json").read_text(encoding="utf-8"))
    with np.load(RELIEF3D / "neu" / "felder.npz", allow_pickle=False) as archive:
        fields = {name: archive[name] for name in archive.files}
    return source, vector, fields


def test_profile_mesh_changes_only_d1_and_g1_and_preserves_cliff_and_tile_edges():
    source, vector, fields = _inputs()
    for tile in ("D1", "G1"):
        candidate, stats = terrain_heights(source, tile, vector, fields, "1")
        x0, z0, x1, z1 = TILE_BOUNDS[tile]
        rs = int(source.data["rs"])
        base = source.heights[z0 * rs : z1 * rs + 1, x0 * rs : x1 * rs + 1]
        delta = candidate - base
        assert stats["changed_vertices"] > 0
        assert stats["max_abs_delta_m"] <= 0.1
        assert np.array_equal(candidate[[0, -1], :], base[[0, -1], :])
        assert np.array_equal(candidate[:, [0, -1]], base[:, [0, -1]])

    d1, _ = terrain_heights(source, "D1", vector, fields, "1")
    # The specified cliff control point remains at exactly the visible GB value.
    point = d1[35 * 2, (140 - 126) * 2]
    assert point.tobytes() == source.heights[35 * 2, 140 * 2].tobytes()

    d2, stats = terrain_heights(source, "D2", vector, fields, "1")
    expected = source.heights[43 * 2 : 86 * 2 + 1, 126 * 2 : 168 * 2 + 1]
    assert stats["changed_vertices"] == 0
    assert d2.tobytes() == expected.tobytes()


def test_control_variant_is_source_locked():
    source, vector, fields = _inputs()
    for tile in ("D1", "G1", "D2"):
        candidate, stats = terrain_heights(source, tile, vector, fields, "0")
        x0, z0, x1, z1 = TILE_BOUNDS[tile]
        rs = int(source.data["rs"])
        expected = source.heights[z0 * rs : z1 * rs + 1, x0 * rs : x1 * rs + 1]
        assert candidate.tobytes() == expected.tobytes()
        assert stats["changed_vertices"] == 0


def test_default_variant_is_source_locked(monkeypatch):
    monkeypatch.delenv("RELIEF_GELAENDE_VAR", raising=False)
    manifest = build_manifest(
        RELIEF3D / "relief_daten.json.gz",
        RELIEF3D / "zellen_relief.csv",
        RELIEF3D / "neu" / "vektor.json",
        RELIEF3D / "neu" / "felder.npz",
    )
    assert manifest["terrain_variant"] == "0"
    assert all(manifest["terrain"][tile]["changed_vertices"] == 0 for tile in ("D1", "G1", "D2"))


def test_damped_variant_is_weaker_than_full_profiles():
    source, vector, fields = _inputs()
    for tile in ("D1", "G1"):
        full, full_stats = terrain_heights(source, tile, vector, fields, "1")
        damped, damped_stats = terrain_heights(source, tile, vector, fields, "2")
        assert full_stats["changed_vertices"] > 0
        assert damped_stats["changed_vertices"] > 0
        assert damped_stats["max_abs_delta_m"] < full_stats["max_abs_delta_m"]
        assert np.max(np.abs(damped - source.heights[
            TILE_BOUNDS[tile][1] * 2 : TILE_BOUNDS[tile][3] * 2 + 1,
            TILE_BOUNDS[tile][0] * 2 : TILE_BOUNDS[tile][2] * 2 + 1,
        ])) < full_stats["max_abs_delta_m"]
