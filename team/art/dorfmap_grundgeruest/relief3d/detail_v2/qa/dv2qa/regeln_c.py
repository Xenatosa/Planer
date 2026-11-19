"""Q11-Q14 (Datenschicht/queryPoint, Bruecken, Abnahmebilder, Layout-Treue)."""
import json, subprocess, os, tempfile
from pathlib import Path
import numpy as np
from .geom import KLASSEN
from .regeln_a import erg, _r, _mittellinien
from .welt import Fehlt

NODE_HARNESS = r'''
import { pathToFileURL } from 'node:url';
import { readFileSync, writeFileSync } from 'node:fs';
const [, , modPfad, datenDir, punkte, aus] = process.argv;
const m = await import(pathToFileURL(modPfad).href);
for (const f of ['lade', 'laden', 'init']) { if (typeof m[f] === 'function') { await m[f](datenDir); break; } }
const P = JSON.parse(readFileSync(punkte, 'utf8'));
const out = [];
for (const [x, z] of P) { let r; try { r = await m.queryPoint(x, z); } catch (e) { r = { fehler: String(e) }; } out.push(r); }
writeFileSync(aus, JSON.stringify(out));
'''


def _klasse_name(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool): return KLASSEN[int(v)] if 0 <= int(v) < len(KLASSEN) else str(v)
    return str(v)


def q11(ctx):
    S = ctx.k['schwellen']; d = ctx.wurzel / ctx.k['daten_ordner']
    mod = d / 'query.mjs'
    if not mod.exists(): raise Fehlt(f'{mod} fehlt')
    rng = np.random.default_rng(611)
    B = np.array([kd['bounds'] for kd in ctx.kacheln.values()], float)
    k = rng.integers(0, len(B), S['q11_punkte'])
    P = np.c_[rng.uniform(B[k, 0], B[k, 2]), rng.uniform(B[k, 1], B[k, 3])]
    for br in ctx.k['bruecken'].values():                      # Brueckenfussabdruck: queryPoint darf Deckhoehe liefern
        m = (P[:, 0] >= br['x'][0] - 1) & (P[:, 0] <= br['x'][1] + 1) & (P[:, 1] >= br['z'][0] - 1) & (P[:, 1] <= br['z'][1] + 1)
        P = P[~m]
    tmp = Path(os.environ.get('DV2QA_TMP', '/tmp/dv2_qa')); tmp.mkdir(parents=True, exist_ok=True)
    hp = tmp / 'q11_harness.mjs'; hp.write_text(NODE_HARNESS)
    pp = tmp / 'q11_punkte.json'; pp.write_text(json.dumps(P.round(4).tolist())); ap = tmp / 'q11_aus.json'
    r = subprocess.run(['node', str(hp), str(mod.resolve()), str(d.resolve()), str(pp), str(ap)], capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        return erg('Q11', False, {'node_exit': r.returncode}, [{'fehler': 'queryPoint-Harness', 'stderr': r.stderr[-400:]}])
    res = json.loads(ap.read_text())
    o = ctx.ortung(('gelaende',)); h, t = o.hoehe(P[:, 0], P[:, 1])
    n = ctx.netz(('gelaende',)); kl = np.where(t >= 0, n['klasse'][np.maximum(t, 0)], '')
    try:
        ow = ctx.ortung(('wasser',)); hw, tw = ow.hoehe(P[:, 0], P[:, 1]); unter = (tw >= 0) & (hw > h)
        kl = np.where(unter, 'wasser', kl)
    except Fehlt:
        pass
    qh = np.array([x.get('hoehe', np.nan) if isinstance(x, dict) else np.nan for x in res], float)
    qf = np.array([_klasse_name(x.get('flaeche')) if isinstance(x, dict) else '' for x in res])
    dh = np.abs(qh - h); gueltig = ~np.isnan(h)
    fehl_h = np.nonzero(gueltig & ~(dh <= S['q11_dh_m'] + 1e-9))[0]
    gleich = float((qf[gueltig] == kl[gueltig]).mean()) if gueltig.any() else 0
    felder = all(isinstance(x, dict) and all(f in x for f in ('hoehe', 'flaeche', 'untergrund', 'begehbar', 'slot', 'kachel')) for x in res)
    # node --test
    td = d / 'test'
    if td.exists():
        dateien = sorted(str(x) for x in td.rglob('*.test.mjs')) + sorted(str(x) for x in td.rglob('*.test.js'))
        if dateien:
            tr = subprocess.run(['node', '--test', *dateien], capture_output=True, text=True, timeout=600, cwd=str(d))
            tests_ok = tr.returncode == 0; tests = (tr.stdout + tr.stderr)[-400:]
        else:
            tests_ok = False; tests = 'keine *.test.mjs in test/'
    else:
        tests_ok = False; tests = 'test/ fehlt'
    bef = [{'art': 'hoehe', 'x': _r(P[i, 0], 2), 'z': _r(P[i, 1], 2), 'query_m': _r(qh[i]), 'mesh_m': _r(h[i]), 'dh_m': _r(dh[i])} for i in fehl_h[np.argsort(-np.nan_to_num(dh[fehl_h], nan=9))][:10]]
    if gleich < S['q11_flaeche_anteil']:
        falsch = np.nonzero(gueltig & (qf != kl))[0]
        bef += [{'art': 'flaeche', 'anteil_gleich': _r(gleich, 5)}] + [{'art': 'flaeche_pkt', 'x': _r(P[i, 0], 2), 'z': _r(P[i, 1], 2), 'query': qf[i], 'mesh': kl[i]} for i in falsch[:5]]
    if not felder: bef.append({'art': 'felder', 'fehler': 'queryPoint liefert nicht alle Felder {hoehe, flaeche, untergrund, begehbar, slot, kachel}'})
    if not tests_ok: bef.append({'art': 'node --test', 'ausgabe': tests})
    return erg('Q11', not bef, {'punkte': int(len(P)), 'dh_max_m': _r(np.nanmax(dh[gueltig]) if gueltig.any() else np.nan), 'ueber_2cm': int(len(fehl_h)),
                                'flaeche_gleich': _r(gleich, 5), 'felder_vollstaendig': felder, 'tests_gruen': tests_ok}, bef,
               '10 000 Zufallspunkte (Seed 611) in den Manifest-Kacheln, Brueckenfussabdruecke +1 m ausgenommen; Sollklasse = Dreiecksklasse bzw. wasser, wenn Wassermesh ueber Gelaende.')


def q12(ctx):
    S = ctx.k['schwellen']; mods = ctx.modelle(); o = ctx.ortung(('gelaende',))
    pflicht = {'bohle': ['bohle'], 'traeger': ['traeger'], 'pfosten': ['pfosten'], 'gelaender': ['gelaender', 'handlauf'], 'auflager': ['widerlager', 'auflager']}
    bef, w = [], {}
    for name, br in ctx.k['bruecken'].items():
        prims = next((v for k, v in mods.items() if k.lower() == br['datei'].lower()), None)   # Gross/klein egal (P3: bruecke_e2.glb)
        if prims is None:
            bef.append({'bruecke': name, 'fehler': f"modelle/{br['datei']}.glb fehlt"}); continue
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


def q14(ctx):
    from shapely import LineString, union_all
    S = ctx.k['schwellen']
    if ctx.referenz is None or not (ctx.referenz / 'referenz_alt.json').exists(): raise Fehlt('referenz/referenz_alt.json fehlt')
    ref = json.loads((ctx.referenz / 'referenz_alt.json').read_text())
    idp = ctx.k['mittellinien']['id_prop']
    neu = {}
    for pl, pr in _mittellinien(ctx):
        key = str(pr.get(idp)) + ('/' + str(pr['teil']) if 'teil' in pr else '')
        neu.setdefault(key, []).append(LineString(pl))
    bef, worst, fehlt = [], 0.0, []
    for wg in ref['wege']:
        key = wg['id'] + ('/' + str(wg['teil']) if 'teil' in wg else '')
        if key not in neu: fehlt.append(key); continue
        alt = LineString(wg['pl']); nn = union_all(neu[key])
        hd = alt.hausdorff_distance(nn); worst = max(worst, hd)
        if hd > S['q14_weg_m']:
            bef.append({'weg': key, 'hausdorff_m': _r(hd, 3)})
    for k in fehlt[:20]: bef.append({'weg': k, 'fehler': 'Mittellinie fehlt in wege.geojson'})
    zus = sorted(set(neu) - {w['id'] + ('/' + str(w['teil']) if 'teil' in w else '') for w in ref['wege']})
    wa = union_all([g for g, _ in ctx.polygone(ctx.k['wasser']['datei'])]).area
    bz_p = [g for g, _ in ctx.polygone(ctx.k['bauzone']['datei'], ctx.k['bauzone']['filter'])]
    bz = union_all(bz_p).area if bz_p else 0.0
    rw = wa / ref['wasser_m2'] - 1; rb = bz / ref['bauzone_m2'] - 1
    if abs(rw) > S['q14_wasser_rel']: bef.append({'art': 'wasserflaeche', 'neu_m2': _r(wa, 1), 'alt_m2': ref['wasser_m2'], 'rel': _r(rw)})
    if abs(rb) > S['q14_bauzone_rel']: bef.append({'art': 'bauzone', 'neu_m2': _r(bz, 1), 'alt_m2': ref['bauzone_m2'], 'rel': _r(rb)})
    return erg('Q14', not bef, {'wege_alt': len(ref['wege']), 'wege_fehlend': len(fehlt), 'wege_zusaetzlich': len(zus), 'hausdorff_max_m': _r(worst, 3),
                                'wasser_rel': _r(rw), 'bauzone_rel': _r(rb), 'referenz': ref.get('quelle')}, bef,
               'Hausdorff je Weg-ID (id[/teil]) alt (vektor.json/1,2) vs. neu; Wasser = Vereinigung wasser.geojson vs. alte WV-Flaeche; Bauzone = zonen.geojson[bauzone] vs. alt.')
