#!/usr/bin/env python3
"""P10b / QA P4b Punkt 3: Herkunft der frei stehenden dunklen Wandobjekte (nur Analyse, nichts geaendert).

Quelle der Wandkoerper: neu/vektor.json ['waende'] (260 Profile) -> neu/wand.py
build_wall_manifest -> _chunks (Chaikin + Clipping je Kachel mit Rand breite*1,05) -> _network_solid.
Geprueft wird:
  * Einheit von mittellinie_m (Meter) gegenueber dem Zellraster, in dem _chunks clippt und der Viewer zeichnet,
  * Abstand jeder Wandlinie zu ihren eigenen quellzellen (wie gezeichnet / wenn Meter durch 1,2 geteilt),
  * abgeschnittene Enden an der Clip-Kante und kurze Stuecke je Kachel (index.html-Stand D1/G1 und alle 56).
Aufruf (im relief3d-Ordner): python3 pruefung/alle_kacheln/wand_herkunft.py > /tmp/p10b/wand_herkunft.json
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from neu import wand as W  # noqa: E402

NX, NY, CELL_M = 336, 303, 1.2
v = json.load(open(ROOT / 'neu' / 'vektor.json'))
walls = v['waende']
A = np.concatenate([np.asarray(w['mittellinie_m'], float) for w in walls])
einheit = {
    'mittellinie_m_max_x': round(float(A[:, 0].max()), 2), 'mittellinie_m_max_z': round(float(A[:, 1].max()), 2),
    'karte_zellen_nx_ny': [NX, NY], 'karte_meter': [NX * CELL_M, NY * CELL_M],
    'befund': 'mittellinie_m reicht bis ~403 x 311 = Kartengroesse in Metern (336x303 Zellen * 1,2 m); '
              '_chunks clippt sie aber gegen Zellgrenzen (TILE_BOUNDS) und der Viewer zeichnet sie als Zellkoordinaten.',
}
je_wand = []
for w in walls:
    # wie gezeichnet: neu/wand.py ab P10c rechnet ueber _centerline_cells (Meter / CELL_M), davor Meter als Zellen
    P = W._centerline_cells(w) if hasattr(W, '_centerline_cells') else np.asarray(w['mittellinie_m'], float)
    q = np.asarray(w['quellzellen'], int)
    C = np.stack([q % NX + 0.5, q // NX + 0.5], 1)
    from scipy.spatial import cKDTree
    T = cKDTree(C)
    je_wand.append({'wand': f"{w['name']}:{w['teil']}", 'punkte': len(P),
                    'abstand_quelle_gezeichnet_median': float(np.median(T.query(P)[0])),
                    'abstand_quelle_meter_durch_1_2_median': float(np.median(T.query(np.asarray(w['mittellinie_m'], float) / CELL_M)[0])),
                    'ausserhalb_karte_gezeichnet': bool((P[:, 0] > NX).all() or (P[:, 1] > NY).all())})
d_g = np.array([x['abstand_quelle_gezeichnet_median'] for x in je_wand])
d_s = np.array([x['abstand_quelle_meter_durch_1_2_median'] for x in je_wand])


def kacheln():
    B = {}
    for iz in range(7):
        for ix in range(8):
            B['ABCDEFGH'[ix] + str(iz + 1)] = (ix * 42, iz * 43, ix * 42 + 42, NY if iz == 6 else iz * 43 + 43)
    return B


def stuecke(tiles):
    out = {}
    for t, b in tiles.items():
        rows = []
        for w in walls:
            width = float(w['breite_min_m'])
            m = (width / CELL_M if hasattr(W, '_centerline_cells') else width) * 1.05
            for pts, top, bot in W._chunks(w, b, width, W.DEFAULT_VARIANT):
                L = float(np.sum(np.linalg.norm(np.diff(pts, axis=0), axis=1)))
                ends = 0
                for p in (pts[0], pts[-1]):
                    if min(p[0] - (b[0] + m), (b[2] - m) - p[0], p[1] - (b[1] + m), (b[3] - m) - p[1]) < 1e-6:
                        ends += 1
                rows.append({'wand': f"{w['name']}:{w['teil']}", 'laenge_zellen': round(L, 2), 'enden_an_clipkante': ends,
                             'start': [round(float(x), 1) for x in pts[0]], 'ende': [round(float(x), 1) for x in pts[-1]],
                             'oben_mittel': round(float(np.mean(top)), 2), 'unten_mittel': round(float(np.mean(bot)), 2)})
        if rows:
            out[t] = {'stuecke': len(rows), 'kurz_unter_5': sum(r['laenge_zellen'] < 5 for r in rows),
                      'enden_an_clipkante': sum(r['enden_an_clipkante'] for r in rows), 'liste': rows}
    return out


alle = kacheln()
# Klippenzellen je Kachel (WAND/KANTE aus raster_c20_z25_zellen.csv, Zuordnung wie pruefe_regeln.feld())
import csv
klippe = {t: 0 for t in alle}
with open(ROOT.parent / 'raster_c20_z25_zellen.csv', encoding='utf-8-sig', newline='') as fh:
    for row in csv.DictReader(fh):
        if row['klippe'] in ('WAND', 'KANTE'):
            klippe['ABCDEFGH'[min(int(row['cx']) // 42, 7)] + str(min(int(row['cy']) // 43, 6) + 1)] += 1
idx = stuecke({t: alle[t] for t in ('D1', 'G1')})
ges = stuecke(alle)
print(json.dumps({
    'wand_py_einheit': 'Zellen (P10c, _centerline_cells)' if hasattr(W, '_centerline_cells') else 'Meter als Zellen (vor P10c)',
    'einheit': einheit,
    'waende_gesamt': len(walls),
    'abstand_quelle_gezeichnet': {'median': round(float(np.median(d_g)), 2), 'max': round(float(d_g.max()), 2)},
    'abstand_quelle_meter_durch_1_2': {'median': round(float(np.median(d_s)), 2), 'max': round(float(d_s.max()), 2)},
    'waende_gezeichnet_ganz_ausserhalb_karte': sum(x['ausserhalb_karte_gezeichnet'] for x in je_wand),
    'index_html_D1_G1': idx,
    'alle_56_summe': {'kacheln_mit_wand': len(ges), 'stuecke': sum(x['stuecke'] for x in ges.values()),
                      'kurz_unter_5': sum(x['kurz_unter_5'] for x in ges.values()),
                      'enden_an_clipkante': sum(x['enden_an_clipkante'] for x in ges.values())},
    'alle_56_je_kachel': {t: {**{k: x[k] for k in ('stuecke', 'kurz_unter_5', 'enden_an_clipkante')}, 'klippenzellen': klippe[t]}
                          for t, x in ges.items()},
    'klippe_ohne_wand': {t: klippe[t] for t in alle if klippe[t] > 0 and t not in ges},
    'wand_ohne_klippe': {t: ges[t]['stuecke'] for t in ges if klippe[t] == 0},
    'hinweis_D2': 'D2-Stuecke werden von build_wall_manifest bewusst verworfen (D2 wandfrei)',
    'je_wand': je_wand,
}, indent=1))
