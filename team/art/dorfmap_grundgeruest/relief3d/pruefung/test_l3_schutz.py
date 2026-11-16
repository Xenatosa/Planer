"""L3c: Test Masstab relief_l3.schutz() (vektor.json Meter -> Zellen, zellweite_m 1,2).
Belegt: (1) Quellzellen jedes vektor.json-Weges liegen auf der umgerechneten Mittellinie (Meter/1,2), nicht auf Meter-als-Zellen;
(2) nach dem Fix sind alle Quellzellen-Mittelpunkte der Wege und Kreuzungen im Schutz (Gewicht 0); (3) WEGA-Zellen geschuetzt.
Aufruf: python3 pruefung/test_l3_schutz.py  (Exit 0 = bestanden)"""
import json, gzip, sys, importlib.util
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("l3", R / "relief_l3.py"); l3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(l3)
V = json.loads((R / "neu" / "vektor.json").read_text()); zw = V["karte"]["zellweite_m"]; nx = V["karte"]["nx"]
D = json.load(gzip.open(R / "relief_daten.json.gz")); rs = D["rs"]; GY, GX = D["ny"] * rs + 1, D["nx"] * rs + 1
def dist(P, Q):
    best = np.full(len(Q), 1e9)
    for a, b in zip(P[:-1], P[1:]):
        ab = b - a; t = np.clip(((Q - a) @ ab) / max(ab @ ab, 1e-12), 0, 1); best = np.minimum(best, np.hypot(*(Q - (a + t[:, None] * ab)).T))
    return best
dm, dz = [], []
for w in V["wege"]:
    P = np.asarray(w["mittellinie_m"], float)
    if len(P) < 2 or not w.get("quellzellen"): continue
    Q = np.array([[c % nx + 0.5, c // nx + 0.5] for c in w["quellzellen"]], float)
    dm.append(np.median(dist(P / zw, Q))); dz.append(np.median(dist(P, Q)))
erg = {"zellweite_m": zw, "median_abstand_quellzelle_mittellinie_umgerechnet": round(float(np.median(dm)), 3),
       "median_abstand_meter_als_zellen_alt": round(float(np.median(dz)), 3)}
W = l3.schutz(D, GY, GX, rs, 1.5, True, 0.5, 2.0)
pz = [];  
for w in V["wege"]:
    for c in w.get("quellzellen", []): pz.append((c // nx, c % nx))
for k in V["kreuzungen"]:
    for q in k.get("quellzellen", []): pz.append((q["cy"], q["cx"]))
geschuetzt = [W[int((y + 0.5) * rs), int((x + 0.5) * rs)] == 0.0 for y, x in pz]
erg["quellzellen_wege_kreuzungen"] = len(pz); erg["davon_im_schutz"] = int(sum(geschuetzt))
# Nur der vektor.json-Anteil (WEGA/wege/bruecken/rampen ausgeblendet): deckt er die Quellzellen?
import base64 as _b
Dv = dict(D); Dv["WEGA"] = _b.b64encode(np.zeros(GY * GX, np.uint8).tobytes()).decode(); Dv["wege"] = []; Dv["bruecken"] = []; Dv["rampenwege"] = []
Wv = l3.schutz(Dv, GY, GX, rs, 1.5, False, 0.0, 2.0)
erg["nur_vektor_quellzellen_im_schutz_anteil"] = round(float(np.mean([Wv[int((y + 0.5) * rs), int((x + 0.5) * rs)] == 0.0 for y, x in pz])), 4)
WEGA = np.frombuffer(__import__("base64").b64decode(D["WEGA"]), np.uint8).reshape(GY, GX) > 0
erg["wega_vertices_im_schutz_anteil"] = round(float((W[WEGA] == 0).mean()), 4)
ok = erg["median_abstand_quellzelle_mittellinie_umgerechnet"] < erg["median_abstand_meter_als_zellen_alt"] and erg["median_abstand_quellzelle_mittellinie_umgerechnet"] < 1.0 \
     and erg["davon_im_schutz"] == len(pz) and erg["nur_vektor_quellzellen_im_schutz_anteil"] >= 0.99 and erg["wega_vertices_im_schutz_anteil"] == 1.0
erg["bestanden"] = bool(ok); print(json.dumps(erg, indent=1)); sys.exit(0 if ok else 1)
