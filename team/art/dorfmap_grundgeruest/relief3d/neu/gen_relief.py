"""Generator-Einstieg fuer RELIEF_NEU=1; laesst alle Legacy-Artefakte unangetastet."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

from .felder import build_fields
from .vektor import OUT, SOURCE, build
from .pipeline import build as build_mesh_package


def run() -> None:
    result = build()
    fields = build_fields(result)
    # Die neue Sidecar-Basis ist eine bytegenaue Kopie der Zellquelle. Die
    # Prototypschichten duerfen keine Quellspalte umschreiben.
    shutil.copyfile(SOURCE, OUT / "zellen_relief.csv")
    src_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    copy_sha = hashlib.sha256((OUT / "zellen_relief.csv").read_bytes()).hexdigest()
    if src_sha != copy_sha:
        raise RuntimeError("Zellquellen-Sidecar ist nicht bytegleich")
    summary = {
        "schema": "dorfmap-neu-1", "vektor_sha256": hashlib.sha256((OUT / "vektor.json").read_bytes()).hexdigest(),
        "felder_sha256": hashlib.sha256((OUT / "felder.npz").read_bytes()).hexdigest(),
        "zellen_sha256": copy_sha, "zellen_quell_diff": 0,
        "felder": sorted(fields), "prototype_kacheln": result["daten"]["prototype_kacheln"],
    }
    (OUT / "build.json").write_text(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    build_mesh_package()
    print(json.dumps(summary, ensure_ascii=False))
