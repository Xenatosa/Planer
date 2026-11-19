#!/usr/bin/env python3
"""Baut die Alt-Referenz fuer Q7/Q14 aus dem Repo-Ist (nur lesen):
- referenz/d2_alt.npz: alte D2-Vertices (x, h, z) aus dem alle_kacheln-Paket (Kachel D2, 0,5 m, 7395 Vertices).
- referenz/referenz_alt.json: alte Weg-Mittellinien (neu/vektor.json /1,2), Wasserflaeche (DS = WV - GB > 0, 0,5-m-Raster),
  Bauzone (zellen_relief.csv bauzone_plan, 1 m2/Zelle).
Aufruf: python3 baue_referenz.py [--paket /tmp/dv2_qa/alt]   (Paket ggf. vorher: python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/dv2_qa/alt --ohne-html)"""
import argparse, base64, csv, gzip, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np

QA = Path(__file__).resolve().parent
RELIEF = QA.parents[1]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--paket', default='/tmp/dv2_qa/alt'); a = ap.parse_args()
    pk = Path(a.paket) / 'alle_kacheln.json.gz'
    if not pk.exists():
        subprocess.run([sys.executable, str(RELIEF / 'pruefung/alle_kacheln/baue_alle_kacheln.py'), '--out', a.paket, '--ohne-html'], check=True, cwd=RELIEF)
    d = json.load(gzip.open(pk))
    t = d['alle_kacheln']['tiles']['D2']
    xyz = np.frombuffer(base64.b64decode(t['vertices_xyz_f32']), np.float32).reshape(-1, 3)
    assert len(xyz) == int(t['vertices']) == 7395, len(xyz)
    (QA / 'referenz').mkdir(exist_ok=True)
    np.savez_compressed(QA / 'referenz' / 'd2_alt.npz', xyz=xyz)
    nx, ny, rs = d['nx'], d['ny'], d['rs']
    W, H = nx * rs + 1, ny * rs + 1
    wv = np.frombuffer(base64.b64decode(d['WV']), np.float32).reshape(H, W)
    gb = np.frombuffer(base64.b64decode(d['GB']), np.float32).reshape(H, W) if isinstance(d['GB'], str) else np.array(d['GB'], np.float32).reshape(H, W)
    wv_punkte = int((wv > -900).sum()); ds_pos = int(((wv > -900) & (wv - gb > 0)).sum())
    v = json.loads((RELIEF / 'neu/vektor.json').read_text())
    wege = []
    for w in v['wege']:
        e = {'id': w['id'], 'pl': (np.array(w['mittellinie_m'], float) / 1.2).round(4).tolist(), 'breite_m': round(float(w['breite_m']) / 1.2, 4), 'klasse': w.get('klasse')}
        if 'teil' in w: e['teil'] = w['teil']
        wege.append(e)
    bz = 0; wasser_zellen = 0
    with open(RELIEF / 'zellen_relief.csv') as f:
        for r in csv.DictReader(f):
            bz += r['bauzone_plan'] not in ('', '0', 'False', 'false')
            wasser_zellen += r['untergrund'] == 'WASSER_EIS'
    ref = {'quelle': 'Repo-Ist d2d4824: alle_kacheln (D2), neu/vektor.json (/1,2), WV/GB, zellen_relief.csv',
           'quelle_sha256': {'alle_kacheln.json.gz': hashlib.sha256(pk.read_bytes()).hexdigest()[:16],
                             'vektor.json': hashlib.sha256((RELIEF / 'neu/vektor.json').read_bytes()).hexdigest()[:16]},
           'wege': wege,
           'wasser_m2': ds_pos * rs ** -2, 'wasser_alternativen_m2': {'WV_punkte_x0,25': wv_punkte * rs ** -2, 'zellen_WASSER_EIS': wasser_zellen,
                                                                      'vektor_wasser_polygone': round(sum(float(p['area_m2']) for p in v['wasser']) / 1.44, 2)},
           'bauzone_m2': float(bz), 'd2': {'vertices': int(len(xyz)), 'height_sha256': t['height_sha256'], 'bounds': t['bounds']}}
    (QA / 'referenz' / 'referenz_alt.json').write_text(json.dumps(ref, ensure_ascii=False))
    print(json.dumps({k: ref[k] for k in ('wasser_m2', 'wasser_alternativen_m2', 'bauzone_m2', 'd2')}, ensure_ascii=False), len(wege), 'Wege')


if __name__ == '__main__':
    main()
