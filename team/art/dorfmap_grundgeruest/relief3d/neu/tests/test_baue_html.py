from pathlib import Path

from neu import baue_viewer


def test_mesh_viewer_builder_emits_offline_page_from_current_package(tmp_path, monkeypatch):
    root = tmp_path / "relief3d"
    output = root / "neu"
    output.mkdir(parents=True)
    data = output / "relief_neu.json.gz"
    data.write_bytes(b"deterministic mesh package")
    monkeypatch.setattr(baue_viewer, "ROOT", root)

    def fake_esbuild(args, *, cwd, env, check):
        assert cwd == root
        assert check is True
        bundle_arg = next(arg for arg in args if arg.startswith("--outfile="))
        Path(bundle_arg.removeprefix("--outfile=")).write_text(
            "window.RELIEF_NEU_VIEWER=1; window.drawNeuMeshTiles();",
            encoding="utf-8",
        )

    monkeypatch.setattr(baue_viewer.subprocess, "run", fake_esbuild)
    baue_viewer.run()

    root_html = (root / "index.html").read_text(encoding="utf-8")
    neu_html = (output / "index.html").read_text(encoding="utf-8")
    assert root_html == neu_html
    assert 'data-core="relief-neu-mesh"' in root_html
    assert "window.NEU_GZ=\"ZGV0ZXJtaW5pc3RpYyBtZXNoIHBhY2thZ2U=\"" in root_html
    assert "window.drawNeuMeshTiles()" in root_html
    assert '<script src=' not in root_html
