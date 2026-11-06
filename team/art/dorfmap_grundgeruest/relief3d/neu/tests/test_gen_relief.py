import gzip
import json

import numpy as np

from neu.gen_relief import SOURCE_COLUMNS, build
from neu.tests.helpers import make_data


def load(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def test_selected_tile_rebuild_preserves_sources_and_d2(tmp_path):
    source_path = tmp_path / "source.json.gz"
    before = make_data(source_path)
    out = tmp_path / "candidate"
    summary = build(source_path, out, "1")
    after = load(out / "relief_daten_neu.json.gz")
    assert summary["quellspalten_diff_summe"] == 0
    assert all(summary["quellspalten_diff_werte"][key] == 0 for key in SOURCE_COLUMNS)
    assert all(summary["D2_anzeige_bytegleich"].values())
    assert np.array_equal(np.frombuffer(__import__("base64").b64decode(before["G"]), np.float32),
                          np.frombuffer(__import__("base64").b64decode(after["G"]), np.float32))
    assert summary["geaenderte_gb_punkte"] > 0
    assert after["relief_neu"]["kacheln"] == ["D1", "G1", "D2"]


def test_candidate_is_byte_deterministic(tmp_path):
    source_path = tmp_path / "source.json.gz"
    make_data(source_path)
    a, b = tmp_path / "a", tmp_path / "b"
    build(source_path, a, "1")
    build(source_path, b, "1")
    assert (a / "relief_daten_neu.json.gz").read_bytes() == (b / "relief_daten_neu.json.gz").read_bytes()
