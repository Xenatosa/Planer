# ERGEBNIS_p3d37

Stand 2026-11-15 · Worktree `/workspace/wt_dorfmap_p3d37` · Branch `art/dorfmap-p3d37` · Basis `origin/art/dorfmap-p3d36 @ eb2cd86` · Kosten 0 EUR.

Laufzeitnachweis: `/workspace/codex_jobs/log_p3d37.txt` (`gpt-6-luna`, `xhigh`). Marker: [S] gemessen · [R] Code-/Modellbefund · [A] Annahme/Grenze · [F] Entscheidung.

## Ergebnis

[F] **STOPP ohne Konstruktion und ohne Mesh.** Die verlangte 58,527-mm-Stufe am rampe_11-Start ist im p3d36-All-Familien-Optimum vorhanden, aber die Gegenproben zeigen, dass sie nicht durch eine einzelne Nachbarzeile oder einzelne Modellfamilie erzwungen wird. Ein exakter diagnostischer Lock auf 54 mm ist mit allen Familien elastisch erfüllbar; der harte Gesamt-LP ist separat an einem festen Paar außerhalb des D1-Fensters infeasible. Eine eindeutige, sichere Einzelersetzung, die zugleich den Zielkonflikt erklärt, ist damit nicht belegt; keine Schwelle wurde geändert.

[S] Hinzugefügt wurden ausschließlich Diagnose-/LP-Werkzeuge und kompakte Belege unter `codex_jobs/tools/p3d37/` sowie dieser Bericht. `P3D37_POLICY=official` und `P3D37_POLICY=p3d36` reproduzieren derzeit beide p3d36, weil keine Regel ersetzt wurde. Zellquellen, Overlay, Prüfer, `relief_o18n.py`, `../referenz/*`, Rampenführung und Relief/Mesh-Ausgaben blieben unangetastet.

## 1. Startbanddiagnose

### Lauf und Nachbarzeilen

[S] Der harte LP-IIS-Lauf nutzte HiGHS 1.15.1, eine kontinuierliche LP mit 20.413 Variablen, 75.287 Zeilen und null Integer-Variablen, einen Thread und `iis_strategy=6`. Das Zeitlimit war 840 s (höchstens 15 min); HiGHS lieferte ein gültiges IIS in 0,114 s. Die vollständige kompakte Belegdatei ist `codex_jobs/tools/p3d37/results/p3d37_startband_iis.json`.

[S] Im elastischen All-Familien-Lauf war `endpoint_stage_extra_m=0,00462663517 m` der einzige positive Schlupf; darin sind 0,0001 m Float32-Wache enthalten. Das LP meldet am Zielpaar [147,5|5,0]–[147,5|5,25] 0,058526635 m statt höchstens 0,054 m, also 0,004526635 m tatsächliche Überschreitung. Nach Float32-Export wurden 12,500476837 m und 12,441950321 m gemessen, Differenz 0,058526516 m.

| z bei x=147,5 | p3d17-Höhe (m) | All-Familien-Optimum Float32 (m) | Ziel-Lock, übrige Familien elastisch (m) |
|---:|---:|---:|---:|
| 4,50 | 12,150277 | 12,591752 | 12,593180 |
| 4,75 | 12,174459 | 12,546114 | 12,550731 |
| 5,00 | 12,198642 | 12,500477 | 12,508282 |
| 5,25 | 12,419736 | 12,441950 | 12,454382 |
| 5,50 | 12,640830 | 12,383424 | 12,400482 |
| 5,75 | 12,599821 | 12,324897 | 12,341955 |
| 6,00 | 12,558812 | 12,266371 | 12,283428 |

[R] Das Zielpaar ist im LP als Viertelzellen-Prüferzeile enthalten. Es wird auf dem 0,5-m-Raster über die beiden Nachbarvariablen `surface_x_147.500_z_5.000` und `surface_x_147.500_z_5.500` linear ausgewertet: je 0,5 Koeffizient, Zeilen 63910/63914 in der All-Familien-Zeilenprüfung. Beide Richtungen sind im elastischen Optimum bis auf numerisches Rauschen an der LP-Grenze 0,0539 m aktiv; ihre Dualwerte sind 0. Das heißt: die gemeinsame Endpunkt-Schlupfvariable erlaubt die Überschreitung, sie belegt keine zwingende lokale Höhe von 58,527 mm.

[S] Der lokale Zeilenauditpunkt [147,5|5,125], Radius 1,5 m, fand 160 aktive/enge lokale Zeilen: 115 Klippenform-Krümmung, 24 R3 längs, 9 R3 quer, 4 Endpunktstufe, 3 Querfall, 3 Achsstütze und 2 Variablengrenzen. Die Zeilen sind im Ergebnis-JSON aufgelistet; alle ausgewiesenen Dualwerte waren 0. Das ist wegen Degeneration kein belastbarer Einzelursachennachweis.

### IIS, Gegenproben und Prüfervergleich

| Lauf | Status/Schlupf | Ort und beteiligte Zeile(n) | Aussage |
|---|---|---|---|
| Harte Gesamt-LP, IIS 6 | Infeasible; gültiges IIS aus 1 Zeile/1 Spalte | Zeile 65382 `endpoint_stage_pairs`, Paar [171,25|24,75]–[171,5|24,75], nahe `rampe_2_ende` [175,085573|25,697639], Mittelpunktabstand 4,595604 m. Die Zeile hat keine veränderliche Höhen-Spalte; allein `endpoint_stage_extra_m` wäre nötig, dessen obere Grenze im harten LP 0 ist. | Festes Außenpaar in Kachel E1, x>168 und damit außerhalb des D1-Modellfensters. Implizite feste Stufe 0,056967497 m; erforderlich wären 0,003067497 m modellierter Schlupf einschließlich Float32-Wache, entsprechend 0,002967497 m über der unveränderten 0,054-m-Grenze. Es ist nicht das rampe_11-Zielpaar. |
| All-Familien-Filter | Optimal; Schlupf 0,004626635 m | Maximum am rampe_11-Paar [147,5|5,0]–[147,5|5,25] | Float32-Stufe 0,058526516 m. |
| Exakter Ziel-Lock, alle Familien elastisch | Optimal; Schlupf bleibt 0,004626635 m | Zielpaar hart bei 0,0539 m; maximaler Restschlupf wandert zum Paar [153,25|35,5]–[153,5|35,5] | Float32-Zielstufe 0,053899765 m. Damit ist die 58,527-mm-Stufe am Ziel nicht unvermeidbar. |
| Ziel-Lock, jeweils eine andere Modellfamilie hart | 28/28 Läufe optimal, je Solve höchstens 6,3 s | R3 längs/quer/Wölbung, R8a, R3-/Plattform-/Achsen-/Variablen-/Profil-/Lokalitäts-/Klippen-/Drainage-/Event- und Querfallfamilien einzeln festgehalten | Zielstufen 0,049504757–0,053900242 m. Keine einzelne getestete Familie verhindert für sich den Ziel-Lock, wenn die übrigen elastisch sind. |
| Einzel-Familienfilter mit harter 54-mm-Endpunktgrenze | Insgesamt 49 Filter-/Lockläufe: 31 Optimal, 18 Infeasible | Einzelne Kandidatenfamilien und lokaler Zeilenaudit | Der kompakte JSON-Beleg enthält Status, Schlupf, Ort, Profilfenster und Zeilenbelege je Lauf. |

[R] Die harte IIS-Zeile liegt in der 4-Mapeinheiten-Endpunktkulisse des LP, aber ihr Mittelpunkt ist 4,596 m vom Endpunkt entfernt. Der offizielle R8-Prüfer bildet Rampencluster und meldet Stufen erst über 0,20 m; für das IIS-Paar ist die feste 56,967-mm-Stufe darunter. Die offizielle R8a-Maske in `r8_kreuzung.py` verlangt `lo` zwischen −1 und +4 sowie `|quer|≤2,5`; für dieses Paar ist `lo=−3,571`, daher gehört es nicht zum R8a-Auslauf. Auch das Zielpaar liegt außerhalb des R8a-Auslaufs (`lo=−2,787`), obwohl es nahe einem R8-Rampencluster liegt. Die offizielle R8a-Schwelle beträgt 0,10 m, die einzige Ausnahme bleibt 0,18 m für `rampe_2_anfang` bei [126,51|31,62] mit Toleranz 1e−5.

| Zeile | Modellformulierung | Offizielle Prüferdefinition | Urteil und Behandlung |
|---|---|---|---|
| Zielpaar [147,5|5,0]–[147,5|5,25] | Viertelzellen-Stufenzeile, 0,0539 m LP-Cap inklusive 0,1-mm-Wache; im All-Familien-Lauf gemeinsame Endpunkt-Schlupfvariable | `r8_kreuzung.py`: R8-Stufe >0,20 m; R8a nur innerhalb der offiziellen Auslaufmaske (0,10 m, einmal 0,18 m) | 54 mm ist hier ein ausdrücklich verlangtes Projektziel und bleibt unverändert. Der Prüfer selbst ist nicht bindend. Kein einzelner anderer Zeilentyp erzwingt die Überschreitung; keine Ersetzung. |
| IIS-Paar nahe `rampe_2_ende` | Feste Außenwerte plus dieselbe 0,0539-m-Endpunktzeile; Paarstufe 0,056967497 m | `r8_kreuzung.py`: R8-Stufe >0,20 m; R8a-Auslaufmaske schließt den Punkt aus | Die starre Außenhöhe ist stärker als die lokale R8-Stufenregel. Eine lokale Außenöffnung wäre eine eigene Ausnahme außerhalb des D1-Fensters und erklärt die rampe_11-Zielstufe nicht; sie wurde nicht vorgenommen. Die 0,054-m-Grenze wurde nicht gelockert. |
| Enge lokale R3-Zeilen am Ziel | LP-Grenzen mit 0,0001-m Float32-Wache | `pruefe_regeln.py`: R3 längs ≤0,08 m, quer ≤3,5 %, Wölbung ≤0,08 m; Prüfsektionen mit 16 Viertelzellen-Samples | Modellgrenzen 0,0799 m/3,49 %/0,0799 m sind die beabsichtigte Wache und entsprechen den offiziellen R3-Operatoren. Einzelnes Hartlassen einer R3-Familie verhindert den Ziel-Lock nicht. |
| Profil-/Fenstergrenze rampe_11 | Variabel 0–90 m; physischer Weg 57,0 m, 191/191 Samples variabel | Keine absolute Höhenbindung in R3, R8 oder R8a | Am Startband gibt es keine feste Profilnaht. Für eine Fensteröffnung oder Profilersetzung fehlt daher ein Beleg. |

[A] Der kurze IIS ist ein minimales Konfliktzertifikat für die harte Endpunktmodellierung, nicht für die lokale Ursache des rampe_11-Werts 58,527 mm. Der Filterlauf optimiert eine gemeinsame Familien-Schlupfvariable; die Gegenprobe mit Ziel-Lock zeigt, dass sich der Schlupf auf andere Endpunktpaare verlagern kann. Eine Fenster-Bisektion war deshalb nicht aussagekräftig genug, um eine weitere lokale Sperre eindeutig und allein verantwortlich zu erklären.

### Rampe-11-Profil im Diagnosevergleich

[S] Es gab keine p3d37-Profiländerung. Zur Einordnung zeigt die Tabelle p3d31 V3 als Ausgangsprofil sowie zwei reine p3d37-Diagnoselösungen; die zweite erzwingt das Zielpaar bei 53,900 mm, ist aber wegen der übrigen elastischen Familien kein freizugebender Kandidat. Steigungen/Übergänge wurden nicht als Produktionsprofil abgenommen.

| Station (m) | p3d31 V3 vorher (m) | All-Familien-Optimum (m) | Ziel-Lock-Diagnose (m) |
|---:|---:|---:|---:|
| 0,0 | 12,905089 | 12,789899 | 12,789899 |
| 3,0 | 12,617188 | 12,543185 | 12,543185 |
| 6,0 | 12,139040 | 12,009618 | 11,969618 |
| 9,0 | 11,448132 | 11,711885 | 11,715684 |
| 12,0 | 10,797924 | 11,219331 | 11,219331 |
| 15,0 | 9,879534 | 10,500109 | 10,540107 |
| 18,0 | 8,950605 | 9,585949 | 9,585927 |
| 20,1 | 8,112218 | 8,652446 | 8,652426 |

## 2. Machbarkeit und Konstruktion

[S] Der harte Ausgangs-LP blieb infeasible; es gab keinen p3d37-Konstruktions-/Priority-Flood-/Checkerloop und keine Float32-Prüfprobe. Die 49 Diagnose-LPs nutzten höchstens 180 s Limit je Solve, ein Thread und blieben alle unter 6,3 s. Der IIS nutzte 840 s Limit und endete nach 0,114 s. Vor den Läufen waren 32 GB frei, über der geforderten 15-GB-Untergrenze.

[F] Keine Schwelle, keine Außenhöhe und keine Klippen-/Lokalitätsregel wurde geändert. Es gibt keinen p3d37-Kandidaten, für den R3/R8/R8a/R5/G5/G6/R9w-Ziele geprüft oder als bestanden ausgewiesen werden könnten.

## 3. Regelzahlen und Tile-Zahlen

[A] Da kein offizielles p3d37-Float32-Relief entstand, sind alle p3d37-Nachherwerte `n/a`, nicht 0. Zum nachvollziehbaren Vergleich stehen hier der im Auftrag genannte ältere Stand 9d3f8fc und der versionierte p3d17-Replay sowie die vorläufige p3d36-Probe 1 (unvollständige Endpunktkulisse; kein Freigabekandidat). p3d17-Replay: `pruefe_regeln` 600, R8 46 (9/10/4/23), R9 344 (23/34/287). Auftrag-Baseline 9d3f8fc: 596, R8 48 (9/10/5/24), R9 334 (25/34/275).

| pruefe_regeln | p3d17 Replay gesamt | p3d36 Probe 1 gesamt | D1/G1/D2 in p3d36 Probe 1 | p3d37 |
|---|---:|---:|---:|---|
| G11_objekt_schwebt_sinkt | 4 | 4 | 2/2/0 | n/a |
| G2_spitze_oben | 3 | 3 | 0/0/0 | n/a |
| G2_spitze_oben_fein | 8 | 8 | 0/0/0 | n/a |
| G3_spitze_unten | 4 | 3 | 0/0/0 | n/a |
| G3_spitze_unten_fein | 2 | 2 | 0/0/0 | n/a |
| G5_beule_klippe | 69 | 74 | 7/0/0 | n/a |
| G6_facette | 219 | 222 | 6/3/0 | n/a |
| G7_wand_glatte_flaeche | 1 | 1 | 0/0/0 | n/a |
| G7b_wandkontur_feld | 25 | 25 | 1/0/0 | n/a |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0/0/0 | n/a |
| G7b_wandkontur_rauheit | 1 | 1 | 0/0/0 | n/a |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0/0/0 | n/a |
| R1_blind | 24 | 24 | 2/1/0 | n/a |
| R1_wand | 0 | 2 | 2/0/0 | n/a |
| R2_getrennt | 15 | 15 | 1/0/1 | n/a |
| R3_laengs_m | 35 | 29 | 0/1/0 | n/a |
| R3_quer_pct | 29 | 12 | 0/0/0 | n/a |
| R3_woelb_m | 31 | 12 | 0/0/0 | n/a |
| R4_rand | 1 | 1 | 1/0/0 | n/a |
| R5_loch | 25 | 29 | 12/0/0 | n/a |
| R6_wasser_schnee | 4 | 4 | 0/3/0 | n/a |
| T1_fleckrand | 94 | 94 | 0/3/7 | n/a |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0/0/0 | n/a |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0/0/0 | n/a |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0/0/0 | n/a |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0/0/0 | n/a |

| R8 | p3d17 Replay | p3d36 Probe 1 | D1/G1/D2 in Probe 1 | p3d37 |
|---|---:|---:|---:|---|
| R8_gitter | 10 | 10 | 2/0/0 | n/a |
| R8_quer | 4 | 6 | 2/0/0 | n/a |
| R8_stufe | 9 | 9 | 2/0/0 | n/a |
| R8a_wegende | 23 | 23 | 3/0/0 | n/a |

| R9 | p3d17 Replay | p3d36 Probe 1 | D1/G1/D2 in Probe 1 | p3d37 |
|---|---:|---:|---:|---|
| R8b_delle | 23 | 23 | 1/0/0 | n/a |
| R9_saegezahn | 34 | 34 | 1/1/0 | n/a |
| R9w_wellen | 287 | 285 | 24/12/0 | n/a |

[S] p3d36 Probe 1 hatte zusammen D1/G1/D2: `pruefe_regeln` 34/13/8, R8 9/0/0, R9 26/13/0; D2-Treffer waren in dieser Vorprobe bitgleich zur Referenz. Sie verfehlte harte Ziele: G5 74 gesamt/7 D1, R5-Loch 29/12, G6 D1 6, R9w 285. p3d35 R0: `pruefe_regeln` 607, R8 44, R9 344, R5-Loch 25/8, R9w 287, D1 R3 13/21/20. p3d31 Runde 3: G5 71/4, R5-Loch 24/7, G6 D1 2, R5-Spitze 0, R8b D1 1, D1 R3 6/7/7, R9w 283, Kreuzung Stufe/Gitter 0,073/0,019 m.

## 4. Mesh-Gate

[F] Kein Mesh gebaut: die Startbanddiagnose ergab keine zulässige einzelne Ersetzung und der harte LP blieb infeasible. `gen_relief.py`, `baue_html.py`, pytest, Lochscan, `t42u`, Klippen-Gate, LOD1- und Bildpflicht wurden deshalb nicht ausgeführt. Es gibt keinen Mesh-Nachherwert; `lod1 < 1,3 Mio.` und `t42u summe=0` wurden für p3d37 nicht neu gemessen.

## 5. Prüfer, Hashes und Speicher

[S] Selbst berechnete SHA-256 der unveränderten Eingaben und des p3d17-Referenzmanifests:

| Prüffeld | SHA-256 |
|---|---|
| `neu/zellen_relief.csv` | `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa` |
| `neu/vektor.json` | `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e` |
| `neu/felder.json` | `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435` |
| G1-Probehöhe (Referenzmanifest) | `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` |
| D2-Probehöhe (Referenzmanifest) | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` |
| p3d17-Quellrelief gzip | `b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6` |
| Transferbasis p3d21 | `07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287` |

[S] Der eigene Prüfer-Diff gegen `89c61ce` enthält nur die drei bereits geerbten Dateien `r8_kreuzung.py`, `r8a_policy.py` und `test_r8a_policy_p3d26.py`; p3d37 änderte keine davon. G1/D2 wurden im unveränderten Referenzmanifest selbst nachberechnet und stimmen mit den Schutzhashes überein. Die fünf bekannten roten Bestandstests wurden nicht ausgeführt oder verändert.

[S] `codex_jobs/tools/p3d37/results/` belegt rund 1,6 MB (unter 30 MB); darin liegen ausschließlich kompakte JSON-Belege und keine LP/MPS-Dateien. Eigene temporäre p3d37-Solvermodelle, IIS-LP-Datei, Quellkopie und stdout wurden nach Übernahme der kompakten Belege aus `/tmp/p3d37/` entfernt. Vor dem Aufräumen waren 32 GB frei.

## Schluss in drei Sätzen

[S] Das All-Familien-Optimum zeigt am rampe_11-Start 58,526635 mm (LP), beziehungsweise 58,526516 mm nach Float32, während der Ziel-Lock unter elastischen Gegenbedingungen 53,899765 mm erreicht. [R] Die harte IIS-Zeile sitzt stattdessen an einem festen Außenpaar nahe rampe_2-ende; lokale Zeilenaudits und 28 Einzelfamilien-Gegenproben weisen keine einzelne strengere Sperre als Ursache des rampe_11-Werts nach. [F] Daher blieb die 54-mm-Grenze unverändert, es wurde keine Konstruktion freigegeben und kein Mesh gebaut.
