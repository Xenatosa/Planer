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
    'Q14_fehlt': ('Q14', 'Referenz-Teilstueck W8/0 fehlt in wege.geojson, nicht in q14_ausnahmen -> bleibt hart', 'Mittellinie fehlt'),
    'Q14_zelle_fehlt': ('Q14', 'Bauzone Zellformat (#61): 1 Zelle aus der CSV fehlt in zonen.geojson', 'fehlen in zonen.geojson'),
    'Q3_bruecke_p5_laengs': ('Q3', 'P5-Regel an: Deckecken frei, aber Delle 4 cm auf der Laengsseite des Brueckenrechtecks bleibt hart', 'flaechentyp_br01'),
    'Q3_wegende_weit': ('Q3', 'Delle ~4,1 cm an Grund-Zone, aber > 3 m vor jedem Wegende -> hart', 'flaechentyp_gr01'),
    'Q3_wegende_gross': ('Q3', 'Delle ~6 cm (> 4,8 cm) 2 m vor Wegende W5 -> hart', 'flaechentyp_gr01'),
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
    out += einheit_f11()
    return out


def einheit_f11():
    """F11 (Runde 4): Zonenringe - Kartenrand und +-0,5 m um Stosspunkte (>= 3 Zonen) ausgenommen, alles andere hart.
    Karte 20 x 10 m: A = [0,10]x[0,10], B = [10,20]x[5,10], C = [10,20]x[0,5]; Stosspunkt (10|5)."""
    from shapely import box
    from dv2qa.regeln_a import zonen_stosspunkte, zonen_maske
    zk = {'kartenrand_tol_m': 0.01, 'stoss_fenster_m': 0.5, 'stoss_tol_m': 0.01, 'hart_typen': ['bruecke']}
    rand = box(0, 0, 20, 10).boundary
    def ring(x0, x1, z0, z1, d=0.05):
        e = [(x0, z0), (x1, z0), (x1, z1), (x0, z1), (x0, z0)]; P = []
        for (ax, az), (bx, bz) in zip(e[:-1], e[1:]):
            n = int(round(max(abs(bx - ax), abs(bz - az)) / d)); t = np.arange(n) / n; P.append(np.c_[ax + t * (bx - ax), az + t * (bz - az)])
        return np.vstack(P)
    def zonen(typ_c='grund', delle=None):
        A = ring(0, 10, 0, 10)
        if delle is not None:     # Buckel 5 cm (x-Richtung) auf A-Ostkante bei z = delle (Breite 0,2 m)
            m = np.abs(A[:, 0] - 10) < 1e-9; A[m, 0] -= 0.05 * np.clip(1 - np.abs(A[m, 1] - delle) / 0.1, 0, 1)
        return [(A, True, {'id': 'A', 'typ': 'grund'}), (ring(10, 20, 5, 10), True, {'id': 'B', 'typ': 'weg'}), (ring(10, 20, 0, 5), True, {'id': 'C', 'typ': typ_c})]
    def mess(zr, wen):
        st = zonen_stosspunkte(zr, zk, rand)
        pl, g, pr = [z for z in zr if z[2]['id'] == wen][0]
        R, abw, knick = form_abw(pl, 1.0, True, 0.05)
        aus, gr = zonen_maske(R, pl, True, {'stoss': st, 'pr': pr}, rand, zk)
        ub = ((abw > 0.03) | (knick > 15)) & ~aus
        return st, R, abw, knick, aus, gr, ub
    out = []
    st, R, abw, knick, aus, gr, ub = mess(zonen(), 'B')
    ecke_rand = np.hypot(R[:, 0] - 20, R[:, 1] - 10) < 0.3          # Kartenecke (20|10), Abschnitt auf dem Kartenrand
    out.append(('F11 Kartenrand-Abschnitt + Kartenecke ausgenommen', bool(aus[ecke_rand].all()) and abw[ecke_rand].max() > 0.03 and not ub[ecke_rand].any(),
                f"Ring B, Ecke (20|10): roh abw {abw[ecke_rand].max()*100:.1f} cm / Knick {knick[ecke_rand].max():.0f} Grad, ausgenommen {int(aus[ecke_rand].sum())}/{int(ecke_rand.sum())} Punkte (Gruppe kartenrand)"))
    sp = [d for d in st if abs(d['x'] - 10) < 0.02 and abs(d['z'] - 5) < 0.02]
    fen = np.hypot(R[:, 0] - 10, R[:, 1] - 5) <= 0.3
    out.append(('F11 Stosspunkt-Fenster +-0,5 m ausgenommen', len(sp) == 1 and sp[0]['ausgenommen'] and sp[0]['zonen'] == ['A', 'B', 'C']
                and bool(aus[fen].all()) and knick[fen].max() > 15 and not ub[np.hypot(R[:, 0] - 10, R[:, 1] - 5) <= 0.5].any(),
                f"Stosspunkt {[(d['x'], d['z'], d['zonen']) for d in sp]} (dazu {len(st) - 1} am Kartenrand, F13); Ring B roh Knick {knick[fen].max():.0f} Grad an (10|5), im Fenster ausgenommen, kein Rest-Befund im Fenster"))
    st, R, abw, knick, aus, gr, ub = mess(zonen(delle=5.65), 'A')
    bu = (np.abs(R[:, 1] - 5.65) < 0.15) & (np.abs(R[:, 0] - 10) < 0.1)
    out.append(('F11 Knick knapp ausserhalb des Fensters gefunden', bool(ub[bu].any()) and not aus[bu].any(),
                f"Buckel 5 cm bei 0,65 m Bogenlaenge vom Stosspunkt: abw {abw[bu].max()*100:.1f} cm, Knick {knick[bu].max():.0f} Grad, Gruppe {sorted(set(gr[bu & ub]))}"))
    st, R, abw, knick, aus, gr, ub = mess(zonen(typ_c='bruecke'), 'B')
    fen = np.hypot(R[:, 0] - 10, R[:, 1] - 5) <= 0.3
    sp = [d for d in st if abs(d['x'] - 10) < 0.02 and abs(d['z'] - 5) < 0.02]
    out.append(('F11 Brueckenecke bleibt hart', len(sp) == 1 and not sp[0]['ausgenommen'] and bool(ub[fen].any()) and not aus[fen].any(),
                f"C typ bruecke: Stosspunkt (10|5) ausgenommen={sp[0]['ausgenommen'] if sp else None}, Ring B Knick {knick[fen].max():.0f} Grad gefunden, Gruppe {sorted(set(gr[fen & ub]))}"))
    # F13 (Runde 5): 2 Zonen treffen auf den Kartenrand = Stosspunkt (Zone, Zone, ausserhalb) -> Fenster; Bruecke bleibt hart
    zr = [(ring(0, 10, 0, 10), True, {'id': 'A', 'typ': 'grund'}), (ring(10, 20, 0, 10), True, {'id': 'B', 'typ': 'weg'})]
    st = zonen_stosspunkte(zr, zk, rand); st0 = zonen_stosspunkte(zr, zk)
    pl, g, pr = zr[1]; R, abw, knick = form_abw(pl, 1.0, True, 0.05)
    aus, gr = zonen_maske(R, pl, True, {'stoss': st, 'pr': pr}, rand, zk)
    t = np.hypot(R[:, 0] - 10, R[:, 1] - 10) <= 0.5
    ub = ((abw > 0.03) | (knick > 15)) & ~aus
    out.append(('F13 Kartenrand-Stoss (2 Zonen + Rand) im Fenster ausgenommen', len(st0) == 0 and len(st) == 2 and all(d['kartenrand'] and d['ausgenommen'] and 'ausserhalb' in d['zonen'] for d in st)
                and bool(aus[t].all()) and abw[t].max() > 0.03 and not ub.any(),
                f"ohne Rand {len(st0)} Stosspunkte, mit Rand {len(st)}: {[(d['x'], d['z'], d['zonen']) for d in st]}; Ring B roh abw {abw[t].max()*100:.1f} cm an (10|10) ausgenommen, Ring B ohne Rest-Befund"))
    zr[1] = (zr[1][0], True, {'id': 'B', 'typ': 'bruecke'})
    st = zonen_stosspunkte(zr, zk, rand); aus, gr = zonen_maske(R, pl, True, {'stoss': st, 'pr': zr[1][2]}, rand, zk)
    ub = ((abw > 0.03) | (knick > 15)) & ~aus
    out.append(('F13 Kartenrand-Stoss mit Bruecke bleibt hart', len(st) == 2 and not any(d['ausgenommen'] for d in st) and bool(ub[t].any()),
                f"B typ bruecke: {len(st)} Stosspunkte hart, Ring B an (10|10) gefunden (abw {abw[t & ub].max()*100:.1f} cm)"))
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
         lambda x: x['status'] == 'offen' and any('Eingabe fehlt' in str(b.get('fehler', '')) for b in x['befunde'])),
        ('Q14_zellen', 'Q14', 'ok', 'Bauzone Zellformat (#61, 2 Komponenten + Slot-Punkt): Zellsumme = Soll, Zellmenge deckungsgleich mit CSV',
         lambda x: x['status'] == 'ok' and x['werte']['bauzone_format'] == 'zellen' and x['werte']['bauzone_zellen']['deckungsgleich'] and x['werte']['bauzone_zellen']['komponenten'] == 2),
        ('Q3_logik', 'Q3', 'ok', 'zackige Slot- und Bauzonen-Polygone + Zellpunkte in zonen.geojson, Q3-Quelle ohne Layer-Filter: Logikschichten ausgeschlossen',
         lambda x: x['status'] == 'ok' and x['werte']['ausgeschlossen_logikschicht'] >= 2),
        ('Q3_bruecke', 'Q3', 'offen', 'F14: Brueckenrechteck (Platzhalter) - Ecken 90 Grad = offener Befund P5 (nicht ok, nicht Ausnahme)',
         lambda x: x['status'] == 'offen' and any(b.get('offen') == 'P5' and b['id'] == 'flaechentyp_br01' for b in x['befunde']) and 'flaechentyp_br01' in x['werte']['bruecke_offen_p5']['ringe']),
        ('Q3_bruecke_p5', 'Q3', 'ok', 'F14 P5-Regel an (konfig q3_bruecke_p5.aktiv): 4 Deckecken je +-0,5 m frei, Laengsseiten glatt -> ok',
         lambda x: x['status'] == 'ok' and len(x['werte'].get('p5_deckecken', [])) == 4 and not x['werte']['bruecke_offen_p5']['ringe']),
        ('Q3_wegende', 'Q3', 'ok', 'F15: Delle ~4,1 cm (Knick 13 Grad) an Grund-Zone 2 m vor Wegende W5 -> Ausnahme A-DV2-01',
         lambda x: x['status'] == 'ok' and x['werte']['wegenden_ausnahme']['abschnitte'] >= 1 and list(x['werte']['wegenden_ausnahme']['ringe']) == ['flaechentyp_gr01']),
        ('Q14_ausnahme', 'Q14', 'ok', 'W9/0 fehlt, steht aber in q14_ausnahmen (wie A-DV2-02): Ausnahme statt Fehler',
         lambda x: x['status'] == 'ok' and x['werte']['wege_ausnahme'] == ['W9/0 (A-TEST)'] and any(b.get('ausnahme') == 'A-TEST' for b in x['befunde']))):
        baue_dummy.baue(tmp / v, v)
        x = lauf(v, {q})['regeln'][q]
        good = bool(pruef(x)); ok_ges &= good
        w = x['werte']; det = {k: w.get(k) for k in ('p5_regel', 'p5_deckecken', 'bruecke_offen_p5', 'wegenden_ausnahme', 'bauzone_format', 'bauzone_zellen', 'ausgeschlossen_logikschicht', 'wege_ausnahme', 'uv2_enge_kurve_dreiecke', 'uv2_enge_kurve_ueber_10pct_gekennzeichnet', 'uv2_enge_kurve_max_abw', 'kurvenradius_min_m', 'uv2_ueber_10pct', 'bauzone') if k in w}
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
