import base64
import hashlib
import json
from pathlib import Path

import numpy as np

from neu.mesh import build_manifest, load_relief, mesh_height_bytes, source_column_hashes


RELIEF3D = Path(__file__).resolve().parents[2]


def test_mesh_manifest_is_deterministic_and_keeps_sources_and_d2_locked():
    relief = RELIEF3D / "relief_daten.json.gz"
    cells = RELIEF3D / "neu" / "zellen_relief.csv"
    vector = RELIEF3D / "neu" / "vektor.json"
    fields = RELIEF3D / "neu" / "felder.npz"

    first = build_manifest(relief, cells, vector, fields, variant="2")
    second = build_manifest(relief, cells, vector, fields, variant="2")
    encode = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    assert encode(first) == encode(second)
    assert tuple(first["tiles"]) == ("D2", "G1", "D1")
    assert first["source_cell_column_sha256"] == source_column_hashes(cells)
    assert set(first["source_cell_columns"]) == {
        "untergrund", "hindernis_id", "hindernis_art", "wasser_eis", "ebene",
        "bauzone_bestand", "bauzone_plan", "begehbar", "bebaubar",
    }

    source = load_relief(relief)
    d2 = np.frombuffer(
        base64.b64decode(first["tiles"]["D2"]["vertices_xyz_f32"]), dtype="<f4",
    ).reshape(-1, 3)[:, 1]
    expected_d2 = mesh_height_bytes(source, "D2")
    assert d2.tobytes() == expected_d2
    assert first["tiles"]["D2"]["height_sha256"] == hashlib.sha256(expected_d2).hexdigest()


def test_mesh_source_hashes_cover_unchanged_cell_columns():
    hashes = source_column_hashes(RELIEF3D / "neu" / "zellen_relief.csv")
    assert len(hashes) == 9
    assert all(len(value) == 64 for value in hashes.values())
