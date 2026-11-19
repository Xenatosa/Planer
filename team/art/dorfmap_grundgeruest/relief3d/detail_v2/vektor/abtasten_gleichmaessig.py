#!/usr/bin/env python3
"""P1b3: gleichmaessige Abtastung 0,05 m entlang der #58-Geometrie, ohne Douglas-Peucker-Ausduennung, ohne Nachglaetten.

Ursache P1b3: #58 hatte nach dem 5-cm-Resampling noch eine 1-mm-DP-Ausduennung -> ungleich verteilte Stuetzpunkte; QA q3 (#55)
mittelt die Stuetzpunkte im +-0,5-m-Fenster, dichte Punkte in Kurven ziehen das Mittel dann zu weit nach innen.
Hier: jede Linie / jeder Ring wird entlang seines Polygonzugs exakt gleichmaessig abgetastet (Abstand L/n, n = round(L/0,05)).
  - offene Linien: Endpunkte bleiben;
  - Ringe ohne feste Ecken: geschlossen gleichmaessig;
  - Ringe mit festen Ecken (Kartenrand, Knick > 20 Grad wie an Band-/Kartenrand-Schnitten): Ecken bleiben, Stuecke dazwischen gleichmaessig.
Punkt-Attribute (spiegel_m, breite_m) werden nach Bogenlaenge linear uebertragen.
Uferbaender: nach dem Abtasten wird das neue Wasser abgezogen, damit die Bandinnenkante exakt die Wasser-Stuetzpunkte traegt
(sonst kreuzen sich die Sehnen von Band und Wasser um < 1 mm).
  python3 detail_v2/vektor/abtasten_gleichmaessig.py [--ordner detail_v2/vektor]   (laeuft auch am Ende von extrahiere_wasser.py)
"""
import argparse, json
from pathlib import Path
import numpy as np

HIER = Path(__file__).resolve().parent
SCHRITT = 0.05
KARTE = (336.0, 303.0)
ECKE_GRAD = 20.0
DATEIEN = ("wasser.geojson", "ufer.geojson", "bach_mitte.geojson")
PUNKT_ATTR = ("spiegel_m", "breite_m")


def bogen(P):
    return np.concatenate([[0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])


def stueck(P):
    """offenes Stueck gleichmaessig, Endpunkte exakt; gibt auch die Bogenlaengen-Parameter (alt) der neuen Punkte zurueck."""
    s = bogen(P); L = s[-1]
    n = max(int(round(L / SCHRITT)), 1)
    t = np.linspace(0, L, n + 1)
    Q = np.column_stack([np.interp(t, s, P[:, 0]), np.interp(t, s, P[:, 1])]); Q[0], Q[-1] = P[0], P[-1]
    return Q, t, s


def ring(R):
    """R geschlossen (erster = letzter Punkt)."""
    R = np.asarray(R, float)
    P = R[:-1]
    W, H = KARTE; tol = 1e-6
    rand = (np.abs(P[:, 0]) < tol) | (np.abs(P[:, 0] - W) < tol) | (np.abs(P[:, 1]) < tol) | (np.abs(P[:, 1] - H) < tol)
    v1 = P - np.roll(P, 1, axis=0); v2 = np.roll(P, -1, axis=0) - P
    c = (v1 * v2).sum(1) / (np.hypot(*v1.T) * np.hypot(*v2.T) + 1e-15)
    fest = rand | (np.degrees(np.arccos(np.clip(c, -1, 1))) > ECKE_GRAD)
    if not fest.any():
        Q, _, _ = stueck(R)
        return Q                                          # letzter = erster
    st = int(np.argmax(fest)); P = np.roll(P, -st, axis=0); fest = np.roll(fest, -st)
    P = np.vstack([P, P[:1]]); fest = np.append(fest, True)
    idx = np.nonzero(fest)[0]; out = [P[0]]
    for a, b in zip(idx[:-1], idx[1:]):
        Q, _, _ = stueck(P[a:b + 1]); out.extend(Q[1:])
    return np.asarray(out)


def linie(f):
    C = np.asarray(f["geometry"]["coordinates"], float)
    Q, t, s = stueck(C)                                   # geschlossene Uferlinien: Start = Ende bleibt, also ebenfalls korrekt
    pr = f["properties"]
    for a in PUNKT_ATTR:
        if a in pr and isinstance(pr[a], list) and len(pr[a]) == len(C):
            pr[a] = np.round(np.interp(t, s, np.asarray(pr[a], float)), 3).tolist()
    f["geometry"]["coordinates"] = np.round(Q, 4).tolist()


def flaeche(f):
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    neu = [[np.round(ring(r), 4).tolist() for r in poly] for poly in polys]
    g["coordinates"] = neu[0] if g["type"] == "Polygon" else neu


def punkte(g):
    t = g["type"]
    if t == "LineString": return len(g["coordinates"])
    if t == "Polygon": return sum(len(r) for r in g["coordinates"])
    if t == "MultiPolygon": return sum(len(r) for p in g["coordinates"] for r in p)
    if t == "GeometryCollection": return sum(punkte(x) for x in g["geometries"])
    return 0


def bearbeite(ordner):
    from shapely.geometry import shape, mapping
    from shapely.ops import unary_union
    import shapely
    ordner = Path(ordner); n = {}; wasser = None
    for name in DATEIEN:
        p = ordner / name; d = json.load(open(p, encoding="utf-8"))
        for f in d["features"]:
            t = f["geometry"]["type"]
            if t == "LineString": linie(f)
            elif t in ("Polygon", "MultiPolygon"): flaeche(f)
            elif t == "GeometryCollection":            # Uferband als Sammlung (Flaechen + Restkanten aus difference)
                for gg in f["geometry"]["geometries"]:
                    if gg["type"] in ("Polygon", "MultiPolygon"): flaeche({"geometry": gg})
            if f["properties"].get("typ") == "uferband" and wasser is not None:
                g = shape(f["geometry"])
                g = unary_union([x for x in getattr(g, "geoms", [g]) if x.geom_type in ("Polygon", "MultiPolygon")]).difference(wasser)
                if not g.is_valid: g = shapely.make_valid(g)
                g = shapely.set_precision(g, 1e-4)
                f["geometry"] = mapping(g); f["properties"]["flaeche_m2"] = round(g.area, 3)
        if name == "wasser.geojson":
            wasser = shapely.set_precision(unary_union([shape(f["geometry"]) for f in d["features"]]), 1e-4)
        d["abtastung"] = "gleichmaessig 0,05 m entlang der #58-Geometrie, ohne DP (P1b3)"
        p.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        n[name] = sum(punkte(f["geometry"]) for f in d["features"])
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--ordner", default=str(HIER))
    print(json.dumps(bearbeite(ap.parse_args().ordner)))
