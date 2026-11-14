# Ergebnis p3d32

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d32` · Branch `art/dorfmap-p3d32` · Basis `origin/art/dorfmap-p3d31` @ `dc98146` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen · `[R]` Modell-/Gruppenfilterbefund · `[A]` Annahme oder Grenze · `[F]` Entscheidung.

## Ergebnis

`[F]` Die feste-Weghöhen-LP ist strukturell infeasible. Der geforderte All-Familien-Gruppenfilter wurde optimal gelöst; allein die Gruppe `variable_bounds` benötigt 0,05154638898 m Schlupf an rampe_2, Station 37,5 m. Das verletzt die geforderten festen Wegzellenhöhen; daher endet p3d32 hier ohne Float32-Probe und ohne Mesh.

## Konstruktion und LP

`[R]` Es wurde nur Variante 1 ausgeführt (`P3D32_VARIANT=1`, Standard): Kreuzungsplattformzentrum `[152,5|28,5]`, Ebenenkernradius 2 m, Quergefälle 1,5 %. Die Referenzhöhe 4,0545051228 m stammt aus der V3-Runde 3 von p3d31 (`p3d31_V3_round03_model.json`, SHA-256 `b8aed2cf…`). Das Gefälle folgt dem negativen bilinearen zentralen Höhengradienten dieser Lösung, physikalische Richtung `[-0,098598; 0,995127]`; benannter Auslauf ist `[152,5|30,0]` mit Plattformhöhe 4,0276366842 m. Am ungerundeten R8-Zentrum beträgt die Ebenenhöhe 4,0573571061 m. Der rampe_2-Start `[126,51|31,62]` ist auf 12,4698095322 m festgesetzt, ebenfalls aus dem p3d31-V3-Runde-3-Wegprofil.

`[R]` Das LP-Fenster umfasst die Rasterknoten `x=126..168`, `z=0..43`, Rasterweite 0,5 m: Kern plus 7,5-m-Ring. Darin sind 5.980 Höhen aktiv (2.802 Kern, 3.178 Ring); außerhalb liegen 1.415 Transferknoten fest auf Referenz. Das Arbeitsfeld hat 85×87 Knoten. R8-Kreuzungsbereich: Radius 4 m; Wegband: 4,5 m. Die Übertragungsstützen außerhalb des aktiven Fensters sind im Modell 0. Profilhöhen aller Rampen sind auf die p3d31-V3-Runde-3-Werte festgesetzt.

`[R]` Das Modell hat 20.411 Variablen, davon 0 ganzzahlig, und 76.616 Zeilen. Die verlangten R3-, R4-, R5-, R8-, G5/G6/G11-, Lokalitäts-, Drainage-, Wegprofil-, Plattform-, Endpunkt- und Klippenformbedingungen wurden als LP-Zeilen aktiviert. Die Klippenform bleibt außerhalb Wegband, Kreuzungskern und Ausläufen hart; für harte Krümmungszeilen gilt `max(0,02 m; 25 % · |Referenz-Zweitdifferenz|)`. Der Primärschritt minimiert die maximale Stufe; der sekundäre LP minimiert L1-Bewegung zur p3d17-Oberfläche und p3d17-Wegreferenz, wobei die p3d31-V3-Wegprofile hart festgesetzt bleiben, sowie gewichtete Krümmungsabweichungen. Der zusätzliche p3d32-Glättungsterm minimiert die L1-Abweichung der Zweitdifferenzen von p3d17 auf aktiven, nicht an Klippen liegenden Stencils mit Referenzgefälle 0,15–0,80. R9w-Pinning und R9w-Gleichheitssperren sind nicht gesetzt (`R9w_exact_bandpass_lock_points=0`, `regression_locks=0`).

`[R]` Der implementierte Priority-Flood nutzt Epsilon 0,001 m, 8-Nachbarschaft und die offizielle Senkenpolitik. Im infeasibility-Lauf wurden 0 Flood-Cuts und 0 Ereignis-Lazy-Cuts erzeugt. Ohne zulässiges LP-Ergebnis gab es keine Flood-Anhebung; angehobene Zellen, Summe und Maximum sind daher `n/a`. Die vorgesehenen Flood-Ausnahmen für Wegzellen, Anker, Fensterrand und Klippenbereiche wurden nicht praktisch an einer Kandidatenoberfläche geprüft.

`[A]` Ein Warmstart aus p3d31 Runde 3 wurde nicht verwendet. Dessen Oberfläche ist kein nachgewiesener zulässiger Startpunkt für die neuen festen Plattform- und Wegprofilbedingungen; ein Vergleich zweier LP-Solves wurde deshalb nicht ausgeführt. Die zweite implementierte Plattformvariante (2 % Quergefälle) wurde wegen des nachfolgend nachgewiesenen Strukturkonflikts nicht gestartet.

## Machbarkeit und Gruppenfilter

`[S]` Der erste Versuch ließ versehentlich Rampenprofile variabel und war nicht anforderungskonform. Sein Gruppenfilter verlangte 0,05154638898 m Schlupf bei rampe_2, Station 14,7 m, Karte `138,68964|30,34365`; dieser Vorversuch ist unter `codex_jobs/tools/p3d32/results/_alt/` erhalten. Nach Fixierung der Profile endete ein Lauf mit Presolve aus nach 600 s ohne primalen Punkt (Zeitlimit, kein Unmachbarkeitsnachweis). Der dafür gestartete Diagnoseversuch ohne Presolve wurde nach etwa 170 s ohne Befund beendet. Beide Läufe sind separat unter `_alt/p3d32_fixed_routes_presolve_off/` archiviert.

`[S]` Der korrigierte LP-Lauf mit deterministischem HiGHS-Presolve endete mit `Infeasible` (Code 8, HiGHS-Infeasibilität bewiesen, 1 Thread). Der anschließende All-Familien-Gruppenfilter war `Optimal` (Code 7). Von 26 aktivierten Diagnosegruppen war ausschließlich `variable_bounds` positiv; alle anderen Gruppen hatten Schlupf 0. Der einzige Maximalbefund ist:

| Feld | Gruppenfilterbefund |
|---|---:|
| Weg | rampe_2, route 2 |
| Station / Karte | 37,5 m / `157,43153097|27,42298231` |
| Festes Höhenband | Unter- und Obergrenze je 3,9332051388 m |
| Diagnostischer Höhenwert | 3,8816587498 m |
| Erforderlicher Bounds-Schlupf | 0,05154638898 m nach unten |

`[R]` Das ist ein optimaler Gruppenfilterbefund, kein zeilenweises IIS. Er zeigt, dass die übrigen geprüften Gruppen gemeinsam ohne Lockerung erfüllbar bleiben, wenn diese feste Weghöhe um rund 5,15 cm abgesenkt werden darf. Eine solche Änderung wäre eine Verletzung der festgesetzten p3d31-Wegzellenhöhen; sie wurde nicht übernommen. Der frühere ungültige Solvervektor und die dortige Zeilennummer sind kein zusätzlicher Ursachenbeweis.

## Runden und Checkerzahlen

`[S]` Es gab **keine offizielle Float32-Probe**. Die einzige korrigierte LP-Runde stoppte vor Float32-Transfer und Prüferlauf; für p3d32 existieren deshalb keine Nachherzahlen je Regel oder Kachel. Es wurde kein Prüferlauf mit einer erfundenen Ersatzoberfläche gemacht.

| Kennzahl | Ausgangswert vor p3d32 (9d3f8fc, Nutzerangabe) | p3d31 V3 Runde 3 (Vergleich, nicht p3d32) | p3d32 Runde 1 |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 596 | 576 | n/a — LP infeasible, keine Probe |
| R8 gesamt | 48 | 42 | n/a — keine Probe |
| R8 Stufe / Gitter / Quer / Wegende | 9 / 10 / 5 / 24 | 9 / 9 / 4 / 20 | n/a — keine Probe |
| R9 gesamt | 334 | 340 | n/a — keine Probe |
| R8b / R9 Sägezahn / R9w | 25 / 34 / 275 | 23 / 34 / 283 | n/a — keine Probe |

`[S]` Zum verlangten Kachelvergleich zeigt die letzte verfügbare offizielle Referenzprobe (p3d31 Runde 3; nicht p3d32) folgende Werte. Bei `pruefe_regeln` ist dies die Summe der dort ausgegebenen Regeltreffer je Kachel; R8 und R9 sind die offiziellen Kachelsummen. p3d32-Nachher bleibt mangels Probe in allen drei Kacheln offen.

| Checker | D1, p3d31 R3 | G1, p3d31 R3 | D2, p3d31 R3 | D1/G1/D2 p3d32 |
|---|---:|---:|---:|---|
| `pruefe_regeln` | 39 | 13 | 8 | n/a / n/a / n/a |
| R8 | 3 | 0 | 0 | n/a / n/a / n/a |
| R9 | 25 | 13 | 0 | n/a / n/a / n/a |

`[S]` p3d31-Runde-3-Treffer in D1 zur Einordnung: G5 4, R5_loch 7, G6 2, R5_spitze 0, R8b 1, G3 0, R4 0, R3 6/7/7, R9w 23; Gesamtwerte G5 71, R5_loch 24 und R9w 283. Die Kreuzung maß damals Stufe 0,073 m und Gitter 0,019 m. Dies sind keine p3d32-Werte. Die Zielgrenzen selbst wurden nicht gelockert.

`[S]` Die verbleibenden p3d31-Runde-3-D1-Orte als Vergleich (keine p3d32-Treffer): G5 bei `154,5|30,5` (0,66), `154,0|31,0` (1,01), `149,5|34,5` (1,58), `159,0|35,0` (1,96); R5_loch bei `143,5|8,0` (1,17 m), `143,5|10,0` (1,75 m), `154,0|14,0` (1,15 m), `155,0|15,5` (1,41 m), `157,5|16,5` (2,86 m), `159,0|18,5` (2,17 m), `157,5|20,0` (1,45 m). Die 23 R9w-Maxima liegen bei `141,2|0,2`, `143,5|0,5`, `153,5|0,2`, `152,8|2,2`, `159,9|9,5`, `152,6|5,5`, `140,9|11,1`, `167,8|13,8`, `137,0|20,8`, `164,4|22,4`, `164,5|24,1`, `149,3|27,0`, `158,9|26,5`, `139,8|28,1`, `165,6|28,9`, `156,6|29,2`, `128,5|30,0`, `135,7|32,4`, `163,8|31,0`, `155,4|35,2`, `135,7|40,1`, `154,6|39,3`, `155,0|40,8`.

## Unveränderte Eingaben, Prüferdiff und Gateumfang

`[S]` Selbst berechnete SHA-256 der Zellquellen und Geometrieeingaben:

| Datei | SHA-256 |
|---|---|
| `relief3d/neu/zellen_relief.csv` | `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa` |
| `relief3d/neu/vektor.json` | `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e` |
| `relief3d/neu/felder.json` | `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435` |

`[S]` Die p3d17-/p3d31-Referenzhashes der Float32-Höhenkanäle sind G1 `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` und D2 `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`; sie stimmen mit den gespeicherten p3d31-Proben überein. **Für p3d32 gibt es keinen Ergebnis-Hash**, daher wird Bitgleichheit eines p3d32-Kandidaten für G1/D2 nicht behauptet. Ebenso ist die Modellpinning-Regel außerhalb des Fensters dokumentiert, aber mangels Kandidaten nicht per Float32-Vergleich bestätigt.

`[S]` Der Prüfer-Python-Diff gegen `89c61ce` enthält nur die freigegebenen Dateien: `r8_kreuzung.py` (geändert), `r8a_policy.py` und `test_r8a_policy_p3d26.py` (hinzugefügt). `pruefe_regeln.py`, `relief_o18n.py`, `r9_form.py` sowie die R8a-Policy-Ausnahme wurden in p3d32 nicht geändert.

`[F]` Wegen des Strukturstopps liefen keine vorgeschriebenen Probe-Gates, kein `gen_relief.py`, kein `baue_html.py`, kein Mesh, kein `delta.py`, kein pytest und kein t42u-Lauf. Die fünf bekannten roten Bestandstests wurden nicht angefasst und nicht ausgeführt; Lod1, Bilder, t42u-Summe und der komplette Mesh-Gate sind folglich nicht gemessen. Das Overlay, `../referenz/*`, die Zellquellwerte und die p3d17-Eingabedateien wurden nicht geändert.

## Annahmen, Grenzen und offene Punkte

`[A]` Anker und festgesetzte Rampenprofile beziehen sich auf p3d31 V3 Runde 3; die Distanz- und Glättungsreferenz ist p3d17. Priority-Flood-Epsilon ist 1 mm. Die Gruppenfilterdiagnose minimiert gruppenweise normalisierte Schlupfe und ist ausdrücklich kein zeilenweises IIS.

`[R]` Die Grenze dieses Befunds ist lokalisiert: unter der verlangten Fixierung fehlen 5,15 cm an genau einer Rampenhöhe; alle anderen Diagnostikgruppen benötigen laut optimalem Filter keinen Schlupf. Der zuerst gefundene ähnliche Schlupf bei Station 14,7 m stammt aus dem verworfenen Modell mit variablen Rampen und ist kein p3d32-Ergebnis.

`[F]` Offen bleibt eine neue, autorisierte Modellvorgabe für rampe_2 bei Station 37,5 m. Solange Wegzellenhöhen fest bleiben müssen, sind eine weitere LP-Variante, Float32-Probe, Kachelprüfung und Mesh nicht zulässig.

## Selbstprüfung der Anforderungen 1–8

1. `[R]` Plattform, feste Höhenanker, Auslauf, Quergefälle und Fenster sind im Modell festgelegt; Stufen-, Gitter-, Quer- und Wegendwerte konnten mangels zulässigem Kandidaten nicht gemessen werden.
2. `[R]` Das Modell ist ein reines LP im D1-Kern-plus-7,5-m-Ring mit Randpinning, festen Wegprofilen und den vorhandenen Familienzeilen. Die LP-Zielfunktion und Glättung sind oben beschrieben; die Zielfunktion konnte wegen Infeasibilität nicht optimal gelöst werden.
3. `[R]` Priority-Flood/Epsilon und erneute LP-Prüfung sind implementiert; es gab keinen zulässigen Ausgangspunkt und folglich keine Flood-Anhebung oder Nachprüfung.
4. `[R]` Der Prüfer-Lazy-Cut-Loop ist implementiert; ohne offizielle Float32-Probe wurden keine Prüfertreffer nachgeschärft. Die p3d31-Runde-3-D1-Komponenten sind oben als Vergleich aufgeführt.
5. `[S]` Erfüllt: die feste-Weghöhen-LP ist bewiesen infeasible, der All-Familien-Gruppenfilter lokalisiert den Bounds-Schlupf auf rampe_2 Station 37,5 m; Stopp.
6. `[F]` Harte Ziele und Schwellen wurden im p3d32-Modell nicht gelockert. Es gibt keinen Messnachweis, dass sie erreicht sind.
7. `[F]` Nicht ausgelöst: weil keine Float32-Probe alle Ziele hält, wurde kein Mesh gebaut und kein Bild-Gate gestartet.
8. `[F]` Erfüllt: Fehlschlag, Ort und Schlupf sind berichtet; keine MIP-Ausweichvariante und kein Mesh.

## Schluss

`[F]` Die konstruktive reine LP scheitert mit fixierten V3-Wegprofilen an einer notwendigen Absenkung von rampe_2 um 0,05155 m bei Station 37,5 m. Der Gruppenfilter lässt nur die Weghöhen-Grenze locker und bestätigt den Strukturkonflikt, deshalb stoppt p3d32 wie gefordert vor Float32-Probe und Mesh. Alle p3d32-Nachher-Gates bleiben offen; die genannten p3d31- und Ausgangswerte sind Vergleichswerte, kein p3d32-Erfolg.
