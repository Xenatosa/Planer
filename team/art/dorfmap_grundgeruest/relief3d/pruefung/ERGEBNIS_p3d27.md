# Ergebnis p3d27

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d27` · Branch `art/dorfmap-p3d27` · Basis `5089c33` (`origin/art/dorfmap-p3d26`) · Kosten **0 EUR**.

`[S]` Sechs serielle V3-Float32-Proberunden abgeschlossen; keine Runde erfüllt alle harten Ziele, deshalb **kein Mesh gebaut** und der Auftrag endet nach Schritt 4. Die offizielle Probe lief auf der temporären V3-Quelle und dem unveränderten Transfer.

Marker: `[S]` direkt gemessen oder unverändert ausgeführter Prüfer/Test · `[R]` Modellbefund oder abgeleitete Diagnose · `[A]` Annahme · `[F]` Freigabe.

## 0. Bestandstests, Bereinigung und Kalibrierung

`[S]` `python3 -m pytest -q neu/tests` wurde auf p3d26-HEAD `5089c33` und in einem abgetrennten `/tmp`-Worktree auf `89c61ce` ausgeführt. Beide Läufe: **26 bestanden, dieselben 5 fehlgeschlagen** (85,74 s bzw. 84,33 s):

| Test | Fehler in beiden Läufen |
|---|---|
| `test_wegende_allgemein_mesh_ohne_blindenden` | 20 R8a-Wegenden statt 0 |
| `test_saegezahn_d1_mesh_count` | D1-Sägezahnwert 86 statt 0 |
| `test_verwaschene_wand_d1_kantenschaerfe` | 2,24 statt mindestens 3,00 Graustufen/Pixel |
| `test_wegende_f1_c1_meshmessung` | F1 0,17 m statt höchstens 0,10 m; C1 meldet 0 explizite Wegenden |
| `test_schattenartefakt_renderbild` | 0,307 statt höchstens 0,25 Graustufen |

`[R]` Alle fünf Fehler bestanden schon auf `89c61ce`; die p3d26-Ausnahme hat sie nicht verursacht. Tests, Schwellen und Ausnahme-Implementierung blieben unverändert.

`[S]` `codex_jobs/tools/p3d23/diagnose_slack_p3d23.py` ist exakt auf `89c61ce` zurückgesetzt; die ausnahmefähige Arbeitskopie liegt als `codex_jobs/tools/p3d27/diagnose_slack_p3d27.py`. Die p3d27-Probe-, Runner- und Ableitungsskripte sowie JSON-Belege liegen separat unter `codex_jobs/tools/p3d27/`.

`[S]` Die R3-Kalibrierung wurde einmal bestätigt: D1 `6/17/19`, Höhenhash `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`, Transfer bytegleich. [Kalibrierungsbeleg](../../../../../codex_jobs/tools/p3d27/results/p3d27_R3_calibration_after.json).

## 1. V3 Float32-Probe mit Checker-in-the-loop

`[S]` Sechs Runden, jeweils höchstens 600 s Solve-Zeit, strikt seriell und mit allen 22 Familien. Runde 3 und 5 erreichten das Zeitlimit, hatten aber einen zulässigen Solver-Incumbent, der jeweils direkt durch den offiziellen Float32-Prüfer lief. Nach jeder Runde wurden frische G5-/R5-Loch-/G11-Schnitte ergänzt; die Event-Schnitte stiegen von 50 auf 1.426. Quelle `/tmp/p3d22_v3_source.json.gz` SHA-256 `b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6`; Transfer `neu/p3d21_transfer_base_route3_v29.json` SHA-256 `07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287`.

`[S]` Die Zählwerte je Runde stehen als Gesamtzahl und D1/G1/D2. Die Reihenfolge in jeder Klammer ist **D1/G1/D2**.

| Runde | `pruefe_regeln` gesamt (D1/G1/D2) | R8 gesamt (D1/G1/D2) | R9 gesamt (D1/G1/D2) | Solver | Prüferbeleg |
|---:|---:|---:|---:|---|---|
| 1 | 777 (242/13/8) | 49 (10/0/0) | 333 (14/13/0) | Optimal | [Runde 01](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round01_official_probe.json) |
| 2 | 833 (298/13/8) | 50 (11/0/0) | 331 (12/13/0) | Optimal | [Runde 02](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round02_official_probe.json) |
| 3 | 812 (277/13/8) | 44 (5/0/0) | 331 (12/13/0) | Time limit reached; feasible incumbent | [Runde 03](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round03_official_probe.json) |
| 4 | 820 (285/13/8) | 45 (6/0/0) | 330 (11/13/0) | Optimal | [Runde 04](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round04_official_probe.json) |
| 5 | 823 (288/13/8) | 45 (6/0/0) | 327 (9/13/0) | Time limit reached; feasible incumbent | [Runde 05](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round05_official_probe.json) |
| 6 | 785 (250/13/8) | 47 (8/0/0) | 329 (10/13/0) | Optimal | [Runde 06](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round06_official_probe.json) |

`[S]` Rundenziele, jeweils als gemessener Istwert; Kreuzungs-Quer ist „kein Treffer“ falls `—`. R3-Spalten sind D1 längs/quer/wölbung.

| Runde | R5-Spitze D1 | G6 D1 | R8b D1 | G3 D1 | R9w gesamt | G5 gesamt / D1 | R5-Loch gesamt / D1 | R4-Schlucht D1 | R3 D1 längs/quer/wölbung | Kreuzung Stufe / Gitter / Quer | R8a D1 unzulässig |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|
| 1 | 0 | 1 | 11 | 0 | 266 | 145 / 78 | 121 / 104 | 5 | 6/7/7 | 0.116 m / 0.019 m / — | 2 |
| 2 | 0 | 0 | 5 | 0 | 270 | 139 / 72 | 199 / 182 | 7 | 6/7/7 | 0.116 m / 0.019 m / — | 2 |
| 3 | 0 | 0 | 7 | 0 | 268 | 129 / 62 | 187 / 170 | 7 | 6/7/7 | 0.116 m / 0.019 m / — | 0 |
| 4 | 0 | 2 | 5 | 0 | 269 | 119 / 52 | 203 / 186 | 8 | 6/7/7 | 0.116 m / 0.019 m / — | 0 |
| 5 | 0 | 1 | 5 | 0 | 266 | 106 / 39 | 202 / 185 | 9 | 21/7/7 | 0.116 m / 0.019 m / — | 0 |
| 6 | 0 | 2 | 5 | 0 | 268 | 101 / 34 | 186 / 169 | 7 | 6/7/7 | 0.116 m / 0.019 m / — | 0 |

`[S]` Round 6 verfehlt R8b D1 (5 statt ≤1), G5 gesamt/D1 (101/34 statt ≤69/2), R5-Loch gesamt/D1 (186/169 statt ≤22/5) und D1-R4-Schlucht (7 statt 0). Runde 5 verfehlte zusätzlich R3 längs D1 (21 statt ≤6); Runde 6 ist wieder bei `6/7/7`. R5-Spitze D1=0, G6 D1=2, G3 D1=0, R9w=268 und die Kreuzung (0,116 m Stufe; 0,019 m Gitter; kein Quer-Treffer im Cluster) halten ihre Einzelziele.

`[R]` Nach den Rundungen 1–2 wurden im Modell 0,00001 m innere Float32-Puffer unter den offiziellen Endstufen- und R8a-Grenzen ergänzt; offizielle Prüferregeln oder Ausnahmen wurden nicht geändert. Dadurch sind ab Runde 3 die D1-R8a-Treffer einschließlich nicht erlaubter R8a-Enden auf 0. In Runde 1–2 meldete der Prüfer neben dem ausdrücklich erlaubten rampe_2-Start bei `126,5|31,6` zwei zusätzliche R8a-Enden; der zulässige rampe_2-Ausnahmefall wird in der Zielauswertung nicht als unzulässig gewertet. Endstufenmodell: Grenze 0,054 m, interner Puffer 0,00001 m, kein Modellverstoß in Runde 3–6.

`[S]` Vollständige Rundenergebnisse, Cuts, Solver- und Prüferdaten: [Checker-in-the-loop JSON](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_checker_loop.json) und [kompakte finale Gate-Zusammenfassung](../../../../../codex_jobs/tools/p3d27/results/p3d27_final_gate_summary.json).

## 2. Regelzahlen Runde 6: vorher / nachher

`[S]` Allgemeine Regeln vergleichen den p3d17-Replay im aktuellen Schema (600 Treffer) mit Runde 6; die historische 9d3f8fc-Basis ohne G11 betrug 596. Die letzte Spalte zeigt D1/G1/D2 in Runde 6. Neue Regeln ohne p3d17-Eintrag haben Baseline 0.

| Regel | p3d17 vorher | Runde 6 nachher | Δ | D1/G1/D2 |
|---|---:|---:|---:|---|
| `G11_baum_an_wand` | 0 | 12 | +12 | 12/0/0 |
| `G11_objekt_schwebt_sinkt` | 4 | 5 | +1 | 3/2/0 |
| `G2_spitze_oben` | 3 | 3 | +0 | 0/0/0 |
| `G2_spitze_oben_fein` | 8 | 8 | +0 | 0/0/0 |
| `G3_spitze_unten` | 4 | 3 | -1 | 0/0/0 |
| `G3_spitze_unten_fein` | 2 | 2 | +0 | 0/0/0 |
| `G5_beule_klippe` | 69 | 101 | +32 | 34/0/0 |
| `G6_facette` | 219 | 218 | -1 | 2/3/0 |
| `G7_wand_glatte_flaeche` | 1 | 1 | +0 | 0/0/0 |
| `G7b_wandkontur_feld` | 25 | 23 | -2 | 0/0/0 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 | 0/0/0 |
| `G7b_wandkontur_rauheit` | 1 | 0 | -1 | 0/0/0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 | 0/0/0 |
| `R1_blind` | 24 | 24 | +0 | 2/1/0 |
| `R2_getrennt` | 15 | 15 | +0 | 1/0/1 |
| `R3_laengs_m` | 35 | 35 | +0 | 6/1/0 |
| `R3_quer_pct` | 29 | 19 | -10 | 7/0/0 |
| `R3_woelb_m` | 31 | 19 | -12 | 7/0/0 |
| `R4_rand` | 1 | 0 | -1 | 0/0/0 |
| `R4_schlucht` | 0 | 7 | +7 | 7/0/0 |
| `R5_loch` | 25 | 186 | +161 | 169/0/0 |
| `R6_wasser_schnee` | 4 | 4 | +0 | 0/3/0 |
| `T1_fleckrand` | 94 | 94 | +0 | 0/3/7 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 | 0/0/0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 | 0/0/0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 | 0/0/0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 | 0/0/0 |

`[R]` Die Regelgrenze „höchstens +5“ ist in Runde 6 bei `G11_baum_an_wand` (+12), `G5_beule_klippe` (+32), `R4_schlucht` (+7) und `R5_loch` (+161) überschritten. Alle übrigen allgemeinen Regeln liegen innerhalb von +5.

`[S]` R8 (Ausgang 48, Runde 6: 47; nach Regel R8_stufe 9/9, R8_gitter 10/11, R8_quer 5/7, R8a_wegende 24/20). R9 (Ausgang 334, Runde 6: 329; R8b_delle 25/27, R9_saegezahn 34/34, R9w_wellen 275/268). R8 D1/G1/D2=`8/0/0`; R9 D1/G1/D2=`10/13/0`. Damit bleibt R9 jede Regel in +5; R8 bleibt ebenfalls in +5.

`[S]` Allgemeine Treffer Runde 6 je Kachel (D1/G1/D2) pro Regel sind in der vorhergehenden Tabelle ausgewiesen. Summen: `pruefe_regeln` **785 / 250 / 13 / 8**; R8 **47 / 8 / 0 / 0**; R9 **329 / 10 / 13 / 0** (gesamt / D1 / G1 / D2). D2 hat keine neuen allgemeinen Treffer; D2-R8 und D2-R9 bleiben 0. G1-Höhenhash `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` und D2-Höhenhash `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` stimmen mit den vorgegebenen Werten überein.

## 3. Verbleibende Runde-6-Treffer in D1

`[S]` Orte sind aus den offiziellen Trefferlisten im Float32-Probe-JSON übernommen und auf Prüferkoordinaten mit einer Dezimalstelle geschrieben.

**G11 Baum-an-Wand (12):**

`157.8|8.5; 159.2|11.5; 163.5|11.7; 160.3|9.3; 158.9|8.3; 138.7|12.1; 140.0|6.7; 139.9|5.0; 140.8|6.0; 159.3|9.4; 136.2|39.8; 138.2|37.8`

**G5 Beule/Klippe (34):**

`141.0|2.0; 143.5|3.0; 150.2|5.5; 151.5|6.5; 154.0|6.5; 152.5|7.0; 151.0|7.5; 138.5|8.0; 153.5|8.0; 158.5|9.5; 139.5|10.0; 157.0|10.5; 159.0|10.5; 161.0|11.0; 162.5|11.5; 159.0|12.0; 139.5|12.5; 160.5|12.5`

`141.0|13.5; 143.5|18.5; 146.5|18.8; 146.0|20.0; 146.5|20.5; 138.5|21.5; 139.5|21.5; 141.0|22.0; 142.0|22.0; 146.5|22.0; 134.5|24.0; 134.0|24.5; 156.9|30.8; 158.0|31.5; 131.0|34.5; 153.5|39.0`

**R4 Schlucht (7):**

`128.0|31.4; 135.2|30.6; 139.2|30.3; 152.8|28.3; 148.5|2.5; 150.9|14.0; 156.2|21.5`

**R8b Delle (5):**

`146.0|26.5; 146.5|27.0; 160.0|31.0; 160.5|31.5; 151.0|36.0`

**R5 Loch (169):**

`141.0|7.5; 141.5|2.0; 145.0|2.0; 143.5|3.5; 144.0|2.5; 146.0|3.0; 140.0|3.5; 145.5|4.0; 146.5|5.0; 143.0|5.0; 142.0|5.0; 149.5|5.0; 142.5|5.5; 143.0|9.0; 142.0|6.0; 140.5|9.0; 144.5|8.5; 146.0|9.5`

`152.5|9.5; 140.0|10.0; 143.0|10.0; 155.0|11.0; 139.0|11.5; 144.0|11.5; 157.0|11.5; 140.0|12.0; 136.5|12.5; 145.5|12.5; 144.5|13.0; 146.0|13.0; 141.5|13.5; 142.0|14.0; 154.0|14.0; 154.5|15.5; 161.5|15.0; 162.0|15.5`

`162.5|16.0; 166.5|16.0; 147.5|16.5; 159.5|17.0; 146.0|17.0; 141.5|17.5; 143.5|17.5; 142.0|18.0; 144.5|18.0; 163.0|18.0; 143.5|19.5; 144.0|18.5; 145.0|19.0; 163.5|19.0; 144.5|19.5; 150.5|20.0; 156.5|19.5; 144.0|20.5`

`145.0|20.0; 147.0|20.0; 150.5|21.5; 156.0|20.0; 161.5|20.0; 163.5|20.5; 145.5|21.0; 149.5|20.5; 155.5|20.5; 137.0|24.0; 155.0|21.5; 166.5|21.5; 139.0|21.5; 142.0|23.5; 143.0|21.5; 144.5|21.5; 146.0|21.5; 160.0|21.5`

`128.0|29.0; 132.0|22.0; 133.5|22.0; 134.5|22.0; 144.0|22.0; 145.0|22.0; 151.0|26.0; 156.5|22.0; 157.0|24.5; 167.0|24.5; 134.0|22.5; 142.5|22.5; 143.5|22.5; 154.5|23.0; 146.0|23.0; 155.5|24.5; 127.0|23.5; 134.5|23.5`

`143.0|23.5; 154.0|24.0; 134.0|24.0; 136.5|24.5; 152.5|24.0; 164.0|24.0; 139.0|25.5; 161.5|24.5; 134.0|25.0; 156.5|25.5; 160.5|25.0; 163.5|25.0; 142.5|26.0; 159.0|25.5; 165.0|25.5; 167.5|25.5; 158.0|26.5; 161.0|26.5`

`148.0|27.5; 149.0|27.0; 167.5|27.5; 141.5|27.5; 161.0|28.0; 136.0|28.0; 143.5|28.0; 144.5|28.0; 159.0|28.0; 157.0|28.5; 166.0|31.0; 142.0|29.0; 144.0|29.0; 161.0|33.0; 129.5|29.5; 145.0|29.5; 157.5|29.5; 161.5|29.5`

`129.0|30.5; 159.5|34.5; 162.5|30.5; 136.5|31.5; 148.5|32.0; 149.5|32.0; 149.5|33.5; 151.0|32.5; 154.5|33.5; 162.5|33.5; 143.5|34.0; 146.0|34.5; 149.0|34.5; 156.0|34.5; 167.5|35.0; 134.5|35.0; 142.5|35.5; 147.5|42.5`

`156.5|35.0; 158.5|35.0; 167.0|36.0; 138.0|35.5; 148.0|37.5; 162.0|36.0; 135.5|37.0; 138.5|36.0; 145.5|38.0; 129.5|36.5; 131.0|37.0; 141.5|39.5; 132.0|37.5; 134.0|37.5; 153.5|38.0; 132.0|39.0; 135.0|38.0; 134.0|38.5`

`135.5|40.0; 149.0|38.5; 131.5|40.5; 145.5|39.5; 148.0|39.0; 143.5|39.5; 146.0|41.0`

`[R]` Für 15 weitere R5-Komponenten ließ sich kein Flutsattel zum Ableiten eines gültigen Ereignisschnitts gewinnen; sie wurden nicht durch erfundene Schnitte ersetzt. Orte: `144.5|13.0; 147.5|16.5; 146.0|17.0; 147.0|20.0; 139.0|21.5; 142.0|23.5; 143.0|21.5; 144.5|21.5; 144.0|22.0; 145.0|22.0; 142.5|22.5; 143.5|22.5; 146.0|23.0; 143.0|23.5; 139.0|25.5. Begründungs- und Detailwerte: [Runde-6-Ableitung](../../../../../codex_jobs/tools/p3d27/results/p3d27_V3_round06_derived_summary.json).

## 4. Mesh-Gate, Annahmen und offene Punkte

`[S]` Kein Mesh-Bau: `gen_relief.py`, `baue_html.py` und alle Mesh-Gates wurden nach der verfehlten Probe nicht ausgeführt. Folglich gibt es keinen Mesh-Delta-Vergleich gegen VAR0/p3d6/p3d8/p3d16/p3d17/p3d18, keinen Mesh-pytest, xvfb-Lochscan, t42u-Nachweis, Klippenmesswert bei `140|35`, LOD1-Dreieckszahl, Vergleich der `zellen_relief`-/`vektor.json`-/`felder.json`-Hashes und keine vorgeschriebenen Vorher-/Nachher-Bilder; `pruefung/bilder_p3d27/` wurde nicht erstellt.

`[S]` Die Float32-Probe selbst zeigt für alle sechs Runden unveränderte G1- und D2-Höhenhashes, keine neuen D2-Regeltreffer sowie keine D2-R8/R9-Treffer. Die Produktions-Mesh-Anforderungen, insbesondere t42u-Summe 0 und LOD1 <1,3 Mio. Dreiecke, sind mangels Mesh nicht nachgewiesen.

`[A]` Die interne 0,00001-m-Rundungsreserve dient nur dem numerischen Solverabstand zu den unveränderten offiziellen Limits; sie ist kein geänderter Prüfergrenzwert. R5 ohne ableitbaren Flutsattel bleibt eine bekannte Lücke des Checker-in-the-loop-Ereignismodells.

`[R]` Die Probe endet am Sechs-Runden-Limit mit erheblichen G5-/R5-Loch-/R4-Treffern und vier Regelüberschreitungen gegenüber der p3d17-Regelbaseline. Sie erlaubt keine Mesh-Freigabe und beantwortet weder die Bildprüfung noch die Mesh-Regressionen.

## Drei-Satz-Schluss

`[S]` Die fünf Bestandstests waren bereits auf `89c61ce` rot, das p3d23-Werkzeug ist zurückgesetzt und R3 wurde mit `6/17/19` bestätigt. `[S]` Sechs V3-Float32-Proberunden wurden geprüft; Runde 6 verfehlt R8b, G5, R5-Loch und R4-Schlucht, daher wurde kein Mesh gebaut. `[F]` Der p3d27-Lauf ist gemäß Schritt 4 beendet; die verbleibenden Treffer und Grenzen sind in Bericht und JSON-Belegen dokumentiert.
