import importlib.util
import json
from pathlib import Path


RELIEF3D = Path(__file__).resolve().parents[2]
SCRIPT = RELIEF3D / "pruefung" / "regelmessung.py"
MAP_ROOT = RELIEF3D.parent


def _load_module():
    spec = importlib.util.spec_from_file_location("regelmessung", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_source_map_measurement_counts_and_repeatability():
    m = _load_module()
    args = (MAP_ROOT / "raster_c20_z25_zellen.csv", MAP_ROOT / "pruefung/quelle_plaetze_wachstum_ausbau_planm.json", RELIEF3D / "relief_daten.json.gz")
    a = m.measure(*args)
    b = m.measure(*args)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["quelle"]["rows"] == 336 * 303
    assert a["elemente"]["wald_boden"]["source_cells"] == 11217
    assert a["elemente"]["gebaeude_platzhalter"]["E40_plan_polygons"] == 233
    assert a["elemente"]["fels"]["eligible_placement_cells_deko_fels_ok"] == 62391
    assert a["elemente"]["gebirge"]["named_wall_bands"]["Nord"]["source_cells"] == 6661
