#!/usr/bin/env python3
"""P1b detail_v2 (DETAIL_V2_PLAN 3.1): Wasser-/Uferlinien, Uferbaender und Bach-Mittellinien als GeoJSON in Viewer-Metern.

Koordinaten: [x, z] in Viewer-Einheiten (1 Einheit = 1 Zelle; Gitterpunkt (Zeile r, Spalte c) liegt bei x = c/2, z = r/2).
Quelle: WV (Spiegel, -999 = Land) und GB (Boden) aus dem alle_kacheln-Paket:
    python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/dv2_wasser
Verfahren:
  1. DS = Spiegel - Boden; Spiegel auf Land = Spiegel der naechsten nassen Ecke. Damit kein Wasser verloren geht und kein neues entsteht,
     wird DS auf nassen Ecken auf >= +2 cm und auf trockenen auf <= -2 cm geklemmt (die Maske bleibt die Wahrheit, die Lage der Linie
     zwischen nasser und trockener Ecke folgt dem Gelaende).
  2. Marching Squares (skimage.measure.find_contours, Level 0).
  3. Die Rasterkontur folgt noch der 0,5-m-Treppe (E2/E3). Darum je Ring: gleichmaessig 0,1 m abtasten, laengs gaussgeglaettet
     (sigma 0,6 m, geschlossen), dann Douglas-Peucker 0,05 m und Chaikin 2x (Plan 3.1).
  3b. P1b2 (QA misst Q3 mit gleitendem 1-m-Mittel): je Gewaesser Kruemmungsradius >= 1,6 m nur durch Hinzufuegen von Wasser
     (sparsame Kreise R 1,6 an zu engen Spitzen und an nassen Ecken > 0,27 m ausserhalb, dann Schliessen R 1,6, Union mit Original),
     siehe ausrunden(); ersetzt die Kapseln aus P1b.
  4. Polygone: Ringe nach Verschachtelung (gerade Tiefe = Ufer aussen, ungerade = Insel) zu Polygonen mit Loechern; shapely make_valid nur falls noetig.
  5. Uferband = landseitiger Puffer 2,5 m minus Wasser. Uferlinien tragen die Spiegelhoehe je Punkt (spiegel_m).
  6. Bach-Mittellinien: Wasser bei 0,25 m gerastert, skeletonize, Skelett in Polylinien zerlegt (Aeste < 2 m weg), geglaettet wie 3.,
     Breite je Punkt = 2 x Distanzfeld (breite_m).
Ausgabe: detail_v2/vektor/wasser.geojson, ufer.geojson, bach_mitte.geojson, extrahiere_wasser_bericht.json, uebersicht_wasser.jpg.
  python3 detail_v2/vektor/extrahiere_wasser.py [--paket /tmp/dv2_wasser/alle_kacheln.json.gz]
"""
import argparse, base64, gzip, json, math
from pathlib import Path
import numpy as np
from scipy import ndimage as nd
from skimage import measure, morphology, draw
import shapely
import shapely.ops
from shapely.geometry import Polygon, LineString, MultiPolygon, mapping, Point
from shapely.ops import unary_union

HIER = Path(__file__).resolve().parent
RS = 2
KACHEL_X, KACHEL_Z = 42, 43           # Kachelgroesse in Zellen (A-H x 1-7)
DS_KLEMME = 0.02
ABTAST = 0.1
SIGMA_M = 0.35
DP_TOL = 0.05
BAND_M = 2.5
SKEL_PX = 0.25
AST_MIN_M = 2.0
LOCH_MIN_M2 = 0.25
RAND_PAD = 4                          # Gitterpunkte (= 2 m)
KAPSEL_R = 0.3
AUSRUND_R = 1.6                       # P1b2: Mindest-Kruemmungsradius der Uferlinien
AUSRUND_PRUEF = 1.7                   # Pruefradius mit Reserve
SCHLIESS_R = 0.6                      # Ausrundung der Kapselansaetze
ABDECK_TOL = 0.3                      # P1b2-Vorgabe: kein nasser Rasterpunkt > 0,3 m ausserhalb


def lade(paket):
    d = json.load(gzip.open(paket)); ny, nx = d["ny"] * d["rs"] + 1, d["nx"] * d["rs"] + 1
    GB = np.frombuffer(base64.b64decode(d["GB"]), np.float32).reshape(ny, nx).astype(np.float64)
    WV = np.frombuffer(base64.b64decode(d["WV"]), np.float32).reshape(ny, nx).astype(np.float64)
    return GB, WV


def kachel(x, z):
    return "ABCDEFGH"[min(int(x // KACHEL_X), 7)] + str(min(int(z // KACHEL_Z), 6) + 1)


def resample(P, step, closed):
    if closed and not np.allclose(P[0], P[-1]): P = np.vstack([P, P[:1]])
    seg = np.hypot(*np.diff(P, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)]); L = s[-1]
    if L < step * 2: return P[:-1] if closed else P
    n = max(int(round(L / step)), 3); t = np.linspace(0, L, n + 1)
    Q = np.column_stack([np.interp(t, s, P[:, 0]), np.interp(t, s, P[:, 1])])
    return Q[:-1] if closed else Q


def gauss_linie(Q, sigma_pts, closed):
    if sigma_pts <= 0 or len(Q) < 5: return Q
    mode = "wrap" if closed else "nearest"
    R = np.column_stack([nd.gaussian_filter1d(Q[:, k], sigma_pts, mode=mode) for k in range(2)])
    if not closed: R[0], R[-1] = Q[0], Q[-1]          # Enden festhalten
    return R


def ringflaeche(Q):
    x, z = Q[:, 0], Q[:, 1]
    return 0.5 * float(np.dot(x, np.roll(z, -1)) - np.dot(z, np.roll(x, -1)))   # vorzeichenbehaftet


def flaeche_erhalten(Q, A_soll):
    """Glaettung schrumpft konvexe Spitzen; Ring entlang seiner Normalen um (A_soll - A)/Umfang versetzen,
    damit kein Wasser verloren geht (Inseln entsprechend). Zwei Durchgaenge reichen auf < 0,1 %."""
    for _ in range(3):
        A = ringflaeche(Q); L = np.hypot(*(np.roll(Q, -1, axis=0) - Q).T).sum()
        if L <= 0 or abs(A) < 1e-9: return Q
        d = (abs(A_soll) - abs(A)) / L
        if abs(d) < 1e-5: break
        t = np.roll(Q, -1, axis=0) - np.roll(Q, 1, axis=0); t /= np.maximum(np.hypot(*t.T), 1e-12)[:, None]
        n = np.column_stack([t[:, 1], -t[:, 0]]) * (1.0 if A > 0 else -1.0)   # nach aussen
        Q = Q + d * n
    return Q


def chaikin(P, n, closed):
    for _ in range(n):
        if closed:
            A = P; B = np.roll(P, -1, axis=0)
            Q = np.empty((2 * len(P), 2)); Q[0::2] = 0.75 * A + 0.25 * B; Q[1::2] = 0.25 * A + 0.75 * B; P = Q
        else:
            A, B = P[:-1], P[1:]
            Q = np.empty((2 * len(A), 2)); Q[0::2] = 0.75 * A + 0.25 * B; Q[1::2] = 0.25 * A + 0.75 * B
            P = np.vstack([P[:1], Q, P[-1:]])
    return P


def glatte_linie(P, closed, sigma_m=SIGMA_M):
    Q = resample(P, ABTAST, closed)
    A0 = ringflaeche(Q) if closed else None
    Q = gauss_linie(Q, sigma_m / ABTAST, closed)
    if closed: Q = flaeche_erhalten(Q, A0)
    g = LineString(np.vstack([Q, Q[:1]]) if closed else Q).simplify(DP_TOL, preserve_topology=False)
    C = np.asarray(g.coords)
    if closed:
        C = C[:-1]
        if len(C) < 3: return None
    elif len(C) < 2: return None
    C = chaikin(C, 2, closed)                        # Plan: Chaikin 2x ...
    for _ in range(4):                               # ... und weiter, solange ein Knick > 12 Grad bleibt (nur bei engen DP-Ecken)
        if knick_max(C, closed) <= 12.0: break
        C = chaikin(C, 1, closed)
    # Nachglaettung: DP+Chaikin laesst an engen Spitzen (Bachenden, R < 0,5 m) Kruemmungsspruenge von 2-6 cm;
    # darum fein (5 cm) abtasten, leicht laengs glaetten (sigma 0,2 m) und verlustarm ausduennen (1 mm).
    Q = resample(C, 0.05, closed)
    Q = gauss_linie(Q, 0.2 / 0.05, closed)
    if closed: Q = flaeche_erhalten(Q, A0)
    for _ in range(15):                              # einzelne Tropfenspitzen (W07, Bachenden): nachglaetten bis Q3 mit Reserve erfuellt
        z, k = zacke_knick(Q, closed)
        if z <= 0.02 and k <= 10.0: break
        Q = resample(gauss_linie(Q, 0.3 / 0.05, closed), 0.05, closed)
        if closed: Q = flaeche_erhalten(Q, A0)
    if closed:
        g = LineString(np.vstack([Q, Q[:1]])).simplify(0.001, preserve_topology=False); C = np.asarray(g.coords)[:-1]
    else:
        C = np.asarray(LineString(Q).simplify(0.001, preserve_topology=False).coords)
    if len(C) < (3 if closed else 2): return None
    return C


def knick_max(C, closed):
    P = np.vstack([C, C[:2]]) if closed else C
    v = np.diff(P, axis=0); n = np.hypot(*v.T); v = v[n > 1e-9]
    if len(v) < 2: return 0.0
    a = np.degrees(np.arctan2(v[:, 1], v[:, 0]))
    return float(np.abs((np.diff(a) + 180) % 360 - 180).max())


def ds_feld(GB, WV):
    nass = WV > -900
    _, (iz, ix) = nd.distance_transform_edt(~nass, return_indices=True)
    S = WV[iz, ix]                                   # Spiegel ueberall (Land: naechste nasse Ecke)
    DS = S - GB
    DS = np.where(nass, np.maximum(DS, DS_KLEMME), np.minimum(DS, -DS_KLEMME))
    return nass, S, DS


def ringe(DS):
    # Kartenrand: Wasser, das den Rand beruehrt, 2 m ueber den Rand fortsetzen (Randwerte), spaeter auf die Karte zuschneiden
    P = np.pad(np.pad(DS, RAND_PAD, mode="edge"), 1, constant_values=-1.0)
    out = []
    for c in measure.find_contours(P, 0.0):
        c = c - 1.0 - RAND_PAD
        xz = np.column_stack([c[:, 1] / RS, c[:, 0] / RS])
        if len(xz) >= 4: out.append(xz)
    return out


def polygone(rohe_ringe):
    glatt = []
    for r in rohe_ringe:
        g = glatte_linie(r, True)
        if g is None: continue
        pg = Polygon(g)
        if pg.area < 1e-3: continue
        glatt.append((g, Polygon(r)))
    # Verschachtelungstiefe ueber die Rohringe (exakt, ohne Glaettungsfehler)
    roh = [b for _, b in glatt]; tiefe = []
    idx = shapely.STRtree(roh)
    for i, b in enumerate(roh):
        pt = Point(b.exterior.coords[0]); n = 0
        for j in idx.query(pt):
            if j != i and roh[j].area > b.area and roh[j].contains(pt): n += 1
        tiefe.append(n)
    shells = [i for i, t in enumerate(tiefe) if t % 2 == 0]
    holes = [i for i, t in enumerate(tiefe) if t % 2 == 1]
    polys = []
    for i in shells:
        hs = []
        for j in holes:
            if roh[j].area < LOCH_MIN_M2: continue      # Inseln kleiner als eine Rasterzelle (einzelne trockene Ecke) -> Wasser
            if tiefe[j] == tiefe[i] + 1 and roh[i].contains(Point(roh[j].exterior.coords[0])):
                hs.append(glatt[j][0])
        p = Polygon(glatt[i][0], hs)
        if not p.is_valid:
            p = shapely.make_valid(p)
            p = unary_union([g for g in getattr(p, "geoms", [p]) if g.geom_type == "Polygon"])
        polys.append(p)
    return polys


def linemerge_teile(g):
    from shapely.ops import linemerge
    parts = [x for x in getattr(g, "geoms", [g]) if x.geom_type == "LineString" and not x.is_empty]
    if not parts: return []
    m = linemerge(parts)
    return [x for x in getattr(m, "geoms", [m])]


def sparsamer_kreis(g, q, c0):
    """Kreis R, der die enge Stelle q sicher enthaelt (|c-q| = R-3 cm) und dabei moeglichst wenig Land ueberdeckt:
    Mittelpunktsrichtung um die Innennormale (c0) in 15-Grad-Schritten bis +-75 Grad variiert, kleinste Landflaeche gewinnt.
    (Ein symmetrisch tangentialer Kreis ragt an schraegen Bachkoepfen weit ueber das Gegenufer; das Schliessen fuellt dann
    die ganze Ecke dazwischen.)"""
    n = c0 - q; n /= max(np.hypot(*n), 1e-12); lokal = g.intersection(Point(*q).buffer(2.5 * AUSRUND_R))
    best = None
    for th in np.radians(np.arange(-75, 76, 15)):
        cs, sn = np.cos(th), np.sin(th); d = np.array([n[0] * cs - n[1] * sn, n[0] * sn + n[1] * cs])
        k = Point(*(q + (AUSRUND_R - 0.03) * d)).buffer(AUSRUND_R, quad_segs=64)
        land = k.difference(lokal).area
        if best is None or land < best[0] - 1e-9: best = (land, k)
    return best[1]


def enge_konvexe_stellen(poly, rmin, mit_punkt=False):
    """Punkte (5 cm Abtastung), an denen der Umkreisradius ueber +-0,5 m Bogenlaenge < rmin ist und das Wasser dort
    nach aussen gewoelbt ist (Sehnenmitte liegt im Wasser). Rueckgabe: Kreismittelpunkte R nach innen versetzt."""
    from shapely import contains_xy
    mitten, punkte = [], []
    for ring in [poly.exterior] + list(poly.interiors):
        Q = resample(np.asarray(ring.coords)[:-1], 0.05, True)
        if len(Q) < 30: continue
        A, C = np.roll(Q, 10, axis=0), np.roll(Q, -10, axis=0)
        u, v = Q - A, C - A
        kreuz = np.abs(u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0])
        r = np.hypot(*u.T) * np.hypot(*(C - Q).T) * np.hypot(*v.T) / np.maximum(2 * kreuz, 1e-12)
        M = 0.5 * (A + C)
        eng = (r < rmin) & contains_xy(poly, M[:, 0], M[:, 1])
        if not eng.any(): continue
        n = M[eng] - Q[eng]; n /= np.maximum(np.hypot(*n.T), 1e-12)[:, None]
        mitten.append(Q[eng] + AUSRUND_R * n); punkte.append(Q[eng])
    leer = np.zeros((0, 2))
    if mit_punkt: return (np.vstack(mitten), np.vstack(punkte)) if mitten else (leer, leer)
    return np.vstack(mitten) if mitten else leer


def ausrunden(polys, nass):
    """P1b2: QA misst Q3 mit dem gleitenden 1-m-Mittel; ein Kreis bleibt darunter erst ab R ~1,45 m. Darum je Gewaesser
    Kruemmungsradius >= AUSRUND_R herstellen, nur durch Hinzufuegen von Wasser (Original bleibt Teilmenge):
      a) nasse Ecken, die > 0,2 m ausserhalb liegen (1 Ecke breite Zipfel, die die Glaettung eingezogen hat): Kreis R durch den
         Punkt 0,2 m vor der Ecke, Mittelpunkt R Richtung Ufer -> kleinste runde Beule, die die Ecke erreicht;
      b) konvex zu enge Stellen (Bachenden, Tropfenspitzen): Kreis R tangential an die Spitze (Mittelpunkt R nach innen);
      c) konkav zu enge Stellen und die Ansaetze von a/b: morphologisches Schliessen Buffer(+R)·Buffer(-R) je Gewaesser.
    Wiederholt, bis weder a) noch b) etwas findet."""
    zz, xx = np.nonzero(nass); P = np.column_stack([xx / RS, zz / RS]); pts = shapely.points(P[:, 0], P[:, 1])
    wu = unary_union(polys)
    # nasse Ecken dem naechsten Gewaesser zuordnen
    d_all = np.vstack([shapely.distance(p, pts) for p in polys]); zu = d_all.argmin(axis=0)
    out = []
    for gi, p in enumerate(polys):
        g = p; meine = pts[zu == gi]; Pm = P[zu == gi]
        for it in range(6):
            kreise = []
            d = shapely.distance(g, meine); weg = d > 0.9 * ABDECK_TOL
            for (x, z), pt in zip(Pm[weg], meine[weg]):
                q = np.asarray(shapely.ops.nearest_points(g.boundary, pt)[0].coords[0])
                dv = q - np.array([x, z]); dv /= max(np.hypot(*dv), 1e-9)
                c = np.array([x, z]) + 0.25 * dv + AUSRUND_R * dv
                kreise.append(Point(*c).buffer(AUSRUND_R, quad_segs=64))
            m, qs = enge_konvexe_stellen(g, AUSRUND_PRUEF, mit_punkt=True)
            for c0, q in zip(m[::3], qs[::3]):
                kreise.append(sparsamer_kreis(g, q, c0))
            if not kreise and it > 0: break
            g2 = unary_union([g] + kreise).buffer(AUSRUND_R, quad_segs=64).buffer(-AUSRUND_R, quad_segs=64)
            g2 = unary_union([g2, p])
            if g2.geom_type != "Polygon": g2 = max(getattr(g2, "geoms", [g2]), key=lambda q: q.area)
            g = g2
        ringe_ = []
        for ring in [g.exterior] + list(g.interiors):
            Q = resample(np.asarray(ring.coords)[:-1], 0.05, True)
            ringe_.append(np.asarray(LineString(np.vstack([Q, Q[:1]])).simplify(0.001, preserve_topology=False).coords))
        q = Polygon(ringe_[0], [h for h in ringe_[1:] if len(h) >= 4])
        if not q.is_valid: q = shapely.make_valid(q)
        out.append(q)
    return out


def bilinear(F, x, z):
    return nd.map_coordinates(F, [np.asarray(z) * RS, np.asarray(x) * RS], order=1, mode="nearest")


def skelett_linien(poly):
    minx, minz, maxx, maxz = poly.bounds
    ox, oz = minx - 1.0, minz - 1.0; W = int((maxx - ox + 1.0) / SKEL_PX) + 2; H = int((maxz - oz + 1.0) / SKEL_PX) + 2
    M = np.zeros((H, W), bool)
    for p in getattr(poly, "geoms", [poly]):
        ext = np.asarray(p.exterior.coords); rr, cc = draw.polygon((ext[:, 1] - oz) / SKEL_PX, (ext[:, 0] - ox) / SKEL_PX, M.shape); M[rr, cc] = True
        for h in p.interiors:
            a = np.asarray(h.coords); rr, cc = draw.polygon((a[:, 1] - oz) / SKEL_PX, (a[:, 0] - ox) / SKEL_PX, M.shape); M[rr, cc] = False
    if M.sum() < 9: return [], None
    D = nd.distance_transform_edt(M) * SKEL_PX
    Sk = morphology.skeletonize(M)
    # Graph: Pixel -> Nachbarn
    pts = set(zip(*np.nonzero(Sk)))
    def nb(p):
        r, c = p
        return [(r + dr, c + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr or dc) and (r + dr, c + dc) in pts]
    deg = {p: len(nb(p)) for p in pts}
    knoten = {p for p, k in deg.items() if k != 2}
    besucht = set(); linien = []
    def lauf(a, b):
        weg = [a, b]; besucht.add(frozenset((a, b)))
        while weg[-1] not in knoten:
            nxt = [q for q in nb(weg[-1]) if frozenset((weg[-1], q)) not in besucht]
            if not nxt: break
            besucht.add(frozenset((weg[-1], nxt[0]))); weg.append(nxt[0])
        return weg
    for a in knoten:
        for b in nb(a):
            if frozenset((a, b)) not in besucht: linien.append(lauf(a, b))
    # reine Ringe ohne Knoten
    rest = {p for p in pts if p not in knoten and all(frozenset((p, q)) not in besucht for q in nb(p))}
    while rest:
        a = rest.pop(); n_ = nb(a)
        if not n_: continue
        w = lauf(a, n_[0]); linien.append(w); rest -= set(w)
    out = []
    for w in linien:
        A = np.array(w, float); xz = np.column_stack([A[:, 1] * SKEL_PX + ox, A[:, 0] * SKEL_PX + oz])
        L = np.hypot(*np.diff(xz, axis=0).T).sum() if len(xz) > 1 else 0
        endast = (deg[w[0]] == 1) or (deg[w[-1]] == 1)
        if L < AST_MIN_M and endast: continue
        if L < 0.5: continue
        out.append(xz)
    return out, (D, ox, oz)


def zacke_knick(C, closed):
    """Zackenamplitude gegen 1-m-Glaettung und max. Knick in Grad.
    1-m-Glaettung = Savitzky-Golay, Fenster 1 m (21 Punkte bei 5 cm), Ordnung 2: lokal quadratisch, folgt echten Kurven
    (Kreis R 0,25 m: Restfehler 1,5 mm), Rasterzacken (Wellenlaenge <= 1 m) bleiben als Rest sichtbar."""
    from scipy.signal import savgol_filter
    Q = resample(C, 0.05, closed)
    if len(Q) < 25: return 0.0, knick_max(C, closed)
    G = np.column_stack([savgol_filter(Q[:, i], 21, 2, mode="wrap" if closed else "interp") for i in range(2)])
    return float(np.hypot(*(Q - G).T).max()), knick_max(C, closed)


def zacke_gleitmittel(C, closed):
    """Nur Bericht: Abstand zum gleitenden 1-m-Mittel (bei Kurvenradius < ~1,4 m auch fuer glatte Kreise > 3 cm)."""
    Q = resample(C, 0.05, closed)
    if len(Q) < 25: return 0.0
    w = int(round(1.0 / 0.05)) | 1                  # 21 Punkte = genau 1 m Bogenlaenge
    k = np.ones(w); k[0] = k[-1] = 0.5; k /= k.sum()  # Trapezgewichte = stetiges Mittel ueber 1 m (nicht Punktzahl)
    if closed:
        pad = np.vstack([Q[-w:], Q, Q[:w]])
        Gl = np.column_stack([np.convolve(pad[:, i], k, "same")[w:-w] for i in range(2)]); ref = Q
    else:
        h = w // 2
        if len(Q) <= w + 2: return 0.0
        Gl = np.column_stack([np.convolve(Q[:, i], k, "valid") for i in range(2)]); ref = Q[h:len(Q) - h]
    return float(np.hypot(*(ref - Gl).T).max())


def fc(features):
    return {"type": "FeatureCollection", "crs_hinweis": "Viewer-Meter [x, z], 1 Einheit = 1 Zelle (Gitterpunkt r,c -> x=c/2, z=r/2)", "features": features}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--paket", default="/tmp/dv2_wasser/alle_kacheln.json.gz"); ap.add_argument("--aus", default=str(HIER)); ap.add_argument("--vorher", default=None, help="altes ufer.geojson fuer das Vorher-Nahbild")
    a = ap.parse_args(); aus = Path(a.aus)
    GB, WV = lade(a.paket)
    nass, S, DS = ds_feld(GB, WV)
    polys = polygone(ringe(DS))
    karte = shapely.box(0, 0, (GB.shape[1] - 1) / RS, (GB.shape[0] - 1) / RS)
    polys = ausrunden(polys, nass)
    polys = [p.intersection(karte) for p in polys]
    polys = [g for p in polys for g in getattr(p, "geoms", [p]) if g.geom_type == "Polygon" and not g.is_empty]
    rand = karte.exterior.buffer(1e-6)
    wasser_union = unary_union(polys)
    # Wasser-Features
    wf, uf, bf = [], [], []
    for i, p in enumerate(sorted(polys, key=lambda q: -q.area)):
        c = p.representative_point()
        inner = nass & False
        sp = float(np.median(bilinear(S, np.asarray(p.exterior.coords)[:, 0], np.asarray(p.exterior.coords)[:, 1])))
        gid = f"W{i + 1:02d}"
        wf.append({"type": "Feature", "geometry": mapping(p), "properties": {"id": gid, "typ": "wasser", "kachel_repr": kachel(c.x, c.y),
                   "flaeche_m2": round(p.area, 3), "spiegel_m_median": round(sp, 3), "loecher": len(p.interiors)}})
        # Uferlinien (aussen + Inseln) mit Spiegel je Punkt
        nk = 0
        for k, ring in enumerate([p.exterior] + list(p.interiors)):
            ls = LineString(ring.coords)
            teile = [ls]; zu = True
            if ls.intersects(rand):                      # Kartenrand ist kein Ufer
                d = linemerge_teile(ls.difference(rand)); teile = d; zu = False
            for t in teile:
                R = np.asarray(t.coords)
                if len(R) < 2 or t.length < 0.2: continue
                spk = bilinear(S, R[:, 0], R[:, 1])
                uf.append({"type": "Feature", "geometry": {"type": "LineString", "coordinates": np.round(R, 4).tolist()},
                           "properties": {"id": f"{gid}_U{nk}", "typ": "uferlinie", "gewaesser": gid, "seite": "aussen" if k == 0 else "insel",
                                          "geschlossen": zu, "spiegel_m": np.round(spk, 3).tolist()}}); nk += 1
        band = p.buffer(BAND_M, join_style="round", quad_segs=16).difference(wasser_union).intersection(karte)
        if not band.is_valid: band = shapely.make_valid(band)
        uf.append({"type": "Feature", "geometry": mapping(band), "properties": {"id": f"{gid}_B", "typ": "uferband", "gewaesser": gid,
                   "breite_m": BAND_M, "seite": "landseitig", "flaeche_m2": round(band.area, 3)}})
        # Mittellinien
        linien, dfeld = skelett_linien(p)
        for k, L in enumerate(linien):
            g = glatte_linie(L, False, sigma_m=0.5)
            if g is None or len(g) < 2: continue
            for _ in range(30):                          # Q3 auch fuer Mittellinien (gleitendes 1-m-Mittel) mit Reserve
                if zacke_gleitmittel(g, False) <= 0.025: break
                g = gauss_linie(resample(g, 0.05, False), 0.3 / 0.05, False)
            if not p.buffer(1e-6).contains(LineString(g)): g = np.asarray(LineString(g).intersection(p).coords) if LineString(g).intersection(p).geom_type == "LineString" else g
            D, ox, oz = dfeld
            br = 2 * nd.map_coordinates(D, [(g[:, 1] - oz) / SKEL_PX, (g[:, 0] - ox) / SKEL_PX], order=1, mode="nearest")
            bf.append({"type": "Feature", "geometry": {"type": "LineString", "coordinates": np.round(g, 4).tolist()},
                       "properties": {"id": f"{gid}_M{k}", "typ": "bach_mitte", "gewaesser": gid, "breite_m": np.round(br, 3).tolist(),
                                      "spiegel_m": np.round(bilinear(S, g[:, 0], g[:, 1]), 3).tolist()}})
    for name, f in (("wasser.geojson", wf), ("ufer.geojson", uf), ("bach_mitte.geojson", bf)):
        (aus / name).write_text(json.dumps(fc(f), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    bericht = messe(aus, a.paket)
    (aus / "extrahiere_wasser_bericht.json").write_text(json.dumps(bericht, indent=1, ensure_ascii=False), encoding="utf-8")
    bild(a.paket, aus, a.vorher)
    print(json.dumps({k: v for k, v in bericht.items() if k not in ("uferlinien_einzeln", "mittellinien_schlechteste")}, ensure_ascii=False))


def ist_flaeche(nass, x0=None, x1=None, z0=None, z1=None):
    """Ist-Wasserflaeche = nasse Gitterpunkte x 0,25 m2 (jede Ecke steht fuer 0,5 x 0,5 m)."""
    zz, xx = np.nonzero(nass); x, z = xx / RS, zz / RS
    m = np.ones_like(x, bool)
    if x0 is not None: m = (x >= x0) & (x < x1) & (z >= z0) & (z < z1)
    return float(m.sum() * (1.0 / RS) ** 2)


def messe(aus, paket):
    from shapely.geometry import shape, box
    GB, WV = lade(paket); nass = WV > -900
    W = [shape(f["geometry"]) for f in json.load(open(aus / "wasser.geojson"))["features"]]
    U = json.load(open(aus / "ufer.geojson"))["features"]; B = json.load(open(aus / "bach_mitte.geojson"))["features"]
    wu = unary_union(W)
    r = {"polygone_wasser": len(W), "uferlinien": sum(f["properties"]["typ"] == "uferlinie" for f in U),
         "uferbaender": sum(f["properties"]["typ"] == "uferband" for f in U), "bach_mittellinien": len(B)}
    r["alle_polygone_valid"] = bool(all(g.is_valid for g in W) and all(shape(f["geometry"]).is_valid for f in U if f["properties"]["typ"] == "uferband"))
    ist = ist_flaeche(nass); r["flaeche_ist_m2"] = round(ist, 2); r["flaeche_vektor_m2"] = round(wu.area, 2)
    r["flaeche_abw_prozent"] = round(100 * (wu.area - ist) / ist, 3)
    for kn in ("E2", "E3"):
        cx = "ABCDEFGH".index(kn[0]); cz = int(kn[1]) - 1
        x0, z0 = cx * KACHEL_X, cz * KACHEL_Z; x1, z1 = x0 + KACHEL_X, z0 + KACHEL_Z
        i = ist_flaeche(nass, x0, x1, z0, z1); v = wu.intersection(box(x0, z0, x1, z1)).area
        r[f"flaeche_{kn}"] = {"ist_m2": round(i, 2), "vektor_m2": round(v, 2), "abw_prozent": round(100 * (v - i) / i, 3) if i else None}
    # Ist-Wasser vollstaendig abgedeckt? (kein Wasser entfernt): Anteil nasser Ecken innerhalb des Vektorwassers
    zz, xx = np.nonzero(nass); pts = shapely.points(xx / RS, zz / RS)
    dist = shapely.distance(wu, pts)
    r["nasse_ecken_innen_prozent"] = round(100 * float((dist == 0).mean()), 3)
    r["nasse_ecken_abgedeckt_prozent"] = round(100 * float((dist <= ABDECK_TOL).mean()), 3)
    r["nasse_ecke_max_abstand_m"] = round(float(dist.max()), 3)
    r["nasse_ecken_ueber_toleranz"] = int((dist > ABDECK_TOL).sum())
    # Q3 (QA-Messung): gleitendes 1-m-Mittel ueber Bogenlaenge; Savitzky-Golay nur Zusatzinfo
    je = []
    for f in [x for x in U if x["properties"]["typ"] == "uferlinie"] + B:
        C = np.asarray(f["geometry"]["coordinates"]); closed = bool(f["properties"].get("geschlossen"))
        if closed and np.allclose(C[0], C[-1]): C = C[:-1]
        sg, k = zacke_knick(C, closed); gm = zacke_gleitmittel(C, closed)
        je.append({"id": f["properties"]["id"], "typ": f["properties"]["typ"], "zacke_gleitmittel_m": round(gm, 4),
                   "knick_grad": round(k, 2), "zacke_sg_m_info": round(sg, 4), "laenge_m": round(float(np.hypot(*np.diff(C, axis=0).T).sum()), 1)})
    uf_ = [e for e in je if e["typ"] == "uferlinie"]; bm = [e for e in je if e["typ"] == "bach_mitte"]
    r["ufer_zacke_gleitmittel_max_m"] = max(e["zacke_gleitmittel_m"] for e in uf_)
    r["ufer_knick_max_grad"] = max(e["knick_grad"] for e in uf_)
    r["mitte_zacke_gleitmittel_max_m"] = max(e["zacke_gleitmittel_m"] for e in bm) if bm else 0.0
    r["mitte_knick_max_grad"] = max(e["knick_grad"] for e in bm) if bm else 0.0
    r["zacke_sg_max_m_info"] = max(e["zacke_sg_m_info"] for e in je)
    sp = [f["properties"]["spiegel_m_median"] for f in json.load(open(aus / "wasser.geojson"))["features"]]
    r["ueberlappung_max_m2"] = round(max([W[a].intersection(W[b]).area for a in range(len(W)) for b in range(a + 1, len(W))] or [0.0]), 6)
    r["uferlinien_einzeln"] = uf_
    r["mittellinien_schlechteste"] = sorted(bm, key=lambda e: -e["zacke_gleitmittel_m"])[:8]
    r["schwellen"] = {"zacke_gleitmittel_m": 0.03, "knick_grad": 15.0, "flaeche_prozent": 3.0, "nass_aussen_m": 0.3}
    return r


def bild(paket, aus, vorher=None):
    """Uebersicht: neue Linien ueber der alten Draufsicht (Vertex-Farben VC des Pakets, orthografisch) + Ausschnitte E2/E3
    mit den alten nassen Gitterpunkten als Punkte."""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from shapely.geometry import shape
    d = json.load(gzip.open(paket)); ny, nx = d["ny"] * d["rs"] + 1, d["nx"] * d["rs"] + 1
    VC = np.frombuffer(base64.b64decode(d["VC"]), np.uint8).reshape(ny, nx, 3)
    GB, WV = lade(paket); nass = WV > -900
    U = json.load(open(aus / "ufer.geojson"))["features"]; B = json.load(open(aus / "bach_mitte.geojson"))["features"]
    ext = [0, (nx - 1) / RS, (ny - 1) / RS, 0]
    fig = plt.figure(figsize=(16, 8.4), dpi=100)
    ausschn = [("Gesamt", None), ("E2", (168, 210, 43, 86)), ("E3", (168, 210, 86, 129)),
               ("E2-Nordrand vorher (gruen gestrichelt, P1b) / nachher (rot, P1b2)", (191, 207, 37, 51))]
    ax0 = fig.add_axes([0.0, 0.0, 0.46, 1.0]); a2 = fig.add_axes([0.46, 0.5, 0.27, 0.5]); a3 = fig.add_axes([0.46, 0.0, 0.27, 0.5])
    a4 = fig.add_axes([0.73, 0.2, 0.27, 0.6])
    if vorher and Path(vorher).exists():
        for f in json.load(open(vorher))["features"]:
            if f["properties"]["typ"] == "uferlinie":
                a4.plot(*shape(f["geometry"]).xy, color="#00c000", lw=1.6, ls="--")
    for ax, (name, box_) in zip([ax0, a2, a3, a4], ausschn):
        ax.imshow(VC, extent=ext, interpolation="nearest")
        for f in U:
            g = shape(f["geometry"])
            if f["properties"]["typ"] == "uferband":
                for p in getattr(g, "geoms", [g]):
                    if p.geom_type == "Polygon": ax.fill(*p.exterior.xy, color="#ffd400", alpha=0.25, lw=0)
            else:
                ax.plot(*g.xy, color="#ff2020", lw=0.6 if box_ is None else 1.4)
        if box_:
            x0, x1, z0, z1 = box_
            zz, xx = np.nonzero(nass[int(z0 * RS):int(z1 * RS) + 1, int(x0 * RS):int(x1 * RS) + 1])
            ax.plot(xx / RS + x0, zz / RS + z0, ".", color="#1030ff", ms=1.0)
            ax.set_xlim(x0, x1); ax.set_ylim(z1, z0)
        for f in B:
            ax.plot(*shape(f["geometry"]).xy, color="#00e5ff", lw=0.5 if box_ is None else 1.6)
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(0.01, 0.99, name + (" (rot Uferlinie, gelb Uferband 2,5 m, cyan Mittellinie, blau alte nasse Ecken)" if box_ and len(name) < 4 else ""),
                transform=ax.transAxes, va="top", fontsize=7, color="w", bbox=dict(fc="k", alpha=0.6, lw=0))
    fig.savefig(aus / "uebersicht_wasser.jpg", dpi=100, pil_kwargs={"quality": 80})
    plt.close(fig)


if __name__ == "__main__":
    main()
