import gzip
import json

from neu.nahbild import camera_list
from neu.tests.helpers import make_data


def test_camera_set_has_six_fixed_anchors_per_tile(tmp_path):
    source = tmp_path / "source.json.gz"
    expected = make_data(source)
    cameras = camera_list(expected, ("D1", "G1", "D2"))
    assert len(cameras) == 18
    assert len({camera["n"] for camera in cameras}) == 18
    for tile in ("D1", "G1", "D2"):
        chosen = [camera for camera in cameras if camera["n"].startswith(tile + "_")]
        assert len(chosen) == 6
        assert {camera["n"].split("_", 1)[1] for camera in chosen} == {
            "draufsicht", "streiflicht_west", "streiflicht_ost", "kreuzung", "wegende", "wandfuss"
        }
    west = next(camera for camera in cameras if camera["n"] == "D1_streiflicht_west")
    east = next(camera for camera in cameras if camera["n"] == "D1_streiflicht_ost")
    assert west["az"] == 45 and east["az"] == 225
    assert camera_list(expected, ("D1", "G1", "D2")) == cameras
