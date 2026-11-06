# Ergebnis pwand – getrennte Wandmeshes und 3D-Kachelviewer

Stand: 2026-11-06 · Worktree `wt_dorfmap_pwand` · Branch `art/dorfmap-pwand`

## Aenderungen

- `neu/wand.py` erzeugt aus `neu/vektor.json` separate geschlossene Wandkoerper mit den Profilhoehen oben/unten und der Mindestbreite. WANDVAR=1 ist Standard und verwendet die Profilbreite; WANDVAR=0 erzeugt eine 2,4-m-Variante. D2 wird ausdruecklich wandfrei gehalten.
- `neu/mesh.py` und `neu/pipeline.py` bauen D1/G1 aus den Hoehen der Quellzellen (1-m-Raster; Eckhoehe = Mittel der angrenzenden Zellen). D2 wird direkt aus den sichtbaren `GB`-Hoehen mit 0,5-m-Raster gebaut.
- `neu/viewer.js` zeichnet die drei Geländemeshe samt geschlossenen Fundamenten und die getrennten Wandmeshes. `RELIEF_NEU=1` waehlt den neuen HTML-Builder und Viewer; ohne Schalter bleibt die alte Pipeline Standard. Ohne WebGL wird dieselbe Szene fuer Geometriepruefungen aufgebaut; mit WebGL wird sie gerendert.
- `neu/build.json` dokumentiert Paketgroessen und Quellhashes. Der Zell-Quellvergleich ist 0. Quellzellwerte, Overlay und `../referenz/*` wurden nicht geaendert.

## Mesh und Regression D2

| Kachel | Hoehenraster | Oberflaechen-Vertices | Oberflaechen-Dreiecke | Geschlossenes Gelaende | Wand-Features / Dreiecke |
|---|---:|---:|---:|---:|---:|
| D1 | 1,0 m | 1.892 | 3.612 | 7.564 | 7 / 2.756 |
| G1 | 1,0 m | 1.892 | 3.612 | 7.564 | 13 / 3.892 |
| D2 | 0,5 m | 7.395 | 14.448 | 29.576 | 0 / 0 |
| **LOD1 gesamt** |  |  |  | **44.704** | **6.648; gesamt 51.352** |

LOD1 liegt mit 51.352 Dreiecken unter dem Limit von 1.300.000. D1/G1-Waende haben im Standard eine Mindestbreite von 1,2 m.

D2 sichtbare Hoehenbytes wurden mit dem Blob aus `9d3f8fc` verglichen: bytegleich, SHA-256 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`. Derselbe Hash steht im Meshmanifest. D2 verwendet `GB` unveraendert; es gibt dort kein Wandmesh. `pruefe_t42u.py` meldet Summe 0 und in allen Feldern Abweichung 0.

## Regelpruefungen vorher/nachher

Ausgang ist `9d3f8fc`; die Baseline wurde mit denselben Pruefern gegen die Daten aus diesem Commit erneut berechnet. Die folgenden Werte stammen aus den JSON-Berichten (`summe`):

| pruefe_regeln | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| Gesamtsumme | 596 | 570 | -26 |
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 23 | 23 | 0 |
| R3_woelb_m | 22 | 22 | 0 |
| R5_loch | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 66 | 68 | +2 |
| G6_facette | 249 | 220 | -29 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 23 | 24 | +1 |

| R8-Kreuzung | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| Summe | 48 | 48 | 0 |
| R8_stufe | 9 | 9 | 0 |
| R8_gitter | 10 | 10 | 0 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 24 | 24 | 0 |

| R9-Form | Vorher | Nachher | Delta |
|---|---:|---:|---:|
| Summe | 334 | 334 | 0 |
| R8b_delle | 25 | 25 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 275 | 275 | 0 |

Keine Regel steigt um mehr als 5. Zaehler je Kachel:

| Pruefer | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---:|---:|---:|
| pruefe_regeln | 36 → 36 | 13 → 13 | 8 → 8 |
| r8_kreuzung | 8 → 8 | 1 → 1 | 0 → 0 |
| r9_form | 26 → 26 | 8 → 8 | 0 → 0 |

Die acht D2-Treffer aus `pruefe_regeln` sind dieselben wie in der Baseline; D2 hat in r8 und r9 weiterhin null Treffer. D1/G1 haben bei gleicher Trefferzahl teilweise andere Trefferkoordinaten als der Commit `9d3f8fc`: Der bereits im Branch vorhandene `relief_daten.json.gz`-Blob unterscheidet sich ausserhalb D2 vom Baseline-Blob. Diese Datei wurde in dieser Arbeit nicht geaendert; die D2-Teilflaeche ist bytegleich.

## Pruefungen und Bilder

- Build: `RELIEF_NEU=1 python3 gen_relief.py && RELIEF_NEU=1 python3 baue_html.py` erfolgreich.
- Lochscan: 9 Gelaende-Meshes, 44.704 Dreiecke, 0 innere offene Kanten.
- Kern- und Wandtests: 6 bestanden. Offline-HTML-Test: bestanden; Viewer enthaelt echte D1/G1/D2-Meshes.
- `pruefe_regeln`, `r8_kreuzung` und `r9_form` enden wegen ihrer bestehenden Treffer mit Exitcode 1; die Zahlen entsprechen den obigen Vergleichen. `pruefe_t42u.py`: Summe 0.
- `neu/tests/test_beanstandungen.py`: 7/7 weiterhin rot, ohne Schwellenanpassung: D1/G1-Kreuzungsstufe 1,389 m (Grenze 0,20), 24 Wegenden (erwartet 0), G1-Delle 0,42 m (Grenze 0,30), 41 D1-Saegezahn-Elemente (erwartet 0), Kantenstaerke des dort fest eingebetteten D1-Negativbilds 2,24 (Grenze 3,00), F1-Wegende 0,17 m und C1-Wegenden 0 (Grenze 0,10 bzw. mindestens 1), Schattenartefakt 0,307 (Grenze 0,25). Diese Tests pruefen weiter Teile der Legacy-Hoehenfelder und ein festes Negativbild; die neuen separaten Wandmeshes beheben diese offenen Punkte nicht nachweislich.
- `neu/nahbild.py` erzeugte 36 finale Bilder fuer D1/G1/D2 unter `/tmp/nahbild_pwand_release/` (Ton und Textur). Nahbilder D1/G1 bei Profilwand-Fuss und Streiflicht liegen unter `/tmp/wandnah_pwand_src1/`; die Kameras fuer den gezielten Lauf stammen aus `/tmp/k_n2.json`.

Angesehen wurden insbesondere:

- D1 bei etwa 140|35: `/tmp/wandnah_pwand_src1/D1_wand_140_35_fuss.png` und `/tmp/wandnah_pwand_src1/D1_wand_140_35_streiflicht.png`.
- G1 bei etwa 260|25: `/tmp/wandnah_pwand_src1/G1_wand_260_25_fuss.png` und `/tmp/wandnah_pwand_src1/G1_wand_260_25_streiflicht.png`.
- D1/G1/D2 Ton: `/tmp/nahbild_pwand_release/clay/D1_wandfuss.png`, `/tmp/nahbild_pwand_release/clay/G1_wandfuss.png`, `/tmp/nahbild_pwand_release/clay/D2_draufsicht.png`.

Wandfuss und -krone sind im neuen Mesh geometrisch scharf und nicht durch das Hoehenraster weichgezeichnet. Die Profilpolylinien zeigen an Richtungswechseln weiterhin sichtbare Facetten und eine kantige Kontur. Der feste Negativbildtest ist deshalb weiterhin rot; die 3D-Nahbilder pruefen diese alte Bildmetrik nicht. Die D2-Ton-Draufsicht wirkt nahezu eben, was hier nur die gewaehlte Draufsicht/Kameraposition zeigt; ihre Hoehenwerte sind durch den Bytevergleich abgesichert.

## Annahmen, Grenzen und offene Punkte

- Die Quellzellhoehe ist fuer D1/G1 massgeblich. Eckwerte werden aus angrenzenden Quellzellen gemittelt; die Quellspalten selbst bleiben unveraendert. Dadurch hat D1/G1 ein 1-m-Raster, waehrend D2 exakt auf dem vorhandenen 0,5-m-Raster bleibt.
- Wandprofile werden als absolute Hoehen interpretiert und innerhalb der jeweiligen Kachel mit einem Breitenrand abgeschnitten. WANDVAR=1 ist Standard; WANDVAR=0 ist die getestete breitere Alternative.
- Profilkonturen bleiben an ihren Stützpunkten polygonal. Eine weitere Konturglattung waere ein eigener Variantenvergleich, da sie die vorgegebenen Polylinien veraendern kann.
- Die sieben Beanstandungstests bleiben offen; insbesondere Rampenstufen, Wegenden, Delle, Saegezahn/Wellen und die alte Wandbildmetrik sind nicht Teil dieses Wandmesh-Fixes.
- Die geforderte Pruefung des Codex-Lauf-Logs auf `gpt-6-luna` und `xhigh` war in dieser Laufzeit nicht verfuegbar. Die Codex-Konfiguration wurde nicht geaendert.

Kosten: 0 EUR.
