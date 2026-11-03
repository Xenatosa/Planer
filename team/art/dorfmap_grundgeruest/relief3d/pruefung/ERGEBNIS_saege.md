# Ergebnis Saege: Ziel nicht erreicht

Der angegebene Basisstand und die Relief-Ausgaben bleiben erhalten. Keine der geprüften Varianten senkte `R9_saegezahn` unter 34, ohne eine andere Vorgabe zu verletzen. Deshalb ist keine Geometrieänderung im Endstand enthalten. `WANDSTREIFEN` blieb aus.

## Ursachenmessung

`r9_form.py` liest `G` aus `relief_daten.json.gz`; die späteren Anzeigeänderungen in `GB` beeinflussen diese Regel nicht. Der Diagnose-Snapshot `g_rampen` ist bytegleich mit dem von R9 geprüften `G`.

Alle 34 abschließend betroffenen Kacheln erfüllen die R9-Bedingung bereits im Snapshot `g_wandmodell`, also innerhalb der t42u-Wandmodell-Stufe. Erosion und Rampen verändern dort die Zahl der kurzen Kantenfragmente, aber nicht die Zahl der betroffenen Kacheln. Die genaue erste Abweichung liegt damit im t42u-Aufbau aus Sprungmaske `J`, Wandgewicht `wz`, Wandfläche `Gsamp` und Interpolation; die Diagnose isoliert diese Teilschritte nicht einzeln.

| Snapshot in `gen_relief.py` | R9-Kacheln | Fragmente D1 | Fragmente G1 | Fragmente D2 |
|---|---:|---:|---:|---:|
| `g_wandmodell` | 34 | 59 | 43 | 0 |
| `g_erosion` | 34 | 55 | 47 | 0 |
| `g_rampen` / geprüftes `G` | 34 | 41 | 34 | 0 |

Die abschließenden R9-Meldungen liegen in D1 bei `(140,0|9,2)` mit 41 Fragmenten und in G1 bei `(259,6|20,8)` mit 34. Für alle 34 gemeldeten Kacheln gibt es schon im ersten Wandmodell mindestens drei Fragmente; ihre genauen Schwerpunktkoordinaten können sich in Erosion und Rampen verschieben.

## Ergebnis der Variantenproben

Die Proben wurden einzeln und deterministisch ausgeführt. Keine wurde übernommen.

| Quellstufenprobe | R9 danach | Weitere Beobachtung | Grund verworfen |
|---|---:|---|---|
| `WANDMASKE_SIG=2.5` und `4.0` | 34 | D2 änderte sich; beim stärkeren Wert bis 2,4 cm in `G` | D2-Regression, keine R9-Senkung |
| `WANDJ_GLATT=1/2` (3×3/5×5 schließen) | 34 | D2 blieb bytegleich; R9w stieg um 3 bzw. 2 | keine R9-Senkung |
| `WANDJ_GLATT=3` (3×3 öffnen) | 34 | D2 änderte sich; Wandklassifizierung und Wanddreiecke verschoben sich | D2-Regression, keine R9-Senkung |
| `RIBG=1.0` | 34 | `G` blieb in D2 gleich, `GB` wich dort um bis zu `1,8e-7` ab | D2 nicht bytegleich |
| Kanten-Glättung, isotrop `0.5` / wandseitig `1.0` | 34 | R9w stieg um 13 bzw. 39 | Regelanstieg über +5 |
| Kanten-Glättung tangential `0.5` / `1.0` | 34 | R9w stieg um 3 bzw. 9; `t42u` blieb 0 | keine R9-Senkung; stärkere Variante über +5 |

Diese Messungen zeigen, dass die getesteten Masken- und Glättungsänderungen den R9-Kachelzähler nicht senken. Die stärkere Glättung verschiebt stattdessen Wand- und Hangklassifizierungen. Für einen nächsten Versuch müsste die Kontur innerhalb der t42u-Flächenerzeugung anders modelliert werden; ein nachgelagerter `GB`-Filter erreicht den R9-Prüfer nicht.

## Regeln vorher und nachher

Der Endstand entspricht dem angegebenen Ausgangswert. Die Werte vor und nach sind deshalb für jede Regel gleich.

| Prüfer | Regel | Vorher | Nachher |
|---|---|---:|---:|
| `pruefe_regeln` | R1_blind | 24 | 24 |
| `pruefe_regeln` | R2_getrennt | 15 | 15 |
| `pruefe_regeln` | R3_laengs_m | 35 | 35 |
| `pruefe_regeln` | R3_quer_pct | 23 | 23 |
| `pruefe_regeln` | R3_woelb_m | 22 | 22 |
| `pruefe_regeln` | R5_loch | 17 | 17 |
| `pruefe_regeln` | R6_wasser_schnee | 4 | 4 |
| `pruefe_regeln` | G2_spitze_oben | 3 | 3 |
| `pruefe_regeln` | G3_spitze_unten | 3 | 3 |
| `pruefe_regeln` | G2_spitze_oben_fein | 8 | 8 |
| `pruefe_regeln` | G3_spitze_unten_fein | 2 | 2 |
| `pruefe_regeln` | G5_beule_klippe | 68 | 68 |
| `pruefe_regeln` | G6_facette | 220 | 220 |
| `pruefe_regeln` | G7_wand_glatte_flaeche | 1 | 1 |
| `pruefe_regeln` | G8_fluss_nicht_bis_rand | 1 | 1 |
| `pruefe_regeln` | T1_fleckrand | 94 | 94 |
| `pruefe_regeln` | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 |
| `pruefe_regeln` | T3_streifen_ringe_bildpruefung_offen | 1 | 1 |
| `pruefe_regeln` | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 |
| `pruefe_regeln` | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 |
| `pruefe_regeln` | G7b_wandkontur_rauheit | 1 | 1 |
| `pruefe_regeln` | G7b_wandkontur_kantenschaerfe | 1 | 1 |
| `pruefe_regeln` | G7b_wandkontur_feld | 24 | 24 |
| `pruefe_regeln` | **Summe** | **570** | **570** |
| `r8_kreuzung` | R8_stufe | 9 | 9 |
| `r8_kreuzung` | R8_gitter | 10 | 10 |
| `r8_kreuzung` | R8_quer | 5 | 5 |
| `r8_kreuzung` | R8a_wegende | 24 | 24 |
| `r8_kreuzung` | **Summe** | **48** | **48** |
| `r9_form` | R8b_delle | 25 | 25 |
| `r9_form` | R9_saegezahn | 34 | 34 |
| `r9_form` | R9w_wellen | 275 | 275 |
| `r9_form` | **Summe** | **334** | **334** |

### D1, G1 und D2 je Kachel

Die Einträge zeigen Vorher → Nachher. D2 hat acht bereits vorhandene `pruefe_regeln`-Treffer; es kam keiner hinzu. R8 und R9 bleiben in D2 bei null.

| Prüfer | D1 | G1 | D2 |
|---|---|---|---|
| `pruefe_regeln` | 36 → 36 (R1 2, R2 1, R3 längs 6, R3 quer 11, R3 Wölbung 10, G5 1, G6 5) | 13 → 13 (R1 1, R3 längs 1, R6 3, G3 fein 1, G6 4, T1 3) | 8 → 8 (R2 1, T1 7; keine neuen Treffer) |
| `r8_kreuzung` | 8 → 8 (2, 2, 1, 3) | 1 → 1 (nur R8a: 1) | 0 → 0 |
| `r9_form` | 26 → 26 (R8b 2, R9 1, R9w 23) | 8 → 8 (R8b 1, R9 1, R9w 6) | 0 → 0 |

## Pflichtprüfungen und Bilder

- `python3 gen_relief.py && python3 baue_html.py`: erfolgreich.
- Danach wurde `zellen_relief.csv` wie vorgegeben auf den Branch-Stand zurückgesetzt. Die 1.806 D2-Zeilen des unmittelbar erzeugten CSV waren davor mit dem zurückgesetzten Stand identisch.
- Raycast: `offen_innen=0`, `punkte=0`.
- `pruefe_t42u.py`: Summe 0.
- LOD1: 1.174.554 gerenderte Dreiecke, unter 1,3 Mio.
- D2-Slices in `G`, `GB` und `WV`: bytegleich zum Ausgangsbuild.
- `export_gate.sh`: **rot**, weil `pruefe_regeln.py` weiterhin 570 Treffer meldet. Das ist der unveränderte Ausgangswert; ein grünes Export-Gate wurde nicht erreicht.

Ton-Nahbilder mit derselben Kamera, Clay-Material und LOD0:

| Kachel/Kamera | Vorher | Nachher | Vergleich |
|---|---|---|---|
| D1, Ziel um 140\|35 | [D1 vorher](bilder/saege_vor/D1_140_35.png) | [D1 nachher](bilder/saege_nach/D1_140_35.png) | SHA-256 identisch |
| G1 | [G1 vorher](bilder/saege_vor/G1_wand.png) | [G1 nachher](bilder/saege_nach/G1_wand.png) | SHA-256 identisch |

Die vorhandenen Wanddetails und Kanten sind im Endbild unverändert; damit sind weder neue Zähne noch eine zusätzliche Glättung entstanden. Die schon vorher sichtbaren kurzen Kantenunregelmäßigkeiten bleiben bestehen und gelten ausdrücklich nicht als behoben.

## Annahmen, Grenzen und offene Punkte

- Die Diagnose lokalisiert den Beginn aller 34 R9-Kachelmeldungen auf das t42u-Wandmodell. Innerhalb dieses Blocks wurde nicht gemessen, ob `J`, `wz`, die Wandflächenfunktion oder deren Interpolation den größten Anteil hat.
- Die Zellquellen, Dorfkarte und das Overlay wurden nicht geändert. Es wurde keine Ergebnisdatei auf eine Referenz zurückgesetzt, um einen R9-Wert vorzutäuschen; die vorgeschriebene Rücksetzung betraf nur das generierte `zellen_relief.csv`.
- Die Zielsenkung von R9 wurde nicht erreicht. Das Export-Gate bleibt rot, und die vorhandenen R9-Kanten bleiben offen.
- Nächster sinnvoller Schritt: die t42u-Konturform selbst mit einer Methode untersuchen, die Zellmittel, Zell-Ecken, D2 und die sichtbare D1-Klippe gleichzeitig erhält. Dafür liegt hier noch keine bestandene Variante vor.
