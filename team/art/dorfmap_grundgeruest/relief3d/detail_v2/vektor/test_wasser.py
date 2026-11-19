#!/usr/bin/env python3
"""Abnahme P1b/P1b2/P1b3 (DETAIL_V2_PLAN Q3, Q14): prueft wasser.geojson, ufer.geojson, bach_mitte.geojson.

  python3 detail_v2/vektor/test_wasser.py            (oder: pytest detail_v2/vektor/test_wasser.py)
Mit Paket (DV2_PAKET=/tmp/dv2_wasser/alle_kacheln.json.gz, Standard) wird die Ist-Flaeche aus WV neu gezaehlt und zusaetzlich
geprueft, dass keine nasse Ecke > 0,3 m ausserhalb des Vektorwassers liegt (P1b2-Vorgabe). Ohne Paket gelten die festgehaltenen Ist-Werte.
Eigene Messung (unabhaengig vom Extraktor):
  Zacke = max. Abstand der Linie (5 cm abgetastet) zu ihrem GLEITENDEN 1-m-MITTEL ueber die Bogenlaenge (QA-Messung,
          Trapezgewichte = stetiges Mittel ueber genau 1 m, nicht Punktzahl) <= 3 cm; gilt fuer Ufer- UND Mittellinien.
          Savitzky-Golay (1 m, Ordnung 2) wird nur als Zusatzinfo ausgegeben.
  Knick = max. Richtungsaenderung zwischen Nachbarsegmenten <= 15 Grad
  P1b3: QA-q3 aus #55 @38fa7ec wird IMPORTIERT und aufgerufen (nicht nachgebaut): 0 Funde in ufer.geojson; dieselbe QA-Funktion
        glaettung_abw zusaetzlich fuer Mittellinien und Wasserringe (Punkte > 1 m vom Kartenrand; die Kartenecken sind kein Ufer).
        QA-Code: DV2_QA=<.../detail_v2/qa> oder detail_v2/qa im Repo (nach Merge von #55); sonst
        git archive 38fa7ec team/art/dorfmap_grundgeruest/relief3d/detail_v2/qa | tar -x -C /tmp/dv2_wasser/qa
        Flaeche und Hausdorff zu #58 (git show 10875b1): Flaeche +-1 %, Hausdorff < 1 cm.
  Flaeche gesamt, E2, E3 je +-3 % zum Ist; alle Polygone shapely is_valid; Gewaesser (verschiedener Spiegel) ueberlappen nicht.
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
ZACKE_MAX, KNICK_MAX, FLAECHE_PROZ, ABDECK_TOL = 0.03, 15.0, 3.0, 0.3
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
    """Abstand zum gleitenden 1-m-Mittel (Bogenlaenge)."""
    Q = abtasten(C, 0.05, zu)
    if len(Q) < 25: return 0.0
    k = np.ones(21); k[0] = k[-1] = 0.5; k /= k.sum()
    if zu:
        pad = np.vstack([Q[-21:], Q, Q[:21]])
        G = np.column_stack([np.convolve(pad[:, i], k, "same")[21:-21] for i in range(2)]); ref = Q
    else:
        G = np.column_stack([np.convolve(Q[:, i], k, "valid") for i in range(2)]); ref = Q[10:len(Q) - 10]
    return float(np.hypot(*(ref - G).T).max())


def zacke_sg(C, zu):
    """nur Zusatzinfo"""
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
    F = lade("wasser.geojson"); W = [shape(f["geometry"]) for f in F]
    bander = [shape(f["geometry"]) for f in lade("ufer.geojson") if f["properties"]["typ"] == "uferband"]
    assert W and all(g.is_valid for g in W) and all(g.is_valid for g in bander)
    for a in range(len(W)):
        for b in range(a + 1, len(W)):
            assert W[a].intersection(W[b]).area < 1e-6, (F[a]["properties"]["id"], F[b]["properties"]["id"])
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


QA_KANDIDATEN = [os.environ.get("DV2_QA", ""), str(HIER.parent / "qa"),
                 "/tmp/dv2_wasser/qa/team/art/dorfmap_grundgeruest/relief3d/detail_v2/qa"]
REF58 = "10875b1"                                             # Merge #58 (P1b2)


def qa_modul():
    for k in QA_KANDIDATEN:
        if k and (Path(k) / "dv2qa" / "regeln_a.py").exists():
            if k not in sys.path: sys.path.insert(0, k)
            from dv2qa.welt import Kontext
            from dv2qa import regeln_a
            from dv2qa.geom import glaettung_abw
            return Kontext, regeln_a, glaettung_abw
    raise AssertionError("QA-Code (#55 @38fa7ec) nicht gefunden – DV2_QA setzen")


def test_qa_q3_importiert():
    Kontext, regeln_a, _ = qa_modul()
    ctx = Kontext(HIER.parent)
    ctx.k["q3_quellen"] = [q for q in ctx.k["q3_quellen"] if q["datei"] == "ufer.geojson"]   # nur eigene Datei bewerten
    r = regeln_a.q3(ctx)
    assert r["befunde_anzahl"] == 0 and r["status"] == "ok", r["befunde"][:10]
    assert r["werte"]["abw_max_m"] <= ZACKE_MAX and r["werte"]["knick_max_grad"] <= KNICK_MAX, r["werte"]


def qa_glaettung_rest():
    """QA-Funktion glaettung_abw auf Mittellinien und Wasserringe -> (max abw, max knick) je Datei."""
    _, _, glaettung_abw = qa_modul(); out = {}
    for f in lade("bach_mitte.geojson"):
        a = np.asarray(f["geometry"]["coordinates"], float); ab, kn = glaettung_abw(a, 1.0, False)
        m = out.setdefault("bach_mitte", [0.0, 0.0]); m[0] = max(m[0], float(ab.max())); m[1] = max(m[1], float(kn.max()) if len(kn) else 0)
    for f in lade("wasser.geojson"):
        for r in f["geometry"]["coordinates"]:
            a = np.asarray(r, float); ab, kn = glaettung_abw(a, 1.0, True); P = a[:-1]
            fern = (P[:, 0] > 1) & (P[:, 0] < 335) & (P[:, 1] > 1) & (P[:, 1] < 302)
            m = out.setdefault("wasser", [0.0, 0.0]); m[0] = max(m[0], float(ab[fern].max())); m[1] = max(m[1], float(kn[fern].max()))
    return out


def test_qa_methode_mittellinien_und_wasserringe():
    for k, (a, kn) in qa_glaettung_rest().items():
        assert a <= ZACKE_MAX and kn <= KNICK_MAX, (k, a, kn)


def vergleich_58():
    import subprocess
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HIER, capture_output=True, text=True).stdout.strip()
    if not top: return None
    rel = HIER.relative_to(Path(top))
    def alt(name):
        r = subprocess.run(["git", "show", f"{REF58}:{rel}/{name}"], cwd=top, capture_output=True, text=True)
        return json.loads(r.stdout)["features"] if r.returncode == 0 else None
    A, U = alt("wasser.geojson"), alt("ufer.geojson")
    if A is None or U is None: return None
    fa = unary_union([shape(f["geometry"]) for f in A]).area; fn = unary_union([shape(f["geometry"]) for f in lade("wasser.geojson")]).area
    ua = [shape(f["geometry"]) for f in U if f["properties"]["typ"] == "uferlinie"]
    un = [shape(f["geometry"]) for f in lade("ufer.geojson") if f["properties"]["typ"] == "uferlinie"]
    wa = [shape(f["geometry"]).boundary for f in A]; wn = [shape(f["geometry"]).boundary for f in lade("wasser.geojson")]
    h = max([a.hausdorff_distance(b) for a, b in zip(ua, un)] + [a.hausdorff_distance(b) for a, b in zip(wa, wn)])
    return fa, fn, h, len(ua) == len(un) and len(wa) == len(wn)


def test_gegen_58():
    v = vergleich_58()
    if v is None: return
    fa, fn, h, gleich = v
    assert gleich and abs(fn - fa) / fa <= 0.01 and h < 0.01, v


if __name__ == "__main__":
    fehler = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try: fn(); print("OK  ", name)
            except AssertionError as ex: fehler += 1; print("FAIL", name, ex)
    L = linien(); W = [shape(f["geometry"]) for f in lade("wasser.geojson")]
    U = [x for x in L if x[3]["typ"] == "uferlinie"]; M = [x for x in L if x[3]["typ"] == "bach_mitte"]
    for i, C, zu, _ in U: print(f"  {i:8s} Zacke gleitendes Mittel {100 * zacke(C, zu):.2f} cm  Knick {knick(C, zu):.2f} Grad")
    print(json.dumps({"uferlinien": len(U), "mittellinien": len(M), "polygone": len(W),
                      "ufer_zacke_max_m": round(max(zacke(C, zu) for _, C, zu, _ in U), 4),
                      "mitte_zacke_max_m": round(max(zacke(C, zu) for _, C, zu, _ in M), 4),
                      "knick_max_grad": round(max(knick(C, zu) for _, C, zu, _ in L), 2),
                      "zacke_sg_max_m_info": round(max(zacke_sg(C, zu) for _, C, zu, _ in L), 4), "paket": PAKET.exists()}))
    try:
        Kontext, regeln_a, _ = qa_modul(); ctx = Kontext(HIER.parent)
        ctx.k["q3_quellen"] = [q for q in ctx.k["q3_quellen"] if q["datei"] == "ufer.geojson"]; r = regeln_a.q3(ctx)
        print(json.dumps({"qa_q3_ufer": r["status"], "funde": r["befunde_anzahl"], **r["werte"],
                          "qa_methode_rest": {k: [round(a, 4), round(b, 2)] for k, (a, b) in qa_glaettung_rest().items()}}, ensure_ascii=False))
        v = vergleich_58()
        if v: print(json.dumps({"flaeche_58_m2": round(v[0], 3), "flaeche_neu_m2": round(v[1], 3), "abw_prozent": round(100 * (v[1] - v[0]) / v[0], 4), "hausdorff_58_mm": round(1000 * v[2], 2)}))
    except AssertionError as ex:
        print("QA:", ex)
    sys.exit(1 if fehler else 0)
