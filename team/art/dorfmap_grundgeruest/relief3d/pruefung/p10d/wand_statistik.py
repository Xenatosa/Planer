#!/usr/bin/env python3
"""P10d: Wandstatistik je Kachel vorher/nachher aus zwei 56-Kachel-Paketen (baue_alle_kacheln.py).
Aufruf (relief3d/): python3 pruefung/p10d/wand_statistik.py <vorher/alle_kacheln.json.gz> <nachher/alle_kacheln.json.gz> > statistik.json
Je Kachel: Dreiecke, Vertices, Vertices > 0,1 m ueber Gelaende, max. Hoehe ueber Gelaende,
Vertices |Wand - Gelaende| < 0,02 m (Z-Fighting-Kandidaten, Flaechen fast deckungsgleich), nicht gerenderte Stuecke."""
import base64, gzip, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import w1_wand as W1  # noqa: E402


def lade(p):
    d = json.loads(gzip.decompress(Path(p).read_bytes()))['alle_kacheln']
    G, rs, nx, ny = W1.gelaende_raster()
    for t, x in d['tiles'].items():
        P = np.frombuffer(base64.b64decode(x['vertices_xyz_f32']), '<f4').reshape(-1, 3)
        G[np.rint(P[:, 2] * rs).astype(int), np.rint(P[:, 0] * rs).astype(int)] = P[:, 1]
    out = {}
    for t, w in d['waende']['tiles'].items():
        e = {'dreiecke': int(w.get('triangles', 0)), 'vertices': int(w.get('vertices', 0))}
        if w.get('vertices'):
            P = np.frombuffer(base64.b64decode(w['vertices_xyz_f32']), '<f4').reshape(-1, 3).astype(float)
            dz = P[:, 1] - W1.sample(G, rs, P[:, 0], P[:, 2])
            e.update(ueber_0_1m=int((dz > 0.1).sum()), max_ueber_m=round(float(dz.max()), 2),
                     nahe_gelaende_0_02m=int((np.abs(dz) < 0.02).sum()))
        out[t] = e
    ng = d['waende'].get('nicht_gerendert', {})
    return out, ng


a, _ = lade(sys.argv[1])
b, ng = lade(sys.argv[2])
summe = lambda o, k: sum(v.get(k, 0) for v in o.values())
gruende = {}
for t, L in ng.items():
    for e in L:
        g = e['grund'].split(' (')[0].split(':')[0]
        gruende[g] = gruende.get(g, 0) + 1
print(json.dumps({
    'summe': {k: [summe(a, k), summe(b, k)] for k in ('dreiecke', 'vertices', 'ueber_0_1m', 'nahe_gelaende_0_02m')},
    'kacheln_mit_wand': [sum(1 for v in a.values() if v['dreiecke']), sum(1 for v in b.values() if v['dreiecke'])],
    'max_ueber_gelaende_m': [max(v.get('max_ueber_m', -99) for v in a.values()), max(v.get('max_ueber_m', -99) for v in b.values())],
    'nicht_gerendert_eintraege': sum(len(L) for L in ng.values()), 'nicht_gerendert_gruende': gruende,
    'je_kachel': {t: {'vorher': a.get(t), 'nachher': b.get(t), 'nicht_gerendert': len(ng.get(t, []))} for t in sorted(set(a) | set(b))},
}, ensure_ascii=False, indent=1))
