#!/usr/bin/env python3
"""pruefe_regeln.py (t1744u, Raster-Methode) – Geruest + Kandidaten-Regelbibliothek [A].

Zweck: Basis, um aus Fabians "falsch"-Feldern die zutreffenden Regeln auszuwaehlen bzw. neue abzuleiten.
KEIN Ersatz fuer Fabians Urteil. Alle Regeln sind Annahmen [A], aus frueheren Beanstandungen abgeleitet;
Schwellwerte sind ungeeicht und stehen unten als Parameter.

Quellen (nur gelesen, nichts wird veraendert):
  relief3d/zellen_relief.csv   Zellwerte (1 Zelle = 1 m = 25 px, 336x303)
  relief3d/relief_daten.json.gz  GB (Anzeige-Hoehengitter 0,5 m), WV (Wasserspiegel), FW (Feinband 0,25 m),
                                 Objekte (baeume, felsen, findlinge, steine, geroell, haeuser, bruecken, wege, rampenwege)
  Hinweis: objekte_neu.js (Browser) erzeugt Haus-/Baum-Geometrie aus genau diesen Listen; die Browser-Nachkorrektur
  im Feinband (t59u) wird hier NICHT nachgebildet -> Objekt-Hoehen-Regeln koennen dort abweichen.

Aufruf: python3 pruefe_regeln.py [--regeln R01,R04] [--out DIR]
Ausgabe: treffer.csv, treffer.json, zusammenfassung.json/.md (Treffer je Regel und Feld).
"""
import argparse, base64, csv, gzip, json, os, sys
from collections import Counter, defaultdict
import numpy as np, scipy.ndimage as nd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raster_def import R3D, NX, NY, feld_von

# ======================= Parameter (Schwellwerte, alle [A]) =======================
P = dict(
    R01_weg_min_komponente=6,        # Wegstueck mit weniger Zellen = ausgefranst/Splitter
    R01_ziel_radius_m=3.0,           # Wegende gilt als angebunden, wenn Haus/Bruecke/Rampe/Rand so nah
    R01_rampe_ende_max_m=3.0,        # Rampenende ohne Weg/begehbare Zelle in diesem Abstand = endet ohne Ziel
    R02_baum_rampe_abstand_m=1.5,    # Baum naeher an Rampen-Mittellinie
    R03_fluss_min_luecke=1,          # mehr als 1 Komponente je fluss_id = Luecke
    R03_rand_abstand_m=2,            # Fluss gilt als bis zum Rand gefuehrt
    R04_fenster_m=2.5,               # Median-Fenster (Gitter 0,5 m)
    R04_spitze_m=2.0,                # Vertex ueber Umgebungs-Median
    R04_loch_m=2.0,                  # Vertex unter Umgebungs-Median (ohne Wasser)
    R05_neigung_grad=50.0,           # steil
    R05_rauheit_max_m=0.08,          # Std der Abweichung von Ebene (3x3) darunter = glatt
    R05_min_flaeche_m2=12.0,         # zusammenhaengende glatte Steilflaeche
    R06_schwebt_m=0.35, R06_versunken_m=0.6,
    R07_insel_min_zellen=4,          # begehbare Komponente (nicht die groesste) ab dieser Groesse melden
    R08_bergauf_m=0.15,              # Wasserspiegel steigt in Fliessrichtung
    R09_stufe_m=0.4,                 # Feinband-Randvertex weicht so stark vom Grobgitter ab
    R09_sprung_m=1.5,                # Sprung zwischen Nachbarvertices (GB) ausserhalb Klippe
    R10_faktor=0.6,                  # Ueberlappung: Abstand < Faktor*(r1+r2)
    R11_anteil=0.10,                 # Anteil Klippe/Wasser unter Grundriss
)
REGELN = {
 'R01': 'Weg/Rampe ausgefranst oder endet ohne Ziel', 'R02': 'Baum auf Klippen-Abstiegsweg (Rampe)',
 'R03': 'Fluss endet vor Kartenrand / hat Luecke', 'R04': 'Spitze oder sehr tiefes Loch im Gelaende',
 'R05': 'Senkrechte glatte Wand ohne Kontur', 'R06': 'Objekt schwebend / versunken / im Wasser / auf Weg',
 'R07': 'Begehbare Insel ohne Anbindung', 'R08': 'Wasser fliesst bergauf', 'R09': 'Stufe am Bandrand / Sprung ausserhalb Klippe',
 'R10': 'Objektueberlappung', 'R11': 'Gebaeude/Bauplatz auf Klippe oder Wasser'}

# ======================= Daten laden =======================
def lade():
    Z = defaultdict(lambda: np.empty((NY, NX), object))
    with open(os.path.join(R3D, 'zellen_relief.csv')) as f:
        for z in csv.DictReader(f):
            y, x = int(z['cy']), int(z['cx'])
            for k, v in z.items(): Z[k][y, x] = v
    D = json.load(gzip.open(os.path.join(R3D, 'relief_daten.json.gz')))
    rs = D['rs']; gy, gx = NY*rs+1, NX*rs+1
    f32 = lambda s: np.frombuffer(base64.b64decode(s), np.float32).astype(float)
    D['_GB'] = f32(D['GB']).reshape(gy, gx); D['_WV'] = f32(D['WV']).reshape(gy, gx)
    return Z, D
def num(a, d=0.0):
    o = np.full(a.shape, d); m = a != ''
    o[m] = a[m].astype(float); return o
def gb_at(D, x, z):
    G = D['_GB']; rs = D['rs']; fx, fz = np.clip(x*rs, 0, G.shape[1]-1.001), np.clip(z*rs, 0, G.shape[0]-1.001)
    i, j = int(fx), int(fz); u, v = fx-i, fz-j
    return (G[j,i]*(1-u)*(1-v)+G[j,i+1]*u*(1-v)+G[j+1,i]*(1-u)*v+G[j+1,i+1]*u*v)

T = []
def treffer(regel, x, z, wert, info=''):
    cx, cy = int(np.clip(x, 0, NX-1)), int(np.clip(z, 0, NY-1))
    T.append(dict(regel=regel, feld=feld_von(cx, cy), cx=cx, cy=cy, x_m=round(float(x), 2), z_m=round(float(z), 2), messwert=round(float(wert), 3), info=info))

# ======================= Regeln =======================
def R01(Z, D):
    W = np.zeros((NY, NX), bool)
    for x, y in D['wege']: W[y, x] = True
    lab, n = nd.label(W, np.ones((3, 3)))
    gr = nd.sum(W, lab, range(1, n+1))
    for k, s in enumerate(gr, 1):
        if s < P['R01_weg_min_komponente']:
            ys, xs = np.nonzero(lab == k); treffer('R01', xs.mean()+.5, ys.mean()+.5, s, 'Wegsplitter (Zellen)')
    nb = nd.convolve(W.astype(int), np.ones((3, 3)), mode='constant') - W
    ziel = np.zeros((NY, NX), bool)
    for h in D['haeuser']:
        x0, x1 = int(h['x']-h['b']/2), int(h['x']+h['b']/2); z0, z1 = int(h['z']-h['t']/2), int(h['z']+h['t']/2)
        ziel[max(z0,0):z1+1, max(x0,0):x1+1] = True
    for b in D['bruecken']: ziel[int(np.clip(b[2],0,NY-1)), int(np.clip(b[0],0,NX-1))] = True
    for rw in D['rampenwege']:
        for x, z in rw: ziel[int(np.clip(z,0,NY-1)), int(np.clip(x,0,NX-1))] = True
    ziel[:2, :] = ziel[-2:, :] = True; ziel[:, :2] = ziel[:, -2:] = True
    dz = nd.distance_transform_edt(~ziel)
    for y, x in zip(*np.nonzero(W & (nb == 1))):
        if dz[y, x] > P['R01_ziel_radius_m']: treffer('R01', x+.5, y+.5, dz[y, x], 'Wegende ohne Ziel (Abstand m)')
    dw = nd.distance_transform_edt(~(W | (Z['begehbar_3d'] == '1')))
    for i, rw in enumerate(D['rampenwege']):
        for x, z in (rw[0], rw[-1]):
            d = dw[int(np.clip(z,0,NY-1)), int(np.clip(x,0,NX-1))]
            if d > P['R01_rampe_ende_max_m']: treffer('R01', x, z, d, f'Rampe {i} Ende fern von Weg/begehbar (m)')
def R02(Z, D):
    pts = np.array([p for rw in D['rampenwege'] for p in rw], float)
    if not len(pts): return
    from scipy.spatial import cKDTree
    t = cKDTree(pts)
    for b in D['baeume']:
        d, _ = t.query([b[0], b[2]])
        if d < P['R02_baum_rampe_abstand_m']: treffer('R02', b[0], b[2], d, 'Baum-Abstand zur Rampe (m)')
def R03(Z, D):
    fid = Z['fluss_id']
    for f in sorted(set(fid.ravel()) - {''}):
        m = fid == f; lab, n = nd.label(m)
        if n > P['R03_fluss_min_luecke']:
            gr = nd.sum(m, lab, range(1, n+1))
            for k in np.argsort(gr)[:-1]:
                ys, xs = np.nonzero(lab == k+1); treffer('R03', xs.mean()+.5, ys.mean()+.5, gr[k], f'{f}: abgetrenntes Stueck (Zellen)')
        if f.startswith('BACH'):
            ys, xs = np.nonzero(m); r = P['R03_rand_abstand_m']
            if not ((ys <= r).any() or (ys >= NY-1-r).any() or (xs <= r).any() or (xs >= NX-1-r).any()):
                treffer('R03', xs.mean(), ys.mean(), 0, f'{f}: erreicht keinen Kartenrand')
            # Ende: Zellen mit genau 1 Fluss-Nachbarn in 8er-Nachbarschaft, nicht am Rand
            nb = nd.convolve(m.astype(int), np.ones((3, 3)), mode='constant') - m
            ws = (Z['wasser_anzeige'] == '1')
            for y, x in zip(*np.nonzero(m & (nb <= 2))):
                if r < y < NY-1-r and r < x < NX-1-r and ws[max(y-2,0):y+3, max(x-2,0):x+3].sum() <= nb[y, x]+1:
                    treffer('R03', x+.5, y+.5, nb[y, x], f'{f}: offenes Ende im Feld')
def R04(Z, D):
    G = D['_GB']; rs = D['rs']; w = int(P['R04_fenster_m']*rs)*2+1
    med = nd.median_filter(G, size=w); d = G - med
    nass = D['_WV'] > G - 0.01
    for art, m, thr in (('Spitze', d > P['R04_spitze_m'], 1), ('Loch', (d < -P['R04_loch_m']) & ~nass, -1)):
        lab, n = nd.label(m)
        for sl in nd.find_objects(lab):
            sub = d[sl]; j, i = np.unravel_index(np.argmax(sub*thr), sub.shape)
            treffer('R04', (sl[1].start+i)/rs, (sl[0].start+j)/rs, sub[j, i], f'{art} (m gegen Median {P["R04_fenster_m"]} m)')
def R05(Z, D):
    G = D['_GB']; rs = D['rs']; gz, gx = np.gradient(G, 1/rs)
    nei = np.degrees(np.arctan(np.hypot(gx, gz)))
    plan = nd.uniform_filter(G, 3); rau = np.sqrt(np.maximum(nd.uniform_filter((G-plan)**2, 3), 0))
    # Abweichung von lokaler Ebene: Ebene = Mittel (linearer Anteil hebt sich im 3x3-Mittel auf)
    m = (nei > P['R05_neigung_grad']) & (rau < P['R05_rauheit_max_m'])
    lab, n = nd.label(m); a = 1/rs**2
    for k, sl in enumerate(nd.find_objects(lab), 1):
        s = (lab[sl] == k).sum()*a
        if s >= P['R05_min_flaeche_m2']:
            ys, xs = np.nonzero(lab[sl] == k); treffer('R05', (sl[1].start+xs.mean())/rs, (sl[0].start+ys.mean())/rs, s, 'glatte Steilflaeche (m2)')
def R06(Z, D):
    W = np.zeros((NY, NX), bool)
    for x, y in D['wege']: W[y, x] = True
    nass = Z['wasser_anzeige'] == '1'
    for liste in ('baeume', 'felsen', 'findlinge', 'steine'):
        for o in D[liste]:
            x, y, z = o[0], o[1], o[2]; g = gb_at(D, x, z); cx, cy = int(min(x, NX-1)), int(min(z, NY-1))
            if y - g > P['R06_schwebt_m']: treffer('R06', x, z, y-g, f'{liste}: schwebt (m)')
            elif g - y > P['R06_versunken_m'] + (0.3*o[3] if liste != 'baeume' else 0): treffer('R06', x, z, g-y, f'{liste}: versunken (m)')
            if nass[cy, cx]: treffer('R06', x, z, 1, f'{liste}: im Wasser')
            if W[cy, cx] and liste in ('baeume', 'felsen', 'findlinge'): treffer('R06', x, z, 1, f'{liste}: auf Weg')
def R07(Z, D):
    B = Z['begehbar_3d'] == '1'; lab, n = nd.label(B)
    if n < 2: return
    gr = nd.sum(B, lab, range(1, n+1)); haupt = np.argmax(gr)+1
    for k, sl in enumerate(nd.find_objects(lab), 1):
        if k != haupt and gr[k-1] >= P['R07_insel_min_zellen']:
            ys, xs = np.nonzero(lab[sl] == k); treffer('R07', sl[1].start+xs.mean()+.5, sl[0].start+ys.mean()+.5, gr[k-1], 'begehbare Insel (Zellen)')
def R08(Z, D):
    ws = num(Z['wasserspiegel_anzeige_m'], np.nan); fr = Z['fliess_richtung']
    V = {'N': (0,-1), 'S': (0,1), 'O': (1,0), 'W': (-1,0), 'SO': (1,1), 'SW': (-1,1), 'NO': (1,-1), 'NW': (-1,-1)}
    for y, x in zip(*np.nonzero(fr != '')):
        dx, dy = V.get(fr[y, x], (0, 0)); X, Y = x+dx, y+dy
        if 0 <= X < NX and 0 <= Y < NY and not np.isnan(ws[y, x]) and not np.isnan(ws[Y, X]) and ws[Y, X]-ws[y, x] > P['R08_bergauf_m']:
            treffer('R08', x+.5, y+.5, ws[Y, X]-ws[y, x], f'Spiegel steigt Richtung {fr[y,x]} (m)')
def R09(Z, D):
    F = D['FW']; fs = F['fs']; FXn, FYn = NX*fs+1, NY*fs+1
    band = np.zeros(NX*NY, bool); band[np.frombuffer(base64.b64decode(F['band']), np.uint32)] = True; band = band.reshape(NY, NX)
    vid = np.frombuffer(base64.b64decode(F['vid']), np.uint32); h = np.frombuffer(base64.b64decode(F['h']), np.float32)
    fy, fx = vid // FXn, vid % FXn; X, Zz = fx/fs, fy/fs
    G = D['_GB']; rs = D['rs']
    gi = np.array([gb_at(D, a, b) for a, b in zip(X, Zz)]) if len(vid) < 2_000_000 else None
    rand = band & ~nd.binary_erosion(band)
    cx, cy = np.minimum(X.astype(int), NX-1), np.minimum(Zz.astype(int), NY-1)
    m = rand[cy, cx] & (np.abs(h-gi) > P['R09_stufe_m'])
    seen = set()
    for k in np.nonzero(m)[0]:
        key = (cx[k], cy[k])
        if key in seen: continue
        seen.add(key); treffer('R09', X[k], Zz[k], h[k]-gi[k], 'Feinband-Rand weicht von Grobgitter ab (m)')
    kl = (Z['klippe'] != '') | (Z['wasser_anzeige'] == '1')
    klv = nd.binary_dilation(kl, iterations=1)
    for ax in (0, 1):
        dd = np.abs(np.diff(G, axis=ax)); jj, ii = np.nonzero(dd > P['R09_sprung_m'])
        for j, i in zip(jj, ii):
            x, z = i/rs, j/rs
            if not klv[min(int(z), NY-1), min(int(x), NX-1)]: treffer('R09', x, z, dd[j, i], 'Sprung GB ausserhalb Klippe (m)')
def R10(Z, D):
    from scipy.spatial import cKDTree
    O = [(o[0], o[2], (1.2 if l == 'baeume' else o[3]*0.6), l) for l in ('baeume', 'felsen', 'findlinge') for o in D[l]]
    pts = np.array([(a, b) for a, b, _, _ in O]); t = cKDTree(pts)
    for i, j in t.query_pairs(3.0):
        d = np.hypot(*(pts[i]-pts[j])); r = O[i][2]+O[j][2]
        if d < P['R10_faktor']*r: treffer('R10', *(pts[i]+pts[j])/2, d, f'{O[i][3]}/{O[j][3]} Abstand (m)')
    H = D['haeuser']
    def box(h): return h['x']-h['b']/2, h['x']+h['b']/2, h['z']-h['t']/2, h['z']+h['t']/2
    for a in range(len(H)):
        A = box(H[a])
        for b in range(a+1, len(H)):
            B = box(H[b]); ox = min(A[1], B[1])-max(A[0], B[0]); oz = min(A[3], B[3])-max(A[2], B[2])
            if ox > 0.2 and oz > 0.2: treffer('R10', (H[a]['x']+H[b]['x'])/2, (H[a]['z']+H[b]['z'])/2, ox*oz, f'Haus {H[a]["id"]}/{H[b]["id"]} Ueberlappung (m2)')
        for l in ('baeume', 'felsen', 'findlinge'):
            for o in D[l]:
                if A[0] < o[0] < A[1] and A[2] < o[2] < A[3]: treffer('R10', o[0], o[2], 1, f'{l} in Haus {H[a]["id"]}')
def R11(Z, D):
    schlecht = (Z['klippe'] == 'WAND') | (Z['wasser_anzeige'] == '1') | np.isin(Z['untergrund'], ['KLIPPE_WAND', 'WASSER_EIS'])
    for h in D['haeuser']:
        x0, x1 = int(max(h['x']-h['b']/2, 0)), int(min(h['x']+h['b']/2, NX-1)); z0, z1 = int(max(h['z']-h['t']/2, 0)), int(min(h['z']+h['t']/2, NY-1))
        a = schlecht[z0:z1+1, x0:x1+1].mean()
        if a > P['R11_anteil']: treffer('R11', h['x'], h['z'], a, f'Haus {h["id"]} {h["typ"]} Anteil Klippe/Wasser')
    # Bauplaetze: bauzone_plan/bebaubar auf Klippe/Wasser
    bp = (Z['bauzone_plan'] == '1') | (Z['bebaubar'] == '1')
    for y, x in zip(*np.nonzero(bp & schlecht)): treffer('R11', x+.5, y+.5, 1, 'bebaubar/Bauzone-Zelle auf Klippe/Wasser')

# ======================= Hauptprogramm =======================
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--regeln', default=','.join(REGELN)); ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regeln_lauf'))
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    Z, D = lade(); fehler = {}
    for r in a.regeln.split(','):
        try: globals()[r](Z, D)
        except Exception as e: fehler[r] = repr(e)
    cols = ['regel', 'feld', 'cx', 'cy', 'x_m', 'z_m', 'messwert', 'info']
    with open(os.path.join(a.out, 'treffer.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(T)
    json.dump(T, open(os.path.join(a.out, 'treffer.json'), 'w'), ensure_ascii=False)
    je = Counter(t['regel'] for t in T); jf = defaultdict(Counter)
    for t in T: jf[t['regel']][t['feld']] += 1
    S = dict(parameter=P, fehler=fehler, treffer_je_regel={r: je.get(r, 0) for r in a.regeln.split(',')},
             felder_je_regel={r: len(jf[r]) for r in a.regeln.split(',')}, unterart={r: Counter(t['info'].split(':')[-1].split(' (')[0].strip() if ':' in t['info'] else t['info'].split(' (')[0] for t in T if t['regel'] == r) for r in a.regeln.split(',')})
    json.dump(S, open(os.path.join(a.out, 'zusammenfassung.json'), 'w'), indent=1, ensure_ascii=False)
    L = ['| Regel [A] | Beschreibung | Treffer | Felder |', '|---|---|---|---|'] + [f'| {r} | {REGELN[r]} | {je.get(r,0)} | {len(jf[r])} |' for r in a.regeln.split(',')]
    open(os.path.join(a.out, 'zusammenfassung.md'), 'w').write('\n'.join(L)+'\n' + (f'\nFehler: {fehler}\n' if fehler else ''))
    print('\n'.join(L)); print('Fehler:', fehler or 'keine')
