#!/usr/bin/env python3
"""Abnahme P1b (DETAIL_V2_PLAN Q3, Q14): prueft wasser.geojson, ufer.geojson, bach_mitte.geojson.

  python3 detail_v2/vektor/test_wasser.py            (oder: pytest detail_v2/vektor/test_wasser.py)
Mit Paket (DV2_PAKET=/tmp/dv2_wasser/alle_kacheln.json.gz, Standard) wird die Ist-Flaeche aus WV neu gezaehlt und zusaetzlich
geprueft, dass jede nasse Ecke im Vektorwasser liegt (Toleranz halbe Zelle 0,25 m). Ohne Paket gelten die festgehaltenen Ist-Werte.
Eigene Messung (unabhaengig vom Extraktor):
  Zacke = max. Abstand der Linie (5 cm abgetastet) zu ihrer 1-m-Glaettung (Savitzky-Golay, 1 m Fenster, Ordnung 2) <= 3 cm
  Knick = max. Richtungsaenderung zwischen Nachbarsegmenten <= 15 Grad
  Flaeche gesamt, E2, E3 je +-3 % zum Ist; alle Polygone shapely is_valid; Gewaesser ueberlappen nicht.
"""
import base64, gzip, json, os, sys
from pathlib import Path
import numpy as np
import shapely
from shapely.geometry import shape, box
from shapely.ops import unary_union
from scipy.signal import savgol_filter

HIER = Path(__file__).resolve().parent
PAKET = Path(os.environ.get("DV2_PAKET", "/tmp/dv2_wasser/alle_kacheln.json.gz"))
ZACKE_MAX, KNICK_MAX, FLAECHE_PROZ, ABDECK_TOL = 0.03, 15.0, 3.0, 0.25
IST_FEST = {"gesamt": 6461.25, "E2": 102.5, "E3": 148.25}     # nasse Ecken x 0,25 m2, Stand art/dorfmap-fertig d2d4824
KACHELN = {"E2": (168, 43, 210, 86), "E3": (168, 86, 210, 129)}


def lade(name):
    d = json.load(open(HIER / name, encoding="utf-8"))
    assert d["type"] == "FeatureCollection"
    return d["features"]


def abtasten(C, step, zu):
    if zu: C = np.vstack([C, C[:1]])
    s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(C, axis=0).T))])
    n = max(int(round(s[-1] / step)), 2); t = np.linspace(0, s[-1], n + 1)
    Q = np.column_stack([np.interp(t, s, C[:, 0]), np.interp(t, s, C[:, 1])])
    return Q[:-1] if zu else Q


def zacke(C, zu):
    Q = abtasten(C, 0.05, zu)
    if len(Q) < 25: return 0.0
    G = np.column_stack([savgol_filter(Q[:, i], 21, 2, mode="wrap" if zu else "interp") for i in range(2)])
    return float(np.hypot(*(Q - G).T).max())


def knick(C, zu):
    P = np.vstack([C, C[:2]]) if zu else C
    v = np.diff(P, axis=0); v = v[np.hypot(*v.T) > 1e-9]
    if len(v) < 2: return 0.0
    a = np.degrees(np.arctan2(v[:, 1], v[:, 0]))
    return float(np.abs((np.diff(a) + 180) % 360 - 180).max())


def linien():
    out = []
    for f in [f for f in lade("ufer.geojson") if f["properties"]["typ"] == "uferlinie"] + lade("bach_mitte.geojson"):
        C = np.asarray(f["geometry"]["coordinates"], float); zu = bool(f["properties"].get("geschlossen"))
        if zu and np.allclose(C[0], C[-1]): C = C[:-1]
        out.append((f["properties"]["id"], C, zu, f["properties"]))
    return out


def nass_ecken():
    if not PAKET.exists(): return None
    d = json.load(gzip.open(PAKET)); ny, nx = d["ny"] * d["rs"] + 1, d["nx"] * d["rs"] + 1
    WV = np.frombuffer(base64.b64decode(d["WV"]), np.float32).reshape(ny, nx)
    zz, xx = np.nonzero(WV > -900)
    return xx / d["rs"], zz / d["rs"], 1.0 / d["rs"] ** 2


def test_zacke_und_knick():
    schlecht = [(i, round(zacke(C, zu), 4), round(knick(C, zu), 2)) for i, C, zu, _ in linien()]
    schlecht = [s for s in schlecht if s[1] > ZACKE_MAX or s[2] > KNICK_MAX]
    assert not schlecht, f"Q3 verletzt: {schlecht[:10]}"


def test_attribute_je_punkt():
    for i, C, zu, p in linien():
        n = len(C) + (1 if zu else 0)
        assert len(p["spiegel_m"]) == n, i
        if p["typ"] == "bach_mitte":
            assert len(p["breite_m"]) == n and min(p["breite_m"]) > 0, i


def test_polygone_valid_und_getrennt():
    W = [shape(f["geometry"]) for f in lade("wasser.geojson")]
    bander = [shape(f["geometry"]) for f in lade("ufer.geojson") if f["properties"]["typ"] == "uferband"]
    assert W and all(g.is_valid for g in W) and all(g.is_valid for g in bander)
    for a in range(len(W)):
        for b in range(a + 1, len(W)):
            assert W[a].intersection(W[b]).area < 1e-6, (a, b)
    wu = unary_union(W)
    for g in bander: assert g.intersection(wu).area < 1e-4          # Band liegt landseitig


def test_flaeche():
    wu = unary_union([shape(f["geometry"]) for f in lade("wasser.geojson")])
    e = nass_ecken(); ist = dict(IST_FEST)
    if e is not None:
        x, z, a = e; ist["gesamt"] = len(x) * a
        for k, (x0, z0, x1, z1) in KACHELN.items(): ist[k] = float(((x >= x0) & (x < x1) & (z >= z0) & (z < z1)).sum() * a)
    vek = {"gesamt": wu.area, **{k: wu.intersection(box(*b)).area for k, b in KACHELN.items()}}
    for k in ist:
        abw = 100 * (vek[k] - ist[k]) / ist[k]
        assert abs(abw) <= FLAECHE_PROZ, f"Q14 {k}: {abw:.2f} %"


def test_kein_wasser_entfernt():
    e = nass_ecken()
    if e is None: return
    x, z, _ = e
    wu = unary_union([shape(f["geometry"]) for f in lade("wasser.geojson")])
    d = shapely.distance(wu, shapely.points(x, z))
    assert d.max() <= ABDECK_TOL, f"nasse Ecke {d.max():.3f} m neben dem Wasser"


if __name__ == "__main__":
    fehler = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try: fn(); print("OK  ", name)
            except AssertionError as ex: fehler += 1; print("FAIL", name, ex)
    L = linien(); W = [shape(f["geometry"]) for f in lade("wasser.geojson")]
    print(json.dumps({"linien": len(L), "polygone": len(W), "zacke_max_m": round(max(zacke(C, zu) for _, C, zu, _ in L), 4),
                      "knick_max_grad": round(max(knick(C, zu) for _, C, zu, _ in L), 2), "paket": PAKET.exists()}))
    sys.exit(1 if fehler else 0)
