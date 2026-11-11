# Ergebnis p3d22 — Zwischenstand V24

Stand 11.11.2026, Branch `art/dorfmap-p3d22`, Basis `3c7e688`. Dieser Zwischenstand schließt V24 ab; V29, V30 und V3 folgen im selben Bericht.

Marker: `[S]` direkt gemessen oder aus einem ausgeführten Prüferartefakt übernommen; `[R]` vom Diagnosemodell berechnet; `[A]` Annahme für die Ereignis-/Zählerabbildung.

## Ergebnis V24

Der unveränderte V24-Kern ist mit allen Modellgrenzen und den 50 Schnitten aus Runde 05 lösbar. Alle 13 isolierten Läufe und die gemeinsame gewichtete L1-Minimierung endeten mit HiGHS-Status 7, `primal_feasible=true` und **Nullschlupf**. Der gemeinsame Zielfunktionswert ist 0. Das beweist die Machbarkeit des verwendeten Schnittmodells, aber nicht die offiziellen G5/R5-Ziele: Die bedingte Float32-Direkttransfer-Probe dieses gemeinsamen Kandidaten verfehlte sie deutlich.

Die p3d17-Kalibrierung wurde erneut mit dem offiziellen R3-Prüfer ausgeführt. `[S]` Der D1-Hash stimmt bytegenau mit dem Referenzmesh überein; R3 D1 bleibt **6/17/19** (längs/quer/Wölbung), Quellenhash `5e8fdb51c3f3dff9ad2c03c32c7a39ee1a4f97a3bc0942d47a352b1d0b4f0e88`.

### Modell und Belege

- Unveränderte Geometrie und Transfer: `neu/p3d18_joint_mesh_v24.json`; R8-Zentrum `152.54985704503775|28.48954534572434`.
- Verwendete Datei: `codex_jobs/tools/p3d20_r3/event_cuts_cumulative05.json`, **50 Schnitte** (G5 17, R5 24, R4 5, G6 2, R5sp 1, R8G 1), SHA-256 `cb79b89bbd05d67a4607c5c6fa91dc660ea5cad73b1d2eb8b1aa0f30028b7005`.
- Die gemeinsamen Grenzwerte blieben unverändert: Stufe `0,116 m`, Gitter `0,019 m`, Quer `2,95 %`, Einzelquer `19,5 %`, R3 D1 `6/7/7`, Achs- und Ebenenstützen `±0,02 m`, Ebenenkern `r=2,00 m`, Wegende `0,054 m`. Für den Runde-05-Vergleich war R8a-Endrunout deaktiviert; die p3d21-Runde-00-Läufe verwenden ihn aktiviert.
- Die p3d22-Erweiterung enthält 18 nichtnegative Schlupfvariablen und 46 binäre Ereignisfreigaben. Sie ergänzt sechs Zähler-/Obergrenzenzeilen. Der gespeicherte Runde-05-Solve nennt 7.945 Variablen/11.295 Bedingungen; p3d22 enthält 8.009/11.308. Die 64 zusätzlichen Variablen entsprechen Schlupf- und Ereignisfreigaben. **Sieben der 13 zusätzlichen Bedingungen sind gegenüber dem archivierten Runde-05-Bericht nicht aufgeklärt.** Das ist eine verbleibende Reproduktionsgrenze.
- Die G5/R5/R4-Zähler werden mit der Runde-05-Schnittliste und Budgets G5 `69/2`, R5-Loch `22/5`, R4 D1 `0` abgebildet. Die Schnittfreigaben sind keine frische Komponenten-Neuzählung durch die offiziellen Prüfer.

### Isolierte und gemeinsame Lösungen

Alle Schlupfe sind in Metern, Prozentpunkten oder Trefferzahlen angegeben. Die kombinierte Zielfunktion lautet `Σ Schlupf / Skala` (gewichtete L1; Einheiten-Skalen unten). Für die isolierten Szenarien waren jeweils nur die Spalten der genannten Gruppe freigegeben; die übrigen Gruppen blieben hart. Die Gruppen Gitter, Quer und Einzelquer wurden für die getrennte Sicherheitsabstandsauswertung einzeln isoliert.

| Szenario | HiGHS | primal_feasible | Variablen/Bedingungen | Minimale Schlupfe der Gruppe | L1 |
|---|---:|---:|---:|---|---:|
| R3 längs | 7 | ja | 8.009 / 11.308 | Treffer 0; Operatorrest 0 m | 0 |
| R3 quer | 7 | ja | 8.009 / 11.308 | Treffer 0; Operatorrest 0 Prozentpunkte | 0 |
| R3 Wölbung | 7 | ja | 8.009 / 11.308 | Treffer 0; Operatorrest 0 m | 0 |
| Kreuzungsstufe | 7 | ja | 8.009 / 11.308 | 0 m über `0,116 m` | 0 |
| Achsstützen | 7 | ja | 8.009 / 11.308 | 0 m über `0,02 m` | 0 |
| Ebenenkern, `r=2,00 m` | 7 | ja | 8.009 / 11.308 | 0 m über `0,02 m` | 0 |
| Wegende | 7 | ja | 8.009 / 11.308 | 0 m über `0,054 m` | 0 |
| Sicherheitsabstand Gitter | 7 | ja | 8.009 / 11.308 | 0 m über `0,019 m` | 0 |
| Sicherheitsabstand Quer | 7 | ja | 8.009 / 11.308 | 0 Prozentpunkte über `2,95 %` | 0 |
| Sicherheitsabstand Einzelquer | 7 | ja | 8.009 / 11.308 | 0 Prozentpunkte über `19,5 %` | 0 |
| G5 | 7 | ja | 8.009 / 11.308 | gesamt 0; D1 0 Treffer über `69/2` | 0 |
| R5-Loch | 7 | ja | 8.009 / 11.308 | gesamt 0; D1 0 Treffer über `22/5` | 0 |
| R4 D1 | 7 | ja | 8.009 / 11.308 | 0 Treffer über 0 | 0 |
| Gemeinsam, alle Gruppen | 7 | ja | 8.009 / 11.308 | alle 18 Schlupfvariablen 0 | 0 |

Die Skalen für die L1-Normierung sind: R3-Treffer 1 Treffer, R3 längs/Wölbung 0,08 m Operatorrest, R3 quer 3,5 Prozentpunkte, Kreuzungsstufe 0,116 m, Achse 0,02 m, Ebenenkern 0,02 m, Wegende 0,054 m, Sicherheitsabstand Gitter 0,019 m/Quer 2,95 Prozentpunkte/Einzelquer 19,5 Prozentpunkte sowie je ein Treffer für G5, R5-Loch und R4. G5 und R5-Loch gewichten Gesamt- und D1-Mehrtreffer separat. Der optionale kleinste Ebenenkernradius wurde nicht vermessen; der Radius blieb in allen Läufen fest bei 2,00 m.

### Bedingte offizielle Float32-Probe

Da der gemeinsame Schnittmodell-Kandidat Nullschlupf und null freigegebene G5/R5/R4-Schnitte hatte, wurde genau für diesen Kandidaten eine Float32-Direkttransfer-Probe gerechnet. Es wurde kein Relief-Mesh gebaut. Der vorgeschriebene Lochscan lief mit der bereits vorhandenen `index.html`; Node meldete `offen_innen=0` und 88.728 Dreiecke auf dieser HTML-Seite. Probe-Relief und Gate-Belege liegen in `/tmp` (Dateipfade zusätzlich im JSON).

| Gate | Ausgang `9d3f8fc` | p3d22-V24-Probe | Δ zum Ausgang |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 596 | 626 | +30* |
| R8 gesamt (Stufe/Gitter/Quer/Wegende) | 48 (9/10/5/24) | 48 (9/11/7/21) | 0 gesamt |
| R9 gesamt (Delle/Sägezahn/Wellen) | 334 (25/34/275) | 339 (30/34/275) | +5 gesamt |

`G5_beule_klippe` stieg von 69 auf 74 (**+5**), `R5_loch` von 25 auf 48 (**+23**) und `G11_objekt_schwebt_sinkt` gegenüber dem aktuellen p3d17-Schema von 4 auf 22 (**+18**). Damit ist die gemeinsame offizielle Zielerreichung verfehlt; die Regel-Plus-5-Vorgabe ist ebenfalls verletzt. R8 hat Gitter +1 und Quer +2 gegenüber dem Start, R9 Delle +5. Es wurde keine weitere Gate-Probe gestartet.

\* Der historische Gesamtwert 596 stammt aus einem Prüferschema ohne G11. Der aktuelle p3d17-Replay ist 600; gegenüber diesem gleicheren Schema beträgt die p3d22-Summe +26. Zusätzlich weist der aktuelle Probe-Output `G11_baum_an_wand=4` und `R1_wand=2` aus, die im alten Zählerschema nicht separat vorkommen.

| Regel | Start `9d3f8fc` | p3d22-Probe | Δ |
|---|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 0* (4 aktuell) | 22 | +18 gegen aktuelles Schema |
| G11_baum_an_wand | — | 4 | — |
| G2_spitze_oben | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten | 4 | 3 | -1 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 69 | 74 | +5 |
| G6_facette | 219 | 217 | -2 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G7b_wandkontur_feld | 25 | 23 | -2 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| R1_blind | 24 | 24 | 0 |
| R1_wand | — | 2 | — |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 35 | 35 | 0 |
| R3_quer_pct | 29 | 19 | -10 |
| R3_woelb_m | 31 | 19 | -12 |
| R4_rand | 1 | 2 | +1 |
| R4_schlucht | 0 | 0 | 0 |
| R5_loch | 25 | 48 | +23 |
| R5_spitze | 0 | 0 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten | 1 | 1 | 0 |
| T3_streifen_ringe | 1 | 1 | 0 |
| T4_graue_flussstreifen | 1 | 1 | 0 |
| T5_textur_vs_clay | 1 | 1 | 0 |

| Kachel | p3d20-R05 D1/G1/D2 | p3d22-V24-Probe D1/G1/D2 |
|---|---|---|
| D1 | G11 2; G5 3; G6 2; R1 blind 2; R2 1; R3 längs/quer/Wölbung 4/0/4; R4-Schlucht 1; R5-Loch 6 | G11 Objekt 20, Baum/Wand 4; G5 7; G6 1; R1 blind 2, Wand 2; R2 1; R3 6/7/7; R4-Schlucht 0; R5-Loch 31 |
| G1 | G11 2; G6 3; R1 blind 1; R3 längs 1; R6 3; T1 3 | unverändert: G11 Objekt 2; G6 3; R1 blind 1; R3 längs 1; R6 3; T1 3 |
| D2 | R2 1; T1 7; R8/R9 0 | unverändert: R2 1; T1 7; R8/R9 0; Höhenhash `749d3c4b…` |

Weitere Gate-Werte `[S]` der V24-Probe: R8 D1 `Stufe/Gitter/Quer/Wegende = 2/3/3/1`, G1 und D2 jeweils `0/0/0/0`; R9 D1 `Delle/Sägezahn/Wellen = 8/1/13`, G1 `0/1/12`, D2 `0/0/0`. G1-Hash `38afeb30…`; D2-Hash unverändert `749d3c4b…`.

### Annahmen und Grenzen

- `[S]` Kalibrierung, Hashes, Gate-Zähler und Solverstatus stammen aus ausgeführten Prüfern bzw. gespeicherten Artefakten. `[R]` Schlupf-Minima und L1-Wert sind Solverergebnisse des diagnostischen linearen/MILP-Modells. `[A]` Die festen Nicht-D1-Baselines für die Zählerbudgets sind G5 `67` und R5-Loch `17`, abgeleitet aus dem offiziellen p3d20-R05-Probebericht.
- Der V24-Nullschlupf-Befund gilt für `event_cuts_cumulative05.json`; die Direktprobe belegt, dass diese Schnitte neu entstehende G5/R5-Ereignisse nicht vollständig zählen. Deshalb ist Nullschlupf kein Nachweis der offiziellen Zielerreichung.
- Die HTML-Lochprüfung liest die vorhandene Seite; es gab keinen Meshbau, keine Bilder und keine Übernahme. LOD1 und `t42u` wurden in diesem Auftrag nicht neu berechnet; Quellen, Overlay, G1 und D2 wurden nicht geändert.
- Es wurden weder Prüfer, Grenzwerte noch Zell-/Vektorquellen verändert. Noch offen sind die sieben zusätzlichen Modellbedingungen gegenüber der archivierten p3d20-Runde-05-Zahl und die Validität der Ereignisschnitt-Näherung für neue Komponenten.
