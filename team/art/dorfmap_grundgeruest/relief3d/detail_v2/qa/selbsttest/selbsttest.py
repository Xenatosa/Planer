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
from dv2qa.geom import glaettung_abw

FEHLER = {  # Variante -> (Regel, Beschreibung)
    'Q1': ('Q1', '3 m2 Dreiecke bei 205|110 entfernt + 1 Nahtvertex E2 um 1 mm angehoben'),
    'Q2': ('Q2', 'Mesh-Vertices auf Wegrand z=73,6 (x 140-145) um 4 cm verschoben'),
    'Q3': ('Q3', 'Wegrand W1 rechts x 150-153 Zickzack +-5 cm'),
    'Q4': ('Q4', 'Buckel 5 cm in Kreuzung K1'),
    'Q5': ('Q5', 'Delle 6 cm, r 0,6 m, 2 m neben Wegrand W1 (150|77,6)'),
    'Q6': ('Q6', 'Weg W4 x 150-156 nicht eingesenkt'),
    'Q7': ('Q7', 'D2-Flaeche x140-150 z50-60 um 1,5 cm angehoben (> 1 cm)'),
    'Q7_lage': ('Q7', 'D2-Lage/Form: Weg W1 im D2-Bereich um 0,6 m nach Norden verschoben'),
    'Q8': ('Q8', 'Wasserspiegel in wasser.geojson +10 cm (Schnittlinie wandert vom Uferspline weg)'),
    'Q9': ('Q9', '5 Dreiecke in D3 mit umgedrehter Windung (Normale nach unten)'),
    'Q10': ('Q10', 'Kachel E3: UV0 gespiegelt (u = -x), UV1 um 0,001 versetzt'),
    'Q11': ('Q11', 'hoehe.png 30x30 m +5 cm, flaeche.png 10x10 m auf Fels'),
    'Q12': ('Q12', 'Bruecke E2 ohne Gelaender/Handlauf, Widerlager 5 cm ueber Gelaende'),
    'Q13': ('Q13', '2 der 25 Abnahmebilder fehlen'),
    'Q14': ('Q14', 'Mittellinie W4 0,5 m versetzt, Bauzone +2 % Radius'),
    'Q14_wasser': ('Q14', 'Wasserpolygon 0,3 m breiter (+7 % Flaeche)'),
}


def einheit():
    out = []
    t = np.linspace(0, 2 * np.pi, 400); kreis = np.c_[5 * np.cos(t), 5 * np.sin(t)]
    a, k = glaettung_abw(kreis, 1.0, True); out.append(('Kreis r=5 m glatt', a.max() <= 0.03 and k.max() <= 15, f'abw {a.max():.4f} m, knick {k.max():.1f} Grad'))
    x = np.arange(0, 10, 0.2); zz = np.c_[x, np.where(np.arange(len(x)) % 2, 0.05, -0.05)]
    a, k = glaettung_abw(zz, 1.0); out.append(('Zickzack +-5 cm erkannt', a.max() > 0.03 or k.max() > 15, f'abw {a.max():.4f} m, knick {k.max():.1f} Grad'))
    ecke = np.array([[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]], float)
    a, k = glaettung_abw(ecke, 1.0); out.append(('90-Grad-Ecke erkannt', k.max() > 15, f'knick {k.max():.1f} Grad'))
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
    for v, (q, txt) in FEHLER.items():
        baue_dummy.baue(tmp / v, v)
        x = lauf(v, {q})['regeln'][q]
        good = x['status'] == 'fehler' and not any('ausnahme' in b for b in x['befunde']); ok_ges &= good
        bf = x['befunde'][0] if x['befunde'] else {}
        zeilen.append((v, q, 'fehler', x['status'], good, txt + ' -> ' + json.dumps(bf, ensure_ascii=False)[:150]))
    # Exit-2: leerer Ordner
    leer = tmp / 'leer'; leer.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([sys.executable, str(QA / 'pruefe_alle.py'), '--wurzel', str(leer), '--nur', 'Q1,Q7'], capture_output=True, text=True)
    good = p.returncode == 2; ok_ges &= good
    zeilen.append(('leer', 'Runner', 'exit 2', f'exit {p.returncode}', good, 'fehlende Eingaben -> offen'))
    p = subprocess.run([sys.executable, str(QA / 'pruefe_alle.py'), '--wurzel', str(tmp / 'Q5'), '--referenz', str(tmp / 'Q5' / 'referenz'), '--konfig', str(tmp / 'Q5' / 'konfig_dummy.json'), '--nur', 'Q5'], capture_output=True, text=True)
    good = p.returncode == 1; ok_ges &= good
    zeilen.append(('Q5', 'Runner', 'exit 1', f'exit {p.returncode}', good, 'Fehler -> Exit 1'))
    for name, good, txt in einheit():
        ok_ges &= bool(good); zeilen.append(('einheit', 'Q3-Geometrie', 'ok', 'ok' if good else 'falsch', bool(good), f'{name}: {txt}'))
    dauer = time.time() - t0
    for z in zeilen: print(f"{'OK ' if z[4] else 'XX '} {z[0]:11s} {z[1]:12s} soll={z[2]:7s} ist={z[3]:7s} {z[5]}")
    print(f"SELBSTTEST {'BESTANDEN' if ok_ges else 'NICHT BESTANDEN'} ({len(zeilen)} Faelle, {dauer:.0f} s)")
    if a.md:
        md = ['# Selbsttest QA detail_v2 (P6)', '', f"Lauf: {time.strftime('%Y-%m-%d %H:%M %Z')} · Dauer {dauer:.0f} s · Ergebnis: **{'BESTANDEN' if ok_ges else 'NICHT BESTANDEN'}**", '',
              'Dummy: 4 Kacheln D2/E2/D3/E3 im angenommenen Format (PLAN_QA_DV2.md Abschn. 2), gebaut von `selbsttest/baue_dummy.py` nach `/tmp/dv2_qa/dummy/`.', '',
              '| Fall | Regel | Soll | Ist | ok | Detail |', '|---|---|---|---|---|---|']
        md += [f"| {z[0]} | {z[1]} | {z[2]} | {z[3]} | {'ja' if z[4] else '**nein**'} | {z[5].replace('|', '/')} |" for z in zeilen]
        Path(a.md).write_text('\n'.join(md) + '\n')
    sys.exit(0 if ok_ges else 1)


if __name__ == '__main__':
    main()
