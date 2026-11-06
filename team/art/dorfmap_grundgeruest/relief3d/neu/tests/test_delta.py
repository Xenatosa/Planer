import json

from neu.delta import compare, markdown


def save(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


def test_delta_reports_rule_and_image_increases(tmp_path):
    before, after = tmp_path / "vor", tmp_path / "nach"
    before.mkdir(); after.mkdir()
    for directory, n in ((before, 1), (after, 2)):
        save(directory / "regeln.json", {"treffer": [{"regel": "R5_loch", "feld": "D1"}] * n})
        save(directory / "r8.json", {"je_feld": {"D1": {"R8_stufe": 0}}})
        save(directory / "r9.json", {"je_feld": {"D2": {"R9w_wellen": 1}}})
        save(directory / "loch.json", {"offen_innen": 0, "punkte": []})
        save(directory / "nahbild_werte.json", {"images": [{"tile": "D1", "mode": "clay", "camera": "draufsicht", "kantenzaehne": n}]})
    result = compare(before, after)
    assert result["exit_code"] == 1
    assert any(row["gruppe"] == "regeln" and row["delta"] == 1 for row in result["anstiege"])
    assert any(row["metrik"] == "kantenzaehne" for row in result["anstiege"])
    assert "| Regeln |" not in markdown(result, "vor", "nach")


def test_delta_is_zero_without_increases(tmp_path):
    before, after = tmp_path / "vor", tmp_path / "nach"
    before.mkdir(); after.mkdir()
    for directory in (before, after):
        save(directory / "regeln.json", {"treffer": []})
        save(directory / "r8.json", {"je_feld": {"D2": {"R8_stufe": 0}}})
        save(directory / "r9.json", {"je_feld": {}})
        save(directory / "loch.json", {"offen_innen": 0, "punkte": []})
        save(directory / "nahbild_werte.json", {"images": []})
    assert compare(before, after)["exit_code"] == 0
