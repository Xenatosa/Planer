# P11b (v3) – Endbau mit L3 + L3b + P2b/P2c als echte Schritte, vc idempotent, Standardvariante 0, export_gate.sh (Basis 81b6f94)

Branch `devui/dorfmap-p11b-v3` ab `81b6f94` (art/dorfmap-fertig = L3 + L3b + P2b/P2c + L3c2, #26 gemergt). Kein Force-Push.
- Ersetzt `devui/dorfmap-p11b-v2` (PR #23, Basis d5b17e2) und `devui/dorfmap-p11b` (PR #19, Basis 8cd6d37).
- Kosten: 0 € zusätzlich, Codex: nein (Dev UI selbst), Laufzeit: bau_endstand 435 s (ca. 7 min) / Arbeitszeit ca. 2,5 h (P11b inkl. v2/v3).

## Endbau (Auflage Aufseher): alle Schritte ausgeführt, 25 Ausgaben bitgleich zu 81b6f94
`bau_endstand.sh` baut aus einem leeren Ordner und vergleicht **25 Ausgaben** per sha256: die bisherigen 20 sowie `p2b_rueck.npz`, `p2b_bericht.json`, `l3c_rueck.npz`, `l3c_bericht.json` und `l3c_vc_rueck.npz`.
- **1–6 Grundbau + L3 (8cd6d37):** gen_relief, Variante 0, vc, dann relief_l3-Runden 232f113 → 3e68969 → 8cd6d37 (je `--aus` der Vorrunde → anwenden, dazwischen vc), danach vc, baue_html, payload, waende.
- **7 L3b (d5b17e2):** Runde e7dadd6 ohne vc, danach vc → waende → payload. Die Runden e193584, 9bb5d10 und 1b8a477 (= d5b17e2) laufen je als `--aus` → anwenden → Pipeline.
  - Die letzte Runde läuft mit `relief_l3.py`/`l3_stellen.json` von 1b8a477 (per `git show`). Das aktuelle relief_l3.py ohne Option (L3c2, eingefroren) liefert dieselben Daten, schreibt aber in `l3_bericht.json` zusätzlich `"stufe": "l3_l3b"`.
  - Der Repo-Bericht stammt von 1b8a477; mit dem aktuellen Skript wichen nur diese Datei ab (Probelauf bauD, sonst 24/25 gleich).
  - Die L3b-Schalter (`wasser`, `fw_folgen`, `rampe_m`, `weg_rand_m`, `ufer_*`) sind keine CLI-Flags, sondern stehen je Stelle in `l3_stellen.json`.
  - Die historischen relief_l3.py und l3_stellen.json kommen per `git show` (sha256 geprüft).
- **8 P2b/P2c (a6a4831):** Ablauf wie in `pruefung/p2_analyse/p2c/p2b2_pipe.sh`:
  - Vorher-Stand sichern → `relief_p2b.py` (Basis-GB-Hash-Prüfung im Skript) → `p2b_bruecken.py` → `gen_textur.py vc` → `p2b_vc_lokal.py <Vorher>` → `p2b_r5_textur.py` → payload → waende.
  - P2c ist kein eigener Lauf: Es hat Stellen und relief_p2b.py erweitert und dieselbe Pipeline auf d5b17e2 neu ausgeführt.
- **vc-Läufe:** In den Schritten 2a–7 nutzt der Bau das historische `gen_textur.py@d5b17e2` (sha256 geprüft; seit a10fc1e unverändert). Damit ist der Stand tatsächlich entstanden. Ab Schritt 8 läuft das aktuelle (idempotente) gen_textur.py.
- **11 L3c2 (81b6f94):** Kette wie in ERGEBNIS_L3c2 (Abschnitte 1 und 8): Vorher-Stand sichern → `relief_l3.py --stufe-c` → `gen_textur.py vc` → `pruefung/l3c_vc_lokal.py <Vorher>` → payload → waende.
  - `relief_l3.py` ohne Option (Schritt 7) ist der eingefrorene L3/L3b-Lauf (`massstab_l3_l3b_eingefroren`).
- **Nachweis:** zwei frische Läufe der Endfassung aus leerem Ordner (RELIEF_GELAENDE_VAR=0 explizit und Standardvariante ohne Variable), je 25/25 bitgleich zu 81b6f94 (`sha256_bau_*.txt`). Vorher waren auf a6a4831 zwei Läufe ebenfalls bitgleich.
- Der Repo-Stand ist **unverändert 81b6f94**. Gegenüber v2 entfällt die neue E4-Referenz.

## vc idempotent (Nachtrag 4)
**Ursache.** In `vc_fleckrand_p3` kommen 107 Randpunkte in E4 in 200 Iterationen nicht unter ZIEL 62. Beim Abbruch (max_it) wird das Zwischenergebnis geschrieben, und der nächste Lauf rechnet von dort aus 200 weitere Iterationen.
- Folge: Jeder Lauf ändert E4 weiter (auf d5b17e2 mit altem Code 106/79/48/25 Punkte je Lauf, max. 2).
- Es gibt keinen Zufall (Seeds fest), keine Threads, keine Dict-/Set-/Datei-Reihenfolge, und die Float-Summen sind deterministisch.

**Fix** (`gen_textur.py`): Ohne Konvergenz wird auf dem gerundeten Gitter bis zum Fixpunkt weitergerechnet. Ist die Eingabe schon ein Fixpunkt, bleibt sie unverändert. Wo der Rand konvergiert, ist das Ergebnis byte-gleich wie bisher; die Schwellen sind unverändert.

**Nachweis.**
- Alter Code auf a6a4831, zwei Läufe hintereinander: verschiedene Hashes (123c2910… ≠ 5cc2a53c…).
- `pruefung/test_vc_idempotent.sh` (neuer Code, auf 81b6f94): Lauf 1 = Lauf 2 (`p11b/test_vc_idempotent.txt`).
- Frische Bauläufe sind bitgleich (s. o.).

**Rest in den Daten (bewusst nicht übernommen).** 81b6f94 enthält in E4 noch den historischen, nicht konvergierten Fleckrand. P2b hat ihn mit `p2b_vc_lokal.py` außerhalb der P2b-Stellen sogar ausdrücklich eingefroren.
- Ein vc-Lauf mit dem neuen Code führt ihn **einmal** auf den Fixpunkt: nur E4, x 171,5–178, z 129,5–155,5, 107 Vertices, max. 2 Farbstufen je Kanal; geändert werden VC und das daraus abgeleitete FW.c.
- Danach ist der Stand stabil. Wegen der Auflage „bitgleich zum Endstand“ ist das hier nicht übernommen. Übernehmen wäre eine Entscheidung für Art/Aufseher und mit einem `gen_textur.py vc` erledigt.

**Warum P11 das verdeckt hat.** Beide P11-Nachweisläufe bauten aus leerem Ordner. Sie führten also dieselbe deterministische Folge von vc-Läufen auf denselben Eingaben aus und waren deshalb bitgleich. Die Nicht-Idempotenz zeigt sich erst, wenn vc auf seiner eigenen Ausgabe noch einmal läuft. Deshalb muss der Bau die vc-Runden der Historie nachspielen.

## (b) Standard auf Variante 0 umgestellt: ja
- `neu/mesh.py`: `STANDARD_GELAENDE_VAR = "0"` gilt für `build_manifest()` (wenn `RELIEF_GELAENDE_VAR` fehlt) und als Vorgabe von `terrain_heights()`. Variante 2 bleibt wählbar.
- Beleg: `bau_endstand.sh` mit entfernter Variable (`env -u RELIEF_GELAENDE_VAR`) ergibt alle 20 Ausgaben bitgleich, terrain_variant „0“. D1/G1/D2 sind geometrisch identisch zu index.html. D2 (auf a6a4831 neu gemessen): ebeb46a1/6835acf2/b33d5a64.
- `neu/tests`: Der Test `test_default_variant_is_active_targeted_profile` heißt jetzt `test_variant_2_is_active_targeted_profile`; er setzt `variant="2"` explizit, die Prüfungen sind unverändert. Neu ist `test_default_variant_is_endstand_variant_0`: Ohne Variable gibt es Variante 0, die Höhen-Hashes gleichen dem Viewer-Paket.
- Testlauf: vorher (8cd6d37) 8 failed / 16 passed / 7 errors, nachher 7 failed / 18 passed / 7 errors. Weniger rot: `test_neu_kern` (Pipeline mit Standardvariante läuft). Neu grün: der Endstand-Test. Die übrigen Fehler sind unverändert und schon auf 8cd6d37 vorhanden: Auf v3 (a6a4831) identische Fehlerliste: 7 failed / 18 passed / 7 errors.
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

## Bezugswerte 81b6f94 (neu gemessen, eigene Pfade; v3-Stand = 81b6f94-Daten)
| Prüfer | nachgemessen | Anmerkung |
|---|---|---|
| regeln | 372 | je_regel = L3c2_gate_vorher_nachher „nachher“ (G5 34, G6 217). Die Repo-Datei `pruefung/regeln_letzter_lauf.json` steht noch auf 371, ist also nach L3c2 nicht aktualisiert. |
| r8 | 31 | identisch zur Repo-Datei (je_regel + treffer) |
| r9 | 325 | identisch |
| w1 / w1_alle56 | 0 / 0 | identisch |
| Lochscan offen_innen | 0 | – |

- D2 (index.html): surface ebeb46a1, sides 6835acf2, bottom b33d5a64, Normalen 3bf24e5f. Das ist unverändert seit d5b17e2 (`d2_hashes_81b6f94.json`).
- Gate-Läufe: `gate_81b6f94/`.

## sha256 der Ausgaben
Siehe `sha256_bau_var0_explizit.txt` und `sha256_bau_standardvariante.txt`: 25/25 „gleich“.
