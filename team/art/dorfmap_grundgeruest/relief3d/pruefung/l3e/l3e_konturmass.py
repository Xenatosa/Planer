# L3e Messwert: sichtbare Uferlinie (Hoehenlinie Gelaende = Viewer-Spiegel WR/WE wie viewer_alle.js P12b) je Stelle,
# Anzahl Linienstuecke (zerrissene Linie = Zaehnchen/Inseln) und Abweichung von ihrer eigenen geglaetteten Linie (Gauss, 1 m) = Zacken-/Treppenmass. Aufruf: python3 l3e_konturmass.py <vorher.gz> <nachher.gz>
import sys, json, numpy as np, scipy.ndimage as nd
sys.path.insert(0, __import__('os').path.dirname(__file__)); import l3e_kontur as K
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
BOX = {'F7_nord': (231, 249, 266, 273), 'G7_nord': (246, 276, 250, 268), 'G7_plaettchen': (277, 291, 265, 273)}
def mass(F, b):
    x0, x1, z0, z1 = b; rs = F['rs']; sl = (slice(int(z0*rs), int(z1*rs)+1), slice(int(x0*rs), int(x1*rs)+1))
    X, Z = np.meshgrid(np.arange(sl[1].start, sl[1].stop)/rs, np.arange(sl[0].start, sl[0].stop)/rs)
    D = np.where(F['ring3'][sl], np.nan, (F['GB'] - F['WE'])[sl])
    cs = plt.contour(X, Z, D, [0]); plt.close()
    r = []
    for seg in cs.allsegs[0]:
        if len(seg) < 12: continue
        L = np.r_[0, np.cumsum(np.hypot(*np.diff(seg, axis=0).T))]; t = np.arange(0, L[-1], 0.05)
        P = np.c_[np.interp(t, L, seg[:, 0]), np.interp(t, L, seg[:, 1])]
        S = nd.gaussian_filter1d(P, 20, axis=0, mode='nearest')
        r.append(np.hypot(*(P - S).T)[20:-20])
    n = len(cs.allsegs[0]); kurz = sum(len(q) < 12 for q in cs.allsegs[0])
    r = np.concatenate(r) if r else np.zeros(1)
    return {'linienstuecke': n, 'davon_kurz_unter_12_punkte': int(kurz), 'max_m_zellen': round(float(r.max()), 3), 'p95_zellen': round(float(np.percentile(r, 95)), 3), 'mittel_zellen': round(float(r.mean()), 3)}
A, B = K.feld(sys.argv[1]), K.feld(sys.argv[2])
print(json.dumps({k: {'vorher': mass(A, b), 'nachher': mass(B, b)} for k, b in BOX.items()}, indent=1))
