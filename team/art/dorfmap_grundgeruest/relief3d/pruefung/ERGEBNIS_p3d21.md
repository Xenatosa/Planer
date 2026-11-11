# Ergebnis p3d21

## Ergebnis: keine der drei Wegvarianten ist im festgelegten Modell machbar

Stand 11.11.2026. Branch `art/dorfmap-p3d21`, Basis `385703d` (`origin/art/dorfmap-p3d20`). Die unveränderten p3d18-V24-Polylinien wurden zuerst vermessen. Alle drei erlaubten lokalen Weggeometrien wurden danach mit den unveränderten Modellgrenzen geprüft; alle drei sind im festgelegten p3d20-Modell infeasible. Deshalb wurde für keine dieser Varianten eine offizielle Gate-Probe gestartet und kein Mesh gebaut. Die offiziellen Schwellen und Prüfer blieben unverändert.

Die p3d17-Referenzkalibrierung wurde erneut mit dem unveränderten offiziellen R3-Prüfer ausgeführt. Sie stimmt bytegenau mit dem Referenzmesh überein und zählt in D1 weiterhin **R3 längs/quer/Wölbung = 6/17/19**. Der Messlauf nutzte die V24-Geometrie und den unveränderten Reliefquellenhash `5e8fdb51c3f3f...` sowie `vektor.json` `aac6afff89ec...`.

Alle drei Machbarkeitsläufe verwendeten unverändert die p3d20-Formulierung und dieselben Modelllimits: R8-Stufe `≤0,116 m`, Gitter `≤0,019 m`, Quergefälle `≤2,95 %`, Einzelquerung `≤19,5 %`, R3 D1 `≤6/≤7/≤7`, Achs- und Ebenenstützen `±0,02 m`, Wegende `≤0,054 m` ohne R8a, Ebenenkern `r=2,00 m`. Die unveränderten offiziellen Zielzähler waren R5-Spitze D1 `0`, G6 D1 `≤3`, R8b D1 `≤1`, G3 D1 `≤1`, R9w gesamt `≤280`, G5 gesamt/D1 `≤69/≤2`, R5-Loch gesamt/D1 `≤22/≤5`, R4-Schlucht D1 `0`. Für den letzten Solve wurden Gitter-, Quer-, Einzelquer-, Endpunkt-Stage- und Endpunkt-R8a-Limits zusätzlich explizit in der Umgebung gesetzt.

### Bestätigte Ausgangsgeometrie

`[S]` bezeichnet direkt aus den V24-Polylinien und dem Relief gelesene Werte; `[R]` bezeichnet daraus berechnete Abstände oder Profile; `[A]` bezeichnet eine Modellannahme.

| Größe | rampe_11 | rampe_2 |
|---|---:|---:|
| `[S]` Länge | 57,00 m | 58,80 m |
| `[S]` Anfang → Ende | 148,5\|2,5 → 156,4845\|37,4888 | 126,51\|31,62 → 175,1496\|25,6900 |
| `[S]` Fall | 12,395 m | 12,104 m |
| `[S]` mittlere Neigung | 21,74 % | 20,58 % |
| `[S]` Station zum R8-Zentrum, nächste Achsposition | 41,479 m; 152,4484\|28,4359 | 31,473 m; 152,5442\|28,4428 |
| `[R]` kleinster Abstand Achse–R8-Zentrum | 0,138 m | 0,056 m |

Der tatsächliche Schnitt der zwei diskreten V24-Linien liegt bei `[R]` `152,4380|28,4557`. Der unveränderte offizielle R8-Cluster hat sein ungerundetes Zentrum bei `152,549857|28,489545` und wird als `152,5|28,5` angezeigt.

rampe_11 hat die drei vermessenen Kehren bei `[S]` s=`9,60 m` (`144,8252|9,5397`), s=`28,50 m` (`157,5350|18,8411`) und s=`47,40 m` (`150,1723|32,7338`). Gegenüber dem R8-Zentrum liegt die dritte Kehre bei `[R]` 5,838 m. Bei unverändertem Kernradius 2,00 m sind das 3,838 m Abstand außerhalb des Kerns; gegenüber dem 4,00-m-Übergangsaußenradius bleiben 1,838 m. `[A]` Der 4,00-m-Radius ist die p3d18/V24-Transferfade-Grenze und wird hier als äußerer Rand des Übergangs verwendet.

### Lokale Wegvariante 29, vermessen

Variante 29 ändert ausschließlich die beiden Rampenpfade `rampenwege[2]` und `[11]`; die übrigen elf Rampenpfade sind im Kandidaten semantisch unverändert. Die Kandidatenquelle in `/tmp` hat SHA-256 `9683b9fed1d80980615fe0c6c17ee5b75ae638074ae8c545900f8a4fe326c09f`. `vektor.json`, Dorfwege, Overlay und Zellquellen bleiben dabei unverändert. Die Wegänderungen werden durch `apply_route_variant.py` lokal und reproduzierbar erzeugt.

| Pfad / Station | vorher | Variante 29 | Änderung |
|---|---|---|---:|
| rampe_2, Länge | 58,800 m | 60,128 m | +1,327 m |
| rampe_2, s=20,055 m (R4) | 143,0992\|29,5940 | 143,3360\|31,5479 | 2,362 m |
| rampe_2, s=37,865 m (G5) | 157,8316\|27,7976 | 157,6582\|26,3527 | 1,746 m |
| rampe_2, s=39,752 m (G5) | 159,3922\|27,6041 | 159,1855\|25,8819 | 2,082 m |
| rampe_2, s=42,072 m (G5) | 161,3116\|27,3725 | 161,1352\|25,9027 | 1,777 m |
| rampe_11, Länge | 57,023 m | 55,390 m | −1,633 m |
| rampe_11, s=27,917 m (R5) | 157,1479\|18,5476 | 156,2462\|19,7370 | 1,791 m |
| rampe_11, s=47,400 m (dritte Kehre) | 150,1723\|32,7338 | 150,1722\|32,7339 | 0,0002 m |

Die maximale Quer-Verschiebung beträgt 2,385 m auf rampe_2 und 1,793 m auf rampe_11. Anfangs- und Endkoordinaten bleiben unverändert; alle vier Endpunkte liegen im trockenen Gelände. Der Start von rampe_11 liegt 1,149 m von der nächsten unveränderten Wand-Mittellinie entfernt. Der Rampenverlauf schneidet stellenweise eine Wand-Mittellinie wie schon vorher; der Endpunkt liegt 17,978 m davon entfernt.

Der geometrische Achsschnitt wandert von `[R]` `152,4380|28,4557` nach `152,4944|28,3426` (0,149 m). Das mit dem unveränderten `r8_kreuzung.py` berechnete offizielle Clusterzentrum wandert von `152,549857|28,489545` nach `152,760117|28,071282` (0,575 m); die Gate-Anzeige wird `152,8|28,1`. Das R8-Ziel folgt damit der geänderten Weggeometrie. Ein Quelllauf des offiziellen R8-Prüfers auf der Kandidatenquelle findet das neue Zentrum reproduzierbar; da er noch das unveränderte Höhenfeld sieht, ist seine Stufe `1,389 m` kein Mesh-Kandidat.

Das p3d18/V24-Raster und der Transferoperator wurden für diese Wegstützen unverändert weitergebunden; Beleg [`p3d21_transfer_base_v29.json`](../neu/p3d21_transfer_base_v29.json). Die Transferbasis lädt mit 185 rampe_11- und 201 rampe_2-Stützen.

**Machbarkeit Variante 29: UNMACHBAR im unveränderten Modell.** Ohne neue Ereignisschnitte meldet HiGHS Status 8 (infeasible), 7.856 Variablen und 15.236 Bedingungen. Die feste Konjunktion aus R8, R3, Achsstützen, Wegende und 2-m-Kern hat keinen zulässigen Punkt; deshalb wurde für diese Variante keine offizielle Gate-Probe gestartet. Der verwendete Solver liefert für den infeasiblen MILP-Lauf keine IIS/Einzelzeile, daher wird keine einzelne bindende Bedingung behauptet. Für diesen Kandidaten existieren keine erreichbaren gemeinsamen Meshwerte für G5, R5-Loch, R4, R8/R3 oder die übrigen harten Zähler; die p3d20-Runde-05-Werte oben sind nur der unveränderte Ausgangskandidat. Maschinenbeleg: [`model_round00.json`](../../../../../codex_jobs/tools/p3d21/variant29/model_round00.json).

### Lokale Wegvariante 30, vermessen

Variante 30 ist die zweite und letzte hier geprüfte lokale Weggeometrie. Sie verwendet kleinere, breiter ausgeblendete Offsets als Variante 29: rampe_2 wird bei s≈20 m und s≈40 m jeweils um höchstens 1,0 m, rampe_11 an der zweiten Kehre um höchstens 1,0 m seitlich verschoben. Die Kandidatenquelle ändert weiterhin ausschließlich `rampenwege[2]` und `[11]`; elf andere Rampenpfade, Zellwerte, Vektorwege und Overlay bleiben unverändert. Kandidatenquellenhash: `3a2e81dc6b2132238c92ddca971c1a9c2ad7c161b8facc7ae9e17468d4e89c80`.

| Pfad / Station | vorher | Variante 30 | Änderung |
|---|---|---|---:|
| rampe_2, Länge | 58,800 m | 59,053 m | +0,253 m |
| rampe_2, s=20,055 m (R4) | 143,0992\|29,5940 | 143,1978\|30,4081 | 0,984 m |
| rampe_2, s=37,865 m (G5) | 157,8316\|27,7976 | 157,7462\|27,0855 | 0,861 m |
| rampe_2, s=39,752 m (G5) | 159,3922\|27,6041 | 159,2936\|26,7826 | 0,993 m |
| rampe_2, s=42,072 m (G5) | 161,3116\|27,3725 | 161,2249\|26,6502 | 0,873 m |
| rampe_11, Länge | 57,023 m | 56,071 m | −0,952 m |
| rampe_11, s=27,917 m (R5) | 157,1479\|18,5476 | 156,6465\|19,2090 | 0,996 m |
| rampe_11, s=47,400 m (dritte Kehre) | 150,1723\|32,7338 | 150,1721\|32,7342 | 0,0006 m |

Die Anfangs- und Endkoordinaten bleiben gleich. Alle vier Endpunkte sind trocken; der nächste Wand-Mittellinienabstand am Start von rampe_11 bleibt 1,149 m. Der geometrische Achsschnitt wandert 0,120 m. Das offizielle R8-Clusterzentrum wandert von `152,549857|28,489545` nach `152,657964|28,263810`, also 0,303 m; der unveränderte R8-Prüfer zeigt `152,7|28,3`. Die Rohquellenprobe meldet dort Stufe `1,389 m` und Gitter `2,241 m`, weil das Quellhöhenfeld noch nicht das optimierte Mesh enthält. Transferbasis: [`p3d21_transfer_base_v30.json`](../neu/p3d21_transfer_base_v30.json), mit 187 rampe_11- und 197 rampe_2-Stützen.

**Machbarkeit Variante 30: UNMACHBAR im unveränderten Modell.** Ohne neue Ereignisschnitte meldet HiGHS Status 8 (infeasible), 7.854 Variablen und 15.159 Bedingungen. Es wurde keine offizielle Probe gestartet; eine IIS/Einzelzeile stellt der Solver nicht bereit. Für diese Variante gibt es daher keine gemeinsamen erreichbaren Meshwerte. Maschinenbeleg folgt unter `codex_jobs/tools/p3d21/variant30/model_round00.json`.

### Lokale Wegvariante 3 mit Transfer 29

Als dritte und letzte Geometrievariante bleibt rampe_11 vollständig unverändert; nur rampe_2 wird lokal bei s≈20 m und s≈40 m um bis zu 0,6 m verschoben. Transfer 29 bleibt der direkte p3d18/V24-Transfer. Kandidatenquellenhash: `b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6`; geändert wird ausschließlich `rampenwege[2]`.

| Pfad / Station | vorher | Wegvariante 3 | Änderung |
|---|---|---|---:|
| rampe_2, Länge | 58,800 m | 58,878 m | +0,077 m |
| rampe_2, s=20,055 m (R4) | 143,0992\|29,5940 | 143,1588\|30,0859 | 0,595 m |
| rampe_2, s=37,865 m (G5) | 157,8316\|27,7976 | 157,7788\|27,3569 | 0,533 m |
| rampe_2, s=39,752 m (G5) | 159,3922\|27,6041 | 159,3329\|27,1105 | 0,597 m |
| rampe_2, s=42,072 m (G5) | 161,3116\|27,3725 | 161,2581\|26,9267 | 0,539 m |
| rampe_11, gesamte Linie | unverändert | unverändert | 0,000 m |

Anfangs- und Endkoordinaten bleiben bis auf numerische Rundungsreste unter 0,0001 m gleich; alle vier Endpunkte bleiben trocken. Der geometrische Achsschnitt verschiebt sich 0,102 m. Das offizielle R8-Zentrum bewegt sich von `152,549857|28,489545` nach `152,629292|28,353591` (0,188 m); der unveränderte Prüfer zeigt `152,6|28,4`. Die Rohquellenprobe zeigt dort Stufe `1,389 m` und Gitter `2,234 m`; das ist kein optimiertes Mesh. Der V24-Transfer lädt für die neuen 191/197 Achsstützen unverändert; Beleg [`p3d21_transfer_base_route3_v29.json`](../neu/p3d21_transfer_base_route3_v29.json).

**Machbarkeit Wegvariante 3: UNMACHBAR im unveränderten Modell.** HiGHS meldet Status 8 (infeasible), 7.858 Variablen und 15.256 Bedingungen; `primal_feasible=false`. Die Modellgrenzen waren R3 D1 `≤6/≤7/≤7`, Kreuzungsstufe `≤0,116 m`, Achsstützen `±0,02 m`, Ebenenkern `r=2,00 m` und die zuvor dokumentierten unveränderten Sicherheitsabstände. Maschinenbeleg: [`model_round00.json`](../../../../../codex_jobs/tools/p3d21/variant3/model_round00.json). Der Solver stellt keine IIS/Einzelzeile bereit; daher ist kein einzelner bindender Constraint nachgewiesen. Da die Machbarkeit bereits fehlschlug, gibt es für diese Variante keine offizielle Gate-Probe und keine erreichbaren gemeinsamen Gatewerte. Das R8-Zentrum und die Rohquellenwerte oben sind Geometrie-/Quellendiagnostik, keine Gate-Probe.

### R8-Fenster und Restfehler

Das Längsfenster ist jeweils ±6,0 m um die nächste Achsstation am unveränderten R8-Zentrum. Die übertragenen V24-Höhen ergeben `[R]` für rampe_11 eine mittlere Längsneigung von 19,39 % und maximal 50,00 % pro Stützsegment; rampe_2 ergibt 10,57 % im Mittel und maximal 50,00 %. Querprofile wurden auf dem im Speicher rekonstruierten V24-D1-Mesh beidseits der Achse ausgewertet: bei ±1,5 m Offset beträgt die Querneigung am R8-Zentrum 1,36 % für rampe_11 und 2,48 % für rampe_2. Das Maximum über das jeweilige ±6-m-Fenster beträgt 15,09 % beziehungsweise 29,29 %. Diese Querprofile sind bilineare Achs-Normalprofile und nicht der offizielle R8-Ausgleichsebenenwert.

Die p3d20-Runde-05-Probe bleibt die unveränderte Gate-Ausgangsbasis: R8-Kreuzung `152,5|28,5` mit Stufe `0,11526 m`, Gitter `0,01900 m`, Quer `2,9500 %`; R3 D1 `4/0/4`; Endpunktstufe `0,054 m`, kein R8a. Der offizielle Kandidat verfehlte die gemeinsamen harten Ziele bei G5 `70/3` (gesamt/D1), R5-Loch `23/6` und R4-Schlucht D1 `1`.

| Restfehler aus p3d20 Runde 05 | Abstand zur Achse | Achsstation | Abstand zur nächsten Wand-Mittellinie |
|---|---:|---:|---:|
| `[S]` G5 `161,4|28,1` | rampe_2 0,879 m | 42,072 m | `[R]` 7,096 m (Nord) |
| `[S]` G5 `159,5|28,5` | rampe_2 1,083 m | 39,752 m | `[R]` 7,200 m (Nord) |
| `[S]` G5 `158,2|30,6` | rampe_2 3,392 m | 37,865 m | `[R]` 9,648 m (Nord) |
| `[S]` R5-Loch `158,0|17,5` | rampe_11 1,620 m | 27,917 m | `[R]` 3,000 m (Nord) |
| `[S]` R4-Schlucht `143,1|29,6` | rampe_2 0,007 m | 20,055 m | `[R]` 11,813 m (Nord) |

Wandabstände sind zur unveränderten Vektor-Mittellinie gerechnet, nicht zu einer neu triangulierten Wandfläche. Die R5-Stelle liegt nahe der zweiten Kehre von rampe_11; die R4-Stelle liegt praktisch auf rampe_2. Die drei G5-Stellen liegen östlich der Kreuzung nahe rampe_2.

### Zahlenstand der Regeln und Kacheln

Für p3d21 gibt es keine Mesh- oder Gate-Nachher-Zähler: Alle drei Geometrien scheiterten vor der Gate-Probe. Die folgenden vollständigen Zähler sind deshalb ausdrücklich der letzte verfügbare Vorher-/Vergleichsstand aus p3d20 Runde 05, kein Ergebnis einer p3d21-Variante. Beim allgemeinen Regelzähler verwendet der historische Start 596 den Prüferstand ohne G11; p3d20 Runde 05 wurde mit dem aktuellen Prüfer gezählt. Im aktuellen Schema ergibt ein p3d17-Replay 600 und Runde 05 563; G11 ist in beiden 4. Der p3d20-Bericht dokumentiert den Schemaunterschied.

| Regel | Start `9d3f8fc` | letzter verfügbarer Probe-Stand p3d20 R05 | p3d21 | Δ Start→p3d20 |
|---|---:|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 0* | 4 | nicht gemessen | +4* |
| G2_spitze_oben | 3 | 3 | nicht gemessen | 0 |
| G2_spitze_oben_fein | 8 | 8 | nicht gemessen | 0 |
| G3_spitze_unten | 4 | 3 | nicht gemessen | -1 |
| G3_spitze_unten_fein | 2 | 2 | nicht gemessen | 0 |
| G5_beule_klippe | 69 | 70 | nicht gemessen | +1 |
| G6_facette | 219 | 218 | nicht gemessen | -1 |
| G7_wand_glatte_flaeche | 1 | 1 | nicht gemessen | 0 |
| G7b_wandkontur_feld | 25 | 25 | nicht gemessen | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | nicht gemessen | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | nicht gemessen | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | nicht gemessen | 0 |
| R1_blind | 24 | 24 | nicht gemessen | 0 |
| R2_getrennt | 15 | 15 | nicht gemessen | 0 |
| R3_laengs_m | 35 | 33 | nicht gemessen | -2 |
| R3_quer_pct | 29 | 12 | nicht gemessen | -17 |
| R3_woelb_m | 31 | 16 | nicht gemessen | -15 |
| R4_rand | 1 | 0 | nicht gemessen | -1 |
| R4_schlucht | 0 | 1 | nicht gemessen | +1 |
| R5_loch | 25 | 23 | nicht gemessen | -2 |
| R5_spitze | 0 | 0 | nicht gemessen | 0 |
| R6_wasser_schnee | 4 | 4 | nicht gemessen | 0 |
| T1_fleckrand | 94 | 94 | nicht gemessen | 0 |
| T2_textur_abgeschnitten | 1 | 1 | nicht gemessen | 0 |
| T3_streifen_ringe | 1 | 1 | nicht gemessen | 0 |
| T4_graue_flussstreifen | 1 | 1 | nicht gemessen | 0 |
| T5_textur_vs_clay | 1 | 1 | nicht gemessen | 0 |
| **Summe** | **596** | **563** | **nicht gemessen** | **-33** |

\* Die historische 596er-Tabelle enthält keinen G11-Zähler; der gleiche aktuelle Prüfer zählt im p3d17-Replay und p3d20 R05 jeweils G11 `4`, also keine Änderung gegenüber diesem aktuellen Schema.

| R8-Regel | Start `9d3f8fc` | letzter verfügbarer Probe-Stand p3d20 R05 | p3d21 |
|---|---:|---:|---:|
| R8_stufe | 9 | 7 | nicht gemessen |
| R8_gitter | 10 | 8 | nicht gemessen |
| R8_quer | 5 | 4 | nicht gemessen |
| R8a_wegende | 24 | 20 | nicht gemessen |
| **R8 gesamt** | **48** | **39** | **nicht gemessen** |

| R9-Regel | Start `9d3f8fc` | letzter verfügbarer Probe-Stand p3d20 R05 | p3d21 |
|---|---:|---:|---:|
| R8b_delle | 25 | 23 | nicht gemessen |
| R9_saegezahn | 34 | 34 | nicht gemessen |
| R9w_wellen | 275 | 280 | nicht gemessen |
| **R9 gesamt** | **334** | **337** | **nicht gemessen** |

Die p3d20 Runde-05-Probe nutzte einen Dummy-`LOCHSCAN`-Wert, keinen Live-Lochscan; die Summen sind Prüfer-Probe-Zahlen, keine gebaute Mesh-Auswertung.

| Regel / Messwert | D1 p3d18 → letzter p3d20 R05 | G1 p3d18 → letzter p3d20 R05 | D2 p3d18 → letzter p3d20 R05 | p3d21 Mesh |
|---|---:|---:|---:|---:|
| G3_spitze_unten | 2 → 0 | 0 → 0 | 0 → 0 | kein Mesh |
| G5_beule_klippe | 2 → 3 | 0 → 0 | 0 → 0 | kein Mesh |
| G6_facette | 7 → 2 | 3 → 3 | 0 → 0 | kein Mesh |
| R3_laengs_m | 6 → 4 | 1 → 1 | 0 → 0 | kein Mesh |
| R3_quer_pct | 5 → 0 | 0 → 0 | 0 → 0 | kein Mesh |
| R3_woelb_m | 6 → 4 | 0 → 0 | 0 → 0 | kein Mesh |
| R4_schlucht | 0 → 1 | 0 → 0 | 0 → 0 | kein Mesh |
| R5_loch | 5 → 6 | 0 → 0 | 0 → 0 | kein Mesh |
| R5_spitze | 5 → 0 | 0 → 0 | 0 → 0 | kein Mesh |
| R8b_delle | 3 → 1 | 0 → 0 | 0 → 0 | kein Mesh |
| R9w_wellen | 23 → 21 | 12 → 12 | 0 → 0 | kein Mesh |
| R8/R8a am Zielkreuz/Wegende | 1 Quer-Treffer am Kreuz → 0 | 0 → 0 | 0 → 0 | kein Mesh |

Nicht aufgeführte Kachelregeln blieben im p3d20-Vergleich unverändert; D2 hatte 0 R8/R9-Treffer, Hash `749d3c4b…`, G1-Hash `38afeb30…`. Diese p3d20 Werte sind Referenzkontext und nicht mit p3d21-Ergebnissen gleichzusetzen. Für die drei p3d21-Varianten gibt es keine D1/G1/D2 Meshzähler.

### Belege und Grenzen dieses Ergebnisses

- [`messung_p3d21_v24.json`](messung_p3d21_v24.json) enthält Koordinaten, Höhenfenster, Querprofile, Kehrenabstände, Restfehlerabstände und Quellhashes. [`measure_routes.py`](../../../../../codex_jobs/tools/p3d21/measure_routes.py) rekonstruiert den unveränderten V24-Transfer im Speicher.
- Die Kalibrierung ergab wieder D1 `6/17/19`, V24-D1-Hash `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29` und den bisherigen Reliefhash `5e8fdb51c3f3f...`.
- Die Wandabstände sind Mittellinienabstände. Die Querprofile sind keine offiziellen R8-Ausgleichsebenenmessungen.
- Alle drei geometrischen Varianten sind in den jeweils dokumentierten Modellläufen infeasible; die solverseitigen Ergebnisse liefern keine IIS und belegen daher nicht, welcher Einzelconstraint bindet. Varianten 29 und 30 bewegen beide Pfade; Variante 3 bewegt nur rampe_2 maximal 0,598 m und lässt rampe_11 unverändert. Der Transfer war p3d18/V24, Ebenenkern `r=2,00 m`; keine p3d19-Pinning-Surrogate und keine R9w-Gleichheitsfixierung wurden eingesetzt.
- Wegen der Unmachbarkeit wurden keine offiziellen Gate-Proben für diese Kandidaten und kein Mesh ausgeführt. Damit gibt es für p3d21 keine erreichbaren gemeinsamen Werte für G5 gesamt/D1, R5-Loch gesamt/D1, R4 D1, R8 Gitter/Quer/Stufe, R3 D1, R5-Spitze/G6/R8b/G3 D1 oder R9w. Die p3d20 Runde-05-Werte sind nur der letzte verfügbare Vergleichsstand, nicht p3d21.
- Zellquellen, Overlay, `vektor.json`, die elf anderen Rampen, G1 und D2 wurden nicht geändert. Der Messlauf erzeugte Kandidaten nur in temporären Dateien; die Quellreliefhashes der Wegvarianten sind jeweils dokumentiert. Es wurde kein Mesh gebaut.
- Nicht ausgeführt, weil kein Mesh gebaut wurde: `gen_relief.py`, `baue_html.py`, Live-Lochscan/xvfb, `t42u`, pytest, Gelände-Mesh-Prüfung, delta.py, LOD1-Zählung und Bildpflicht. `t42u=0` ist daher hier nicht neu bestätigt; D2 blieb als Quelle unberührt.
