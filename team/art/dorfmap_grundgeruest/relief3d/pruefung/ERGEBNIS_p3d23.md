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

Noch nicht ausgeführt in diesem Zwischenstand. Der nächste Schritt ist die serielle offizielle Float32-Direktprobe für V24 mit der Round05-Cutliste, danach höchstens acht Checker-Runden mit frischer G5-/R5-/G11-Zählung. Es wird kein Mesh gebaut und keine Wegvariante übernommen.

## Vorläufige Drei-Satz-Aussage

V29/V30/V3 benötigen am Anfangsauslauf der Rampe 2 mindestens 0,072285 m zusätzliche R8a-Höhenänderung über der 0,10-m-Paargrenze, also 0,172285 m zwischen den bindendsten Nachbarpunkten. Das liegt außerhalb der unveränderten 0,10-m-Modellgrenze für R8a-Auslaufpaare; R3, Ebenenneigung, route/same-route Gefälle und Höhen-/Stufenschranken müssen dafür nicht gelockert werden. Die Wegführung kann in diesem Ansatz nur durch einen anders verteilten oder verlängerten Rampenstart-Auslauf mit der Grenze vereinbar werden; eine konkrete Wegänderung ist nicht Teil dieser Messung.

## Artefakte und Grenzen

JSON-Belege liegen unter `codex_jobs/tools/p3d23/results/`: p3d17-R3-Kalibrierung, Round00-All-open-Solves, sechs Familienfilterläufe, Round05-Row-Callsite-Diff und Familien-Diff-Rekonstruktion. `[A]` Der R8a-Maximalrest ist eine Diagnose des p3d22 linearen/MILP-Modells und noch kein offizieller R8/R9/Regel-Prüferlauf der resultierenden Float32-Fläche. Die ungerundeten Koordinaten und Transferbasen sind aus den p3d22-Artefakten übernommen.
