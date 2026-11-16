# P2 Wegnetz – Ergebnis (Basis art/dorfmap-fertig @dc8c174, ohne L1)

Branch `wege/dorfmap-p2-gen` = dc8c174 + Cherry-Picks a0c8697 (→3d24796), 93398fc (→1a0c4f1) + Analyse + Erzeugung.

## Erzeugung (tatsächlich verwendet) [S]
1. `python3 gen_relief.py` (Legacy, P2_RAMPEN=1 Standard) → relief_daten.json.gz, zellen_relief.csv, glb, Prüfer-JSONs
2. `RELIEF_NEU=1 RELIEF_GELAENDE_VAR=0 python3 gen_relief.py` → neu/relief_neu.json.gz, neu/build.json
3. `RELIEF_NEU=1 BUNDLE_OUT=/tmp/p2_bundle_r.js python3 baue_html.py` → index.html (kein Schreiben nach /tmp/w3)
4. Gate: loch_o18g.js (eigene Ausgabe /tmp/p2_gate_loch.json), pruefe_regeln.py, r8_kreuzung.py, r9_form.py
5. Nahbilder: `RELIEF_GELAENDE_VAR=0 sh pruefung/alle_kacheln/alles.sh /tmp/p2_p10_nachher`

`RELIEF_GELAENDE_VAR=0` ist nötig, weil Kreuzungsvariante 24 rampe_2/rampe_11 voraussetzt (Abbruch „Erwartete D1-Kreuzung … fehlt“). Folge: D1/G1-Viewer-Meshes kommen direkt aus GB. D2 unverändert (Vertex-Hash D2 surface ebeb46a1… vorher = nachher).
NACH_L1.md (Legacy-baue_html) ist damit überholt – dieser Ablauf gilt.

## Zusätzliche Änderungen [S]
- gen_relief.py: G11-Block (nur P2): Bäume/Felsen/Findlinge/Steine/Felsblöcke auf sichtbare Höhe gesetzt, wenn Abweichung >0,6 m (147/16/8/3). Ohne ihn G11 0→174.
- pruefe_regeln.py: nur Absturzschutz `_KP` bei <12 Rampen (toter Code, `_ausnahme()` aus). Nullprobe auf Vorher-Daten: identisch 570. Schwellen unverändert.

## Gate vorher → nachher
| Datei | vorher | nachher |
|---|---|---|
| regeln | 570 | 499 |
| r8 | 48 | 3 |
| r9 | 334 | 278 |
| Trefferkarte gesamt | 952 | 780 |

Familien (regeln): R1 24→1, R2 15→2, R3_laengs 35→2, R3_quer 23→6, R3_woelb 22→6, G5 68→55, G2_fein 8→6, R6 4→4, **G3_fein 2→11, G6 220→239, G7b_feld 24→33, R5 17→22, T1 94→98** (schlechter, s. Ausnahmen), Rest gleich.
r8: R8_stufe 9→1, R8_gitter 10→1, R8_quer 5→0, R8a 24→1. r9: R8b 25→15, R9 34→34, R9w 275→229. lochscan offen_innen 0. G11 0.

## D2 (bitgleich) [S]
GB 749d3c4b…, VC b67dc719…, WV 4b33ed17…, WEGA e6cf61d2… – vorher = nachher. build.json D2 height_sha256 749d3c4b.

## Randprüfung D1|D2 [S]
z 40–46, x 120–174: keine G2/G3/G6 vorher und nachher. Weicher Übergang 4 Zellen (Gewicht 1−d/9).

## D4 „Pfeil“-Wegenden (QA P4) [S]
Ursache war rampe_12 (R1/R8a/R3 bei 127.5|133.5, 130.4|130.8). Rampe entfällt → in D4 keine R1/R8a/R3 mehr. Bild: d4_pfeil_vorher_nachher.jpg. [A] Unten links bleibt eine schmale Rinne sichtbar → Sichtprüfung QA.

## Ausnahmen
1. R1 + R8_stufe/R8_gitter D1 156.5|37.5 (rampe_11, Ende, Lücke 9 Zellen) – D2-Sperre, freigegeben. Bild: ausnahmen_x084_g2_nahbild.png
2. R2 G2 270.9|62.2 (1588) – freigegeben, QA P4. R2 D1 151.2|19.6 (62).
3. R8a D1 148.5|2.5 (0,13 m, Grenze 0,1) – rampe_11 Anfang.
4. R6 4 – beim Dorfmap-Bot.
5. Schlechtere Familien G3_fein/G6/G7b_feld/R5/T1: 142 neue Treffer (>3 Zellen von alten Treffern) mit Messwert + Nahbild vorher|nachher in `ausnahmen/` und `ausnahmen_kandidaten.json` (G6 99, R5 13, T1 11, G3f 10, G7b 9).
   **Wichtig:** R5 C4 121.5|161.5 wächst 1,5 → 147,5 m² (Wert 1,25→3,26), sichtbar als Rinne um das Plateau: c4_r5_vorher_nachher.jpg. Ursache nicht behoben [A: freigelegte Muldenstruktur nach Rampenentfernung].

## Nahbilder
Betroffene Kacheln (37, Liste betroffene_kacheln.txt): `nahbilder_vorher/` und `nahbilder_nachher/`. Vorher-Lauf mit Standard-Variante, nachher mit RELIEF_GELAENDE_VAR=0 (betrifft nur D1/G1).
Trefferkarte: trefferkarte_p2/vergleich.html|png.
