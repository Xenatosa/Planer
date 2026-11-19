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


def q8(ctx):
    from shapely import linestrings, points, distance, union_all, LineString, contains_xy, STRtree
    S = ctx.k['schwellen']; n = ctx.netz(('gelaende',)); V, T = n['V'], n['T']; o = ctx.ortung(('gelaende',))
    sp = ctx.k['wasser']['spiegel_prop']
    ufer = [pl for pl, _, _ in ctx.linien(ctx.k['uferlinie'])]
    bef, w = [], {'gewaesser': 0, 'kontur_ufer_max_m': 0.0, 'ufer_kontur_max_m': 0.0, 'nicht_monoton': 0, 'ueber_krone': 0, 'profile': 0}
    ul = union_all([LineString(u) for u in ufer]) if ufer else None
    bp = ctx.k['mittellinien']['breite_prop']
    wz = [LineString(pl).buffer(float(pr.get(bp, 2.0)) / 2 + 0.4, cap_style='flat') for pl, pr in _mittellinien(ctx)]
    wz += [g.buffer(0.4) for g, _ in ctx.polygone(ctx.k['kreuzungen']['datei'], pflicht=False)]
    wegzone = union_all(wz) if wz else None
    for g, pr in ctx.polygone(ctx.k['wasser']['datei']):
        w['gewaesser'] += 1
        spiegel = float(pr[sp])
        nah = g.buffer(3.0)
        cm = contains_xy(nah, V[T].mean(1)[:, 0], V[T].mean(1)[:, 2])
        segs = _konturen(V, T[cm], spiegel)
        if ul is None or len(segs) == 0:
            bef.append({'gewaesser': pr.get('id'), 'fehler': 'keine Uferlinie/Kontur'}); continue
        uf_hier = ul.intersection(nah)
        sl = linestrings(segs)
        d1 = distance(points(segs.reshape(-1, 2)), uf_hier)          # Kontur -> Uferlinie
        teile = [abtasten(np.array(l.coords), 0.1) for l in getattr(uf_hier, 'geoms', [uf_hier]) if l.length > 0]
        us = np.vstack(teile)
        tg = np.vstack([np.gradient(t, axis=0) for t in teile])         # Tangente je Teillinie
        tree = STRtree(sl); ii, jj = tree.query_nearest(points(us), return_distance=False)
        d2 = np.full(len(us), np.inf); np.minimum.at(d2, ii, distance(points(us[ii]), sl[jj]))
        w['kontur_ufer_max_m'] = max(w['kontur_ufer_max_m'], float(d1.max())); w['ufer_kontur_max_m'] = max(w['ufer_kontur_max_m'], float(d2.max()))
        for d, pts, art in ((d1, segs.reshape(-1, 2), 'kontur->ufer'), (d2, us, 'ufer->kontur')):
            if d.max() > S['q8_ufer_m']:
                k = int(np.argmax(d)); bef.append({'gewaesser': pr.get('id'), 'art': art, 'abstand_m': _r(d[k]), 'x': _r(pts[k, 0], 2), 'z': _r(pts[k, 1], 2)})
        # Boeschung: Profile senkrecht zur Uferlinie, landeinwaerts 0..2,5 m
        tg /= np.hypot(*tg.T)[:, None] + 1e-15; nr = np.c_[-tg[:, 1], tg[:, 0]]
        probe = us + 0.3 * nr; aussen = ~contains_xy(g.buffer(1e-3), probe[:, 0], probe[:, 1]); nr[~aussen] *= -1
        off = np.arange(0, S['q8_boeschung_m'] + 1e-9, 0.1)
        Q = us[:, None] + off[None, :, None] * nr[:, None]
        h, _ = o.hoehe(Q[..., 0].ravel(), Q[..., 1].ravel()); h = h.reshape(len(us), len(off))
        if wegzone is not None:                               # Profil endet am Wegband (Weg/Kreuzung inkl. 0,4-m-Rampe)
            inw = contains_xy(wegzone, Q[..., 0], Q[..., 1]); inw = np.maximum.accumulate(inw, axis=1); h = np.where(inw, np.nan, h)
        ok = ~np.isnan(h[:, :2]).any(1); w['profile'] += int(ok.sum())
        dd = np.diff(h, axis=1)
        nm = ok & (np.nan_to_num(dd, nan=0) < -S['q8_mono_tol_m']).any(1)
        krone = ok & (np.nanmax(h, 1) <= spiegel)
        w['nicht_monoton'] += int(nm.sum()); w['ueber_krone'] += int(krone.sum())
        for i in np.nonzero(nm)[0][:5]: bef.append({'gewaesser': pr.get('id'), 'art': 'boeschung nicht monoton', 'x': _r(us[i, 0], 2), 'z': _r(us[i, 1], 2)})
        for i in np.nonzero(krone)[0][:5]: bef.append({'gewaesser': pr.get('id'), 'art': 'wasser ueber krone', 'x': _r(us[i, 0], 2), 'z': _r(us[i, 1], 2)})
    w = {k: _r(v) if isinstance(v, float) else v for k, v in w.items()}
    return erg('Q8', not bef and w['gewaesser'] > 0, {**w, 'schwelle_m': S['q8_ufer_m']}, bef,
               'Exakte Nullkontur (Gelaende - Spiegel) aus den Dreiecken vs. Uferlinie (beidseitig); Profile alle 10 cm, 0-2,5 m landeinwaerts monoton (1 mm Toleranz); Krone > Spiegel.')


# ------------------------------------------------------------------ Q9
def q9(ctx):
    from shapely import STRtree, points, distance, LineString, union_all
    S = ctx.k['schwellen']; n = ctx.netz(('gelaende',)); V, T = n['V'], n['T']
    P = V[T]
    # Normalen nach oben (glTF: CCW = Vorderseite; y oben)
    nr = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); ny = nr[:, 1]
    flaeche = np.linalg.norm(nr, axis=1) / 2
    unten = np.nonzero(ny <= 0)[0]; entartet = np.nonzero(flaeche < 1e-6)[0]
    # Kantenlaengen (3D) je Dreieck
    G = P[:, :, [0, 2]]                                         # Kantenlaenge im Grundriss (= Punktabstand, Annahme)
    L = np.stack([np.linalg.norm(G[:, 1] - G[:, 0], axis=1), np.linalg.norm(G[:, 2] - G[:, 1], axis=1), np.linalg.norm(G[:, 0] - G[:, 2], axis=1)], 1).max(1)
    cen = P.mean(1)[:, [0, 2]]
    cl = ctx.constraint_linien()
    lines = [LineString(pl) for pl, *_ in cl]
    tree = STRtree(lines)
    ii, jj = tree.query(points(cen), predicate='dwithin', distance=S['q9_band_breite_m'])
    im_band = np.zeros(len(T), bool); im_band[ii] = True
    ml = [LineString(pl) for pl, _ in _mittellinien(ctx)]
    fern = np.zeros(len(T), bool)
    if ml:
        tw = STRtree(ml); near = np.zeros(len(T), bool)
        a, _ = tw.query(points(cen), predicate='dwithin', distance=S['q9_fern_ab_weg_m']); near[a] = True; fern = ~near
    f = S['q9_diagonal_faktor']
    grenze = np.where(im_band, S['q9_band_abstand_m'] * f, np.where(fern, S['q9_fern_abstand_m'] * f, S['q9_begehbar_abstand_m'] * f))
    begehbar = np.isin(n['klasse'], ['grund', 'weg', 'ufer', 'bruecke'])
    zu_lang = np.nonzero(begehbar & (L > grenze + 1e-6))[0]
    # Min-Winkel (im Grundriss XZ), ausser Dreiecke mit Constraint-Ecke
    w = dreieckswinkel(P[:, :, [0, 2]])
    ecken = []
    for pl, geschl, *_ in cl:
        if not geschl: ecken += [pl[0], pl[-1]]
        if len(pl) > 2:
            v1 = pl[1:-1] - pl[:-2]; v2 = pl[2:] - pl[1:-1]
            c = (v1 * v2).sum(1) / (np.hypot(*v1.T) * np.hypot(*v2.T) + 1e-15)
            ecken += list(pl[1:-1][c < np.cos(np.radians(10))])
    # Schnittpunkte Linie x Linie und Linie x Kachelschnitt sind ebenfalls Constraint-Ecken
    from shapely import box
    kb = [box(*kd['bounds']).boundary for kd in ctx.kacheln.values()]
    allel = lines + kb
    tr2 = STRtree(allel)
    a, b = tr2.query(allel, predicate='intersects')
    for i, j in zip(a, b):
        if i < j and (i < len(lines) or j < len(lines)):
            x = allel[i].intersection(allel[j])
            for gg in getattr(x, 'geoms', [x]):
                if gg.geom_type == 'Point': ecken.append([gg.x, gg.y])
    ecken = np.array(ecken) if ecken else np.zeros((0, 2))
    ausnahme = np.zeros(len(T), bool)
    if len(ecken):
        from scipy.spatial import cKDTree
        kd = cKDTree(ecken)
        for k in range(3):
            d, _ = kd.query(P[:, k][:, [0, 2]]); ausnahme |= d < 1e-3
    spitz = np.nonzero((w < S['q9_min_winkel']) & ~ausnahme & begehbar)[0]
    kz = {}
    for kid in ctx.kacheln:
        kz[kid] = int(sum(len(p['idx']) for p in ctx.kacheln[kid]['prims'] if p['art'] in ('gelaende', 'wasser', 'wand')))
    gesamt = sum(kz.values())
    ueber = {k: v for k, v in kz.items() if v > S['q9_dreiecke_kachel']}
    bef = [{'art': 'normale_unten', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2)} for i in unten[:10]]
    bef += [{'art': 'entartet', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2)} for i in entartet[:5]]
    bef += [{'art': 'kante_zu_lang', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2), 'kante_m': _r(L[i]), 'grenze_m': _r(grenze[i])} for i in zu_lang[np.argsort(-L[zu_lang])][:10]]
    bef += [{'art': 'winkel<20', 'x': _r(cen[i, 0], 2), 'z': _r(cen[i, 1], 2), 'winkel_grad': _r(w[i], 1)} for i in spitz[np.argsort(w[spitz])][:10]]
    bef += [{'art': 'budget_kachel', 'kachel': k, 'dreiecke': v} for k, v in ueber.items()]
    if gesamt > S['q9_dreiecke_gesamt']: bef.append({'art': 'budget_gesamt', 'dreiecke': gesamt})
    return erg('Q9', not bef, {'dreiecke_gesamt': gesamt, 'dreiecke_max_kachel': max(kz.values()), 'normale_unten': int(len(unten)),
                               'entartet': int(len(entartet)), 'kante_zu_lang': int(len(zu_lang)), 'min_winkel_grad': _r(float(w[~ausnahme & begehbar].min()) if (~ausnahme & begehbar).any() else 0, 2),
                               'winkel_unter_20': int(len(spitz)), 'constraint_ecken': int(len(ecken)),
                               'kante_max_band_m': _r(L[im_band & begehbar].max() if (im_band & begehbar).any() else 0),
                               'kante_max_begehbar_m': _r(L[~im_band & ~fern & begehbar].max() if (~im_band & ~fern & begehbar).any() else 0)}, bef,
               'Kantenschwelle = Punktabstand x sqrt2 (+1 %) (Annahme, offene Frage); Band = Schwerpunkt <= 1,5 m von Constraint-Linie; fern = > 30 m von Weg-Mittellinien -> 1,0 m.')


# ------------------------------------------------------------------ Q10
def q10(ctx):
    S = ctx.k['schwellen']; W, H = ctx.k['welt_m']
    n = ctx.netz(('gelaende',)); V, T = n['V'], n['T']; P = V[T]
    if n['uv0'] is None or n['uv1'] is None: raise Fehlt('TEXCOORD_0/1 fehlen in mindestens einem Primitive')
    u0 = n['uv0']; u1 = n['uv1']
    def sflaeche(Q):
        a = Q[:, 1] - Q[:, 0]; b = Q[:, 2] - Q[:, 0]; return (a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]) / 2
    axz = sflaeche(P[:, :, [0, 2]]); a0 = sflaeche(u0); a1 = sflaeche(u1)
    gross = np.abs(axz) > 1e-9
    gesp0 = np.nonzero(gross & (np.sign(a0) != np.sign(axz)))[0]
    gesp1 = np.nonzero(gross & (np.sign(a1) != np.sign(axz)))[0]
    soll1 = np.stack([P[:, :, 0] / W, P[:, :, 2] / H], -1)
    abw1 = np.abs(u1 - soll1).max((1, 2)); uv1_falsch = np.nonzero(abw1 > 1e-5)[0]
    a3 = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1) / 2
    nrm = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); neig = np.degrees(np.arccos(np.clip(np.abs(nrm[:, 1]) / (np.linalg.norm(nrm, axis=1) + 1e-15), 0, 1)))
    verz = np.abs(1 - np.abs(a0) / (a3 + 1e-15))
    bis = (neig <= S['q10_bis_grad']) & (a3 > 1e-9)
    zu = np.nonzero(bis & (verz > S['q10_verzerrung']))[0]
    w = {'gespiegelt_uv0': int(len(gesp0)), 'gespiegelt_uv1': int(len(gesp1)), 'uv1_abweichend': int(len(uv1_falsch)),
         'verzerrung_max_bis35': _r(float(verz[bis].max()) if bis.any() else 0), 'verzerrung_ueber_10pct': int(len(zu)),
         'max_neigung_grad': _r(float(neig.max()), 1)}
    bef = [{'art': 'uv0_gespiegelt', 'x': _r(P[i, :, 0].mean(), 2), 'z': _r(P[i, :, 2].mean(), 2)} for i in gesp0[:10]]
    bef += [{'art': 'uv1_gespiegelt', 'x': _r(P[i, :, 0].mean(), 2), 'z': _r(P[i, :, 2].mean(), 2)} for i in gesp1[:5]]
    bef += [{'art': 'uv1_nicht_(x/336,z/303)', 'x': _r(P[i, :, 0].mean(), 2), 'z': _r(P[i, :, 2].mean(), 2), 'abw': _r(abw1[i], 6)} for i in uv1_falsch[:5]]
    bef += [{'art': 'verzerrung', 'x': _r(P[i, :, 0].mean(), 2), 'z': _r(P[i, :, 2].mean(), 2), 'verz': _r(verz[i]), 'neigung_grad': _r(neig[i], 1)} for i in zu[np.argsort(-verz[zu])][:10]]
    # Waende: Box-UV
    try:
        nw = ctx.netz(('wand',), modelle=False)
        if nw['uv0'] is not None:
            Pw = nw['V'][nw['T']]; aw3 = np.linalg.norm(np.cross(Pw[:, 1] - Pw[:, 0], Pw[:, 2] - Pw[:, 0]), axis=1) / 2
            vw = np.abs(1 - np.abs(sflaeche(nw['uv0'])) / (aw3 + 1e-15)); w['wand_verzerrung_max'] = _r(float(vw.max()))
            for i in np.nonzero(vw > S['q10_wand'])[0][:5]: bef.append({'art': 'wand_verzerrung', 'verz': _r(vw[i])})
        else: w['wand'] = 'ohne UV0'
    except Fehlt:
        w['wand'] = 'keine Wandmeshes in Kacheln (P5 offen)'
    return erg('Q10', not bef, w, bef,
               'Spiegelung = Vorzeichen UV- vs. XZ-Flaeche; UV1 = (x/336, z/303) +-1e-5; Verzerrung = |1 - Flaeche_UV0/Flaeche_3D| (woertlich; bei UV0 = Welt-XZ ab 25,8 Grad > 10 % -> offene Frage).')
