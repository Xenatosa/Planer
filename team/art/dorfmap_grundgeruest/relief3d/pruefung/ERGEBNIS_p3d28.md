# Ergebnis p3d28

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d28` · Branch `art/dorfmap-p3d28` · Basis `origin/art/dorfmap-p3d27` @ `0dfd939` · Kosten **0 EUR**.

Marker: `[S]` gemessen oder unverändert ausgeführter Prüfer · `[R]` Modellbefund/abgeleitete Diagnose · `[A]` Annahme · `[F]` Freigabe.

## 1. Diagnose der p3d27-Runden 1 und 6

`[S]` Die p3d17-D1-Referenz wurde zunächst aus dem archivierten Float32-Relief `/tmp/relief_p3d27_r3_reference_after.json.gz` ausgelesen. Zusätzlich reproduziert das p3d28-Modell sie aus dem unveränderten Basisrelief und `p3d17_joint_mesh_v22.json`; der SHA-256 ist erneut `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`. Die zwei offiziellen p3d27-Probereliefs wurden direkt aus ihren `GB`-Float32-Rastern verglichen; der D1-Ausschnitt hat 7.395 Punkte bei 0,5 Karten-Einheiten Abstand.

| Runde | mittlere absolute Abweichung | P95 `|Δh|` | Maximum `|Δh|` | Punkte `>1 mm` | Punkte `>1 cm` | Punkte `>10 cm` |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2,269 m | 4,687 m | 7,014 m | 4.923 | 4.899 | 4.771 |
| 6 | 2,285 m | 4,719 m | 7,014 m | 4.922 | 4.906 | 4.784 |

`[S]` Runde 1: R5-Loch 104, G5-Beule 78, R4-Schlucht 5 und R8b-Delle 11. Runde 6: R5-Loch 169, G5-Beule 34, R4-Schlucht 7 und R8b-Delle 5. Alle jeweiligen Treffer liegen auf D1-Gitterpunkten, deren nächste 0,5er-Meshhöhe mehr als 1 cm von p3d17 abweicht. In Runde 6 liegen die R5-Punkte über `x=127,0..167,5`, `z=2,0..42,5`; ihre mediane absolute Abweichung ist 4,000 m (Spannweite −5,323 bis −2,024 m). G5 liegt über `x=131,0..162,5`, `z=2,0..39,0`; mediane Abweichung +4,081 m (Spannweite +3,832 bis +5,932 m). R4 liegt über `x=128,0..156,2`, `z=2,5..31,4`; mediane absolute Abweichung 0,755 m. Die R5-/G5-Treffer liegen damit überwiegend auf großflächig veränderten Zellen und nicht nur im unmittelbaren Weg-/Kreuzungsband.

`[R]` Der p3d27-Solve lief mit `objective_mode=diagnostic`. Bei Familienschlupf 0 wird darin keine Bewegung zur p3d17-Höhenfläche minimiert; der sekundäre L1-Tie-Break wird in diesem Modus übersprungen. Das Feld hat 7.395 freie D1-Meshhöhen. `variable_bounds` begrenzt abgedeckte Höhen nur auf ±4 m gegenüber dem Quellfeld; die 22 Familien sichern lokale Weg-/Kreuzungsbeziehungen, pinnen die übrige D1-Fläche aber nicht an p3d17. Das erklärt, warum zusätzliche Ereignisschnitte die weit verteilten R5-/G5-Ereignisse nicht stabil beseitigten.

`[S]` Karte, Float32-Differenzraster und Trefferkoordinaten: [`p3d28_d1_delta_comparison.svg`](../../../../../codex_jobs/tools/p3d28/results/p3d28_d1_delta_comparison.svg), [`p3d28_diagnose_d1.json`](../../../../../codex_jobs/tools/p3d28/results/p3d28_diagnose_d1.json).

## 2. Konstruktionsmodell

`[R]` Das Modell ergänzt die unveränderten 22 Modellfamilien um harte lineare Lokalitäts-, Priority-Flood-Abfluss-, Klippenform-, R4-Querschnitts- und Baumfußbedingungen. Prüfer, Prüfschwellen, Quellzellwerte, Overlay und Wegführung blieben unverändert. Es gibt keine p3d19-Pinning-Surrogate und keine R9w-Gleichheitsfixierung; das p3d17-Zielfeld kommt nur beim sekundären L1-Tie-Break nach dem Schlupfziel vor.

`[S]` Arbeitskern: Vereinigung aus 4,5-m-Rampenband (p3d23-Paarfamilienradius), 4-Karteneinheiten-Kreis um das ungerundete V3-D1-Kreuzungszentrum, expliziten Auslaufstreifen und den exakten Stützpunkten des unveränderten `RELIEF_WEGEND_VAR=1`-Endauslaufs. Der Übergangsring klingt linear von 20 mm zulässiger Abweichung am Innenrand auf 1 mm am Außenrand ab; außerhalb gilt höchstens 1 mm Abweichung von p3d17. Die drei schaltbaren Ringbreiten sind 4,5/6,0/7,5 m (`P3D28_CONSTRUCTION_VARIANT=1/2/3`).

`[S]` Bei 4,5 m: 2.802 Kern-, 2.087 Ring- und 4.889 aktive Rasterpunkte; 2.506 außen. Der unveränderte Transfer umfasst 4.924 Stützpunkte, davon 632 außerhalb des Arbeitsbereichs. Bei 6,0 m sind 2.802 Kern-, 2.721 Ring- und 5.523 aktive Punkte; 1.872 außen. Bei 7,5 m sind es 2.802 Kern-, 3.178 Ring- und 5.980 aktive Punkte; 1.415 außen; kein Transferstützpunkt liegt mehr außerhalb der aktiven Fläche. Diese Lokalitätsgrenze ist eine Arbeitsbereichsgrenze, keine R9w-Fixierung.

`[R]` Priority-Flood auf p3d17 bestimmt deterministisch einen 8-Nachbar-Abflussbaum mit Auslässen am Rand des Arbeitsbereichs. Die Rampenachsen werden zum tieferen p3d17-Ende und von dort bis zum Arbeitsbereichsrand geführt. Baumkanten fordern `h[Zelle] >= h[Nachfolger] + eps`; `eps=1 mm`, auf Straße, im 1,81-m-Wegband und im 4-Karteneinheiten-Kreuzungsbereich `eps=0`.

`[R]` Im Wand-/Klippenbereich (Referenzgradient über 1 m/m, Abstand höchstens 6 m, außerdem 4,8 m um Wegachsen) werden zweite Differenzen in vier Rasterrichtungen auf ±0,02 m um p3d17 begrenzt. Lineare Querschnitte begrenzen den R4-Schluchtindikator auf 1,499 m. Baumstandorte/Objekte bleiben unverändert; Bodenstichproben 3×3 am Baum werden auf 1 mm zur Referenz begrenzt.

`[A]` Standard ist Ring 7,5 m: Diese Stufe hat im linearen Relaxations-Minimalschlupf den kleinsten gewichteten Zielfunktionswert der drei Breiten. Sie ist trotzdem kein machbarer Kandidat; alle drei harten Varianten sind unlösbar. 4,5 m und 6,0 m bleiben über die Umgebungsvariable schaltbar.

## 3. Machbarkeit, Minimalschlupf und Float32-Probe

`[S]` Nach dem Korrigieren der bilinearen Rasterzeilenbegrenzung (Z-Index musste auf Rasterhöhe statt -breite begrenzt werden) wurden alle drei erlaubten harten MILP-Varianten neu gelöst. Jede Ringverbreiterung folgte auf die bewiesene Unzulässigkeit der vorigen Stufe. Die HiGHS-Solves liefen seriell mit einem Thread und höchstens 600 s je Solve; HiGHS meldete jeweils bewiesene Unzulässigkeit (Status 8). Die veraltete erste Runde vor dieser Korrektur wird nicht als gültige Machbarkeitsprobe gezählt.

| Stufe | Ring | harter Solve | zusätzliche Konstruktionszeilen | Float32-Checker-Runden |
|---:|---:|---|---:|---:|
| 1 | 4,5 m | Infeasible, bewiesen | 48.870 | 0 |
| 2 | 6,0 m | Infeasible, bewiesen | 52.809 | 0 |
| 3 | 7,5 m | Infeasible, bewiesen | 55.189 | 0 |

`[S]` Für die Diagnose wurden zusätzlich LP-Relaxationen des Integrality-Modells mit allen 26 Schlupfgruppen minimiert. Sie sind **keine** offiziellen Float32-Kandidaten. Ihre gewichteten L1-Minima und positiven Gruppen-Schlupfe waren:

| Schlupfgruppe | Einheit | Ring 4,5 m | Ring 6,0 m | Ring 7,5 m |
|---|---|---:|---:|---:|
| `grade_same` | m | 0,190625 | 0,189519 | 0,188856 |
| `p3d28_cliff_form` | m | 1,512650 | 1,513243 | 1,513599 |
| `p3d28_drainage` | m | 0,008984 | 0,008984 | 0,008984 |
| `p3d28_locality` | m | 0,118654 | 0,116757 | 0,115619 |
| `route_profile_slope` | m | 0,391928 | 0,391403 | 0,391087 |
| `safety_single_quer` | Prozentpunkte | 56,849256 | 56,771997 | 56,725642 |
| `source_monotone` | m | 0,070250 | 0,070245 | 0,070242 |
| `variable_bounds` | m | 0,593959 | 0,593846 | 0,593778 |
| gewichtetes L1-Minimum | normierte Zielfunktion | 95,205764 | 95,133143 | 95,089571 |

`[R]` Ein serieller gruppenweiser Löschfilter der 7,5-m-LP-Relaxation lässt nur `p3d28_cliff_form` und `p3d28_drainage` als notwendige Schlupfgruppen übrig. Mit ausschließlich diesen beiden Gruppen weich ist die Relaxation zulässig (gewichtetes Minimum 207,322043); die jeweils einzeln hart gesetzte Gruppe bleibt bei Lockerung der anderen getesteten Kandidatenfamilien infeasible. Das ist ein irreduzibler gruppenweiser Konfliktbefund **für die lineare Relaxation**, kein exakter Zeilen-IIS und kein Integer-IIS.

`[S]` Im auf diese zwei Gruppen beschränkten LP-Minimalschlupf beträgt der Formschlupf 1,793205 m und der Abflussschlupf 0,117662 m. Größter Formkonflikt: Stencilzentrum `151,5|34,0`; dort weicht die zweite Differenz −1,701742 m von der Referenzdifferenz +0,111463 m ab. Der gleiche Formschlupf tritt in einem R4-Referenzquerschnitt bei Zentrum `134,4529|30,6662`, Seite `134,8801|34,6433` auf. Größter Abflusskonflikt: Kante Kind `150,0|13,0` → Nachfolger `150,0|13,5` (dort ist `eps=0`). Der separate ganzzahlige Minimalschlupflauf auf Ring 4,5 m erreichte die 600-s-Grenze ohne primal zulässigen Punkt.

`[S]` **Offizielle Float32-Probe: 0 Runden**, weil kein harter Modellpunkt existiert. `pruefe_regeln`, `r8_kreuzung.py` und `r9_form.py` wurden für p3d28 daher nicht auf einem neuen Relief ausgeführt. Es gibt keine p3d28-Nachher-Regelzahlen und keine D1/G1/D2-Probeergebnisse; die nachstehende Baseline ist ausdrücklich kein p3d28-Ergebnis.

### Regelzahlen vorher/nachher

`[S]` Vorherwerte stammen aus dem p3d17-Replay mit G11 und dem unveränderten p3d27-Baseline-Artefakt. Nachherwerte sind nicht erhoben, da keine offizielle Probe lief.

| `pruefe_regeln`-Regel | p3d17 vorher | p3d28 nachher |
|---|---:|---|
| `G11_objekt_schwebt_sinkt` | 4 | nicht erhoben |
| `G2_spitze_oben` | 3 | nicht erhoben |
| `G2_spitze_oben_fein` | 8 | nicht erhoben |
| `G3_spitze_unten` | 4 | nicht erhoben |
| `G3_spitze_unten_fein` | 2 | nicht erhoben |
| `G5_beule_klippe` | 69 | nicht erhoben |
| `G6_facette` | 219 | nicht erhoben |
| `G7_wand_glatte_flaeche` | 1 | nicht erhoben |
| `G7b_wandkontur_feld` | 25 | nicht erhoben |
| `G7b_wandkontur_kantenschaerfe` | 1 | nicht erhoben |
| `G7b_wandkontur_rauheit` | 1 | nicht erhoben |
| `G8_fluss_nicht_bis_rand` | 1 | nicht erhoben |
| `R1_blind` | 24 | nicht erhoben |
| `R2_getrennt` | 15 | nicht erhoben |
| `R3_laengs_m` | 35 | nicht erhoben |
| `R3_quer_pct` | 29 | nicht erhoben |
| `R3_woelb_m` | 31 | nicht erhoben |
| `R4_rand` | 1 | nicht erhoben |
| `R5_loch` | 25 | nicht erhoben |
| `R6_wasser_schnee` | 4 | nicht erhoben |
| `T1_fleckrand` | 94 | nicht erhoben |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | nicht erhoben |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | nicht erhoben |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | nicht erhoben |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | nicht erhoben |
| Summe `pruefe_regeln` historischer Stand 9d3f8fc | 596 | nicht erhoben |
| Summe p3d17-Replay mit G11 | 600 | nicht erhoben |

| R8-Regel | vorher | nachher |
|---|---:|---|
| `R8_gitter` | 10 | nicht erhoben |
| `R8_quer` | 5 | nicht erhoben |
| `R8_stufe` | 9 | nicht erhoben |
| `R8a_wegende` | 24 | nicht erhoben |
| **R8 gesamt** | **48** | **nicht erhoben** |

| R9-Regel | vorher | nachher |
|---|---:|---|
| `R8b_delle` | 25 | nicht erhoben |
| `R9_saegezahn` | 34 | nicht erhoben |
| `R9w_wellen` | 275 | nicht erhoben |
| **R9 gesamt** | **334** | **nicht erhoben** |

### D1/G1/D2 nach Kachel

`[S]` Die p3d17-Allgemeinregel-Baseline enthält 63 Treffer in D1, 13 in G1 und 8 in D2. Mangels p3d28-Proberelief sind die Nachherzahlen für alle drei Kacheln nicht erhoben; daraus folgt **keine** Aussage, dass D2-Gates bestanden wären. R8-/R9-Gesamtbaselines stehen in den obigen Tabellen; ein p3d28-Kachelvergleich ist nicht vorhanden.

| Kachel | p3d17 Allgemeinregeln vorher | p3d28 allgemein nachher | p3d28 R8 nachher | p3d28 R9 nachher |
|---|---:|---:|---:|---:|
| D1 | 63 | nicht erhoben | nicht erhoben | nicht erhoben |
| G1 | 13 | nicht erhoben | nicht erhoben | nicht erhoben |
| D2 | 8 | nicht erhoben | nicht erhoben | nicht erhoben |

Die Detailcounts und der Abbruchgrund sind in [`p3d28_gate_baseline_and_not_run.json`](../../../../../codex_jobs/tools/p3d28/results/p3d28_gate_baseline_and_not_run.json) dokumentiert.

## 4. Mesh-Gates, Annahmen und offene Punkte

`[S]` Kein Mesh gebaut. Daher nicht ausgeführt: `gen_relief.py`, `baue_html.py`, direkter Float32-Transfer, `delta.py` gegen VAR0/p3d6/p3d8/p3d16/p3d17/p3d18, pytest, xvfb-Lochscan, t42u-Summe, Klippe `140|35`, LOD1-Dreieckszahl, Hashvergleich und geforderte Vorher/Nachher-Bilder. Keine Bilddateien erzeugt.

`[A]` Die Arbeitsbereichsbreite leitet sich aus den p3d23-Familien ab: 4,5 m Rampen-Paarfamilie, 4 Karteneinheiten Kreuzung, 1 m Längs- plus 4 m Auslauf und 2,5 m Querband; der Ring wurde nur in den erlaubten zwei Schritten erweitert. Für das Standardprofil wurde das kleinere gewichtete LP-Minimalschlupfziel als Auswahlkriterium verwendet.

`[R]` Offen ist ein Konstruktionsmodell, das die Klippen-/R4-Referenzform und den Abflussbaum gleichzeitig mit den unveränderten Weg-/Kreuzungsfamilien hart erfüllt. Ein konkreter Grund der Konflikte ist der im Ergebnis ausgewiesene Formstencil-/R4-Querschnitt nahe `151,5|34,0` beziehungsweise `134,4529|30,6662` und die Abflusskante `150|13 → 150|13,5`. Ohne zulässigen Höhenpunkt sind Float32-Checker-in-the-loop, Regelziele und Mesh-Gates unentschieden.

## 5. Schluss

Das neue lineare Senken-Konstruktionsmodell wurde mit drei Arbeitsringbreiten geprüft; alle drei harten Varianten sind unzulässig, daher gab es keine offizielle Float32-Proberunde und keinen Mesh-Bau. Die LP-Diagnose grenzt den irreduziblen Gruppen-Schlupf auf Klippenform und Abflussbaum ein und lokalisiert beide Konflikte. D1-Zielwerte, D2-Regressionsfreiheit, LOD1 und Mesh-Hashes sind für p3d28 nicht nachgewiesen; Bericht und JSON-Belege sind im Branch `art/dorfmap-p3d28` festgehalten.
