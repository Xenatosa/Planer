#!/usr/bin/env python3
"""Replay the unchanged p3d17 v22 transfer through the official R3 checker."""
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

ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = Path(__file__).with_name("joint_mesh_r3_official_p3d18.py")
SPEC = importlib.util.spec_from_file_location("p3d18_official_r3_model", MODEL_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("R3-Modellmodul konnte nicht geladen werden")
MODEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODEL
SPEC.loader.exec_module(MODEL)


def main() -> None:
    source_bytes = MODEL.RELIEF.read_bytes()
    data = json.loads(gzip.decompress(source_bytes))
    transfer_fixed, transfer_coverage, delivered, context = MODEL.p3d17_transfer_context()
    reconstructed = (
        transfer_fixed + transfer_coverage * context["target"]
    ).astype("<f4")
    if not np.array_equal(reconstructed, delivered):
        raise RuntimeError("Die Modellzeilen bilden den p3d17-Transfer nicht bytegenau ab")

    field = np.frombuffer(base64.b64decode(data["GB"]), dtype=np.float32).copy().reshape(
        int(data["ny"]) * int(data["rs"]) + 1,
        int(data["nx"]) * int(data["rs"]) + 1,
    )
    x0, z0, x1, z1 = (int(value) for value in MODEL.D1_BOUNDS)
    rs = int(data["rs"])
    field[z0 * rs : z1 * rs + 1, x0 * rs : x1 * rs + 1] = delivered
    data["GB"] = base64.b64encode(field.astype("<f4", copy=False).tobytes()).decode("ascii")

    gate_path = Path("/tmp/gate_loch_p3d18_kalibrierung.json.gz")
    rules_path = Path("/tmp/regeln_p3d18_kalibrierung.json")
    gate_path.write_bytes(gzip.compress(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        compresslevel=9,
        mtime=0,
    ))
    completed = subprocess.run(
        [sys.executable, str(MODEL.OFFICIAL_RULES), str(gate_path), str(rules_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1) or not rules_path.exists():
        raise RuntimeError(
            "Offizieller R3-Prueferlauf fehlgeschlagen: "
            f"code={completed.returncode}; stdout={completed.stdout[-1000:]}; stderr={completed.stderr[-1000:]}"
        )
    result = json.loads(rules_path.read_text(encoding="utf-8"))
    counts = {name: 0 for name in ("R3_laengs_m", "R3_quer_pct", "R3_woelb_m")}
    for hit in result.get("treffer", []):
        if hit.get("feld") == "D1" and hit.get("regel") in counts:
            counts[hit["regel"]] += 1
    expected = {"R3_laengs_m": 6, "R3_quer_pct": 17, "R3_woelb_m": 19}
    d1 = field[z0 * rs : z1 * rs + 1, x0 * rs : x1 * rs + 1]
    height_hash = hashlib.sha256(d1.astype("<f4", copy=False).tobytes()).hexdigest()
    summary = {
        "calibration": "p3d17 v22 unchanged solution -> affine transfer rows -> official pruefe_regeln.py",
        "source_relief_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "D1_height_sha256": height_hash,
        "p3d17_D1_hash_matches_report": height_hash == "26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29",
        "reconstructed_mesh_byte_equal": True,
        "official_R3_D1_counts": counts,
        "expected_official_R3_D1_counts": expected,
        "matches": counts == expected,
        "gate_input": str(gate_path),
        "rules_output": str(rules_path),
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    if counts != expected or not summary["p3d17_D1_hash_matches_report"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
