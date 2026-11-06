from __future__ import annotations

import base64
import gzip
import json
from pathlib import Path

import numpy as np

RELIEF3D = Path(__file__).resolve().parents[2]


def _payload(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def _field(data: dict, key: str) -> np.ndarray:
    return np.frombuffer(base64.b64decode(data[key]), dtype=np.float32).reshape(
        data["ny"] * data["rs"] + 1, data["nx"] * data["rs"] + 1,
    )


def test_mesh_gate_adapter_uses_visible_mesh_and_locks_d2(tmp_path: Path) -> None:
    import subprocess
    import sys

    output = tmp_path / "mesh-gates.json.gz"
    subprocess.run(
        [sys.executable, str(RELIEF3D / "pruefung" / "neu_mesh_adapter.py"),
         "--mesh", str(RELIEF3D / "neu" / "relief_neu.json.gz"), "--out", str(output)],
        cwd=RELIEF3D,
        check=True,
        capture_output=True,
        text=True,
    )
    original = _payload(RELIEF3D / "relief_daten.json.gz")
    adapted = _payload(output)
    assert adapted["neu_mesh_gate"]["tiles_patched"] == ["D1", "G1"]
    assert adapted["neu_mesh_gate"]["d2_gb_mesh_bytegleich"] is True

    for key in ("G", "GB"):
        before, after = _field(original, key), _field(adapted, key)
        assert before[43 * 2 : 86 * 2 + 1, 126 * 2 : 168 * 2 + 1].tobytes() == after[
            43 * 2 : 86 * 2 + 1, 126 * 2 : 168 * 2 + 1
        ].tobytes()
        assert before[0 : 43 * 2 + 1, 126 * 2 : 168 * 2 + 1].tobytes() != after[
            0 : 43 * 2 + 1, 126 * 2 : 168 * 2 + 1
        ].tobytes()

    old_fw = original["FW"]
    new_fw = adapted["FW"]
    ids = np.frombuffer(base64.b64decode(old_fw["vid"]), dtype=np.uint32)
    old_h = np.frombuffer(base64.b64decode(old_fw["h"]), dtype=np.float32)
    new_h = np.frombuffer(base64.b64decode(new_fw["h"]), dtype=np.float32)
    width = original["nx"] * old_fw["fs"] + 1
    x, z = ids % width, ids // width
    d2 = (x >= 126 * old_fw["fs"]) & (x <= 168 * old_fw["fs"]) & (z >= 43 * old_fw["fs"])
    assert old_h[d2].tobytes() == new_h[d2].tobytes()
    assert np.count_nonzero(old_h != new_h) > 0
