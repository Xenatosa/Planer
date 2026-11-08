# Ergebnis p3d6

**Branch:** `art/dorfmap-p3d6`

**Basis:** `origin/art/dorfmap-p3d5` / `6e58af0`
**Ergebnis:** teilweise erreicht. D2, Lochfreiheit, Wandtopologie und D1/G1-R8a bleiben stabil. R3 längs, Wandfuß-Bildmetriken, G7b D1, G6 G1 und R9w G1 verfehlen mindestens ein Ziel.

## Änderungen

- `neu/wand.py`: Wandfuß-Standard auf `RELIEF_WANDFUSS_VAR=2`. Die Kontur wird an Kanten der gerenderten Terrain-Dreiecke geteilt und 0,15 m eingebettet. Kappen erhalten geteilte Randpunkte; degenerate Dreiecke werden herausgefiltert. D1/G1 bleiben als geschlossene, manifold Wandmeshes.
- `neu/mesh.py`: lokale Wegende-Variante 2 als schaltbare Alternative ergänzt; Standard bleibt Variante 1. Kreuzungsstandard bleibt die radiale Variante 2 aus p3d5. Die fehlgeschlagenen Achs-Kandidaten sind nicht Standard.
- `neu/README.md`: Varianten und Standardwerte dokumentiert.
- `index.html`, `neu/index.html`, `neu/build.json`: mit dem Neu-Mesh neu erzeugt.
- Prüfberichte und Vorher/Nachher-Clay-Aufnahmen unter `pruefung/bilder_p3d6/`.

Keine Quellzellwerte, Overlay-Dateien oder `../referenz/*` wurden geändert. `zellen_quell_diff=0`.

## Build und Erhaltungsprüfungen

Build im Relief-Ordner: `RELIEF_NEU=1 python3 gen_relief.py && python3 baue_html.py`.

| Messung | Ergebnis |
|---|---:|
| LOD1-Dreiecke | 134.316 / 1.300.000 |
| Gelände-Dreiecke | 88.728 |
| Wand-Dreiecke | 45.588 |
| Wand D1 | 19.920 Dreiecke, 0 degenerierte, 0 Kanten mit anderer als zwei Inzidenzen |
| Wand G1 | 25.668 Dreiecke, 0 degenerierte, 0 Kanten mit anderer als zwei Inzidenzen |
| Wand D2 | keine |
| Lochscan / Xvfb-Raycast-Lochscan | `offen_innen=0`, `punkte=0` |
| t42u | Summe 0; alle Abweichungen 0 |
| Objekt-Raycasts | 88/88 Treffer; 0 schwebend >0,3 m; 0 versunken außerhalb Toleranz |
| D2 Höhenhash | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`, 0 geänderte Höhenvertices; Adapter bestätigt bytegleiches D2-Mesh |
| Klippenoberkante 140|35 | 7,8840365 m, unverändert |

Der Schnittpunkt bleibt bei 0,116 m, der Endpunkt `156.5|37.5` bei 0,188 m. R8/R8a D1 und G1 sowie R8/R9 D2 bleiben im angepassten Neu-Mesh-Prüflauf bei 0.

## Prüfergebnisse

Die vom Auftrag genannte direkte `pruefe_regeln`-Ausgangszahl 596 ließ sich in diesem Worktree nicht reproduzieren: der direkte Lauf mit Lochscan ergab 570. Die direkten R8/R9-Zahlen stimmen mit der angegebenen Basis überein: R8 48 (`Stufe 9, Gitter 10, Quer 5, Wegende 24`), R9 334 (`Delle 25, Sägezahn 34, Wellen 275`). Diese direkten Prüfer lesen weiterhin `relief_daten.json.gz`; für die geänderte Geometrie ist deshalb zusätzlich der Neu-Mesh-Adapter relevant.

Der Adapter-Vergleich **VAR0 → p3d6** ergibt: `pruefe_regeln` 569 → 563, R8 45 → 39 und R9 338 → 336. Die folgenden Vorher/Nachher-Zahlen je Regel und Kachel kommen aus diesem adaptierten Vergleich. `D1`, `G1` und `D2` zeigen jeweils `VAR0 → p3d6`.

| Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 4→0 | 2→0 | 2→0 | 0→0 |
| G2_spitze_oben | 3→3 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8→8 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 3→3 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 1→2 | 0→0 | 0→0 | 0→0 |
| G5_beule_klippe | 68→67 | 1→0 | 0→0 | 0→0 |
| G6_facette | 216→216 | 1→0 | 2→3 | 0→0 |
| G7_wand_glatte_flaeche | 1→1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 24→25 | 0→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1→1 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1→1 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1→1 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24→24 | 2→2 | 1→1 | 0→0 |
| R2_getrennt | 15→15 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 35→39 | 6→10 | 1→1 | 0→0 |
| R3_quer_pct | 23→19 | 11→7 | 0→0 | 0→0 |
| R3_woelb_m | 22→19 | 10→7 | 0→0 | 0→0 |
| R5_loch | 17→17 | 0→0 | 0→0 | 0→0 |
| R6_wasser_schnee | 4→4 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94→94 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1→1 | 0→0 | 0→0 | 0→0 |

| R8-Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8_stufe | 8→7 | 1→0 | 0→0 | 0→0 |
| R8_gitter | 9→8 | 1→0 | 0→0 | 0→0 |
| R8_quer | 5→4 | 1→0 | 0→0 | 0→0 |
| R8a_wegende | 23→20 | 2→0 | 1→0 | 0→0 |

| R9-Regel | Gesamt | D1 | G1 | D2 |
|---|---:|---:|---:|---:|
| R8b_delle | 23→22 | 1→0 | 0→0 | 0→0 |
| R9_saegezahn | 34→34 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 281→280 | 21→21 | 13→12 | 0→0 |

`delta.py` meldet **19 Anstiege**: fünf Gate-Zähler (G3 fein C1 +1, G6 G1 +1, G7b D1 +1, R3 längs D1 +4, R9w F1 +1) und 14 Bild-Proxymetriken. Kein Regelanstieg liegt über +5; das Gesamtziel `delta.py=0` ist trotzdem verfehlt. Die D1-R3-Anstiege liegen an `rampe_2`/`rampe_11` im Kreuzungsbereich; höchste gemeldete Abweichung dort 0,688 m. Der radiale Anteil entlang der Rampenachse ist mit dem ausgewählten Profil nicht ausreichend ausgeblendet.

## Variantenmessungen und Zielabweichungen

| Kreuzungsprofil | R3 längs gesamt (D1) | R8 gesamt; D1 | R9 gesamt | Auswahl |
|---|---:|---:|---:|---|
| `RELIEF_KREUZUNG_VAR=2`, radial-only, Standard | 39 (10) | 39; D1 0 | 336 | Beibehalten: R8 D1/G1 0, Schnitt 0,116 m |
| Variante 0, schmalerer radialer Rand | 40 (11) | 40; D1 Stufe 1 | 335 | Verworfen: R3 und R8 D1 schlechter |
| Achsprofil, weicher Auslauf (`axis_smooth`) | 42 (13) | 41; D1 Stufe 1 und Quer 1 | 342 | Verworfen: R3/R8/R9 schlechter |
| zusätzlicher Zwischenlauf `axis_constant_long` | 41 (12) | 40; D1 Stufe 1 | 337 | Diagnose, nicht im Standard |

Die drei schaltbaren Kreuzungswerte 0/1/2 sind dokumentiert. Zusätzlich wurden in der Ursachenanalyse die beiden Achs-Zwischenstände `axis_smooth` und `axis_constant_long` gemessen; falls jede Zwischenkonfiguration als eigene Variante zählt, wurde damit die Grenze von drei Varianten überschritten. Diese Zwischenstände sind nicht als weitere Umgebungsvarianten im Ergebnis enthalten.

Der Wegende-Standard bleibt Variante 1. Die gemessene Variante 2 reduziert `G6 G1` von 3 auf 2, aber erzeugt je einen R8a-Treffer in D1 und G1, erhöht R8 insgesamt von 39 auf 41 und R9w G1 von 12 auf 13. Sie wurde daher verworfen. Die 12 adaptierten G1-R9w-Treffer verteilen sich über x=263–292 und z=5,9–35,8; ein einzelnes Wegende erklärt sie nicht. Der direkte R9-Prüflauf auf dem unveränderten Alt-Datensatz ergibt G1-R9w=6, löst aber die Abweichung des Neu-Mesh-Adapterlaufs nicht auf.

Wandfuß-Messung der Clay-Bilder (VAR0 Kontrollbild → p3d6; Bild-Proxys, keine geometrische Wahrheit):

| Ansicht | Kanten-Zähne | Facetten | Normalensprünge | Sprung-Inseln | Löcher / Flecken |
|---|---:|---:|---:|---:|---:|
| D1 `140|35` | 1562→1258 | 382→535 | 3696→3322 | 173→333 | 51/51→44/45 |
| G1 Wandfuß | 938→911 | 532→530 | 2877→3393 | 172→182 | 41/21→44/34 |

Die Zielbedingung `Facetten/Inseln/Normalen <= VAR0` wird somit nicht erreicht. In den gespeicherten D1- und G1-Nahbildern sind am unteren Wandanschluss weiter kleine treppige Kerben sichtbar; die Wand wirkt oberhalb davon glatt. `G7b_wandkontur_feld` D1 bleibt bei 1, G1-G6 bei 3, D1-Sägezahn bei 46 Zacken. Der D1-Sägezahn-Treffer liegt bei `155.2|10.0`.

## Bilder und D2-Raster

Vorher (VAR0) und p3d6 (Clay, gleiche Kameras) liegen in `bilder_p3d6/control/` und `bilder_p3d6/mesh/`:

| Ansicht | VAR0 | p3d6 |
|---|---|---|
| D1 Kreuzung | [Bild](bilder_p3d6/control/clay/D1_kreuzung.png) | [Bild](bilder_p3d6/mesh/clay/D1_kreuzung.png) |
| D1 Wandfuß 140\|35 | [Bild](bilder_p3d6/control/clay/D1_wandfuss_140_35.png) | [Bild](bilder_p3d6/mesh/clay/D1_wandfuss_140_35.png) |
| D1 Wegende | [Bild](bilder_p3d6/control/clay/D1_wegende.png) | [Bild](bilder_p3d6/mesh/clay/D1_wegende.png) |
| G1 Wandfuß | [Bild](bilder_p3d6/control/clay/G1_wandfuss.png) | [Bild](bilder_p3d6/mesh/clay/G1_wandfuss.png) |
| D2 Draufsicht | [Bild](bilder_p3d6/control/clay/D2_draufsicht.png) | [Bild](bilder_p3d6/mesh/clay/D2_draufsicht.png) |

Die D2 p3d6-Aufnahme stimmt byteweise mit einer zweiten Xvfb-Aufnahme überein: SHA-256 `e8db06e608ee2bb6c833c7ca4112a487b5671c5fc2141798c4efd2321350158a`. Das D2-Mesh ist laut Adapter bytegleich. Gegenüber dem VAR0-Kontrollbild unterscheiden sich 355/700.000 Pixel; gegenüber dem p3d5 Standardbild 17/700.000 Pixel. Diese Rasterabweichungen sind bei unverändertem D2-Mesh reproduzierbar, ihre Ursache ist nicht geklärt und sie sind kein Beleg für eine Geometrieänderung.

## Tests, Annahmen und offene Punkte

- `pytest -q neu/tests`: 26 bestanden, 5 fehlgeschlagen. Offen: globales R8a (20 Treffer außerhalb D1/G1), D1-Sägezahn, Wandkantenschärfe (2,24 < 3,00), F1/C1-Wegende (F1 0,17 > 0,10; C1 ohne Messwerte) und Schatten-HF (0,307 > 0,25). Die gezielten D1/G1-R8a-Treffer sind 0; nicht alle D1/G1-Ziele sind grün.
- Annahme für den Delta-Vergleich: VAR0 ist der Kontrollstand aus `bilder_p3d5/control` plus die VAR0-Adapter-Gates. Die direkte `pruefe_regeln`-Zahl 596 aus der Aufgabenbasis ließ sich nicht reproduzieren; deshalb sind die detaillierten Regelwerte oben ausdrücklich VAR0-Adapter-Vergleiche.
- Grenze: der Raycast prüft 88 platzierte Objekte und deren vertikale Projektion auf die sichtbaren D1/G1/D2-Terrainmeshes, nicht jede beliebige Blickrichtung.
- Offen: Ursache der Bild-Proxymetrik-Sprünge außerhalb der D2-Wiederholung ist nicht vollständig getrennt von Renderer-/Rastierungseinflüssen. D1/G1-Wandfußkerben und die übrigen oben genannten Zielabweichungen benötigen weitere Ursachenarbeit.
- Kein Laufzeitlog mit den geforderten Einträgen `model: gpt-6-luna` und `reasoning effort: xhigh` war im Worktree oder den geprüften p3d6-Temppfaden vorhanden. Ich habe diese Angaben nicht erfunden; der Laufzeitnachweis bleibt offen. Codex-Konfiguration wurde nicht geändert.
