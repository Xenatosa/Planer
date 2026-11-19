"""Wortgleich uebernommen aus origin/art/dv2-qa @ 33d0d86, detail_v2/qa/dv2qa/geom.py
(QA P6 Runde 3: q3 abtastunabhaengig). Nicht aendern; bei QA-Update neu kopieren."""
import numpy as np


def neu_abtasten(pl, schritt=0.05, geschlossen=False):
    """Linie gleichmaessig nach Bogenlaenge neu abtasten (lineare Interpolation entlang der Polylinie).
    Offen: Endpunkte bleiben, Schritt = L / round(L / schritt). Geschlossen: Ring ohne Doppelpunkt, gleicher Schritt rundum."""
    pl = np.asarray(pl, float)
    if geschlossen:
        if np.allclose(pl[0], pl[-1]): pl = pl[:-1]
        pl = np.vstack([pl, pl[:1]])
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(pl, axis=0).T))]
    if d[-1] <= 0: return pl[:1].copy()
    n = max(int(round(d[-1] / schritt)), 1)
    s = np.linspace(0, d[-1], n + 1)
    if geschlossen: s = s[:-1]
    return np.c_[np.interp(s, d, pl[:, 0]), np.interp(s, d, pl[:, 1])]


def _abstand_lokal(R, g, m, geschlossen):
    """Abstand jedes Punkts R[i] zur Polylinie g, nur Segmente g[i-m .. i+m] (gleichmaessige Abtastung -> exakt wie global,
    solange die Linie sich nicht innerhalb von 1 m selbst naehert)."""
    n = len(R); best = np.full(n, np.inf); i = np.arange(n)
    nseg = n if geschlossen else n - 1
    for o in range(-m, m + 1):
        j = i + o
        if geschlossen: j = j % n; ok = np.ones(n, bool)
        else: ok = (j >= 0) & (j < nseg); j = np.clip(j, 0, nseg - 1)
        a = g[j]; b = g[(j + 1) % n] if geschlossen else g[j + 1]
        ab = b - a; t = np.clip(((R - a) * ab).sum(1) / ((ab * ab).sum(1) + 1e-30), 0, 1)
        d = np.hypot(*(R - a - ab * t[:, None]).T)
        best = np.where(ok, np.minimum(best, d), best)
    return best


def form_abw(pl, fenster=1.0, geschlossen=False, schritt=0.05):
    """q3 abtastunabhaengig (Entscheidung Grundgeruest/QA 19.11. Runde 3): Linie zuerst gleichmaessig auf 'schritt' m neu
    abtasten, dann gleitendes Mittel ueber 'fenster' m Bogenlaenge (offen: an Enden symmetrisch verkuerzt, Endpunkte 0).
    Abweichung = Abstand Abtastpunkt -> gemittelte Linie. Knick = Winkel zwischen den Abtastsegmenten vor und nach dem
    Punkt mit einem Segment Luecke (Sehne 2 x schritt): ein Stuetzpunktknick zwischen zwei Abtastpunkten zaehlt voll.
    -> (R n x 2, abw n, knick n)."""
    from shapely import LineString, points, distance
    from scipy.ndimage import uniform_filter1d
    R = neu_abtasten(pl, schritt, geschlossen)
    n = len(R)
    if n < 5: return R, np.zeros(n), np.zeros(n)
    seg = np.hypot(*np.diff(np.vstack([R, R[:1]]) if geschlossen else R, axis=0).T)
    h = schritt if not len(seg) else float(np.median(seg))
    k = max(int(round(fenster / 2 / h)), 1)                     # halbes Fenster in Abtastpunkten
    if geschlossen:
        g = uniform_filter1d(R, size=2 * k + 1, axis=0, mode='wrap')
    else:
        c = np.vstack([np.zeros((1, 2)), np.cumsum(R, axis=0)])
        i = np.arange(n); hw = np.minimum(np.minimum(i, n - 1 - i), k)
        g = (c[i + hw + 1] - c[i - hw]) / (2 * hw + 1)[:, None]
    abw = _abstand_lokal(R, g, k + 2, geschlossen)              # Abstand zur gemittelten Linie (lokal, +-k+2 Segmente)
    if not geschlossen: abw[0] = abw[-1] = 0
    P = np.vstack([R[-2:], R, R[:2]]) if geschlossen else np.vstack([R[:1], R[:1], R, R[-1:], R[-1:]])
    v1 = P[1:-3] - P[:-4]; v2 = P[4:] - P[3:-1]                  # Segment (i-2, i-1) vs. (i+1, i+2)
    nv = np.hypot(*v1.T) * np.hypot(*v2.T)
    c = (v1 * v2).sum(1) / (nv + 1e-15)
    knick = np.where(nv > 1e-12, np.degrees(np.arccos(np.clip(c, -1, 1))), 0)
    if not geschlossen: knick[:2] = 0; knick[-2:] = 0
    return R, abw, knick
