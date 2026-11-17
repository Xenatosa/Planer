"""QA P4b: Messwerte je Stelle aus dem GB-Hoehenfeld (relief_daten.json.gz, 0,5-m-Raster).
zacke_m = max |h - h_glatt| im Radius r (h_glatt = 5x5-Mittel, 2,5 m) -> Amplitude von Zacken/Saegezahn.
hang_max_grad = steilste Zellneigung im Radius r; wand = hang_max_grad > 45.
Aufruf (im Ordner relief3d): python3 pruefung/qa_p4b/messung.py punkte.json [r=3]
Hinweis: Prototyp-Kacheln D1/D2/G1 haben im Viewer lokale Profile; dort ist GB nur Naeherung."""
import sys, json, sys as _s
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[2]
_s.path.insert(0, str(R))
from neu import mesh as M
src = M.load_relief(R / "relief_daten.json.gz"); rs = int(src.data["rs"]); H = src.heights.astype(np.float64)
k = 5; p = k // 2; P = np.pad(H, p, mode="edge")
G = sum(P[i:i + H.shape[0], j:j + H.shape[1]] for i in range(k) for j in range(k)) / k / k
gz, gx = np.gradient(H, 1.0 / rs); S = np.degrees(np.arctan(np.hypot(gx, gz)))
pts = json.load(open(sys.argv[1])); r = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
aus = []
for q in pts:
    ix, iz = int(round(q["x"] * rs)), int(round(q["z"] * rs)); n = int(r * rs)
    sl = (slice(max(iz - n, 0), iz + n + 1), slice(max(ix - n, 0), ix + n + 1))
    d = np.abs(H[sl] - G[sl]); s = S[sl]
    aus.append({"n": q["n"], "x": q["x"], "z": q["z"], "h_m": round(float(H[iz, ix]), 2),
                "zacke_m": round(float(d.max()), 2), "hang_max_grad": round(float(s.max()), 1),
                "hang_mittel_grad": round(float(s.mean()), 1), "wand": bool(s.max() > 45)})
print(json.dumps(aus, ensure_ascii=False, indent=0))
