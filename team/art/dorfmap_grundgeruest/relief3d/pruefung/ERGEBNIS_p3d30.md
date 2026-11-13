# Ergebnis p3d30

Stand 13.11.2026 · Worktree `/workspace/wt_dorfmap_p3d30` · Branch `art/dorfmap-p3d30` · Basis `origin/art/dorfmap-p3d29` @ `177989a` · Kosten 0 EUR.

Marker: `[S]` Solver-/Prüfer-/Hashmessung · `[R]` Modellbefund oder daraus abgeleitete Diagnose · `[A]` Annahme oder Grenze · `[F]` Freigabe-/Abbruchentscheidung.

## Ergebnis in Kürze

`[F]` Ziel nicht erreicht: Keine der beiden harten Drainagevarianten lieferte einen zulässigen Modellpunkt, und der einzige erlaubte Soft-Fallback erreichte das Zeitlimit ohne zulässigen Punkt. Es gab deshalb keine offizielle Float32-Probe und keinen Meshbau; alle p3d30-Prüfer-Nachherwerte und harten Zielwerte bleiben **nicht gemessen**.

`[R]` Der LP-Gruppenfilter lässt in beiden Varianten die Drainage als einzige notwendige Konfliktgruppe stehen. In der ersten Variante beträgt der größte relaxierte Abflusskanten-Schlupf 0,017688 m; in Variante 2 beträgt er 0,017709 m, jeweils an Kind `150,0|0,5` → Nachfolger `149,5|1,0`.

## 1. Modelländerung gegenüber p3d29

`[R]` Die p3d29-Konstruktion und Modellfamilien liegen als neue, getrennte Dateien unter `codex_jobs/tools/p3d30/`. Die V3-Wegführung, Ringbreite 7,5 m, Kern-/Ring-Lokalität, 22 Modellfamilien, R4-Ereignisschnitt-Mechanik, Klippenformbindung, Weghöhen, Schwellen und Referenzrelief blieben im Modellaufbau aus p3d29 übernommen. Es wurden keine Prüfer, Schwellen, Tests, Quellzellwerte, Overlay-, Referenz-, G1- oder D2-Dateien für p3d30 geändert.

`[R]` Im aktiven Gebiet (Kern plus Ring) gibt es 5.980 Rasterzellen: 2.802 Kernzellen und 3.178 Ringzellen. 402 aktive Randzellen sind Auslässe; die übrigen 5.578 Zellen geben je eine Einheit Abfluss ab und wählen genau einen gerichteten 8er-Nachfolger. Für jede Kandidatenkante gibt es eine Binärvariable `y` und eine Flussvariable `f`; `sum(y)=1` an jeder Nicht-Auslasszelle, die Höhenbedingung `h(Kind) >= h(Nachfolger) + eps` gilt nur auf der gewählten Kante. Die Flussbilanz mit Kapazität `N*y` zwingt alle gewählten Pfade zu einem Rand-Auslass und schließt Zyklen aus. `eps=1 mm` im Gelände und `eps=0` in den unveränderten Weg-, Kreuzungs-, Auslauf- und Rampenendbereichen.

`[R]` Innerhalb des 4,8-m-Wegbands oder der WEGA-Straßenmaske werden seitliche Querungen der Rampenachse aus dem Kandidatengraphen ausgeschlossen: erlaubt sind lokale Bewegungen entlang der Achse oder vom Weg weg. 6.938 mögliche Kanten wurden aus diesem Grund verworfen. 3.275 Zellen liegen in diesem Wegband. Alle 5.980 aktiven Zellen im ausgewählten Graphen können topologisch einen Auslass erreichen.

| Schaltwert `P3D30_DRAINAGE_VARIANT` | Kandidatenregel | gerichtete Kanten = Drainage-Binär- und Flussvariablen | Graphreichweite |
|---|---|---:|---|
| `1` (Standard) | alle aktiven 8er-Nachbarn, nach Weg-Richtungsfilter | 37.686 | 5.980/5.980 Zellen |
| `2` | zusätzlich p3d17-Nachbarhöhe höchstens eigene Höhe + 0,02 m; bei 56 lokalen Minima nur der geringste wegeinheitliche Anstieg; 364 zusätzliche Erreichbarkeits-Ausweichkanten | 22.240 | 5.980/5.980 Zellen |

`[R]` Variante 1 ist der vollständig lokale Graph und bleibt Standard. Variante 2 spart 41 % der Kanten, begrenzt die Kandidaten aber anhand der Referenzneigung; sie wurde als zweite und letzte erlaubte Variante geprüft. Beide blieben im aktiven Bereich unabhängig vom p3d29-Priority-Flood-Baum. Dieser Baum bleibt nur als Vergleichsinformation im Konstruktionsbeleg, nicht als festgelegte Nachfolgerwahl. Außerhalb des aktiven Bereichs bleibt die p3d29-Konstruktion und ihre Höhenbindung unverändert.

`[A]` Auslässe wurden an allen 402 Randzellen des aktiven Bereichs angesetzt; es wurden keine zusätzlichen inneren Senken an Wasserläufen oder p3d17-Senken angenommen. Die Straßen-Richtungsregel ist eine geometrische Kandidatenregel auf dem 0,5-m-Raster. Eine offizielle Wirkungsprüfung dieser Regel ist mangels Float32-Probe nicht erfolgt.

`[R]` Eine alternative lokale Senkenfreigabe nur um die sieben bekannten G5-Komponenten wurde verworfen: Im p3d29-Festbaum widersprechen 624 Wegbandkanten der oben festgelegten Richtungsregel; davon liegen 608 außerhalb der erlaubten ±1,5-m-Senkenfenster. Diese begrenzte Senkenvariante hätte die festgelegten Wegbandbedingungen nicht konsistent erfüllt.

## 2. Harte Machbarkeit, LP-Gruppenfilter und Soft-Fallback

Alle MILP-/LP-Solves liefen seriell mit einem Thread und maximal 600 s je Solve. Der Laufzeitnachweis unter `/workspace/codex_jobs/log_p3d30.txt` weist `gpt-6-luna`, reasoning effort `xhigh` aus; der dortige Zeitfenster-Nachweis reicht vom 13.11.2026 20:53:36 bis 23:06:35 CET (ca. 2 h 13 min Wandzeit).

| Rechnung | Drainagegraph | Variablen / Zeilen | Ergebnis |
|---|---|---:|---|
| Hart, alle Familien hart | V1, 37.686 Kanten | 95.347 / 173.134 | `[S]` infeasible, HiGHS Status 8 |
| LP-Gruppenfilter V1 | V1, Relaxation | siehe Einzelbelege | `[S]` einziger verbleibender Konflikt: `p3d30_drainage` |
| All-open LP V1 | V1, Relaxation | 95.347 / 173.134 vor Relaxationsvariablen | `[S]` optimal; Drainage-Maximalschlupf 0,017687724 m, Summe 0,124648396 m über 121 Kanten |
| Einziger Soft-Fallback | V1, Abflusskanten-Slack gewichtet 10.000/m | 133.033 / 210.820 | `[S]` 600-s-Zeitlimit, kein primal zulässiger Punkt; kein Schlupfwert aus einer Lösung vorhanden |
| Hart, alle Familien hart | V2, 22.240 Kanten | 64.455 / 142.242 | `[S]` infeasible, HiGHS Status 8 |
| LP-Gruppenfilter V2 | V2, Relaxation | siehe Einzelbelege | `[S]` im Löschfilter bleibt `p3d30_drainage`; `p3d29_locality` ist keine verbleibende Konfliktgruppe |
| All-open LP V2 | V2, Relaxation | 86.695 / 164.482 | `[S]` optimal; Drainage-Maximalschlupf 0,017709136 m, Summe 0,124681366 m über 121 Kanten; zusätzlich 0,063099245 m Lokalitätsschlupf in diesem All-open-Optimum |

`[S]` V1-All-open-Ort des Maximalschlupfs: Kind `(150.0, 0.5)` → Nachfolger `(149.5, 1.0)`, benötigtes `eps=0`, relaxierter Auswahlwert `y=0,998792`. V2-Ort: dieselbe Kante, benötigtes `eps=0`, `y=1`. Das sind LP-Relaxationsbefunde und keine ganzzahlige Abflusslösung. Der V2-Lokalitätsschlupf im All-open-Optimum ist nicht gleichbedeutend mit einer notwendigen Lokalitätskonfliktgruppe: Laut dem seriellen Löschfilter ist nur die Drainagegruppe notwendig.

`[S]` Der eine zulässige Soft-Fallback wurde auf V1 ausgeführt, nachdem der V1-Gruppenfilter nur Drainage als Ursache auswies. Er fand innerhalb 600 s keinen zulässigen Punkt. Für V2 wurde kein zweiter Soft-Fallback gestartet. Das LP-Gruppenfilter ist ein Relaxations-/Gruppenlöschverfahren und kein Zeilen-IIS oder ganzzahliges IIS.

## 3. Offizielle Float32-Probe und Regelzahlen

`[F]` Offizielle Float32-Probe: **0 von höchstens 4 Runden**. Es gab keinen zulässigen harten oder Soft-Fallback-Modellpunkt, aus dem ein Relief hätte exportiert werden können. Das Checker-in-the-loop wurde daher gemäß Abbruchbedingung nicht gestartet; `R00` enthält keine Ereignisschnitte. Es gibt keine gemessenen p3d30-Nachher-Treffer, Trefferorte, Float32-Werte oder D1/G1/D2-Probeergebnisse.

`[S]` Die Vorherwerte stammen aus dem p3d17-Replay mit G11 (600 Treffer) im aktuellen Prüferschema. Die historischen Werte bei `9d3f8fc` waren `pruefe_regeln=596` ohne G11, R8=48 und R9=334. Die Abweichungen zwischen historischem und p3d17-Replay-R8/R9-Schema sind beibehalten und nicht als p3d30-Änderung gewertet.

### Allgemeine `pruefe_regeln`-Zähler

| Regel | p3d17 gesamt (D1/G1/D2) | historisch `9d3f8fc` gesamt | p3d30 nachher | Δ zu p3d17 |
|---|---:|---:|---:|---:|
| `G11_objekt_schwebt_sinkt` | 4 (2/2/0) | — | nicht gemessen | n.g. |
| `G2_spitze_oben` | 3 (0/0/0) | 3 | nicht gemessen | n.g. |
| `G2_spitze_oben_fein` | 8 (0/0/0) | 8 | nicht gemessen | n.g. |
| `G3_spitze_unten` | 4 (1/0/0) | 4 | nicht gemessen | n.g. |
| `G3_spitze_unten_fein` | 2 (0/0/0) | 2 | nicht gemessen | n.g. |
| `G5_beule_klippe` | 69 (2/0/0) | 69 | nicht gemessen | n.g. |
| `G6_facette` | 219 (3/3/0) | 219 | nicht gemessen | n.g. |
| `G7_wand_glatte_flaeche` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| `G7b_wandkontur_feld` | 25 (1/0/0) | 25 | nicht gemessen | n.g. |
| `G7b_wandkontur_kantenschaerfe` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| `G7b_wandkontur_rauheit` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| `G8_fluss_nicht_bis_rand` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| `R1_blind` | 24 (2/1/0) | 24 | nicht gemessen | n.g. |
| `R2_getrennt` | 15 (1/0/1) | 15 | nicht gemessen | n.g. |
| `R3_laengs_m` | 35 (6/1/0) | 35 | nicht gemessen | n.g. |
| `R3_quer_pct` | 29 (17/0/0) | 29 | nicht gemessen | n.g. |
| `R3_woelb_m` | 31 (19/0/0) | 31 | nicht gemessen | n.g. |
| `R4_rand` | 1 (1/0/0) | 1 | nicht gemessen | n.g. |
| `R5_loch` | 25 (8/0/0) | 25 | nicht gemessen | n.g. |
| `R6_wasser_schnee` | 4 (0/3/0) | 4 | nicht gemessen | n.g. |
| `T1_fleckrand` | 94 (0/3/7) | 94 | nicht gemessen | n.g. |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| `T3_streifen_ringe_bildpruefung_offen` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 (0/0/0) | 1 | nicht gemessen | n.g. |
| **Gesamt** | **600 (63/13/8)** | **596** | **nicht gemessen** | **n.g.** |

### R8- und R9-Zähler

| R8-Regel | p3d17 gesamt (D1/G1/D2) | historisch `9d3f8fc` | p3d30 nachher | Δ |
|---|---:|---:|---:|---:|
| `R8_stufe` | 9 (2/0/0) | 9 | nicht gemessen | n.g. |
| `R8_gitter` | 10 (2/0/0) | 10 | nicht gemessen | n.g. |
| `R8_quer` | 4 (0/0/0) | 5 | nicht gemessen | n.g. |
| `R8a_wegende` | 23 (3/0/0) | 24 | nicht gemessen | n.g. |
| **R8 gesamt** | **46 (7/0/0)** | **48** | **nicht gemessen** | **n.g.** |

| R9-Regel | p3d17 gesamt (D1/G1/D2) | historisch `9d3f8fc` | p3d30 nachher | Δ |
|---|---:|---:|---:|---:|
| `R8b_delle` | 23 (1/0/0) | 25 | nicht gemessen | n.g. |
| `R9_saegezahn` | 34 (1/1/0) | 34 | nicht gemessen | n.g. |
| `R9w_wellen` | 287 (27/12/0) | 275 | nicht gemessen | n.g. |
| **R9 gesamt** | **344 (29/13/0)** | **334** | **nicht gemessen** | **n.g.** |

`[S]` Historische R8-Einzelwerte in der Reihenfolge `Stufe/Gitter/Quer/Wegende`: `9/10/5/24`; historische R9-Einzelwerte: `25/34/275`. Im p3d17-Replay lauten sie `9/10/4/23` und `23/34/287`.

### Kachelvergleich der verfügbaren Baseline

| Gebiet / Zähler | p3d17 D1 | p3d17 G1 | p3d17 D2 | p3d30 D1/G1/D2 |
|---|---:|---:|---:|---|
| Allgemeine Regeln | 63 | 13 | 8 | nicht gemessen / nicht gemessen / nicht gemessen |
| R8 | 7 | 0 | 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R9 | 29 | 13 | 0 | nicht gemessen / nicht gemessen / nicht gemessen |

`[F]` D2 hat in der Baseline null R8- und null R9-Treffer; die 8 allgemeinen D2-Treffer sind die Referenzwerte. Weil keine p3d30-Probe erzeugt wurde, lässt sich weder bestätigen noch widerlegen, ob ein D2-Treffer neu hinzugekommen wäre. Die D2-Regressionsbedingung ist damit **nicht neu nachgewiesen**.

### Harte Zielwerte – p3d30 nicht gemessen

| Ziel | p3d17 Referenz, soweit verfügbar | p3d30-Probe | Bewertung |
|---|---:|---:|---|
| R5-Spitzen D1 = 0 | 0 | n.g. | nicht verifiziert |
| G6 D1 ≤ 3 | 3 | n.g. | nicht verifiziert |
| R8b D1 ≤ 1 | 1 | n.g. | nicht verifiziert |
| G3 D1 ≤ 1 | 1 (fein zusätzlich 0) | n.g. | nicht verifiziert |
| R9w gesamt ≤ 280 | 287 | n.g. | nicht verifiziert |
| G5 gesamt ≤ 69 und D1 ≤ 2 | 69; D1=2 | n.g. | nicht verifiziert |
| R5-Loch gesamt ≤ 22 und D1 ≤ 5 | 25; D1=8 | n.g. | nicht verifiziert |
| D1-R4-Schlucht = 0 | 0 | n.g. | nicht verifiziert |
| R3 D1 längs/quer/Wölbung ≤ 6/7/7 | 6/17/19 | n.g. | nicht verifiziert |
| Kreuzung `152,5|28,5`: Stufe ≤ 0,116 m; Gitter ≤ 0,020 m; Quer ≤ 3 %, Einzelquer ≤ 20 % | kein p3d30-Messwert | n.g. | nicht verifiziert |
| Wegenden-Stufe ≤ 0,054 m | kein p3d30-Messwert | n.g. | nicht verifiziert |
| R8a ≤ 0,10 m; Ausnahme rampe_2-Start `126,51|31,62` ≤ 0,18 m | kein p3d30-Messwert | n.g. | nicht verifiziert |
| Alle Regeln höchstens +5 gegen p3d17-Replay | Baseline siehe Tabellen | n.g. | nicht verifiziert |
| D2: keine neuen allgemeinen Treffer, R8/R9 bleiben 0 | 8 allgemein, R8=0, R9=0 | n.g. | nicht verifiziert |

## 4. Mesh-Gates, Hashes und Prüfer-Diff

`[F]` Kein Float32-Proberelief erfüllte die Voraussetzung für den Meshbau. Deshalb wurden `python3 gen_relief.py`, `python3 baue_html.py`, `delta.py` gegen VAR0/p3d6/p3d8/p3d16/p3d17/p3d18, `pytest`, xvfb-Lochscan, `t42u`, Klippenmessung bei `140|35`, LOD1-Zählung und die geforderten Vorher-/Nachher-Bilder nicht ausgeführt. Es wurde kein p3d30-Mesh erstellt; kein Mesh-Gate gilt als bestanden. Die fünf bekannten roten Bestandstests blieben unberührt und wurden nicht ausgeführt.

`[S]` Quell- und Referenzhashes selbst neu berechnet:

| Datei / Feld | SHA-256 |
|---|---|
| `neu/zellen_relief.csv` | `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa` |
| `neu/vektor.json` | `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e` |
| `neu/felder.json` | `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435` |
| G1-Referenzhöhe | `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` |
| D2-Referenzhöhe | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` |
| Quellrelief `/tmp/p3d22_v3_source.json.gz` | `b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6` |
| Transferbasis `p3d21_transfer_base_route3_v29.json` | `07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287` |

`[S]` Der Prüfer-/Test-Diff gegen `89c61ce` enthält ausschließlich die freigegebenen Bestandsunterschiede `pruefung/r8_kreuzung.py`, `pruefung/r8a_policy.py` und `pruefung/test_r8a_policy_p3d26.py`; keine dieser Dateien wurde für p3d30 geändert. Die übrigen p3d30 Änderungen liegen in den neuen Tools, Solverbelegen und diesem Ergebnisbericht.

## 5. Annahmen, Grenzen und offene Punkte

`[A]` Die Randzellen des aktiven Kern-/Ringgebiets werden als zulässige natürliche Auslässe behandelt. Das Modell weist eine Netzwerktopologie zu Rand-Auslässen nach, aber ohne ganzzahligen Höhenpunkt weder eine tatsächliche Fließlinie noch eine schadlose Verbindung zu einem Gewässer.

`[R]` Der LP-Maximalschlupf zeigt einen konkreten Konflikt zwischen mindestens einer ausgewählten lokalen Drainagekante und den übrigen harten Modellbedingungen. Wegen der relaxierten Binärwahl und fehlendem zulässigem Soft-Fallback lässt sich daraus keine eindeutige einzelne Höhen- oder Checkerursache ableiten. Die offiziellen Ereignisprüfer haben keine p3d30-Kandidaten bewertet; daher gibt es keine verlässliche Liste verbleibender G5-, R5-Loch-, R8b-, G6-, R5-Spitzen- oder G11-Treffer samt Orten.

`[A]` Für Variante 2 wurden bei 56 lokalen Referenzminima jeweils nur die geringste aufwärts gerichtete, wegeinheitliche Kante behalten und für 364 weitere Kanten reine Erreichbarkeits-Ausnahmen ergänzt. Das erhält Graphreichweite, lockert aber die strikte Bedingung `h(nachbar) ≤ h(eigene)+0,02 m` an diesen dokumentierten Ausnahmen; keine der beiden Varianten ist ein vollständig ausnahmsloser Referenzgefällegraph.

`[F]` Es wurden keine Kosten verursacht und keine Nachrichten versendet. Zellquellwerte, Overlay, Referenzen und Prüfer/Schwellen blieben unangetastet; kein Ergebnis für D2 wurde durch eine p3d30-Höhenänderung erzeugt. `t42u=0` und `LOD1 < 1,3 Mio.` wurden mangels Mesh nicht neu gemessen.

## Anforderungen 1–7: Selbstprüfung

| Nr. | Selbstprüfung |
|---:|---|
| 1 | `[R]` p3d29-Aufbau, Lokalität, Ring, V3-Wegführung, Familien, Klippenform und R4-Schnittmechanik als getrennte p3d30-Modellkopie übernommen; keine Probe, daher kein offizieller Ergebnisnachweis. |
| 2 | `[S]` Lokale Nachfolgerwahl, Höhenkopplung, Einheitszufluss und Flusskopplung implementiert; V1/V2 mit Kanten- und Variablenzahlen dokumentiert. |
| 3 | `[S]` Harte MIP-Versuche infeasible; LP-Gruppenfilter isoliert Drainage; genau ein Soft-Fallback bis zum 600-s-Limit, ohne zulässigen Punkt. |
| 4 | `[F]` Checker-in-the-loop nicht gestartet: 0/4 Runden, weil kein zulässiger Reliefpunkt vorlag. |
| 5 | `[F]` Sämtliche harten Ziele bleiben unbestätigt; kein Grenzwert wurde gelockert. |
| 6 | `[F]` Meshbau und Mesh-Gates nicht gestartet, weil keine Float32-Probe alle Ziele belegen konnte. |
| 7 | `[F]` Abbruch mit ehrlichem Nicht-Ergebnis; keine verbleibenden offiziellen Treffer behauptet, da ohne Probe nicht gemessen. |

## Drei-Satz-Schluss

`[F]` p3d30 hat den p3d29-Abfluss lokal umleitbar formuliert, aber keine der zwei getesteten harten Graphvarianten war machbar. `[S]` Der LP-Gruppenfilter weist in beiden Fällen auf die Drainageformulierung; der einzige hoch gewichtete Drainage-Soft-Fallback endete am 600-s-Limit ohne zulässigen Punkt. `[F]` Daher gibt es keine offizielle Float32-Probe, keinen bestätigten Zielerfolg und keinen p3d30-Meshbau.
