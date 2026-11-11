#!/usr/bin/env python3
"""Evaluate a p3d21 direct-transfer candidate with unchanged official gates."""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

from run_model import RELIEF3D, load_model

if str(RELIEF3D) not in sys.path:
    sys.path.insert(0, str(RELIEF3D))
from neu import mesh as neu_mesh
from pruefung import neu_mesh_adapter


def run_gate(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=RELIEF3D, env=env, capture_output=True, text=True)
    if result.returncode not in (0, 1):
        raise RuntimeError(f"Gate command failed: {args}; stderr={result.stderr[-1000:]}")
    return result


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_model.py MODEL_SUMMARY.json OUT_PREFIX")
    model_path, prefix = Path(sys.argv[1]), Path(sys.argv[2])
    model = load_model()
    solution = json.loads(model_path.read_text(encoding="utf-8"))
    if not solution.get("success") or "surface_grid" not in solution:
        raise RuntimeError("No feasible p3d21 model surface")
    source_path = Path(os.environ["P3D21_SOURCE_RELIEF"])
    source_bytes = source_path.read_bytes()
    source = json.loads(gzip.decompress(source_bytes))

    fixed, coverage, _, _ = model.p3d17_transfer_context()
    target = np.asarray(solution["surface_grid"]["heights_m"], dtype=np.float64)
    candidate = (fixed + coverage * target).astype("<f4")

    old_cross = os.environ.get("RELIEF_KREUZUNG_VAR")
    old_end = os.environ.get("RELIEF_WEGEND_VAR")
    os.environ["RELIEF_KREUZUNG_VAR"] = "24"
    os.environ["RELIEF_WEGEND_VAR"] = "1"
    try:
        manifest = neu_mesh.build_manifest(
            source_path,
            RELIEF3D / "neu/zellen_relief.csv",
            RELIEF3D / "neu/vektor.json",
            RELIEF3D / "neu/felder.npz",
            variant="2",
        )
    finally:
        if old_cross is None:
            os.environ.pop("RELIEF_KREUZUNG_VAR", None)
        else:
            os.environ["RELIEF_KREUZUNG_VAR"] = old_cross
        if old_end is None:
            os.environ.pop("RELIEF_WEGEND_VAR", None)
        else:
            os.environ["RELIEF_WEGEND_VAR"] = old_end

    d1 = manifest["tiles"]["D1"]
    positions = np.frombuffer(base64.b64decode(d1["vertices_xyz_f32"]), dtype="<f4").copy().reshape(-1, 3)
    if len(positions) != candidate.size:
        raise RuntimeError("D1 candidate does not match the direct-transfer tile raster")
    positions[:, 1] = candidate.ravel()
    d1["vertices_xyz_f32"] = base64.b64encode(positions.tobytes()).decode("ascii")
    d1["height_sha256"] = hashlib.sha256(positions[:, 1].tobytes()).hexdigest()

    package = dict(source)
    package["neu_mesh_tiles"] = manifest
    gate_data = neu_mesh_adapter.adapt_data(source, package)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    probe = Path(f"/tmp/relief_p3d21_{prefix.name}.json.gz")
    probe.write_bytes(gzip.compress(
        json.dumps(gate_data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        compresslevel=9, mtime=0,
    ))
    loch = Path(f"/tmp/gate_loch_p3d21_{prefix.name}.json")
    loch.write_text('{"offen_innen":0}\n', encoding="utf-8")
    rules_out = Path(f"/tmp/regeln_p3d21_{prefix.name}.json")
    r8_out = Path(f"/tmp/r8_p3d21_{prefix.name}.json")
    r9_out = Path(f"/tmp/r9_p3d21_{prefix.name}.json")
    env = dict(os.environ, LOCHSCAN=str(loch))
    run_gate([sys.executable, str(RELIEF3D / "pruefung/pruefe_regeln.py"), str(probe), str(rules_out)], env)
    run_gate([sys.executable, str(RELIEF3D / "pruefung/r8_kreuzung.py"), str(probe), str(r8_out)])
    run_gate([sys.executable, str(RELIEF3D / "pruefung/r9_form.py"), str(probe), str(r9_out)])
    rules = json.loads(rules_out.read_text(encoding="utf-8"))
    r8 = json.loads(r8_out.read_text(encoding="utf-8"))
    r9 = json.loads(r9_out.read_text(encoding="utf-8"))
    tile_rules = {tile: {} for tile in ("D1", "G1", "D2")}
    d1_rules = {}
    for hit in rules.get("treffer", []):
        tile_name = hit.get("feld")
        if tile_name in tile_rules:
            counts = tile_rules[tile_name]
            counts[hit["regel"]] = counts.get(hit["regel"], 0) + 1
        if tile_name == "D1":
            d1_rules[hit["regel"]] = d1_rules.get(hit["regel"], 0) + 1
    baseline_rules = json.loads(
        (RELIEF3D / "pruefung/bilder_p3d17/nachher/regeln.json").read_text(encoding="utf-8")
    ).get("je_regel", {})
    violations = {
        name: {"baseline": count, "candidate": rules.get("je_regel", {}).get(name, 0), "limit": count + 5}
        for name, count in baseline_rules.items()
        if rules.get("je_regel", {}).get(name, 0) > count + 5
    }
    result = {
        "candidate_kind": "p3d20 exact event model direct-transfer probe; LOCHSCAN dummy, no live scan",
        "source_relief_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "D1_height_sha256": d1["height_sha256"],
        "G1_height_sha256": manifest["tiles"]["G1"]["height_sha256"],
        "D2_height_sha256": manifest["tiles"]["D2"]["height_sha256"],
        "model_gate_metrics": solution.get("R8_gate_metrics_solution"),
        "model_R8_gate_center_unrounded_map": solution.get("R8_gate_center_unrounded_map"),
        "D1_rules": d1_rules,
        "D1_rule_hits": [hit for hit in rules.get("treffer", []) if hit.get("feld") == "D1"],
        "D1_G1_D2_rules": tile_rules,
        "common_plus_five_violations": violations,
        "rules_total": rules.get("summe"), "rules_by_rule": rules.get("je_regel", {}),
        "R8_total": r8.get("summe"), "R8_by_rule": r8.get("je_regel", {}),
        "R8_by_tile": r8.get("je_feld", {}),
        "R8_D1_hits": [hit for hit in r8.get("treffer", []) if hit.get("feld") == "D1"],
        "R8_D1_list": [entry for entry in r8.get("liste", []) if entry.get("feld") == "D1"],
        "R9_total": r9.get("summe"), "R9_by_rule": r9.get("je_regel", {}),
        "R9_by_tile": r9.get("je_feld", {}),
        "R9_D1_hits": [hit for hit in r9.get("treffer", []) if hit.get("feld") == "D1"],
        "probe_relief": str(probe),
    }
    prefix.with_suffix(".json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
