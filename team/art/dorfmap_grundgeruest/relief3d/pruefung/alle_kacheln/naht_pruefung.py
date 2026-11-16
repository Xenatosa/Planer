#!/usr/bin/env python3
"""P10b / QA P4b Punkt 2: Kachelnaehte exakt pruefen (Vertex-Positionen bitweise, T-Junctions).

Vergleicht fuer jedes Nachbarpaar der 56 Kacheln die Oberflaechen-Vertices auf der gemeinsamen
Kante (x bzw. z exakt gleich der Kachelgrenze) aus alle_kacheln.json.gz: gleiche (x,z)-Menge
(sonst T-Junction/Versatz) und bitgleiches y.
Aufruf: python3 naht_pruefung.py /tmp/p10b/alle_kacheln.json.gz > naht_vertex.json
"""
import base64, gzip, json, sys
import numpy as np

d = json.loads(gzip.decompress(open(sys.argv[1], 'rb').read()))['alle_kacheln']['tiles']
V = {t: np.frombuffer(base64.b64decode(x['vertices_xyz_f32']), '<f4').reshape(-1, 3) for t, x in d.items()}
res = []
tot = dict(paare=0, vertices=0, y_abweichend=0, nur_einseitig=0, max_dy=0.0)
for t, x in d.items():
    x0, z0, x1, z1 = x['bounds']
    for nb, achse, w in ((chr(ord(t[0]) + 1) + t[1], 0, x1), (t[0] + str(int(t[1]) + 1), 2, z1)):
        if nb not in d:
            continue
        def kante(k):
            P = V[k]
            P = P[P[:, achse] == np.float32(w)]
            return {tuple(r[[0, 2]].view('<u4')): r[1] for r in P}
        a, b = kante(t), kante(nb)
        gem = set(a) & set(b)
        ein = len(set(a) ^ set(b))
        dy = [abs(float(a[q]) - float(b[q])) for q in gem]
        gleich = sum(1 for q in gem if np.float32(a[q]).view('<u4') == np.float32(b[q]).view('<u4'))
        res.append(dict(paar=f'{t}|{nb}', vertices_a=len(a), vertices_b=len(b), gemeinsam=len(gem),
                        nur_einseitig=ein, y_bitgleich=gleich, max_dy=max(dy) if dy else None))
        tot['paare'] += 1; tot['vertices'] += len(gem); tot['y_abweichend'] += len(gem) - gleich
        tot['nur_einseitig'] += ein; tot['max_dy'] = max(tot['max_dy'], max(dy) if dy else 0.0)
print(json.dumps(dict(summe=tot, paare=res), indent=1))
