import base64
import gzip
import json
from pathlib import Path

import numpy as np


def b64(a):
    return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode("ascii")


def pack_column(values, words):
    words = list(words)
    lookup = {v: i for i, v in enumerate(words)}
    codes = np.fromiter((lookup[v] for v in values), dtype=np.uint8, count=len(values))
    return {"w": words, "t": "uint8", "i": b64(codes)}


def make_data(path: Path):
    nx, ny, rs = 336, 303, 2
    gx, gy = nx * rs + 1, ny * rs + 1
    yy, xx = np.mgrid[0:gy, 0:gx]
    g = (10 + 0.003 * xx + 0.002 * yy).astype(np.float32)
    residual = (0.08 * np.sin(xx * 0.7) + 0.05 * np.cos(yy * 0.9)).astype(np.float32)
    gb = g + residual
    fw_fs, fx = 4, nx * 4 + 1
    coords = [(140 * fw_fs, 20 * fw_fs), (260 * fw_fs, 20 * fw_fs), (140 * fw_fs, 50 * fw_fs)]
    vids = np.asarray([z * fx + x for x, z in coords], dtype=np.uint32)
    fh = np.asarray([10.0, 10.0, 10.0], dtype=np.float32)
    n = nx * ny
    source_cols = {}
    names = {
        "untergrund": ["BODEN"], "hindernis_id": ["0"], "hindernis_art": [""],
        "wasser_eis": ["0"], "ebene": ["HANG"], "bauzone_bestand": ["0"],
        "bauzone_plan": ["0"], "begehbar": ["1"], "bebaubar": ["0"],
    }
    for key, words in names.items():
        source_cols[key] = pack_column([words[0]] * n, words)
    for key, default, words in (
        ("klippe", "", ["", "WAND_FUSS", "WAND"]),
        ("wand_name", "", ["", "Nord"]),
    ):
        vals = [default] * n
        vals[20 * nx + 140] = "WAND_FUSS" if key == "klippe" else "Nord"
        source_cols[key] = pack_column(vals, words)
    arr = {
        "nx": nx, "ny": ny, "rs": rs, "G": b64(g), "GB": b64(gb),
        "VC": b64(np.full((gy, gx, 3), 180, dtype=np.uint8)),
        "WEGA": b64(np.zeros((gy, gx), dtype=np.uint8)),
        "WV": b64(np.full((gy, gx), -999, dtype=np.float32)),
        "spalten": source_cols, "reihenfolge": list(source_cols),
        "wege": [], "rampenwege": [],
        "FW": {"fs": fw_fs, "band": b64(np.zeros(nx * ny, dtype=np.uint8)), "vid": b64(vids), "h": b64(fh), "c": b64(np.full((len(vids), 3), 180, dtype=np.uint8))},
    }
    with path.open("wb") as f:
        f.write(gzip.compress(json.dumps(arr, separators=(",", ":")).encode(), mtime=0))
    return arr
