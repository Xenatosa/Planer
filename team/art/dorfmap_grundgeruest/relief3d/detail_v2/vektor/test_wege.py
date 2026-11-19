#!/usr/bin/env python3
"""P1a Abnahme fuer wege.geojson / kreuzungen.geojson (aus relief3d/):  python3 detail_v2/vektor/test_wege.py [--json AUS.json]
Q3  Zackenamplitude jeder Randlinie gegen ihre 1-m-Glaettung <= 3 cm, hart mit ZWEI Methoden:
    A (fein): Linie auf 0,05 m nachgetastet, gleitendes Mittel 1 m Bogenlaenge, 0,5 m an offenen Enden ausgenommen;
    B (QA): gleitendes 1-m-Mittel ueber die Stuetzpunkte der Linie selbst (0,25 m -> +-2 Punkte), Enden ausgenommen,
      Kreuzungsringe zyklisch. B ist bei Kurven strenger (Kreisbogen R: A ~ 4,2 cm/R, B ~ 6,25 cm/R).
    Knick zwischen Nachbarsegmenten (0,25-m-Abtastung) <= 15 Grad.
    Geprueft: alle Randlinien (rand_links/rand_rechts) und Kreuzungsumrisse; zusaetzlich getrennt der sichtbare Teil
    (Randlinie ausserhalb der Kreuzungen).
Q14 Mittellinie <= 0,3 m vom alten Verlauf (vektor.json /1,2), beidseitig (Hausdorff).
Luecken: (a) jede nicht freie Wegende liegt in einer Kreuzung oder auf einem anderen Band, (b) Netz-Zusammenhang je
    WEGA>=0,5-Komponente (relief_daten.json.gz) genau ein Netzteil, (c) WEGA>=0,5-Knoten ausserhalb des Netzes (+0,25 m).
Formal: Polygone gueltig, Ringe geschlossen."""
import base64, gzip, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
from shapely.geometry import shape, LineString, Point, Polygon
from shapely.ops import unary_union
import shapely as shp
from shapely import contains_xy

R = Path(__file__).resolve().parents[2]; H = Path(__file__).resolve().parent
ZACK_MAX = 0.03; KNICK_MAX = 15.0; MITTE_MAX = 0.30

def nachtasten(P, s=0.05, ring=False):
    P = np.asarray(P, float)
    if ring and not np.allclose(P[0], P[-1]): P = np.vstack([P, P[:1]])
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    n = max(2, int(round(d[-1] / s)) + 1); u = np.linspace(0, d[-1], n)
    return np.c_[np.interp(u, d, P[:, 0]), np.interp(u, d, P[:, 1])], d[-1] / (n - 1)

def zacken(P, ring=False):
    Q, s = nachtasten(P, 0.05, ring); k = max(1, int(round(0.5 / s)))
    if ring:
        Qr = Q[:-1]; n = len(Qr); idx = (np.arange(n)[:, None] + np.arange(-k, k + 1)[None]) % n
        M = Qr[idx].mean(1); return float(np.hypot(*(Qr - M).T).max())
    if len(Q) <= 2 * k + 1: return 0.0
    c = np.cumsum(np.vstack([[0, 0], Q]), 0); M = (c[2 * k + 1:] - c[:-2 * k - 1]) / (2 * k + 1)
    return float(np.hypot(*(Q[k:len(Q) - k] - M).T).max())

def zacken_b(P, ring=False):
    P = np.asarray(P, float)
    if ring and np.allclose(P[0], P[-1]): P = P[:-1]
    n = len(P)
    if n < 3: return 0.0
    k = max(1, int(round(0.5 / np.hypot(*np.diff(P, axis=0).T).mean())))
    if ring:
        idx = (np.arange(n)[:, None] + np.arange(-k, k + 1)[None]) % n; return float(np.hypot(*(P - P[idx].mean(1)).T).max())
    if n <= 2 * k + 1: return 0.0
    c = np.cumsum(np.vstack([[0, 0], P]), 0); M = (c[2 * k + 1:] - c[:-2 * k - 1]) / (2 * k + 1)
    return float(np.hypot(*(P[k:n - k] - M).T).max())

def knick(P, ring=False):
    P = np.asarray(P, float)
    if ring:
        if np.allclose(P[0], P[-1]): P = P[:-1]
        P = np.vstack([P[-1:], P, P[:1]])
    v = np.diff(P, axis=0); v = v[np.hypot(*v.T) > 1e-6]
    if len(v) < 2: return 0.0
    a = np.degrees(np.arctan2(v[:, 1], v[:, 0])); d = np.abs((np.diff(a) + 180) % 360 - 180); return float(d.max())

def bild(pfad):
    """Uebersicht: alte Draufsicht (VC-Farben der Karte, WEGA>=0,5 rot getoent) + neue Vektoren (Raender schwarz,
    Mittellinien gelb, Kreuzungen blau, WEGA-Ergaenzungen magenta). Links ganze Karte, rechts Ausschnitt Dorfkern."""
    from PIL import Image, ImageDraw
    D = json.load(gzip.open(R / "relief_daten.json.gz")); rs = D["rs"]; GX, GY = D["nx"] * rs + 1, D["ny"] * rs + 1
    VC = np.frombuffer(base64.b64decode(D["VC"]), np.uint8).reshape(GY, GX, 3).astype(float)
    A = np.frombuffer(base64.b64decode(D["WEGA"]), np.uint8).reshape(GY, GX) >= 128
    VC[A] = VC[A] * 0.55 + np.array([200, 40, 40]) * 0.45
    W = json.load(open(H / "wege.geojson")); K = json.load(open(H / "kreuzungen.geojson"))
    def zeichne(px, box):
        x0, z0, x1, z1 = box
        sub = VC[int(z0 * rs):int(z1 * rs) + 1, int(x0 * rs):int(x1 * rs) + 1]
        im = Image.fromarray(sub.astype(np.uint8)).resize((int((x1 - x0) * px), int((z1 - z0) * px)), Image.BILINEAR); d = ImageDraw.Draw(im)
        T = lambda P: [((x - x0) * px, (z - z0) * px) for x, z in P]
        for f in K["features"]:
            d.line(T(f["geometry"]["coordinates"][0]), fill=(30, 90, 230), width=max(1, px // 3))
        for f in W["features"]:
            r = f["properties"]["rolle"]; erg = f["properties"].get("quelle") == "WEGA-Ergaenzung"
            if r in ("rand_links", "rand_rechts"): d.line(T(f["geometry"]["coordinates"]), fill=(200, 0, 200) if erg else (0, 0, 0), width=max(1, px // 3))
            if r == "mittellinie": d.line(T(f["geometry"]["coordinates"]), fill=(255, 215, 0), width=1)
        return im
    a = zeichne(2, (130, 20, 340, 215)); b = zeichne(10, (180, 95, 240, 140))
    c = Image.new("RGB", (a.width + b.width + 10, max(a.height, b.height) + 24), "white"); c.paste(a, (0, 24)); c.paste(b, (a.width + 10, 24))
    ImageDraw.Draw(c).text((4, 5), "P1a Wege: alte Draufsicht (VC, WEGA>=0,5 rot) + neu: Raender schwarz, Mitte gelb, Kreuzungen blau, Ergaenzung magenta | rechts Dorfkern 180-240|95-140", fill="black")
    c.save(pfad, quality=85)

def main():
    if "--bild" in sys.argv: bild(sys.argv[sys.argv.index("--bild") + 1]); return
    W = json.load(open(H / "wege.geojson")); K = json.load(open(H / "kreuzungen.geojson"))
    V = json.load(open(R / "neu" / "vektor.json"))
    kp = [shape(f["geometry"]) for f in K["features"]]; Kall = unary_union(kp)
    erg = {"rand": [], "kreuzung": [], "sichtbar": []}; erg_b = {"rand": [], "kreuzung": []}; fehler = []
    for f in W["features"]:
        if f["properties"]["rolle"] in ("rand_links", "rand_rechts"):
            g = shape(f["geometry"]); P = np.asarray(g.coords)
            erg["rand"].append((zacken(P), knick(P), f["properties"]["id"], f["properties"]["teil"], f["properties"]["rolle"]))
            erg_b["rand"].append((zacken_b(P), f["properties"]["id"], f["properties"]["teil"], f["properties"]["rolle"]))
            vis = g.difference(Kall)
            for v in getattr(vis, "geoms", [vis]):
                if v.is_empty or v.geom_type != "LineString" or v.length < 0.3: continue
                Pv = np.asarray(v.coords); erg["sichtbar"].append((zacken(Pv), knick(Pv[1:-1]) if len(Pv) > 3 else 0.0, f["properties"]["id"], f["properties"]["teil"], f["properties"]["rolle"]))
    for f, g in zip(K["features"], kp):
        if not g.is_valid: fehler.append(f"Kreuzung {f['properties']['id']} ungueltig")
        P = np.asarray(g.exterior.coords); erg["kreuzung"].append((zacken(P, True), knick(P, True), f["properties"]["id"], 0, "umriss"))
        erg_b["kreuzung"].append((zacken_b(P, True), f["properties"]["id"], 0, "umriss"))
    out = {}
    for k, L in erg.items():
        z = max(L, key=lambda t: t[0]); kn = max(L, key=lambda t: t[1])
        out[k] = {"linien": len(L), "zacken_max_m": round(z[0], 4), "zacken_max_bei": z[2:], "knick_max_grad": round(kn[1], 2), "knick_max_bei": kn[2:],
                  "zacken_ueber": sum(t[0] > ZACK_MAX for t in L), "knick_ueber": sum(t[1] > KNICK_MAX for t in L),
                  "zacken_p95_m": round(float(np.percentile([t[0] for t in L], 95)), 4), "knick_p95_grad": round(float(np.percentile([t[1] for t in L], 95)), 2)}
    for k, L in erg.items():
        out[k]["zacken_top5_A_cm"] = [[round(t[0] * 100, 2)] + list(t[2:]) for t in sorted(L, key=lambda t: -t[0])[:5]]
        out[k]["zacken_ueber_2_7cm_A"] = sum(t[0] > 0.027 for t in L)
    for k, L in erg_b.items():
        L = sorted(L, key=lambda t: -t[0])
        out[k + "_methodeB"] = {"linien": len(L), "zacken_max_m": round(L[0][0], 4), "zacken_max_bei": L[0][1:], "zacken_ueber": sum(t[0] > ZACK_MAX for t in L),
                                "zacken_ueber_2_7cm": sum(t[0] > 0.027 for t in L), "zacken_top5_cm": [[round(t[0] * 100, 2)] + list(t[1:]) for t in L[:5]]}
    # Mittellinie gegen alt
    alt = {}
    for w in V["wege"]:
        P = np.asarray(w["mittellinie_m"], float) / 1.2
        if len(P) >= 2: alt[(w["id"], w["teil"])] = LineString(P)
    dmax = 0; dbei = None; erg_ids = []
    for f in W["features"]:
        p = f["properties"]
        if p["rolle"] != "mittellinie": continue
        g = shape(f["geometry"])
        if (p["id"], p["teil"]) not in alt: erg_ids.append(p["id"]); continue   # WEGA-Ergaenzung: eigener Test unten
        a = alt[(p["id"], p["teil"])]
        Q, _ = nachtasten(np.asarray(g.coords), 0.05); Qa, _ = nachtasten(np.asarray(a.coords), 0.05)
        d1 = max(a.distance(Point(q)) for q in Q[::2]); d2 = max(g.distance(Point(q)) for q in Qa[::2]); d = max(d1, d2)
        if d > dmax: dmax, dbei = d, (p["id"], p["teil"])
    out["mittellinie"] = {"max_abweichung_m": round(dmax, 4), "bei": dbei}
    # Luecken (a) Wegenden
    baender = [(f["properties"], shape(f["geometry"])) for f in W["features"] if f["properties"]["rolle"] == "band"]
    mitte = {(f["properties"]["id"], f["properties"]["teil"]): shape(f["geometry"]) for f in W["features"] if f["properties"]["rolle"] == "mittellinie"}
    offen = []
    for (pr, b) in baender:
        L = mitte[(pr["id"], pr["teil"])]
        for seite, frei in ((0, pr["frei_anfang"]), (1, pr["frei_ende"])):
            if frei: continue
            p = Point(L.coords[0] if seite == 0 else L.coords[-1])
            if Kall.buffer(1e-6).contains(p): continue
            if any(b2.contains(p) for (p2, b2) in baender if (p2["id"], p2["teil"]) != (pr["id"], pr["teil"])): continue
            offen.append((pr["id"], pr["teil"], seite))
    netz = [shape(f["geometry"]) for f in W["features"] if f["properties"]["rolle"] == "netz"][0]
    teile = list(getattr(netz, "geoms", [netz]))
    # (b)/(c) WEGA
    D = json.load(gzip.open(R / "relief_daten.json.gz")); rs = D["rs"]; GX, GY = D["nx"] * rs + 1, D["ny"] * rs + 1
    A = np.frombuffer(base64.b64decode(D["WEGA"]), np.uint8).reshape(GY, GX); M = A >= 128
    zz, xx = np.nonzero(M); x = xx / rs; z = zz / rs
    nb = netz.buffer(0.25); innen = contains_xy(nb, x, z)
    lab, n = nd.label(M, structure=np.ones((3, 3)))
    aussen = np.zeros_like(M); aussen[zz[~innen], xx[~innen]] = True; la, na = nd.label(aussen, structure=np.ones((3, 3)))
    groesste = int(np.bincount(la.ravel())[1:].max()) if na else 0
    komp = []
    for k in range(1, n + 1):
        sel = lab[zz, xx] == k; ids = set()
        for i, t in enumerate(teile):
            if contains_xy(t.buffer(0.25), x[sel], z[sel]).any(): ids.add(i)
        komp.append(len(ids))
    # Netzteile ohne WEGA
    teile_ohne = sum(1 for t in teile if not contains_xy(t, x, z).any())
    # WEGA-Ergaenzungen: Mittellinie muss in WEGA>=0,5 liegen (Abstand zum naechsten WEGA-Knoten)
    from scipy.spatial import cKDTree
    baum = cKDTree(np.c_[x, z]); erg = {}
    for f in W["features"]:
        p = f["properties"]
        if p["rolle"] == "mittellinie" and p["id"] in erg_ids:
            Q, _ = nachtasten(np.asarray(f["geometry"]["coordinates"]), 0.25); d, _ = baum.query(Q)
            erg[p["id"]] = {"klasse": p["klasse"], "laenge_m": round(shape(f["geometry"]).length, 2), "max_abstand_zu_wega_m": round(float(d.max()), 3)}
    out["ergaenzungen"] = erg
    out["luecken"] = {"offene_wegenden": offen, "netz_teile": len(teile), "wega_komponenten": int(n),
                      "wega_komponenten_mit_mehr_als_einem_netzteil": int(sum(c > 1 for c in komp)), "wega_komponenten_ohne_netz": int(sum(c == 0 for c in komp)),
                      "netzteile_ohne_wega": teile_ohne,
                      "wega_knoten": int(M.sum()), "wega_knoten_ausserhalb_netz": int((~innen).sum()), "groesster_ausserhalb_cluster_knoten": groesste,
                      "wega_abdeckung": round(float(innen.mean()), 4)}
    # Raender vs Offset +-Breite/2 (Abweichung = |Abstand zur Mittellinie - Breite/2|; Innenrundung r und Ringglaettung erlaubt)
    dv = []
    for f in W["features"]:
        p = f["properties"]
        if p["rolle"] in ("rand_links", "rand_rechts"):
            L = mitte[(p["id"], p["teil"])]; Q = np.asarray(f["geometry"]["coordinates"])
            dv.append(np.abs(shp.distance(L, shp.points(Q)) - p["breite"] / 2))
    dv = np.concatenate(dv)
    out["rand_offset"] = {"p50_m": round(float(np.percentile(dv, 50)), 4), "p95_m": round(float(np.percentile(dv, 95)), 4), "max_m": round(float(dv.max()), 3),
                          "anteil_unter_2cm": round(float((dv <= 0.02).mean()), 4)}
    # Platzanschluss: Wegenden <= 1,5 m an einer Platzzelle (Overlay) liegen in einer Kreuzung (weg_platz) oder auf dem Platz
    import csv
    pl = [(int(r["cx"]), int(r["cy"])) for r in csv.DictReader(open(R.parent / "raster_c20_z25_overlay_plaetze_wege.csv")) if r["platz"]]
    platz = unary_union([Polygon([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]) for x, y in pl])
    nah = 0; offen_platz = []; ueberlapp = []; bandd = {(pr["id"], pr["teil"]): b for pr, b in baender}; ziel = unary_union([platz, Kall])
    for (pid, teil), L in mitte.items():
        brt = [pr["breite"] for pr, b in baender if (pr["id"], pr["teil"]) == (pid, teil)][0]
        for q in (L.coords[0], L.coords[-1]):
            P_ = Point(q)
            if P_.distance(platz) > 1.5: continue
            nah += 1
            kappe = bandd[(pid, teil)].intersection(P_.buffer(brt / 2 + 0.3)); a_ = kappe.intersection(ziel).area; ueberlapp.append(a_)
            if a_ < 0.05: offen_platz.append((pid, teil, [round(q[0], 1), round(q[1], 1)], round(a_, 3)))
    # Kreuzungseinpassung: Ueberstand der Kreuzungsumrisse ueber Bandnetz/Platz (Eckausrundung zwischen Armen liegt aussen)
    ziel_k = unary_union([b for _, b in baender] + [platz]); shp.prepare(ziel_k); ue = []
    for f in K["features"]:
        C = np.asarray(shape(f["geometry"]).exterior.coords); ue.append((float(shp.distance(ziel_k, shp.points(C)).max()), f["properties"]["id"]))
    ue.sort(reverse=True)
    out["kreuzung_ueberstand"] = {"max_m": round(ue[0][0], 3), "bei": ue[0][1], "p50_m": round(float(np.median([u for u, _ in ue])), 3), "grenze_m": 1.5, "grund": "Dorfmap-Entscheid zu #56; Eckradius >= 2,35 m (Zacken B <= 2,7 cm) bei 2-3 m breiten Wegen"}
    out["platzanschluss"] = {"kriterium": "Wegende <= 1,5 m an Platzzelle: Bandkappe (Band im Kreis Breite/2+0,3 m um das Ende) ueberlappt Platz oder Kreuzung >= 0,05 m2 (keine Luecke)",
                             "wegenden_am_platz": nah, "min_ueberlappung_m2": round(min(ueberlapp), 3) if ueberlapp else None, "nicht_angeschlossen": offen_platz}
    # Randvollstaendigkeit: je Weg genau eine rand_links und eine rand_rechts, je >= 40 % der Mittellinienlaenge
    # (Innenrand enger Kurven ist kuerzer); Band ohne Fuellklumpen: Flaeche <= 1,15 x (L*b + Kappen)
    from collections import defaultdict
    rl = defaultdict(list); bf = {}
    for f in W["features"]:
        p = f["properties"]
        if p["rolle"] in ("rand_links", "rand_rechts"): rl[(p["id"], p["teil"], p["rolle"])].append(LineString(f["geometry"]["coordinates"]).length)
        if p["rolle"] == "band": bf[(p["id"], p["teil"])] = (shape(f["geometry"]).area, p["breite"])
    unvoll = []; qmin = 9; amax = 0
    for (pid, teil), L in mitte.items():
        for r in ("rand_links", "rand_rechts"):
            ls = rl.get((pid, teil, r), []); q = sum(ls) / L.length; qmin = min(qmin, q)
            if len(ls) != 1 or q < 0.4: unvoll.append((pid, teil, r, len(ls), round(q, 2)))
        A, b_ = bf[(pid, teil)]; a_ = A / (L.length * b_ + np.pi * b_ * b_ / 4); amax = max(amax, a_)
        if a_ > 1.15: unvoll.append((pid, teil, "band_klumpen", round(a_, 2)))
    out["randvollstaendigkeit"] = {"min_randlaenge_zu_mittellinie": round(qmin, 3), "max_bandflaeche_zu_soll": round(amax, 3), "maengel": unvoll}
    out["formal"] = {"fehler": fehler, "netz_gueltig": bool(netz.is_valid)}
    ok = (out["rand_methodeB"]["zacken_max_m"] <= ZACK_MAX and out["kreuzung_methodeB"]["zacken_max_m"] <= ZACK_MAX
          and out["rand"]["zacken_max_m"] <= ZACK_MAX and out["rand"]["knick_max_grad"] <= KNICK_MAX and out["kreuzung"]["zacken_max_m"] <= ZACK_MAX
          and out["kreuzung"]["knick_max_grad"] <= KNICK_MAX and out["mittellinie"]["max_abweichung_m"] <= MITTE_MAX and not offen
          and out["luecken"]["wega_komponenten_mit_mehr_als_einem_netzteil"] == 0 and not fehler and not offen_platz and not unvoll and ue[0][0] <= 1.5)
    out["bestanden"] = bool(ok)
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    if "--json" in sys.argv: json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1, ensure_ascii=False, default=str)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
