"""P1c Nacharbeit: konstruktive Flaechentyp- und Untergrund-Partition.

Flaechentyp: aus den gemergten, bereits glatten Vektoren (wasser.geojson,
ufer.geojson Baender, wege.geojson Netz) plus Bruecken-Platzhalter und einer
SDF-geglaetteten Felsmaske, Prioritaet Wasser > Bruecke > Weg > Ufer > Fels >
Grund per exakter shapely-difference. Untergrund: Multi-Label-Glaettung
(Indikator je Label auf 0,1 m, Gauss, argmax ueber kumulative Maxima),
Konturen per marching squares. Keine Zellpolygonisierung.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from shapely import get_parts, make_valid, unary_union, set_precision
from shapely.geometry import LineString, Point, Polygon, box, shape
from shapely.ops import polygonize
from skimage.measure import find_contours

RES = 0.1          # Raster der Glaettungsfelder in m
UP = 10            # Zelle 1 m -> 10 x 10 Pixel
NX, NY = 336, 303
RECT = box(0, 0, NX, NY)
BRUECKEN_SCHNITT: list = []  # (z-Schnitt, Quellflaeche, Ergebnis)
BRIDGES = {"E2": box(186, 73, 197, 75), "E3_west": box(174, 126, 186, 128)}
FELS_SIGMA_M = 1.0
UNTER_SIGMA_M = 3.5   # [A] 1,5 m liess Zungen/Spitzen r < 1,6 m (Q3 bis 5,6 cm), siehe Bericht
UNTER_INSEL_M2 = 12.0  # Kreis 12 m2: r 1,95 m, Umfang 12,3 m (Q3-faehig)
MIN_AREA = 4.0
R_RUND = 2.0        # Mindestradius der Ausrundung (Kreis r=2 m -> 1-m-Mittel ~2,1 cm)


FELS_RING_SIGMA_M = 1.0
FELS_SCHLIESSEN_M = 2.5
FELS_OEFFNEN_M = 2.5   # Finger < 5 m Breite entfallen, konvexe Boegen r >= 2,5 m (QA-Mittel ~1,7 cm)


def _resample_ring(p, n):
    p = np.asarray(p, float)
    if np.allclose(p[0], p[-1]):
        p = p[:-1]
    ext = np.vstack([p, p[:1]])
    seg = np.hypot(*np.diff(ext, axis=0).T)
    se = np.r_[0, np.cumsum(seg)]
    L = se[-1]
    ss = np.arange(n) * (L / n)
    return np.column_stack((np.interp(ss, se, ext[:, 0]), np.interp(ss, se, ext[:, 1]))), L


def ring_glatt(coords, sigma_m: float, step: float = 0.05, out_step: float = 0.10):
    """Geschlossenen Ring nach Bogenlaenge gleichmaessig abtasten, zyklisch
    Gauss-filtern (sigma in m) und mit <= out_step gleichmaessig neu abtasten."""
    L0 = LineString(coords).length
    n = max(16, int(np.ceil(L0 / step)))
    p, L = _resample_ring(coords, n)
    p = ndi.gaussian_filter1d(p, sigma=sigma_m / (L / n), axis=0, mode="wrap")
    L1 = LineString(np.vstack((p, p[:1]))).length
    m = max(8, int(np.ceil(L1 / out_step)))
    o, _ = _resample_ring(np.vstack((p, p[:1])), m)
    return np.vstack((o, o[:1]))


RING_SIGMAS = (1.0, 1.5, 2.0, 2.5, 3.0)
RING_LOG = []
RING_DROPPED = []
RING_ZIEL_M, RING_ZIEL_GRAD = 0.025, 12.0   # Reserve zu 3 cm / 15 Grad


def ring_q3(c):
    """Strengere der beiden Messarten (QA-Stuetzpunktmittel und 5-cm-Abtastung)."""
    from shapely import distance, points
    p = np.asarray(c, float)[:-1]
    n = len(p)
    if n < 5:
        return 0.0, 0.0
    seg = np.hypot(*np.diff(np.vstack([p, p[:1]]), axis=0).T)
    s = np.r_[0, np.cumsum(seg)][:n]
    L = s[-1] + seg[-1]
    # Fenster |ds| <= 0,5 m zyklisch, vektorisiert ueber verdreifachte Reihe
    s3 = np.r_[s - L, s, s + L]; p3 = np.vstack([p, p, p])
    cs = np.vstack([np.zeros((1, 2)), np.cumsum(p3, axis=0)])
    lo = np.searchsorted(s3, s - 0.5 - 1e-12, side="left")
    hi = np.searchsorted(s3, s + 0.5 + 1e-12, side="right")
    g = (cs[hi + n] - cs[lo + n]) / (hi - lo)[:, None] if False else (cs[hi] - cs[lo]) / (hi - lo)[:, None]
    qa = float(distance(points(p), LineString(np.vstack([g, g[:1]]))).max())
    ss = np.arange(max(1, int(np.ceil(L / 0.05)))) * (L / max(1, int(np.ceil(L / 0.05))))
    if len(ss) < 30:
        qa_only = True
    else:
        qa_only = False
    ext = np.vstack([p, p[:1]]); se = np.r_[s, L]
    xy = np.column_stack((np.interp(ss, se, ext[:, 0]), np.interp(ss, se, ext[:, 1])))
    if qa_only:
        xy = np.vstack([xy] * 30)
    pad = np.vstack((xy[-10:], xy, xy[:10]))
    m = np.column_stack([np.convolve(pad[:, k], np.ones(21) / 21, mode="valid") for k in range(2)])
    fine_ = 0.0 if qa_only else float(np.hypot(*(xy - m).T).max())
    v1 = p - np.roll(p, 1, axis=0); v2 = np.roll(p, -1, axis=0) - p
    cosv = (v1 * v2).sum(1) / (np.hypot(*v1.T) * np.hypot(*v2.T) + 1e-15)
    return max(qa, fine_), float(np.degrees(np.arccos(np.clip(cosv, -1, 1))).max())


RING_MIN_LAENGE_M = 16.0   # Kreis r=1,6 m hat 10 m Umfang; kuerzere Ringe sind nicht Q3-faehig


RING_DROP_LAENGE_M = 40.0   # kurze Ringe, die kein sigma Q3-faehig macht, entfallen


def ring_adaptiv(coords):
    """Ring-Gauss mit steigendem sigma; erstes sigma, das beide Messarten mit
    Reserve haelt, sonst das beste. Rueckgabe (Ring, bestanden)."""
    best = None
    for sg in RING_SIGMAS:
        c = ring_glatt(coords, sg)
        a_, k_ = ring_q3(c)
        score = max(a_ / RING_ZIEL_M, k_ / RING_ZIEL_GRAD)
        if best is None or score < best[0]:
            best = (score, sg, a_, k_, c)
        if score <= 1.0:
            break
    score, sg, a_, k_, c = best
    RING_LOG.append((sg, round(a_, 4), round(k_, 2), round(LineString(c).length, 1),
                     round(float(c[:, 0].mean()), 1), round(float(c[:, 1].mean()), 1), score <= 1.0))
    return c, (a_ <= 0.0295 and k_ <= 14.5)


def ringe_glaetten(geom, sigma_m: float):
    out = []
    for poly in polys(geom):
        if poly.area < MIN_AREA:
            continue
        if poly.exterior.length < RING_MIN_LAENGE_M:
            continue
        ext, ok = ring_adaptiv(poly.exterior.coords)
        if not ok and poly.exterior.length < RING_DROP_LAENGE_M:
            RING_DROPPED.append(("teil", round(poly.area, 1), round(poly.centroid.x, 1), round(poly.centroid.y, 1)))
            continue
        holes = []
        for r in poly.interiors:
            if Polygon(r).area < MIN_AREA or r.length < RING_MIN_LAENGE_M:
                continue
            h, ok = ring_adaptiv(r.coords)
            if not ok and r.length < RING_DROP_LAENGE_M:
                RING_DROPPED.append(("loch", round(Polygon(r).area, 1), round(Polygon(r).centroid.x, 1), round(Polygon(r).centroid.y, 1)))
                continue
            holes.append(h)
        shell = clean(Polygon(ext))
        for h in holes:
            shell = shell.difference(clean(Polygon(h)))
        out.append(clean(shell))
    return clean(unary_union(out)) if out else Polygon()


def schliessen(g, r=R_RUND):
    """Morphologisches Schliessen (konkave Ecken auf Radius r ausrunden)."""
    return g.buffer(r, quad_segs=64, join_style="round").buffer(-r, quad_segs=64, join_style="round")


AUSSEN = box(-10, -10, NX + 10, NY + 10).difference(RECT)


def _gespiegelt(gi, rand):
    """gi plus Spiegelbilder an den vier Kartenkanten und den vier Ecken (nur Randstreifen)."""
    from shapely import affinity
    teile = [gi]
    for sx, ox in ((1, None), (-1, 0.0), (-1, float(NX))):
        for sy, oy in ((1, None), (-1, 0.0), (-1, float(NY))):
            if sx == 1 and sy == 1:
                continue
            fx0 = 0.0 if ox is None else ox
            fy0 = 0.0 if oy is None else oy
            streifen = box(-10 if ox is None else fx0 - rand, -10 if oy is None else fy0 - rand,
                           NX + 10 if ox is None else fx0 + rand, NY + 10 if oy is None else fy0 + rand)
            teil = gi.intersection(streifen)
            if teil.is_empty:
                continue
            teile.append(affinity.scale(teil, xfact=sx, yfact=sy, origin=(fx0, fy0)))
    return unary_union(teile)


def schliessen_rand(g, r=R_RUND):
    """Schliessen am Kartenrand ohne Randartefakte (P1c2): statt eines Aussenbands
    (fuellte die vier Kartenecken und erzeugte zum Rand tangentiale Keile) wird die
    Flaeche an den Kartenkanten gespiegelt; Grenzen treffen den Rand dadurch
    rechtwinklig, Ecken bleiben unberuehrt."""
    gi = g.intersection(RECT)
    return clean(schliessen(_gespiegelt(gi, 2 * r + 1.0), r).intersection(RECT))


def oeffnen(g, r=R_RUND):
    return g.buffer(-r, quad_segs=64, join_style="round").buffer(r, quad_segs=64, join_style="round")
FELS_UNTERGRUND = ("FELS", "KLIPPE_WAND", "KLIPPE_KANTE")
NICHT_UNTERGRUND = FELS_UNTERGRUND + ("WASSER_EIS",)


def polys(geom):
    if geom is None or geom.is_empty:
        return []
    return [g for g in get_parts(geom) if g.geom_type == "Polygon" and not g.is_empty] + \
        [p for g in get_parts(geom) if g.geom_type in ("MultiPolygon", "GeometryCollection") for p in polys(g)]


def load_vectors(vec: Path):
    def feats(name):
        return json.loads((vec / name).read_text(encoding="utf-8"))["features"]
    water = unary_union([shape(f["geometry"]) for f in feats("wasser.geojson") if f["properties"].get("typ") == "wasser"])
    ufer = unary_union([p for f in feats("ufer.geojson") if f["properties"].get("typ") == "uferband"
                        for p in polys(shape(f["geometry"]))])
    netz = [shape(f["geometry"]) for f in feats("wege.geojson") if f["properties"].get("rolle") == "netz"]
    if netz:
        weg = unary_union(netz)
    else:  # Rueckfall: Baender + Kreuzungen
        weg = unary_union([shape(f["geometry"]) for f in feats("wege.geojson") if f["properties"].get("rolle") == "band"] +
                          [shape(f["geometry"]) for f in feats("kreuzungen.geojson")])
    return water, ufer, weg


def fine(mask_cells: np.ndarray) -> np.ndarray:
    return np.repeat(np.repeat(mask_cells, UP, axis=0), UP, axis=1)


def field_regions(field: np.ndarray, pad: int, level: float = 0.0, clip: bool = True) -> object:
    """Polygone {field > level}; field auf 0,1-m-Pixeln mit pad Randpixeln."""
    lo = min(float(field.min()), level) - 1.0
    f = np.pad(field, 1, constant_values=lo)
    rings = []
    for c in find_contours(f, level):
        pts = np.column_stack(((c[:, 1] - 1 - pad + 0.5) * RES, (c[:, 0] - 1 - pad + 0.5) * RES))
        if len(pts) >= 4:
            rings.append(LineString(pts))
    faces = list(polygonize(unary_union(rings)))
    keep = []
    for face in faces:
        rp = face.representative_point()
        iy = (rp.y / RES - 0.5) + pad
        ix = (rp.x / RES - 0.5) + pad
        v = ndi.map_coordinates(field, [[iy], [ix]], order=1, mode="nearest")[0]
        if v > level:
            keep.append(face)
    if not keep:
        return Polygon()
    u = unary_union(keep)
    return u.intersection(RECT) if clip else u


def sdf_smooth_region(mask_cells: np.ndarray, sigma_m: float, min_area: float, pad_m: float = 6.0, clip: bool = True):
    """Signed-Distance-Feld der Zellmaske, Gauss-geglaettet, Kontur bei 0."""
    pad = int(round(pad_m / RES))
    m = np.pad(fine(mask_cells.astype(bool)), pad, mode="edge")
    inside = ndi.distance_transform_edt(m) * RES
    outside = ndi.distance_transform_edt(~m) * RES
    sdf = inside - outside  # > 0 innen
    sm = ndi.gaussian_filter(sdf, sigma=sigma_m / RES, mode="nearest")
    region = field_regions(sm, pad, clip=clip)
    return unary_union([p for p in polys(region) if p.area >= min_area]) if not region.is_empty else region


def knoten_neu(regions: dict, grid: float = 1e-3):
    """Exakt verknotete Partition: alle Raender auf 1e-6 m rasten, gemeinsam
    verknoten (polygonize, entfernt Nullflaechen-Spitzen), Flaechen per
    repraesentativem Punkt wieder dem Label zuordnen."""
    from shapely.strtree import STRtree
    items = [(n, p) for n in sorted(regions) for p in polys(regions[n])]
    # gemeinsames Snap-Rounding aller Raender auf 1 mm: T-Stoesse (Knoten des einen
    # Polygons wenige 1e-5 m neben der Kante des anderen) werden echte Knoten.
    lines = unary_union([p.boundary for _, p in items] + [RECT.boundary], grid_size=grid)
    faces = list(polygonize(lines))
    tree = STRtree([p for _, p in items])
    new = {n: [] for n in regions}
    for face in faces:
        rp = face.representative_point()
        hits = [int(i) for i in tree.query(rp) if items[int(i)][1].covers(rp)]
        if not hits:
            hits = [int(min(tree.query(face.buffer(0.01)), key=lambda i: items[int(i)][1].distance(rp)))] if len(tree.query(face.buffer(0.01))) else []
        if hits:
            n = max(hits, key=lambda i: items[i][1].intersection(face).area)
            new[items[n][0]].append(face)
    return {n: clean(unary_union(v)) if v else Polygon() for n, v in new.items()}


def boegen_bereinigen(regions: dict, min_seg: float = 0.02):
    """Gemeinsame Boegen zwischen Knoten einmal bereinigen (Stuetzpunkte naeher
    als min_seg am vorigen bzw. am Bogenende entfallen; Endknoten fix), dann
    polygonize und Label-Zuordnung. Jeder Bogen gehoert beiden Nachbarn, die
    Partition bleibt exakt."""
    from shapely import line_merge
    from shapely.strtree import STRtree
    items = [(n, p) for n in sorted(regions) for p in polys(regions[n])]
    merged = line_merge(unary_union([p.boundary for _, p in items] + [RECT.boundary]))
    arcs = []
    for line in get_parts(merged):
        c = np.asarray(line.coords)
        if len(c) <= 2:
            arcs.append(line)
            continue
        keep = [c[0]]
        for q in c[1:-1]:
            if np.hypot(*(q - keep[-1])) >= min_seg and np.hypot(*(q - c[-1])) >= min_seg:
                keep.append(q)
        keep.append(c[-1])
        if len(keep) >= 2 and not (len(keep) == 2 and np.allclose(keep[0], keep[1])):
            arcs.append(LineString(keep))
    faces = list(polygonize(unary_union(arcs)))
    tree = STRtree([p for _, p in items])
    new = {n: [] for n in regions}
    for face in faces:
        cand = [int(i) for i in tree.query(face)]
        if not cand:
            continue
        best = max(cand, key=lambda i: items[i][1].intersection(face).area)
        new[items[best][0]].append(face)
    return {n: clean(unary_union(v)) if v else Polygon() for n, v in new.items()}


def _glatt_offen(p, sigma_m, step=0.05, out_step=0.10):
    line = LineString(p)
    L = line.length
    n = max(2, int(np.ceil(L / step)))
    ss = np.linspace(0.0, L, n + 1)
    seg = np.hypot(*np.diff(p, axis=0).T); se = np.r_[0, np.cumsum(seg)]
    q = np.column_stack((np.interp(ss, se, p[:, 0]), np.interp(ss, se, p[:, 1])))
    k = int(min(len(q) - 1, max(1, round(3 * sigma_m / step))))
    a, b = q[0], q[-1]
    # punktsymmetrische Spiegelung an den festen Enden: Ende bleibt fix, keine Endschleppe
    ext = np.vstack([2 * a - q[k:0:-1], q, 2 * b - q[-2:-k - 2:-1]])
    sm = ndi.gaussian_filter1d(ext, sigma=sigma_m / (L / n), axis=0, mode="nearest")[k:k + len(q)]
    sm[0], sm[-1] = a, b
    L1 = LineString(sm).length
    m = max(1, int(np.ceil(L1 / out_step)))
    seg = np.hypot(*np.diff(sm, axis=0).T); se = np.r_[0, np.cumsum(seg)]
    so = np.linspace(0.0, se[-1], m + 1)
    o = np.column_stack((np.interp(so, se, sm[:, 0]), np.interp(so, se, sm[:, 1])))
    o[0], o[-1] = a, b
    return o


def boegen_glaetten(regions: dict, sigma_m: float = 0.8):
    """Partition-erhaltende Bogenglaettung: jeder gemeinsame Bogen zwischen zwei
    Knoten (>= 3 Kanten bzw. Kartenrand) wird einmal geglaettet, Enden fix;
    danach polygonize und Label-Zuordnung nach groesster Ueberlappung."""
    from shapely import line_merge
    from shapely.strtree import STRtree
    items = [(n, p) for n in sorted(regions) for p in polys(regions[n])]
    merged = line_merge(unary_union([p.boundary for _, p in items] + [RECT.boundary], grid_size=1e-3))
    fb = RECT.boundary.buffer(1e-6)
    arcs = []
    for line in get_parts(merged):
        c = np.asarray(line.coords)
        if fb.contains(line) or len(c) < 3:
            arcs.append(line)
        elif line.is_ring:
            arcs.append(LineString(ring_glatt(c, sigma_m)))
        else:
            arcs.append(LineString(_glatt_offen(c, sigma_m)))
    faces = list(polygonize(unary_union(arcs)))
    tree = STRtree([p for _, p in items])
    new = {n: [] for n in regions}
    for face in faces:
        cand = [int(i) for i in tree.query(face)]
        if cand:
            best = max(cand, key=lambda i: items[i][1].intersection(face).area)
            new[items[best][0]].append(face)
    return {n: clean(unary_union(v)) if v else Polygon() for n, v in new.items()}


def coverage_glatt(regions: dict, tol: float = 0.01):
    """Mikro-Spitzen/Doppelpunkte der gemeinsamen Kanten topologisch entfernen."""
    from shapely import coverage_simplify
    items = [(n, p) for n in sorted(regions) for p in polys(regions[n])]
    simp = coverage_simplify([p for _, p in items], tol, simplify_boundary=False)
    new = {n: [] for n in regions}
    for (n, _), g in zip(items, simp):
        new[n].extend(polys(clean(g)))
    return {n: clean(unary_union(v)) if v else Polygon() for n, v in new.items()}


def clean(g):
    if not g.is_valid:
        g = make_valid(g)
    return unary_union(polys(g)) if polys(g) else Polygon()


def flaechentyp_partition(vec: Path, substrates: np.ndarray):
    water, ufer, weg = load_vectors(vec)
    fels_mask = np.isin(substrates.astype(str), FELS_UNTERGRUND)
    # Felsflaeche ueber den Kartenrand hinaus (6 m Randfortsetzung) glaetten,
    # erst danach auf das Rechteck schneiden: keine Abrundung am Kartenrand.
    fels = sdf_smooth_region(fels_mask, FELS_SIGMA_M, MIN_AREA, clip=False)
    fels = oeffnen(fels, FELS_OEFFNEN_M) if FELS_OEFFNEN_M > 0 else fels
    if FELS_SCHLIESSEN_M > 0:
        fels = schliessen(fels, FELS_SCHLIESSEN_M)
    fels = ringe_glaetten(fels, FELS_RING_SIGMA_M).intersection(RECT)
    fels = unary_union([p for p in polys(fels) if p.area >= MIN_AREA])
    weg_quelle, ufer_quelle = weg, ufer
    weg = schliessen_rand(weg)
    # Band und Wasser teilen die Uferlinie; Schliessen der Vereinigung fuellt
    # numerische Spalten zwischen Bandinnenrand und Wasserrand (Wasser hat Vorrang).
    ufer = schliessen_rand(unary_union([ufer, water]))
    # Bruecken-Platzhalter: Die Rechtecke dienen als Auswahlfenster. Brueckenflaeche
    # = Komponenten von (ausgerundetes Wegnetz geschnitten mit ausgerundetem
    # Uferband, ohne Wasser), die ein Rechteck schneiden. So enden alle
    # Brueckenraender an echten Schnitten glatter Boegen statt an 90-Grad-Ecken.
    # [A] Ist eine Komponente > 3 % groesser als dieselbe Konstruktion aus den
    # Quellvektoren (Ausrundung laeuft am Ufer entlang, E3-West bis z 137), wird
    # sie mit einer waagrechten Linie z = c gekappt; c per Bisektion so, dass die
    # Flaeche der Quellkonstruktion entspricht. Der abgeschnittene Rest liegt im
    # Uferband (nur die Weg-Ausrundung hatte ihn erfasst) und wird Ufer mit Vorrang
    # vor Weg; so enden beide Schnittenden an Tripelpunkten (Bruecke/Weg/Ufer bzw.
    # Bruecke/Wasser/Ufer) statt an 2-Label-Ecken.
    BRUECKEN_SCHNITT.clear()
    kandidaten = polys(clean(weg.intersection(ufer).difference(water)))
    quelle = polys(clean(weg_quelle.intersection(ufer_quelle).difference(water)))
    teile, ueberschuss = [], []
    for p in kandidaten:
        if not any(p.intersects(r) for r in BRIDGES.values()):
            continue
        ref = sum(q.area for q in quelle if q.intersects(p) and any(q.intersects(r) for r in BRIDGES.values()))
        if ref > 0 and p.area > 1.03 * ref:
            lo, hi = p.bounds[1], p.bounds[3]
            for _ in range(60):
                c = 0.5 * (lo + hi)
                if p.intersection(box(-10, -10, NX + 10, c)).area < ref:
                    lo = c
                else:
                    hi = c
            c = round(0.5 * (lo + hi), 3)
            ueberschuss.append(clean(p.difference(box(-10, -10, NX + 10, c))))
            p = clean(p.intersection(box(-10, -10, NX + 10, c)))
            BRUECKEN_SCHNITT.append((c, round(ref, 2), round(p.area, 2)))
        teile.append(p)
    bruecke_roh = unary_union(teile) if teile else Polygon()
    ufer_vorrang = unary_union(ueberschuss) if ueberschuss else Polygon()
    layers = [("wasser", water), ("bruecke", bruecke_roh), ("ufer_vorrang", ufer_vorrang),
              ("weg", weg), ("ufer", ufer), ("fels", fels)]
    claimed = Polygon()
    out = {}
    raw = {}
    for name, g in layers:
        g = clean(g.intersection(RECT))
        raw[name] = g
        part = clean(g.difference(claimed))
        out[name] = part
        claimed = clean(unary_union([claimed, part]))
    # Felsreste < 4 m2 nach dem Verschneiden gehen an Grund (Fels ist die
    # niedrigste Klasse vor Grund; seine Grenzen zu hoeheren Klassen sind deren Boegen).
    klein = [p for p in polys(out["fels"]) if p.area < MIN_AREA]
    if klein:
        out["fels"] = clean(unary_union([p for p in polys(out["fels"]) if p.area >= MIN_AREA]))
    out["grund"] = clean(RECT.difference(unary_union([out[n] for n, _ in layers])))
    out["ufer"] = clean(unary_union([out["ufer"], out.pop("ufer_vorrang")]))
    raw.pop("ufer_vorrang", None)
    return out, raw


def untergrund_partition(substrates: np.ndarray, sigma_m: float = UNTER_SIGMA_M, pad_m: float = 4.0):
    ny, nx = substrates.shape
    labels_all = substrates.astype(str)
    valid = ~np.isin(labels_all, NICHT_UNTERGRUND)
    # Wasser/Fels-Zellen dem naechsten echten Untergrund zuordnen
    _, (iy, ix) = ndi.distance_transform_edt(~valid, return_indices=True)
    assigned = labels_all[iy, ix]
    names = sorted(set(assigned.ravel().tolist()), key=lambda n: (-int(np.count_nonzero(assigned == n)), n))
    pad = int(round(pad_m / RES))
    fields = []
    for n in names:
        ind = np.pad(fine(assigned == n).astype(np.float32), pad, mode="edge")
        fields.append(ndi.gaussian_filter(ind, sigma=sigma_m / RES, mode="nearest"))
    F = np.stack(fields)
    top = np.sort(F, axis=0)
    regions = {}
    cum = None
    claimed = Polygon()
    for k, n in enumerate(names[:-1]):
        others = np.where(F[k] == top[-1], top[-2], top[-1])
        g = F[k] - others
        cum = g if cum is None else np.maximum(cum, g)
        ck = field_regions(cum, pad)
        part = clean(ck.difference(claimed))
        regions[n] = part
        claimed = clean(unary_union([claimed, part]))
    regions[names[-1]] = clean(RECT.difference(claimed))
    return regions, assigned


def merge_small(regions: dict, min_area: float = MIN_AREA, duenn_m: float = 0.0):
    """Schnelle Variante: alle Teile < min_area auf einmal dem Nachbarteil mit
    laengster gemeinsamer Grenze zuschlagen (iteriert, bis stabil)."""
    from shapely.strtree import STRtree
    merged_total = 0
    for _ in range(6):
        items = [(n, p) for n in sorted(regions) for p in polys(regions[n])]
        geoms = [p for _, p in items]
        tree = STRtree(geoms)
        target = {}
        for i, (n, p) in enumerate(items):
            if p.area >= min_area and not (duenn_m > 0 and p.area < 50.0 and p.area / p.length < duenn_m):
                continue
            best, blen = None, 0.0
            for j in tree.query(p):
                j = int(j)
                if j == i or items[j][0] == n:
                    continue
                L = p.boundary.intersection(geoms[j].boundary).length
                if L > blen:
                    best, blen = items[j][0], L
            if best is not None:
                target[i] = best
        if not target:
            break
        new = {n: [] for n in regions}
        for i, (n, p) in enumerate(items):
            new[target.get(i, n)].append(p)
        regions = {n: clean(unary_union(v)) if v else Polygon() for n, v in new.items()}
        merged_total += len(target)
    return regions, merged_total


def merge_small_alt(regions: dict, min_area: float = MIN_AREA):
    """Teilflaechen < min_area dem Nachbarn mit laengster gemeinsamer Grenze geben."""
    changed = True
    rounds = 0
    merged = 0
    while changed and rounds < 5:
        changed = False
        rounds += 1
        for n in sorted(regions):
            parts = polys(regions[n])
            small = [p for p in parts if p.area < min_area]
            if not small:
                continue
            keep = [p for p in parts if p.area >= min_area]
            for p in small:
                best, blen = None, 0.0
                for m in sorted(regions):
                    if m == n:
                        continue
                    L = p.boundary.intersection(regions[m].boundary).length if p.intersects(regions[m]) else 0.0
                    if L > blen:
                        best, blen = m, L
                if best is None:
                    keep.append(p)
                    continue
                regions[best] = clean(unary_union([regions[best], p]))
                merged += 1
                changed = True
            regions[n] = clean(unary_union(keep)) if keep else Polygon()
    return regions, merged


def _inseln_entfernen(L: np.ndarray, n_labels: int, min_px: int):
    """Zusammenhangskomponenten < min_px dem haeufigsten Nachbarlabel geben."""
    changed = 0
    for _ in range(4):
        any_change = False
        for k in range(n_labels):
            cc, num = ndi.label(L == k)
            if num == 0:
                continue
            sizes = ndi.sum(np.ones_like(cc), cc, index=np.arange(1, num + 1))
            for comp in np.where(sizes < min_px)[0] + 1:
                sl = ndi.find_objects((cc == comp).astype(np.uint8))[0]
                sl = tuple(slice(max(0, s.start - 1), s.stop + 1) for s in sl)
                m = cc[sl] == comp
                ring = ndi.binary_dilation(m) & ~m
                vals = L[sl][ring]
                vals = vals[vals != k]
                if len(vals) == 0:
                    continue
                L[sl][m] = np.bincount(vals).argmax()
                changed += 1
                any_change = True
        if not any_change:
            break
    return L, changed


def untergrund_partition_v2(substrates: np.ndarray, sigma_m: float = UNTER_SIGMA_M, arc_sigma_m: float = 0.8,
                            pad_m: float = 4.0):
    """Multi-Label-Glaettung: Indikator je Label auf 0,1 m, Gauss sigma, argmax,
    Inseln < 4 m2 an den Nachbarn, exakte Pixelkanten-Partition, dann jeden
    gemeinsamen Bogen zwischen Knoten einmal Gauss-glaetten (Enden fix)."""
    from shapely import line_merge
    from shapely.geometry import MultiLineString
    ny, nx = substrates.shape
    labels_all = substrates.astype(str)
    valid = ~np.isin(labels_all, NICHT_UNTERGRUND)
    _, (iy, ix) = ndi.distance_transform_edt(~valid, return_indices=True)
    assigned = labels_all[iy, ix]
    names = sorted(set(assigned.ravel().tolist()), key=lambda n: (-int(np.count_nonzero(assigned == n)), n))
    pad = int(round(pad_m / RES))
    best = None
    arg = None
    for k, n in enumerate(names):
        ind = np.pad(fine(assigned == n).astype(np.float32), pad, mode="edge")
        f = ndi.gaussian_filter(ind, sigma=sigma_m / RES, mode="nearest")[pad:-pad, pad:-pad]
        if best is None:
            best, arg = f, np.zeros(f.shape, np.uint8)
        else:
            upd = f > best
            best = np.where(upd, f, best)
            arg[upd] = k
    L, inseln = _inseln_entfernen(arg, len(names), int(round(UNTER_INSEL_M2 / RES / RES)))
    H, W = L.shape
    segs = []
    ii, jj = np.nonzero(L[1:, :] != L[:-1, :])
    for i, j in zip(ii, jj):
        z = (i + 1) * RES
        segs.append(((j * RES, z), ((j + 1) * RES, z)))
    ii, jj = np.nonzero(L[:, 1:] != L[:, :-1])
    for i, j in zip(ii, jj):
        x = (j + 1) * RES
        segs.append(((x, i * RES), (x, (i + 1) * RES)))
    net = unary_union([MultiLineString(segs), RECT.boundary], grid_size=1e-6)
    merged = line_merge(net)
    fb = RECT.boundary.buffer(1e-6)
    arcs = []
    for line in get_parts(merged):
        c = np.asarray(line.coords)
        if fb.contains(line) or len(c) < 3:
            arcs.append(line)
        else:
            o, ok = bogen_adaptiv(c, line.is_ring)
            if line.is_ring and not ok and Polygon(c).area >= 40.0:
                # grosse Insel: erst Oeffnen/Schliessen r=2 m, dann adaptiv glaetten
                rp = schliessen(oeffnen(Polygon(c), 2.0), 2.0)
                parts = [q for q in polys(rp) if q.area >= UNTER_INSEL_M2]
                if parts:
                    q = max(parts, key=lambda g: g.area)
                    o2, ok2 = bogen_adaptiv(np.asarray(q.exterior.coords), True)
                    if ok2 or LineString(o2).length > 0:
                        o, ok = o2, ok2
                        if not ok:
                            BOGEN_INSELN_ENTFALLEN.append(("rest", round(q.area, 1), round(float(o[:, 0].mean()), 1), round(float(o[:, 1].mean()), 1)))
                        arcs.append(LineString(o))
                        continue
            if line.is_ring and not ok:
                # geschlossene Insel, die kein sigma Q3-faehig macht (schmale
                # Ellipse < ~3,2 m Breite): Insel entfaellt, Flaeche geht an die Umgebung
                BOGEN_INSELN_ENTFALLEN.append((round(Polygon(c).area, 1), round(float(c[:, 0].mean()), 1), round(float(c[:, 1].mean()), 1)))
                continue
            arcs.append(LineString(o))
    faces = list(polygonize(unary_union(arcs)))
    regions = {n: [] for n in names}
    for face in faces:
        rp = face.representative_point()
        i = min(H - 1, max(0, int(rp.y / RES))); j = min(W - 1, max(0, int(rp.x / RES)))
        # Mehrheitslabel der Pixelmitten in der Flaeche (robust gegen Randpixel)
        x0, y0, x1, y1 = face.bounds
        j0, j1 = max(0, int(x0 / RES)), min(W, int(np.ceil(x1 / RES)))
        i0, i1 = max(0, int(y0 / RES)), min(H, int(np.ceil(y1 / RES)))
        from shapely import contains_xy
        xs, ys = np.meshgrid((np.arange(j0, j1) + 0.5) * RES, (np.arange(i0, i1) + 0.5) * RES)
        inside = contains_xy(face, xs, ys)
        if inside.any():
            k = int(np.bincount(L[i0:i1, j0:j1][inside]).argmax())
        else:
            k = int(L[i, j])
        regions[names[k]].append(face)
    regions = {n: clean(unary_union(v)) if v else Polygon() for n, v in regions.items()}
    return regions, assigned, {"inseln_umgelabelt": int(inseln), "labels": names}


def bogen_q3(p):
    """Offener Bogen: max(QA-Stuetzpunktmittel, 5-cm-Abtastung mit 0,5-m-Endschutz), Knick."""
    from shapely import distance, points
    p = np.asarray(p, float)
    n = len(p)
    if n < 3:
        return 0.0, 0.0
    seg = np.hypot(*np.diff(p, axis=0).T)
    s = np.r_[0, np.cumsum(seg)]
    T = s[-1]
    hw = np.minimum(0.5, np.minimum(s, T - s))
    lo = np.searchsorted(s, s - hw - 1e-9, side="left")
    hi = np.searchsorted(s, s + hw + 1e-9, side="right")
    cs = np.vstack([np.zeros((1, 2)), np.cumsum(p, axis=0)])
    g = (cs[hi] - cs[lo]) / (hi - lo)[:, None]
    qa = distance(points(p), LineString(g))
    qa[0] = qa[-1] = 0
    qa = float(qa.max())
    fine_ = 0.0
    if T >= 1.0:
        ss = np.linspace(0.0, T, max(2, int(np.ceil(T / 0.05)) + 1))
        xy = np.column_stack((np.interp(ss, s, p[:, 0]), np.interp(ss, s, p[:, 1])))
        m = np.column_stack([np.convolve(xy[:, k], np.ones(21) / 21, mode="valid") for k in range(2)])
        c, cs_ = xy[10:-10], ss[10:-10]
        v = (cs_ >= 0.5) & (cs_ <= T - 0.5)
        if v.any():
            fine_ = float(np.hypot(*(c - m).T)[v].max())
    v1 = p[1:-1] - p[:-2]; v2 = p[2:] - p[1:-1]
    cosv = (v1 * v2).sum(1) / (np.hypot(*v1.T) * np.hypot(*v2.T) + 1e-15)
    return max(qa, fine_), float(np.degrees(np.arccos(np.clip(cosv, -1, 1))).max())


BOGEN_SIGMAS = (0.8, 1.2, 1.6, 2.0, 2.5, 3.0, 4.0, 5.0, 6.5, 8.0)
BOGEN_INSELN_ENTFALLEN = []
BOGEN_LOG = []


def bogen_adaptiv(c, closed: bool):
    best = None
    for sg in BOGEN_SIGMAS:
        o = ring_glatt(c, sg) if closed else _glatt_offen(c, sg)
        a_, k_ = ring_q3(o) if closed else bogen_q3(o)
        score = max(a_ / RING_ZIEL_M, k_ / RING_ZIEL_GRAD)
        if best is None or score < best[0]:
            best = (score, sg, a_, k_, o)
        if score <= 1.0:
            break
    BOGEN_LOG.append(best[:4] + (round(float(best[4][:, 0].mean()), 1), round(float(best[4][:, 1].mean()), 1)))
    return best[4], (best[2] <= 0.0295 and best[3] <= 14.5)

