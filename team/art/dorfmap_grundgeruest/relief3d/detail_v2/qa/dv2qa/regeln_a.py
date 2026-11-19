"""Q1-Q5 (Topologie/Loecher, Constraint-Treue, Glaette, Kreuzungen, Dellen)."""
import numpy as np
from .geom import Ortung, abtasten, glaettung_abw, kanten_von, form_abw
from .welt import Fehlt


def erg(regel, ok, werte, befunde=(), notiz=''):
    b = list(befunde)
    return {'regel': regel, 'status': 'ok' if ok else 'fehler', 'werte': werte, 'befunde_anzahl': len(b), 'befunde': b[:40], 'notiz': notiz}


def _r(v, n=4):
    return None if v is None or (isinstance(v, float) and np.isnan(v)) else round(float(v), n)


# ------------------------------------------------------------------ Q1
def q1(ctx):
    S = ctx.k['schwellen']
    n = ctx.netz(('gelaende',))
    V, T = n['V'], n['T']
    mf = ctx.manifest_fehler()
    e = kanten_von(T)
    u, cnt = np.unique(e, axis=0, return_counts=True)
    mehr = u[cnt > 2]
    rand = u[cnt == 1]
    # erlaubter Rand = Aussenrand der Vereinigung aller Manifest-Kacheln
    B = np.array([kd['bounds'] for kd in ctx.kacheln.values()], float)
    from shapely import box, union_all, distance, points
    rand_u = union_all([box(*b) for b in B]).boundary
    def auf_aussenrand(p):
        return distance(points(p), rand_u) < 1e-4
    mid = (V[rand[:, 0]][:, [0, 2]] + V[rand[:, 1]][:, [0, 2]]) / 2
    innen_rand = rand[~auf_aussenrand(mid)] if len(rand) else rand
    # Kachelschnitt bitgleich: Vertices je Kachel auf gemeinsamen Schnittlinien vergleichen
    naht = []
    ids = list(ctx.kacheln)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            ax0, az0, ax1, az1 = ctx.kacheln[a]['bounds']; bx0, bz0, bx1, bz1 = ctx.kacheln[b]['bounds']
            if ax1 == bx0 or bx1 == ax0: achse, wert, lo, hi = 0, (ax1 if ax1 == bx0 else ax0), max(az0, bz0), min(az1, bz1)
            elif az1 == bz0 or bz1 == az0: achse, wert, lo, hi = 1, (az1 if az1 == bz0 else az0), max(ax0, bx0), min(ax1, bx1)
            else: continue
            if hi <= lo: continue
            def mengen(kid):
                s = set()
                for p in ctx.kacheln[kid]['prims']:
                    if p['art'] != 'gelaende': continue
                    P = p['pos32']
                    m = (P[:, achse] == np.float32(wert)) & (P[:, 2 - 2 * achse] >= lo) & (P[:, 2 - 2 * achse] <= hi)
                    s |= {r.tobytes() for r in P[m]}
                return s
            sa, sb = mengen(a), mengen(b)
            if sa != sb:
                d = sa ^ sb
                naht.append({'kacheln': f'{a}|{b}', 'abweichend': len(d), 'je_seite': [len(sa), len(sb)]})
    # Strahl-Lochscan
    loch = _strahlscan(ctx, n)
    befunde = [{'art': 'kante>2', 'x': _r(V[k[0], 0], 2), 'z': _r(V[k[0], 2], 2)} for k in mehr[:10]]
    befunde += [{'art': 'innenrand', 'x': _r(V[k[0], 0], 2), 'z': _r(V[k[0], 2], 2)} for k in innen_rand[:10]]
    befunde += [{'art': 'naht', **x} for x in naht]
    befunde += [{'art': 'loch_strahl', **x} for x in loch['befunde'][:10]]
    befunde += [{'art': 'manifest', 'fehler': x} for x in mf]
    if n['gemischt']: befunde.append({'art': 'gemischte_dreiecke', 'anzahl': n['gemischt']})
    ok = len(mehr) == 0 and len(innen_rand) == 0 and not naht and loch['loecher'] == 0 and not mf and n['gemischt'] == 0
    return erg('Q1', ok, {'kanten': int(len(u)), 'vertices_roh': int(len(n['P_roh'])), 'duplikate_verschweisst': n['duplikate'],
                          'gemischte_dreiecke': n['gemischt'], 'manifest_fehler': len(mf), 'kanten_mehr_als_2': int(len(mehr)), 'randkanten_innen': int(len(innen_rand)),
                          'naht_abweichend': len(naht), 'strahlen': loch['strahlen'], 'strahl_loecher': loch['loecher'],
                          'orte_gescannt': loch['orte']}, befunde,
               'Verschweissen nach Position (Toleranz 0,1 mm; duplizierte Klassengrenz-Vertices gelten als verbunden); Randkanten nur am Aussenrand der Manifest-Kacheln; Naht = float32-bitgleiche Vertexmengen je Kachelschnitt; Manifest-Schema und Klassenreinheit (Entscheidung Grundgeruest 19.11.).')


def _strahlscan(ctx, n):
    """360 Azimute x 14 Neigungen je Ort/Augenhoehe; Schritt 5 cm; Loch = unbedecktes Kartenstueck, an dem der Strahl
    unter die zuletzt gesehene Gelaendehoehe faellt (= man saehe durchs Netz)."""
    try:
        o = ctx.ortung(('gelaende',), modelle=True)
    except Fehlt:
        o = ctx.ortung(('gelaende',))
    B = np.array([kd['bounds'] for kd in ctx.kacheln.values()], float)
    def in_karte(x, z):
        r = np.zeros(len(x), bool)
        for x0, z0, x1, z1 in B: r |= (x >= x0) & (x <= x1) & (z >= z0) & (z <= z1)
        return r
    orte = {k: v for k, v in ctx.k['orte'].items() if in_karte(np.array([v[0]]), np.array([v[1]]))[0]}
    dist = np.geomspace(1.0, 60.0, 14)
    az = np.radians(np.arange(360))
    gesamt, loecher, bef = 0, 0, []
    for name, (ox, oz) in orte.items():
        h0, _ = o.hoehe(np.array([ox]), np.array([oz]))
        if np.isnan(h0[0]): continue
        for aug in ctx.k['q1_augenhoehen']:
            ey = h0[0] + aug
            for d in dist:
                el = aug / d                                   # tan(Neigung): trifft flaches Gelaende in Distanz d
                smax = d * 1.5
                s = np.arange(0.05, smax, 0.05)
                X = ox + np.cos(az)[:, None] * s[None]; Z = oz + np.sin(az)[:, None] * s[None]
                Y = ey - el * s[None]
                h, t = o.hoehe(X.ravel(), Z.ravel()); h = h.reshape(X.shape); bedeckt = ~np.isnan(h)
                ink = in_karte(X.ravel(), Z.ravel()).reshape(X.shape)
                hl = np.where(bedeckt, h, np.nan)
                # zuletzt gesehene Hoehe vorwaerts fuellen
                idx = np.where(bedeckt, np.arange(len(s))[None], 0); np.maximum.accumulate(idx, axis=1, out=idx)
                last = np.take_along_axis(np.where(bedeckt, h, -np.inf), idx, 1)
                treffer = bedeckt & (Y <= hl)
                erst = np.where(treffer.any(1), treffer.argmax(1), len(s))
                vor = np.arange(len(s))[None] < erst[:, None]
                lo = (~bedeckt) & ink & vor & (Y <= last)
                gesamt += len(az)
                k = lo.any(1)
                if k.any():
                    loecher += int(k.sum())
                    for i in np.nonzero(k)[0][:3]:
                        j = lo[i].argmax(); bef.append({'ort': name, 'auge_m': aug, 'az_grad': int(i), 'x': round(float(X[i, j]), 2), 'z': round(float(Z[i, j]), 2)})
    return {'strahlen': gesamt, 'loecher': loecher, 'befunde': bef, 'orte': list(orte)}


# ------------------------------------------------------------------ Q2
def q2(ctx):
    from shapely import STRtree, linestrings, points, LineString
    S = ctx.k['schwellen']; thr = S['q2_hausdorff_m']
    n = ctx.netz(('gelaende',)); V, T = n['V'], n['T']
    e = np.unique(kanten_von(T), axis=0)
    A = V[e[:, 0]][:, [0, 2]]; Bp = V[e[:, 1]][:, [0, 2]]
    segs = linestrings(np.stack([A, Bp], 1))
    tree = STRtree(segs)
    dvec = Bp - A; dl = np.hypot(*dvec.T) + 1e-15
    worst, bef, n_lin = 0.0, [], 0
    for pl, geschl, pr, datei in ctx.constraint_linien():
        n_lin += 1
        s = abtasten(pl, 0.05)
        L = LineString(pl)
        # Richtung je Abtastpunkt
        dfw = np.diff(s, axis=0); dfw /= np.hypot(*dfw.T)[:, None] + 1e-15
        tf = np.vstack([dfw, dfw[-1:]]); tb = np.vstack([dfw[:1], dfw])          # Richtung vor/nach dem Abtastpunkt
        # Mesh-Kanten nahe der Linie (<= 0.1 m) und parallel (< 20 Grad)
        ii, jj = tree.query(points(s), predicate='dwithin', distance=0.1)
        ev = dvec[jj] / dl[jj, None]; cw = np.cos(np.radians(20))
        par = (np.abs((ev * tf[ii]).sum(1)) > cw) | (np.abs((ev * tb[ii]).sum(1)) > cw)
        ii, jj = ii[par], jj[par]
        from shapely import distance
        dmin = np.full(len(s), np.inf)
        if len(ii):
            dd = distance(points(s[ii]), segs[jj]); np.minimum.at(dmin, ii, dd)
        # Gegenrichtung: Endpunkte der zugeordneten Kanten -> Linie
        uj = np.unique(jj)                                      # Kanten, die die Linie darstellen: beide Enden <= 0,1 m
        if len(uj):
            de = distance(points(np.vstack([A[uj], Bp[uj]])), L).reshape(2, -1).max(0); uj = uj[de <= 0.1]
        d2 = distance(points(np.vstack([A[uj], Bp[uj]])), L) if len(uj) else np.zeros(1)
        h = max(float(dmin.max()), float(d2.max()))
        if h > worst: worst = h
        if h > thr:
            k = int(np.argmax(dmin))
            bef.append({'datei': datei, 'id': pr.get('id'), 'hausdorff_m': _r(min(h, 9.99)), 'x': _r(s[k, 0], 2), 'z': _r(s[k, 1], 2)})
    return erg('Q2', not bef, {'linien': n_lin, 'hausdorff_max_m': _r(min(worst, 9.99)), 'schwelle_m': thr}, bef,
               'Je Linie: Abtastpunkte 5 cm -> naechste parallele Mesh-Kante (<=0,1 m, <20 Grad) und zurueck; fehlende Kante = 9,99.')


# ------------------------------------------------------------------ Q3
def q3(ctx):
    """Glaette (Entscheidung QA/Grundgeruest 19.11. Runde 3): jede Linie - Vektorquellen und Mesh-Kantenzuege gleich -
    zuerst gleichmaessig auf q3_abtastung_m (0,05 m) nach Bogenlaenge neu abgetastet, dann gleitendes q3_fenster_m-Mittel;
    Abweichung <= 3 cm hart fuer alle Linien; Knick <= 15 Grad ausser in Kreuzungspolygonen (R8/Q4 gilt dort)."""
    from shapely import union_all, contains_xy
    S = ctx.k['schwellen']; h, fen = S['q3_abtastung_m'], S['q3_fenster_m']
    kz = [g for g, _ in ctx.polygone(ctx.k['kreuzungen']['datei'], pflicht=False)]
    kreuz = union_all([g.buffer(0.05) for g in kz]) if kz else None
    w = {'linien': 0, 'abw_max_m': 0.0, 'knick_max_grad': 0.0, 'mesh_kantenzuege': 0, 'mesh_abw_max_m': 0.0, 'mesh_knick_max_grad': 0.0}
    bef = []
    zk = ctx.k.get('q3_zonen', {})
    from shapely import box
    karte_rand = box(0, 0, *ctx.k['welt_m']).boundary
    def pruefe(pl, geschl, quelle, pid, mesh=False, zone=None):
        R, abw, knick = form_abw(pl, fen, geschl, h)
        if kreuz is not None and len(R): knick = np.where(contains_xy(kreuz, R[:, 0], R[:, 1]), 0, knick)
        gruppe = None
        if zone is not None and len(R):                         # F11: Kartenrand + Stossfenster ausgenommen, sonst hart
            aus, gruppe = zonen_maske(R, pl, geschl, zone, karte_rand, zk)
            abw = np.where(aus, 0, abw); knick = np.where(aus, 0, knick); w['zonen_ausgenommen_punkte'] += int(aus.sum())
        a = float(abw.max()) if len(abw) else 0.0; k = float(knick.max()) if len(knick) else 0.0
        pre = 'mesh_' if mesh else ''
        w[pre + 'abw_max_m'] = max(w[pre + 'abw_max_m'], a); w[pre + 'knick_max_grad'] = max(w[pre + 'knick_max_grad'], k)
        if a > S['q3_glatt_m'] or k > S['q3_knick_grad']:
            i = int(np.argmax(abw)) if a > S['q3_glatt_m'] else int(np.argmax(knick))
            b = {'datei': quelle, 'id': pid, 'quelle': 'mesh' if mesh else 'vektor', 'abw_m': _r(a), 'knick_grad': _r(k, 1), 'x': _r(R[i, 0], 2), 'z': _r(R[i, 1], 2)}
            if gruppe is not None:
                ub = (abw > S['q3_glatt_m']) | (knick > S['q3_knick_grad'])
                b['gruppe'] = str(gruppe[i]); b['gruppen_punkte'] = {g: int((ub & (gruppe == g)).sum()) for g in np.unique(gruppe[ub])}
            bef.append(b)
    linien = []
    zonen_q = [q for q in ctx.k['q3_quellen'] if q.get('zonenringe')]
    zringe = [(pl, g, pr) for q in zonen_q for pl, g, pr in ctx.linien(q)]
    stoss = zonen_stosspunkte(zringe, zk) if zringe else []
    w['zonen_stosspunkte_anzahl'] = len(stoss); w['zonen_stosspunkte_ausgenommen'] = sum(1 for x in stoss if x['ausgenommen'])
    w['zonen_ausgenommen_punkte'] = 0
    for q in ctx.k['q3_quellen']:
        for pl, geschl, pr in ctx.linien(q):
            w['linien'] += 1; linien.append((pl, geschl, q['datei'], pr.get('id')))
            pruefe(pl, geschl, q['datei'], pr.get('id'), zone=({'stoss': stoss, 'pr': pr} if q.get('zonenringe') else None))
    # Mesh-Kantenzuege: Mesh-Vertices <= 2 cm an der Linie, nach Bogenlaenge der Linie geordnet -> dieselbe Messung
    try:
        n = ctx.netz(('gelaende',)); V = n['V'][:, [0, 2]]
    except Fehlt:
        n = None; w['mesh_kantenzuege'] = 'offen (kein Mesh)'
    if n is not None and linien:
        from shapely import STRtree, points, LineString
        pts = points(V); tree = STRtree(pts)
        for pl, geschl, quelle, pid in linien:
            L = LineString(pl)
            idx = tree.query(L, predicate='dwithin', distance=S['q2_hausdorff_m'])
            if len(idx) < 5: continue
            from shapely import line_locate_point
            t = line_locate_point(L, pts[idx])
            o = np.argsort(t); kette = V[idx[o]]
            kette = kette[np.r_[True, np.hypot(*np.diff(kette, axis=0).T) > 1e-6]]
            if len(kette) < 3: continue
            w['mesh_kantenzuege'] += 1; pruefe(kette, geschl, quelle, pid, mesh=True)
    w = {k: _r(v) if isinstance(v, float) else v for k, v in w.items()}
    w['schwellen'] = {'abw_m': S['q3_glatt_m'], 'knick_grad': S['q3_knick_grad'], 'abtastung_m': h, 'fenster_m': fen}
    w['grat_silhouette'] = 'Sa per Bild (Q13)'
    zb = [b for b in bef if 'gruppe' in b]
    w['zonen_rest'] = {'ringe': len(zb), 'ringe_je_gruppe': {g: sum(1 for b in zb if b['gruppe'] == g) for g in sorted({b['gruppe'] for b in zb})},
                       'punkte_je_gruppe': {g: sum(b['gruppen_punkte'].get(g, 0) for b in zb) for g in sorted({k for b in zb for k in b['gruppen_punkte']})}}
    w['zonen_stosspunkte'] = stoss
    w['zonen_regel'] = ('F11 (Grundgeruest 19.11.): Zonenringe layer=flaechentyp - ausgenommen NUR Abschnitte auf dem Kartenrand (inkl. Ecken, Toleranz '
                        f"{zk.get('kartenrand_tol_m')} m) und +-{zk.get('stoss_fenster_m')} m Bogenlaenge um Stosspunkte mit >= 3 Zonen; Stosspunkte mit "
                        f"{zk.get('hart_typen')} (Brueckenrechteck, Platzhalter P5) bleiben hart. Sichtpruefung 1,7 m Pflicht (zackiger Stosspunkt = Befund).")
    return erg('Q3', not bef, w, bef,
               'Neuabtastung 0,05 m nach Bogenlaenge (lin. Interpolation, Endpunkte bleiben), gleitendes 1-m-Mittel, Abstand Abtastpunkt -> gemittelte Linie <= 3 cm hart fuer alle Linien '
               '(Vektor und Mesh-Kantenzug = Mesh-Vertices <= 2 cm an der Linie); Knick <= 15 Grad (Sehnen vor/nach dem Punkt), in Kreuzungspolygonen ausgenommen (Q4/R8 gilt dort).')


def zonen_stosspunkte(ringe, zk):
    """Stosspunkte der Zonenringe: Ringstuetzpunkte, an denen >= 3 verschiedene Zonen (Polygon-id) innerhalb stoss_tol_m
    zusammenstossen; benachbarte Kandidaten (< 0,05 m) zu einem Punkt zusammengefasst.
    -> [{'x', 'z', 'zonen': [id], 'typen': [typ], 'ausgenommen': bool}] (hart, wenn ein Typ in hart_typen)."""
    from shapely import STRtree, points, LineString
    from scipy.spatial import cKDTree
    tol = zk.get('stoss_tol_m', 0.01); hart = set(zk.get('hart_typen', []))
    je = {}
    for pl, g, pr in ringe: je.setdefault(pr.get('id'), [pr, []])[1].append(pl)
    ids = list(je); typ = {i: je[i][0].get('typ') for i in ids}
    geoms, gz = [], []                                          # Ringe in Stuecke zu 32 Segmenten (schnelle Baumabfrage)
    for n, i in enumerate(ids):
        for pl in je[i][1]:
            r = np.vstack([pl, pl[:1]])
            for s in range(0, len(r) - 1, 32):
                geoms.append(LineString(r[s:s + 33])); gz.append(n)
    gz = np.array(gz)
    P = np.unique(np.round(np.vstack([pl for pl, _, _ in ringe]), 4), axis=0)
    a, b = STRtree(geoms).query(points(P), predicate='dwithin', distance=tol)
    if not len(a): return []
    ab = np.unique(np.c_[a, gz[b]], axis=0); a, b = ab[:, 0], ab[:, 1]
    cnt = np.bincount(a, minlength=len(P))                     # a/b eindeutig je (Punkt, Zone)
    kand = np.nonzero(cnt >= 3)[0]
    if not len(kand): return []
    zon = {i: set() for i in kand}
    for i, j in zip(a, b):
        if i in zon: zon[i].add(ids[j])
    par = np.arange(len(kand)); pos = {k: n for n, k in enumerate(kand)}
    for x, y in cKDTree(P[kand]).query_pairs(0.05):
        rx, ry = x, y
        while par[rx] != rx: rx = par[rx]
        while par[ry] != ry: ry = par[ry]
        par[max(rx, ry)] = min(rx, ry)
    grp = {}
    for n in range(len(kand)):
        r = n
        while par[r] != r: r = par[r]
        grp.setdefault(r, []).append(kand[n])
    out = []
    for g in grp.values():
        z = sorted(set().union(*[zon[i] for i in g]), key=str); c = P[g].mean(0); t = sorted({str(typ[i]) for i in z})
        out.append({'x': _r(c[0], 3), 'z': _r(c[1], 3), 'zonen': z, 'typen': t, 'ausgenommen': not (set(t) & hart)})
    return sorted(out, key=lambda d: (d['x'], d['z']))


def zonen_maske(R, pl, geschl, zone, karte_rand, zk):
    """-> (ausgenommen[n], gruppe[n]) fuer die Abtastpunkte R eines Zonenrings (F11).
    ausgenommen: auf dem Kartenrand (<= kartenrand_tol_m) oder <= stoss_fenster_m Bogenlaenge um einen ausgenommenen Stosspunkt.
    gruppe (fuer den Bericht): kartenrand | stossfenster | kartenrand_nah (<= 1 m) | bruecke (Ring einer Bruecken-Zone oder
    <= 1 m um einen harten Stosspunkt) | stoss_nah (<= 1 m um Stosspunkt) | sonst."""
    from shapely import points, distance, LineString, line_locate_point
    tol = zk.get('kartenrand_tol_m', 0.01); fen = zk.get('stoss_fenster_m', 0.5); stol = zk.get('stoss_tol_m', 0.01)
    hart = set(zk.get('hart_typen', []))
    dr = distance(points(R), karte_rand); rand = dr <= tol
    ring = np.vstack([pl, pl[:1]]) if geschl and not np.allclose(pl[0], pl[-1]) else pl
    L = LineString(ring); Lt = L.length
    # R (neu_abtasten) startet an pl[0] und ist gleichmaessig nach Bogenlaenge abgetastet
    sR = np.arange(len(R)) * (Lt / len(R)) if geschl else np.linspace(0, Lt, len(R))
    fenster = np.zeros(len(R), bool); nah_ok = np.zeros(len(R), bool); nah_hart = np.zeros(len(R), bool)
    st = zone['stoss']
    if st:
        S = np.array([[d['x'], d['z']] for d in st]); dS = distance(points(S), L)
        for d, p in zip(np.array(st)[dS <= stol + 1e-3], S[dS <= stol + 1e-3]):
            sj = float(line_locate_point(L, points(p)))
            ds = np.abs(sR - sj)
            if geschl: ds = np.minimum(ds, Lt - ds)
            if d['ausgenommen']: fenster |= ds <= fen + 1e-9; nah_ok |= ds <= 1.0
            else: nah_hart |= ds <= 1.0
    aus = rand | fenster
    br = str(zone['pr'].get('typ')) in hart
    gruppe = np.full(len(R), 'sonst', dtype=object)
    gruppe[nah_ok & ~aus] = 'stoss_nah'
    gruppe[(nah_hart | br) & ~aus] = 'bruecke'
    gruppe[(dr <= 1.0) & ~aus] = 'kartenrand_nah'
    gruppe[fenster] = 'stossfenster'; gruppe[rand] = 'kartenrand'
    return aus, gruppe


# ------------------------------------------------------------------ Q4
def q4(ctx):
    from shapely import contains_xy
    S = ctx.k['schwellen']; o = ctx.ortung(('gelaende',))
    n = ctx.netz(('gelaende',)); V = n['V']
    bef, worst_g, worst_r, anz, je_art = [], 0.0, 0.0, 0, {}
    for g, pr in ctx.polygone(ctx.k['kreuzungen']['datei']):
        anz += 1; je_art[str(pr.get('art'))] = je_art.get(str(pr.get('art')), 0) + 1
        m = contains_xy(g, V[:, 0], V[:, 2]); P = V[m]
        x0, z0, x1, z1 = g.bounds
        gx, gz = np.meshgrid(np.arange(x0, x1, 0.1), np.arange(z0, z1, 0.1))
        mm = contains_xy(g, gx, gz); gx, gz = gx[mm], gz[mm]
        h, _ = o.hoehe(gx, gz); ok = ~np.isnan(h)
        X = np.r_[P[:, 0], gx[ok]]; Z = np.r_[P[:, 2], gz[ok]]; H = np.r_[P[:, 1], h[ok]]
        if len(X) < 3: bef.append({'id': pr.get('id'), 'fehler': 'keine Messpunkte'}); continue
        A = np.c_[X, Z, np.ones_like(X)]; c, *_ = np.linalg.lstsq(A, H, rcond=None)
        gef = float(np.hypot(c[0], c[1])); rest = float(np.abs(H - A @ c).max())
        worst_g = max(worst_g, gef); worst_r = max(worst_r, rest)
        if gef > S['q4_gefaelle'] or rest > S['q4_rest_m']:
            c0 = g.centroid
            bef.append({'id': pr.get('id'), 'art': pr.get('art'), 'gefaelle': _r(gef), 'rest_m': _r(rest), 'x': _r(c0.x, 2), 'z': _r(c0.y, 2)})
    return erg('Q4', not bef and anz > 0, {'kreuzungen': anz, 'je_art': je_art, 'gefaelle_max': _r(worst_g), 'rest_max_m': _r(worst_r),
                                           'schwellen': [S['q4_gefaelle'], S['q4_rest_m']]}, bef,
               'Ebenen-Fit ueber Mesh-Vertices + 0,1-m-Abtastung im Kreuzungspolygon.')


# ------------------------------------------------------------------ Q5
def _mittellinien(ctx):
    q = ctx.k['mittellinien']
    return [(pl, pr) for pl, _, pr in ctx.linien({'datei': q['datei'], 'filter': q['filter']})]


def q5(ctx):
    from scipy.ndimage import minimum_filter
    from shapely import LineString, union_all, contains_xy
    S = ctx.k['schwellen']; o = ctx.ortung(('gelaende',))
    bp = ctx.k['mittellinien']['breite_prop']
    ml = _mittellinien(ctx)
    nq = ctx.k.get('wegnetz')
    netz = [g for g, _ in ctx.polygone(nq['datei'], nq.get('filter'), pflicht=False)] if nq else []
    weg = union_all(netz) if netz else union_all([LineString(pl).buffer(float(pr.get(bp, 2.0)) / 2, cap_style='flat') for pl, pr in ml])
    band = weg.buffer(S['q5_band_m']).difference(weg)
    wasser = union_all([g for g, _ in ctx.polygone(ctx.k['wasser']['datei'], pflicht=False)] or [LineString([(0, 0), (0, 0.001)]).buffer(0)])
    bef, worst, n_ges = [], 0.0, 0
    r = S['q5_radius_m']; ring = np.linspace(0, 2 * np.pi, 48, endpoint=False)
    x0, z0, x1, z1 = band.bounds
    for bx in np.arange(np.floor(x0), x1, 40):
        for bz in np.arange(np.floor(z0), z1, 40):
            gx, gz = np.meshgrid(np.arange(bx - 1.2, bx + 41.2, 0.1), np.arange(bz - 1.2, bz + 41.2, 0.1))
            h, _ = o.hoehe(gx.ravel(), gz.ravel()); h = h.reshape(gx.shape)
            hf = np.where(np.isnan(h), np.inf, h)
            lokmin = (hf == minimum_filter(hf, size=7, mode='nearest')) & np.isfinite(hf)
            inb = contains_xy(band, gx, gz) & ~contains_xy(wasser, gx, gz) & (gx >= bx) & (gx < bx + 40) & (gz >= bz) & (gz < bz + 40)
            cand = np.nonzero(lokmin & inb)
            if len(cand[0]) == 0: continue
            cx, cz, ch = gx[cand], gz[cand], h[cand]
            rx = cx[:, None] + r * np.cos(ring)[None]; rz = cz[:, None] + r * np.sin(ring)[None]
            rh, _ = o.hoehe(rx.ravel(), rz.ravel()); rh = rh.reshape(rx.shape)
            tiefe = np.nanmin(rh, 1) - ch                          # >0: rundum hoeher = Senke
            n_ges += len(ch)
            m = tiefe > S['q5_delle_m']
            if len(tiefe): worst = max(worst, float(np.nanmax(tiefe)))
            for i in np.nonzero(m)[0][:5]:
                bef.append({'x': _r(cx[i], 2), 'z': _r(cz[i], 2), 'tiefe_m': _r(tiefe[i])})
    return erg('Q5', not bef, {'kandidaten': n_ges, 'tiefe_max_m': _r(worst), 'schwelle_m': S['q5_delle_m'],
                               'band_m': S['q5_band_m']}, bef,
               'Lokale Minima (0,1-m-Raster, 0,7-m-Fenster) im Band 0-3 m neben der Wegflaeche (wege.geojson rolle=netz, sonst Mittellinie+Breite); Tiefe = tiefster Punkt eines 1-m-Rings minus Minimum; Wasser ausgenommen.')
