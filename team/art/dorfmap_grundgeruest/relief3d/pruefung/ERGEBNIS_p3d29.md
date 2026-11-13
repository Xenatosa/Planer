# Ergebnis p3d29

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d29` · Branch `art/dorfmap-p3d29` · Basis `origin/art/dorfmap-p3d28` @ `29cebf3` · Kosten **0 EUR**.

Marker: `[S]` direkt gemessen oder unverändert ausgeführter Prüfer · `[R]` Modellbefund/abgeleitete Diagnose · `[A]` Annahme · `[F]` Freigabe.

## 1. Modellaenderungen gegen p3d28

`[R]` V3-Wegführung und Kreuzung bleiben bestehen; der Übergangsring ist auf 7,5 m festgelegt. Lokalität im Kern und Ring bleibt hart: außerhalb höchstens 1 mm Abweichung zu p3d17, im Ring linear von 20 mm auf 1 mm. Alle 22 Familien bleiben hart.

`[R]` Der Priority-Flood wurde auf einem Hilfsrelief neu bestimmt: Weg-, Kreuzungs-, Auslauf- und Rampenendzellen tragen die p3d26-V3-Modellhöhe, alle übrigen Zellen p3d17. Das p3d26-Modell hat SHA-256 `0b03648f7d71a25783d111b81d7d8b4980e3a5ad9c6760d76209cebae241245e`. Epsilon beträgt 0 auf den genannten Zellen und Rampenenden, sonst 1 mm im Gelände.

`[R]` Außerhalb des 4,8-m-Wegbands, des 4-m-Kreuzungskerns und der Ausläufe bleibt die zweite Differenz hart an die p3d17-Referenz gebunden, mit Toleranz `max(0,02 m; 25 % × |Referenz-Zweitdifferenz|)`. Die 2-cm-Untergrenze bewahrt die p3d28-Toleranz bei flachen Stencils; die relative Komponente lässt große Referenzkrümmungen proportional atmen. Innerhalb dieser Zonen entfällt die harte Formbindung; die Abweichung wird mit Gewicht `1 / max(0,02 m; 25 % × |Referenz-Zweitdifferenz|)` als L1-Term bestraft.

`[R]` p3d28-R4-Referenzquerschnitte wurden entfernt. R4 bleibt nur an der offiziellen Grenze über harte Ereignisschnitte gebunden. Es gibt keine R9w-Höhen-Pins und keine R9w-Gleichheitsfixierung. Frische R5-Loch-, R8b-, G5- und G11-Schnitte werden aus der Float32-Probe abgeleitet; zusätzlich wurden G6- und R5-Spitzenereignisse aufgenommen, weil diese explizite D1-Zielwerte haben.

`[S]` Änderungen liegen unter `codex_jobs/tools/p3d29/`, im Ergebnisbericht und in dessen JSON-Belegen. Offizielle Prüfer, Schwellen, Zellquellwerte, Overlay, Referenzdateien, Wegführung, G1 und D2 wurden nicht geändert.

## 2. Machbarkeit

`[S]` Der serielle Hard-Solve endete mit HiGHS Status 8 (`Infeasible`), ohne zulässigen Primalpunkt. Der LP-Gruppenfilter mit allen Gruppen offen war optimal; die positiven Slackgruppen waren `endpoint_r8a`, `p3d29_cliff_form`, `p3d29_drainage`, `p3d29_locality`, `source_monotone` und `variable_bounds`. Beim seriellen Gruppenlöschen blieb als notwendiger Konfliktbestandteil ausschließlich `p3d29_drainage`. Das ist ein LP-Gruppenbefund und kein Zeilen-IIS oder Integer-IIS. [Filter](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_lp_group_filter.json)

`[S]` Der einmalige Soft-Fallback öffnete nur die Abflusskanten-Slacks; das L1-Gewicht beträgt 10.000 pro Meter je Kante. HiGHS fand Status 7 (`Optimal`), aber damit ist der harte Abflussbaum gelockert: Summe der Kantenabweichungen 78,456860 m über 5.579 Kanten; Maximum 6,151269 m an Kind `128,0|36,5` → Nachfolger `127,5|36,0` (epsilon 0). Alle anderen expliziten Familien-Slacks sind 0. [Machbarkeit](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_feasibility.json) · [Modell](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_round01_model.json)

`[S]` Nach den 20 Schnitten aus Runde 1 war Runde 2 mit dem Soft-Abflussmodus infeasible. Ein zusätzlicher LP-Gruppenfilter auf diesen Schnitten fand den Restkonflikt `g5` + `p3d29_drainage`; All-open war optimal. Die All-open-Slacks betrugen 1,998617 zusätzliche G5-D1/G5-gesamt-Ereignisse (normalisiert ebenfalls 1,998617) und 413190,655 normalisierte Abfluss-L1-Einheiten; der maximale Abfluss-Slack des All-open-Punkts ist 5,818794 m. G5-Schnitte liegen an den Komponentenzentren `127,56|27,72`, `128,5|29,0`, `129,25|28,5`, `145,83|5,83`, `147,5|9,5`, `168,0|28,0` und `168,17|29,17`; die vollständigen 20 Stützpunkte stehen in [Runde-1-Folgecuts](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_round01_next_cuts.json). Der All-open-Lauf benötigt zusätzlich 0,141343 m Endauslauf-Slack am rampe_2-Start, Paar `127,25|31,0`–`127,25|31,25`; dieser Endpoint-Slack wurde im Löschfilter aus dem Restkonflikt entfernt. Exakte G5-/Abfluss-Zeilenpositionen gibt der Diagnoselauf nicht aus (`null`), der Filter ist kein Zeilen-IIS. [Runde-2-Filter](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_round02_lp_group_filter.json)

## 3. Float32-Gate-Probe mit Checker-in-the-loop

`[S]` Der unveränderte Float32-Direkttransfer und die offiziellen Prüfer wurden in Runde 1 ausgeführt. Der bestmögliche Probekandidat ist Runde 1; Zielabweichungen blieben. Runde 2 endete beim erneuten Solve infeasible, sodass keine zweite Probe ausgeführt wurde. Damit endete die Schleife nach zwei von höchstens vier Runden. [Loop-Protokoll](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_checker_loop.json)

| Runde | Solve | pruefe_regeln gesamt (D1/G1/D2) | R8 gesamt (D1/G1/D2) | R9 gesamt (D1/G1/D2) | Ergebnis |
|---:|---|---:|---:|---:|---|
| 1 | Optimal | 586 (47/13/8) | 44 (5/0/0) | 347 (31/13/0) | Ziele verfehlt; 20 Schnitte abgeleitet |
| 2 | Infeasible | keine Probe | keine Probe | keine Probe | 20 Schnitte aktiv; LP-Restkonflikt G5 + Abfluss |

`[S]` Runde 1 verfehlte: R5-Spitzen D1 = 3 statt 0; G6 D1 = 11 statt höchstens 3; R9w gesamt = 291 statt höchstens 280; G5 gesamt/D1 = 76/7 statt höchstens 69/2. Gegen p3d17 Replay liegen G5 bei +7 und G6 bei +8; beide überschreiten damit auch die +5-Regelgrenze. R9w liegt bei +4 gegen p3d17, aber verfehlt die strengere absolute Grenze 280.

`[S]` Weitere Ziele aus Runde 1, die bestanden:

- G3 D1 = 0 (Grenze 1)
- R8b D1 = 0 (Grenze 1)
- R5-Löcher = 17 gesamt, 0 D1 (Grenzen 22/5)
- R4-Schlucht D1 = 0
- R3 D1 längs/quer/wölbung = 5/7/7 (Grenzen 6/7/7)
- Kreuzung `152.6|28.4` Stufe/Gitter = 0.073 m/0.019 m, R8 quer ohne Treffer
- Endstufen-Modellgruppe max. Zusatzverletzung = 0 m bei Grenze 0,054 m; D1-R8a-Treffer = 0
- G1 Treffer/Hash unverändert, D2 keine neuen allgemeinen Treffer, D2 R8/R9 = 0/0 und Hash unverändert.

`[S]` Die noch offenen D1-Treffer aus Runde 1 mit Ort (`x|z`, danach Prüferwert):

- G5, 7 Treffer: 145.8|5.8 (0.96); 147.5|9.5 (0.73); 127.6|27.7 (0.86); 129.2|28.5 (0.93); 167.0|28.5 (0.98); 128.5|29.0 (1.05); 135.5|31.9 (1.38).
- G6, 11 Treffer: 142.7|2.1 (28); 146.0|6.8 (47); 146.0|11.5 (36); 150.3|12.3 (15); 151.8|13.0 (6); 154.2|21.5 (14); 155.6|26.2 (7); 126.0|28.4 (9); 132.3|29.1 (6); 157.7|35.4 (7); 152.1|36.6 (8).
- R5-Spitze, 3 Treffer: 148.5|6.0 (0.56); 148.0|6.5 (0.62); 148.0|7.0 (0.59).
- R9w, D1 30 Treffer (global 291, davon G1 12, D2 0): 141.4|0.3 (0.17); 144.1|1.4 (0.28); 146.4|0.5 (0.22); 153.5|0.2 (0.27); 142.4|2.1 (0.29); 152.8|2.4 (0.14); 142.7|11.7 (0.29); 160.1|9.7 (0.41); 145.5|6.7 (0.43); 147.6|6.8 (0.35); 151.0|10.4 (0.4); 167.8|13.8 (0.23); 139.2|19.8 (0.56); 158.8|25.6 (0.23); 164.2|25.2 (0.21); 164.7|26.8 (0.17); 130.8|27.4 (0.37); 135.4|27.8 (0.38); 149.0|27.4 (0.42); 157.3|28.6 (0.41); 167.6|29.9 (0.35); 139.3|31.1 (0.54); 136.8|32.0 (0.39); 139.1|33.0 (0.48); 130.2|33.4 (1.22); 153.6|35.6 (0.19); 157.8|35.9 (0.35); 135.3|40.1 (0.51); 150.0|38.2 (0.23); 155.0|40.8 (0.15). Die vollständige Karte der globalen Treffer steht im [Probe-JSON](../../../../../codex_jobs/tools/p3d29/results/p3d29_V3_round01_official_probe.json).

`[S]` R8 im D1-Checker: `R8_stufe` 2, `R8_gitter` 2 und `R8_quer` 1. Die einzelnen D1-Treffer liegen bei `126,5|31,6` (rampe_2-Start: Stufe 0,44 m, Gitter 0,15), `148,5|2,5` (rampe_11-Start: Stufe 0,40 m) und `156,5|37,5` (rampe_11-Ende: Gitter 0,20, Quer 3,2 %). Das ist getrennt vom Modellindikator für die 0,054-m-Endstufenpaare, dessen maximale Zusatzverletzung 0 m ausweist. D1 hat keinen R8a-Treffer; die insgesamt 20 R8a-Treffer liegen außerhalb D1/G1/D2. Der Kreuzungscluster am offiziellen Prüfpunkt `152,6|28,4` meldet Stufe 0,073 m und Gitter 0,019 m; R8-Quer meldet dort keinen Treffer.

`[S]` D2 entspricht dem p3d17-Replay: 8 allgemeine Treffer, keine R8/R9-Treffer und kein neuer allgemeiner Treffer. G1 hat dieselben 13 allgemeinen Treffer. Die gemessenen Höhenhashes sind G1 `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` und D2 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`, identisch zu den Referenzhashes.

## 4. Regelzahlen vorher/nachher

`[S]` Vorher ist der p3d17-Replay im aktuellen Prüferschema (`pruefe_regeln` 600, einschließlich G11). Die historischen Ausgangssummen aus 9d3f8fc waren 596 ohne G11; historisch R8 48 (9/10/5/24) und R9 334 (25/34/275). Der aktuelle p3d17-Replay hat R8 46 (9/10/4/23) und R9 344 (23/34/287). Runde 1 ist die einzige p3d29-Nachhermessung.

### Allgemeine Regeln (pruefe_regeln)

| Regel | p3d17 Replay: gesamt (D1/G1/D2) | p3d29 Runde 1: gesamt (D1/G1/D2) | Δ gesamt |
|---|---:|---:|---:|
| `G11_objekt_schwebt_sinkt` | 4 (2/2/0) | 4 (2/2/0) | +0 |
| `G2_spitze_oben` | 3 (0/0/0) | 4 (1/0/0) | +1 |
| `G2_spitze_oben_fein` | 8 (0/0/0) | 8 (0/0/0) | +0 |
| `G3_spitze_unten` | 4 (1/0/0) | 3 (0/0/0) | -1 |
| `G3_spitze_unten_fein` | 2 (0/0/0) | 2 (0/0/0) | +0 |
| `G5_beule_klippe` | 69 (2/0/0) | 76 (7/0/0) | +7 |
| `G6_facette` | 219 (3/3/0) | 227 (11/3/0) | +8 |
| `G7_wand_glatte_flaeche` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| `G7b_wandkontur_feld` | 25 (1/0/0) | 25 (1/0/0) | +0 |
| `G7b_wandkontur_kantenschaerfe` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| `G7b_wandkontur_rauheit` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| `G8_fluss_nicht_bis_rand` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| `R1_blind` | 24 (2/1/0) | 24 (2/1/0) | +0 |
| `R2_getrennt` | 15 (1/0/1) | 15 (1/0/1) | +0 |
| `R3_laengs_m` | 35 (6/1/0) | 34 (5/1/0) | -1 |
| `R3_quer_pct` | 29 (17/0/0) | 19 (7/0/0) | -10 |
| `R3_woelb_m` | 31 (19/0/0) | 19 (7/0/0) | -12 |
| `R4_rand` | 1 (1/0/0) | 0 (0/0/0) | -1 |
| `R5_loch` | 25 (8/0/0) | 17 (0/0/0) | -8 |
| `R5_spitze` | 0 (0/0/0) | 3 (3/0/0) | +3 |
| `R6_wasser_schnee` | 4 (0/3/0) | 4 (0/3/0) | +0 |
| `T1_fleckrand` | 94 (0/3/7) | 94 (0/3/7) | +0 |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| `T3_streifen_ringe_bildpruefung_offen` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 (0/0/0) | 1 (0/0/0) | +0 |
| **Gesamt** | **600 (63/13/8)** | **586 (47/13/8)** | **-14** |

### R8-Regeln

| Regel | p3d17 Replay: gesamt (D1/G1/D2) | p3d29 Runde 1: gesamt (D1/G1/D2) | Δ gesamt |
|---|---:|---:|---:|
| `R8_gitter` | 10 (2/0/0) | 10 (2/0/0) | +0 |
| `R8_quer` | 4 (0/0/0) | 5 (1/0/0) | +1 |
| `R8_stufe` | 9 (2/0/0) | 9 (2/0/0) | +0 |
| `R8a_wegende` | 23 (3/0/0) | 20 (0/0/0) | -3 |
| **R8 Summe** | **46 (7/0/0)** | **44 (5/0/0)** | **-2** |

### R9-Regeln

| Regel | p3d17 Replay: gesamt (D1/G1/D2) | p3d29 Runde 1: gesamt (D1/G1/D2) | Δ gesamt |
|---|---:|---:|---:|
| `R8b_delle` | 23 (1/0/0) | 22 (0/0/0) | -1 |
| `R9_saegezahn` | 34 (1/1/0) | 34 (1/1/0) | +0 |
| `R9w_wellen` | 287 (27/12/0) | 291 (30/12/0) | +4 |
| **R9 Summe** | **344 (29/13/0)** | **347 (31/13/0)** | **+3** |

`[S]` Per-Regel-Vergleiche zeigen außer den gesondert genannten +5-Überschreitungen keine weitere allgemeine/R8/R9-Regel über p3d17 Replay +5. Die absoluten R5-Spitzen-, G6-D1-, G5- und R9w-Ziele sind unabhängig davon wie oben verfehlt.

## 5. Mesh-Gates und nicht ausgeführte Prüfungen

`[F]` Kein Meshbau: die Float32-Probe besteht nicht alle harten Ziele. `python3 gen_relief.py && python3 baue_html.py` wurde nicht ausgeführt. Daher wurden Mesh-Deltas gegen VAR0/p3d6/p3d8/p3d16/p3d17/p3d18, `pytest`, xvfb-Lochscan, `t42u`, LOD1-Dreieckzahl, Mesh-/Datenhashes und die neun geforderten Vorher/Nachher-Bildpaare nicht gemessen. Die fünf bekannten roten Bestandstests wurden nicht geändert oder ausgeführt. Das ist kein bestandenes Mesh-Gate; die 0-Grenze für t42u und lod1 < 1,3 Mio. Dreiecke sind in p3d29 nicht neu verifiziert.

## 6. Annahmen, Grenzen und offene Punkte

`[A]` Die p3d26-`surface_grid` ist als V3-Hilfsreliefhöhe an den festen D1-Gitterpunkten interpretiert. Die Flood-Seed-Maske umfasst Wegband, Kreuzung, Ausläufe und Rampenenden; der übrige Bereich übernimmt p3d17. `[R]` Der Soft-Abflusskandidat verletzt die harte Abflussbedingung deutlich und kann nicht als fertiges Relief freigegeben werden.

`[R]` Einziger offizieller Float32-Punkt ist Runde 1; Runde 2 ist vor der offiziellen Probe infeasible. D1/G1/D2-Zahlen in den Regel- und Kacheltabellen beziehen sich daher auf Runde 1 und sagen nichts über die infeasible Runde 2 aus. Es gibt keine Mesh-, Bild-, Delta- oder LOD-Aussage. Das Rund-2-LP-Gruppenfilter ist ein Relaxations- und Löschfilter, kein Zeilen-IIS; G5/Abfluss-Locations sind dafür nicht bestimmbar.

## Drei-Satz-Schluss

`[S]` Das p3d29-Modell mit 7,5-m-Ring und einmaligem Abfluss-L1-Fallback wurde gebaut und in einer offiziellen Float32-Probe gemessen. `[S]` Die Probe verfehlt R5-Spitze, G5, G6 und R9w; 20 frische Schnitte machen den Folgesolve mit G5/Abfluss-Restkonflikt infeasible. `[F]` Es wurde kein Mesh gebaut oder freigegeben, und alle davon abhängigen Mesh-Gates bleiben offen.
