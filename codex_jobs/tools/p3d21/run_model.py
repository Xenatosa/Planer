#!/usr/bin/env python3
"""Run the unchanged p3d20 event model on a p3d21 route candidate."""
from __future__ import annotations

import os
from pathlib import Path
import sys
import types

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
P3D20_MODEL = ROOT / "codex_jobs/tools/p3d20_r3/joint_mesh_r3_exact_p3d20.py"


def load_model():
    source = P3D20_MODEL.read_text(encoding="utf-8")
    old_relief = 'RELIEF = ROOT / "team/art/dorfmap_grundgeruest/relief3d/relief_daten.json.gz"'
    new_relief = (
        'RELIEF = Path(os.environ.get("P3D21_SOURCE_RELIEF", '
        'str(ROOT / "team/art/dorfmap_grundgeruest/relief3d/relief_daten.json.gz")))'
    )
    if old_relief not in source:
        raise RuntimeError("p3d20-Modell hat die erwartete Reliefpfadzeile geändert")
    source = source.replace(old_relief, new_relief, 1)
    old_guard = (
        'if p3d18_reference_hash != "9619da5083720eb43f736043452b28f87dd2f9aa946dc2cb453b5ed972d02c6c":\n'
        '        raise RuntimeError("Die unveraenderte p3d18-Variante-24 Referenz passt nicht zum Bericht")'
    )
    new_guard = (
        'expected_reference_hash = os.environ.get("P3D21_EXPECT_REFERENCE_SHA256")\n'
        '    if expected_reference_hash and p3d18_reference_hash != expected_reference_hash:\n'
        '        raise RuntimeError("p3d18-Transferreferenz weicht vom dokumentierten Hash ab")'
    )
    if old_guard not in source:
        raise RuntimeError("p3d20-Modell hat die erwartete Referenz-Hashprüfung geändert")
    source = source.replace(old_guard, new_guard, 1)

    module = types.ModuleType("p3d21_p3d20_event_model")
    module.__file__ = str(P3D20_MODEL)
    module.__package__ = ""
    exec(compile(source, str(P3D20_MODEL), "exec"), module.__dict__)

    center = np.asarray([float(v) for v in os.environ["P3D21_R8_CENTER"].split(",")], dtype=np.float64)
    if center.shape != (2,):
        raise ValueError("P3D21_R8_CENTER muss x,z enthalten")
    module.R8_GATE_CENTER = center.copy()
    module.CROSSING = center.copy()

    from neu import mesh as neu_mesh
    transfer = Path(os.environ["P3D21_TRANSFER_BASE_FILE"])
    neu_mesh.KREUZUNG_SETTINGS["24"]["solution_file"] = transfer.name
    neu_mesh.KREUZUNG_SETTINGS["24"]["crossing_center_map"] = center.tolist()
    return module


def main() -> None:
    model = load_model()
    sys.argv = [str(P3D20_MODEL), *sys.argv[1:]]
    model.main()


if __name__ == "__main__":
    main()
