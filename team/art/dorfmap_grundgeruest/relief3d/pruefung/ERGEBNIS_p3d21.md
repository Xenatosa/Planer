# Ergebnis p3d21

## Zwischenstand: Vermessung vor einer Wegänderung

Stand 11.11.2026. Branch `art/dorfmap-p3d21`, Basis `385703d` (`origin/art/dorfmap-p3d20`). Die unveränderten p3d18-V24-Polylinien wurden vermessen, bevor eine Geometrie geändert wurde. Zu diesem Zwischenstand gibt es noch keine Wegvariante und kein neues Mesh.

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
