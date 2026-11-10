#!/usr/bin/env python3
"""Run unchanged official gates on a direct-transfer optimization candidate."""
from __future__ import annotations

import base64
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import sys

ROOT = Path(__file__).resolve().parents[3]
RELIEF3D = ROOT / "team/art/dorfmap_grundgeruest/relief3d"
if str(RELIEF3D) not in sys.path:
    sys.path.insert(0, str(RELIEF3D))
from neu import mesh as neu_mesh
from pruefung import neu_mesh_adapter
MODEL_PATH = Path(__file__).with_name("joint_mesh_r3_safety_p3d19.py")
SPEC = importlib.util.spec_from_file_location("p3d19_safety_model", MODEL_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("p3d19-Modellmodul konnte nicht geladen werden")
MODEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODEL
SPEC.loader.exec_module(MODEL)


def run_gate(args: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(args, cwd=RELIEF3D, env=env, capture_output=True, text=True)
    if completed.returncode not in (0, 1):
        raise RuntimeError(
            f"Gate fehlgeschlagen: {args}; code={completed.returncode}; "
            f"stdout={completed.stdout[-1000:]}; stderr={completed.stderr[-1000:]}"
        )
    return completed


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_model_solution.py MODEL_SUMMARY.json OUT_PREFIX")
    model_path, prefix = Path(sys.argv[1]), Path(sys.argv[2])
    solution = json.loads(model_path.read_text(encoding="utf-8"))
    if not solution.get("success") or "surface_grid" not in solution:
        raise RuntimeError("Kein feasible Modellgitter im Eingabebericht")
    source_bytes = MODEL.RELIEF.read_bytes()
    source = json.loads(gzip.decompress(source_bytes))
    fixed, coverage, _, _ = MODEL.p3d17_transfer_context()
    target = np.asarray(solution["surface_grid"]["heights_m"], dtype=np.float64)
    candidate = (fixed + coverage * target).astype("<f4")
    source_obj = neu_mesh.load_relief(MODEL.RELIEF)
    vector = json.loads((RELIEF3D / "neu/vektor.json").read_text(encoding="utf-8"))
    with np.load(RELIEF3D / "neu/felder.npz", allow_pickle=False) as archive:
        fields = {name: archive[name] for name in archive.files}
    old_cross = __import__("os").environ.get("RELIEF_KREUZUNG_VAR")
    old_end = __import__("os").environ.get("RELIEF_WEGEND_VAR")
    __import__("os").environ["RELIEF_KREUZUNG_VAR"] = "24"
    __import__("os").environ["RELIEF_WEGEND_VAR"] = "1"
    try:
        manifest = neu_mesh.build_manifest(
            MODEL.RELIEF,
            RELIEF3D / "neu/zellen_relief.csv",
            RELIEF3D / "neu/vektor.json",
            RELIEF3D / "neu/felder.npz",
            variant="2",
        )
    finally:
        if old_cross is None:
            __import__("os").environ.pop("RELIEF_KREUZUNG_VAR", None)
        else:
            __import__("os").environ["RELIEF_KREUZUNG_VAR"] = old_cross
        if old_end is None:
            __import__("os").environ.pop("RELIEF_WEGEND_VAR", None)
        else:
            __import__("os").environ["RELIEF_WEGEND_VAR"] = old_end
    positions = np.frombuffer(
        base64.b64decode(manifest["tiles"]["D1"]["vertices_xyz_f32"]), dtype="<f4",
    ).copy().reshape(-1, 3)
    if len(positions) != candidate.size:
        raise RuntimeError("D1-Kandidatenraster passt nicht zum Neu-Mesh-Manifest")
    positions[:, 1] = candidate.ravel()
    manifest["tiles"]["D1"]["vertices_xyz_f32"] = base64.b64encode(positions.tobytes()).decode("ascii")
    manifest["tiles"]["D1"]["height_sha256"] = hashlib.sha256(positions[:, 1].tobytes()).hexdigest()
    package = dict(source)
    package["neu_mesh_tiles"] = manifest
    data = neu_mesh_adapter.adapt_data(source, package)

    probe_path = Path(f"/tmp/relief_p3d19_{prefix.name}.json.gz")
    probe_path.write_bytes(gzip.compress(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        compresslevel=9, mtime=0,
    ))
    loch = Path(f"/tmp/gate_loch_p3d19_{prefix.name}.json")
    loch.write_text('{"offen_innen":0}\n', encoding="utf-8")
    rules_out = Path(f"/tmp/regeln_p3d19_{prefix.name}.json")
    r8_out = Path(f"/tmp/r8_p3d19_{prefix.name}.json")
    r9_out = Path(f"/tmp/r9_p3d19_{prefix.name}.json")
    env = dict(__import__("os").environ)
    env["LOCHSCAN"] = str(loch)
    run_gate([sys.executable, str(RELIEF3D / "pruefung/pruefe_regeln.py"), str(probe_path), str(rules_out)], env=env)
    run_gate([sys.executable, str(RELIEF3D / "pruefung/r8_kreuzung.py"), str(probe_path), str(r8_out)])
    run_gate([sys.executable, str(RELIEF3D / "pruefung/r9_form.py"), str(probe_path), str(r9_out)])
    rules = json.loads(rules_out.read_text(encoding="utf-8"))
    r8 = json.loads(r8_out.read_text(encoding="utf-8"))
    r9 = json.loads(r9_out.read_text(encoding="utf-8"))
    d1_rules: dict[str, int] = {}
    rules_by_tile = {tile: {} for tile in ("D1", "G1", "D2")}
    for hit in rules.get("treffer", []):
        tile = hit.get("feld")
        if tile in rules_by_tile:
            rules_by_tile[tile][hit["regel"]] = rules_by_tile[tile].get(hit["regel"], 0) + 1
        if hit.get("feld") == "D1":
            d1_rules[hit["regel"]] = d1_rules.get(hit["regel"], 0) + 1
    baseline_rules = json.loads(
        (RELIEF3D / "pruefung/bilder_p3d17/nachher/regeln.json").read_text(encoding="utf-8")
    ).get("je_regel", {})
    rules_by_rule = rules.get("je_regel", {})
    rules_over_limit = {
        rule: {"p3d17": count, "candidate": rules_by_rule.get(rule, 0), "max": count + 5}
        for rule, count in baseline_rules.items()
        if rules_by_rule.get(rule, 0) > count + 5
    }
    result = {
        "candidate_kind": "linear optimizer transfer, without gen_relief.py build",
        "source_relief_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "D1_height_sha256": hashlib.sha256(candidate.tobytes()).hexdigest(),
        "G1_height_sha256": manifest["tiles"]["G1"].get("height_sha256"),
        "D2_height_sha256": manifest["tiles"]["D2"].get("height_sha256"),
        "model_gate_metrics": solution.get("R8_gate_metrics_solution"),
        "D1_rules": d1_rules,
        "D1_rule_hits": [h for h in rules.get("treffer", []) if h.get("feld") == "D1"],
        "D1_G1_D2_rules": rules_by_tile,
        "common_plus_five_violations": rules_over_limit,
        "rules_total": rules.get("summe"),
        "rules_by_rule": rules_by_rule,
        "R8_total": r8.get("summe"),
        "R8_by_rule": r8.get("je_regel", {}),
        "R8_by_tile": r8.get("je_feld", {}),
        "R8_D1_end_or_cross_hits": [h for h in r8.get("treffer", []) if h.get("feld") == "D1"],
        "R8_D1_list": [x for x in r8.get("liste", []) if x.get("feld") == "D1"],
        "R8_by_rule_by_tile": r8.get("je_feld", {}),
        "R9_total": r9.get("summe"),
        "R9_by_rule": r9.get("je_regel", {}),
        "R9_by_tile": r9.get("je_feld", {}),
        "R9_D1_hits": [h for h in r9.get("treffer", []) if h.get("feld") == "D1"],
        "R9_by_rule_by_tile": r9.get("je_feld", {}),
        "probe_relief": str(probe_path),
    }
    prefix.parent.mkdir(parents=True, exist_ok=True)
    prefix.with_suffix(".json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
