"""Globale signierte Abstandsfelder ohne Kachel-Crops oder Nahtbehandlung."""
from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

from .vektor import CELL_M, NX, NY, OUT, build


def signed_distance(mask: np.ndarray) -> np.ndarray:
    if mask.shape != (NY, NX):
        raise ValueError(f"Falsche Feldform {mask.shape}; erwartet {(NY, NX)}")
    if not mask.any():
        return np.full(mask.shape, np.hypot(NX, NY) * CELL_M, dtype=np.float32)
    if mask.all():
        return np.full(mask.shape, -np.hypot(NX, NY) * CELL_M, dtype=np.float32)
    outside = ndi.distance_transform_edt(~mask) * CELL_M
    inside = ndi.distance_transform_edt(mask) * CELL_M
    return (outside - inside).astype(np.float32)


def save_deterministic_npz(path: Path, fields: dict[str, np.ndarray]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(fields):
            payload = io.BytesIO()
            np.lib.format.write_array(payload, np.ascontiguousarray(fields[name]), allow_pickle=False)
            info = zipfile.ZipInfo(f"{name}.npy", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            info.create_system = 3
            archive.writestr(info, payload.getvalue(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build_fields(vector_result: dict | None = None) -> dict[str, np.ndarray]:
    v = vector_result or build()
    masks = {
        "weg": v["wegmaske"], "kreuzung": v["kreuzungsmaske"],
        "wand": v["wandmaske"], "wasser": v["wassermaske"],
        "bauzone_bestand": v["bauzone_bestand"], "bauzone_plan": v["bauzone_plan"],
    }
    fields = {name: signed_distance(mask) for name, mask in masks.items()}
    save_deterministic_npz(OUT / "felder.npz", fields)
    metadata = {"shape": [NY, NX], "cell_m": CELL_M, "innen": "negativ", "felder": sorted(fields),
                "global_tiles": 56, "kachelraender_berechnet": False}
    (OUT / "felder.json").write_text(json.dumps(metadata, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return fields


if __name__ == "__main__":
    fields = build_fields()
    print(json.dumps({"shape": [NY, NX], "felder": sorted(fields)}, ensure_ascii=False))
