from __future__ import annotations

import base64
from pathlib import Path

import numpy as np

from neu.wand import build_wall_manifest


ROOT = Path(__file__).resolve().parents[2]


def test_wall_meshes_are_deterministic_profiled_and_exclude_d2():
    source = ROOT / "neu" / "vektor.json"
    a = build_wall_manifest(source, variant=1)
    b = build_wall_manifest(source, variant=1)
    assert a == b
    assert a["tiles"]["D1"]["triangles"] > 0
    assert a["tiles"]["G1"]["triangles"] > 0
    assert a["tiles"]["D2"]["triangles"] == 0
    for tile in ("D1", "G1"):
        wall = a["tiles"][tile]
        points = np.frombuffer(base64.b64decode(wall["vertices_xyz_f32"]), dtype="<f4")
        indices = np.frombuffer(base64.b64decode(wall["indices_u32"]), dtype="<u4")
        assert points.size == wall["vertices"] * 3
        assert indices.size // 3 == wall["triangles"]
        assert np.isfinite(points).all()
        assert wall["min_width_m"] >= 1.2


def test_wall_variant_is_explicit_and_keeps_d2_empty():
    source = ROOT / "neu" / "vektor.json"
    narrow = build_wall_manifest(source, variant=1)
    wide = build_wall_manifest(source, variant=0)
    assert wide["tiles"]["D1"]["min_width_m"] >= narrow["tiles"]["D1"]["min_width_m"]
    assert wide["tiles"]["D2"]["triangles"] == narrow["tiles"]["D2"]["triangles"] == 0
