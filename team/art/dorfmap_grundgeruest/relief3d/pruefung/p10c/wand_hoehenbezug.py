#!/usr/bin/env python3
"""P10c-Befund: Hoehenbezug der Wandprofile (vektor.json hoehe_oben_m/hoehe_unten_m) gegen das
sichtbare Gelaende GB aus relief_daten.json.gz, an der (korrigierten) Mittellinie in Zellen.
Nur Analyse. Aufruf (relief3d/): python3 pruefung/p10c/wand_hoehenbezug.py
"""
import base64, gzip, json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from neu import wand as W  # noqa: E402
d = json.loads(gzip.decompress((ROOT / 'relief_daten.json.gz').read_bytes()))
rs = int(d['rs'])
GB = np.frombuffer(base64.b64decode(d['GB']), '<f4').reshape(d['ny'] * rs + 1, d['nx'] * rs + 1)
v = json.loads((ROOT / 'neu' / 'vektor.json').read_text(encoding='utf-8'))
fam = {}
for w in v['waende']:
    P = W._centerline_cells(w)
    i = np.clip(np.rint(P[:, 0] * rs).astype(int), 0, GB.shape[1] - 1)
    j = np.clip(np.rint(P[:, 1] * rs).astype(int), 0, GB.shape[0] - 1)
    # hoechstes/tiefstes sichtbares Gelaende im 11x11-Zellfenster (wie vektor.py fuer 'top')
    g_max = np.array([GB[max(0, b - 5 * rs):b + 5 * rs + 1, max(0, a - 5 * rs):a + 5 * rs + 1].max() for a, b in zip(i, j)])
    g_min = np.array([GB[max(0, b - 5 * rs):b + 5 * rs + 1, max(0, a - 5 * rs):a + 5 * rs + 1].min() for a, b in zip(i, j)])
    top = np.asarray(w['hoehe_oben_m'], float)
    f = fam.setdefault(w['name'], {'waende': 0, 'oben_minus_GBmax': [], 'oben_minus_GBmin': [], 'oben': []})
    f['waende'] += 1
    f['oben_minus_GBmax'] += (top - g_max).tolist(); f['oben_minus_GBmin'] += (top - g_min).tolist(); f['oben'] += top.tolist()
out = {}
for n, f in fam.items():
    a, b, c = (np.array(f[k]) for k in ('oben_minus_GBmax', 'oben_minus_GBmin', 'oben'))
    out[n] = {'waende': f['waende'], 'punkte': len(a), 'hoehe_oben_median': round(float(np.median(c)), 2),
              'oben_minus_GB_max_fenster_median': round(float(np.median(a)), 2),
              'oben_minus_GB_min_fenster_median': round(float(np.median(b)), 2),
              'anteil_oben_unter_GB_krone': round(float((a < -0.5).mean()), 3),
              'anteil_oben_ueber_GB_fuss_8m': round(float((b > 8).mean()), 3)}
print(json.dumps({'GB_max': float(GB.max()), 'GB_min': float(GB.min()), 'familien': out}, indent=1))
