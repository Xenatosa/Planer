# Ergebnis pgelaende

## Ergebnis

Der opt-in Pfad erzeugt ein deterministisches 3D-Mesh-Paket für D1, G1 und D2 und der Offline-Viewer liest dessen Vertices in das sichtbare Three.js-Geländenetz ein. Die Profilberechnung für Wege, Kreuzungen, Wegenden, Wasser und Bauzonen ist implementiert. **Das gewünschte Profil ist nicht Standard:** Sowohl Profilvariante 1 als auch die auf 0,02 gedämpfte Variante 2 erzeugten kleine positive Clay-Bildmetriken in D1/G1. Um die vorgegebene Delta-Abbruchregel einzuhalten, ist Variante 0 (Quellhöhen-Kontrollmesh) Standard. D2 blieb unverändert.

## Änderungen

- `neu/mesh.py`: Höhenfeld und indizierte Tiles aus GB; Profilvarianten für Spline-Wege mit Breite/Längsprofil, Kreuzungsebene mit weichem Rand, Wegenden-Auslauf, Wasser/Ufer und lokale Bauzonenprofile. Wandabstandsschutz und 3-m-Kachelrand-Fade.
- `neu/pipeline.py`, `neu/gen_relief.py`: `RELIEF_NEU=1` schreibt `neu/relief_neu.json.gz` mit `neu_mesh_tiles`.
- `main.js`: Die Tile-Vertices werden in das bestehende 3D-Geländenetz übernommen und mit dessen Material/LOD gerendert; D2-Höhenbytes werden beim Einlesen geprüft.
- `neu/baue_html.py`: erzeugt `neu/index.html` als eigenständigen Offline-3D-Viewer. Die Ausgabe normalisiert Leerzeichen am Zeilenende für deterministische, saubere Diffs.
- README und Tests unter `neu/tests/` ergänzt bzw. angepasst.

## Gates und Zähler

Vorher/Nachher bedeutet hier: der vor Änderung im tatsächlichen Checkout `HEAD 9c9bf53` gemessene Stand gegen den aktuellen Build. Alle Werte je Regel sind unverändert; D2 hat keine neuen Treffer.

| Gate | vorher | nachher | Änderung |
|---|---:|---:|---:|
| `pruefe_regeln.py` inkl. G7b | 570 | 570 | +0 |
| `r8_kreuzung.py` | 48 | 48 | +0 |
| `r9_form.py` | 334 | 334 | +0 |

Die Kachelzahlen für D1/G1/D2 über alle Regeln des jeweiligen Gates:

| Gate | Kachel | vorher | nachher | Δ |
|---|---|---:|---:|---:|
| pruefe_regeln | D1 | 36 | 36 | +0 |
| pruefe_regeln | G1 | 13 | 13 | +0 |
| pruefe_regeln | D2 | 8 | 8 | +0 |
| R8/R8a | D1 | 8 | 8 | 0 |
| R8/R8a | G1 | 1 | 1 | 0 |
| R8/R8a | D2 | 0 | 0 | 0 |
| R8b/R9/R9w | D1 | 26 | 26 | 0 |
| R8b/R9/R9w | G1 | 8 | 8 | 0 |
| R8b/R9/R9w | D2 | 0 | 0 | 0 |

Details je Regel (vorher → nachher sowie die Treffer in den drei Prototypkacheln):

| Bereich | Regel | gesamt vorher → nachher | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---|---:|---:|---:|---:|
| Prüfregeln | `G2_spitze_oben` | 3 → 3 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G2_spitze_oben_fein` | 8 → 8 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G3_spitze_unten` | 3 → 3 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G3_spitze_unten_fein` | 2 → 2 | 0 → 0 | 1 → 1 | 0 → 0 |
| Prüfregeln | `G5_beule_klippe` | 68 → 68 | 1 → 1 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G6_facette` | 220 → 220 | 5 → 5 | 4 → 4 | 0 → 0 |
| Prüfregeln | `G7_wand_glatte_flaeche` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G7b_wandkontur_feld` | 24 → 24 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G7b_wandkontur_kantenschaerfe` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G7b_wandkontur_rauheit` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `G8_fluss_nicht_bis_rand` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `R1_blind` | 24 → 24 | 2 → 2 | 1 → 1 | 0 → 0 |
| Prüfregeln | `R2_getrennt` | 15 → 15 | 1 → 1 | 0 → 0 | 1 → 1 |
| Prüfregeln | `R3_laengs_m` | 35 → 35 | 6 → 6 | 1 → 1 | 0 → 0 |
| Prüfregeln | `R3_quer_pct` | 23 → 23 | 11 → 11 | 0 → 0 | 0 → 0 |
| Prüfregeln | `R3_woelb_m` | 22 → 22 | 10 → 10 | 0 → 0 | 0 → 0 |
| Prüfregeln | `R5_loch` | 17 → 17 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `R6_wasser_schnee` | 4 → 4 | 0 → 0 | 3 → 3 | 0 → 0 |
| Prüfregeln | `T1_fleckrand` | 94 → 94 | 0 → 0 | 3 → 3 | 7 → 7 |
| Prüfregeln | `T2_textur_abgeschnitten_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `T3_streifen_ringe_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `T4_graue_flussstreifen_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| Prüfregeln | `T5_textur_vs_clay_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |

| Bereich | Regel | gesamt vorher → nachher | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---|---:|---:|---:|---:|
| R8/R8a | `R8_gitter` | 10 → 10 | 2 → 2 | 0 → 0 | 0 → 0 |
| R8/R8a | `R8_quer` | 5 → 5 | 1 → 1 | 0 → 0 | 0 → 0 |
| R8/R8a | `R8_stufe` | 9 → 9 | 2 → 2 | 0 → 0 | 0 → 0 |
| R8/R8a | `R8a_wegende` | 24 → 24 | 3 → 3 | 1 → 1 | 0 → 0 |

| Bereich | Regel | gesamt vorher → nachher | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---|---:|---:|---:|---:|
| R8b/R9/R9w | `R8b_delle` | 25 → 25 | 2 → 2 | 1 → 1 | 0 → 0 |
| R8b/R9/R9w | `R9_saegezahn` | 34 → 34 | 1 → 1 | 1 → 1 | 0 → 0 |
| R8b/R9/R9w | `R9w_wellen` | 275 → 275 | 23 → 23 | 6 → 6 | 0 → 0 |

Die Gate-Skripte `pruefe_regeln.py`, `r8_kreuzung.py` und `r9_form.py` liefern Exit 1, weil ihre bestehenden Befunde weiter vorhanden sind; die Zähler sind gegenüber dem Pre-Change-Lauf unverändert. `pruefe_t42u.py` lieferte `summe=0`, alle neun Abweichungsfelder 0.

**Baseline-Abweichung:** Der Auftrag nennt 596 `pruefe_regeln`-Treffer bei Stand `9d3f8fc`. Im unveränderten Checkout dieses Worktrees (`9c9bf53`, Nachfahre von `9d3f8fc`) waren vor Änderungen 570 reproduzierbar, nach Änderungen ebenfalls 570. Die vorgegebene 596-Zahl konnte ich in diesem Checkout nicht reproduzieren; die Regelprüfer und Schwellen wurden nicht geändert. R8=48 und R9=334 stimmen mit den Auftragswerten überein.

## Geländevarianten und Bilddelta

| Variante | D1 veränderte Vertices / max. Δ | G1 veränderte Vertices / max. Δ | D2 | Clay-Bilddelta gegen Basis |
|---|---:|---:|---:|---|
| `RELIEF_GELAENDE_VAR=0` (Standard) | 0 / 0 m | 0 / 0 m | 0 / 0 m | 0 Anstiege; alle 18 Bilder pixelgleich |
| `=1` | 184 / 0,029399 m | 293 / 0,071783 m | 0 / 0 m | 8 Metrikwerte stiegen: D1 Facetten Draufsicht +1, West +3, Wandfuß +1, Wegende +2; G1 Kantenzaehne Kreuzung +6, Facetten West +3, Facetten Wandfuß +1, Kantenzaehne Wandfuß +4 |
| `=2` (Gewicht 0,02) | 84 / 0,000588 m | 209 / 0,001436 m | 0 / 0 m | 2 Metrikwerte stiegen um je 1 (D1 Wegende, G1 West) |

Für den finalen Standardlauf verglich `neu/delta.py` 18 Clay-Nahbilder: 0 Anstiege, Exit 0. Pixelweiser Vergleich aller 18 finalen PNGs gegen die vorherigen Basisbilder ergab jeweils 0 geänderte Pixel. Ich habe D1-Wandfuß/Klippenbereich, G1-Wandfuß und D2-Draufsicht angesehen; Wandkanten und Klippenform bleiben in diesem Standardlauf identisch. Der Kontrollpunkt D1 (140,35) ist beim Profilmesh bytegleich mit GB. Bilder: `/tmp/nahbilder_pgelaende_final/clay/` (D1/G1/D2, je Draufsicht, Kreuzung, Ost-/West-Streiflicht, Wandfuß, Wegende), darunter `D1_wandfuss.png`, `G1_wandfuss.png`, `D2_draufsicht.png`. Delta-Protokoll: `/tmp/delta_pgelaende_final.md`.

## Mesh, Quellen und Reproduzierbarkeit

- Je Tile: 7.395 Vertices / 14.448 Dreiecke; 3 Tiles zusammen 43.344 Dreiecke. LOD1 wurde zuvor mit dem Browser-Gate mit **1.174.554** gerenderten Dreiecken gemessen (<1,3 Mio.).
- Der erfolgreiche Lochscan vor dem finalen Browser-Ausfall meldete 1.700.454 Dreiecke, 0 offene Innenkanten und 0 Punkte. Beim erneuten Pflichtlauf nach dem letzten Standard-Neuaufbau schlug Playwright nach 300 s bei `window.__test.bereit` fehl: Browserfehler „WebGL ist in diesem Browser nicht verfügbar“. Ein Minimalcheck auf `about:blank` bestätigte, dass WebGL in der aktuellen Browserumgebung deaktiviert ist; der Pflichtlauf schrieb daher keine neue Lochscan-Datei. `pruefe_regeln.py` wurde mit dem letzten erfolgreichen Lochscan und aktuellem Höhen-/Regelstand ausgeführt; R8/R9 und t42u liefen frisch gegen die aktuellen Daten. Alle Zähler blieben gegenüber dem Pre-Change-Lauf identisch. Das ist ein offener Prüfpunkt, kein bestandener finaler Lochscan.
- `relief_daten.json.gz` blieb unverändert, SHA-256 `5e8fdb51c3f3dff9ad2c03c32c7a39ee1a4f97a3bc0942d47a352b1d0b4f0e88`.
- Die neun Quellspalten (`untergrund`, `hindernis_id`, `hindernis_art`, `wasser_eis`, `ebene`, `bauzone_bestand`, `bauzone_plan`, `begehbar`, `bebaubar`) hatten `zellen_quell_diff=0`; bestehende Zellwerte, Overlay und `../referenz/*` blieben unangetastet. D2-Höhenbytes stimmen exakt mit GB/Legacy überein; sein Mesh-SHA ist `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`.
- `neu/relief_neu.json.gz` SHA-256 `1a7ac9de153e189a58021884c3f891b2a3394dacfa81db2e7dc9d692b5e1bc8c`; zweifacher Pipeline-Build erzeugte denselben Hash. `vektor.json`, `felder.npz`, `felder.json`, `build.json`, `zellen_relief.csv` und Diagnose-PNGs waren ebenfalls deterministisch.
- Standardbuild `python3 gen_relief.py && python3 baue_html.py` und opt-in Build `RELIEF_NEU=1 python3 gen_relief.py && RELIEF_NEU=1 python3 baue_html.py` wurden ausgeführt. `node neu/tests/test_html.js`, `node neu/tests/test_pipeline.js` und neun Python-Testfunktionen liefen erfolgreich direkt. `pytest` ist nicht installiert.

## Annahmen, Grenzen und offene Punkte

- Höhen-Grundlage ist das sichtbare GB-Feld; Geländeprofile nutzen Vektoren/Felder als weiche Ziele. Zellquellspalten werden nicht als Schreibziel verwendet.
- D2 ist ein harter Legacy-Kontrollbereich. Dadurch wird dort kein neues Profil gezeichnet.
- Profilvarianten 1/2 sind wegen der kleinen positiven Clay-Metrikdeltas nicht als Standard freigegeben. Das Profilziel (sichtbar geformte Wege/Kreuzungen/Wasser/Bauzonen im Standardlauf) ist somit noch nicht erreicht.
- Der aktuelle Browser-Gate-Ausfall beruht auf fehlendem WebGL in der Laufumgebung; erneuter Lochscan und aktueller LOD1-Messlauf bleiben offen. Die vorigen erfolgreichen Messungen sind dokumentiert, ersetzen aber keinen neuen Browserlauf.
- Der Codex-Sitzungslog ist über die verfügbaren Arbeitsbereichswerkzeuge nicht zugänglich; die gezielte Suche in vorhandenen `/tmp`-Logs lieferte keine Modell-/Denkstufenangabe. Ich kann daher nicht bestätigen, dass dort `gpt-6-luna` und `xhigh` stehen. Die Konfiguration wurde nicht geändert.
- Kosten: 0 EUR. Keine Prozesspools verwendet.
