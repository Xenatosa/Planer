# P11b (v2) – Standardvariante 0, export_gate.sh mit eigenem Lochscan-Pfad, L3 + L3b im Endbau, vc idempotent (Basis d5b17e2)

Branch `devui/dorfmap-p11b-v2` ab `d5b17e2` (art/dorfmap-fertig mit L3b). Ersetzt `devui/dorfmap-p11b` (PR #19, Basis 8cd6d37; kein Force-Push).
P2b (PR #21) ist nicht enthalten.

## L3 + L3b im Endbau
`bau_endstand.sh` vergleicht 20 Ausgaben. Zwei frische Läufe aus leerem Ordner sind bitgleich (277 s / 270 s).
- L3 (8cd6d37): Runden 232f113, 3e68969, 8cd6d37 (`--aus` der Vorrunde → anwenden, dazwischen vc), dann vc, baue_html, payload, waende.
- L3b (d5b17e2), so wie es entstanden ist (Commit-Historie + ERGEBNIS_L3b „Pipeline“):
  - Runde e7dadd6 anwenden (ohne vc), dann vc → waende → payload (= 4b42226);
  - danach Runden e193584 und 9bb5d10 sowie der aktuelle Stand (= 1b8a477), jeweils `--aus` → anwenden → vc → waende → payload.
- Der Aufruf von `relief_l3.py` ist unverändert. Die neuen L3b-Schalter (`wasser`, `fw_folgen`, `rampe_m`, `weg_rand_m`, `ufer_*`) stehen je Stelle in `l3_stellen.json` und sind keine CLI-Flags.
- Jede Runde ist einzeln gegen ihren Commit nachgemessen: relief_daten, relief_neu, index.html, l3_rueck.npz und l3_bericht.json sind gleich, mit vc genau 1× je Runde.
- Mit dem alten vc ergab der Bau alle 20 Ausgaben bitgleich zu d5b17e2. Mit dem idempotenten vc (s. u.) weichen relief_daten, relief_neu und index.html ab; abweichend ist nur VC (nur E4).

## vc idempotent (Nachtrag 4)
**Ursache.** In `vc_fleckrand_p3` kommen 107 Randpunkte in E4 in 200 Iterationen nicht unter ZIEL 62. Am Abbruch (max_it) wird das Zwischenergebnis geschrieben. Jeder weitere Lauf startet vom eigenen Ausgabestand und rechnet 200 weitere Iterationen. Messung auf d5b17e2 mit altem Code: 106, 79, 48, 25 Punkte je Lauf geändert, max. 2.
- Kein Zufall: Die Seeds sind fest (rng 5/7).
- Es gibt keine Threads und keine Dict-/Set-/Datei-Reihenfolge.
- Die Float-Summen sind deterministisch.

**Fix** (`gen_textur.py`): Ohne Konvergenz nach max_it wird auf dem gerundeten Gitter bis zum Fixpunkt weitergerechnet (hier 2–20 Schritte). Ist die Eingabe schon ein Fixpunkt, bleibt sie unverändert. Wo der Rand konvergiert, ist das Ergebnis byte-gleich wie bisher. Die Schwellen sind unverändert.

**Nachweis.**
- `pruefung/test_vc_idempotent.sh`: Zwei Läufe auf demselben Stand sind bitgleich, auch gleich dem Repo-Stand (`p11b/test_vc_idempotent.txt`).
- Alter Code auf derselben Eingabe: zwei verschiedene Hashes (ea51c6d6…, 45eaf9ed…).
- Zwei frische bau_endstand-Läufe: bitgleich.

**Neue Referenz.** Neu ist der Fixpunkt desselben Verfahrens; der alte Stand war ein zufälliger Zwischenstand nach N Läufen.

| | |
|---|---|
| Abweichung zu d5b17e2 | nur `VC` |
| Kachel | E4, x 171,5–178, z 129,5–155,5, grauer Streifen |
| geänderte Vertices | 249 |
| max. Farbdifferenz | 27 (je Kanal) |
| unverändert | FW.c, GB, WV, FW.h und alle anderen Schlüssel |

- Bild: `/workspace/p11b_vc/E4_vc_vorher_nachher_diff.png`.
- Gate je Regel **und** Trefferliste identisch zu d5b17e2.

**Warum P11 das verdeckt hat.** Beide P11-Nachweisläufe bauten aus leerem Ordner. Sie führten also dieselbe deterministische Folge von vc-Läufen auf denselben Eingaben aus und waren deshalb bitgleich. Die Nicht-Idempotenz zeigt sich erst, wenn vc auf seiner eigenen Ausgabe nochmals läuft. Genau deshalb musste der Bau die vc-Runden der L3-Historie nachspielen (in P11b dokumentiert).
- Die Historie bleibt nötig, weil jede vc-Runde mit anderem GB vom vorherigen VC aus rechnet.
- Ein historienfreier Bau bräuchte ein gespeichertes Basis-VC. Das wäre eine Entscheidung für Art/Aufseher.

## (b) Standard auf Variante 0 umgestellt: ja
- `neu/mesh.py`: `STANDARD_GELAENDE_VAR = "0"` gilt für `build_manifest()` (wenn `RELIEF_GELAENDE_VAR` fehlt) und als Vorgabe von `terrain_heights()`. Variante 2 bleibt wählbar.
- Beleg: `bau_endstand.sh` mit entfernter Variable (`env -u RELIEF_GELAENDE_VAR`) ergibt alle 20 Ausgaben bitgleich, terrain_variant „0“. D1/G1/D2 sind geometrisch identisch zu index.html. D2 (auf d5b17e2 neu gemessen und im v2-Stand): ebeb46a1/6835acf2/b33d5a64.
- `neu/tests`: Der Test `test_default_variant_is_active_targeted_profile` heißt jetzt `test_variant_2_is_active_targeted_profile`; er setzt `variant="2"` explizit, die Prüfungen sind unverändert. Neu ist `test_default_variant_is_endstand_variant_0`: Ohne Variable gibt es Variante 0, die Höhen-Hashes gleichen dem Viewer-Paket.
- Testlauf: vorher (8cd6d37) 8 failed / 16 passed / 7 errors, nachher 7 failed / 18 passed / 7 errors. Weniger rot: `test_neu_kern` (Pipeline mit Standardvariante läuft). Neu grün: der Endstand-Test. Die übrigen Fehler sind unverändert und schon auf 8cd6d37 vorhanden: Auf v2 (d5b17e2 + vc-Fix) identische Fehlerliste: 7 failed / 18 passed / 7 errors.
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

## Gate je Regel (Bezug d5b17e2, eigene Pfade; nachher = v2-Stand)
| Prüfer | vorher | nachher | je_regel + treffer identisch |
|---|---|---|---|
| regeln | 374 | 374 | ja |
| r8 | 33 | 33 | ja |
| r9 | 325 | 325 | ja |
| w1 | 0 | 0 | ja |
| w1_alle56 | 0 | 0 | ja |

## sha256 der Ausgaben (d5b17e2 | v2-Stand = zwei frische Bauläufe)
| Ausgabe | d5b17e2 | v2 |
|---|---|---|
| `relief_daten.json.gz` | 35e40810ded5 | 4973373fabd4 |
| `zellen_relief.csv` | 36f6763bab5e | 36f6763bab5e |
| `relief_zaehlung.json` | 84b1a5f1a69e | 84b1a5f1a69e |
| `pruefung/platzierung_t59u.json` | 5ba9370696c8 | 5ba9370696c8 |
| `pruefung/o18/aenderungen_o18.json` | b5930ff23213 | b5930ff23213 |
| `pruefung/runde_m_aenderungen_t65u.json` | 3f37aaded8a8 | 3f37aaded8a8 |
| `neu/vektor.json` | aac6afff89ec | aac6afff89ec |
| `neu/felder.json` | e4e2ec8f5f4b | e4e2ec8f5f4b |
| `neu/felder.npz` | 64db8aac398f | 64db8aac398f |
| `neu/zellen_relief.csv` | 99d30e553104 | 99d30e553104 |
| `neu/debug_D1.png` | 87a18bed4248 | 87a18bed4248 |
| `neu/debug_D2.png` | 402ccbf6ec15 | 402ccbf6ec15 |
| `neu/debug_G1.png` | 3b2984491d69 | 3b2984491d69 |
| `dorfmap_relief_z25.glb` | dac86ea9f254 | dac86ea9f254 |
| `pruefung/l3_rueck.npz` | b9201bbf00c2 | b9201bbf00c2 |
| `pruefung/l3_bericht.json` | a93919cd2430 | a93919cd2430 |
| `neu/build.json` | fd49358e7079 | fd49358e7079 |
| `neu/relief_neu.json.gz` | 8f4e50381e41 | 1f08242c31ba |
| `index.html` | 7cd7e2d28a07 | 2a2e9aa7df6d |
| `neu/index.html` | 7cd7e2d28a07 | 2a2e9aa7df6d |
