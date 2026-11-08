# Ergebnis p3d8

**Ergebnis: teilweise erreicht.** Variante 5 macht die D1-Kreuzungsfläche eben und verbessert die Kreuzungsbild-Metriken. Die R3-Zielwerte werden verfehlt; der Gesamtvergleich `VAR0 → p3d8` hat 20 statt weniger als 19 Anstiege.

**Branch:** `art/dorfmap-p3d8`

**Basis:** `origin/art/dorfmap-p3d6` bei `0cdb862`
**Laufzeitnachweis:** `/workspace/codex_jobs/log_p3d8.txt` (`gpt-6-luna`, `xhigh`).

## Änderung

- `neu/mesh.py` löst die Längsprofile von `rampe_2` und `rampe_11` gemeinsam mit dem R3-Operator `h - gaussian_filter1d(h, sigma=8)`. Variante 3, 4 und 5 sind über `RELIEF_KREUZUNG_VAR` auswählbar; **Variante 5 ist Standard**.
- Die Profilhöhe wird mit dem tatsächlichen seitlichen und längsgerichteten Gewicht in die p3d6-Fläche gemischt. Die gemeinsame ebene Fläche erhält zusätzlich einen radial auslaufenden Übergang. Die linearen Solver-Gewichte werden nicht als harte Höhenzuweisung auf den ganzen Korridor übertragen.
- `neu/README.md` beschreibt Schalter, Auswahl und gemessene Grenze. Es wurden keine Prüfer, Tests, Zellquellwerte, Overlay- oder Referenzdateien geändert.

## Build und Schutzprüfungen

Gebaut im Relief-Ordner mit `RELIEF_NEU=1 python3 gen_relief.py && RELIEF_NEU=1 python3 baue_html.py`.

| Messung | p3d8 |
|---|---:|
| LOD1 gesamt | 134.316 / 1.300.000 Dreiecke |
| Gelände / Wände | 88.728 / 45.588 Dreiecke |
| Lochscan im Neu-Viewer | 0 offene Innenkanten, 0 Punkte; 9 Meshes, 88.728 Dreiecke |
| `t42u` | Summe 0; alle neun Abweichungsfelder 0 |
| Zellquell-Diff | 0 |
| D1 Klippenwert bei `140|35` | 7,8840365 m, unverändert |

Adapter-Hashes: D1 änderte sich von `bbc2de2fe035800122fae0b222e55247e5cece3d0ebba131447cf41a367c97e2` auf `d8d44ff95c7d748e77696a3d0b9027007836c5b18b5e362df0b97db7969a9ecc`. G1 blieb `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`, D2 blieb `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`; der Adapter bestätigt D2 bytegleich.

Der größte D1-Höhenunterschied zur Quelle beträgt 2,908248 m bei `148.0|29.5` (Quelle 6,967429 m, Mesh 4,059180 m). Bei `144.5|21.5` liegen Quelle und Mesh bei 12,865277 m beziehungsweise 12,863120 m; dort gibt es keinen Mehr-Meter-Absturz. Der p3d7-Wert von 5,970740 m wird nicht erreicht.

## Prüfergebnisse

Die direkte `pruefe_regeln`-Ausgangszahl 596 aus der Aufgabenbasis ließ sich wie schon im p3d6-Bericht nicht reproduzieren. Der direkte Lauf auf `relief_daten.json.gz` ergibt 570; direktes R8 ergibt 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24), direktes R9 334 (Delle 25, Sägezahn 34, Wellen 275). Diese direkten Werte sind gegenüber p3d6 unverändert. Für das neue Mesh sind die folgenden Adapterwerte maßgeblich.

### Adapter-Regeln p3d6 → p3d8

| Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| G2_spitze_oben | 3→3 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8→8 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 3→3 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 2→2 | 0→0 | 0→0 | 0→0 |
| G5_beule_klippe | 67→67 | 0→0 | 0→0 | 0→0 |
| G6_facette | 216→216 | 0→0 | 3→3 | 0→0 |
| G7_wand_glatte_flaeche | 1→1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 25→25 | 1→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1→1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1→1 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1→1 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24→24 | 2→2 | 1→1 | 0→0 |
| R2_getrennt | 15→15 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 39→43 | 10→14 | 1→1 | 0→0 |
| R3_quer_pct | 19→21 | 7→9 | 0→0 | 0→0 |
| R3_woelb_m | 19→20 | 7→8 | 0→0 | 0→0 |
| R5_loch | 17→17 | 0→0 | 0→0 | 0→0 |
| R6_wasser_schnee | 4→4 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94→94 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |

`pruefe_regeln` gesamt: 563→570. Kein einzelner Regelzähler steigt gegenüber p3d6 um mehr als 5; der größte Anstieg ist R3 längs D1 mit +4. D2 erhält in keiner Regel einen neuen Treffer.

| R8-Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8_stufe | 7→7 | 0→0 | 0→0 | 0→0 |
| R8_gitter | 8→8 | 0→0 | 0→0 | 0→0 |
| R8_quer | 4→4 | 0→0 | 0→0 | 0→0 |
| R8a_wegende | 20→20 | 0→0 | 0→0 | 0→0 |

| R9-Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8b_delle | 22→22 | 0→0 | 0→0 | 0→0 |
| R9_saegezahn | 34→34 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 280→280 | 21→21 | 12→12 | 0→0 |

Am Kreuzungspunkt `152.5|28.5` sinkt R8-Stufe von 0,116 m auf **0,043 m**, R8-Gitter bleibt 0,000 m; die lokale Ausgleichsebene hat 0,000 % Neigung. Am Rampenende `156.5|37.5` sinkt die Stufe von 0,188 m auf **0,135 m** (Gitter 0,090 m, Querneigung 1,4 %). D1/G1 bleiben bei R8/R8a trefferfrei; D2 bleibt bei R8/R9 trefferfrei.

Der D1-Sägezahn-Treffer bleibt ein Treffer am selben Ort `155.2|10.0`, sein Testwert steigt aber von 46 auf **47**. G1-G6 bleibt 3, G1-R9w bleibt 12 und D1-G7b bleibt 1. Diese Nebenwerte wurden nicht optimiert.

### Rampenprofile

`s_rel` ist die Station relativ zum Rampenschnittpunkt in den im R3-Prüfer verwendeten Koordinateneinheiten; Höhen und `lr` sind Meter. Es sind Stationen alle 2 Einheiten gelistet. `lr` ist vorzeichenbehaftet `h_p3d8 - gaussian_filter1d(h_p3d8, sigma=8)`.

**rampe_2** — größtes `|lr|` im 18-Einheiten-Fenster: 0,725 m.

| s_rel | x|z | h_Quelle | h_p3d6 | h_p3d8 | lr_p3d8 |
|---:|---:|---:|---:|---:|---:|
| -12 | 140.66|29.90 | 9.402 | 9.402 | 9.402 | +0.085 |
| -10 | 142.64|29.65 | 8.718 | 8.718 | 8.679 | +0.256 |
| -8 | 144.63|29.41 | 8.076 | 8.076 | 7.416 | +0.322 |
| -6 | 146.61|29.17 | 7.355 | 7.189 | 5.130 | -0.418 |
| -4 | 148.60|28.93 | 6.702 | 5.061 | 4.012 | -0.460 |
| -2 | 150.58|28.68 | 6.151 | 5.030 | 4.012 | -0.072 |
| 0 | 152.57|28.44 | 5.519 | 5.030 | 4.012 | -0.006 |
| +2 | 154.55|28.20 | 5.262 | 5.030 | 4.012 | -0.008 |
| +4 | 156.54|27.96 | 4.964 | 5.024 | 4.012 | -0.027 |
| +6 | 158.52|27.71 | 4.542 | 4.546 | 4.145 | +0.123 |
| +8 | 160.51|27.47 | 4.042 | 4.042 | 3.981 | +0.144 |
| +10 | 162.49|27.23 | 3.491 | 3.491 | 3.489 | +0.053 |
| +12 | 164.48|26.99 | 2.915 | 2.915 | 2.915 | +0.009 |

**rampe_11** — größtes `|lr|` im 18-Einheiten-Fenster: 0,579 m.

| s_rel | x|z | h_Quelle | h_p3d6 | h_p3d8 | lr_p3d8 |
|---:|---:|---:|---:|---:|---:|
| -12 | 156.74|18.24 | 7.302 | 7.302 | 7.296 | -0.017 |
| -10 | 157.11|19.72 | 6.820 | 6.820 | 6.794 | +0.177 |
| -8 | 156.16|21.48 | 6.198 | 6.198 | 5.854 | +0.107 |
| -6 | 155.22|23.24 | 5.595 | 5.558 | 4.610 | -0.240 |
| -4 | 154.27|25.01 | 5.066 | 5.032 | 4.012 | -0.250 |
| -2 | 153.34|26.77 | 4.700 | 5.030 | 4.012 | -0.040 |
| 0 | 152.40|28.54 | 5.604 | 5.030 | 4.012 | +0.001 |
| +2 | 151.45|30.30 | 3.383 | 5.030 | 4.012 | +0.052 |
| +4 | 150.51|32.06 | 2.739 | 4.894 | 4.009 | +0.328 |
| +6 | 151.03|33.51 | 2.114 | 3.151 | 3.462 | +0.546 |
| +8 | 152.65|34.69 | 1.468 | 1.507 | 1.552 | -0.342 |
| +10 | 154.26|35.87 | 0.987 | 0.987 | 0.988 | -0.145 |
| +12 | 155.88|37.05 | 0.614 | 0.614 | 0.614 | -0.117 |

## Variantenvergleich und Bilder

| Kreuzungsvariante | R8-Stufe am Schnitt | D1-Kreuzung Clay-Facetten | `pruefe_regeln` gesamt | R8/R9 gesamt | Delta p3d6→Variante | Delta VAR0→Variante |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 0,044 m | 373 | 569 | 39/336 | 14 | 23 |
| 4 | 0,042 m | 353 | 571 | 39/335 | 15 | 21 |
| **5 (Standard)** | **0,043 m** | **317** | **570** | **39/336** | **14** | **20** |

Variante 5 wurde gewählt, weil sie als einzige die p3d6-Grenze von 351 Kreuzungs-Facetten unterschreitet. VAR0→p3d8 liegt weiterhin um einen Anstieg über dem Ziel `<19`. Der Vergleich enthält 5 Gate-Anstiege und 15 Bild-Proxys. Die Bildwerte stammen aus dem VAR0-Kontrollsatz des p3d6-Berichts; dieser Bericht weist bereits bei unverändertem D2-Mesh Rasterunterschiede zwischen Kontroll- und Mesh-Aufnahme aus. Die Werte bleiben im Delta-Bericht enthalten und werden nicht als Geometriebeweis interpretiert.

Im p3d6→p3d8-Delta gibt es 14 Anstiege: 3 Gate-Zähler (R3 längs D1 +4, R3 quer D1 +2, R3 Wölbung D1 +1) und 11 Bild-Proxys. Die D1-Kreuzungswerte verbessern sich dabei von 51 auf 36 Kantenzähnen, 351 auf 317 Facetten, 802 auf 484 Normalensprüngen und 117 auf 57 Sprung-Inseln. D1-Wandfuß- und Wegende-Proxys steigen teilweise; sie sind in den Rohberichten enthalten.

Vorher/Nachher-Bilder mit identischem Neu-Viewer und denselben sechs Kameras liegen in `bilder_p3d8/vorher/` und `bilder_p3d8/nachher/`. D2-Draufsicht hat auf beiden Seiten SHA-256 `e8db06e608ee2bb6c833c7ca4112a487b5671c5fc2141798c4efd2321350158a`; G1-Wandfuß hat auf beiden Seiten `6a391991ecdee07c10383399b91745244b56cfa0c9d6a88d6fdfce1c2f465c81`. Die D1-Kreuzung und das Streiflicht entlang `rampe_11` unterscheiden sich sichtbar.

Die ersten Renderbilder entstanden versehentlich im Legacy-Viewer. Sie und die verworfenen Kandidaten sind unter `bilder_p3d8/_alt/` aufbewahrt; sie wurden weder für die finalen Bilder noch für die genannten Delta-Zahlen verwendet. Die gültige Vorher-Serie wurde anschließend mit p3d6 und dem Neu-Viewer neu gerendert.

Detailberichte: [Delta p3d6→p3d8](bilder_p3d8/delta_p3d6_p3d8.md), [Delta VAR0→p3d8](bilder_p3d8/delta_var0_p3d8.md). Die sechs Clay-Aufnahmen und das Streiflicht sind in `bilder_p3d8/` gespeichert.

## Tests, Annahmen und offene Punkte

- `~/.local/bin/pytest -q neu/tests`: **26 bestanden, 5 fehlgeschlagen**, gleiche fünf Tests wie im p3d6-Bericht: globales R8a (20), D1-Sägezahn (hier 47), D1-Wandkantenschärfe (2,24 < 3,00), F1/C1-Wegende (F1 0,17 > 0,10; C1 ohne Messwerte) und Schatten-HF (0,307 > 0,25). Die Anzahl ist nicht schlechter als p3d6 (26/5); der D1-Sägezahnwert steigt von 46 auf 47.
- Das gemeinsame LP begrenzt die zwei Achsprofile und der 2D-Transfer mischt tatsächlich mit dem Gelände. Die 2D-R3-Messung bleibt trotzdem deutlich über dem Ziel: R3 längs D1 14 statt höchstens 6 und auch schlechter als p3d6 mit 10. Die R3-Zielbedingung ist **nicht erreicht**.
- D1-R3-Überschreitungen bleiben nahe der Kreuzung; der größte gelistete Profilrest beträgt 0,725 m. Die vorgelegten Stationswerte sind lineare Abtastungen mit 0,25 Koordinateneinheiten, passend zum Prüfer.
- Der VAR0-Delta-Zähler liegt mit 20 über der geforderten Grenze. Davon sind 5 Gate-Anstiege und 15 Bild-Proxys; die alte Kontrollbildbasis ist für unveränderte D2/G1-Geometrie nicht pixelneutral.
- Die neue Variante senkt das Rampenprofil am Schnitt auf ungefähr 4,01 m gegenüber etwa 5,03 m in p3d6. Der R8-Schnitt bleibt flach; die Formqualität entlang der Achse bleibt offen.
