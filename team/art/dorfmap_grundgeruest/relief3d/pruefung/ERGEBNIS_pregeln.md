# Ergebnis `pregeln`

Stand: 04.11.2026 · Branch `art/dorfmap-pregeln` · Arbeitsbasis vor Arbeit: `7c0df80` · angegebene Vergleichsrevision: `9d3f8fc`

## Änderungen

- `../../REGELWERK_LANDSCHAFT_VOLLSTAENDIG.md` wurde fortgeführt. Die vorherige Fassung liegt per `git mv` unter `../../_alt/REGELWERK_LANDSCHAFT_VOLLSTAENDIG_vor_pregeln.md`. Die neue Fassung ergänzt die geforderte Elementmatrix mit Aussehen, Herkunft, Prüfzahl, Bildpfad und Status sowie die Abschlussmatrix „Element × Prüfzahl × fehlender Prüfer“.
- `pruefung/regelmessung.py` misst die Zellquelle `../raster_c20_z25_zellen.csv` direkt und schreibgeschützt. Es erfasst unter anderem Waldflächen und 8-Nachbar-Gruppen, Pflanz-/Felseignung, E40-Baupolygone, Deko-Kapazität, benannte Gebirgsbänder und Materialzellen. Karten-Eignungszellen und Relief-Objektinstanzen werden getrennt ausgewiesen.
- `neu/` enthält einen deterministischen, lokalen Prototyp. `RELIEF_NEU=1` leitet beide Einstiegsskripte dorthin um; ohne Schalter bleibt die bestehende Pipeline Standard. Der Prototyp erzeugt die Höhenfelder D1/G1 aus den Quellzellhöhen. D2 wird als unveränderter GB/VC/WV/WEGA-Referenzblock eingebettet. Er schreibt keine Legacy-Ausgabedatei.
- Automatische Tests liegen in `neu/tests/`; die vier Node-Tests prüfen Schalter, Messwerkzeug, Datenbauer und HTML-Bauer.

## Gates: Revision `9d3f8fc` → Standardbau nach Änderung

Die Vergleichswerte der Revision `9d3f8fc` wurden aus deren eingechecktem Reliefdatensatz erneut mit den unveränderten aktuellen Gate-Skripten gemessen. Der aktuelle Branch lag **vor dem Standardbau bereits bei 570** Treffern im Regelgate. Der Standardbau änderte diesen Wert nicht.

| Gate | `9d3f8fc` | Branch vor Standardbau | Branch nach Standardbau | Änderung im Branch |
|---|---:|---:|---:|---:|
| `pruefe_regeln.py` (inkl. G7b) | 596 | 570 | 570 | 0 |
| `r8_kreuzung.py` | 48 | 48 | 48 | 0 |
| `r9_form.py` | 334 | 334 | 334 | 0 |
| `loch_o18g.js` `offen_innen` | 0 | 0 | 0 | 0 |

Der Unterschied `596 → 570` stammt aus dem bereits vorliegenden Branchstand gegenüber `9d3f8fc`, nicht aus dem Neubau in diesem Branch. Gegenüber `9d3f8fc` steigt keine Einzelregel um mehr als fünf Treffer. Die einzigen Zunahmen sind G5 `66 → 68` (+2) und G7b-Feld `23 → 24` (+1); G6 sinkt `249 → 220` (−29). Alle übrigen Einzelregeln bleiben gleich.

### `pruefe_regeln.py` je Regel

| Regel | `9d3f8fc` | vor Arbeit / vor Bau | nach Bau | Δ gegen `9d3f8fc` |
|---|---:|---:|---:|---:|
| R1_blind | 24 | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 22 | 0 |
| R5_loch | 17 | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 8 | 0 |
| G3_spitze_unten | 3 | 3 | 3 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 2 | 0 |
| G5_beule_klippe | 66 | 68 | 68 | +2 |
| G6_facette | 249 | 220 | 220 | −29 |
| G7_wand_glatte_flaeche | 1 | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 24 | 24 | +1 |
| T1_fleckrand | 94 | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 1 | 0 |

### R8/R9 je Regel

| Gate/Regel | `9d3f8fc` | Branch vor Arbeit / nach Bau |
|---|---:|---:|
| R8_stufe | 9 | 9 / 9 |
| R8_gitter | 10 | 10 / 10 |
| R8_quer | 5 | 5 / 5 |
| R8a_wegende | 24 | 24 / 24 |
| **R8 gesamt** | **48** | **48 / 48** |
| R8b_delle | 25 | 25 / 25 |
| R9_saegezahn | 34 | 34 / 34 |
| R9w_wellen | 275 | 275 / 275 |
| **R9 gesamt** | **334** | **334 / 334** |

### Treffer je Kachel D1/G1/D2

| Gate / Regel | D1 vor → nach | G1 vor → nach | D2 vor → nach |
|---|---:|---:|---:|
| `pruefe_regeln.py` gesamt | 36 → 36 | 13 → 13 | 8 → 8 |
| davon D2 `R2_getrennt` / `T1_fleckrand` | — | — | 1 / 7 → 1 / 7 |
| R8 gesamt | 8 → 8 | 1 → 1 | 0 → 0 |
| R8-Stufe / Gitter / Quer / Wegende, D1 | 2 / 2 / 1 / 3 → gleich | — | — |
| R8-Stufe / Gitter / Quer / Wegende, G1 | — | 0 / 0 / 0 / 1 → gleich | — |
| R9 gesamt | 26 → 26 | 8 → 8 | 0 → 0 |
| R9-Delle / Sägezahn / Wellen, D1 | 2 / 1 / 23 → gleich | — | — |
| R9-Delle / Sägezahn / Wellen, G1 | — | 1 / 1 / 6 → gleich | — |

D2 hatte bereits in der Vergleichsrevision acht `pruefe_regeln`-Treffer (ein R2, sieben T1); **kein neuer D2-Treffer** kam hinzu. D2 bleibt in R8 und R9 bei null.

## Kartenmessung und Objektzahlen

Die reproduzierbare Detailausgabe liegt unter `/tmp/regelmessung_pregeln.json`. Die Zellquelle enthält 336 × 303 = 101 808 Zellen, nominal 1 m² je Zelle.

| Messung | Ergebnis |
|---|---:|
| WALD-Fläche / 8-Nachbar-Gruppen | 11 217 m² / 64 Gruppen; größte Gruppe 5 967 Zellen |
| Einzelbaum-Quellstandorte | nicht enthalten; 34 705 `deko_baum_ok`-Eignungszellen |
| Bäume im aktuellen Reliefbestand | 1 481 |
| Gebäudeplanung E40 | 233 Polygone; Breite P5/Median/P95 4,8038/6/11,365 m; Tiefe 4,9992/6/10,9992 m |
| Bebaubarkeit | 23 123 `bauzone_bestand`, 31 893 `bauzone_plan`, 27 140 `bebaubar` |
| Fels | 2 123 FELS-Terrainzellen, 62 391 Fels-Eignungszellen; 96 Felsen, 32 Findlinge, 0 Felsblöcke im Modellbestand |
| Deko | 62 391 positive Kapazitätszellen, Summe 27 452,04 Quell-Einheiten; 3 917 Grasinstanzen |
| Gebirgszonen | 20 099 Quellzellen; Nord 6 661, Südgrat 5 688, Krater 3 143, Ostgrat 2 742 |

Ausgewählte Quell- und Modellzahlen je Prototypkachel:

| Kachel | WALD-Zellen | Baum-Eignungszellen | Fels-Eignungszellen | E40-Polygone | Modelle: Bäume/Häuser/Gras |
|---|---:|---:|---:|---:|---:|
| D1 | 25 | 553 | 900 | 2 | 12 / 2 / 85 |
| G1 | 18 | 224 | 686 | 2 | 7 / 2 / 67 |
| D2 | 5 | 298 | 1 681 | 7 | 0 / 7 / 63 |

## D2, Quellspalten, T42 und Dreiecke

- Der Standardbau erzeugte denselben Hash für `relief_daten.json.gz` wie vor dem Bau. D2-GB, VC, WV und WEGA sind bytegleich zur Vorarbeitsdatei und zur Revision `9d3f8fc`. SHA-256 der ausgeschnittenen D2-Felder: GB `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`, VC `b67dc7199dcd4fe28bb242295f928355a85fc84bee12e390e060c9e7cbbcf2bf`, WV `4b33ed17db72aa7b29472ef5b50f05196ea61eb7a11a7db3b7a8684eb8d3880a`, WEGA `e6cf61d23389529a95f01526b5c914401ef9d6ea9295b417155e4c8841606f7e`.
- Die Quellkarte blieb bytegleich; SHA-256 `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa`. In `zellen_relief.csv` änderten sich beim erlaubten Neu-Export **0 Zellwerte** in den neun physischen Quellspalten `untergrund`, `hindernis_id`, `hindernis_art`, `wasser_eis`, `ebene`, `bauzone_bestand`, `bauzone_plan`, `begehbar`, `bebaubar` (die sieben logischen Quellgruppen aus dem Auftrag).
- Die einzige CSV-Spalte mit geändertem Inhalt war die abgeleitete Spalte `boden_anzeige_m`: 14 429 Zellen insgesamt; davon D1 282, G1 199, D2 0. D2-Quellzellen und D2-Anzeigefelder sind unverändert.
- `pruefe_t42u.py`: **Summe 0** (alle neun Einzelabweichungen 0).
- `test_dreiecke_l1.js` im Viewer mit `?lod=1`: **1 174 554 gerenderte Dreiecke**, damit 125 446 unter der Grenze 1,3 Mio. Die separate Lochprüfung zählt 1 700 454 Dreiecke im vollständigen geladenen Mesh; das ist nicht der LOD1-Wert.
- Prototyp-Schätzung: 21 672 LOD1-Dreiecke über D1/G1-Quellraster und D2-Referenzraster.

## Tests und Aufrufe

Ausgeführt:

```text
python3 gen_relief.py
python3 baue_html.py
HTML=index.html OUT=/tmp/gate_loch_pregeln.json RAND=0.6 NODE_PATH=/tmp/w3/node_modules node pruefung/loch_o18g.js
LOCHSCAN=/tmp/gate_loch_pregeln.json python3 pruefung/pruefe_regeln.py relief_daten.json.gz /tmp/regeln_pregeln.json
python3 pruefung/r8_kreuzung.py relief_daten.json.gz /tmp/r8_pregeln.json
python3 pruefung/r9_form.py relief_daten.json.gz /tmp/r9_pregeln.json
python3 pruefung/pruefe_t42u.py
NODE_PATH=/tmp/w3/node_modules node test_dreiecke_l1.js file:///workspace/wt_dorfmap_pregeln/team/art/dorfmap_grundgeruest/relief3d/index.html?lod=1
node --test neu/tests/*.test.js
python3 pruefung/regelmessung.py --out /tmp/regelmessung_pregeln.json
```

Node-Tests: 4 bestanden, 0 fehlgeschlagen. `python3 -m pytest -q neu/tests` war nicht verfügbar (`No module named pytest`); dieselben neuen Werkzeuge sind über die vorhandenen Node-Tests abgedeckt.

Prototyp-Schalter:

```sh
RELIEF_NEU=1 python3 gen_relief.py
RELIEF_NEU=1 python3 baue_html.py
```

Die Prototypdateien landen standardmäßig unter `/tmp/relief_neu_pregeln/`. Der HTML-Inspektionsblick ist offline und nutzt keine externen Skripte.

## Annahmen, Grenzen und offene Punkte

- `hoehe_m` aus der Dorfkarten-Zellquelle wird für D1/G1 als Quellhöhe interpretiert. Das 1-m-Prototypraster mittelt die benachbarten Zellmitten auf jeden Rastervertex; die zwei Dreiecke pro Zelle sind deterministisch. Das ist ein Neubau-Prototyp für die Geländegrundfläche, noch kein Ersatz für die komplette Reliefpipeline.
- D2 wird im Prototyp bewusst nicht neu berechnet: sein bestehender, unveränderter Anzeige- und Overlay-Payload ist eine schreibgeschützte Referenz. Der Test prüft GB/VC/WV/WEGA-Bytes, nicht einen gerenderten Frame-Hash. Die vorhandene Standardanzeige bleibt die maßgebliche D2-Ansicht.
- Einzelbaum-, Fels- und Deko-Koordinaten stehen nicht in den Zellquellen. Eignungsflächen und vorhandene Reliefinstanzen sind deshalb getrennte Zahlen; ein Karten-Symbol-zu-Mesh-Abgleich bleibt offen.
- Die Master-PNG ist nicht in diesem Worktree. Die Berichtsbilder unter `../../REGELWERK_LANDSCHAFT_VOLLSTAENDIG.md` sind vorhandene Diagnose-/Vorherbilder; mehrere Elemente haben noch kein spezifisches Negativbild.
- Der Prototyp rendert keine vollständigen Gebäude, Wege, Brücken, Wasser-/Eisdetails, Texturen, dynamischen Schatten oder Deko-Meshes. Hierfür fehlen noch Quelle/Regeln sowie eigene Schwellenprüfer, siehe Abschnitt 10 des Regelwerks.
- Die einzelne neue Geometrievariante wird ausschließlich mit `RELIEF_NEU=1` aktiviert. Es gibt keine Zufallswerte, Prozesspools, externen Dienste oder kostenpflichtigen Schritte.
