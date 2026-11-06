"""Neu-Mesh gate checks and fixed regression-image checks."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

import pytest

RELIEF3D = Path(__file__).resolve().parents[2]
NEG = RELIEF3D / "neu" / "referenz_neg"
ADAPTER = RELIEF3D / "pruefung" / "neu_mesh_adapter.py"


def _gate(script: str, data: Path, tmp_path: Path) -> dict:
    out = tmp_path / f"{script}.json"
    result = subprocess.run(
        [sys.executable, str(RELIEF3D / "pruefung" / script), str(data), str(out)],
        cwd=RELIEF3D,
        text=True,
        capture_output=True,
        check=False,
    )
    assert out.exists(), f"{script} did not write its measurements: {result.stderr}"
    return json.loads(out.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def mesh_gate_inputs(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    root = tmp_path_factory.mktemp("mesh-gates")
    control, candidate = root / "control.json.gz", root / "candidate.json.gz"
    result = subprocess.run(
        [sys.executable, str(ADAPTER), "--variant", "0", "--out", str(control)],
        cwd=RELIEF3D,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert control.exists(), "Neu-Mesh-Adapter hat Kontrollvariante 0 nicht geschrieben"
    result = subprocess.run(
        [sys.executable, str(ADAPTER), "--mesh", str(RELIEF3D / "neu" / "relief_neu.json.gz"),
         "--out", str(candidate)],
        cwd=RELIEF3D,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert candidate.exists(), "Neu-Mesh-Adapter hat das sichtbare relief_neu.json.gz nicht gelesen"
    return control, candidate


@pytest.fixture(scope="module")
def r8(mesh_gate_inputs: tuple[Path, Path], tmp_path_factory: pytest.TempPathFactory) -> dict:
    return _gate("r8_kreuzung.py", mesh_gate_inputs[1], tmp_path_factory.mktemp("r8"))


@pytest.fixture(scope="module")
def r8_control(mesh_gate_inputs: tuple[Path, Path], tmp_path_factory: pytest.TempPathFactory) -> dict:
    return _gate("r8_kreuzung.py", mesh_gate_inputs[0], tmp_path_factory.mktemp("r8-control"))


@pytest.fixture(scope="module")
def r9(mesh_gate_inputs: tuple[Path, Path], tmp_path_factory: pytest.TempPathFactory) -> dict:
    return _gate("r9_form.py", mesh_gate_inputs[1], tmp_path_factory.mktemp("r9"))


def test_kreuzung_d1_g1_mesh_stufe(r8: dict) -> None:
    d1 = next(k for k in r8["liste"] if k["feld"] == "D1" and k["art"] == "rampe_2x11")
    g1 = next(k for k in r8["liste"] if k["feld"] == "G1" and k["art"] == "rampe_1_anfang")
    stufe_m = max(float(d1["stufe"]), float(g1["stufe"]))
    assert stufe_m <= 0.20, f"ROT: Kreuzung D1/G1 Stufe {stufe_m:.3f} m; Grenze 0.20 m"


def test_wegende_d1_g1_meshmessung_verbessert(r8: dict, r8_control: dict) -> None:
    def selected(data: dict) -> list[float]:
        return [
            float(hit["wert"]) for hit in data["treffer"]
            if hit["regel"] == "R8a_wegende" and hit["feld"] in ("D1", "G1")
        ]

    before, after = selected(r8_control), selected(r8)
    assert len(after) <= len(before)
    assert sum(after) < sum(before), (
        f"ROT: R8a D1/G1 am Neu-Mesh nicht messbar verbessert: {sum(before):.2f} m -> {sum(after):.2f} m"
    )


def test_delle_g1_278_5_27_0_hoehenfeld(r9: dict) -> None:
    hit = next((
        t for t in r9["treffer"]
        if t["regel"] == "R8b_delle" and t["feld"] == "G1"
        and abs(float(t["x"]) - 278.5) < 0.01 and abs(float(t["z"]) - 27.0) < 0.01
    ), None)
    tiefe_m = float(hit["wert"]) if hit else 0.0
    assert tiefe_m <= 0.30, f"ROT: Delle G1 {tiefe_m:.2f} m; Grenze 0.30 m"


def test_saegezahn_d1_mesh_count(r9: dict) -> None:
    hit = next(t for t in r9["treffer"] if t["regel"] == "R9_saegezahn" and t["feld"] == "D1")
    zacken = int(hit["wert"])
    assert zacken == 0, f"ROT: D1 hat {zacken} Zaehnelemente; Grenze 0"


def test_verwaschene_wand_d1_kantenschaerfe() -> None:
    image = np.asarray(Image.open(NEG / "wand_D1_ton.png").convert("L"), dtype=float)
    # Fixed wall crop of the D1 Fabian render; 90th-percentile edge gradient.
    crop = image[400:720, 500:900]
    gy, gx = np.gradient(crop)
    edge = float(np.percentile(np.hypot(gx, gy), 90))
    assert edge >= 3.0, f"ROT: D1-Wandkantenstaerke {edge:.2f} Graustufen/Pixel; Grenze 3.00"


def test_d2_control_remains_out_of_r8_r9(r8: dict, r9: dict) -> None:
    assert not any(hit["feld"] == "D2" for hit in r8["treffer"])
    assert not any(hit["feld"] == "D2" for hit in r9["treffer"])


def test_schattenartefakt_renderbild() -> None:
    image = np.asarray(Image.open(NEG / "saege_D1_schatten_an.png").convert("L"), dtype=float)
    # Fixed camera crop from the paired Fabian shadow comparison.
    crop = image[300:600, 500:1050]
    residual = np.abs(crop - gaussian_filter(crop, sigma=1.0))
    score = float(residual.mean())
    assert score <= 0.25, f"ROT: Schattenbild-Hochfrequenz {score:.3f}; Grenze 0.25 Graustufen"
