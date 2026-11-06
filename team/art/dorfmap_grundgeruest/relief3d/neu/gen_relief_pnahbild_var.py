"""Isolierter, deterministischer Anzeige-Rest-Prototyp fuer D1 und G1.

Die kanonische 0,5-m-Quellflaeche G und alle Zellquellen bleiben unveraendert.
Nur hochfrequente Anteile des Anzeige-Restfelds (GB-G und FW.h-G) werden im
Inneren von D1/G1 reduziert. Die Rand-Fade-Zone haelt Kachelnaehte fest.
"""
from __future__ import annotations

import base64
import csv
import gzip
import json
import os
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("RELIEF_NEU_DIR", Path(__file__).parent / "build"))
SOURCE_COLUMNS = (
    "untergrund", "hindernis_id", "hindernis_art", "wasser_eis", "ebene",
    "bauzone_bestand", "bauzone_plan", "begehbar", "bebaubar",
)
VARIANTS = {
    # Der Kontrolllauf bleibt Standard, bis eine Filterstaerke die Bildzahlen verbessert.
    "0": ("kontrolle", 0.0, 0.0),
    "1": ("rest_06m", 0.60, 0.40),
}


def _decode(text: str, dtype: np.dtype, shape: tuple[int, ...]) -> np.ndarray:
    return np.frombuffer(base64.b64decode(text), dtype=dtype).reshape(shape).copy()


def _encode(array: np.ndarray) -> str:
    return base64.b64encode(np.ascontiguousarray(array).tobytes()).decode("ascii")


def _columns(d: dict) -> dict[str, np.ndarray]:
    result = {}
    for name, col in d["spalten"].items():
        dt = {"uint8": np.uint8, "uint16": np.uint16, "uint32": np.uint32}[col["t"]]
        idx = np.frombuffer(base64.b64decode(col["i"]), dtype=dt).astype(np.int64)
        words = np.asarray(col["w"], dtype=object)
        result[name] = words[idx]
    return result


def _tiles(nx: int, ny: int) -> dict[str, tuple[int, int, int, int]]:
    # Tile labels use 42 m by 43 m cells, matching the unchanged gate scripts.
    return {
        name: (ci * 42, min((ci + 1) * 42, nx), ri * 43, min((ri + 1) * 43, ny))
        for name, ci, ri in (("D1", 3, 0), ("G1", 6, 0), ("D2", 3, 1))
    }


def _road_mask(d: dict, nx: int, ny: int, rs: int, gx: int, gy: int) -> np.ndarray:
    road = np.frombuffer(base64.b64decode(d["WEGA"]), np.uint8).reshape(gy, gx) > 20
    for x, z in d.get("wege", []):
        x, z = int(x), int(z)
        road[z * rs:min(z * rs + rs + 1, gy), x * rs:min(x * rs + rs + 1, gx)] = True
    for path in d.get("rampenwege", []):
        p = np.asarray(path, dtype=float)
        if len(p) < 2:
            continue
        lengths = np.hypot(*(np.diff(p, axis=0).T))
        for (x0, z0), (x1, z1), length in zip(p[:-1], p[1:], lengths):
            n = max(1, int(np.ceil(length * rs * 2)))
            t = np.linspace(0.0, 1.0, n + 1)
            xi = np.clip(np.rint((x0 + (x1 - x0) * t) * rs).astype(int), 0, gx - 1)
            zi = np.clip(np.rint((z0 + (z1 - z0) * t) * rs).astype(int), 0, gy - 1)
            road[zi, xi] = True
    # The roads and ramp center lines are protected with a 2.5 m margin.
    return ndi.distance_transform_edt(~road) / rs <= 2.5


def _tile_weight(bounds: tuple[int, int, int, int], gx: int, gy: int, rs: int, guard_m: float) -> np.ndarray:
    x0, x1, z0, z1 = bounds
    x = np.arange(gx, dtype=np.float32)[None, :] / rs
    z = np.arange(gy, dtype=np.float32)[:, None] / rs
    dist = np.minimum.reduce((
        np.broadcast_to(x - x0, (gy, gx)),
        np.broadcast_to(x1 - x, (gy, gx)),
        np.broadcast_to(z - z0, (gy, gx)),
        np.broadcast_to(z1 - z, (gy, gx)),
    ))
    t = np.clip(dist / max(guard_m, 1e-6), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _display_d2_equal(before: dict, after: dict, bounds: tuple[int, int, int, int], rs: int) -> dict:
    nx, ny = before["nx"], before["ny"]
    gx, gy = nx * rs + 1, ny * rs + 1
    x0, x1, z0, z1 = bounds
    sl = (slice(z0 * rs, z1 * rs + 1), slice(x0 * rs, x1 * rs + 1))
    result = {}
    for key in ("G", "GB", "VC", "WEGA", "WV"):
        dt = np.uint8 if key in ("VC", "WEGA") else np.float32
        shape = (gy, gx, 3) if key == "VC" else (gy, gx)
        a = _decode(before[key], dt, shape)
        b = _decode(after[key], dt, shape)
        result[key] = bool(np.array_equal(a[sl], b[sl]))
    fw0, fw1 = before["FW"], after["FW"]
    fs = fw0["fs"]
    fx = nx * fs + 1
    vids = np.frombuffer(base64.b64decode(fw0["vid"]), np.uint32)
    old = np.frombuffer(base64.b64decode(fw0["h"]), np.float32)
    new = np.frombuffer(base64.b64decode(fw1["h"]), np.float32)
    vx, vz = vids % fx, vids // fx
    in_d2 = (vx >= x0 * fs) & (vx <= x1 * fs) & (vz >= z0 * fs) & (vz <= z1 * fs)
    result["FW.h"] = bool(np.array_equal(old[in_d2], new[in_d2]))
    return result


def _write_sidecar(src: Path, dst: Path, gb: np.ndarray, d: dict, tiles: dict) -> None:
    nx, ny, rs = d["nx"], d["ny"], d["rs"]
    gx, gy = nx * rs + 1, ny * rs + 1
    sums = sum(gb[dy:dy + gy - 1:rs, dx:dx + gx - 1:rs][:ny, :nx] for dy in range(3) for dx in range(3)) / 9.0
    selected = np.zeros((ny, nx), dtype=bool)
    for name in ("D1", "G1"):
        x0, x1, z0, z1 = tiles[name]
        selected[z0:z1, x0:x1] = True
    with src.open(newline="", encoding="utf-8") as f_in, dst.open("w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in reader:
            z, x = int(row["cy"]), int(row["cx"])
            if selected[z, x]:
                row["boden_anzeige_m"] = f"{sums[z, x]:.2f}"
            writer.writerow(row)


def build(input_path: Path | None = None, output_dir: Path | None = None, variant: str | None = None) -> dict:
    input_path = input_path or ROOT / "relief_daten.json.gz"
    output_dir = output_dir or OUT
    variant = variant or os.environ.get("RELIEF_NEU_VAR", "0")
    if variant not in VARIANTS:
        raise ValueError(f"RELIEF_NEU_VAR muss einer von {', '.join(VARIANTS)} sein")
    label, sigma_m, blend = VARIANTS[variant]
    output_dir.mkdir(parents=True, exist_ok=True)

    with gzip.open(input_path, "rt", encoding="utf-8") as f:
        source = json.load(f)
    d = json.loads(json.dumps(source, ensure_ascii=False))
    nx, ny, rs = d["nx"], d["ny"], d["rs"]
    gx, gy = nx * rs + 1, ny * rs + 1
    g = _decode(d["G"], np.float32, (gy, gx))
    gb = _decode(d["GB"], np.float32, (gy, gx))
    original_gb = gb.copy()
    residual = gb.astype(np.float64) - g.astype(np.float64)
    wet = _decode(d["WV"], np.float32, (gy, gx)) > -900.0
    road = _road_mask(d, nx, ny, rs, gx, gy)
    land = ~wet & ~road
    changes = np.zeros((gy, gx), dtype=np.float64)
    tile_bounds = _tiles(nx, ny)
    if sigma_m > 0 and blend > 0:
        smoothed = ndi.gaussian_filter(residual, sigma=sigma_m * rs, mode="nearest")
        high_frequency = residual - smoothed
        for name in ("D1", "G1"):
            weight = _tile_weight(tile_bounds[name], gx, gy, rs, guard_m=8.0)
            weight *= land
            changes += -blend * high_frequency * weight
    gb_new = (gb.astype(np.float64) + changes).astype(np.float32)
    d["GB"] = _encode(gb_new)

    fw = d["FW"]
    fs = fw["fs"]
    vids = np.frombuffer(base64.b64decode(fw["vid"]), np.uint32)
    old_h = np.frombuffer(base64.b64decode(fw["h"]), np.float32).copy()
    if sigma_m > 0 and blend > 0:
        fx = nx * fs + 1
        vx = (vids % fx).astype(float)
        vz = (vids // fx).astype(float)
        delta = ndi.map_coordinates(changes, [vz / fs * rs, vx / fs * rs], order=1, mode="nearest")
        old_h += delta.astype(np.float32)
    fw["h"] = _encode(old_h)

    source_column_diff = {}
    for key in SOURCE_COLUMNS:
        a, b = source.get("spalten", {}).get(key), d.get("spalten", {}).get(key)
        if a is None and b is None:
            source_column_diff[key] = 0
        elif a is None or b is None:
            source_column_diff[key] = nx * ny
        else:
            # Compare the encoded source bytes, vocabulary, and storage dtype, not decoded values.
            changed = a["w"] != b["w"] or a["t"] != b["t"] or a["i"] != b["i"]
            source_column_diff[key] = int(changed) * nx * ny
            if changed:
                raise AssertionError(f"Quellspalte {key} wurde veraendert")
    if not np.array_equal(g, _decode(d["G"], np.float32, (gy, gx))):
        raise AssertionError("G darf im Anzeige-Prototyp nicht geaendert werden")
    d2_display = _display_d2_equal(source, d, tile_bounds["D2"], rs)
    if not all(d2_display.values()):
        raise AssertionError(f"D2 Anzeige wurde veraendert: {d2_display}")

    max_change = float(np.abs(gb_new - original_gb).max())
    changed_vertices = int((np.abs(gb_new - original_gb) > 1e-7).sum())
    meta = {
        "schema": "pnahbild-neu-v1",
        "variante": variant,
        "profil": label,
        "sigma_m": sigma_m,
        "blend": blend,
        "kacheln": ["D1", "G1", "D2"],
        "geaenderte_gb_punkte": changed_vertices,
        "gb_max_aenderung_m": round(max_change, 6),
        "quellspalten_diff_werte": source_column_diff,
        "quellspalten_diff_summe": int(sum(source_column_diff.values())),
        "D2_anzeige_bytegleich": d2_display,
        "annahmen": [
            "GB-G ist das Anzeige-Restfeld; G und damit t42u bleiben die kanonische Zellhoehe.",
            "Anzeige-Aenderungen sind auf D1/G1 beschraenkt und haben 8 m Fade zu Kachelraendern.",
            "Wasser und Wege mit 2,5 m Abstand bleiben von der Restfeldfilterung ausgenommen.",
        ],
    }
    d["relief_neu"] = meta
    data_path = output_dir / "relief_daten_neu.json.gz"
    with data_path.open("wb") as f:
        f.write(gzip.compress(json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), compresslevel=9, mtime=0))
    base_csv = ROOT / "zellen_relief.csv"
    if base_csv.exists():
        _write_sidecar(base_csv, output_dir / "zellen_relief_neu.csv", gb_new, d, tile_bounds)
    (output_dir / "relief_neu_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"datei": str(data_path), **meta}


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, sort_keys=True))
