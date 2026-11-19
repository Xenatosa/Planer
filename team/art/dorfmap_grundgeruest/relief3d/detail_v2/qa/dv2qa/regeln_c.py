"""Q11-Q14 (Datenschicht/queryPoint, Bruecken, Abnahmebilder, Layout-Treue)."""
import json, subprocess, os, tempfile
from pathlib import Path
import numpy as np
from .geom import KLASSEN
from .regeln_a import erg, _r, _mittellinien
from .welt import Fehlt

NODE_HARNESS = r'''
// Q11-Harness: nutzt die echte Datenschicht (daten/manifest.mjs ladeMesh, daten/query.mjs ladeDatenschicht).
import { pathToFileURL } from 'node:url';
import { readFileSync, writeFileSync } from 'node:fs';
const [, , datenDir, manifestPfad, punkte, aus] = process.argv;
const q = await import(pathToFileURL(datenDir + '/query.mjs').href);
const mm = await import(pathToFileURL(datenDir + '/manifest.mjs').href);
const mesh = await mm.ladeMesh(manifestPfad);
const ds = await q.ladeDatenschicht(datenDir, { gelaende: mesh.gelaende });
const P = JSON.parse(readFileSync(punkte, 'utf8'));
const out = [];
for (const [x, z] of P) { let r; try { r = ds.queryPoint(x, z); r = { ...r, slot: r.slot === null ? null : 1 }; } catch (e) { r = { fehler: String(e) }; } out.push(r); }
let dk = null; try { dk = q.pruefeDreiecksklasse(ds, mesh.gelaende, 10000, 611); dk = { ...dk, beispiele: (dk.beispiele || []).slice(0, 5) }; } catch (e) { dk = { fehler: String(e) }; }
writeFileSync(aus, JSON.stringify({ punkte: out, quellen: ds.quellen(), pruefung: mesh.pruefung, dreiecksklasse: dk }));
'''


def _klasse_name(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool): return KLASSEN[int(v)] if 0 <= int(v) < len(KLASSEN) else str(v)
    return str(v)


def q11(ctx):
    '''Datenschicht vs. Mesh (Entscheidung Grundgeruest 19.11.: query.mjs baueMeshIndex/ladeDatenschicht + manifest.mjs ladeMesh nutzen).'''
    S = ctx.k['schwellen']; d = ctx.wurzel / ctx.k['daten_ordner']
    for f in ('query.mjs', 'manifest.mjs'):
        if not (d / f).exists(): raise Fehlt(f'{d / f} fehlt')
    rng = np.random.default_rng(611)
    B = np.array([kd['bounds'] for kd in ctx.kacheln.values()], float)
    k = rng.integers(0, len(B), S['q11_punkte'])
    P = np.c_[rng.uniform(B[k, 0], B[k, 2]), rng.uniform(B[k, 1], B[k, 3])]
    for br in ctx.k['bruecken'].values():
        m = (P[:, 0] >= br['x'][0] - 1) & (P[:, 0] <= br['x'][1] + 1) & (P[:, 1] >= br['z'][0] - 1) & (P[:, 1] <= br['z'][1] + 1)
        P = P[~m]
    tmp = Path(os.environ.get('DV2QA_TMP', '/tmp/dv2_qa')); tmp.mkdir(parents=True, exist_ok=True)
    hp = tmp / 'q11_harness.mjs'; hp.write_text(NODE_HARNESS)
    pp = tmp / 'q11_punkte.json'; pp.write_text(json.dumps(P.round(4).tolist())); ap = tmp / 'q11_aus.json'
    r = subprocess.run(['node', str(hp), str(d.resolve()), str((ctx.wurzel / ctx.k['mesh_manifest']).resolve()), str(pp), str(ap)],
                       capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        return erg('Q11', False, {'node_exit': r.returncode}, [{'fehler': 'Datenschicht-Harness', 'stderr': r.stderr[-500:]}])
    aus = json.loads(ap.read_text()); res = aus['punkte']
    o = ctx.ortung(('gelaende',)); h, t = o.hoehe(P[:, 0], P[:, 1])
    n = ctx.netz(('gelaende',)); kl = np.where(t >= 0, n['klasse'][np.maximum(t, 0)], '')
    # Wasserspiegel-Modell (Entscheidung 19.11. Runde 2): sichtbare Oberflaeche = Spiegel, wo er ueber dem Bett liegt
    try:
        hw, _ = ctx.wasser_ortung().hoehe(P[:, 0], P[:, 1])
        ueber = ~np.isnan(hw) & (np.isnan(h) | (hw > h)); h = np.where(ueber, hw, h); kl = np.where(ueber, 'wasser', kl)
        spiegel_pkt = int(ueber.sum())
    except Fehlt:
        spiegel_pkt = None
    qh = np.array([x.get('hoehe') if isinstance(x, dict) and x.get('hoehe') is not None else np.nan for x in res], float)
    qf = np.array([_klasse_name(x.get('flaeche')) if isinstance(x, dict) else '' for x in res])
    dh = np.abs(qh - h); gueltig = ~np.isnan(h)
    fehl_h = np.nonzero(gueltig & ~(dh <= S['q11_dh_m'] + 1e-9))[0]
    gleich = float((qf[gueltig] == kl[gueltig]).mean()) if gueltig.any() else 0
    felder = all(isinstance(x, dict) and all(f in x for f in ('hoehe', 'flaeche', 'untergrund', 'begehbar', 'slot', 'kachel')) for x in res)
    td = d / 'test'
    dateien = sorted(str(x) for x in td.rglob('*.test.mjs')) if td.exists() else []
    if dateien:
        tr = subprocess.run(['node', '--test', *dateien], capture_output=True, text=True, timeout=900, cwd=str(d))
        tests_ok = tr.returncode == 0; tests = (tr.stdout + tr.stderr)[-400:]
    else:
        tests_ok, tests = False, 'keine *.test.mjs in daten/test/'
    bef = [{'art': 'hoehe', 'x': _r(P[i, 0], 2), 'z': _r(P[i, 1], 2), 'query_m': _r(qh[i]), 'mesh_m': _r(h[i]), 'dh_m': _r(dh[i])} for i in fehl_h[np.argsort(-np.nan_to_num(dh[fehl_h], nan=9))][:10]]
    if gleich < S['q11_flaeche_anteil']:
        falsch = np.nonzero(gueltig & (qf != kl))[0]
        bef += [{'art': 'flaeche', 'anteil_gleich': _r(gleich, 5)}] + [{'art': 'flaeche_pkt', 'x': _r(P[i, 0], 2), 'z': _r(P[i, 1], 2), 'query': qf[i], 'mesh': kl[i]} for i in falsch[:5]]
    if not felder: bef.append({'art': 'felder', 'fehler': 'queryPoint liefert nicht alle Felder {hoehe, flaeche, untergrund, begehbar, slot, kachel}'})
    if not tests_ok: bef.append({'art': 'node --test', 'ausgabe': tests})
    dk = aus.get('dreiecksklasse') or {}
    return erg('Q11', not bef, {'punkte': int(len(P)), 'dh_max_m': _r(np.nanmax(dh[gueltig]) if gueltig.any() else np.nan), 'ueber_2cm': int(len(fehl_h)),
                                'flaeche_gleich': _r(gleich, 5), 'felder_vollstaendig': felder, 'tests_gruen': tests_ok, 'test_dateien': len(dateien),
                                'quellen': aus.get('quellen'), 'p4_pruefeDreiecksklasse_quote': dk.get('quote'),
                                'p4_gemischte_dreiecke': (aus.get('pruefung') or {}).get('gemischte_dreiecke'), 'punkte_auf_spiegel': spiegel_pkt}, bef,
               'Echte Datenschicht (ladeMesh + ladeDatenschicht) an 10 000 Zufallspunkten (Seed 611), Brueckenfussabdruecke +1 m ausgenommen; Hoehe vs. Python-Ortung (sichtbare Oberflaeche: Gelaende, ueber Wasser der Spiegel); Flaeche vs. _FLAECHE-Klasse; node --test daten/test/*.test.mjs.')


def q12(ctx):
    S = ctx.k['schwellen']; mods = ctx.modelle(); o = ctx.ortung(('gelaende',))
    pflicht = {'bohle': ['bohle'], 'traeger': ['traeger'], 'pfosten': ['pfosten'], 'gelaender': ['gelaender', 'handlauf'], 'auflager': ['widerlager', 'auflager']}
    bef, w = [], {}
    for name, br in ctx.k['bruecken'].items():
        prims = next((v for k, v in mods.items() if k.lower() == br['id'].lower()), None)
        if prims is None:
            bef.append({'bruecke': name, 'fehler': f"manifest.modelle[id={br['id']}] fehlt"}); continue
        teile = {k: [p for p in prims if any(s in p['teil'] for s in v)] for k, v in pflicht.items()}
        fehlt = [k for k, v in teile.items() if not v]
        ww = {'teile': {k: len(v) for k, v in teile.items()}}
        if fehlt: bef.append({'bruecke': name, 'fehlende_teile': fehlt})
        if teile['auflager']:
            A = np.vstack([p['pos'] for p in teile['auflager']])
            unten = A[A[:, 1] <= A[:, 1].min() + 0.05]
            h, _ = o.hoehe(unten[:, 0], unten[:, 2])
            spalt = float(np.nanmax(unten[:, 1] - h)) if (~np.isnan(h)).any() else np.nan
            ww['spalt_max_m'] = _r(max(spalt, 0))
            if not (spalt <= S['q12_spalt_m'] + 1e-6): bef.append({'bruecke': name, 'art': 'spalt auflager', 'spalt_m': _r(spalt)})
        if teile['bohle']:
            D = np.vstack([p['pos'] for p in teile['bohle']])
            c = D[:, [0, 2]].mean(0); u, s, vt = np.linalg.svd(D[:, [0, 2]] - c); ax = vt[0]
            t = (D[:, [0, 2]] - c) @ ax
            stufen = []
            for sg in (-1, 1):
                ende = sg * t.max() if sg > 0 else t.min()
                m = np.abs(t - ende) < 0.3; deck = D[m, 1].max()
                p = c + ax * (ende + sg * 0.15)
                hg, _ = o.hoehe(np.array([p[0]]), np.array([p[1]]))
                stufen.append(float(abs(deck - hg[0])))
            ww['stufe_max_m'] = _r(max(stufen))
            if not max(stufen) <= S['q12_stufe_m'] + 1e-6: bef.append({'bruecke': name, 'art': 'stufe weg-bruecke', 'stufe_m': _r(max(stufen))})
            if teile['gelaender']:
                G = np.vstack([p['pos'] for p in teile['gelaender']]); gh = G[:, 1].max() - D[:, 1].max()
                ww['gelaender_hoehe_m'] = _r(gh)
                if abs(gh - 1.0) > 0.1: bef.append({'bruecke': name, 'art': 'gelaenderhoehe', 'm': _r(gh)})
        w[name] = ww
    return erg('Q12', not bef, w, bef,
               'Teile ueber Knoten-/Meshnamen; Spalt = Auflager-Unterkante minus Gelaende; Stufe = Deckoberkante am Ende vs. Gelaende 15 cm davor; Gelaender 1,0 +- 0,1 m.')


def _jpeg_q(im):
    std = np.array([16, 11, 10, 16, 24, 40, 51, 61, 12, 12, 14, 19, 26, 58, 60, 55, 14, 13, 16, 24, 40, 57, 69, 56, 14, 17, 22, 29, 51, 87, 80, 62,
                    18, 22, 37, 56, 68, 109, 103, 77, 24, 35, 55, 64, 81, 104, 113, 92, 49, 64, 78, 87, 103, 121, 120, 101, 72, 92, 95, 98, 112, 100, 103, 99])
    q = getattr(im, 'quantization', None)
    if not q: return None
    t = np.array(q[0]); best, bq = 1e9, None
    for qq in range(1, 101):
        sc = 5000 / qq if qq < 50 else 200 - 2 * qq
        ref = np.clip((std * sc + 50) // 100, 1, 255)
        e = np.abs(np.sort(ref) - np.sort(t)).sum()
        if e < best: best, bq = e, qq
    return bq


def q13(ctx):
    from PIL import Image
    if ctx.abnahme is None: raise Fehlt('--abnahme nicht angegeben')
    d = ctx.abnahme
    soll = []
    for ort in ctx.k['orte']:
        for h in ctx.k['q13_hoehen']: soll.append(f"{ort}_clay_{('%g' % h).replace('.', ',')}m.jpg")
        soll.append(f'{ort}_wire_5m.jpg')
    bef, qual = [], {}
    quellen = (d / 'QUELLEN.txt').read_text() if (d / 'QUELLEN.txt').exists() else None
    if quellen is None: bef.append({'fehler': 'QUELLEN.txt fehlt'})
    for f in soll:
        p = d / f
        if not p.exists(): bef.append({'datei': f, 'fehler': 'fehlt'}); continue
        try:
            im = Image.open(p)
            if im.format != 'JPEG': bef.append({'datei': f, 'fehler': f'kein JPEG ({im.format})'}); continue
            q = _jpeg_q(im); qual[f] = q
            if q is None or abs(q - 90) > 2: bef.append({'datei': f, 'fehler': f'Qualitaet ~{q} statt 90'})
        except Exception as e:
            bef.append({'datei': f, 'fehler': str(e)[:80]})
        if quellen is not None and f not in quellen: bef.append({'datei': f, 'fehler': 'nicht in QUELLEN.txt'})
    return erg('Q13', not bef, {'soll': len(soll), 'vorhanden': len(qual), 'qualitaet': sorted(set(qual.values()))}, bef,
               'Soll: 5 Orte x Clay 1,7/5/12/30 m + Wire 5 m = 25 JPG q90 (Name <ort>_clay_<h>m.jpg / <ort>_wire_5m.jpg) + QUELLEN.txt mit jedem Dateinamen.')


def _spiegel_flaechen(ctx):
    """-> (Grundrissflaeche Spiegelmodell gesamt, sichtbarer Teil: 0,1-m-Zellmitten mit Spiegel > Gelaende) oder (None, None)."""
    try:
        wo = ctx.wasser_ortung()
    except Fehlt:
        return None, None
    nw = ctx.netz((), 'wasser'); P = nw['V'][nw['T']][:, :, [0, 2]]
    a_ = P[:, 1] - P[:, 0]; b_ = P[:, 2] - P[:, 0]; ges = float(np.abs(a_[:, 0] * b_[:, 1] - a_[:, 1] * b_[:, 0]).sum() / 2)
    o = ctx.ortung(('gelaende',)); x0, z0 = P.reshape(-1, 2).min(0); x1, z1 = P.reshape(-1, 2).max(0)
    sicht = 0
    for zs in np.arange(np.floor(z0 * 10) / 10, z1, 20.0):
        gx, gz = np.meshgrid(np.arange(np.floor(x0 * 10) / 10 + 0.05, x1, 0.1), np.arange(zs + 0.05, min(zs + 20, z1), 0.1))
        hw, _ = wo.hoehe(gx.ravel(), gz.ravel()); hg, _ = o.hoehe(gx.ravel(), gz.ravel())
        sicht += int((~np.isnan(hw) & ((hw > hg) | np.isnan(hg))).sum())
    return ges, sicht * 0.01


def q14(ctx):
    from shapely import LineString, union_all
    S = ctx.k['schwellen']
    if ctx.referenz is None or not (ctx.referenz / 'referenz_alt.json').exists(): raise Fehlt('referenz/referenz_alt.json fehlt')
    ref = json.loads((ctx.referenz / 'referenz_alt.json').read_text())
    idp = ctx.k['mittellinien']['id_prop']
    neu, je_id = {}, {}
    for pl, pr in _mittellinien(ctx):
        key = str(pr.get(idp)) + ('/' + str(pr['teil']) if 'teil' in pr else '')
        neu.setdefault(key, []).append(LineString(pl)); je_id.setdefault(str(pr.get(idp)), []).append(LineString(pl))
    def rkey(wg): return wg['id'] + ('/' + str(wg['teil']) if 'teil' in wg else '')
    bef, worst, fehlt = [], 0.0, []
    for wg in ref['wege']:
        key = rkey(wg); ziel = neu.get(key) if 'teil' in wg else je_id.get(wg['id'])
        if not ziel: fehlt.append(key); continue
        alt = LineString(wg['pl']); nn = union_all(ziel)
        hd = alt.hausdorff_distance(nn); worst = max(worst, hd)
        if hd > S['q14_weg_m']:
            bef.append({'weg': key, 'hausdorff_m': _r(hd, 3)})
    for k in fehlt[:20]: bef.append({'weg': k, 'fehler': 'Mittellinie fehlt in wege.geojson'})
    bekannt = {rkey(w) for w in ref['wege']} | {w['id'] for w in ref['wege'] if 'teil' not in w}
    zus = sorted(k for k in neu if k not in bekannt and k.split('/')[0] not in bekannt)
    n = ctx.netz(('gelaende',)); Pw = n['V'][n['T'][n['klasse'] == 'wasser']][:, :, [0, 2]]
    a_ = Pw[:, 1] - Pw[:, 0]; b_ = Pw[:, 2] - Pw[:, 0]
    wk4 = float(np.abs(a_[:, 0] * b_[:, 1] - a_[:, 1] * b_[:, 0]).sum() / 2)         # Klasse-4-Bett (Grundriss), nur Bericht
    rq = ctx.k['q14_wasser_referenz']                                               # Referenz zur Laufzeit aus wasser.geojson (Runde 3)
    rp = [g for g, _ in ctx.polygone(rq['datei'], rq.get('filter'))]
    if not rp: raise Fehlt(f"Referenz {rq['datei']} ohne Wasserpolygone")
    wref = float(union_all(rp).area)
    sp_ges, sp_sicht = _spiegel_flaechen(ctx)                                        # massgeblich: sichtbarer Spiegel
    bz_p = []
    zonen_da = (ctx.wurzel / ctx.k['vektor_ordner'] / ctx.k['bauzone']['datei']).exists()
    for g, pr in ctx.polygone(ctx.k['bauzone']['datei'], ctx.k['bauzone'].get('filter'), pflicht=False):
        if ctx.k['bauzone'].get('filter'): bz_p.append(g); continue
        v = pr.get(ctx.k['bauzone'].get('prop', 'bauzone_plan'))
        if v is True or v == 1 or (isinstance(v, str) and v.lower() in ('ja', 'true', '1')) or \
           'bauzone_plan' in (str(pr.get('klasse', '')).lower(), str(pr.get('id', '')).lower(), str(pr.get('typ', '')).lower()): bz_p.append(g)
    bz = union_all(bz_p).area if bz_p else 0.0
    rw = (sp_sicht / wref - 1) if sp_sicht is not None else None; rb = bz / ref['bauzone_m2'] - 1
    if sp_sicht is None: bef.append({'art': 'wasserflaeche', 'fehler': 'kein Wasserspiegel-Modell (manifest.modelle klasse 4)', 'klasse4_m2': _r(wk4, 1)})
    elif abs(rw) > S['q14_wasser_rel']: bef.append({'art': 'wasserflaeche', 'spiegel_sichtbar_m2': _r(sp_sicht, 1), 'referenz_m2': wref, 'rel': _r(rw), 'klasse4_m2': _r(wk4, 1)})
    if zonen_da and abs(rb) > S['q14_bauzone_rel']: bef.append({'art': 'bauzone', 'neu_m2': _r(bz, 1), 'alt_m2': ref['bauzone_m2'], 'rel': _r(rb)})
    if zonen_da and not bz_p: bef.append({'art': 'bauzone', 'fehler': 'zonen.geojson ohne bauzone_plan'})
    r = erg('Q14', not bef, {'wege_alt': len(ref['wege']), 'wege_fehlend': len(fehlt), 'wege_zusaetzlich': len(zus), 'hausdorff_max_m': _r(worst, 3),
                                'wasser_massgeblich': 'spiegel_sichtbar_m2 (Spiegelmodell, sichtbarer Teil = Spiegel ueber Gelaende)',
                                'wasser_spiegel_sichtbar_m2': _r(sp_sicht, 2), 'wasser_spiegel_modell_gesamt_m2': _r(sp_ges, 2), 'wasser_klasse4_bett_m2': _r(wk4, 2),
                                'wasser_referenz_m2': _r(wref, 2), 'wasser_referenz_quelle': rq['datei'] + ' (Vereinigung, zur Laufzeit)', 'wasser_rel': _r(rw), 'wasser_klasse4_rel': _r(wk4 / wref - 1),
                                'bauzone': ('Eingabe fehlt: ' + ctx.k['bauzone']['datei'] + ' (P1c)') if not zonen_da else 'vorhanden',
                                'bauzone_m2': _r(bz, 1) if zonen_da else None, 'bauzone_rel': _r(rb) if zonen_da else None,
                                'wasser_alte_quellen_nur_bericht_m2': ref.get('wasser_alternativen_m2'), 'referenz': ref.get('quelle')}, bef,
               'Hausdorff je Weg-ID (id[/teil]) alt (vektor.json/1,2) vs. neu (rolle=mittellinie); Wasser massgeblich = sichtbare Spiegelmodell-Flaeche '
               '(0,1-m-Raster: Spiegel ueber Gelaende) vs. Flaeche wasser.geojson zur Laufzeit +-3 % (Runde 3), Klasse-4-Bett und Spiegel gesamt nur Bericht; '
               'Bauzone = zonen.geojson layer=bauzone_plan vs. 31 927 m2 +-1 %.')
    if not zonen_da:
        r['notiz'] += ' Bauzone: Eingabe fehlt (zonen.geojson, P1c) - nicht bestanden, offen.'
        r['befunde'].append({'art': 'bauzone', 'fehler': 'Eingabe fehlt: zonen.geojson (P1c)'}); r['befunde_anzahl'] += 1
        if r['status'] == 'ok': r['status'] = 'offen'
    return r
