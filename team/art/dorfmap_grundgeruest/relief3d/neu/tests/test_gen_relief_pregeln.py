import json

import numpy as np

from neu import felder


def test_build_fields_keeps_inside_sign_and_writes_deterministically(tmp_path, monkeypatch):
    mask = np.zeros((felder.NY, felder.NX), dtype=bool)
    mask[40:44, 70:75] = True
    vector = {
        "wegmaske": mask,
        "kreuzungsmaske": mask.copy(),
        "wandmaske": mask.copy(),
        "wassermaske": mask.copy(),
        "bauzone_bestand": mask.copy(),
        "bauzone_plan": mask.copy(),
    }
    monkeypatch.setattr(felder, "OUT", tmp_path)
    monkeypatch.setattr(felder, "build", lambda: vector)

    first_fields = felder.build_fields()
    first_package = (tmp_path / "felder.npz").read_bytes()
    first_metadata = (tmp_path / "felder.json").read_bytes()
    second_fields = felder.build_fields()
    second_package = (tmp_path / "felder.npz").read_bytes()
    second_metadata = (tmp_path / "felder.json").read_bytes()

    assert first_package == second_package
    assert first_metadata == second_metadata
    assert set(first_fields) == {
        "weg", "kreuzung", "wand", "wasser", "bauzone_bestand", "bauzone_plan",
    }
    metadata = json.loads(first_metadata)
    assert metadata["shape"] == [felder.NY, felder.NX]
    assert metadata["innen"] == "negativ"
    for name in first_fields:
        values = first_fields[name]
        assert values.dtype == np.float32
        assert values.shape == (felder.NY, felder.NX)
        assert np.array_equal(values, second_fields[name])
        assert np.all(values[mask] < 0)
        assert np.isclose(values[40, 69], felder.CELL_M)
        assert np.all(values[~mask] > 0)
    with np.load(tmp_path / "felder.npz", allow_pickle=False) as saved:
        for name, values in first_fields.items():
            assert np.array_equal(saved[name], values)
