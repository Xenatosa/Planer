#!/usr/bin/env python3
"""Dummy-Datensatz im angenommenen detail_v2-Format (PLAN_QA_DV2.md Abschn. 2) fuer den QA-Selbsttest.
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
    return k


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


def schreibe_png16(pfad, arr):
    from PIL import Image
    Image.fromarray(arr.astype(np.uint16)).save(pfad)


def schreibe_png8(pfad, arr):
    from PIL import Image
    Image.fromarray(arr.astype(np.uint8)).save(pfad)


QUERY_MJS = r'''// Dummy-queryPoint (QA-Selbsttest P6) - liest die PNGs der Datenschicht (0,1 m/px).
import { readFileSync } from 'node:fs';
import { inflateSync } from 'node:zlib';
import { join } from 'node:path';
function png(p) {
  const b = readFileSync(p); let o = 8, w, h, bd, ct; const idat = [];
  while (o < b.length) { const n = b.readUInt32BE(o), t = b.toString('latin1', o + 4, o + 8), d = b.subarray(o + 8, o + 8 + n);
    if (t === 'IHDR') { w = d.readUInt32BE(0); h = d.readUInt32BE(4); bd = d[8]; ct = d[9]; } if (t === 'IDAT') idat.push(d); o += 12 + n; }
  if (ct !== 0) throw new Error('nur Graustufen');
  const bpp = bd / 8, st = w * bpp, raw = inflateSync(Buffer.concat(idat)), out = Buffer.alloc(st * h);
  for (let y = 0; y < h; y++) { const f = raw[y * (st + 1)], s = raw.subarray(y * (st + 1) + 1, (y + 1) * (st + 1)), r = out.subarray(y * st, (y + 1) * st), u = y ? out.subarray((y - 1) * st, y * st) : null;
    for (let i = 0; i < st; i++) { const a = i >= bpp ? r[i - bpp] : 0, c = u ? u[i] : 0, cc = u && i >= bpp ? u[i - bpp] : 0; let v = s[i];
      if (f === 1) v += a; else if (f === 2) v += c; else if (f === 3) v += (a + c) >> 1; else if (f === 4) { const p = a + c - cc, pa = Math.abs(p - a), pb = Math.abs(p - c), pc = Math.abs(p - cc); v += (pa <= pb && pa <= pc) ? a : (pb <= pc ? c : cc); }
      r[i] = v & 255; } }
  const px = bd === 16 ? (i) => out.readUInt16BE(2 * i) : (i) => out[i];
  return { w, h, at: (x, y) => px(y * w + x) };
}
let D = null, L = null;
export function lade(dir) {
  L = JSON.parse(readFileSync(join(dir, 'legende.json'), 'utf8'));
  D = { hoehe: png(join(dir, 'hoehe.png')), flaeche: png(join(dir, 'flaeche.png')), begehbar: png(join(dir, 'begehbar.png')), slot: png(join(dir, 'slot.png')) };
}
export function queryPoint(x, z) {
  const H = D.hoehe, fx = x * 10 - 0.5, fz = z * 10 - 0.5, ix = Math.max(0, Math.min(H.w - 2, Math.floor(fx))), iz = Math.max(0, Math.min(H.h - 2, Math.floor(fz)));
  const tx = fx - ix, tz = fz - iz, g = (a, b) => H.at(a, b) * L.hoehe.skala_m + L.hoehe.offset_m;
  const hoehe = (g(ix, iz) * (1 - tx) + g(ix + 1, iz) * tx) * (1 - tz) + (g(ix, iz + 1) * (1 - tx) + g(ix + 1, iz + 1) * tx) * tz;
  const px = Math.min(H.w - 1, Math.floor(x * 10)), pz = Math.min(H.h - 1, Math.floor(z * 10));
  const flaeche = D.flaeche.at(px, pz);
  return { hoehe, flaeche, untergrund: L.flaeche[flaeche], begehbar: D.begehbar.at(px, pz) === 1, slot: D.slot.at(px, pz),
           kachel: 'ABCDEFGH'[Math.floor(x / 42)] + (Math.floor(z / 43) + 1) };
}
'''
TEST_MJS = r'''import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { lade, queryPoint } from '../query.mjs';
lade(join(dirname(fileURLToPath(import.meta.url)), '..'));
test('Weg W4 ist Weg und eingesenkt', () => { const a = queryPoint(150, 100), b = queryPoint(150, 102.5);
  assert.equal(a.flaeche, 1); assert.ok(b.hoehe - a.hoehe > 0.03); assert.equal(a.kachel, 'D3'); });
test('Bach ist Wasser und nicht begehbar', () => { const q = queryPoint(191.5, 100); assert.equal(q.flaeche, 4); assert.equal(q.begehbar, false); });
'''


def fc(features):
    return {'type': 'FeatureCollection', 'features': features}


def feat(geom, **pr):
    return {'type': 'Feature', 'properties': pr, 'geometry': geom}


def baue(ziel, fehler=None):
    ziel = Path(ziel)
    if ziel.exists(): shutil.rmtree(ziel)
    for d in ('mesh', 'vektor', 'daten/test', 'modelle', 'referenz', 'abnahme'): (ziel / d).mkdir(parents=True, exist_ok=True)
    P, T = baue_netz()
    H = hoehe(P[:, 0], P[:, 1], fehler)
    if fehler == 'Q2':   # Constraint-Vertices auf Wegrand z=73.6, x 140-145 um 4 cm verschoben
        m = (np.abs(P[:, 1] - 73.6) < 1e-6) & (P[:, 0] > 140) & (P[:, 0] < 145); P = P.copy(); P[m, 1] += 0.04
    if fehler == 'Q7_lage':  # Lage: Weg W1 im D2-Bereich um 0,6 m nach Norden verschoben (Hoehen)
        H = hoehe(P[:, 0], np.where(P[:, 0] < 168, P[:, 1] - 0.6, P[:, 1]), None, d2_toleranz=False)
    V = np.c_[P[:, 0], H, P[:, 1]]
    cen = P[T].mean(1)
    kl = klasse(cen[:, 0], cen[:, 1])
    kid = np.array([kachel_id(x, z) for x, z in cen])
    if fehler == 'Q1':
        weg = np.hypot(cen[:, 0] - 205, cen[:, 1] - 110) < 0.5; T, kl, kid, cen = T[~weg], kl[~weg], kid[~weg], cen[~weg]
    if fehler == 'Q9':
        sel = np.nonzero(kid == 'D3')[0][:5]; T = T.copy(); T[sel] = T[sel][:, [0, 2, 1]]
    manifest = {'format': 'dv2-mesh-1', 'einheit': 'm', 'welt': [336, 303], 'klassen': KLASSEN, 'kacheln': []}
    kach = {'D2': (126, 43, 168, 86), 'E2': (168, 43, 210, 86), 'D3': (126, 86, 168, 129), 'E3': (168, 86, 210, 129)}
    ges = {}
    for k, bd in kach.items():
        sel = kid == k; Tk = T[sel]; used = np.unique(Tk); remap = -np.ones(len(V), int); remap[used] = np.arange(len(used))
        Vk = V[used].copy()
        if fehler == 'Q1' and k == 'E2':
            m = np.nonzero((np.abs(Vk[:, 0] - 168) < 1e-6) & (np.abs(Vk[:, 2] - 50.2) < 1e-6))[0]; assert len(m) == 1; Vk[m, 1] += 0.001
        uv0 = Vk[:, [0, 2]].copy(); uv1 = np.c_[Vk[:, 0] / 336, Vk[:, 2] / 303]
        if fehler == 'Q10' and k == 'E3': uv0[:, 0] *= -1; uv1[:, 0] += 0.001
        prims = []
        for c in np.unique(kl[sel]):
            prims.append({'pos': Vk, 'uv0': uv0, 'uv1': uv1, 'normal': np.tile([0, 1, 0], (len(Vk), 1)), 'idx': remap[Tk[kl[sel] == c]], 'extras': {'klasse': KLASSEN[c]}})
        meshes = [{'name': 'gelaende', 'prims': prims}]
        x0, z0, x1, z1 = bd
        if x1 > XC - HW - 1 and x0 < XC + HW + 1:
            wv = np.array([[XC - HW - 1, SPIEGEL, z0], [XC + HW + 1, SPIEGEL, z0], [XC + HW + 1, SPIEGEL, z1], [XC - HW - 1, SPIEGEL, z1]])
            meshes.append({'name': 'wasser', 'prims': [{'pos': wv, 'idx': np.array([[0, 2, 1], [0, 3, 2]]), 'uv0': wv[:, [0, 2]], 'uv1': np.c_[wv[:, 0] / 336, wv[:, 2] / 303]}]})
        schreibe_glb(ziel / 'mesh' / f'{k}.glb', meshes)
        ges[k] = int(len(Tk)) + (2 if len(meshes) > 1 else 0)
        manifest['kacheln'].append({'id': k, 'datei': f'{k}.glb', 'bounds': list(bd), 'dreiecke': ges[k]})
    (ziel / 'mesh' / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    schreibe_glb(ziel / 'modelle' / 'bruecke_E2.glb', bruecke(fehler))
    # ---- Vektoren
    wf = []
    for wid, pl, b in WEGE:
        mitte = np.array(pl)
        if fehler == 'Q14' and wid == 'W4': mitte = mitte + [0, 0.5]
        wf.append(feat({'type': 'LineString', 'coordinates': mitte.tolist()}, art='mitte', id=wid, breite_m=b))
        (ax, az), (bx, bz) = pl
        for sg in (-1, 1):
            if az == bz:
                xs = np.round(np.arange(ax, bx + 1e-9, F), 6); r = np.c_[xs, np.full_like(xs, az + sg * b / 2)]
            else:
                zs = np.round(np.arange(az, bz + 1e-9, F), 6); r = np.c_[np.full_like(zs, ax + sg * b / 2), zs]
            if fehler == 'Q3' and wid == 'W1' and sg == 1:
                m = (r[:, 0] >= 150) & (r[:, 0] <= 153); r[m, 1] += np.where(np.arange(m.sum()) % 2, 0.05, -0.05)
            wf.append(feat({'type': 'LineString', 'coordinates': r.tolist()}, art='rand', id=f'{wid}_{"lr"[sg > 0]}'))
    (ziel / 'vektor' / 'wege.geojson').write_text(json.dumps(fc(wf)))
    kx0, kz0, kx1, kz1 = KREUZ
    (ziel / 'vektor' / 'kreuzungen.geojson').write_text(json.dumps(fc([feat({'type': 'Polygon', 'coordinates': [[[kx0, kz0], [kx1, kz0], [kx1, kz1], [kx0, kz1], [kx0, kz0]]]}, id='K1')])))
    sp = SPIEGEL + (0.1 if fehler == 'Q8' else 0)
    wpoly = [[XC - HW, Z0], [XC + HW, Z0], [XC + HW, Z1], [XC - HW, Z1], [XC - HW, Z0]]
    if fehler == 'Q14_wasser': wpoly = [[XC - HW, Z0], [XC + HW + 0.3, Z0], [XC + HW + 0.3, Z1], [XC - HW, Z1], [XC - HW, Z0]]
    (ziel / 'vektor' / 'wasser.geojson').write_text(json.dumps(fc([feat({'type': 'Polygon', 'coordinates': [wpoly]}, id='BACH', spiegel_m=sp)])))
    zs = np.round(np.arange(Z0, Z1 + 1e-9, F), 6)
    (ziel / 'vektor' / 'ufer.geojson').write_text(json.dumps(fc([feat({'type': 'LineString', 'coordinates': np.c_[np.full_like(zs, XC + s * HW), zs].tolist()}, art='uferlinie', id=f'U{i}') for i, s in enumerate((-1, 1))])))
    ang = np.linspace(0, 2 * np.pi, 151)
    r = BAU_R * (1.02 if fehler == 'Q14' else 1.0)
    ring = np.c_[BAU_C[0] + r * np.cos(ang), BAU_C[1] + r * np.sin(ang)]; ring[-1] = ring[0]
    (ziel / 'vektor' / 'zonen.geojson').write_text(json.dumps(fc([feat({'type': 'Polygon', 'coordinates': [ring.tolist()]}, id='Z1', bauzone=True, constraint=False)])))
    for n in ('kanten.geojson', 'grat.geojson'): (ziel / 'vektor' / n).write_text(json.dumps(fc([])))
    # ---- Datenschicht 0,1 m/px, 3360 x 3030 (ausserhalb der Dummy-Kacheln 0)
    o = Ortung(V, T)
    ix = np.arange(int(X0 * 10), int(X1 * 10)); iz = np.arange(int(Z0 * 10), int(Z1 * 10))
    GX, GZ = np.meshgrid(np.clip((ix + 0.5) / 10, X0, X1), np.clip((iz + 0.5) / 10, Z0, Z1))
    ix = np.r_[ix[0] - 1, ix, ix[-1] + 1]; iz = np.r_[iz[0] - 1, iz, iz[-1] + 1]          # 1 px Rand fuer bilineare Abfrage
    GX = np.pad(GX, 1, mode='edge'); GZ = np.pad(GZ, 1, mode='edge')
    hh, _ = o.hoehe(GX.ravel(), GZ.ravel()); hh = hh.reshape(GX.shape)
    kk = klasse(GX, GZ)
    if fehler == 'Q11':
        hh[300:600, 100:400] += 0.05; kk[500:600, 500:600] = 3
    hoe = np.zeros((3030, 3360), np.uint16); hoe[iz[0]:iz[-1] + 1, ix[0]:ix[-1] + 1] = np.round((np.nan_to_num(hh) + 10) / 0.001)
    fl = np.zeros((3030, 3360), np.uint8); fl[iz[0]:iz[-1] + 1, ix[0]:ix[-1] + 1] = kk
    schreibe_png16(ziel / 'daten' / 'hoehe.png', hoe); schreibe_png8(ziel / 'daten' / 'flaeche.png', fl)
    schreibe_png8(ziel / 'daten' / 'begehbar.png', (fl != 4) & (fl != 3)); schreibe_png16(ziel / 'daten' / 'slot.png', np.zeros((3030, 3360)))
    (ziel / 'daten' / 'legende.json').write_text(json.dumps({'hoehe': {'skala_m': 0.001, 'offset_m': -10.0}, 'flaeche': {str(i): k for i, k in enumerate(KLASSEN)}}))
    (ziel / 'daten' / 'query.mjs').write_text(QUERY_MJS); (ziel / 'daten' / 'test' / 'query.test.mjs').write_text(TEST_MJS)
    # ---- Referenz (Dummy-"alt"): D2-Vertices 0,5 m, alte Wege, Wasser, Bauzone
    gx, gz = np.meshgrid(np.arange(126, 168.001, 0.5), np.arange(43, 86.001, 0.5))
    hd = hoehe(gx.ravel(), gz.ravel(), None, d2_toleranz=False)
    np.savez_compressed(ziel / 'referenz' / 'd2_alt.npz', xyz=np.c_[gx.ravel(), hd, gz.ravel()].astype(np.float32))
    ref = {'quelle': 'Dummy (baue_dummy.py)', 'wege': [{'id': w, 'pl': [list(p) for p in pl]} for w, pl, _ in WEGE],
           'wasser_m2': 2 * HW * (Z1 - Z0), 'bauzone_m2': float(0.5 * BAU_R ** 2 * 150 * np.sin(2 * np.pi / 150))}
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
    (ziel / 'konfig_dummy.json').write_text(json.dumps(kd, indent=1))
    return {'vertices': int(len(V)), 'dreiecke': ges}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--ziel', default='/tmp/dv2_qa/dummy/sauber'); ap.add_argument('--fehler')
    a = ap.parse_args(); print(json.dumps(baue(a.ziel, a.fehler)))
