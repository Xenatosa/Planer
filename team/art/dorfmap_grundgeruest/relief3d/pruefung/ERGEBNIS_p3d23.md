# Ergebnis p3d23 — Familien-IIS und Checker-in-the-loop

Stand: 11.11.2026 · Worktree `/workspace/wt_dorfmap_p3d23` · Branch `art/dorfmap-p3d23` · Basis `99bc3ad` (`origin/art/dorfmap-p3d22`) · Kosten **0 EUR**. Diagnoseauftrag; keine Weg- oder Prüferänderung und kein Meshbau.

Marker: `[S]` ausgeführter Prüfer oder reproduzierter Modelllauf · `[R]` Diagnosemodell · `[A]` Annahme.

## Teil A — Unlösbarkeit von V29/V30/V3

### Kalibrierung und Modellidentität

`[S]` Die offizielle R3-Kalibrierung auf p3d17 stimmt bytegenau mit dem gespeicherten D1-Referenzraster überein (SHA-256 `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`); der unveränderte Prüfer zählt D1 **6/17/19**. Quellenhash: `5e8fdb51c3f3dff9ad2c03c32a7c39ee1a4f97a3bc0942d47a352b1d0b4f0e88`.

`[S]` Die drei Round00-Eingaben, Transferbasen und ungerundeten R8-Zentren entsprechen den p3d22-Belegen. Alle nutzten dieselbe leere Ereignisschnittliste (SHA-256 `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`). Es gab keine Routenrekonstruktion, keinen Prüferaufruf und keinen Meshbau in Teil A.

| Geometrie | Relief-SHA-256 | Transferbasis (SHA-256) | R8-Zentrum `x|z` | Variablen / Familienzeilen |
|---|---|---|---|---:|
| V29 | `9683b9fed1d80980615fe0c6c17ee5b75ae638074ae8c545900f8a4fe326c09f` | `p3d21_transfer_base_v29.json` (`2974d27b8770684b8b37bc6369df020c9bbbaae9b48cc087b515554a07a6e6a3`) | `152.7601173875546|28.07128239088488` | 7.883 / 25.736 |
| V30 | `3a2e81dc6b2132238c92ddca971c1a9c2ad7c161b8facc7ae9e17468d4e89c80` | `p3d21_transfer_base_v30.json` (`e01165fb0b36e2186d05ea7eed6ced5aae28a44a98f1f0f78dab36d36611bed6`) | `152.65796405573423|28.263810474520962` | 7.881 / 25.695 |
| V3 | `b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6` | `p3d21_transfer_base_route3_v29.json` (`07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287`) | `152.6292918620858|28.353590994151514` | 7.885 / 25.886 |

### Bedingungsfamilien und Zeilenzahlen

`[R]` Die Zeilenzahlen beziehen sich auf das erweiterte p3d23-Round00-Modell je Geometrie. Zwei einseitige Ungleichungen pro Paar bzw. Stützpunkt sind als zwei Zeilen gezählt. Die R8a-/Wegende-Familien sind in V29/V30/V3 aktiv. Die D1-Regressionszäune aus p3d22 enthalten keine Zeilen; auch in Round00 gibt es keine Ereignisschnitte.

| Familie | V29 | V30 | V3 | Einheit / Inhalt |
|---|---:|---:|---:|---|
| Paargefälle, verschiedene Routen | 1.972 | 1.822 | 1.808 | Zeilen; `|hᵢ-hⱼ| ≤ 0,45·d` |
| Paargefälle, gleiche Route | 392 | 426 | 436 | Zeilen; gleiche Grenze |
| R8-Nachbarpaare / Kreuzungsstufe | 2.148 | 2.210 | 2.222 | Zeilen, Stufenvariable |
| Wegende-Stufenpaare, 0,054 m | 932 | 916 | 920 | Zeilen |
| Wegende-R8a-Auslaufpaare, 0,10 m | 4.104 | 4.102 | 4.108 | Zeilen |
| Achsauflagen | 714 | 712 | 718 | Zeilen, ±0,02 m |
| Ebenenkern-Stützpunkte | 282 | 278 | 286 | Zeilen, ±0,02 m |
| R8-Gitterabstand | 540 | 540 | 560 | Zeilen, 0,019 m |
| R8-Querneigung | 32 | 32 | 32 | Zeilen, 2,95 % |
| Ebenenneigung, Boxschranken | 4 | 4 | 4 | Zeilen, ±3 % |
| Ebenenneigung, Polygon | 32 | 32 | 32 | Zeilen, 3 % |
| Profilgefälle | 768 | 764 | 772 | Zeilen, 0,60 m/m je Abtastschritt |
| Quellgefälle-Monotonie | 379 | 376 | 381 | Zeilen |
| R3 längs | 773 | 769 | 777 | Operator- und Trefferzeilen |
| R3 quer/Wölbung/Einzelquerung | 2.168 | 2.180 | 2.204 | Operator-, Einzelwert- und Trefferzeilen |
| Endliche Höhen-/Stufen-/Zielflächen-Schranken | 10.495 | 10.531 | 10.625 | Zeilen; je endlicher Unter-/Obergrenze |
| D1-Regressionszäune `R5_spitze/G6/R8b/G3/R9w` | 0 | 0 | 0 | keine solchen Modellzeilen in p3d22 |
| Round00-Ereignisschnitte und Zählerkappen | 0 | 0 | 0 | leere Round00-Cutliste |
| Explizite Kreuzungsstufen-Kappe | 1 | 1 | 1 | Zeile, 0,116 m |

Die alten 18 Schlupfvariablen bilden 13 Gruppen (R3 längs/quer/Wölbung, Kreuzungsstufe, Achsauflagen, Ebenenkern, Wegende-Stufe, Gitter, Quer, Einzelquer, G5, R5-Loch, R4). Die zusätzlichen schaltbaren Familien sind Routenpaargefälle getrennt nach Route/gleicher Route, Wegende-R8a, Ebenenneigung getrennt nach Box/Polygon, endliche Variablenschranken, Profilgefälle und Quellmonotonie. Alle neu geöffneten Gruppen erhielten nichtnegative Schlupfe; p3d22s Bedingungen, Schwellen, Daten und Transfer blieben unverändert.

### All-open und Familienfilter

`[R]` Zuerst wurden alle alten und neuen Teil-A-Familien gemeinsam geöffnet. V29, V30 und V3 endeten jeweils optimal und machbar (HiGHS 7). In jedem Solve war ausschließlich `endpoint_r8a_extra_m` positiv: **0,072285079956 m**; alle anderen Schlupfe einschließlich route/same-route Gefälle, Wegende-Stufe, Ebenenneigung, Variablenschranken und R3/R8 blieben 0. Der gewichtete L1-Wert beträgt für jede Geometrie **0,722850799561** (Schlupf / jeweilige Skala; R8a-Skala 0,10 m), der größte normierte Gruppenschlupf ebenfalls 0,722850799561.

Der Deletion-Filter wurde je Geometrie mit zwei Gegenproben abgesichert: nur R8a geöffnet war optimal und machbar; bei geöffneten übrigen Familien, aber harter R8a-Grenze, war das Modell nachgewiesen unlösbar (HiGHS 8). Damit ist `{Wegende-R8a-Auslaufpaare}` eine belegte minimale Familien-IIS für jede der drei Geometrien; daraus wird keine Einzelzeilen-IIS behauptet.

| Geometrie | Alle Familien offen | Minimal bindende Familienmenge | R8a-L1 / maximal nötiger Schlupf | Größtes Paar `x|z` (m), Höhendifferenz nach Lockerung | nächster Routenendpunkt |
|---|---|---|---|---|---|
| V29 | Optimal, machbar | `{R8a-Auslaufpaare}` | 0,722851 / 0,072285 m | `127,25|31,25`–`127,25|31,50`: 0,172285 m statt 0,10 m | Rampe 2, Start nahe `126,51|31,62` |
| V30 | Optimal, machbar | `{R8a-Auslaufpaare}` | 0,722851 / 0,072285 m | `127,00|29,25`–`127,00|29,50`: 0,172285 m statt 0,10 m | Rampe 2, Start nahe `126,51|31,62` |
| V3 | Optimal, machbar | `{R8a-Auslaufpaare}` | 0,722851 / 0,072285 m | `126,50|29,25`–`126,50|29,50`: 0,172285 m statt 0,10 m | Rampe 2, Start nahe `126,51|31,62` |

`[R]` Der Maximalwert bezieht sich auf die gemeinsame additive Obergrenze für die R8a-Paarfamilie; dadurch wird der bindendste Paarrest minimiert. Innerhalb dieser Familie wurden keine zeilenweisen Schlupfe summiert. `variable_bounds_extra_m` lockert gemeinsam alle endlichen Höhen-/Zielraster-/Stufen-Schranken; im Optimum war der Schlupf 0 m.

### Diff der acht zuvor ungeklärten Round05-Bedingungen

`[R]` Der instrumentierte Row-Callsite-Vergleich erklärt den Nettoanstieg von 13 Zeilen zwischen dem archivierten Round05-Bericht (11.295) und p3d22 (11.308): fünf Ereigniszählerkappen (G5 gesamt/D1, R5 gesamt/D1, R4 D1) plus acht Nettozeilen. Der p3d22-Round05-Modellmittelpunkt ist das ungerundete R8-Zentrum; dadurch steigt die Zahl der Ebenenkern-Stützpunkte von 137 auf 141, also um vier Stützpunkte mit je zwei Ungleichungen (**+8 Zeilen**). p3d22 formuliert zusätzlich die Kreuzungsstufenkappe als explizite Zeile (**+1**); die archivierte p3d20-Zeilenangabe zählt ihrerseits die nach dem primären Solve für den sekundären Tie-break ergänzte `t ≤ primary_step`-Zeile (**−1** gegenüber der Primärmatrix): `5 + 8 + 1 − 1 = 13`. Der Callsite-Replay des eingecheckten p3d20-Modells ergibt primär 11.294 Zeilen und trifft p3d22 mit 11.308; der archivierte p3d20-Endbericht mit 11.295 enthält die sekundäre Tie-break-Zeile.

## Teil B — V24 Checker-in-the-loop

`[S]` V24 wurde als Float32-Direkttransfer-Probe über der unveränderten p3d18-Variante 24 gemessen. Es gab keinen Meshbau: das Probe-Relief lag je Runde unter `/tmp`; `loch_o18g.js`, `pruefe_regeln.py`, `r8_kreuzung.py` und `r9_form.py` liefen unverändert. Die G5-/R5-Komponenten wurden nach jeder offiziellen Probe frisch gezählt. Runde 1 startete mit den 50 p3d20-Round05-Schnitten; danach wurden erkannte G5-, R5-Loch- und neue D1-G11-Objektereignisse angefügt.

`[R]` Die G11-Objektschnittbedingung verwendet intern `|h−Objekt| ≤ 0,59999 m`, also 10 µm Abstand zur unveränderten offiziellen 0,60-m-Grenze. Dieser kleine Sicherheitsabstand fängt Float32-Rundung am strikten Prüfervergleich ab. Vier verworfene Läufe sind mit den Belegen `attempt0` bis `attempt3` getrennt archiviert: Big-M-Fehler, falsches Interzept-Vorzeichen, historischer Score ohne G11 und exakte 0,60-m-Modellgrenze ohne Float32-Abstand. Keiner davon zählt als Messrunde. Der unten ausgewertete Loop nutzt den aktuellen p3d17-Prüfer-Replay: 600 Gesamt-Treffer, davon G11-Objekt 4; neue Regelbezeichnungen ohne Eintrag in diesem Replay werden für die +5-Auswertung mit Baseline 0 angesetzt `[A]`.

### Checker-Runden

`[S]` Jeder Solve war seriell, HiGHS mit einem Thread und 600 s Einzelzeitlimit. In allen vier ausgewerteten Runden waren die alten 18 Diagnose-Schlupfwerte sowie der zusätzliche G11-Zählerschlupf 0; gewichteter L1-Wert und maximaler normierter Schlupf waren ebenfalls 0. „Bestscore“ ist die Summe der Treffer oberhalb der je-Regel-Plus-5-Grenzen, der R8/R9-Grenzen und der kalibrierten D1-R3-Zähler 6/17/19. Das ist ein Vergleichswert, kein Beweis eines global minimalen Prüfergebnisses.

| Runde | Modellstatus | Schnitte vor → nach | Neue Schnitte G5/R5/G11 | L1 / Max.-Schlupf | `pruefe_regeln` gesamt | G5 Gesamt/D1 | R5-Loch Gesamt/D1 | R4-Schlucht Gesamt/D1 | G11-Objekt Gesamt/D1 | Bestscore |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Optimal, machbar, Optimalität bewiesen | 50 → 102 | 5 / 29 / 18 | 0 / 0 | 626 | 74 / 7 | 51 / 34 | 0 / 0 | 22 / 20 | 35 |
| 2 | Optimal, machbar, Optimalität bewiesen | 102 → 133 | 8 / 24 / 0 | 0 / 0 | **614** | **75 / 8** | **46 / 29** | 0 / 0 | **4 / 2** | **28** |
| 3 | Optimal, machbar, Optimalität bewiesen | 133 → 170 | 1 / 36 / 0 | 0 / 0 | 622 | 70 / 3 | 58 / 41 | 0 / 0 | 4 / 2 | 36 |
| 4 | Optimal, machbar, Optimalität bewiesen | 170 → 194 | 2 / 24 / 0 | 0 / 0 | 610 | 71 / 4 | 46 / 29 | 0 / 0 | 4 / 2 | 29 |

| Runde | R8 Gesamt `Stufe/Gitter/Quer/Wegende` | R8 D1 `Stufe/Gitter/Quer/Wegende` | R9 Gesamt `Delle/Sägezahn/Wellen` | R9 D1 `Delle/Sägezahn/Wellen` | R3 D1 `längs/quer/Wölbung` | Score über Grenzwert |
|---:|---|---|---|---|---|---|
| 1 | 9 / 11 / 6 / 21 | 2 / 3 / 2 / 1 | 31 / 34 / 276 | 9 / 1 / 14 | 6 / 7 / 7 | Delle +1; R5 +21; G11-Objekt +13 |
| 2 | 9 / 11 / 7 / 21 | 2 / 3 / 3 / 1 | 35 / 34 / 275 | 13 / 1 / 13 | 6 / 7 / 7 | G5 +1; R5 +16; G11-Baum/Wand +6; Delle +5 |
| 3 | 9 / 11 / 6 / 21 | 2 / 3 / 2 / 1 | 32 / 34 / 272 | 10 / 1 / 10 | 6 / 6 / 7 | R5 +28; G11-Baum/Wand +6; Delle +2 |
| 4 | 9 / 11 / 6 / 21 | 2 / 3 / 2 / 1 | 37 / 34 / 276 | 15 / 1 / 14 | 6 / 7 / 7 | R5 +16; G11-Baum/Wand +6; Delle +7 |

`[S]` Der Loop stoppte nach Runde 4, nachdem die Runden 3 und 4 den besten Score nicht verbesserten. Runde 2 ist der beste beobachtete Kandidat (Score 28); Runde 4 erreicht 29. Damit ist kein globales Minimum bewiesen: Die offiziellen R5-Zahlen schwanken trotz frischer Komponenten-Schnitte, und die R5-Loch-Schnittnäherung bildet die offiziellen Ereignisse nach vier Runden nicht vollständig ab. G11-Objekt fällt in Runde 2 auf den aktuellen p3d17-Baselinewert 4 (D1=2, G1=2); G11-Baum/Wand ist eine andere Prüferregel und wurde nicht als Ereignisschnitt modelliert.

### Regeln vorher/nachher

`[S]` Die linke Spalte ist der historische Stand `9d3f8fc` (Summe 596); der aktuelle p3d17-Replay hat Summe 600, weil G11-Objekt dort 4 Treffer zählt. Für neue Kategorien ohne historischen Eintrag ist Baseline 0 angenommen. Bei Runde 2 beträgt die aktuelle Prüfersumme 614 (historischer Vergleich +18; gleiches aktuelles Schema +14).

| Regel | Historisch 9d3f8fc | Best V24 R2 | Δ gegen vergleichbare Baseline | Über +5? |
|---|---:|---:|---:|---:|
| G11-Baum/Wand `[A: Baseline 0]` | — | 11 | +11 | +6 |
| G11-Objekt schweben/sinken `[S: aktueller Replay 4]` | — | 4 | 0 | 0 |
| G2-Spitze oben | 3 | 3 | 0 | 0 |
| G2-Spitze oben fein | 8 | 8 | 0 | 0 |
| G3-Spitze unten | 4 | 3 | −1 | 0 |
| G3-Spitze unten fein | 2 | 2 | 0 | 0 |
| G5-Beule/Klippe | 69 | 75 | +6 | +1 |
| G6-Facette | 219 | 218 | −1 | 0 |
| G7-Wand glatte Fläche | 1 | 1 | 0 | 0 |
| G7b-Wandkontur Feld | 25 | 23 | −2 | 0 |
| G7b-Wandkontur Kantenschärfe | 1 | 1 | 0 | 0 |
| G7b-Wandkontur Rauheit | 1 | 1 | 0 | 0 |
| G8-Fluss nicht bis Rand | 1 | 1 | 0 | 0 |
| R1-blind | 24 | 24 | 0 | 0 |
| R1-Wand `[A: Baseline 0]` | — | 2 | +2 | 0 |
| R2-getrennt | 15 | 15 | 0 | 0 |
| R3-längs | 35 | 35 | 0 | 0 |
| R3-quer | 29 | 19 | −10 | 0 |
| R3-Wölbung | 31 | 19 | −12 | 0 |
| R4-Rand | 1 | 1 | 0 | 0 |
| R4-Schlucht `[A: Baseline 0]` | — | 0 | 0 | 0 |
| R5-Loch | 25 | 46 | +21 | +16 |
| R6-Wasser/Schnee | 4 | 4 | 0 | 0 |
| T1-Fleckrand | 94 | 94 | 0 | 0 |
| T2-Textur abgeschnitten | 1 | 1 | 0 | 0 |
| T3-Streifen/Ringe | 1 | 1 | 0 | 0 |
| T4-graue Flussstreifen | 1 | 1 | 0 | 0 |
| T5-Textur vs Clay | 1 | 1 | 0 | 0 |

| R8-Regel | Start `9d3f8fc` | Best V24 R2 | Δ |
|---|---:|---:|---:|
| Stufe | 9 | 9 | 0 |
| Gitter | 10 | 11 | +1 |
| Quer | 5 | 7 | +2 |
| Wegende | 24 | 21 | −3 |
| **R8 gesamt** | **48** | **48** | **0** |

| R9-Regel | Start `9d3f8fc` | Best V24 R2 | Δ | Über +5? |
|---|---:|---:|---:|---:|
| Delle | 25 | 35 | +10 | +5 |
| Sägezahn | 34 | 34 | 0 | 0 |
| Wellen | 275 | 275 | 0 | 0 |
| **R9 gesamt** | **334** | **344** | **+10** | — |

### Kachelwerte D1/G1/D2

`[S]` Für die Regelzähler je Kachel ist links der offizielle p3d20-Round05-Probeausgang als Schnitteingang, rechts der beste p3d23-Probelauf R2 angegeben. Die R8-Spalten notieren `Stufe/Gitter/Quer/Wegende`; R9 notiert `Delle/Sägezahn/Wellen`.

| Kachel | `pruefe_regeln` p3d20 R05 → p3d23 R2 | R8 p3d20 R05 → R2 | R9 p3d20 R05 → R2 |
|---|---|---|---|
| D1 | R05: G11-Objekt 2, G5 3, G6 2, G7b-Feld 1, R1-blind 2, R2 1, R3 4/0/4, R4-Schlucht 1, R5 6. R2: G11-Baum/Wand 11, G11-Objekt 2, G5 8, G6 2, R1-blind 2, R1-Wand 2, R2 1, R3 6/7/7, R4-Schlucht 0, R5 29. | R05 listet 4 D1-Kreuzungseinträge; R2: 2/3/3/1. | 1/1/21 → 13/1/13 |
| G1 | G11-Objekt 2, G6 3, R1-blind 1, R3-längs 1, R6 3, T1 3 → unverändert | 0/0/0/0 → 0/0/0/0 | 0/1/12 → 0/1/12 |
| D2 | R2 1, T1 7 → unverändert | 0/0/0/0 → 0/0/0/0 | 0/0/0 → 0/0/0 |

`[S]` R8a-Wegende ist in D1 in jeder Looprunde ein offizieller Treffer (1); die D1-Kreuzungsstufe zählt 2. G1 und D2 bleiben bei R8/R9 null. Die G1-Höhenhashes bleiben `38afeb30…`, D2 `749d3c4b…`; D2-Regelzähler und Höhenbytes sind unverändert. D1-Probenhash Runde 2: `a22be9548f7f3f3e5735ad7ffbc03b415ed66ccd980737bae2a90665548039ac`.

## Drei-Satz-Aussage

V29/V30/V3 benötigen am Anfangsauslauf der Rampe 2 zusätzlich 0,072285 m über der 0,10-m-R8a-Paargrenze; für V24 bleiben im besten event-aware Probelauf mindestens 1 G5-, 16 R5-Loch-, 5 R9-Dellen- und 6 G11-Baum/Wand-Treffer über den aktuellen je-Regel-Plus-5-Grenzen, zusammen 28 Regelzählereinheiten. Damit liegt die R8a-Lockerung außerhalb der unveränderten 0,10-m-Modellgrenze und der V24-Probelauf außerhalb der Plus-5-Grenzen, während R8 gesamt bei 48 bleibt und G11-Objekt auf seinem aktuellen Referenzwert liegt. Die Messung belegt keinen passenden neuen Verlauf: R5-Komponenten blieben nach vier Schnittrunden instabil, R8a bindet am Start von Rampe 2, und eine konkrete Wegänderung lässt sich aus diesen Läufen nicht ableiten.

## Artefakte, Annahmen und Grenzen

JSON-Belege liegen unter `codex_jobs/tools/p3d23/results/`: R3-Kalibrierung, alle Teil-A-Solves und Filter, Row-Diff, Checker-Loop mit den vier gültigen Runden, vollständige offizielle Probes und die getrennten, als ungültig markierten Diagnoseversuche. `[S]` Die D2-Höhenhashes und Regeln blieben unverändert; G1 ebenfalls. `[A]` Für `G11_baum_an_wand` und `R1_wand` fehlt ein Eintrag im historischen Regelreport; ihre +5-Auswertung setzt daher Baseline 0. `[R]` Der Score 28 ist der beste beobachtete Stand, keine IIS und kein Beweis einer global minimalen Trefferzahl. Nicht gelöst sind die verbleibenden R5/G5-Checkerereignisse und die getrennte G11-Baum/Wand-Regel. Es gab keine Änderung an Wegführung, Prüfern, Schwellen, Overlay, Zellquellen oder Mesh; Kosten 0 EUR.
