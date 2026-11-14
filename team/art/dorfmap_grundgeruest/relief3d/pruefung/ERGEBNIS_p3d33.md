# Ergebnis p3d33

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d33` · Branch `art/dorfmap-p3d33` · Basis `origin/art/dorfmap-p3d32` @ `b8b9364` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen · `[R]` Modell-/Gruppenfilterbefund · `[A]` Annahme oder Grenze · `[F]` Entscheidung.

## Zwischenstand

`[F]` Die p3d33-Implementierung ist vorbereitet; Ergebnis, Machbarkeit, Float32-Probe und Mesh-Entscheidung folgen nach dem deterministischen LP-Lauf. Bis dahin wird kein Mesh gebaut.

`[R]` `P3D33_VARIANT=1` (Standard) gibt nur rampe_2-Profilpunkte mit physischer Station 25–50 m frei. `P3D33_VARIANT=2` erweitert bei bewiesener Infeasibilität ausschließlich auf 20–55 m. Außerhalb des ausgewählten Fensters bleiben Rampenhöhen auf p3d31 V3 Runde 3 gepinnt; rampe_11, der rampe_2-Start, Plattformmittelpunkt `[152,5|28,5]`, Plattformgefälle 1,5 %, Auslauf, Zellquellen und Grundriss bleiben wie p3d32.

`[R]` Die diskrete Profilinterpolation ist C0-stetig. An den beiden Nahtpunkten werden gleiche einseitige erste Differenzen hart als LP-Gleichheit gesetzt (damit ist die Naht-Zweitdifferenz 0). Zusätzlich wird am Rand das offizielle R3-Wölb-Stencil `|h(0) − (h(+1,5)+h(−1,5))/2| ≤ 0,08 m` hart erzwungen. Die offiziellen R3-Stencils verwenden 0,25 map-Einheiten, Sigma 8 Stichproben, Abschnittsbreite 16 Stichproben, Querstichproben bei ±1,5 m sowie Grenzwerte 0,08 m/3,5 %; die LP-Hitbudgets betragen 6/7/7 in D1 und werden an der Float32-Probe nochmals mit dem unveränderten Prüfer kontrolliert.

`[R]` Die Kreuzungs-LP-Grenzen sind Stufe 0,116 m, Gitter 0,020 m und Quergefälle 3 %; Einzelquer ist 20 %. Wegendstufe ist 0,054 m, R8a ist 0,10 m mit der einzigen offiziellen 0,18-m-Ausnahme am rampe_2-Start `[126,51|31,62]`. p3d33 enthält keine Änderung an den Prüfern.

## Eingang, Prüfer und Unverändertes

`[S]` Vor dem Solve selbst berechnete Hashes:

| Datei/Kanal | SHA-256 |
|---|---|
| `neu/zellen_relief.csv` | `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa` |
| `neu/vektor.json` | `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e` |
| `neu/felder.json` | `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435` |
| G1-Höhenkanal Soll | `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` |
| D2-Höhenkanal Soll | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` |

`[S]` Der erwartete Quellrelief-Hash ist `b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6`; der unveränderte Transferbasis-Hash ist `07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287`. Die p3d17-Referenzdatei hat SHA-256 `f7c332dcc0585949fd124213d31965a42af1e35359e99d9881198d0a75c4d775`.

`[S]` Der Prüfer-Python-Diff gegen `89c61ce` wird für die Schlussfassung ausgewiesen. p3d33 ändert keine Datei unter `relief3d/pruefung/` außer diesem Ergebnisbericht; insbesondere bleiben `pruefe_regeln.py`, `r8_kreuzung.py`, `r8a_policy.py`, `r9_form.py` und `relief_o18n.py` unverändert.

## p3d32-Schlupf und p3d33-Prüfung

`[S]` p3d32 meldete in der korrigierten LP `0,05154638898 m` Bounds-Schlupf bei rampe_2 Station 37,5 m (`157,43153097|27,42298231`). Der verworfene Vorversuch mit variablen Rampen meldete denselben Betrag bei Station 14,7 m (`138,68964|30,34365`), allerdings gegen eine andere untere Höhenbegrenzung. Gleicher Betrag allein belegt keine gemeinsame Zeilenursache; p3d33 prüft, ob das freigegebene Fenster den korrigierten Schlupf auflösen kann. Die Diagnose wird nach dem Lauf anhand beider Gruppenfilter-Zeilen und ihrer Höhenbänder vervollständigt.

`[R]` LP-Machbarkeit, gegebenenfalls Gruppenfilter/IIS, Float32-Probezahlen und verbleibende Treffer sind noch offen. Die zulässigen Probe-Runden sind seriell, mit einem HiGHS-Thread und maximal 600 s je Solve; die Ergebnisse werden unter `codex_jobs/tools/p3d33/results/` gespeichert.

| Kennzahl | Ausgang 9d3f8fc | p3d31 V3 Runde 3 | p3d33 |
|---|---:|---:|---:|
| `pruefe_regeln` gesamt | 596 | 576 | offen |
| R8 gesamt (Stufe/Gitter/Quer/Wegende) | 48 (9/10/5/24) | 42 (9/9/4/20) | offen |
| R9 gesamt (R8b/Sägezahn/R9w) | 334 (25/34/275) | 340 (23/34/283) | offen |
| pruefe_regeln D1/G1/D2 | offen | 39/13/8 | offen |
| R8 D1/G1/D2 | offen | 3/0/0 | offen |
| R9 D1/G1/D2 | offen | 25/13/0 | offen |

`[A]` Der p3d31-Runde-3-Vergleich hatte G5 71/4 gesamt/D1, R5_loch 24/7, G6 D1 2, R5_spitze D1 0, R8b D1 1, G3 D1 0, R4-Schlucht D1 0, R3 D1 6/7/7 und R9w gesamt 283. Kreuzungswerte waren Stufe 0,073 m und Gitter 0,019 m. Diese Werte sind nur Vergleich, keine p3d33-Messung.

## Mesh, Grenzen und Abschluss

`[F]` Mesh-Bau erfolgt nur, wenn mindestens eine unveränderte offizielle Float32-Probe alle harten Ziele und die +5-Schranke erfüllt. Dann werden vollständiges Mesh-Gate, Delta, Tests, t42u, lod1 und geforderte Vorher-/Nachherbilder ergänzt; andernfalls endet die Arbeit vor `gen_relief.py`/`baue_html.py`.

`[A]` Grenzen/offene Punkte bis zum Schluss: Machbarkeit der Fenster-LP, exakte Nahtwerte und Profiltabelle, R9w-/G5-/R5-Loch-Lazy-Cut-Konvergenz, D1/G1/D2-Kachelsummen, Bitgleichheit außerhalb des Aktivfensters, D2-Treffervergleich sowie Mesh- und Bildgate.

## Selbstprüfung Anforderungen 1–8

1. `[R]` Fenster 25–50 m (Standard) und ausschließlich bei Infeasibilität 20–55 m sind implementiert; Stationen außerhalb bleiben fest.
2. `[R]` Offizielle Prüfer-Stencils und Grenzwerte sind im LP abgebildet; finaler Float32-Nachweis offen.
3. `[R]` C0/C1 und Rand-Wölb-Stencil sind implementiert; Messnachweis folgt aus Probe.
4. `[R]` p3d32-Konstruktion, reine kontinuierliche LP, 22 Familien, Lokalität, feste Plattform, feste andere Wege, Priority-Flood und lokale Prüfer-Cuts wurden übernommen; Prüfer und Quellflächen sind unangetastet.
5. `[F]` Bei bewiesener Infeasibilität wird der All-Familien-Gruppenfilter ausgeführt und vor einer Probe gestoppt; Ergebnis offen.
6. `[R]` Harte Ziele und p3d17-+5-Schranke sind unverändert im Gate; Messung offen.
7. `[F]` Mesh und Bilder nur nach bestandener Probe; noch nicht ausgelöst.
8. `[F]` Bei verfehltem Ziel wird ohne Mesh gestoppt und mit Treffern/Orten berichtet; Ergebnis offen.

## Schluss

`[F]` p3d33 erweitert ausschließlich die rampe_2-Höhenlinie im definierten Stationsfenster und erhält an beiden Fensterrändern eine C1-stetige Verbindung. Ob die 25–50-m-Variante die LP-Machbarkeit und alle Float32-Ziele erreicht, ist noch nicht gemessen. Bis zu einem vollständig bestandenen Proben-Gate wird kein Mesh gebaut.
