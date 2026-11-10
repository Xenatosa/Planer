import json
from pathlib import Path

from neu.baue_html import build
from neu.gen_relief import SOURCE, LEGACY, build as build_data


def test_html_builder_emits_offline_review_page(tmp_path):
    data_path = tmp_path / "prototyp.json"
    html_path = tmp_path / "index.html"
    build_data(SOURCE, LEGACY, data_path)
    rendered = build(data_path, html_path)
    assert html_path.read_text(encoding="utf-8") == rendered
    assert "D1 · source_cell_centres_mean_at_vertices" in rendered
    assert "D2 · locked_legacy_reference" in rendered
    assert "G1 · source_cell_centres_mean_at_vertices" in rendered
    assert "GB SHA-256" in rendered
    assert '<script src=' not in rendered
