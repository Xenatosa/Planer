"""Geometrie-Helfer: Punktortung auf Dreiecksnetzen (XZ), Hoeheninterpolation, Polylinien."""
import numpy as np

KLASSEN = ['grund', 'weg', 'ufer', 'fels_klippe', 'wasser', 'bruecke']   # manifest.klassen 0..5 = _FLAECHE = flaeche.png (Entscheidung Grundgeruest 19.11.)


class Ortung:
    """Punktortung in XZ fuer Dreiecke (V: n x 3 mit y = Hoehe, T: m x 3). Gitterzellen 'zelle' m.
    Senkrechte Dreiecke (XZ-Flaeche ~0) werden ignoriert."""

    def __init__(self, V, T, zelle=0.5):
        self.V, self.T, self.z = V, T, zelle
        P = V[:, [0, 2]][T]                                    # m x 3 x 2
        a = P[:, 1] - P[:, 0]; b = P[:, 2] - P[:, 0]
        det = a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]
        ok = np.abs(det) > 1e-12
        self.P, self.det, self.ok = P, det, ok
        lo = P.min(1); hi = P.max(1)
        self.x0, self.z0 = lo[:, 0].min() - 1, lo[:, 1].min() - 1
        self.nx = int((hi[:, 0].max() - self.x0) / zelle) + 2; self.nz = int((hi[:, 1].max() - self.z0) / zelle) + 2
        i0 = np.floor((lo - [self.x0, self.z0]) / zelle).astype(int); i1 = np.floor((hi - [self.x0, self.z0]) / zelle).astype(int)
        zell, tri = [], []
        idx = np.nonzero(ok)[0]
        span = (i1 - i0 + 1)[idx]
        for sx in range(1, span[:, 0].max() + 1):
            for sz in range(1, span[:, 1].max() + 1):
                sel = idx[(span[:, 0] >= sx) & (span[:, 1] >= sz)]
                if len(sel) == 0: continue
                cx = i0[sel, 0] + sx - 1; cz = i0[sel, 1] + sz - 1
                zell.append(cz * self.nx + cx); tri.append(sel)
        zell = np.concatenate(zell); tri = np.concatenate(tri)
        o = np.argsort(zell, kind='stable'); zell, tri = zell[o], tri[o]
        self.start = np.searchsorted(zell, np.arange(self.nx * self.nz + 1))
        self.tri = tri
        self.kmax = int(np.diff(self.start).max())

    def finde(self, x, z, alle=False):
        """-> (dreieck_index (-1 = keins), baryzentrisch n x 3). Bei mehreren Treffern das hoechste Dreieck (alle=False)."""
        x = np.asarray(x, float); z = np.asarray(z, float); n = len(x)
        res = np.full(n, -1); bar = np.zeros((n, 3)); besth = np.full(n, -np.inf)
        cx = np.floor((x - self.x0) / self.z).astype(int); cz = np.floor((z - self.z0) / self.z).astype(int)
        inn = (cx >= 0) & (cx < self.nx) & (cz >= 0) & (cz < self.nz)
        c = np.where(inn, cz * self.nx + cx, 0)
        s0 = np.where(inn, self.start[c], 0); cnt = np.where(inn, self.start[c + 1] - s0, 0)
        for k in range(self.kmax):
            m = cnt > k
            if not m.any(): break
            ii = np.nonzero(m)[0]; t = self.tri[s0[ii] + k]
            P = self.P[t]; d = self.det[t]
            px = x[ii] - P[:, 0, 0]; pz = z[ii] - P[:, 0, 1]
            a = P[:, 1] - P[:, 0]; b = P[:, 2] - P[:, 0]
            l1 = (px * b[:, 1] - pz * b[:, 0]) / d; l2 = (a[:, 0] * pz - a[:, 1] * px) / d; l0 = 1 - l1 - l2
            e = -1e-9
            hit = (l0 >= e) & (l1 >= e) & (l2 >= e)
            if not hit.any(): continue
            ii, t = ii[hit], t[hit]; L = np.stack([l0[hit], l1[hit], l2[hit]], 1)
            h = (self.V[self.T[t], 1] * L).sum(1)
            better = h > besth[ii]
            ii, t, L, h = ii[better], t[better], L[better], h[better]
            res[ii] = t; bar[ii] = L; besth[ii] = h
        return res, bar

    def hoehe(self, x, z):
        t, L = self.finde(x, z)
        h = np.full(len(t), np.nan); m = t >= 0
        h[m] = (self.V[self.T[t[m]], 1] * L[m]).sum(1)
        return h, t


def abtasten(pl, schritt):
    """Polylinie (n x 2) gleichmaessig nach Bogenlaenge abtasten (inkl. Endpunkt)."""
    pl = np.asarray(pl, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(pl, axis=0).T))]
    if d[-1] == 0: return pl[:1]
    s = np.arange(0, d[-1], schritt)
    s = np.r_[s[s < d[-1] - 1e-6], d[-1]]
    return np.c_[np.interp(s, d, pl[:, 0]), np.interp(s, d, pl[:, 1])]


def glaettung_abw(pl, fenster=1.0, geschlossen=False):
    """Abweichung jedes Stuetzpunkts von der gleitenden Mittelung ueber 'fenster' m Bogenlaenge
    (Abstand Punkt -> geglaettete Linie, in m) und Knickwinkel (Grad) zwischen Nachbarsegmenten."""
    from shapely import LineString, points, distance
    pl = np.asarray(pl, float)
    if geschlossen and np.allclose(pl[0], pl[-1]): pl = pl[:-1]
    n = len(pl)
    if n < 3: return np.zeros(n), np.zeros(max(n - 2, 0))
    seg = np.hypot(*np.diff(np.vstack([pl, pl[:1]]) if geschlossen else pl, axis=0).T)
    s = np.r_[0, np.cumsum(seg)][:n]
    L = s[-1] + (seg[-1] if geschlossen else 0)
    g = np.empty_like(pl)
    for i in range(n):
        if geschlossen:
            dd = np.abs(s - s[i]); dd = np.minimum(dd, L - dd); m = dd <= fenster / 2
        else:
            hw = min(fenster / 2, s[i], s[-1] - s[i])            # an Enden symmetrisch verkuerztes Fenster
            m = (s >= s[i] - hw - 1e-9) & (s <= s[i] + hw + 1e-9)
        g[i] = pl[m].mean(0)
    gl = LineString(np.vstack([g, g[:1]]) if geschlossen else g)
    abw = distance(points(pl), gl)
    if not geschlossen:                                        # Endpunkte: Mittelung verzerrt -> nur innere Punkte
        abw[0] = abw[-1] = 0
    P = np.vstack([pl[-1:], pl, pl[:1]]) if geschlossen else pl
    v1 = P[1:-1] - P[:-2]; v2 = P[2:] - P[1:-1]
    c = (v1 * v2).sum(1) / (np.hypot(*v1.T) * np.hypot(*v2.T) + 1e-15)
    knick = np.degrees(np.arccos(np.clip(c, -1, 1)))
    return abw, knick


def kanten_von(T):
    e = np.sort(np.vstack([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), axis=1)
    return e


def dreieckswinkel(P):
    """P: m x 3 x 2|3 -> kleinster Innenwinkel (Grad) je Dreieck."""
    a = np.linalg.norm(P[:, 1] - P[:, 2], axis=1); b = np.linalg.norm(P[:, 0] - P[:, 2], axis=1); c = np.linalg.norm(P[:, 0] - P[:, 1], axis=1)
    def w(x, y, z):
        return np.degrees(np.arccos(np.clip((y * y + z * z - x * x) / (2 * y * z + 1e-15), -1, 1)))
    return np.minimum(np.minimum(w(a, b, c), w(b, a, c)), w(c, a, b))


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
