#!/usr/bin/env python3
"""QA-Selbsttest P6: sauberer Dummy muss alle Regeln bestehen (Durchlass), jede Fehlervariante muss ihre Regel
reissen (Fund). Zusaetzlich Kurven-Einheitstests (Kreis/Zickzack) fuer Q3-Geometrie und Exit-2-Fall.
Aufruf: python3 selbsttest/selbsttest.py [--tmp /tmp/dv2_qa/dummy] [--md ERGEBNIS_SELBSTTEST.md]"""
import argparse, json, subprocess, sys, time
from pathlib import Path
import numpy as np
QA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(QA)); sys.path.insert(0, str(QA / 'selbsttest'))
import baue_dummy
from pruefe_alle import laufe
from dv2qa.geom import glaettung_abw, form_abw

FEHLER = {  # Variante -> (Regel, Beschreibung)
    'Q1': ('Q1', '3 m2 Dreiecke bei 205|110 entfernt + 1 Nahtvertex E2 um 1 mm angehoben'),
    'Q1_bett': ('Q1', 'Loch r 0,5 m im Bachbett (Klasse 4) unter dem Spiegelmodell - Spiegel ist nicht Teil von Q1', 'innenrand'),
    'Q1_luecke': ('Q1', 'echte Naht-Luecke: Weg-Duplikate am Klassenrand z=99 (x 150-153) um 1 cm verschoben'),
    'Q2': ('Q2', 'Mesh-Vertices auf Wegrand z=73,6 (x 140-145) um 4 cm verschoben'),
    'Q3': ('Q3', 'Wegrand W1 rechts x 150-153 Zickzack +-5 cm'),
    'Q4': ('Q4', 'Buckel 5 cm in Kreuzung K1'),
    'Q5': ('Q5', 'Delle 6 cm, r 0,6 m, 2 m neben Wegrand W1 (150|77,6)'),
    'Q6': ('Q6', 'Weg W4 x 150-156 nicht eingesenkt'),
    'Q7': ('Q7', 'D2-Flaeche x140-150 z50-60 um 1,5 cm angehoben (> 1 cm)'),
    'Q7_lage': ('Q7', 'D2-Lage/Form: Weg W1 im D2-Bereich um 0,6 m nach Norden verschoben'),
    'Q8': ('Q8', 'Spiegelmodell +10 cm (Schnittlinie wandert vom Uferspline weg)'),
    'Q8_spalt': ('Q8', 'Spalt Spiegel/Ufer: linke Spiegelkante 15 cm vor dem Ufer (Kante ueber dem Bett)', 'spalt spiegel/ufer'),
    'Q8_ueberlappung': ('Q8', 'Spiegelkanten 0,3 m ins Ufer gezogen (Ueberlappung > 10 cm, kein Spalt)', 'ueberlappung spiegel/ufer'),
    'Q8_ohne_schnitt': ('Q8', 'Spiegel 0,4 m tiefer = unter Bett und Uferkante, schneidet das Ufer nicht', 'spiegel unter uferkante ohne schnitt'),
    'Q9': ('Q9', '5 Dreiecke in D3 mit umgedrehter Windung (Normale nach unten)'),
    'Q10': ('Q10', 'Kachel E3: UV0 gespiegelt (u = -x), UV1 um 0,001 versetzt'),
    'Q10_triplanar': ('Q10', 'Triplanar-Zone (Felskegel, Klasse 3, ~40 Grad): UV0 mit NaN und 5-cm-Spruengen an Duplikaten'),
    'Q10_flip': ('Q10', 'Triplanar-Zone: UV0 gespiegelt (u = 2*143 - x)'),
    'Q10_uv2': ('Q10', 'UV2 Weg W4 x 150-160: Bogenlaenge x 1,3 (30 % Verzerrung)'),
    'Q11': ('Q11', 'flaeche.png 10x10 m auf Fels (echte Datenschicht query.mjs/manifest.mjs)'),
    'Q12': ('Q12', 'Bruecke E2 ohne Gelaender/Handlauf, Widerlager 5 cm ueber Gelaende'),
    'Q13': ('Q13', '2 der 25 Abnahmebilder fehlen'),
    'Q14': ('Q14', 'Mittellinie W4 0,5 m versetzt, Bauzone +2 % Radius'),
    'Q14_wasser': ('Q14', 'Spiegelmodell +5 cm und 0,5 m ins Ufer: sichtbare Spiegelflaeche ~+9 %'),
}


def einheit():
    """Q3-Einheitstests (Runde 3: abtastunabhaengige Messung form_abw, Neuabtastung 0,05 m, Fenster 1 m)."""
    from shapely import LineString
    out = []
    def kreis(r, d):
        n = int(round(2 * np.pi * r / d)); t = np.linspace(0, 2 * np.pi, n, endpoint=False); k = np.c_[r * np.cos(t), r * np.sin(t)]
        return np.vstack([k, k[:1]])
    # (a) Kreis r 2,0 m mit 0,25 m und 0,05 m Stuetzpunktabstand
    w = {}
    for d in (0.25, 0.05):
        _, a, k = form_abw(kreis(2.0, d), 1.0, True, 0.05); a_alt, k_alt = glaettung_abw(kreis(2.0, d), 1.0, True)
        w[d] = (a.max(), k.max(), a_alt.max(), k_alt.max())
    dif = abs(w[0.25][0] - w[0.05][0])
    out.append(('(a) Kreis r 2,0 m: 0,25 vs. 0,05 m', dif <= 0.005 and max(w[0.25][0], w[0.05][0]) <= 0.03,
                f"neu abw {w[0.25][0]*100:.2f} / {w[0.05][0]*100:.2f} cm (Diff {dif*1000:.1f} mm, Sehnenpfeil 0,25-m-Polygon {2*(1-np.cos(0.0625))*1000:.1f} mm), "
                f"Knick {w[0.25][1]:.1f}/{w[0.05][1]:.1f} Grad; alt abw {w[0.25][2]*100:.2f} / {w[0.05][2]*100:.2f} cm (Diff {abs(w[0.25][2]-w[0.05][2])*1000:.1f} mm)"))
    # (b) ungleich verteilte DP-Stuetzpunkte auf derselben Form wie dicht
    x = np.arange(0, 20.0001, 0.01); dicht = np.c_[x, 1.5 * np.sin(x / 3) + 0.4 * np.sin(x / 1.3)]
    dp = np.array(LineString(dicht).simplify(0.003).coords)
    sp = np.hypot(*np.diff(dp, axis=0).T)
    _, a1, k1 = form_abw(dicht, 1.0, False, 0.05); _, a2, k2 = form_abw(dp, 1.0, False, 0.05)
    a1o, _ = glaettung_abw(dicht, 1.0); a2o, _ = glaettung_abw(dp, 1.0)
    dif = abs(a1.max() - a2.max())
    out.append(('(b) DP-Stuetzpunkte = dicht', dif <= 0.003 and (a1.max() <= 0.03) == (a2.max() <= 0.03),
                f"{len(dp)} DP-Punkte (Abstand {sp.min():.2f}-{sp.max():.2f} m) vs. {len(dicht)} dicht: neu {a2.max()*100:.2f} / {a1.max()*100:.2f} cm (Diff {dif*1000:.1f} mm); alt {a2o.max()*100:.2f} / {a1o.max()*100:.2f} cm"))
    # (c) echte Delle 5 cm (Breite 0,4 m) und Zickzack +-5 cm / 90-Grad-Ecke werden gefunden - dicht und DP
    xd = np.arange(0, 10.0001, 0.01); delle = np.c_[xd, -0.05 * np.clip(1 - np.abs(xd - 5) / 0.2, 0, 1)]
    dd = np.array(LineString(delle).simplify(0.003).coords)
    _, ad, _ = form_abw(delle, 1.0, False, 0.05); _, add_, _ = form_abw(dd, 1.0, False, 0.05)
    out.append(('(c) Delle 5 cm gefunden (dicht + DP)', ad.max() > 0.03 and add_.max() > 0.03, f'abw dicht {ad.max()*100:.2f} cm, DP ({len(dd)} Punkte) {add_.max()*100:.2f} cm'))
    xz = np.arange(0, 10, 0.2); zz = np.c_[xz, np.where(np.arange(len(xz)) % 2, 0.05, -0.05)]
    _, a, k = form_abw(zz); out.append(('(c) Zickzack +-5 cm gefunden', a.max() > 0.03 or k.max() > 15, f'abw {a.max()*100:.2f} cm, Knick {k.max():.1f} Grad'))
    ecke = np.array([[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]], float)
    _, a, k = form_abw(ecke); out.append(('(c) 90-Grad-Ecke gefunden', k.max() > 15, f'Knick {k.max():.1f} Grad, abw {a.max()*100:.1f} cm'))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tmp', default='/tmp/dv2_qa/dummy'); ap.add_argument('--md')
    a = ap.parse_args(); tmp = Path(a.tmp); t0 = time.time()
    zeilen, ok_ges = [], True
    def lauf(v, nur=None):
        d = tmp / v
        return laufe(d, d / 'referenz', d / 'abnahme', nur, d / 'konfig_dummy.json', still=True)
    baue_dummy.baue(tmp / 'sauber')
    r = lauf('sauber')
    for q, x in r['regeln'].items():
        good = x['status'] == 'ok'; ok_ges &= good
        zeilen.append(('sauber', q, 'ok', x['status'], good, json.dumps(x['werte'], ensure_ascii=False)[:160]))
    q8 = r['regeln']['Q8']['werte']
    good = q8['spalt_punkte'] == 0 and q8['ohne_schnitt'] == 0 and q8['spiegel_randpunkte'] > 0 and r['regeln']['Q14']['werte']['wasser_rel'] is not None and abs(r['regeln']['Q14']['werte']['wasser_rel']) < 0.01
    ok_ges &= good
    zeilen.append(('sauber', 'Q8/Q14-Spiegel', 'ok', f"{q8['spiegel_randpunkte']} Randpkt., Spalt {q8['spalt_punkte']}", good,
                   f"Spiegelmodell 5 cm im Ufer, Schnitt an jeder Station; sichtbar {r['regeln']['Q14']['werte']['wasser_spiegel_sichtbar_m2']} m2 vs. Bett Kl. 4 {r['regeln']['Q14']['werte']['wasser_klasse4_bett_m2']} m2"))
    q1 = r['regeln']['Q1']['werte']
    good = q1['duplikate_verschweisst'] > 0 and q1['randkanten_innen'] == 0 and q1['strahl_loecher'] == 0; ok_ges &= good
    zeilen.append(('sauber', 'Q1-Duplikate', 'kein Loch', f"{q1['duplikate_verschweisst']} dupl., {q1['randkanten_innen']} Rand", good,
                   'positionsgleiche Klassengrenz-Duplikate werden verschweisst, 0 Innenrandkanten, 0 Strahlloecher'))
    for v, (q, txt, *kw) in FEHLER.items():
        baue_dummy.baue(tmp / v, v)
        x = lauf(v, {q})['regeln'][q]
        good = x['status'] == 'fehler' and not any('ausnahme' in b for b in x['befunde'])
        bf = x['befunde'][0] if x['befunde'] else {}
        if kw:   # erwartete Befundart muss dabei sein
            treffer = [b for b in x['befunde'] if kw[0] in json.dumps(b, ensure_ascii=False)]
            good = good and bool(treffer); bf = treffer[0] if treffer else bf
        ok_ges &= good
        zeilen.append((v, q, 'fehler', x['status'], good, txt + ' -> ' + json.dumps(bf, ensure_ascii=False)[:150]))
    # Sonderfaelle mit Soll != fehler
    for v, q, soll, txt, pruef in (
        ('Q10_kurve', 'Q10', 'ok', 'enge S-Kurve W4 (r ~4 m) mit 15 % UV2-Stauchung: nur gekennzeichnet, nicht blockierend',
         lambda x: x['status'] == 'ok' and x['werte']['uv2_enge_kurve_ueber_10pct_gekennzeichnet'] > 0 and x['werte']['uv2_ueber_10pct'] == 0),
        ('Q14_ohne_zonen', 'Q14', 'offen', 'zonen.geojson fehlt (P1c): Bauzone "Eingabe fehlt", nicht bestanden',
         lambda x: x['status'] == 'offen' and any('Eingabe fehlt' in str(b.get('fehler', '')) for b in x['befunde']))):
        baue_dummy.baue(tmp / v, v)
        x = lauf(v, {q})['regeln'][q]
        good = bool(pruef(x)); ok_ges &= good
        w = x['werte']; det = {k: w.get(k) for k in ('uv2_enge_kurve_dreiecke', 'uv2_enge_kurve_ueber_10pct_gekennzeichnet', 'uv2_enge_kurve_max_abw', 'kurvenradius_min_m', 'uv2_ueber_10pct', 'bauzone') if k in w}
        zeilen.append((v, q, soll, x['status'], good, txt + ' -> ' + json.dumps(det, ensure_ascii=False)[:150]))
    # Exit-2: leerer Ordner
    leer = tmp / 'leer'; leer.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([sys.executable, str(QA / 'pruefe_alle.py'), '--wurzel', str(leer), '--nur', 'Q1,Q7'], capture_output=True, text=True)
    good = p.returncode == 2; ok_ges &= good
    zeilen.append(('leer', 'Runner', 'exit 2', f'exit {p.returncode}', good, 'fehlende Eingaben -> offen'))
    p = subprocess.run([sys.executable, str(QA / 'pruefe_alle.py'), '--wurzel', str(tmp / 'Q5'), '--referenz', str(tmp / 'Q5' / 'referenz'), '--konfig', str(tmp / 'Q5' / 'konfig_dummy.json'), '--nur', 'Q5'], capture_output=True, text=True)
    good = p.returncode == 1; ok_ges &= good
    zeilen.append(('Q5', 'Runner', 'exit 1', f'exit {p.returncode}', good, 'Fehler -> Exit 1'))
    # Q14-Referenz: wasser.geojson (#54) = 6547,84 m2 und konfig.json
    import json as _j
    from shapely.geometry import shape
    from shapely import union_all
    wg = QA.parent / 'vektor' / 'wasser.geojson'
    kq = _j.loads((QA / 'konfig.json').read_text())['q14_wasser_referenz']
    if wg.exists():
        fl = union_all([shape(f['geometry']) for f in _j.loads(wg.read_text())['features'] if f['properties'].get('typ') == kq['filter']['typ']]).area
        good = abs(fl - 6630.17) < 0.05 and kq['datei'] == 'wasser.geojson'
        zeilen.append(('repo', 'Q14-Referenz', '~6630,17', f'{fl:.2f}', good, 'Referenz zur Laufzeit aus wasser.geojson (konfig q14_wasser_referenz, Runde 3), Stand art/dorfmap-fertig aa78160'))
    else:
        good = False; zeilen.append(('repo', 'Q14-Referenz', '6547,84', 'fehlt', False, 'vektor/wasser.geojson fehlt'))
    ok_ges &= good
    for name, good, txt in einheit():
        ok_ges &= bool(good); zeilen.append(('einheit', 'Q3-Geometrie', 'ok', 'ok' if good else 'falsch', bool(good), f'{name}: {txt}'))
    dauer = time.time() - t0
    for z in zeilen: print(f"{'OK ' if z[4] else 'XX '} {z[0]:11s} {z[1]:12s} soll={z[2]:7s} ist={z[3]:7s} {z[5]}")
    print(f"SELBSTTEST {'BESTANDEN' if ok_ges else 'NICHT BESTANDEN'} ({len(zeilen)} Faelle, {dauer:.0f} s)")
    if a.md:
        md = ['# Selbsttest QA detail_v2 (P6)', '', f"Lauf: {time.strftime('%Y-%m-%d %H:%M %Z')} · Dauer {dauer:.0f} s · Ergebnis: **{'BESTANDEN' if ok_ges else 'NICHT BESTANDEN'}**", '',
              'Dummy: 4 Kacheln D2/E2/D3/E3 im verbindlichen Format (PLAN_QA_DV2.md Abschn. 8 inkl. Runde 2: Bett Kl. 4 geschlossen, Spiegelmodell, wege/kreuzungen im #56-Schema), gebaut von `selbsttest/baue_dummy.py` nach `/tmp/dv2_qa/dummy/`.', '',
              '| Fall | Regel | Soll | Ist | ok | Detail |', '|---|---|---|---|---|---|']
        md += [f"| {z[0]} | {z[1]} | {z[2]} | {z[3]} | {'ja' if z[4] else '**nein**'} | {z[5].replace('|', '/')} |" for z in zeilen]
        Path(a.md).write_text('\n'.join(md) + '\n')
    sys.exit(0 if ok_ges else 1)


if __name__ == '__main__':
    main()
