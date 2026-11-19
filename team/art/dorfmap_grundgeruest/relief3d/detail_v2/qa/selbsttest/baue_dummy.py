#!/usr/bin/env python3
"""Dummy-Datensatz im verbindlichen detail_v2-Format (PLAN_QA_DV2.md Abschn. 8) fuer den QA-Selbsttest.
Seit Runde 2 (19.11.): Gelaende geschlossen inkl. Bachbett (Klasse 4 unter dem Spiegel), Wasserspiegel als eigenes Modell
modelle[wasser_W01] (klasse 4, 5 cm ins Ufer gezogen); wege.geojson/kreuzungen.geojson im echten Schema (#56).
4 Kacheln D2/E2/D3/E3 (x 126-210, z 43-129). Sauber + je eine Fehlervariante pro Regel (--fehler Q5 ...).
Netz: zweistufiger Quadtree (0,4 m Grund, 0,2 m in Baendern +-1,5 m um Constraint-Linien und um den Schnitt z=86),
alle Constraint-Linien liegen auf dem 0,2-m-Raster (Dummy-Vereinfachung, echte Kurven testet selbsttest.py separat)."""
import argparse, json, shutil, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dv2qa.glb import schreibe_glb
from dv2qa.geom import KLASSEN, Ortung

X0, Z0, X1, Z1 = 126.0, 43.0, 210.0, 129.0
F = 0.2                                        # feines Raster
XC, HW, WB, D = 191.5, 2.1, 3.5, 0.75           # Bach: Mitte, halbe Wasserbreite, Boeschungsoberkante, Tiefe
H_FLACH = 3.0 + 0.015 * 54
SPIEGEL = H_FLACH - D * (1 - (HW / WB) ** 2)   # = 3.106
WEGE = [  # id, Mittellinie, Breite
    ('W1', [(130.0, 74.6), (188.0, 74.6)], 2.0),
    ('W2', [(195.0, 74.6), (197.6, 74.6)], 2.0),
    ('W3', [(200.0, 60.0), (200.0, 125.0)], 2.0),
    ('W4', [(130.0, 100.0), (186.0, 100.0)], 2.0),
]
KREUZ = (197.6, 72.2, 202.4, 77.0)
BAU_C, BAU_R = (205.0, 112.0), 6.0
FELS_C, FELS_H = (143.0, 113.2), 2.5
BR = dict(x0=187.6, x1=195.4, z0=73.6, z1=75.6, deck=H_FLACH - 0.04)


def smooth(e0, e1, v):
    t = np.clip((v - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)


def h_grund(x, z):
    s = 1 - smooth(160, 180, x)
    return 3.0 + 0.015 * np.minimum(x - 126, 54) + 0.1 * np.sin(z / 8) * s


def senk_faktor(x, z):
    f = np.zeros_like(x)
    for _, pl, b in WEGE:
        (ax, az), (bx, bz) = pl
        if az == bz:   # entlang x
            t, d, lo, hi = x, np.abs(z - az), min(ax, bx), max(ax, bx)
        else:
            t, d, lo, hi = z, np.abs(x - ax), min(az, bz), max(az, bz)
        quer = 1 - np.clip((d - b / 2) / 0.4, 0, 1)
        laengs = np.clip((t - lo) / 0.4, 0, 1) * np.clip((hi - t) / 0.4, 0, 1)
        if (pl == WEGE[1][1]) or (pl == WEGE[0][1]):   # Bruecken-/Kreuzungsanschluss: am Bruecken-/Kreuzungsende voll
            pass
        f = np.maximum(f, quer * laengs)
    kx0, kz0, kx1, kz1 = KREUZ
    dx = np.maximum(np.maximum(kx0 - x, x - kx1), 0); dz = np.maximum(np.maximum(kz0 - z, z - kz1), 0)
    f = np.maximum(f, 1 - np.clip(np.hypot(dx, dz) / 0.4, 0, 1))
    return f


def hoehe(x, z, fehler=None, d2_toleranz=True):
    h = h_grund(x, z)
    dx = np.abs(x - XC)
    h = h - np.where(dx < WB, D * (1 - (dx / WB) ** 2), 0)
    # Bachbett (Klasse 4) setzt die Boeschungsparabel unter dem Spiegel fort: Gelaende geschlossen, Tiefe Mitte 0,27 m unter Spiegel
    h = h + FELS_H * np.clip(1 - np.maximum(np.abs(x - FELS_C[0]), np.abs(z - FELS_C[1])) / 3.0, 0, 1)   # Felskegel (> 25 Grad)
    f = senk_faktor(x, z)
    if fehler == 'Q6':   # Weg W4 auf x 150-156 nicht eingesenkt
        f = np.where((x >= 150) & (x <= 156) & (np.abs(z - 100) < 1.5), 0, f)
    h = h - 0.04 * f
    if fehler == 'Q4':   # Buckel 5 cm in der Kreuzung
        h = h + 0.05 * np.clip(1 - np.hypot(x - 200, z - 74.6) / 1.2, 0, 1)
    if fehler == 'Q5':   # Delle 6 cm, 2 m neben Wegrand W1
        h = h - 0.06 * np.clip(1 - ((x - 150) ** 2 + (z - 77.6) ** 2) / 0.36, 0, 1)
    if fehler == 'Q7':   # D2: Flaeche 1,5 cm angehoben (> 1 cm)
        h = h + np.where((x >= 140) & (x <= 150) & (z >= 50) & (z <= 60), 0.015, 0)
    elif d2_toleranz:   # sauber: 0,8 cm Toleranzfall (<= 1 cm) im D2-Bereich
        h = h + np.where((x >= 140) & (x <= 150) & (z >= 50) & (z <= 60), 0.008, 0)
    return h


def klasse(x, z):
    k = np.zeros(x.shape, int)
    dx = np.abs(x - XC)
    k[(dx < HW + 2.6)] = 2   # Uferband 2,6 m (auf 0,2-m-Raster)
    k[(dx < HW)] = 4
    for _, pl, b in WEGE:
        (ax, az), (bx, bz) = pl
        if az == bz: m = (np.abs(z - az) < b / 2) & (x > min(ax, bx)) & (x < max(ax, bx))
        else: m = (np.abs(x - ax) < b / 2) & (z > min(az, bz)) & (z < max(az, bz))
        k[m] = 1
    kx0, kz0, kx1, kz1 = KREUZ
    k[(x > kx0) & (x < kx1) & (z > kz0) & (z < kz1)] = 1
    k[(np.abs(x - FELS_C[0]) < 3.0) & (np.abs(z - FELS_C[1]) < 3.0)] = 3
    return k


def weg_chart(x, z):
    """UV2-Karte je Wegdreieck: Index in WEGE (Kreuzung -> W3) und (u, v) = (Bogenlaenge, quer 0-1)."""
    c = np.full(x.shape, -1)
    for i, (_, pl, b) in enumerate(WEGE):
        (ax, az), (bx, bz) = pl
        if az == bz: m = (np.abs(z - az) < b / 2) & (x > min(ax, bx)) & (x < max(ax, bx))
        else: m = (np.abs(x - ax) < b / 2) & (z > min(az, bz)) & (z < max(az, bz))
        c[m & (c < 0)] = i
    kx0, kz0, kx1, kz1 = KREUZ
    c[(x > kx0) & (x < kx1) & (z > kz0) & (z < kz1)] = 2
    return c


def weg_uv2(i, x, z):
    _, pl, b = WEGE[i]; (ax, az), (bx, bz) = pl
    if az == bz: return np.c_[x - ax, (z - (az - b / 2)) / b]
    return np.c_[z - az, (x - (ax - b / 2)) / b]


def constraint_segmente():
    seg = []
    for _, pl, b in WEGE:
        (ax, az), (bx, bz) = pl
        if az == bz: seg += [((ax, az - b / 2), (bx, az - b / 2)), ((ax, az + b / 2), (bx, az + b / 2))]
        else: seg += [((ax - b / 2, az), (ax - b / 2, bz)), ((ax + b / 2, az), (ax + b / 2, bz))]
    kx0, kz0, kx1, kz1 = KREUZ
    seg += [((kx0, kz0), (kx1, kz0)), ((kx1, kz0), (kx1, kz1)), ((kx1, kz1), (kx0, kz1)), ((kx0, kz1), (kx0, kz0))]
    seg += [((XC - HW, Z0), (XC - HW, Z1)), ((XC + HW, Z0), (XC + HW, Z1))]
    return seg


def baue_netz():
    """-> V (n x 2 xz), Dreiecke (m x 3) mit Orientierung 'Normale nach oben'."""
    ni, nj = round((X1 - X0) / F), round((Z1 - Z0) / F)
    seg = constraint_segmente() + [((X0, 86.0), (X1, 86.0))]
    from shapely import STRtree, linestrings, points, distance
    tree = STRtree(linestrings(np.array(seg)))
    knoten = {}
    pts = []
    def vid(i2, j2):   # Index in halben Feinzellen (0,1 m), damit Mittelpunkte ganzzahlig sind
        k = (i2, j2)
        if k not in knoten:
            knoten[k] = len(pts); pts.append((round(X0 + 0.1 * i2, 6), round(Z0 + 0.1 * j2, 6)))
        return knoten[k]
    # Grundzellen 0,4 m (2x2 fein), Reihen ab Z0; die Reihe ueber z=86 (j 214-216) wird verfeinert
    fein = np.zeros((ni // 2, (nj + 1) // 2), bool)
    I, J = np.meshgrid(np.arange(ni // 2), np.arange((nj + 1) // 2), indexing='ij')
    cx = X0 + 0.4 * I + 0.2; cz = Z0 + 0.4 * J + 0.2
    d = np.full(cx.shape, np.inf)
    ii, jj = tree.query(points(np.c_[cx.ravel(), cz.ravel()]), predicate='dwithin', distance=1.5 + 0.2829 + 0.01)
    fein.ravel()[np.unique(ii)] = True
    fein |= (cz + 0.2 > Z1)   # letzte (halbe) Reihe
    tris = []
    for a in range(ni // 2):
        for b in range((nj + 1) // 2):
            i0, j0 = 2 * a, 2 * b
            if fein[a, b]:
                for di in (0, 1):
                    for dj in (0, 1):
                        i, j = i0 + di, j0 + dj
                        if j >= nj: continue
                        p00, p10, p01, p11 = vid(2 * i, 2 * j), vid(2 * i + 2, 2 * j), vid(2 * i, 2 * j + 2), vid(2 * i + 2, 2 * j + 2)
                        tris += [(p00, p10, p11), (p00, p11, p01)]
            else:
                nb = lambda aa, bb: 0 <= aa < fein.shape[0] and 0 <= bb < fein.shape[1] and fein[aa, bb]
                h_s, h_n, h_w, h_e = nb(a, b - 1), nb(a, b + 1), nb(a - 1, b), nb(a + 1, b)
                if not (h_s or h_n or h_w or h_e):
                    p00, p10, p01, p11 = vid(2 * i0, 2 * j0), vid(2 * i0 + 4, 2 * j0), vid(2 * i0, 2 * j0 + 4), vid(2 * i0 + 4, 2 * j0 + 4)
                    tris += [(p00, p10, p11), (p00, p11, p01)]
                else:
                    c = vid(2 * i0 + 2, 2 * j0 + 2)
                    ring = [(0, 0)] + ([(2, 0)] if h_s else []) + [(4, 0)] + ([(4, 2)] if h_e else []) + [(4, 4)] + \
                           ([(2, 4)] if h_n else []) + [(0, 4)] + ([(0, 2)] if h_w else [])
                    r = [vid(2 * i0 + u, 2 * j0 + v) for u, v in ring]
                    for k in range(len(r)): tris.append((c, r[k], r[(k + 1) % len(r)]))
    P = np.array(pts); T = np.array(tris)
    # Orientierung: Normale nach oben <=> signierte XZ-Flaeche < 0
    a = P[T[:, 1]] - P[T[:, 0]]; b = P[T[:, 2]] - P[T[:, 0]]
    sa = a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]
    T[sa > 0] = T[sa > 0][:, [0, 2, 1]]
    return P, T


def kachel_id(x, z):
    return 'ABCDEFGH'[int(x // 42)] + str(int(z // 43) + 1)


def box(x0, x1, y0, y1, z0, z1):
    v = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], float)
    f = [(0, 1, 3), (0, 3, 2), (4, 6, 7), (4, 7, 5), (0, 4, 5), (0, 5, 1), (2, 3, 7), (2, 7, 6), (0, 2, 6), (0, 6, 4), (1, 5, 7), (1, 7, 3)]
    return v, np.array(f)


def bruecke(fehler=None):
    teile = {}
    def add(name, v, f):
        if name in teile:
            V, Fa = teile[name]; teile[name] = (np.vstack([V, v]), np.vstack([Fa, f + len(V)]))
        else: teile[name] = (v, f)
    b = BR; top = b['deck']
    x = b['x0']
    while x < b['x1'] - 1e-6:
        add('bohlen', *box(x + 0.01, min(x + 0.19, b['x1']), top - 0.05, top, b['z0'], b['z1'])); x += 0.2
    for zt in (b['z0'] + 0.2, b['z1'] - 0.35):
        add('traeger', *box(b['x0'], b['x1'], top - 0.3, top - 0.05, zt, zt + 0.15))
    for xp in np.arange(b['x0'] + 0.1, b['x1'], 1.6):
        for zp in (b['z0'], b['z1'] - 0.1): add('pfosten', *box(xp, xp + 0.1, top, top + 1.0, zp, zp + 0.1))
    if fehler != 'Q12':
        for zp in (b['z0'], b['z1'] - 0.1):
            add('handlauf', *box(b['x0'], b['x1'], top + 0.94, top + 1.0, zp, zp + 0.1))
            add('gelaender', *box(b['x0'], b['x1'], top + 0.45, top + 0.5, zp + 0.02, zp + 0.08))
    # Widerlager: Unterkante 0,6 m im Gelaende (Fehlervariante: Unterkante 5 cm UEBER dem Gelaende -> Spalt)
    for xa, xb in ((b['x0'] - 0.2, b['x0'] + 0.4), (b['x1'] - 0.4, b['x1'] + 0.2)):
        if fehler == 'Q12': add('widerlager', *box(xa, xb, H_FLACH + 0.05, H_FLACH + 0.35, b['z0'], b['z1']))
        else: add('widerlager', *box(xa, xb, top - 0.6, top - 0.3, b['z0'], b['z1']))
    return [{'name': k, 'prims': [{'pos': v, 'idx': f}]} for k, (v, f) in teile.items()]


def spiegel_modell(fehler=None):
    """Wasserspiegel als eigenes Modell (klasse 4): Streifen ueber dem Bett, 5 cm ins Ufer gezogen; Fehlervarianten:
    Q8 +10 cm, Q8_spalt linke Kante 15 cm zu kurz (Spalt), Q8_ohne_schnitt 0,4 m tiefer (unter dem Bett), Q14_wasser +5 cm (Kante 0,5 m),
    Q8_ueberlappung Kanten 0,3 m ins Ufer (> 10 cm)."""
    y = SPIEGEL + {'Q8': 0.1, 'Q8_ohne_schnitt': -0.4, 'Q14_wasser': 0.05}.get(fehler, 0.0)
    ue = {'Q14_wasser': 0.5, 'Q8_ueberlappung': 0.3}.get(fehler, 0.05)
    xl = XC - HW + 0.15 if fehler == 'Q8_spalt' else XC - HW - ue; xr = XC + HW + ue
    zs = np.arange(Z0, Z1 + 1e-9, 1.0); n = len(zs)
    pos = np.vstack([np.c_[np.full(n, xl), np.full(n, y), zs], np.c_[np.full(n, xr), np.full(n, y), zs]])
    idx = []
    for i in range(n - 1): idx += [(i, n + i, n + i + 1), (i, n + i + 1, i + 1)]
    I = np.array(idx); P2 = pos[:, [0, 2]]; a = P2[I[:, 1]] - P2[I[:, 0]]; b = P2[I[:, 2]] - P2[I[:, 0]]
    sa = a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]; I[sa > 0] = I[sa > 0][:, [0, 2, 1]]
    return {'pos': pos, 'idx': I, 'flaeche': np.full(len(pos), 4.0), 'normal': np.tile([0, 1, 0], (len(pos), 1)),
            'uv0': pos[:, [0, 2]].copy(), 'uv1': np.c_[pos[:, 0] / 336, pos[:, 2] / 303]}


def schreibe_png16(pfad, arr):
    from PIL import Image
    Image.fromarray(arr.astype(np.uint16)).save(pfad)


def schreibe_png8(pfad, arr):
    from PIL import Image
    Image.fromarray(arr.astype(np.uint8)).save(pfad)


TEST_MJS = r'''// Dummy-Test fuer den QA-Selbsttest: echte Datenschicht (query.mjs/manifest.mjs aus art/dorfmap-fertig) auf dem Dummy-Mesh.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { ladeDatenschicht } from '../query.mjs';
import { ladeMesh } from '../manifest.mjs';
const hier = dirname(fileURLToPath(import.meta.url));
const mesh = await ladeMesh(join(hier, '..', '..', 'mesh', 'manifest.json'));
const ds = await ladeDatenschicht(join(hier, '..'), { gelaende: mesh.gelaende });
test('Weg W4 ist Weg und eingesenkt', () => { const a = ds.queryPoint(150, 100), b = ds.queryPoint(150, 102.5);
  assert.equal(a.flaeche, 'weg'); assert.ok(b.hoehe - a.hoehe > 0.03); assert.equal(a.kachel, 'D3'); });
test('Bach ist Wasser und nicht begehbar', () => { const q = ds.queryPoint(191.5, 100); assert.equal(q.flaeche, 'wasser'); assert.equal(q.begehbar, false); });
test('Dreiecke klassenrein', () => { assert.equal(mesh.pruefung.gemischte_dreiecke, 0); });
'''


def fc(features):
    return {'type': 'FeatureCollection', 'features': features}


def feat(geom, **pr):
    return {'type': 'Feature', 'properties': pr, 'geometry': geom}


def baue(ziel, fehler=None):
    ziel = Path(ziel)
    if ziel.exists(): shutil.rmtree(ziel)
    for d in ('mesh/kacheln', 'mesh/modelle', 'vektor', 'daten/test', 'referenz', 'abnahme'): (ziel / d).mkdir(parents=True, exist_ok=True)
    P, T = baue_netz()
    H = hoehe(P[:, 0], P[:, 1], fehler)
    if fehler == 'Q2':   # Constraint-Vertices auf Wegrand z=73.6, x 140-145 um 4 cm verschoben
        m = (np.abs(P[:, 1] - 73.6) < 1e-6) & (P[:, 0] > 140) & (P[:, 0] < 145); P = P.copy(); P[m, 1] += 0.04
    if fehler == 'Q7_lage':  # Lage: Weg W1 im D2-Bereich um 0,6 m nach Norden verschoben (Hoehen)
        H = hoehe(P[:, 0], np.where(P[:, 0] < 168, P[:, 1] - 0.6, P[:, 1]), None, d2_toleranz=False)
    V = np.c_[P[:, 0], H, P[:, 1]]
    cen = P[T].mean(1)
    kl = klasse(cen[:, 0], cen[:, 1])
    chart = np.where(kl == 1, weg_chart(cen[:, 0], cen[:, 1]), -1)
    kid = np.array([kachel_id(x, z) for x, z in cen])
    if fehler in ('Q1', 'Q1_bett'):   # Q1_bett: Loch im Bachbett unter dem Spiegel (Spiegel darf es nicht verdecken)
        mx, mz = (205, 110) if fehler == 'Q1' else (XC, 110)
        weg = np.hypot(cen[:, 0] - mx, cen[:, 1] - mz) < 0.5; T, kl, kid, cen, chart = T[~weg], kl[~weg], kid[~weg], cen[~weg], chart[~weg]
    if fehler == 'Q9':
        sel = np.nonzero(kid == 'D3')[0][:5]; T = T.copy(); T[sel] = T[sel][:, [0, 2, 1]]
    manifest = {'version': 1, 'einheit': 'm', 'ursprung': 'weltecke', 'karte': {'breite': 336, 'tiefe': 303},
                'klassen': {str(i): k for i, k in enumerate(KLASSEN)}, 'attribute': {'flaeche': '_FLAECHE'},
                'uv': {'TEXCOORD_0': 'welt_xz_m', 'TEXCOORD_1': 'karte_norm', 'TEXCOORD_2': 'wegband'}, 'kacheln': [],
                'modelle': [{'id': 'bruecke_E2', 'glb': 'modelle/bruecke_E2.glb', 'klasse': 5},
                            {'id': 'wasser_W01', 'glb': 'modelle/wasser_W01.glb', 'klasse': 4}]}
    kach = {'D2': (126, 43, 168, 86), 'E2': (168, 43, 210, 86), 'D3': (126, 86, 168, 129), 'E3': (168, 86, 210, 129)}
    ges = {}; dup = 0
    for k, bd in kach.items():
        sel = np.nonzero(kid == k)[0]
        # Vertices je (Klasse, UV2-Karte) duplizieren -> Dreiecke klassenrein, Grenzvertices positionsgleich doppelt
        schl = kl[sel] * 10 + (chart[sel] + 1)
        pos, flae, uv2, idx = [], [], [], []
        basis = 0
        for sk in np.unique(schl):
            ts = T[sel[schl == sk]]; used = np.unique(ts); remap = np.full(len(V), -1); remap[used] = np.arange(len(used)) + basis
            Vk = V[used].copy(); c = sk // 10; ch = sk % 10 - 1
            if fehler == 'Q1' and k == 'E2':
                m = np.nonzero((np.abs(Vk[:, 0] - 168) < 1e-6) & (np.abs(Vk[:, 2] - 50.2) < 1e-6))[0]; Vk[m, 1] += 0.001
            if fehler == 'Q1_luecke' and c == 1 and ch == 3:   # echte Luecke: Weg-Duplikate am Rand z=99 (x 150-153) 1 cm verschoben
                m = (np.abs(Vk[:, 2] - 99.0) < 1e-6) & (Vk[:, 0] >= 150) & (Vk[:, 0] <= 153); Vk[m, 2] += 0.01
            pos.append(Vk); flae.append(np.full(len(Vk), c, float))
            u2k = weg_uv2(ch, Vk[:, 0], Vk[:, 2]) if ch >= 0 else np.zeros((len(Vk), 2))
            if fehler == 'Q10_kurve' and ch == 3: u2k[:, 0] += 0.15 * np.clip(Vk[:, 0] - 152.5, 0, 3)   # 15 % Stauchung in enger Kurve (r < 10 m)
            uv2.append(u2k)
            idx.append(remap[ts]); basis += len(used)
        Vk = np.vstack(pos); fl = np.concatenate(flae); u2 = np.vstack(uv2); I = np.vstack(idx)
        dup += len(Vk) - len(np.unique(np.round(Vk, 5), axis=0))
        uv0 = Vk[:, [0, 2]].copy(); uv1 = np.c_[Vk[:, 0] / 336, Vk[:, 2] / 303]
        if fehler == 'Q10' and k == 'E3': uv0[:, 0] *= -1; uv1[:, 0] += 0.001
        fels = fl == 3
        if fehler == 'Q10_triplanar': uv0[np.nonzero(fels)[0][::7], 0] = np.nan; uv0[np.nonzero(fels)[0][1::7]] += 0.05   # NaN + Sprung
        if fehler == 'Q10_flip': uv0[fels, 0] = 2 * FELS_C[0] - uv0[fels, 0]        # gespiegelte UV in der Triplanar-Zone
        if fehler == 'Q10_uv2': u2[(fl == 1) & (np.abs(Vk[:, 2] - 100) < 1.01) & (Vk[:, 0] > 150) & (Vk[:, 0] < 160), 0] *= 1.3
        prim = {'pos': Vk, 'uv0': uv0, 'uv1': uv1, 'uv2': u2, 'flaeche': fl, 'normal': np.tile([0, 1, 0], (len(Vk), 1)), 'idx': I}
        schreibe_glb(ziel / 'mesh' / 'kacheln' / f'{k}.glb', [{'name': f'gelaende_{k}', 'prims': [prim]}])
        ges[k] = int(len(I))
        ka = {str(c): round(float((fl[I[:, 0]] == c).mean()), 4) for c in range(6) if (fl[I[:, 0]] == c).any()}
        manifest['kacheln'].append({'id': k, 'glb': f'kacheln/{k}.glb', 'bbox': list(bd), 'dreiecke': ges[k], 'klassen_anteil': ka})
    (ziel / 'mesh' / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    teile = bruecke(fehler)
    for t in teile:
        for p in t['prims']: p['flaeche'] = np.full(len(p['pos']), 5.0)
    schreibe_glb(ziel / 'mesh' / 'modelle' / 'bruecke_E2.glb', teile)
    schreibe_glb(ziel / 'mesh' / 'modelle' / 'wasser_W01.glb', [{'name': 'wasser_W01', 'prims': [spiegel_modell(fehler)]}])
    # ---- Vektoren: wege.geojson / kreuzungen.geojson im echten Schema (#56): rolle mittellinie|rand_links|rand_rechts|band|netz
    from shapely.geometry import Polygon, mapping
    from shapely import union_all
    wf, baender = [], []
    kx0, kz0, kx1, kz1 = KREUZ
    for wid, pl, b in WEGE:
        mitte = np.array(pl)
        if fehler == 'Q14' and wid == 'W4': mitte = mitte + [0, 0.5]
        if fehler == 'Q10_kurve' and wid == 'W4':   # enge S-Kurve (r ~ 4 m) x 152-156 nur in der Mittellinie
            xs = np.round(np.arange(130, 186.001, 0.25), 3); mitte = np.c_[xs, 100 + np.where((xs > 152) & (xs < 156), 0.2 * np.sin(np.pi * (xs - 152) / 4) ** 2, 0)]
        basis = dict(id=wid, teil=0, klasse='GASSE', breite=b)
        wf.append(feat({'type': 'LineString', 'coordinates': mitte.tolist()}, rolle='mittellinie', **basis))
        (ax, az), (bx, bz) = pl
        rr = {}
        for sg in (-1, 1):
            if az == bz:
                xs = np.round(np.arange(ax, bx + 1e-9, F), 6); r = np.c_[xs, np.full_like(xs, az + sg * b / 2)]
            else:
                zs = np.round(np.arange(az, bz + 1e-9, F), 6); r = np.c_[np.full_like(zs, ax + sg * b / 2), zs]
            if fehler == 'Q3' and wid == 'W1' and sg == 1:
                m = (r[:, 0] >= 150) & (r[:, 0] <= 153); r[m, 1] += np.where(np.arange(m.sum()) % 2, 0.05, -0.05)
            rolle = 'rand_links' if sg < 0 else 'rand_rechts'; rr[rolle] = r
            wf.append(feat({'type': 'LineString', 'coordinates': r.tolist()}, rolle=rolle, **basis))
        band = Polygon(np.vstack([rr['rand_links'], rr['rand_rechts'][::-1]])); baender.append(band)
        wf.append(feat(mapping(band), rolle='band', **basis))
    kpoly = Polygon([(kx0, kz0), (kx1, kz0), (kx1, kz1), (kx0, kz1)])
    netz = union_all(baender + [kpoly])
    netz_g = mapping(netz) if netz.geom_type == 'MultiPolygon' else {'type': 'MultiPolygon', 'coordinates': [mapping(netz)['coordinates']]}
    wf.append(feat(json.loads(json.dumps(netz_g)), rolle='netz', teile=len(getattr(netz, 'geoms', [netz]))))
    (ziel / 'vektor' / 'wege.geojson').write_text(json.dumps(fc(wf)))
    (ziel / 'vektor' / 'kreuzungen.geojson').write_text(json.dumps(fc([feat({'type': 'Polygon', 'coordinates': [[[kx0, kz0], [kx1, kz0], [kx1, kz1], [kx0, kz1], [kx0, kz0]]]},
        id='K001', art='weg_kreuzung', weg_ids=['W2', 'W3'], platz_ids=[], flaeche=round(kpoly.area, 3))])))
    sp = SPIEGEL
    wpoly = [[XC - HW, Z0], [XC + HW, Z0], [XC + HW, Z1], [XC - HW, Z1], [XC - HW, Z0]]
    (ziel / 'vektor' / 'wasser.geojson').write_text(json.dumps(fc([feat({'type': 'Polygon', 'coordinates': [wpoly]}, id='W01', typ='wasser', spiegel_m_median=sp, flaeche_m2=2 * HW * (Z1 - Z0))])))
    zs = np.round(np.arange(Z0, Z1 + 1e-9, F), 6)
    (ziel / 'vektor' / 'ufer.geojson').write_text(json.dumps(fc([feat({'type': 'LineString', 'coordinates': np.c_[np.full_like(zs, XC + s_ * HW), zs].tolist()},
        id=f'W01_U{i}', typ='uferlinie', gewaesser='W01', seite='aussen', geschlossen=False, spiegel_m=[round(sp, 4)] * len(zs)) for i, s_ in enumerate((-1, 1))])))
    ang = np.linspace(0, 2 * np.pi, 151)
    r = BAU_R * (1.02 if fehler == 'Q14' else 1.0)
    if fehler == 'Q14_ohne_zonen': r = None
    ring = np.c_[BAU_C[0] + (r or 1) * np.cos(ang), BAU_C[1] + (r or 1) * np.sin(ang)]; ring[-1] = ring[0]
    if r is not None:
        (ziel / 'vektor' / 'zonen.geojson').write_text(json.dumps(fc([feat({'type': 'Polygon', 'coordinates': [ring.tolist()]}, id='bauzone_plan_00001', klasse=0, layer='bauzone_plan', typ='bauzone', untergrund='SCHNEE')])))
    for n in ('kanten.geojson', 'grat.geojson'): (ziel / 'vektor' / n).write_text(json.dumps(fc([])))
    # ---- Datenschicht: echte Module aus art/dorfmap-fertig + Dummy-Masken (0,1 m/px, 3360 x 3030)
    dsrc = Path(__file__).resolve().parents[2] / 'daten'
    for f in ('query.mjs', 'manifest.mjs', 'glb.mjs', 'png.mjs', 'legende.json'):
        shutil.copy(dsrc / f, ziel / 'daten' / f)
    ix = np.arange(int(X0 * 10), int(X1 * 10)); iz = np.arange(int(Z0 * 10), int(Z1 * 10))
    GX, GZ = np.meshgrid((ix + 0.5) / 10, (iz + 0.5) / 10)
    kk = klasse(GX, GZ)
    if fehler == 'Q11': kk[500:600, 500:600] = 3
    fl = np.zeros((3030, 3360), np.uint8); fl[iz[0]:iz[-1] + 1, ix[0]:ix[-1] + 1] = kk
    schreibe_png8(ziel / 'daten' / 'flaeche.png', fl)
    schreibe_png8(ziel / 'daten' / 'begehbar.png', (fl != 4) & (fl != 3))
    (ziel / 'daten' / 'test' / 'query.test.mjs').write_text(TEST_MJS)
    # ---- Referenz (Dummy-"alt"): D2-Vertices 0,5 m, alte Wege, Bauzone
    gx, gz = np.meshgrid(np.arange(126, 168.001, 0.5), np.arange(43, 86.001, 0.5))
    hd = hoehe(gx.ravel(), gz.ravel(), None, d2_toleranz=False)
    np.savez_compressed(ziel / 'referenz' / 'd2_alt.npz', xyz=np.c_[gx.ravel(), hd, gz.ravel()].astype(np.float32))
    ref = {'quelle': 'Dummy (baue_dummy.py)', 'wege': [{'id': w, 'teil': 0, 'pl': [list(p) for p in pl]} for w, pl, _ in WEGE],
           'bauzone_m2': float(0.5 * BAU_R ** 2 * 150 * np.sin(2 * np.pi / 150)), 'wasser_alternativen_m2': {'dummy': 2 * HW * (Z1 - Z0)}}
    (ziel / 'referenz' / 'referenz_alt.json').write_text(json.dumps(ref))
    # ---- Abnahme (Q13)
    from PIL import Image
    k = json.loads((Path(__file__).resolve().parents[1] / 'konfig.json').read_text())
    namen = []
    for ort in k['orte']:
        for h in k['q13_hoehen']: namen.append(f"{ort}_clay_{('%g' % h).replace('.', ',')}m.jpg")
        namen.append(f'{ort}_wire_5m.jpg')
    rng = np.random.default_rng(1)
    for i, n in enumerate(namen):
        if fehler == 'Q13' and i in (3, 7): continue
        Image.fromarray((rng.random((48, 64, 3)) * 255).astype(np.uint8)).save(ziel / 'abnahme' / n, quality=90)
    (ziel / 'abnahme' / 'QUELLEN.txt').write_text('Dummy-Abnahmebilder (Rauschen) fuer den QA-Selbsttest\n' + '\n'.join(namen) + '\n')
    kd = dict(k); kd['bruecken'] = {'E2': k['bruecken']['E2']}
    kd['schwellen'] = dict(k['schwellen'])   # Q14-Referenz kommt zur Laufzeit aus vektor/wasser.geojson des Dummys
    (ziel / 'konfig_dummy.json').write_text(json.dumps(kd, indent=1))
    return {'vertices_welt': int(len(V)), 'duplikate': int(dup), 'dreiecke': ges}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--ziel', default='/tmp/dv2_qa/dummy/sauber'); ap.add_argument('--fehler')
    a = ap.parse_args(); print(json.dumps(baue(a.ziel, a.fehler)))
