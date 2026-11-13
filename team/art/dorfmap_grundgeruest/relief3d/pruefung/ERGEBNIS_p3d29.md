# Ergebnis p3d29 — Zwischenstand

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d29` · Branch `art/dorfmap-p3d29` · Basis `origin/art/dorfmap-p3d28` @ `29cebf3` · Kosten **0 EUR**.

`[S]` Der p3d29-Machbarkeitssolve und der einmalige Drainage-L1-Fallback sind abgeschlossen; die offizielle Float32-Proberunde 1 steht als Nächstes an. Dieser Zwischenbericht wird nach jedem abgeschlossenen Prüfeschritt aktualisiert.

Marker: `[S]` direkt gemessen oder unverändert ausgeführter Prüfer · `[R]` Modellbefund/abgeleitete Diagnose · `[A]` Annahme · `[F]` Freigabe.

## 1. Modellaenderungen gegen p3d28

`[R]` Die V3-Wegführung, Kreuzung, alle 22 Familien und der Lokalitätskern bleiben aus p3d28 erhalten. Der Übergangsring ist fest 7,5 m breit; seine zulässige Abweichung klingt linear von 20 mm innen auf 1 mm außen ab, außerhalb gilt höchstens 1 mm Abstand zur p3d17-Referenz.

`[R]` Der Priority-Flood nutzt ein Hilfsrelief mit der p3d26-V3-Modellfläche in Weg-/Kreuzungs-/Auslauf-/Rampenendzellen und p3d17-Höhen im restlichen D1-Gitter. Die gespeicherte p3d26-Lösung hat SHA-256 `0b03648f7d71a25783d111b81d7d8b4980e3a5ad9c6760d76209cebae241245e`. Epsilon ist 0 in diesen Zellen und an Übergangskanten mit einem solchen Endpunkt, sonst 1 mm im Gelände.

`[R]` In den bisherigen Klippen-/Schluchtstencils außerhalb des 4,8-m-Wegbands, des 4-m-Kreuzungskerns und der Ausläufe bleibt die zweite Differenz hart an p3d17 gebunden, mit Toleranz `max(0,02 m; 25 % × |Referenz-Zweitdifferenz|)`. Die 2-cm-Untergrenze bewahrt die p3d28-Toleranz für flache Stencils; die relative Komponente lässt große Referenzkrümmungen proportional atmen, statt sie pauschal um 2 cm zu verformen. Innerhalb dieser Zonen entfällt die harte Formbindung; Abweichungen werden als gewichtete L1-Summe mit Gewicht `1 / max(0,02 m; 25 % × |Referenz-Zweitdifferenz|)` bestraft.

`[R]` Die p3d28-R4-Referenzquerschnitte sind entfernt. Der R4-Indikator wird nur über offizielle R4-Ereignisschnitte auf der unveränderten 1,5-m-Grenze abgesichert. R5-Loch-, R8b-Dellen-, G5- und G11-Ereignisschnitte werden nach den Float32-Prüfungen frisch abgeleitet. Es gibt keine R9w-Höhen-Pins oder R9w-Gleichheitsfixierung.

`[S]` Die einzigen p3d29-Änderungen liegen in `codex_jobs/tools/p3d29/`; offizielle Prüfer, Schwellen, Zellquellwerte, Overlay, D1-Wegführung, G1 und D2 wurden nicht verändert. Die p3d29-Ringwahl ist auf 7,5 m festgelegt (`P3D29_CONSTRUCTION_VARIANT=3`, Standard). Der weiche Abflussmodus (`P3D29_DRAINAGE_MODE=soft`) ist ausschließlich der einmalige Hochgewicht-L1-Fallback, falls der harte Solve infeasible ist.

## 2. Machbarkeit

`[S]` Der serielle Hard-Solve endete mit HiGHS Status 8 (`Infeasible`), ohne zulässigen Primalpunkt. Der LP-Gruppenfilter fand bei 6 positiven Slackgruppen einen gruppenweisen Restkonflikt ausschließlich bei `p3d29_drainage`; die LP-Relaxation mit allen Gruppen offen war optimal. Der Filter ist ein gruppenweiser Relaxationsbefund, kein Zeilen-IIS oder Integer-IIS. [Filterbeleg](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_lp_group_filter.json)

`[S]` Der einmalige Soft-Fallback öffnete nur die Abflusskanten-Slacks, mit 10.000 pro Meter und Kante im gewichteten L1-Ziel; alle anderen Gruppen blieben hart. HiGHS fand einen optimalen zulässigen Punkt (Status 7). Die Summe der Kantenabweichungen beträgt 78,456860 m über 5.579 Kanten; die größte Einzelabweichung beträgt 6,151269 m an Kind `128,0|36,5` → Nachfolger `127,5|36,0` (dort `eps=0`). Der gewählte Punkt erfüllt damit die Modellmachbarkeit mit weichem Abfluss, aber nicht die harte Abflussbaum-Bedingung. [Machbarkeitsbeleg](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_feasibility.json) · [Modellbeleg](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_round01_model.json)

Belege liegen unter `codex_jobs/tools/p3d29/results/`.

## 3. Probezahlen je Runde

`[S]` Noch keine offizielle Float32-Proberunde. Es gibt daher keine p3d29-Nachherzahlen und keine Aussage, dass die Ziele oder D2-Regression bestanden sind.

## 4. Regelzahlen vorher/nachher

`[S]` Die Vorher-Spalte „p3d17 Replay“ stammt aus den unveränderten aktuellen-schema Gate-Artefakten. `nicht erhoben` ist ausdrücklich kein bestandenes Gate.

| Regel | 9d3f8fc vorher | p3d17 Replay | p3d29 nachher | D1/G1/D2 vorher |
|---|---:|---:|---:|---:|
| `R1_blind` | 24 | 24 | nicht erhoben | 2/1/0 |
| `R2_getrennt` | 15 | 15 | nicht erhoben | 1/0/1 |
| `R3_laengs_m` | 35 | 35 | nicht erhoben | 6/1/0 |
| `R3_woelb_m` | 31 | 31 | nicht erhoben | 19/0/0 |
| `R3_quer_pct` | 29 | 29 | nicht erhoben | 17/0/0 |
| `R4_rand` | 1 | 1 | nicht erhoben | 1/0/0 |
| `R5_loch` | 25 | 25 | nicht erhoben | 8/0/0 |
| `R6_wasser_schnee` | 4 | 4 | nicht erhoben | 0/3/0 |
| `G2_spitze_oben` | 3 | 3 | nicht erhoben | 0/0/0 |
| `G3_spitze_unten` | 4 | 4 | nicht erhoben | 1/0/0 |
| `G2_spitze_oben_fein` | 8 | 8 | nicht erhoben | 0/0/0 |
| `G3_spitze_unten_fein` | 2 | 2 | nicht erhoben | 0/0/0 |
| `G5_beule_klippe` | 69 | 69 | nicht erhoben | 2/0/0 |
| `G6_facette` | 219 | 219 | nicht erhoben | 3/3/0 |
| `G7_wand_glatte_flaeche` | 1 | 1 | nicht erhoben | 0/0/0 |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | nicht erhoben | 0/0/0 |
| `G11_objekt_schwebt_sinkt` | 0 | 4 | nicht erhoben | 2/2/0 |
| `T1_fleckrand` | 94 | 94 | nicht erhoben | 0/3/7 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | nicht erhoben | 0/0/0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | nicht erhoben | 0/0/0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | nicht erhoben | 0/0/0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | nicht erhoben | 0/0/0 |
| `G7b_wandkontur_rauheit` | 1 | 1 | nicht erhoben | 0/0/0 |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | nicht erhoben | 0/0/0 |
| `G7b_wandkontur_feld` | 25 | 25 | nicht erhoben | 1/0/0 |

| R8-Regel | 9d3f8fc vorher | p3d17 Replay | p3d29 nachher | D1/G1/D2 vorher |
|---|---:|---:|---:|---:|
| `R8_stufe` | 9 | 9 | nicht erhoben | 2/0/0 |
| `R8_gitter` | 10 | 10 | nicht erhoben | 2/0/0 |
| `R8_quer` | 5 | 4 | nicht erhoben | 0/0/0 |
| `R8a_wegende` | 24 | 23 | nicht erhoben | 3/0/0 |
| **R8 Summe** | **48** | **46** | **nicht erhoben** | **7/0/0** |

| R9-Regel | 9d3f8fc vorher | p3d17 Replay | p3d29 nachher | D1/G1/D2 vorher |
|---|---:|---:|---:|---:|
| `R8b_delle` | 25 | 23 | nicht erhoben | 1/0/0 |
| `R9_saegezahn` | 34 | 34 | nicht erhoben | 1/1/0 |
| `R9w_wellen` | 275 | 287 | nicht erhoben | 27/12/0 |
| **R9 Summe** | **334** | **344** | **nicht erhoben** | **29/13/0** |

| Kachel | `pruefe_regeln` p3d17 | R8 p3d17 | R9 p3d17 | p3d29 Probe |
|---|---:|---:|---:|---|
| D1 | 63 | 7 | 29 | nicht erhoben |
| G1 | 13 | 0 | 13 | nicht erhoben |
| D2 | 8 | 0 | 0 | nicht erhoben |

Historische 9d3f8fc Summen: `pruefe_regeln` 596 (ohne G11), R8 48 (`R8_stufe` 9, `R8_gitter` 10, `R8_quer` 5, `R8a_wegende` 24), R9 334 (`R8b_delle` 25, `R9_saegezahn` 34, `R9w_wellen` 275). Der p3d17 Replay im aktuellen Schema hat 600 allgemeine Treffer; R8=46 und R9=344.

## 5. Annahmen, Grenzen und offene Punkte

`[A]` Die p3d26-`surface_grid` ist als V3-Hilfsreliefhöhe an den festen D1-Gitterpunkten interpretiert. Für die Flood-Seed-Maske gelten Kernzellen (Wegband, Kreuzung, Auslauf und Rampenenden); der verbleibende Bereich übernimmt p3d17.

`[R]` Noch offen sind Machbarkeit, eventuelle LP-Schlupfgruppen, höchstens vier offizielle Proberunden, D1/G1/D2-Nachherzahlen und alle Mesh-Gates. Bis alle Probezielwerte bestanden sind, wird kein Mesh gebaut; deshalb sind LOD1, t42u, Hashes, pytest und Bilder noch nicht gemessen.

## Drei-Satz-Schluss

`[S]` Der p3d29-Modellcode ist gegenüber p3d28 angepasst und die offiziellen Prüfer sowie Quelldaten sind unangetastet. `[S]` Machbarkeit und Float32-Probe sind noch nicht ausgeführt, daher gibt es keinen Nachweis für die Zielwerte oder D2-Regressionsfreiheit. `[A]` Der 7,5-m-Ring und die p3d26-gestützte Flood-Reihenfolge sind die festgelegte Standardkonstruktion; bei Infeasibility bleibt nur der einmalige Abfluss-L1-Fallback.

## 3. Float32-Gate-Probe mit Checker-in-the-loop

`[S]` Runde 1 abgeschlossen; Checker-in-the-loop wird fortgesetzt Höchstens vier serielle Runden, je Solve höchstens 600 s. Jede Probe lief über den unveränderten Float32-Direkttransfer und die vier unveränderten offiziellen Prüfer.

| Runde | Solve | `pruefe_regeln` gesamt (D1/G1/D2) | R8 gesamt (D1/G1/D2) | R9 gesamt (D1/G1/D2) | offene Ziele |
|---:|---|---|---|---|---|
| 1 | Optimal | 586 (47/13/8) | 44 (5/0/0) | 347 (31/13/0) | R5_spitze_D1, G6_D1, R9w_total, G5_total, G5_D1; [JSON](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_round01_official_probe.json) |
