# P11 – reproduzierbarer Endbau (Basis art/dorfmap-fertig @c6a3db0)

Branch `devui/dorfmap-p11`. Ein Befehl: `sh bau_endstand.sh [AUSGABE]` (aus `relief3d/`, Ausgabeordner leer).

## 1) build_manifest(): D1-Kreuzung an P2 angepasst (neu/mesh.py)
- P2 (5a314c9/9ace686, `P2_BEHALTEN=0,1,2,3,4,7,10,11`) hat die Rampen 5, 6, 8, 9 und X069 entnommen. `relief_daten.json.gz` hat 9 statt 13 `rampenwege`; neue Pfadindizes 0..8 = alte 0,1,2,3,4,7,9,10,11.
- Die D1-Kreuzung ist unverändert dieselbe: alte rampe_2 = Pfad 2, alte rampe_11 (X084) = Pfad 8. Beide Polylinien sind punktgleich zu d181fa6 (geprüft). Der Schnitt liegt bei (152.44, 28.46), Paar (2, 8).
- Geändert: Die Erwartung `(2, 11)` wird zu `D1_KREUZUNG_PAAR = (2, 8)`. Die Polylinien werden über `D1_KREUZUNG_PFAD = {2: 2, 11: 8}` gelesen. Gate- und Lösungsnamen bleiben `rampe_2/rampe_11`, deshalb greifen alle Zweige (`index == 11`) und die Lösungsdateien wie bisher. Keine Prüfung entfernt: Fehlt die Kreuzung, bricht es weiter ab, und der Achsstützen-Vergleich der Lösung bleibt.
- Ergebnis unverändert: Mit der alten Zuordnung auf a10fc1e-Daten liefert der geänderte Code für Variante 2 D1 9619da50…, G1 38afeb30…, D2 749d3c4b…. Das ist bitgleich zu ee46fe5/a10fc1e build.json. Auf P2-Daten läuft Variante 2 jetzt durch (D1 9e589d63…, G1 38afeb30…, D2 749d3c4b…). Der Endstand (Variante 0) ist unberührt.

## 2) p3d17-Prüfsumme (neu/mesh.py, Doku in neu/pipeline.py)
- Ursache: Die Lösungsdateien p3d17/p3d18 tragen `source_relief_sha256 = 5e8fdb51…` (relief_daten von p3d18/ee46fe5). P3 a10fc1e hat nur VC/FW.c geändert (Höhen und Wege bitgleich), danach bfed8424…. P2 9ace686 hat Rampen entnommen, danach b558f441…. Variante 2 brach deshalb seit P3 ab.
- Neu: `P3D17_QUELLE_SOLL_SHA256 = b558f441…` (relief_daten.json.gz von c6a3db0, bitgleich aus dem Endbau) und `P3D17_LOESUNG_HERKUNFT_SHA256 = 5e8fdb51…` (Herkunft der Lösungsdatei). Beide werden geprüft; jede andere Quelle bricht weiter ab. Achsstützen-Prüfung unverändert.
- Endbau mit `RELIEF_GELAENDE_VAR=0` (Variante des Endstands, `terrain_variant "0"` im Paket, Erzeugung laut ERGEBNIS_P2_V2): Dort greifen beide Stellen nicht. `neu/pipeline.py` läuft auch mit Variante 2 ohne Abbruch durch. `neu/tests/test_gen_relief.py` und `test_gelaende_mesh.py` (Variante 2): 6 passed.

## 3) Ein-Befehl-Bau `bau_endstand.sh`
Arbeitskopie unter AUSGABE: versionierte Quellen, ohne Ausgaben und ohne Prüfbilder; `_alt` nur lesend verlinkt. Dann:
`gen_relief.py` → `RELIEF_NEU=1 RELIEF_GELAENDE_VAR=0 gen_relief.py` (pipeline) → `gen_textur.py vc` → `RELIEF_NEU=1 baue_html.py` (Bundle + index.html, neu/index.html) → `html_payload_p3.py` → `waende_einsetzen.py`.
Danach prüft das Skript, welche Dateien geschrieben wurden (genau die 18 Ausgaben), und vergleicht je Ausgabe die sha256 mit dem Repo. Exit 1 bei Abweichung. Laufzeit 101–102 s (gen_relief 71 s, pipeline 10 s, vc 14 s, html 1 s, Wände 5 s), dazu einmalig `npm ci` für die Werkzeuge.

### esbuild-Drift (geklärt, gepinnt)
- Das Bundle in index.html ist seit 6e58af0 (p3d5) unverändert. In c6a3db0 ist es bytegleich zu esbuild 0.19.12…0.24.2 auf `main.js@6e58af0`, getestet mit 0.14–0.28.
- `/tmp/w3` (Link auf `/workspace/.p3_node`) hat esbuild 0.28.2. Ab 0.25 faltet der Minifier Konstanten (`7*16`→`112`) und zieht `REVISION` ein (`"three.js r170"`); dazu kommen Umschreibungen von switch/if. Dadurch ändern sich Bytes und Bezeichner. three ist in beiden 0.170.0.
- Gepinnt: `bau/package.json` + `bau/package-lock.json` (esbuild 0.24.2, three 0.170.0), Installation per `npm ci` nach `NODE_BAU` (Standard /tmp/relief3d_bau_node). /tmp/w3 wird nicht benutzt.
- Viewer-Quelle: `main.js@6e58af0` (sha256 3a942b26…, im Skript geprüft). Die einzige spätere main.js-Änderung b90b0a6 (P3 QA-C3: Feinband FrontSide, Bump) liegt im Legacy-Pfad hinter `if(window.RELIEF_NEU_VIEWER){…return;}` (Zeile 19). Im Relief-Neu-Viewer ist sie nicht erreichbar. `VIEWER_MAIN=arbeitsbaum` baut das aktuelle main.js; das Bundle ist dann absichtlich nicht bitgleich.

### Nebenbefund build.json
In c6a3db0 stand in `neu/build.json` noch der Wandstand aus 5a314c9 (45588 Wanddreiecke), obwohl `relief_neu.json.gz` seit P10e 0 Wanddreiecke hat. `waende_einsetzen.py` hat build.json nie nachgezogen. Jetzt zieht es `waende` und `lod1` nach, im Format von neu/gen_relief.py. build.json ist im Repo auf den frisch gebauten Stand gesetzt (fd49358e…); geändert sind nur die Felder waende und lod1. Das ist die einzige Ausgabe, die nicht bitgleich zu c6a3db0 ist.

## sha256 vorher (c6a3db0) / nachher (zwei frische Bauten in leeren Ordnern)
| Datei | c6a3db0 | Bau 1 | Bau 2 | |
|---|---|---|---|---|
| `relief_daten.json.gz` | b558f441b1fa | b558f441b1fa | b558f441b1fa | gleich |
| `zellen_relief.csv` | 36f6763bab5e | 36f6763bab5e | 36f6763bab5e | gleich |
| `relief_zaehlung.json` | 84b1a5f1a69e | 84b1a5f1a69e | 84b1a5f1a69e | gleich |
| `pruefung/platzierung_t59u.json` | 5ba9370696c8 | 5ba9370696c8 | 5ba9370696c8 | gleich |
| `pruefung/o18/aenderungen_o18.json` | b5930ff23213 | b5930ff23213 | b5930ff23213 | gleich |
| `pruefung/runde_m_aenderungen_t65u.json` | 3f37aaded8a8 | 3f37aaded8a8 | 3f37aaded8a8 | gleich |
| `neu/vektor.json` | aac6afff89ec | aac6afff89ec | aac6afff89ec | gleich |
| `neu/felder.json` | e4e2ec8f5f4b | e4e2ec8f5f4b | e4e2ec8f5f4b | gleich |
| `neu/felder.npz` | 64db8aac398f | 64db8aac398f | 64db8aac398f | gleich |
| `neu/zellen_relief.csv` | 99d30e553104 | 99d30e553104 | 99d30e553104 | gleich |
| `neu/debug_D1.png` | 87a18bed4248 | 87a18bed4248 | 87a18bed4248 | gleich |
| `neu/debug_D2.png` | 402ccbf6ec15 | 402ccbf6ec15 | 402ccbf6ec15 | gleich |
| `neu/debug_G1.png` | 3b2984491d69 | 3b2984491d69 | 3b2984491d69 | gleich |
| `dorfmap_relief_z25.glb` | dac86ea9f254 | dac86ea9f254 | dac86ea9f254 | gleich |
| `neu/build.json` | e8502af5bc63 | fd49358e7079 | fd49358e7079 | Bau1=Bau2, ≠ c6a3db0 |
| `neu/relief_neu.json.gz` | c5d2fca2d64a | c5d2fca2d64a | c5d2fca2d64a | gleich |
| `index.html` | 15bdfabc8317 | 15bdfabc8317 | 15bdfabc8317 | gleich |
| `neu/index.html` | 15bdfabc8317 | 15bdfabc8317 | 15bdfabc8317 | gleich |

Volle Hashes: `sha256_bau1.txt`, `sha256_bau2.txt`. Geschriebene Dateien: `geschrieben_bau1.txt`.

## Nachweise
- Gate (index.html/relief_daten bitgleich): regeln 397, r8 33, r9 325, W1 0, W1 alle 56 0. je_regel und treffer sind identisch zu den P10e-Läufen (`gate_*.json`). Laufzeit 30 s.
- D2 bitgleich: surface ebeb46a1…, sides 6835acf2…, bottom b33d5a64…. D1, G1 und D2 sind geometrisch identisch zu index.html (`hash_vergleich.md`).
- Lochscan 56 Kacheln: offen_innen 0. Kontrolle C3 (1 Dreieck entfernt): 3 Treffer in C3 (`lochscan_*.md`).
- Kein Fallback mehr: `baue_alle_kacheln.py` rechnet build_manifest() mit der Endstand-Variante (0) neu. Jeder Fehler bricht ab. Zusätzlich müssen die Höhen-Hashes zu `neu/relief_neu.json.gz` passen. `prototyp_quelle` im Lauf: `neu.mesh.build_manifest (Variante 0)` (`alle_kacheln_build.json`).
- vektor.json, zellen_relief.csv (beide), felder.json und felder.npz: bitgleich neu erzeugt, im Repo unverändert.
