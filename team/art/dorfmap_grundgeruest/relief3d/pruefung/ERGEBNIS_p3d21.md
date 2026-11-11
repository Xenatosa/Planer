# Ergebnis p3d21

## Zwischenstand: Vermessung vor einer Wegänderung

Stand 11.11.2026. Branch `art/dorfmap-p3d21`, Basis `385703d` (`origin/art/dorfmap-p3d20`). Die unveränderten p3d18-V24-Polylinien wurden vermessen, bevor eine Geometrie geändert wurde. Variante 29 ist danach lokal vermessen; Modell-Machbarkeit und offizielle Kandidatenprobe stehen noch aus. Ein neues Mesh wurde noch nicht gebaut.

Die p3d17-Referenzkalibrierung wurde erneut mit dem unveränderten offiziellen R3-Prüfer ausgeführt. Sie stimmt bytegenau mit dem Referenzmesh überein und zählt in D1 weiterhin **R3 längs/quer/Wölbung = 6/17/19**. Der Messlauf nutzte die V24-Geometrie und den unveränderten Reliefquellenhash `5e8fdb51c3f3f...` sowie `vektor.json` `aac6afff89ec...`.

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

### Belege und Grenzen dieses Zwischenstands

- [`messung_p3d21_v24.json`](messung_p3d21_v24.json) enthält Koordinaten, Höhenfenster, Querprofile, Kehrenabstände, Restfehlerabstände und Quellhashes. [`measure_routes.py`](../../../../../codex_jobs/tools/p3d21/measure_routes.py) rekonstruiert den unveränderten V24-Transfer im Speicher.
- Die Kalibrierung ergab wieder D1 `6/17/19`, V24-D1-Hash `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29` und den bisherigen Reliefhash `5e8fdb51c3f3f...`.
- Die Wandabstände sind Mittellinienabstände. Die Querprofile sind keine offiziellen R8-Ausgleichsebenenmessungen.
- `[A]` Eine minimale Änderung an der dritten rampe_11-Kehre, an rampe_2 östlich der Kreuzung oder am gemeinsamen Kreuzungsbereich könnte den Ereignisraum von G5/R5/R4 verändern. Ob das unveränderte p3d20-Ereignismodell damit eine gemeinsame zulässige Float32-Lösung findet, ist noch offen.
- Zellquellen, Overlay, Vektorwege, G1 und D2 wurden in diesem Messschritt nicht geändert. Es wurde kein Mesh gebaut.
