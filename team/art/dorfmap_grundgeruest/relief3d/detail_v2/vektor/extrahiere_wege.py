#!/usr/bin/env python3
"""P1a detail_v2 (Wege & Deko, 19.11.2026): Weg- und Kreuzungsvektoren als GeoJSON in Viewer-Metern (1 Einheit = 1 Zelle).

  python3 detail_v2/vektor/extrahiere_wege.py        (aus relief3d/; schreibt nur detail_v2/vektor/wege.geojson, kreuzungen.geojson)

Quelle: neu/vektor.json (wege[].mittellinie_m, breite_m, kreuzungen[].polygon_m; alles / 1,2 = Zellen = Viewer-Meter).
Koordinaten [x, z]: x nach Osten, z nach Sueden, Zelle (cx, cy) hat ihre Mitte bei (cx + 0,5, cy + 0,5) wie im Viewer.
Verfahren (DETAIL_V2_PLAN 3.1):
  Mittellinie: Douglas-Peucker 0,05 m -> zentripetaler Catmull-Rom -> alle 0,25 m abgetastet.
  Vorher [A, Methodenwechsel]: Gauss-Vorglaettung laengs (sigma <= 1,5 m, fertige Linie <= 0,25 m vom alten Verlauf), weil die Quelle ein
  Zellmitten-Polygonzug mit 45-Grad-Stufen ist (DP+CR allein: Zacken bis 0,17 m, Knick bis 78 Grad).
  Raender: Band = buffer(Breite/2, rund) = Offset +-Breite/2; enge Innenkurven mit r = RUND_M ausgerundet (Schliessen),
  Bandumriss zyklisch Gauss-geglaettet (sigma 0,3 m); Randlinien = Bandumriss ohne Endkappen (links/rechts), 0,25 m abgetastet. Wegnetz = Union der Baender + Kreuzungen.
  Innenrundung [A]: Schliessen mit r (2,2 m, sonst kleiner), Fuellflaechen breiter als 2*1,7 m (Innenraum von U-/Schleifenwegen) und
  Muendungs-Fuellungen an der eigenen Endkappe werden wieder freigegeben (sonst wurde z. B. G015/G018 zu einem Klumpen ohne Innenrand).
  Kreuzungen [A]: Polygon um e (0-2 m) erweitert, mit dem Bandnetz (+Saum 0-1,0 m) geschnitten, Ecken gerundet (r 2,0/1,85 m),
  Variante mit kleinstem Ueberstand ueber Bandnetz/Platz bei >= 90 % Abdeckung; Chaikin 2x, alle 0,25 m abgetastet.
  Das Bandnetz laeuft darunter durch (keine Luecke).
  Wegenden: Teilstuecke, die nicht frei im Gelaende enden, werden bis in die naechste Kreuzung bzw. das Nachbar-Teilstueck
  verlaengert (Anschluss), wenn sie dort nicht schon liegen.
"""
import base64, gzip, json, math, sys
from pathlib import Path
import numpy as np
import shapely as shp
from shapely.geometry import LineString, Polygon, MultiPolygon, Point, mapping
from shapely.ops import unary_union
from shapely import contains_xy
from scipy import ndimage as nd
from skimage.graph import route_through_array

R = Path(__file__).resolve().parents[2]          # relief3d/
AUS = Path(__file__).resolve().parent
ZW = 1.2                                          # m pro Zelle in vektor.json
DP_M = 0.05; SCHRITT_M = 0.25; RUND_M = 2.2; RUND_K_M = 2.0; KR_RAND_M = 0.6; KR_R = (2.0, 1.85); KR_E = (0.0, 0.5, 1.0, 1.5, 2.0); KR_SAUM = (0.0, 0.3, 0.6, 1.0); ERG_MIN = 40; RING_SIGMA_M = 0.3
RUND_STUFEN = (2.2, 1.8, 1.4, 1.0, 0.7, 0.5, 0.0); FREI_RHO = 1.7; RING_SIGMEN = (0.3, 0.45, 0.6)
KLASSEN = (("GASSE", 3.0), ("ANBINDUNG", 3.2 / 1.2), ("HAUSWEG", 2.0))
VOR_SIGMA_M = (1.5, 1.25, 1.0, 0.75, 0.5, 0.35, 0.25, 0.0); MITTE_MAX_M = 0.25

def catmull_rom(P, schritt=SCHRITT_M, alpha=0.5):
    """zentripetaler Catmull-Rom durch alle Punkte P (n x 2), Enden mit gespiegelten Hilfspunkten; gleichabstaendig abgetastet."""
    P = np.asarray(P, float)
    if len(P) < 2: return P
    if len(P) == 2:
        L = np.hypot(*(P[1] - P[0])); n = max(2, int(math.ceil(L / schritt)) + 1)
        return P[0] + np.linspace(0, 1, n)[:, None] * (P[1] - P[0])
    Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]]); dicht = []
    for i in range(len(Q) - 3):
        p0, p1, p2, p3 = Q[i:i + 4]
        t0 = 0.0; t1 = t0 + max(np.hypot(*(p1 - p0)), 1e-9) ** alpha
        t2 = t1 + max(np.hypot(*(p2 - p1)), 1e-9) ** alpha; t3 = t2 + max(np.hypot(*(p3 - p2)), 1e-9) ** alpha
        n = max(4, int(math.ceil(np.hypot(*(p2 - p1)) / 0.02)))
        t = np.linspace(t1, t2, n, endpoint=False)[:, None]
        A1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
        A2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
        A3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
        B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
        B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3
        dicht.append((t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2)
    dicht.append(P[-1:]); D = np.vstack(dicht)
    return abtasten(D, schritt)

def abtasten(D, schritt=SCHRITT_M, ring=False):
    D = np.asarray(D, float)
    if ring and not np.allclose(D[0], D[-1]): D = np.vstack([D, D[:1]])
    s = np.r_[0, np.cumsum(np.hypot(*np.diff(D, axis=0).T))]
    if s[-1] <= 0: return D[:1]
    n = max(2, int(round(s[-1] / schritt)) + 1); u = np.linspace(0, s[-1], n)
    out = np.c_[np.interp(u, s, D[:, 0]), np.interp(u, s, D[:, 1])]
    return out

def glaetten_sigma(P, sg):
    """[A] Methodenwechsel: die Quell-Mittellinie ist ein Zellmitten-Polygonzug (0/45-Grad-Stufen). DP 0,05 m behaelt die Stufen,
    Catmull-Rom laeuft durch jede Stufenecke -> Zacken bis 0,17 m, Knick bis 78 Grad. Darum vorher Gauss-Glaettung laengs der
    Bogenlaenge (Enden fest, gespiegelt fortgesetzt)."""
    Q = abtasten(P, 0.05); n = len(Q); k = sg / 0.05; r = int(3 * k)
    if n <= r + 1: return None
    x = np.arange(-r, r + 1); g = np.exp(-0.5 * (x / k) ** 2); g /= g.sum()
    pad = np.vstack([2 * Q[0] - Q[r:0:-1], Q, 2 * Q[-1] - Q[-2:-r - 2:-1]])
    S = np.c_[np.convolve(pad[:, 0], g, "valid"), np.convolve(pad[:, 1], g, "valid")]; S[0], S[-1] = Q[0], Q[-1]
    return S

def raender(band, M, h):
    """Randlinien = Aussenring des (geschlossenen) Bandes ohne die beiden Endkappen.
    Kappe = Ringpunkte im Halbraum hinter dem Wegende (Tangente nach aussen) und <= h+5 cm vom Endpunkt.
    Uebrige zyklische Laeufe (normal genau 2) -> Seite per Mehrheit des Vorzeichens zum naechsten Mittelliniensegment."""
    M = np.asarray(M); L = LineString(M)
    ring = abtasten(np.asarray(band.exterior.coords), SCHRITT_M, ring=True)[:-1]
    kappe = np.zeros(len(ring), bool)
    for E, N in ((M[0], M[0] - M[min(4, len(M) - 1)]), (M[-1], M[-1] - M[max(-5, -len(M))])):
        N = N / (np.linalg.norm(N) + 1e-12); v = ring - E
        kappe |= (v @ N > -1e-6) & (np.hypot(v[:, 0], v[:, 1]) <= h + 0.05)
    n = len(ring)
    if kappe.all() or not kappe.any(): return []
    start = int(np.argmax(kappe)); order = np.roll(np.arange(n), -start)
    laeufe = []; cur = []
    for i in order:
        if kappe[i]:
            if len(cur) >= 3: laeufe.append(cur)
            cur = []
        else: cur.append(i)
    if len(cur) >= 3: laeufe.append(cur)
    seg_a = M[:-1]; seg_d = M[1:] - M[:-1]; l2 = (seg_d ** 2).sum(1) + 1e-12
    def seite(q):
        t = np.clip(((q - seg_a) * seg_d).sum(1) / l2, 0, 1); f = seg_a + seg_d * t[:, None]
        k = int(np.argmin(((f - q) ** 2).sum(1))); d = seg_d[k]; v = q - seg_a[k]
        return np.sign(d[0] * v[1] - d[1] * v[0])
    out = []
    for idx in laeufe:
        P = ring[idx]; sg = np.sign(sum(seite(q) for q in P)) or 1
        out.append(("rand_links" if sg > 0 else "rand_rechts", P))
    return out

def chaikin(ring, n=2):
    P = np.asarray(ring, float)
    if np.allclose(P[0], P[-1]): P = P[:-1]
    for _ in range(n):
        Q = np.roll(P, -1, 0); P = np.stack([0.75 * P + 0.25 * Q, 0.25 * P + 0.75 * Q], 1).reshape(-1, 2)
    return np.vstack([P, P[:1]])

def runden(g, r=RUND_M):
    # Schliessen, Oeffnen, Schliessen: konvexe UND konkave Ecken (auch neu entstandene Einschnuerungs-Spitzen) mit Radius r
    return g.buffer(r, quad_segs=32).buffer(-2 * r, quad_segs=32).buffer(2 * r, quad_segs=32).buffer(-r, quad_segs=32)

def schliessen_frei(M, h, rr):
    """Band = Rohband (Offset +-h) geschlossen mit rr (Innenecken enger Kurven ausrunden), dann
    (a) Fuellflaechen breiter als 2*FREI_RHO (Innenraum von U-/Schleifenwegen) per Oeffnung wieder freigeben,
    (b) entsteht dabei ein neues Loch (die Fuellung schliesst die Muendung zwischen Wegende und eigenem Schenkel),
        die an eine Endkappe grenzenden Restfuellungen (> 0,5 m2) ebenfalls freigeben.
    Gibt None zurueck, wenn trotzdem ein neues Loch bleibt."""
    g = LineString(M).buffer(h, quad_segs=32)
    if rr <= 0: return groesste(g)
    c = groesste(g.buffer(rr, quad_segs=32).buffer(-rr, quad_segs=32)); zu = c.difference(g)
    if zu.is_empty: return c
    frei = zu.buffer(-FREI_RHO, quad_segs=32).buffer(FREI_RHO, quad_segs=32)
    if not frei.is_empty and frei.area > 1e-3: c = groesste(c.difference(frei).buffer(0))
    if len(c.interiors) == 0: return c
    rest = zu.difference(frei); kap = unary_union([Point(M[0]).buffer(h + 0.1), Point(M[-1]).buffer(h + 0.1)])
    mund = [q for q in getattr(rest, "geoms", [rest]) if q.area > 0.5 and q.intersects(kap)]
    if mund: c = groesste(c.difference(unary_union(mund)).buffer(0))
    return c if len(c.interiors) == 0 else None

def groesste(g):
    if isinstance(g, MultiPolygon): return max(g.geoms, key=lambda p: p.area)
    return g

def glatter_ring(poly):
    ext = abtasten(chaikin(np.asarray(poly.exterior.coords), 2), SCHRITT_M, ring=True)
    return Polygon(ext)

def wega_maske():
    D = json.load(gzip.open(R / "relief_daten.json.gz")); rs = D["rs"]; GX, GY = D["nx"] * rs + 1, D["ny"] * rs + 1
    A = np.frombuffer(base64.b64decode(D["WEGA"]), np.uint8).reshape(GY, GX)
    return A >= 128, rs

def mittellinie(P):
    """Vorglaettung -> DP 0,05 -> Catmull-Rom; sigma = groesstes, bei dem die FERTIGE Linie <= MITTE_MAX_M vom alten Verlauf bleibt."""
    P = np.asarray(P, float); alt = LineString(P); Qa = abtasten(P, 0.05)
    for sg in VOR_SIGMA_M:
        Pg = glaetten_sigma(P, sg) if sg > 0 else P
        if Pg is None: continue
        dp = np.asarray(LineString(Pg).simplify(DP_M, preserve_topology=False).coords); M = catmull_rom(dp)
        dev = max(float(shp.distance(alt, shp.points(M)).max()), float(shp.distance(LineString(M), shp.points(Qa)).max()))
        if dev <= MITTE_MAX_M or sg == 0: return M, sg

def netz_aus(wege, kpolys=()):
    return unary_union([e["band"] for e in wege] + list(kpolys))

def ring_glaetten(poly, sigma=RING_SIGMA_M):
    """Bandumriss zyklisch gaussgeglaettet (sigma 0,3 m, Verschiebung < 1 cm ausser an engsten Aussenkurven)."""
    Q = abtasten(np.asarray(poly.exterior.coords), 0.05, ring=True)[:-1]; k = sigma / 0.05; r = int(3 * k)
    x = np.arange(-r, r + 1); g = np.exp(-0.5 * (x / k) ** 2); g /= g.sum(); n = len(Q)
    idx = (np.arange(n)[:, None] + x[None]) % n; S = (Q[idx] * g[None, :, None]).sum(1)
    return groesste(Polygon(S).buffer(0))

def band_von(e):
    """Band je Weg: groesster Innenrundungsradius aus RUND_STUFEN und kleinstes Ring-sigma aus RING_SIGMEN, bei dem beide
    Randlinien die Eigenpruefung (Knick <= 14 Grad, Zacken <= 2,9 cm, also mit Reserve zur Abnahme) bestehen; sonst die beste Variante."""
    h = e["breite"] / 2; best = None
    for rr in RUND_STUFEN:
        c = schliessen_frei(e["M"], h, rr)
        if c is None: continue
        for sg in RING_SIGMEN:
            band = ring_glaetten(c, sg); R = raender(band, e["M"], h)
            note = max([rand_note(P) for _, P in R] + [9.0 if len(R) != 2 else 0.0])
            if best is None or note < best[0]: best = (note, band, rr, sg)
            if note <= 1.0: break
        if best[0] <= 1.0: break
    e["guete"], e["band"], e["rund_r"], e["ring_sigma"] = round(best[0], 3), best[1], best[2], best[3]
    return e

def rand_note(P, knick_max=14.0, zack_max=0.029):
    """max(Knick/knick_max, Zacken/zack_max) - wie test_wege.py (Zacken gegen 1-m-Mittel, 0,5 m Endausschluss); <= 1 = gut."""
    P = np.asarray(P)
    if len(P) < 3: return 0.0
    d = np.diff(P, axis=0); a = np.arctan2(d[:, 1], d[:, 0]); k = np.degrees(np.abs((np.diff(a) + np.pi) % (2 * np.pi) - np.pi))
    nk = k.max() / knick_max if k.size else 0.0
    Q = abtasten(P, 0.05); n = 21
    if len(Q) <= n + 20: return nk
    S = np.vstack([np.convolve(Q[:, j], np.ones(n) / n, mode="valid") for j in (0, 1)]).T; Qm = Q[n // 2: n // 2 + len(S)]
    z = np.hypot(*(Qm - S).T)[10:-10]
    return max(nk, (z.max() / zack_max) if z.size else 0.0)

def ergaenzungen(wege, kpolys, M, rs):
    """[A] Abgleich WEGA >= 0,5: Wegstuecke, die in vektor.json fehlen (Skelett-Bruchstuecke, E3-Bruecke), aus der WEGA-Maske
    nachziehen: Cluster ausserhalb des Netzes, die zwei Netzteile verbinden oder >= ERG_MIN Knoten haben -> Weg durch die
    Clustermitte (kuerzester Pfad, Kosten 1/(Randabstand)), Breite = Klassenbreite nach 2 x Median-Randabstand."""
    netz = netz_aus(wege, kpolys); teile = list(getattr(netz, "geoms", [netz]))
    zz, xx = np.nonzero(M); innen = contains_xy(netz.buffer(0.25), xx / rs, zz / rs)
    aus = np.zeros_like(M); aus[zz[~innen], xx[~innen]] = True
    lab, n = nd.label(aus, structure=np.ones((3, 3))); edt = nd.distance_transform_edt(M) / rs
    neu = []
    for k in range(1, n + 1):
        cz, cx = np.nonzero(lab == k)
        if len(cz) < 8: continue
        reg = nd.binary_dilation(lab == k, iterations=6) & M
        rz, rx = np.nonzero(reg & ~(lab == k))   # Anschlussknoten im Netz
        an = {}
        for z, x in zip(rz, rx):
            for i, t in enumerate(teile):
                if t.buffer(0.25).contains(Point(x / rs, z / rs)): an.setdefault(i, []).append((z, x)); break
        if not an: continue
        if len(an) < 2 and len(cz) < ERG_MIN: continue
        kosten = np.where(reg, 1.0 / (edt + 0.25), np.inf)
        if len(an) >= 2:
            a, b = list(an)[:2]; s0 = an[a][len(an[a]) // 2]; s1 = an[b][len(an[b]) // 2]
        else:
            a = list(an)[0]; s0 = an[a][len(an[a]) // 2]
            dd = (cz - s0[0]) ** 2 + (cx - s0[1]) ** 2; j = int(np.argmax(dd)); s1 = (cz[j], cx[j])
        try:
            pfad, _ = route_through_array(np.where(np.isfinite(kosten), kosten, 1e6), s0, s1, fully_connected=True, geometric=True)
        except Exception:
            continue
        P = np.array([(x / rs, z / rs) for z, x in pfad], float)
        if LineString(P).length < 1.0: continue
        brt = 2 * float(np.median(edt[tuple(np.array(pfad).T)]))
        klasse, breite = min(KLASSEN, key=lambda kb: abs(kb[1] - brt))
        Mx, sg = mittellinie(P)
        neu.append(band_von({"w": {"id": f"ERG{len(neu) + 1:02d}", "teil": 0, "klasse": klasse, "breite_m": round(breite * ZW, 3),
                                   "wegenden": [], "quellzellen": []}, "M": Mx, "breite": breite, "frei": {0: len(an) < 2 and False, 1: len(an) < 2},
                             "alt": None, "sigma": sg, "ergaenzung": {"wega_knoten": int(len(cz)), "netzteile": len(an), "breite_wega": round(brt, 2)}}))
    return neu

def platz_flaeche():
    import csv
    pl = [(int(r["cx"]), int(r["cy"])) for r in csv.DictReader(open(R.parent / "raster_c20_z25_overlay_plaetze_wege.csv")) if r["platz"]]
    return unary_union([Polygon([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]) for x, y in pl])

def kreuzung_einpassen(P, netz_baender, ziel):
    """[A, Methodenwechsel] Rohpolygon um e erweitert, auf Bandnetz (+Saum) beschnitten, mit r gerundet (Schliessen/Oeffnen).
    Gesucht ueber r in KR_R (>= 1,85 m, sonst Zacken > 2,9 cm nach Chaikin), e in KR_E, Saum in KR_SAUM: die Variante mit dem kleinsten Ueberstand
    ueber Bandnetz/Platz (ziel), die >= 90 % von P-geschnitten-Bandnetz abdeckt (bei Gleichstand +-5 cm die mit groesserem r).
    Grund: die vektor.json-Polygone sind oft schmaler als 2r (z. B. 1 m breite Rechtecke), Rundung allein loescht sie;
    der fruehere Rueckfall 'P + 2 m' stand bis 2,4 m ueber."""
    ref = P.intersection(netz_baender); best = None
    for r in KR_R:
        for e in KR_E:
            for saum in KR_SAUM:
                roh = groesste(P.buffer(e, quad_segs=32).intersection(netz_baender.buffer(saum, quad_segs=32)))
                if roh.is_empty: continue
                g = groesste(runden(roh, r))
                if g.is_empty or (ref.area > 0 and g.intersection(ref).area < 0.9 * ref.area): continue
                C = abtasten(np.asarray(g.exterior.coords), SCHRITT_M, ring=True); o = float(shp.distance(ziel, shp.points(C)).max())
                if best is None or o < best[0] - 0.05: best = (o, g, {"r": r, "erweiterung": e, "saum": saum, "ueberstand_m": round(o, 3)})
    if best is None: raise RuntimeError("Kreuzung nicht einpassbar")
    return best[1], best[2]

def main():
    V = json.load(open(R / "neu" / "vektor.json", encoding="utf-8"))
    M, rs = wega_maske()
    ausgelassen = []; wege = []
    for w in V["wege"]:
        P = np.asarray(w["mittellinie_m"], float) / ZW
        if len(P) < 2 or LineString(P).length < 0.5:
            ausgelassen.append({"id": w["id"], "teil": w["teil"], "punkte": len(P), "grund": "Teilstueck < 0,5 m (Skelettrest, wird ueber Kreuzung/WEGA-Ergaenzung abgedeckt)"}); continue
        Mx, sg = mittellinie(P)
        ends = {e["zell_id"] for e in w["wegenden"] if e["ziel"] == "gelaende"}; q = w["quellzellen"]
        frei = {0: bool(q and q[0] in ends), 1: False}
        frei[1] = bool(q and q[-1] in ends and (len(q) > 1 or not frei[0]))
        wege.append(band_von({"w": w, "M": Mx, "breite": w["breite_m"] / ZW, "frei": frei, "alt": P, "sigma": sg}))
    kr = [(k, Polygon(np.asarray(k["polygon_m"], float) / ZW).buffer(0)) for k in V["kreuzungen"]]
    wege += ergaenzungen(wege, [p for _, p in kr], M, rs)
    K_alle = unary_union([p for _, p in kr])
    anschluss = []
    for i, e in enumerate(wege):
        for seite in (0, 1):
            if e["frei"][seite]: continue
            Mx = e["M"]; p = Point(Mx[0] if seite == 0 else Mx[-1])
            if K_alle.buffer(0.01).contains(p): continue
            andere = unary_union([f["band"] for j, f in enumerate(wege) if j != i])
            if andere.contains(p): continue
            d = p.distance(unary_union([K_alle, andere]))
            if d > 3.0: anschluss.append({"id": e["w"]["id"], "teil": e["w"]["teil"], "seite": seite, "abstand_m": round(d, 2), "aktion": "keine (> 3 m)"}); continue
            t = (Mx[0] - Mx[1]) if seite == 0 else (Mx[-1] - Mx[-2]); t = t / np.linalg.norm(t)
            ext = np.array(p.coords[0]) + t * (d + 0.5)
            e["M"] = abtasten(np.vstack([ext, Mx]) if seite == 0 else np.vstack([Mx, ext])); band_von(e)
            anschluss.append({"id": e["w"]["id"], "teil": e["w"]["teil"], "seite": seite, "abstand_m": round(d, 2), "aktion": "verlaengert"})
    feats = []
    for e in wege:
        w = e["w"]; h = e["breite"] / 2; L = LineString(e["M"])
        props = {"id": w["id"], "teil": w["teil"], "klasse": w["klasse"], "breite": round(2 * h, 4), "breite_m_quelle": w["breite_m"],
                 "frei_anfang": e["frei"][0], "frei_ende": e["frei"][1], "vorglaettung_sigma_m": e["sigma"], "innenrundung_r": e["rund_r"], "ring_sigma_m": e["ring_sigma"], "rand_eigennote": e["guete"],
                 "quelle": "WEGA-Ergaenzung" if e.get("ergaenzung") else "vektor.json"}
        if e.get("ergaenzung"): props["ergaenzung"] = e["ergaenzung"]
        feats.append({"type": "Feature", "properties": dict(props, rolle="mittellinie"), "geometry": mapping(L)})
        for name, Pr in raender(e["band"], e["M"], h):
            feats.append({"type": "Feature", "properties": dict(props, rolle=name), "geometry": mapping(LineString(Pr))})
        feats.append({"type": "Feature", "properties": dict(props, rolle="band"), "geometry": mapping(e["band"])})
    netz_baender = netz_aus(wege); ziel = netz_baender.union(platz_flaeche()); shp.prepare(ziel)
    kfeats = []; kpolys = []
    for k, P in kr:
        g, saum = kreuzung_einpassen(P, netz_baender, ziel)
        G = groesste(glatter_ring(g).buffer(0))
        kpolys.append(G)
        kfeats.append({"type": "Feature", "properties": {"id": k["id"], "art": k["art"], "weg_ids": k["weg_ids"], "platz_ids": k["platz_ids"],
                       "hoehe_m_quelle": k["hoehe_m"], "flaeche": round(G.area, 3), "einpassung": saum}, "geometry": mapping(G)})
    netz = unary_union([netz_baender] + kpolys)
    feats.append({"type": "Feature", "properties": {"rolle": "netz", "teile": len(getattr(netz, "geoms", [netz]))}, "geometry": mapping(netz)})
    meta = {"einheit": "Viewer-Meter, 1 Einheit = 1 Zelle (= 1,2 m in vektor.json)", "achsen": "[x Ost, z Sued]", "quelle": "neu/vektor.json + WEGA>=0,5 (relief_daten.json.gz)",
            "verfahren": {"vorglaettung": {"sigma_m": VOR_SIGMA_M, "max_abweichung_fertig_m": MITTE_MAX_M}, "dp_m": DP_M, "spline": "Catmull-Rom zentripetal", "abtastung_m": SCHRITT_M,
                          "rand": "buffer(Breite/2) + Innenrundung r (Schliessen, breite Fuellungen/Muendungen wieder frei), Ring-Gauss sigma", "rand_rund_m": RUND_STUFEN, "frei_rho_m": FREI_RHO, "ring_sigma_m": RING_SIGMEN, "kreuzung": {"r_m": KR_R, "erweiterung_m": KR_E, "saum_m": KR_SAUM, "abdeckung_min": 0.9, "wahl": "kleinster Ueberstand"}, "chaikin": 2},
            "ausgelassen": ausgelassen, "anschluss": anschluss}
    def _r(x):   # Koordinaten auf 0,1 mm (4 Nachkommastellen) runden: Dateigroesse, Messwerte unveraendert
        return [_r(y) for y in x] if isinstance(x, (list, tuple)) else round(float(x), 4)
    for f in feats + kfeats: f["geometry"] = dict(f["geometry"], coordinates=_r(f["geometry"]["coordinates"]))
    json.dump({"type": "FeatureCollection", "name": "wege", "meta": meta, "features": feats}, open(AUS / "wege.geojson", "w"), separators=(",", ":"))
    json.dump({"type": "FeatureCollection", "name": "kreuzungen", "meta": {k: meta[k] for k in ("einheit", "achsen", "quelle")}, "features": kfeats}, open(AUS / "kreuzungen.geojson", "w"), separators=(",", ":"))
    print(json.dumps({"wege_teile": len(wege), "ergaenzungen": [(e["w"]["id"], e["w"]["klasse"], e["ergaenzung"]) for e in wege if e.get("ergaenzung")],
                      "ausgelassen": len(ausgelassen), "anschluss": anschluss, "kreuzungen": len(kpolys), "netz_teile": len(getattr(netz, "geoms", [netz]))}, ensure_ascii=False))

if __name__ == "__main__":
    main()
