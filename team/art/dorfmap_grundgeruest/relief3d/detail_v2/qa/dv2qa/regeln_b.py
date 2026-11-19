"""Q6-Q10 (Wegprofil, D2, Ufer, Netzqualitaet, UV)."""
import numpy as np
from .geom import abtasten, dreieckswinkel, kanten_von
from .regeln_a import erg, _r, _mittellinien
from .welt import Fehlt


# ------------------------------------------------------------------ Q6
def q6(ctx):
    from shapely import union_all, contains_xy
    S = ctx.k['schwellen']; o = ctx.ortung(('gelaende',)); bp = ctx.k['mittellinien']['breite_prop']
    kz = [g for g, _ in ctx.polygone(ctx.k['kreuzungen']['datei'], pflicht=False)]
    kreuz = union_all([g.buffer(1.5) for g in kz]) if kz else None
    wasser = [g for g, _ in ctx.polygone(ctx.k['wasser']['datei'], pflicht=False)]
    wass = union_all([g.buffer(1.0) for g in wasser]) if wasser else None
    lo, hi = S['q6_einsenkung_m']
    bef, stat = [], {'stationen': 0, 'einsenkung_min_m': 9, 'einsenkung_max_m': -9, 'quer_max': 0, 'laengs_max_grad': 0}
    for pl, pr in _mittellinien(ctx):
        b = float(pr.get(bp, 2.0))
        s = abtasten(pl, 1.0)
        if len(s) < 3: continue
        tg = np.gradient(s, axis=0); tg /= np.hypot(*tg.T)[:, None] + 1e-15; nrm = np.c_[-tg[:, 1], tg[:, 0]]
        frei = np.ones(len(s), bool); frei[[0, -1]] = False
        if kreuz is not None: frei &= ~contains_xy(kreuz, s[:, 0], s[:, 1])
        sch = b / 2 + 0.4 + 0.3                                 # Schulter ausserhalb der 0,4-m-Rampe
        if wass is not None:
            for sg in (-1, 1):
                q = s + sg * sch * nrm; frei &= ~contains_xy(wass, q[:, 0], q[:, 1])
        off = np.arange(-(b / 2 - 0.1), b / 2 - 0.1 + 1e-9, 0.1)
        Q = s[:, None] + off[None, :, None] * nrm[:, None]
        hq, _ = o.hoehe(Q[..., 0].ravel(), Q[..., 1].ravel()); hq = hq.reshape(len(s), len(off))
        hc, _ = o.hoehe(s[:, 0], s[:, 1])
        hl, _ = o.hoehe(*(s - sch * nrm).T); hr, _ = o.hoehe(*(s + sch * nrm).T)
        eins = (hl + hr) / 2 - hc
        A = np.c_[off, np.ones_like(off)]
        quer = np.abs(np.linalg.lstsq(A, np.nan_to_num(hq.T), rcond=None)[0][0])
        laengs = np.degrees(np.arctan(np.abs(np.gradient(hc, 1.0))))
        for i in np.nonzero(frei)[0]:
            if np.isnan(hq[i]).any() or np.isnan(eins[i]): continue
            stat['stationen'] += 1
            stat['einsenkung_min_m'] = min(stat['einsenkung_min_m'], eins[i]); stat['einsenkung_max_m'] = max(stat['einsenkung_max_m'], eins[i])
            stat['quer_max'] = max(stat['quer_max'], quer[i]); stat['laengs_max_grad'] = max(stat['laengs_max_grad'], laengs[i])
            f = []
            if not (lo - 1e-4 <= eins[i] <= hi + 1e-4): f.append('einsenkung')
            if quer[i] > S['q6_quer'] + 1e-6: f.append('quergefaelle')
            if laengs[i] > S['q6_laengs_grad']: f.append('laengsneigung')
            if f: bef.append({'id': pr.get('id'), 'x': _r(s[i, 0], 2), 'z': _r(s[i, 1], 2), 'art': f, 'einsenkung_m': _r(eins[i]), 'quer': _r(quer[i]), 'laengs_grad': _r(laengs[i], 1)})
    stat = {k: _r(v) if isinstance(v, float) else v for k, v in stat.items()}
    return erg('Q6', not bef and stat['stationen'] > 0, {**stat, 'schwellen': [lo, hi, S['q6_quer'], S['q6_laengs_grad']]}, bef,
               'Stationen alle 1 m; Einsenkung = Mittel der Schultern bei +-(b/2+0,7 m) minus Mitte; Quergefaelle = Geradenfit ueber die Wegbreite; Kreuzungen (+1,5 m), Enden und Uferbereiche ausgenommen.')


# ------------------------------------------------------------------ Q7
def q7(ctx):
    """D2-Regel (Entscheidung New Bot 19.11.2026 ueber Grundgeruest): D2-Bereich Lage und Form erhalten,
    |dh| <= 1 cm an den alten D2-Vertices; ersetzt 'D2 bitgleich'. Alte Dateien/Hashes bleiben unveraendert."""
    S = ctx.k['schwellen']
    if ctx.referenz is None or not (ctx.referenz / 'd2_alt.npz').exists(): raise Fehlt('referenz/d2_alt.npz fehlt')
    alt = np.load(ctx.referenz / 'd2_alt.npz')['xyz'].astype(np.float64)
    o = ctx.ortung(('gelaende',))
    h, t = o.hoehe(alt[:, 0], alt[:, 2])
    fehlt = np.isnan(h); dh = np.abs(h - alt[:, 1])
    x0, z0, x1, z1 = S['q7_bereich']
    d2 = ctx.kacheln.get('D2')
    umriss_ok = d2 is not None and [float(v) for v in d2['bounds']] == [x0, z0, x1, z1]
    # Lage/Form: Wasser-, Weg- und Bauzonen-Umriss im D2-Bereich wird ueber Q14 und die dh-Pruefung erfasst
    over = np.nonzero(~fehlt & (dh > S['q7_dh_m'] + 1e-6))[0]
    bef = [{'x': _r(alt[i, 0], 2), 'z': _r(alt[i, 2], 2), 'dh_m': _r(dh[i])} for i in over[np.argsort(-dh[over])][:20]]
    bef += [{'x': _r(alt[i, 0], 2), 'z': _r(alt[i, 2], 2), 'fehler': 'nicht abgedeckt'} for i in np.nonzero(fehlt)[0][:10]]
    if not umriss_ok: bef.append({'fehler': 'Kachel D2 fehlt oder Umriss != ' + str(S['q7_bereich'])})
    return erg('Q7', not bef, {'alte_vertices': int(len(alt)), 'nicht_abgedeckt': int(fehlt.sum()), 'ueber_schwelle': int(len(over)),
                               'dh_max_m': _r(np.nanmax(dh) if (~fehlt).any() else np.nan, 5), 'dh_p99_m': _r(np.nanpercentile(dh, 99) if (~fehlt).any() else np.nan, 5),
                               'schwelle_m': S['q7_dh_m'], 'umriss_ok': umriss_ok,
                               'regel_quelle': 'Entscheidung New Bot 19.11.2026 ueber Grundgeruest: |dh|<=1 cm statt bitgleich'}, bef,
               'Neue Gelaendehoehe an jedem alten D2-Vertex (alle_kacheln D2, 7395 Vertices) per Dreiecksinterpolation.')


# ------------------------------------------------------------------ Q8
def _konturen(V, T, stufe):
    """Exakte Schnittlinie Gelaende = stufe als Segmentliste (k x 2 x 2)."""
    h = V[T, 1] - stufe
    s = np.sign(h); s[s == 0] = 1e-9
    segs = []
    for (a, b), (c, d) in (((0, 1), (1, 2)), ((1, 2), (2, 0)), ((2, 0), (0, 1))):
        m = (s[:, a] * s[:, b] < 0) & (s[:, c] * s[:, d] < 0)
        if not m.any(): continue
        def p(i, j):
            ta = h[m, i] / (h[m, i] - h[m, j]); A = V[T[m, i]][:, [0, 2]]; B = V[T[m, j]][:, [0, 2]]
            return A + (B - A) * ta[:, None]
        segs.append(np.stack([p(a, b), p(c, d)], 1))
    return np.concatenate(segs) if segs else np.zeros((0, 2, 2))


def _ufer(ctx):
    """Uferlinien (ufer.geojson typ=uferlinie) mit Spiegel je Stuetzpunkt (spiegel_m Liste oder Zahl)."""
    out = []
    for pl, geschl, pr in ctx.linien(ctx.k['uferlinie']):
        sp = pr.get(ctx.k['wasser']['spiegel_prop'])
        if isinstance(sp, list) and len(sp) == len(pl): s = np.array(sp, float)
        elif isinstance(sp, (int, float)): s = np.full(len(pl), float(sp))
        else: s = None
        out.append((pl, geschl, pr, s))
    return out


def q8(ctx):
    """Ufer nach Entscheidung Grundgeruest 19.11. (Runde 2): Gelaendemesh geschlossen inkl. Bachbett (Klasse 4),
    Wasseroberflaeche = eigenes Modell (modelle[], klasse 4, Spiegel aus spiegel_m).
    (a) Spalt: jeder Randpunkt des Spiegelmodells (5 cm) liegt im Ufer, d. h. Gelaende >= Spiegel - Toleranz
        (sonst sieht man von oben zwischen Spiegelkante und Boeschung ins Bett/auf trockenes Bett).
    (b) Schnitt: je Uferstation (10 cm) wechselt Gelaende - Spiegel entlang der Normalen (-2 m Wasser .. +2,5 m Land) von < 0
        auf >= 0; fehlt der Wechsel und liegt der Spiegel ueberall unter dem Gelaende -> 'spiegel unter uferkante ohne schnitt'.
    (c) Schnittlinie Spiegel/Gelaende (exakte Kontur) vs. Uferlinie <= 5 cm, beidseitig.
    (d) Boeschung landeinwaerts monoton (1 mm), Krone > spiegel_m."""
    from shapely import linestrings, points, distance, union_all, LineString, contains_xy, STRtree, box
    S = ctx.k['schwellen']; n = ctx.netz(('gelaende',)); V, T = n['V'], n['T']; o = ctx.ortung(('gelaende',))
    ufer = _ufer(ctx)
    if not ufer: raise Fehlt('keine Uferlinien (ufer.geojson typ=uferlinie)')
    if any(u[3] is None for u in ufer): raise Fehlt('spiegel_m je Uferpunkt fehlt')
    w = {'uferlinien': len(ufer), 'spiegelmodelle': [], 'spiegel_randpunkte': 0, 'spalt_punkte': 0, 'spalt_max_m': 0.0,
         'stationen': 0, 'ohne_schnitt': 0, 'ohne_spiegel': 0, 'schnitt_abstand_max_m': 0.0, 'kontursegmente': 0,
         'kontur_ufer_max_m': 0.0, 'ufer_kontur_max_m': 0.0, 'spiegel_vs_spiegel_m_max_m': 0.0, 'nicht_monoton': 0, 'ueber_krone': 0, 'profile': 0}
    bef = []
    try:
        wo = ctx.wasser_ortung()
    except Fehlt as e:
        return erg('Q8', False, w, [{'fehler': str(e)}])
    w['spiegelmodelle'] = ctx.wasser_ids()
    karte = union_all([box(*kd['bounds']) for kd in ctx.kacheln.values()]).boundary
    wpol = [g for g, _ in ctx.polygone(ctx.k['wasser']['datei'], ctx.k['wasser'].get('filter'))]
    wasser = union_all(wpol) if wpol else None
    ul = union_all([LineString(u[0]) for u in ufer])
    # (a) Spiegelrand im Ufer
    nw = ctx.netz((), 'wasser'); Vw, Tw = nw['V'], nw['T']
    e = np.sort(kanten_von(Tw), 1); u, c = np.unique(e, axis=0, return_counts=True); rk = u[c == 1]
    pts = []
    for i, j in rk:
        A, B = Vw[i], Vw[j]; k = max(int(np.ceil(np.hypot(*(B - A)[[0, 2]]) / 0.05)), 1)
        t = np.linspace(0, 1, k + 1)[:, None]; pts.append(A + (B - A) * t)
    R = np.unique(np.round(np.vstack(pts), 6), axis=0) if pts else np.zeros((0, 3))
    if len(R):
        R = R[distance(points(R[:, [0, 2]]), karte) > 1e-3]           # Kartenrand (Bach laeuft hinaus) ausgenommen
        ht, _ = o.hoehe(R[:, 0], R[:, 2]); sp = R[:, 1] - ht
        spalt = ~np.isnan(ht) & (sp > S['q8_spalt_m'])
        w['spiegel_randpunkte'] = int(len(R)); w['spalt_punkte'] = int(spalt.sum()); w['spalt_max_m'] = float(np.nanmax(sp)) if len(sp) else 0.0
        for i in np.nonzero(spalt)[0][np.argsort(-sp[spalt])][:8]:
            bef.append({'art': 'spalt spiegel/ufer', 'x': _r(R[i, 0], 2), 'z': _r(R[i, 2], 2), 'spiegel_ueber_gelaende_m': _r(sp[i])})
    # (c) Kontur Gelaende = Spiegelmodell auf Gelaende-Dreiecken
    from scipy.spatial import cKDTree
    hs, _ = wo.hoehe(V[:, 0], V[:, 2])
    fehlt = np.isnan(hs)                                          # Spiegelebene bis 1 m ueber die Modellkante fortsetzen (Kontur auch bei Spalt)
    if fehlt.any():
        dk, jk = cKDTree(Vw[:, [0, 2]]).query(V[fehlt][:, [0, 2]], distance_upper_bound=1.0)
        hs[np.nonzero(fehlt)[0][np.isfinite(dk)]] = Vw[jk[np.isfinite(dk)], 1]
    dv = V[:, 1] - hs; dv[np.abs(dv) < 5e-4] = 0.0                  # Vertices auf der Wasserlinie (float32) = 0
    TT = T[~np.isnan(dv[T]).any(1)]
    segs = _kontur_v(V, TT, dv)
    segs = segs[np.hypot(*(segs[:, 1] - segs[:, 0]).T) > 1e-6] if len(segs) else segs
    w['kontursegmente'] = int(len(segs))
    if len(segs) == 0:
        bef.append({'fehler': 'keine Schnittlinie Spiegel/Gelaende'})
        sl = tree = None; sp_pts = np.zeros((0, 2)); d1 = np.zeros(1)
    else:
        sl = linestrings(segs); tree = STRtree(sl)
        sp_pts = segs.reshape(-1, 2)
        sp_pts = sp_pts[distance(points(sp_pts), karte) > 0.5]
        d1 = distance(points(sp_pts), ul) if len(sp_pts) else np.zeros(1)
    bp = ctx.k['mittellinien']['breite_prop']
    wz = [LineString(pl).buffer(float(pr.get(bp, 2.0)) / 2 + 0.4, cap_style='flat') for pl, pr in _mittellinien_opt(ctx)]
    wz += [g.buffer(0.4) for g, _ in ctx.polygone(ctx.k['kreuzungen']['datei'], pflicht=False)]
    wegzone = union_all(wz) if wz else None
    off = np.round(np.arange(-2.0, S['q8_boeschung_m'] + 1e-9, 0.05), 3); i0 = int(np.argmin(np.abs(off)))
    for pl, geschl, pr, spv in ufer:
        us = abtasten(pl, 0.1)
        dd = np.r_[0, np.cumsum(np.hypot(*np.diff(pl, axis=0).T))]; ds = np.r_[0, np.cumsum(np.hypot(*np.diff(us, axis=0).T))]
        spl = np.interp(ds, dd, spv)
        rand = distance(points(us), karte) < 0.5
        d2 = np.full(len(us), 9.99)
        if tree is not None:
            ii, jj = tree.query_nearest(points(us), return_distance=False)
            d2[:] = np.inf; np.minimum.at(d2, ii, distance(points(us[ii]), sl[jj]))
        d2[rand] = 0
        w['ufer_kontur_max_m'] = max(w['ufer_kontur_max_m'], float(d2.max()))
        if d2.max() > S['q8_ufer_m']:
            k = int(np.argmax(d2)); bef.append({'ufer': pr.get('id'), 'art': 'ufer->schnittlinie', 'abstand_m': _r(d2[k]), 'x': _r(us[k, 0], 2), 'z': _r(us[k, 1], 2)})
        tg = np.gradient(us, axis=0); tg /= np.hypot(*tg.T)[:, None] + 1e-15; nr = np.c_[-tg[:, 1], tg[:, 0]]
        if wasser is not None:
            probe = us + 0.3 * nr; nr[contains_xy(wasser.buffer(1e-3), probe[:, 0], probe[:, 1])] *= -1
        else:
            h1, _ = o.hoehe(*(us + 0.5 * nr).T); h2, _ = o.hoehe(*(us - 0.5 * nr).T); nr[np.nan_to_num(h1) < np.nan_to_num(h2)] *= -1
        Q = us[:, None] + off[None, :, None] * nr[:, None]
        h, _ = o.hoehe(Q[..., 0].ravel(), Q[..., 1].ravel()); h = h.reshape(len(us), len(off))
        hw, _ = wo.hoehe(Q[..., 0].ravel(), Q[..., 1].ravel()); hw = hw.reshape(len(us), len(off))
        # (b) Schnitt je Station
        dlt = h - hw; gedeckt = ~np.isnan(dlt)
        wech = gedeckt[:, :-1] & gedeckt[:, 1:] & (dlt[:, :-1] < 0) & (dlt[:, 1:] >= 0)
        hat = wech.any(1); ohne_sp = ~gedeckt.any(1) & ~rand
        ohne = ~hat & gedeckt.any(1) & ~rand & (np.where(gedeckt, dlt, np.inf).min(1) >= 0)
        w['stationen'] += int((~rand).sum()); w['ohne_schnitt'] += int(ohne.sum()); w['ohne_spiegel'] += int(ohne_sp.sum())
        if hat.any():
            k = np.argmax(wech, 1); a0 = dlt[np.arange(len(us)), k]; a1 = dlt[np.arange(len(us)), k + 1]
            pos = off[k] + (off[k + 1] - off[k]) * a0 / (a0 - a1 + 1e-15)
            dk = np.where(hat & ~rand, np.abs(pos), 0); w['schnitt_abstand_max_m'] = max(w['schnitt_abstand_max_m'], float(dk.max()))
        sv = hw[:, i0 - 6]                                           # Spiegelhoehe 30 cm wasserseitig
        dsv = np.abs(sv - spl); dsv = dsv[~np.isnan(dsv) & ~rand]
        if len(dsv): w['spiegel_vs_spiegel_m_max_m'] = max(w['spiegel_vs_spiegel_m_max_m'], float(dsv.max()))
        for i in np.nonzero(ohne)[0][:5]: bef.append({'ufer': pr.get('id'), 'art': 'spiegel unter uferkante ohne schnitt', 'x': _r(us[i, 0], 2), 'z': _r(us[i, 1], 2), 'spiegel_m': _r(np.nanmax(hw[i])), 'gelaende_min_m': _r(np.nanmin(h[i]))})
        for i in np.nonzero(ohne_sp)[0][:5]: bef.append({'ufer': pr.get('id'), 'art': 'kein spiegel am ufer', 'x': _r(us[i, 0], 2), 'z': _r(us[i, 1], 2)})
        # (d) Boeschung landeinwaerts
        hl = h[:, i0:].copy(); Ql = Q[:, i0:]
        if wegzone is not None:
            inw = contains_xy(wegzone, Ql[..., 0], Ql[..., 1]); inw = np.maximum.accumulate(inw, axis=1); hl = np.where(inw, np.nan, hl)
        hl = hl[:, ::2]                                              # 10-cm-Schritte
        ok = ~np.isnan(hl[:, :2]).any(1); w['profile'] += int(ok.sum())
        nm = ok & (np.nan_to_num(np.diff(hl, axis=1), nan=0) < -S['q8_mono_tol_m']).any(1)
        with np.errstate(all='ignore'):
            krone = ok & (np.nanmax(np.where(np.isnan(hl), -np.inf, hl), 1) <= spl)
        w['nicht_monoton'] += int(nm.sum()); w['ueber_krone'] += int(krone.sum())
        for i in np.nonzero(nm)[0][:5]: bef.append({'ufer': pr.get('id'), 'art': 'boeschung nicht monoton', 'x': _r(us[i, 0], 2), 'z': _r(us[i, 1], 2)})
        for i in np.nonzero(krone)[0][:5]: bef.append({'ufer': pr.get('id'), 'art': 'wasser ueber krone', 'x': _r(us[i, 0], 2), 'z': _r(us[i, 1], 2)})
    w['kontur_ufer_max_m'] = float(d1.max())
    if d1.max() > S['q8_ufer_m']:
        k = int(np.argmax(d1)); bef.append({'art': 'schnittlinie->ufer', 'abstand_m': _r(d1[k]), 'x': _r(sp_pts[k, 0], 2), 'z': _r(sp_pts[k, 1], 2)})
    w = {k: _r(v) if isinstance(v, float) else v for k, v in w.items()}
    return erg('Q8', not bef, {**w, 'schwellen_m': {'ufer': S['q8_ufer_m'], 'spalt': S['q8_spalt_m']}}, bef,
               'Spiegelmodell (manifest.modelle klasse 4) vs. geschlossenes Gelaende inkl. Bett: Spiegelrand 5 cm im Ufer (Gelaende >= Spiegel - 2 mm, sonst Spalt); '
               'je Uferstation 10 cm Vorzeichenwechsel Gelaende-Spiegel (-2..+2,5 m), sonst ohne Schnitt; Kontur Gelaende=Spiegel vs. Uferlinie <= 5 cm beidseitig; '
               'Boeschung 0-2,5 m landeinwaerts monoton (endet am Wegband), Krone > spiegel_m. Kartenrand ausgenommen. spiegel_vs_spiegel_m nur Bericht.')


def _kontur_v(V, T, hv):
    """Kontur hv = 0 (hv je Vertex) -> Segmente k x 2 x 2 (XZ)."""
    h = hv[T]
    s = np.sign(h); s[s == 0] = 1
    segs = []
    for (a, b), (c, d) in (((0, 1), (1, 2)), ((1, 2), (2, 0)), ((2, 0), (0, 1))):
        m = (s[:, a] * s[:, b] < 0) & (s[:, c] * s[:, d] < 0)
        if not m.any(): continue
        def p(i, j):
            ta = h[m, i] / (h[m, i] - h[m, j]); A = V[T[m, i]][:, [0, 2]]; B = V[T[m, j]][:, [0, 2]]
            return A + (B - A) * ta[:, None]
        segs.append(np.stack([p(a, b), p(c, d)], 1))
    return np.concatenate(segs) if segs else np.zeros((0, 2, 2))


def _kurvenradien(ctx):
    """Mittellinien je 0,25 m abgetastet; Radius je Punkt = kleinster Umkreisradius (Punkte +-1 m) im Umkreis +-1,5 m Bogenlaenge."""
    from scipy.ndimage import minimum_filter1d
    pts, rad = [], []
    for pl, _ in _mittellinien_opt(ctx):
        s = abtasten(pl, 0.25)
        if len(s) < 9: continue
        a, b, c = s[:-8], s[4:-4], s[8:]
        la = np.hypot(*(b - a).T); lb = np.hypot(*(c - b).T); lc = np.hypot(*(c - a).T)
        cr = np.abs((b - a)[:, 0] * (c - a)[:, 1] - (b - a)[:, 1] * (c - a)[:, 0])
        r = np.where(cr > 1e-9, la * lb * lc / (2 * cr + 1e-30), np.inf)
        r = np.r_[np.full(4, r[0]), r, np.full(4, r[-1])]
        r = minimum_filter1d(r, size=13, mode='nearest')
        pts.append(s); rad.append(r)
    if not pts: return np.zeros((0, 2)), np.zeros(0)
    return np.vstack(pts), np.concatenate(rad)


def _mittellinien_opt(ctx):
    try: return _mittellinien(ctx)
    except Fehlt: return []


def _konturen_lokal(V, T, stufe):
    h = V[T, 1] - stufe[:, None]
    s = np.sign(h); s[s == 0] = 1
    segs = []
    for (a, b), (c, d) in (((0, 1), (1, 2)), ((1, 2), (2, 0)), ((2, 0), (0, 1))):
        m = (s[:, a] * s[:, b] < 0) & (s[:, c] * s[:, d] < 0)
        if not m.any(): continue
        def p(i, j):
            ta = h[m, i] / (h[m, i] - h[m, j]); A = V[T[m, i]][:, [0, 2]]; B = V[T[m, j]][:, [0, 2]]
            return A + (B - A) * ta[:, None]
        segs.append(np.stack([p(a, b), p(c, d)], 1))
    return np.concatenate(segs) if segs else np.zeros((0, 2, 2))


# ------------------------------------------------------------------ Q9
def q9(ctx):
    """Kante <= Punktabstand x sqrt2 (+1 %) im Grundriss: Band 0,2 / Wegband 0,25 / begehbar 0,5 / fern 1,0 m
    (Fernbereich mitgemessen, Entscheidung Grundgeruest 19.11.); Min-Winkel >= 20 Grad ausser Constraint-Ecken; Normalen oben; Budget."""
    from shapely import STRtree, points, LineString, box
    S = ctx.k['schwellen']; n = ctx.netz(('gelaende',)); V, T = n['V'], n['T']
    P = V[T]
    nr = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); ny = nr[:, 1]
    flaeche = np.linalg.norm(nr, axis=1) / 2
    unten = np.nonzero(ny <= 0)[0]; entartet = np.nonzero(flaeche < 1e-6)[0]
    G = P[:, :, [0, 2]]
    L = np.stack([np.linalg.norm(G[:, 1] - G[:, 0], axis=1), np.linalg.norm(G[:, 2] - G[:, 1], axis=1), np.linalg.norm(G[:, 0] - G[:, 2], axis=1)], 1).max(1)
    cen = G.mean(1)
    cl = ctx.constraint_linien()
    lines = [LineString(pl) for pl, *_ in cl]
    im_band = np.zeros(len(T), bool)
    if lines:
        ii, _ = STRtree(lines).query(points(cen), predicate='dwithin', distance=S['q9_band_breite_m']); im_band[ii] = True
    ml = [LineString(pl) for pl, _ in _mittellinien_opt(ctx)]
    fern = np.zeros(len(T), bool)
    if ml:
        a, _ = STRtree(ml).query(points(cen), predicate='dwithin', distance=S['q9_fern_ab_weg_m']); near = np.zeros(len(T), bool); near[a] = True; fern = ~near
    f = S['q9_diagonal_faktor']
    weg = n['klasse'] == 'weg'
    grenze = np.where(im_band, S['q9_band_abstand_m'], np.where(weg, S['q9_wegband_abstand_m'],
                      np.where(fern, S['q9_fern_abstand_m'], S['q9_begehbar_abstand_m']))) * f
    zu_lang = np.nonzero(L > grenze + 1e-6)[0]
    w = dreieckswinkel(G)
    ecken = []
    for pl, geschl, *_ in cl:
        if not geschl: ecken += [pl[0], pl[-1]]
        if len(pl) > 2:
            v1 = pl[1:-1] - pl[:-2]; v2 = pl[2:] - pl[1:-1]
            c = (v1 * v2).sum(1) / (np.hypot(*v1.T) * np.hypot(*v2.T) + 1e-15)
            ecken += list(pl[1:-1][c < np.cos(np.radians(10))])
    kb = [box(*kd['bounds']).boundary for kd in ctx.kacheln.values()]
    allel = lines + kb
    if lines:
        a, b = STRtree(allel).query(allel, predicate='intersects')
        for i, j in zip(a, b):
            if i < j and (i < len(lines) or j < len(lines)):
                x = allel[i].intersection(allel[j])
                for gg in getattr(x, 'geoms', [x]):
                    if gg.geom_type == 'Point': ecken.append([gg.x, gg.y])
    ecken = np.array(ecken) if len(ecken) else np.zeros((0, 2))
    ausnahme = np.zeros(len(T), bool)
    if len(ecken):
        from scipy.spatial import cKDTree
        kd = cKDTree(ecken)
        for k in range(3):
            d, _ = kd.query(G[:, k]); ausnahme |= d < 1e-3
    spitz = np.nonzero((w < S['q9_min_winkel']) & ~ausnahme)[0]
    kz = {kid: int(sum(len(p['idx']) for p in ctx.kacheln[kid]['prims'])) for kid in ctx.kacheln}
    gesamt = sum(kz.values()) + sum(len(p['idx']) for m in ctx.modelle().values() for p in m)
    ueber = {k: v for k, v in kz.items() if v > S['q9_dreiecke_kachel']}
    man = {kid: kd.get('dreiecke_manifest') for kid, kd in ctx.kacheln.items()}
    falsch_man = {k: [man[k], v] for k, v in kz.items() if man[k] is not None and man[k] != v}
    bef = [{'art': 'normale_unten', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2)} for i in unten[:10]]
    bef += [{'art': 'entartet', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2)} for i in entartet[:5]]
    bef += [{'art': 'kante_zu_lang', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2), 'kante_m': _r(L[i]), 'grenze_m': _r(grenze[i])} for i in zu_lang[np.argsort(-(L[zu_lang] / grenze[zu_lang]))][:10]]
    bef += [{'art': 'winkel<20', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2), 'winkel_grad': _r(w[i], 1)} for i in spitz[np.argsort(w[spitz])][:10]]
    bef += [{'art': 'budget_kachel', 'kachel': k, 'dreiecke': v} for k, v in ueber.items()]
    bef += [{'art': 'manifest_dreiecke', 'kachel': k, 'manifest_glb': v} for k, v in falsch_man.items()]
    if gesamt > S['q9_dreiecke_gesamt']: bef.append({'art': 'budget_gesamt', 'dreiecke': gesamt})
    def mx(m): return _r(float(L[m].max())) if m.any() else None
    return erg('Q9', not bef, {'dreiecke_gesamt': gesamt, 'dreiecke_max_kachel': max(kz.values()), 'normale_unten': int(len(unten)),
                               'entartet': int(len(entartet)), 'kante_zu_lang': int(len(zu_lang)),
                               'min_winkel_grad': _r(float(w[~ausnahme].min()) if (~ausnahme).any() else 0, 2),
                               'winkel_unter_20': int(len(spitz)), 'constraint_ecken': int(len(ecken)),
                               'kante_max_m': {'band': mx(im_band), 'wegband': mx(~im_band & weg), 'begehbar': mx(~im_band & ~weg & ~fern), 'fern': mx(~im_band & ~weg & fern)}}, bef,
               'Kante (Grundriss) <= Punktabstand x sqrt2 (+1 %): Band 0,2 / Wegband 0,25 / sonst 0,5 / fern (> 30 m von Wegen) 1,0 m -> 0,286 / 0,357 / 0,714 / 1,428 m; alle Klassen gemessen.')


# ------------------------------------------------------------------ Q10
def q10(ctx):
    """UV nach Entscheidung Grundgeruest 19.11.: UV0 (Welt-XZ) nur fuer Neigung <= 25 Grad und Klasse != 3 mit <= 10 %;
    Triplanar-Zone (Klasse 3 oder > 25 Grad): nur Stetigkeit (keine Spruenge/Flips, keine NaN); UV1 = (x/336, z/303);
    UV2 im Wegband (Klasse 1) <= 10 % Verzerrung."""
    from scipy.spatial import cKDTree
    S = ctx.k['schwellen']; W, H = ctx.k['welt_m']
    n = ctx.netz(('gelaende',)); V, T = n['V'], n['T']; P = V[T]
    u0, u1, u2 = n['uv0'], n['uv1'], n['uv2']
    bef, w = [], {}
    if not n['hat']['uv0'].all() or not n['hat']['uv1'].all(): bef.append({'art': 'TEXCOORD_0/1 fehlt', 'dreiecke': int((~(n['hat']['uv0'] & n['hat']['uv1'])).sum())})
    def sfl(Q):
        a = Q[:, 1] - Q[:, 0]; b = Q[:, 2] - Q[:, 0]; return (a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]) / 2
    nrm = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); a3 = np.linalg.norm(nrm, axis=1) / 2
    neig = np.degrees(np.arccos(np.clip(np.abs(nrm[:, 1]) / (2 * a3 + 1e-15), 0, 1)))
    tri = (n['klasse'] == 'fels_klippe') | (neig > S['q10_uv0_bis_grad'])
    axz = sfl(P[:, :, [0, 2]]); a0 = sfl(u0); a1 = sfl(u1)
    nan0 = np.isnan(u0).any((1, 2)) & n['hat']['uv0']; nan1 = np.isnan(u1).any((1, 2)) & n['hat']['uv1']
    nan2 = np.isnan(u2).any((1, 2)) & n['hat']['uv2']
    gross = np.abs(axz) > 1e-9
    gesp0 = gross & ~nan0 & (np.sign(a0) != np.sign(axz))
    gesp1 = gross & ~nan1 & (np.sign(a1) != np.sign(axz))
    soll1 = np.stack([P[:, :, 0] / W, P[:, :, 2] / H], -1)
    uv1_falsch = ~nan1 & (np.abs(u1 - soll1).max((1, 2)) > 1e-5)
    # Spruenge: positionsgleiche Ecken (verschweisst) mit verschiedenem UV0
    Tf = T.ravel(); U = u0.reshape(-1, 2)
    ok = ~np.isnan(U).any(1)
    o = np.argsort(Tf[ok], kind='stable'); tv, uu = Tf[ok][o], U[ok][o]
    st = np.r_[0, np.nonzero(np.diff(tv))[0] + 1]
    mn = np.minimum.reduceat(uu, st, axis=0); mxx = np.maximum.reduceat(uu, st, axis=0)
    sprung_v = tv[st][(mxx - mn).max(1) > 1e-3]
    sprung = np.isin(T, sprung_v).any(1)
    verz0 = np.abs(1 - np.abs(a0) / (a3 + 1e-15))
    flach = ~tri & (a3 > 1e-9) & ~nan0
    zu0 = flach & (verz0 > S['q10_verzerrung'])
    # UV2 im Wegband: Gradienten von u (laengs, Bogenlaenge) und v (quer) in der Dreiecksebene
    weg = (n['klasse'] == 'weg') & (a3 > 1e-9)
    weg_ohne = weg & (~n['hat']['uv2'] | nan2)
    wg = weg & ~weg_ohne
    zu2 = np.zeros(len(T), bool); g_u = np.full(len(T), np.nan); cosw = np.full(len(T), np.nan); vrel = np.full(len(T), np.nan)
    if wg.any():
        i = np.nonzero(wg)[0]; Pw = P[i]; Uw = u2[i]
        e1 = Pw[:, 1] - Pw[:, 0]; e2 = Pw[:, 2] - Pw[:, 0]
        G = np.stack([e1, e2], 1)                                  # 2x3
        du = np.stack([Uw[:, 1, 0] - Uw[:, 0, 0], Uw[:, 2, 0] - Uw[:, 0, 0]], 1); dv = np.stack([Uw[:, 1, 1] - Uw[:, 0, 1], Uw[:, 2, 1] - Uw[:, 0, 1]], 1)
        Gp = np.linalg.pinv(G)                                    # 3x2: grad = Gp @ d
        gu = np.einsum('nij,nj->ni', Gp, du); gv = np.einsum('nij,nj->ni', Gp, dv)
        nu = np.linalg.norm(gu, axis=1); nv = np.linalg.norm(gv, axis=1)
        g_u[i] = nu; cosw[i] = np.abs((gu * gv).sum(1)) / (nu * nv + 1e-15)
        cc = P[i].mean(1)[:, [0, 2]]; kd = cKDTree(cc)
        nb = kd.query_ball_point(cc, 2.0)
        med = np.array([np.median(nv[b]) for b in nb]); vrel[i] = nv / (med + 1e-15)
        zu2[i] = (np.abs(nu - 1) > S['q10_verzerrung']) | (cosw[i] > S['q10_verzerrung']) | (np.abs(vrel[i] - 1) > S['q10_verzerrung'])
    # Kurvenradius der naechsten Mittellinie (Entscheidung Grundgeruest 19.11. Runde 2): UV2 <= 10 % gilt ab r >= 10 m,
    # darunter nur kennzeichnen und als Zahl berichten (nicht blockierend; nur ok, solange auf dem Clay-Bild nichts sichtbar ist).
    radius = np.full(len(T), np.inf)
    if wg.any():
        rs, rr = _kurvenradien(ctx)
        if len(rs):
            i = np.nonzero(wg)[0]; dd, jj = cKDTree(rs).query(P[i].mean(1)[:, [0, 2]]); radius[i] = rr[jj]
    eng = wg & (radius < S['q10_kurve_radius_m'])
    zu2_eng = zu2 & eng; zu2 = zu2 & ~eng
    w.update({'gespiegelt_uv0': int(gesp0.sum()), 'davon_triplanar': int((gesp0 & tri).sum()), 'gespiegelt_uv1': int(gesp1.sum()),
              'uv1_abweichend': int(uv1_falsch.sum()), 'nan_uv0': int(nan0.sum()), 'nan_uv1': int(nan1.sum()), 'nan_uv2': int(nan2.sum()),
              'spruenge_uv0': int(sprung.sum()), 'triplanar_dreiecke': int(tri.sum()),
              'verzerrung_uv0_max_bis25': _r(float(verz0[flach].max()) if flach.any() else 0), 'verzerrung_uv0_ueber_10pct': int(zu0.sum()),
              'wegband_dreiecke': int(weg.sum()), 'wegband_ohne_uv2': int(weg_ohne.sum()), 'uv2_ueber_10pct': int(zu2.sum()),
              'kurve_eng_schwelle_m': S['q10_kurve_radius_m'], 'uv2_enge_kurve_dreiecke': int(eng.sum()), 'uv2_enge_kurve_ueber_10pct_gekennzeichnet': int(zu2_eng.sum()),
              'uv2_enge_kurve_max_abw': _r(float(np.nanmax(np.abs(g_u[zu2_eng] - 1))) if zu2_eng.any() else 0),
              'kurvenradius_min_m': _r(float(radius[wg].min()) if wg.any() and np.isfinite(radius[wg]).any() else None, 2),
              'enge_kurven_orte': [{'x': _r(P[j, :, 0].mean(), 2), 'z': _r(P[j, :, 2].mean(), 2), 'r_m': _r(radius[j], 2), 'grad_u': _r(g_u[j])} for j in np.nonzero(zu2_eng)[0][:5]],
              'uv2_laengs_max_abw': _r(float(np.nanmax(np.abs(g_u - 1))) if wg.any() else None), 'max_neigung_grad': _r(float(neig.max()), 1)})
    def ort(m, art, extra=None):
        return [{'art': art, 'x': _r(P[i, :, 0].mean(), 2), 'z': _r(P[i, :, 2].mean(), 2), **({k: _r(v[i]) for k, v in (extra or {}).items()})} for i in np.nonzero(m)[0][:8]]
    bef += ort(gesp0, 'uv0_gespiegelt') + ort(gesp1, 'uv1_gespiegelt') + ort(uv1_falsch, 'uv1_nicht_(x/336,z/303)')
    bef += ort(nan0 | nan1 | nan2, 'uv_nan') + ort(sprung, 'uv0_sprung') + ort(zu0, 'uv0_verzerrung', {'verz': verz0, 'neigung_grad': neig})
    bef += ort(weg_ohne, 'wegband_ohne_uv2') + ort(zu2, 'uv2_verzerrung', {'grad_u': g_u, 'scherung_cos': cosw, 'quer_rel': vrel})
    return erg('Q10', not bef, w, bef,
               'UV0: Spiegelung (Vorzeichen UV- vs. XZ-Flaeche), NaN, Spruenge an positionsgleichen Ecken (> 1 mm) ueberall; Verzerrung |1 - A_UV0/A_3D| <= 10 % nur Neigung <= 25 Grad und Klasse != fels_klippe. '
               'UV2 (Klasse weg): |grad u| = 1 +- 10 % (Bogenlaenge), Scherung cos <= 0,1, |grad v| +- 10 % zum Median im 2-m-Umkreis (quer 0-1); '
               'blockierend nur bei Kurvenradius der naechsten Mittellinie >= 10 m, darunter gekennzeichnet (uv2_enge_kurve_*), nicht blockierend - nur ok, solange auf dem Clay-Bild (Q13) nichts sichtbar ist.')
