# Ergebnis pvektor – Vektorschicht und globale Abstandsfelder

Branch `art/dorfmap-pvektor`; Ausgangs-HEAD vor den Änderungen: `7c0df80`. Die Alt-Pipeline bleibt Standard. `RELIEF_NEU=1` leitet `gen_relief.py` und `baue_html.py` auf Ausgaben unter `relief3d/neu/`; der Standardbuild überschreibt diese nicht.

## Änderungen

- `neu/vektor.py` liest die unveränderten Zellquellen und `raster_c20_z25_overlay_plaetze_wege.csv`. Erzeugt Wege als geskelettierte Catmull-Rom-Mittellinien, klassifizierte Breiten, Höhenprofile und 4-m-Ausläufe an echten Linienenden. Alle 2.839 Wegzellen liegen im zugehörigen Korridor. 44 Weg-IDs ergeben 62 Splines.
- Kreuzungen und Weg-Platz-Anschlüsse werden pro zusammenhängendem Cluster als eine gemeinsame ebene Polygonfläche abgelegt. Das Ausgabeformat enthält einen 2,4-m-Weichrand. Insgesamt 88 Flächen; D1: 1, G1: 4, D2: 11.
- Wände/Klippen werden als 260 profilierte Polylinien mit mindestens 1,2 m Breite ausgegeben. Wasser umfasst 60 zusammenhängende Flächen; die Bauzonen umfassen 7 Bestands- und 25 Planflächen.
- `neu/felder.py` erzeugt sechs globale signierte Felder (`weg`, `kreuzung`, `wand`, `wasser`, `bauzone_bestand`, `bauzone_plan`) in 303×336 Zellen über alle 56 Kacheln. Innen ist negativ, außen positiv; es gibt keinen kachelweisen Zuschnitt.
- `neu/gen_relief.py` schreibt `vektor.json`, `felder.npz`, Metadaten und eine bytegenaue Kopie der Zellquelle als `neu/zellen_relief.csv`. Die Quell-Diff-Zahl ist 0; SHA-256 beider CSVs: `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa`. SHA-256 von `vektor.json`: `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e`; von `felder.npz`: `64db8aac398fe627ee92935b662a0106d983337f57dd1b0412a7c3f5561fa41a`.
- `neu/baue_html.py` baut eine Offline-Diagnoseansicht nur für D1/G1/D2. Die drei geprüften Aufsichtbilder liegen unter `neu/debug_D1.png`, `neu/debug_G1.png` und `neu/debug_D2.png`.

Neue Diagnoseausgabe: `RELIEF_NEU=1 python3 gen_relief.py` gefolgt von `RELIEF_NEU=1 python3 baue_html.py` im Ordner `relief3d`.

## Prüfungen

| Prüfung | Ergebnis |
|---|---:|
| `node neu/tests/test_vektor.js` | bestanden; 2.839/2.839 Wegzellen abgedeckt; D1/G1-Flächen vorhanden |
| `node neu/tests/test_felder.js` | bestanden; 303×336, sechs Felder, Kachelnahttest bestanden |
| `node neu/tests/test_pipeline.js` | bestanden; zwei Generatorläufe identische SHA-256; Quell-Diff 0 |
| `node neu/tests/test_html.js` | bestanden; Offline-HTML mit genau D1/G1/D2 |
| `python3 pruefung/pruefe_t42u.py` | Summe **0** |
| LOD1-Render (`test_dreiecke_l1.js`) | **1.174.554 Dreiecke**, Grenze <1,3 Mio. bestanden |
| Lochscan | 0 offene Innenkanten; 1.700.454 Dreiecke im Vollmodell |

Wegenden aus dem Overlay mit gemessenem 4-m-Auslauf: F1 **4**, G1 **6**. C1 enthält **0 Wegzellen** in der Quelle; dort ist kein Wegendpunkt ableitbar oder prüfbar.

## Gates vor/nach

Die bereitgestellte historische Referenz `9d3f8fc` nennt 596 Treffer für `pruefe_regeln`, 48 für R8 und 334 für R9. Auf dem bereits neueren Ausgangs-HEAD `7c0df80` habe ich vor Änderungen 570/48/334 gemessen. Nach dem Standardbuild blieb es bei 570/48/334. Alle unten aufgeführten Regelzahlen und Fundorte sind zwischen dem direkten Vorher- und Nachherlauf identisch; somit beträgt jede Regeländerung 0. Die Differenz 596→570 war bereits im Ausgangsstand vorhanden.

| Gate | Historische Referenz 9d3f8fc | Vor Änderung (7c0df80) | Nach Build |
|---|---:|---:|---:|
| `pruefe_regeln.py` | 596 | 570 | 570 |
| `r8_kreuzung.py` | 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24) | 48 | 48 |
| `r9_form.py` | 334 (Delle 25, Sägezahn 34, Wellen 275) | 334 | 334 |

D1/G1/D2 je Gate (jeweils vor → nach):

| Gate | D1 | G1 | D2 |
|---|---:|---:|---:|
| `pruefe_regeln.py` | 36 → 36 | 13 → 13 | 8 → 8 |
| `r8_kreuzung.py` | 8 → 8 | 1 → 1 | 0 → 0 |
| `r9_form.py` | 26 → 26 | 8 → 8 | 0 → 0 |

Die 8 Treffer in D2 bei `pruefe_regeln.py` waren bereits im Vorherlauf vorhanden; es kam keiner hinzu. D2 bleibt in R8/R9 bei 0. Vollständige Zahlen je Regel und Kachel:

### Pruefe Regeln

| Regel | Gesamt vor → nach | D1 vor → nach | G1 vor → nach | D2 vor → nach |
|---|---:|---:|---:|---:|
| `G2_spitze_oben` | 3 → 3 | 0 → 0 | 0 → 0 | 0 → 0 |
| `G2_spitze_oben_fein` | 8 → 8 | 0 → 0 | 0 → 0 | 0 → 0 |
| `G3_spitze_unten` | 3 → 3 | 0 → 0 | 0 → 0 | 0 → 0 |
| `G3_spitze_unten_fein` | 2 → 2 | 0 → 0 | 1 → 1 | 0 → 0 |
| `G5_beule_klippe` | 68 → 68 | 1 → 1 | 0 → 0 | 0 → 0 |
| `G6_facette` | 220 → 220 | 5 → 5 | 4 → 4 | 0 → 0 |
| `G7_wand_glatte_flaeche` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| `G7b_wandkontur_feld` | 24 → 24 | 0 → 0 | 0 → 0 | 0 → 0 |
| `G7b_wandkontur_kantenschaerfe` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| `G7b_wandkontur_rauheit` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| `G8_fluss_nicht_bis_rand` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| `R1_blind` | 24 → 24 | 2 → 2 | 1 → 1 | 0 → 0 |
| `R2_getrennt` | 15 → 15 | 1 → 1 | 0 → 0 | 1 → 1 |
| `R3_laengs_m` | 35 → 35 | 6 → 6 | 1 → 1 | 0 → 0 |
| `R3_quer_pct` | 23 → 23 | 11 → 11 | 0 → 0 | 0 → 0 |
| `R3_woelb_m` | 22 → 22 | 10 → 10 | 0 → 0 | 0 → 0 |
| `R5_loch` | 17 → 17 | 0 → 0 | 0 → 0 | 0 → 0 |
| `R6_wasser_schnee` | 4 → 4 | 0 → 0 | 3 → 3 | 0 → 0 |
| `T1_fleckrand` | 94 → 94 | 0 → 0 | 3 → 3 | 7 → 7 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 → 1 | 0 → 0 | 0 → 0 | 0 → 0 |

### R8 Kreuzungen und Wegenden

| Regel | Gesamt vor → nach | D1 vor → nach | G1 vor → nach | D2 vor → nach |
|---|---:|---:|---:|---:|
| `R8_gitter` | 10 → 10 | 2 → 2 | 0 → 0 | 0 → 0 |
| `R8_quer` | 5 → 5 | 1 → 1 | 0 → 0 | 0 → 0 |
| `R8_stufe` | 9 → 9 | 2 → 2 | 0 → 0 | 0 → 0 |
| `R8a_wegende` | 24 → 24 | 3 → 3 | 1 → 1 | 0 → 0 |

### R9 Form

| Regel | Gesamt vor → nach | D1 vor → nach | G1 vor → nach | D2 vor → nach |
|---|---:|---:|---:|---:|
| `R8b_delle` | 25 → 25 | 2 → 2 | 1 → 1 | 0 → 0 |
| `R9_saegezahn` | 34 → 34 | 1 → 1 | 1 → 1 | 0 → 0 |
| `R9w_wellen` | 275 → 275 | 23 → 23 | 6 → 6 | 0 → 0 |

## D2-Regressionsbasis und Quelldaten

Vorher/Nachher-SHA-256 von `index.html`: `b723acdf076834ce780fedd6d62020ac838a45530053ec3bbb049115e62978a1`; von `relief_daten.json.gz`: `5e8fdb51c3f3dff9ad2c03c32c7a39ee1a4f97a3bc0942d47a352b1d0b4f0e88`. Beide Standardartefakte blieben bytegleich. Beim neu erzeugten Legacy-Sidecar änderten sich 14.429 Zeilen außerhalb D2, ausschließlich in der abgeleiteten Spalte `boden_anzeige_m`; in D2 änderte sich keine Zeile.

Die neue Sidecar-Datei unter `neu/` ist bytegleich zur Zellquelle. Geänderte Quellwerte je Spalte: `untergrund` 0, `hindernis_art` 0, `hindernis_id` 0, `wasser_eis` 0, `ebene` 0, `bauzone_bestand` 0, `bauzone_plan` 0, `begehbar` 0 und `bebaubar` 0. Die Quelldateien und `../referenz/*` wurden nicht geändert.

## Annahmen und Grenzen

- Straßenbreiten sind aus Rasterdicke und Straßenklasse abgeleitet: Gasse 3,6 m, Anbindung 3,2 m, Hausweg 2,4 m. Die Werte sind nicht als vermessene Breiten belegt.
- Kreuzungen werden aus verschiedenen Weg-IDs oder einem Weg innerhalb von zwei Rasterzellen zu einem `platz` abgeleitet. Höhen werden dort aus dem Median der Quellhöhen gesetzt.
- Wandoberkanten nehmen das lokale Maximum der Quellhöhen im 11×11-Zellenfenster; die Unterkante ist Oberkante minus `klippe_hoehe_m`. Das ist ein Startprofil, keine unabhängige Vermessung.
- Die Zellquelle hat kein Wasser-Spiegelniveau; `z_m` der Wasserpolygone nutzt vorläufig den Median von `hoehe_m`.
- Die neue HTML-Seite ist eine 2D-Diagnoseansicht. Vektorflächen und Abstandsfelder werden noch nicht in ein neues 3D-Mesh eingespeist; die Standard-3D-Ausgabe bleibt daher die Alt-Pipeline.
- Für C1 fehlen Wegquellen im Overlay. Der dort geforderte Auslauf bleibt offen, bis eine Quellgeometrie dafür vorliegt.
