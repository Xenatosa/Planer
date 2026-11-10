# Ergebnis p3d16

**Status: Variante 20 gebaut und geprüft; Ziel verfehlt. Keine weitere Variante.**
Stand: 10.11.2026 · Branch: art/dorfmap-p3d16 · Basis: p3d15 @ cbb1368

## Entscheidung und Änderung

Variante 20 ist als Standard auf Variante 19 aufgebaut: plane_radius_m=2.00, plane_inner_m=2.00 und plane_outer_m=4.0. Die Wegführung in neu/vektor.json blieb unverändert (SHA-256 aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e). Variante 19 und ältere Varianten bleiben schaltbar. Prüfer, Schwellen, Zellquellen und Tests wurden nicht geändert.

Der vollständige gemeinsame Profil-/Kreuzungs-MILP-Nachweis steht im vorherigen Abschnitt dieses Berichts und ist im Commit b14bb72 festgehalten. Der Nachweis war machbar. Das ausgelieferte Mesh erreicht diese Untergrenze im tatsächlichen Transfer jedoch nicht: Der R8-Raster-LP-Untergrenzwert und das Mesh liegen bei 0.158764686 m bzw. 0.158764696 m; die gemeinsame Profil-/R8-Untergrenze bei g=0.45 liegt bei 0.064738629 m. Die Lücke beträgt 0.094026067 m; das Mesh ist damit 2.45-mal so hoch wie die gemeinsame Untergrenze. Gegenüber dem Projektziel 0.116 m fehlen 0.042764696 m. Variante 20 wird deshalb nicht als Zielerreichung freigegeben und es folgt keine Variante 21.

Der innerhalb des RBF/Raster-Transfers eingeführte Minimax-Lauf erreicht sein eigenes Raster-LP-Optimum bis auf 0.000000010 m. Die große Abweichung entsteht somit zwischen der gemeinsamen Stations-/R8-Paarrechnung und der repräsentierbaren glatten Rasterfläche, nicht durch einen nachträglichen Fehler beim Übertragen des Raster-LP-Ergebnisses. Das ist eine Diagnose aus den beiden Optimierungsmodellen. Die Transferparameter zeigen zusätzlich max. Band-Slack 0.585955 m bei 155|27 (Soll 3.797614 m, Feld 4.403569 m) und max. absolute Feldanpassung 1.917075 m. Ohne einen weiteren Build lässt sich der Abstand keinem einzelnen Feldterm als alleiniger Ursache zuordnen.

## Build und Meshwerte

| Messung | Ergebnis | Ziel / Bewertung |
|---|---:|---|
| LOD1-Dreiecke | 134,316 | < 1.3 Mio., bestanden |
| D1-Hash | bf42981fd3c02502a859d70ec9083017e53519092d40ef0c029143b795844759 | neu, nicht in den ausgeschlossenen Hashes |
| G1-Hash | 38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb | unverändert |
| D2-Hash | 749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6 | unverändert |
| Adapter D2-GB-Mesh bytegleich | ja | bestanden |
| Adapter D1-GB-Hash | bf42981f… | neu |
| Adapter G1-GB-Hash | 38afeb30… | unverändert |
| Klippe bei 140|35 | G=GB=7.88403654 m | Soll 7.8840365 m |
| t42u | Summe 0 | bestanden |
| Neu-Viewer Lochscan unter xvfb | 9 Meshes, 88,728 Gelände-Dreiecke, 0 offene Innenkanten, 0 Punkte | bestanden |
| test_gelaende_mesh.py | 4 bestanden | bestanden |
| neu/tests gesamt | 26 bestanden, 5 fehlgeschlagen | Ziel mindestens 26/5 erreicht, aber Suite nicht grün |
| D1 maximale Quellhöhenänderung | 3.014776 m | ≤ 4.0 m, bestanden |

Die fünf Suite-Fehler betreffen: R8a-Wegenden insgesamt 23 statt 0; Sägezahn D1 mit Wert 40 statt 0; Referenz-Wandkantenschärfe 2.24 statt mindestens 3; F1-Wegende R8a 0.17 statt höchstens 0.10 und fehlende C1-Endpunktmessung; Referenz-Schatten hf=0.307 statt höchstens 0.25. Es wurden dafür keine Tests oder Grenzwerte angepasst.

## Untergrenze und gemessene R8-Kreuzung

CELL_M=1.2 m. Die gemeinsame LP-Rechnung nutzt 1,114 lokale R8-Nachbarpaare auf dem 0.25-Map-Einheiten-Raster, 68 Achsstützen, 137 Ebenenkernstützen, die p3d15-Same-Route-Paare sowie den exakten R3-Operator. Der gemeinsame R3-Lauf ist optimal (MIP-Gap 0) und hat in D1 sechs R3-Abschnitte.

| g | isolierte Stufen-Untergrenze | mit R3 D1 ≤ 6 | R3-Abschnitte D1 | engstes lokales Paar mit R3 | Mesh-Messung |
|---:|---:|---:|---:|---|---:|
| 0.45 | 0.064738629 m | 0.064738629 m | 6 | 156.00|28.00: 3.723869 → 156.00|28.25: 3.788608 m | 0.158764696 m |
| 0.60 | 0.052649210 m | 0.052649210 m | 6 | 150.25|30.75: 3.923068 → 150.25|31.00: 3.870419 m | 0.158764696 m |

Ein separater Profil-MILP-Vorlauf vor der gemeinsamen Raster-Minimax-Rechnung ergibt folgende Profile. Er optimiert zuerst Abschnittszahl, danach Same-Route-Summe und Quellverschiebung; er ist nicht der gemeinsame Rasterlauf in der Tabelle oben.

| g | Status | Hc | Ebenenneigung | R3-Abschnitte gesamt / D1 | Paare / Same-Route-Paare | größte Paarneigung | rampe_11 s=45.6→48.9: Δh / Sehne / Neigung |
|---:|---|---:|---:|---:|---:|---:|---|
| 0.45 | optimal | 4.009337 m | 3.000 % | 6 / 4 | 1,075 / 218 | 0.450 | 0.646163 m / 2.538903 m / 25.450 % |
| 0.60 | optimal | 4.029060 m | 3.000 % | 5 / 3 | 1,075 / 218 | 0.600 | 1.226331 m / 2.538903 m / 48.302 % |

Die gebaute Variante nutzt g=0.45. Der R8-Checker misst am Zentrum 152.5|28.5 eine Stufe von 0.159 m (strengere Projektgrenze 0.116 m verfehlt), Gitter 0.373 (Projektziel ≤0.02 m verfehlt) und Quer 3.4 % (Projektziel ≤3 % verfehlt). Der höchste lokale 0.25-Raster-Nachbarschritt im 4-m-Kreis ist 0.158764696 m.

## D1-R8-Treffer: Feinpunkte, Höhen, Stationen und aktive Transferterme

Koordinaten sind Kartenkoordinaten; Höhen und Stationen in Metern. Der R8-Checker fasst Gitter und Quer am Kreuzungszentrum zusammen, sie teilen dort dasselbe kritische Nachbarpaar.

| Treffer | Feinpunkt A → B und Höhen | Beteiligte Stationen | Aktive Transferterme |
|---|---|---|---|
| 152.5|28.5, R8_gitter (0.373) und R8_quer (3.4 %) | 155.25|25.75: 5.038628 → 155.25|26.00: 4.879863 m | rampe_2 idx 117, s=35.1, 155.5448|28.0794; rampe_11 idx 124, s=37.2, 154.1555|25.2253 | rampenkreuzung_gemeinsame_ebene_weicher_rand: gemeinsames Thin-Plate-Spline/RBF-Feld und Rasterfit |
| 148.5|2.5, R8_gitter (0.249) | 149.75|3.00: 13.019716 → 149.75|3.25: 12.891707 m | rampe_11 idx 0, s=0.0, 148.5|2.5 | gemeinsames Kreuzungsfeld plus rampenenden_lokaler_auslauf_ge4m_weich |
| 156.5|37.5, R8_gitter (0.285) | 155.00|36.50: 0.954496 → 155.25|36.50: 0.804046 m | rampe_11 idx 183, s=54.9, 155.0703|36.4581 | gemeinsames Kreuzungsfeld plus rampenenden_lokaler_auslauf_ge4m_weich |
| 126.5|31.6, R8a rampe_2_anfang (0.11) | 126.50|34.00: 12.503831 → 126.75|34.00: 12.389267 m | rampe_2 idx 0, s=0.0, 126.51|31.62 | rampenenden_lokaler_auslauf_ge4m_weich plus rampe_2-Profil im gemeinsamen RBF-Feld |
| 148.5|2.5, R8a rampe_11_anfang (0.23) | 150.50|3.50: 12.997211 → 150.50|3.75: 12.767192 m | rampe_11 idx 0, s=0.0, 148.5|2.5 | rampenenden_lokaler_auslauf_ge4m_weich plus rampe_11-Profil im gemeinsamen RBF-Feld |
| 156.5|37.5, R8a rampe_11_ende (0.19) | 157.50|35.50: 0.871043 → 157.75|35.50: 0.685178 m | rampe_11 idx 189, s=56.7, 156.2818|37.3426 | rampenenden_lokaler_auslauf_ge4m_weich plus rampe_11-Profil im gemeinsamen RBF-Feld |

Die Ausgabe enthält den finalen Blend, nicht die kontrafaktischen Höhen jedes einzelnen Transferterms. Eine numerische Aufteilung der jeweiligen Höhenänderung auf Endauslauf und Kreuzungsfeld wäre ohne Instrumentierung oder weiteren Build nicht belegt. Der Endpunkt 156.5|37.5 bleibt mit lokaler Stufe 0.15045 m, Gitterwert 0.285 und R8a-Wert 0.19 schlechter als p3d11 (0.054 m, kein R8a-Treffer).

## Profile und R3

Das Ebeneninnere hat Hc=4.009337 m, Gradient x=-0.002940514 und z=-0.029855542 (3.0 %), 37 Meshstützen und 222 dichte Stützen; maximale Abweichung von der Ebene 0.02 m. Der interne Profilsolver zählt 4 R3-Abschnitte mit Start in D1 und 6 insgesamt. Der unabhängige Regelprüfer misst jedoch D1-Trefferzahlen 17/22/15 und verfehlt damit die Ziele ≤6/≤7/≤7 sowie die Quergrenze 20 %. Die jeweiligen Maxima sind R3 längs 0.379 m bei 153.7|26.1 (rampe_11), quer 30.7 % bei 146.4|29.2 (rampe_2) und Wölbung 0.434 m bei 154.3|28.2 (rampe_2).

| Route / Stationen | D1 / gesamt | max. |Mesh−Soll| | Minimum / Maximum Mesh−Soll | RMS |
|---|---:|---:|---:|---:|---:|
| rampe_2 | 168 / 197 | 0.020000166 m | -0.020000048 / +0.020000166 m | 0.014974249 m |
| rampe_11 | 191 / 191 | 0.020000375 m | -0.020000287 / +0.020000375 m | 0.015615107 m |

Die Überschreitungen der 0.02-m-Stationsabweichung liegen bei höchstens 0.000000375 m (0.375 µm) und sind als Rohwerte ausgewiesen, nicht weggerundet. Das Build-Manifest rundet den Maximalfehler auf 0.020 m und meldet für seine Achsproben null Werte über 0.02 m. Die genauen Profile stehen in profil_tabelle.csv und profil_messung.json.

## Regeln und Kachelwerte

Die folgende Regel-Tabelle vergleicht die gespeicherten p3d15-Messungen mit p3d16. D1/G1/D2-Spalten zeigen pro Kachel jeweils vorher→nachher. Die historischen Ausgangszahlen von 9d3f8fc waren nur für die Regelsummen dokumentiert, nicht als vollständige Per-Regel-/Per-Kachel-Aufschlüsselung. Deshalb wird die vollständige Tabelle gegen den gespeicherten p3d15-Zwischenstand ausgewiesen.

### pruefe_regeln.py

Gesamt: Ausgang 9d3f8fc = 596; gespeichertes p3d15 = 598; p3d16 = 600 (gegen Ausgang +4, gegen p3d15 +2). D1: 63→65; G1: 11→11; D2: 8→8. Die acht D2-Treffer sind exakt dieselben wie im p3d15-Snapshot; kein neuer D2-Treffer.

| Regel | p3d15 | p3d16 | Δ | D1 vorher→nachher | G1 vorher→nachher | D2 vorher→nachher |
|---|---:|---:|---:|---:|---:|---:|
| G11_baum_an_wand | 2 | 2 | +0 | 2→2 | 0→0 | 0→0 |
| G2_spitze_oben | 3 | 3 | +0 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8 | 8 | +0 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 3 | 3 | +0 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 2 | 2 | +0 | 0→0 | 0→0 | 0→0 |
| G5_beule_klippe | 70 | 67 | -3 | 3→0 | 0→0 | 0→0 |
| G6_facette | 219 | 221 | +2 | 3→5 | 3→3 | 0→0 |
| G7_wand_glatte_flaeche | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 25 | 25 | +0 | 1→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24 | 24 | +0 | 2→2 | 1→1 | 0→0 |
| R2_getrennt | 15 | 15 | +0 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 43 | 46 | +3 | 14→17 | 1→1 | 0→0 |
| R3_quer_pct | 35 | 34 | -1 | 23→22 | 0→0 | 0→0 |
| R3_woelb_m | 26 | 27 | +1 | 14→15 | 0→0 | 0→0 |
| R5_loch | 17 | 17 | +0 | 0→0 | 0→0 | 0→0 |
| R6_wasser_schnee | 4 | 4 | +0 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94 | 94 | +0 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |

### r8_kreuzung.py

Ursprünglicher Vergleichswert: 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24). Gespeichertes p3d15: 47; p3d16: 46. p3d16 hat D1/G1/D2 = 7/0/0. R8 pro Regel:

| Regel | p3d15 | p3d16 | Δ | D1 vorher→nachher | G1 vorher→nachher | D2 vorher→nachher |
|---|---:|---:|---:|---:|---:|---:|
| R8_gitter | 11 | 11 | +0 | 3→3 | 0→0 | 0→0 |
| R8_quer | 5 | 5 | +0 | 1→1 | 0→0 | 0→0 |
| R8_stufe | 8 | 7 | -1 | 1→0 | 0→0 | 0→0 |
| R8a_wegende | 23 | 23 | +0 | 3→3 | 0→0 | 0→0 |

Die strengere p3d16-Stufenzielzahl an der Kreuzung (≤0.116 m) wird trotz der verbesserten Anzahl allgemeiner R8-Treffer verfehlt.

### r9_form.py

Ursprünglicher Vergleichswert: 334 (R8b 25, Sägezahn 34, R9w 275). Gespeichertes p3d15: 343; p3d16: 347. Gegen den Ausgang steigt R9w um 16 (275→291), also mehr als die erlaubten +5. p3d16 hat D1/G1/D2 = 32/13/0. R9 pro Regel:

| Regel | p3d15 | p3d16 | Δ | D1 vorher→nachher | G1 vorher→nachher | D2 vorher→nachher |
|---|---:|---:|---:|---:|---:|---:|
| R8b_delle | 22 | 22 | +0 | 0→0 | 0→0 | 0→0 |
| R9_saegezahn | 34 | 34 | +0 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 287 | 291 | +4 | 27→31 | 12→12 | 0→0 |

## Delta-Vergleiche

Alle vier Delta-Aufrufe endeten mit Exitcode 1, weil Gate-Anstiege vorhanden sind. Die Zahl zählt positive Regel/Kachel-Deltas aufsummiert (nicht Bildindikatoren).

| Vergleich | positive Regel/Kachel-Deltas | Exit von delta.py |
|---|---:|---:|
| VAR0 → p3d16 | 51 | 1 |
| p3d6 → p3d16 | 56 | 1 |
| p3d8 → p3d16 | 49 | 1 |
| p3d15 → p3d16 | 10 | 1 |

p3d15→p3d16 hat vier Gate-Anstiege: G6_facette D1 +2, R3_laengs_m D1 +3, R3_woelb_m D1 +1 und R9w_wellen D1 +4; Summe +10 positive Treffer. Damit wird das Ziel von null Gate-Anstiegen verfehlt. Gegen p3d8 verschlechtern sich D1 G6 (0→5), G11 (0→2) und R9w (21→31), entgegen der dortigen Nichtverschlechterungsziele. Keine neuen D2-Gate-Treffer.

## Bilder und Sichtprüfung

Die sechs p3d16-Bilder liegen in pruefung/bilder_p3d16/nachher/; die Vergleichsstände p3d8 und p3d15 liegen in den jeweiligen vorher_p3d8/ und vorher_p3d15/-Ordnern. Alle sechs Dreiervergleiche (p3d8, p3d15, p3d16) wurden mit Clay beziehungsweise Streiflicht gerendert und angesehen. Der Kreuzungs-Clay-Wert beträgt 244 Facetten (Ziel ≤317, erreicht). Das Streiflicht zeigt weiterhin eine Falte/Knick am Wandfuß bei rampe_11; die geforderte weiche, faltenfreie Ansicht ist nicht erreicht. Das Wegende bleibt sichtbar problematisch. D2- und G1-Meshes sind bytegleich beziehungsweise hashgleich zu ihrem Referenzstand; die Draufsicht von D2 ist visuell unverändert.

| Bild | Facetten | Kanten-Zähne | Normalensprünge | Löcher (Bildindikator) | Flecken |
|---|---:|---:|---:|---:|---:|
| D1 Kreuzung, Clay | 244 | 204 | 536 | 0 | 0 |
| D1 Wandfuß 140|35, Clay | 443 | 1,079 | 3,542 | 65 | 70 |
| D1 Wegende, Clay | 816 | 1,059 | 2,419 | 62 | 53 |
| D1 Kreuzung rampe_11, Streiflicht | 803 | 190 | 2,302 | 1 | 1 |
| G1 Wandfuß, Clay | 530 | 911 | 3,393 | 44 | 34 |
| D2 Draufsicht, Clay | 13 | 313 | 2,275 | 12 | 6 |

Die Bildindikatoren sind nur reproduzierbare Sichtindikatoren; für die visuelle Entscheidung gelten die gespeicherten PNGs. Der Neu-Viewer-Lochscan meldet separat null offene Innenkanten und null Punkte.

## Annahmen, Grenzen und offene Punkte

- Die Machbarkeitsuntergrenze gilt für das dokumentierte lokale Modell, CELL_M=1.2 m, die 0.25-Map-R8-Nachbarpaare, den exakten R3-Operator, Same-Route-Paare und die ausgewiesenen Achs-/Ebenengrenzen. Sie ist keine Garantie, dass die weich ausgeblendete Rasterfläche dieselbe Untergrenze erreicht.
- Der Profilsolver-Abschnittszähler und die unabhängigen R3-Regeltreffer sind verschiedene Messgrößen. Für das Projektziel zählen die unabhängigen Gate-Messungen; sie verfehlen die Grenzwerte.
- D2 blieb im Mesh und in den Regel-Gates unverändert. Die G1-Hash-Prüfung blieb ebenfalls gleich. Keine Quellwerte oder Wege wurden geändert.
- Wände und Wandfuß, G1, D2, Sägezahn, R8 außerhalb D1 und andere Wegenden waren nicht das Arbeitsthema; die hier aufgeführten Sicht- und Gate-Regressionswerte werden trotzdem vollständig berichtet.
- Offen bleiben die Transferlücke zwischen gemeinsamer LP und Rasterfläche, die R3-Gate-Zahlen, Kreuzungsstufe/Gitter/Quer, Endpunktqualität, der sichtbare Wandfußknick, R9w-Anstieg sowie die fünf Neu-Testfehler. An Solvergrenzen, Prüfern oder Quellwegen wurde nichts gelockert.

## Prüfartefakte

Bericht, Zahlen, Roh-Delta-JSON/Markdown, Profilwerte, D1-R8-Feinpunktdetails und alle verlangten Vorher-/Nachher-Bilder liegen unter pruefung/ERGEBNIS_p3d16.md und pruefung/bilder_p3d16/. Der Laufzeitnachweis befindet sich außerhalb des Worktrees unter /workspace/codex_jobs/log_p3d16.txt.
