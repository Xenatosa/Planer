# P11b – Standardvariante 0, export_gate.sh mit eigenem Lochscan-Pfad, L3 im Endbau (Basis 8cd6d37)

## L3 im Endbau (Nachtrag)
`bau_endstand.sh` baut jetzt auch L3 (`relief_l3.py`) und vergleicht 20 Ausgaben, neu sind `pruefung/l3_rueck.npz` und `pruefung/l3_bericht.json`. Alle 20 sind bitgleich zu 8cd6d37. Laufzeit 190–206 s.
- Ein einfacher Nachschritt reicht nicht für bitgleiche Daten. `gen_relief → pipeline → vc → L3 → vc` liefert relief_daten 2287a361 statt 27840c9f; abweichend sind nur `VC` und `FW.c`.
- Ursache: `gen_textur.py vc` ist nicht idempotent, weil es das vorhandene VC weichzeichnet. L3 wurde in drei Runden entwickelt: 232f113, 3e68969 und 253b914 (= 9bf2801). Jede Runde lief `--aus` → anwenden → vc. VC/FW.c hängen deshalb von allen drei vc-Läufen ab. GB, Objekte und D1 hängen nur von der letzten Runde ab.
- Der Bau spielt genau diese Runden nach. Die beiden alten `relief_l3.py` und die damalige `l3_stellen.json` kommen per `git show`, die sha256 werden geprüft. Das ist nachgemessen: Jede Zwischenrunde trifft den relief_daten-Hash ihres Commits.
- **Offener Punkt für Art/Aufseher:** Reproduzierbar ohne Historie wäre es nur mit einmal neu erzeugten L3-Daten aus `… → vc → L3 → vc`. Das ändert VC/FW.c an rund 400 Punkten und erfordert eine neue Gate-Messung. Diese Entscheidung liegt nicht bei Dev UI.

## (b) Standard auf Variante 0 umgestellt: ja
- `neu/mesh.py`: `STANDARD_GELAENDE_VAR = "0"` gilt für `build_manifest()` (wenn `RELIEF_GELAENDE_VAR` fehlt) und als Vorgabe von `terrain_heights()`. Variante 2 bleibt wählbar.
- Beleg: `bau_endstand.sh` mit entfernter Variable (`env -u RELIEF_GELAENDE_VAR`) ergibt alle 20 Ausgaben bitgleich, terrain_variant „0“. D1/G1/D2 sind geometrisch identisch zu index.html. D2: ebeb46a1/6835acf2/b33d5a64.
- `neu/tests`: Der Test `test_default_variant_is_active_targeted_profile` heißt jetzt `test_variant_2_is_active_targeted_profile`; er setzt `variant="2"` explizit, die Prüfungen sind unverändert. Neu ist `test_default_variant_is_endstand_variant_0`: Ohne Variable gibt es Variante 0, die Höhen-Hashes gleichen dem Viewer-Paket.
- Testlauf: vorher (8cd6d37) 8 failed / 16 passed / 7 errors, nachher 7 failed / 18 passed / 7 errors. Weniger rot: `test_neu_kern` (Pipeline mit Standardvariante läuft). Neu grün: der Endstand-Test. Die übrigen Fehler sind unverändert und schon auf 8cd6d37 vorhanden:
  - Seit L3 passt relief_daten (27840c9f) nicht mehr zur p3d17-Sollquelle b558f441, Variante 2 bricht deshalb ab. Die Prüfung greift also wie gewollt.
  - Der Gate-Adapter erwartet die relief_daten von vor vc.
  - test_beanstandungen.
- Hinweis: `neu/build.json` trägt für D1 noch den Hash vor L3 (6838b44c, Paket 60d9e4a5). So war es schon in 8cd6d37, unverändert gelassen.

## (c) export_gate.sh
- Eigener Ordner per `mktemp -d`, Aufräumen per `trap … EXIT`. Der Lochscan-Pfad ist `GATE_LOCH_JSON`, sonst `LOCHSCAN`, sonst mktemp. Eine vorhandene Datei wird genutzt, eine fehlende dort erzeugt. Übergabe an `pruefe_regeln.py` wie bisher per `LOCHSCAN`. W1-56 nutzt denselben Temp-Ordner. Prüfer und Schwellen sind unverändert.
- Test `pruefung/test_export_gate_lochscan.sh` (grün, `test_export_gate_lochscan.txt`):
  - Eine Kontrolldatei mit offen_innen=7 über `LOCHSCAN` bzw. `GATE_LOCH_JSON` ergibt den Treffer G1_loch_offen wert 7. Genau diese Datei wird also gelesen.
  - Ohne Variable: 0.
  - Der mktemp-Ordner ist danach weg.
  - `/tmp/gate_loch.json`: sha256 und mtime sind vorher und nachher gleich.
  - In export_gate.sh steht kein fester Pfad mehr.

## Gate je Regel (vorher 8cd6d37 mit eigenen Pfaden, nachher neues export_gate.sh)
| Prüfer | vorher | nachher | je_regel + treffer identisch |
|---|---|---|---|
| regeln | 378 | 378 | ja |
| r8 | 33 | 33 | ja |
| r9 | 325 | 325 | ja |
| w1 | 0 | 0 | ja |
| w1_alle56 | 0 | 0 | ja |

## sha256 der Ausgaben
| Ausgabe | 8cd6d37 | Bau Var 0 explizit | Bau Standardvariante |
|---|---|---|---|
| `relief_daten.json.gz` | 27840c9f3598 | 27840c9f3598 | 27840c9f3598 |
| `zellen_relief.csv` | 36f6763bab5e | 36f6763bab5e | 36f6763bab5e |
| `relief_zaehlung.json` | 84b1a5f1a69e | 84b1a5f1a69e | 84b1a5f1a69e |
| `pruefung/platzierung_t59u.json` | 5ba9370696c8 | 5ba9370696c8 | 5ba9370696c8 |
| `pruefung/o18/aenderungen_o18.json` | b5930ff23213 | b5930ff23213 | b5930ff23213 |
| `pruefung/runde_m_aenderungen_t65u.json` | 3f37aaded8a8 | 3f37aaded8a8 | 3f37aaded8a8 |
| `neu/vektor.json` | aac6afff89ec | aac6afff89ec | aac6afff89ec |
| `neu/felder.json` | e4e2ec8f5f4b | e4e2ec8f5f4b | e4e2ec8f5f4b |
| `neu/felder.npz` | 64db8aac398f | 64db8aac398f | 64db8aac398f |
| `neu/zellen_relief.csv` | 99d30e553104 | 99d30e553104 | 99d30e553104 |
| `neu/debug_D1.png` | 87a18bed4248 | 87a18bed4248 | 87a18bed4248 |
| `neu/debug_D2.png` | 402ccbf6ec15 | 402ccbf6ec15 | 402ccbf6ec15 |
| `neu/debug_G1.png` | 3b2984491d69 | 3b2984491d69 | 3b2984491d69 |
| `dorfmap_relief_z25.glb` | dac86ea9f254 | dac86ea9f254 | dac86ea9f254 |
| `pruefung/l3_rueck.npz` | 39f830969da8 | 39f830969da8 | 39f830969da8 |
| `pruefung/l3_bericht.json` | 4789f8a0fff6 | 4789f8a0fff6 | 4789f8a0fff6 |
| `neu/build.json` | fd49358e7079 | fd49358e7079 | fd49358e7079 |
| `neu/relief_neu.json.gz` | b2fd88ff5252 | b2fd88ff5252 | b2fd88ff5252 |
| `index.html` | 5a88d6d28f6d | 5a88d6d28f6d | 5a88d6d28f6d |
| `neu/index.html` | 5a88d6d28f6d | 5a88d6d28f6d | 5a88d6d28f6d |
