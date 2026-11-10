# Transfer-Messung p3d17 — Zwischenstand vor dem Bau

Stand: 10.11.2026 · Branch: `art/dorfmap-p3d17` · Basis: p3d16 `3021164`

## Modell und Ergebnis

Die p3d16-Untergrenze `0,064738629 m` verwendete 0,25 Map-Einheiten als freie Flächenstützen. Das ausgegebene D1-Mesh hat 0,5 Map-Einheiten Rasterabstand (`CELL_M=1,2 m`); der Regelprüfer wertet weiterhin bilinear auf 0,25 Map-Einheiten aus. Deshalb habe ich das gemeinsame R8/R3-MILP mit Meshvariablen auf dem 0,5-Raster und derselben 0,25-Prüfauswertung neu gelöst.

Mit exakten Achsstützen und der unveränderten Ebenenkernbindung von ±0,02 m ist die Lösung optimal: **Untergrenze 0,074183458 m**, Dual Bound identisch, MIP-Gap 0, sechs interne R3-Abschnitte in D1. Damit bleibt sie 0,041816542 m unter dem Stufenziel von 0,116 m. Die achsweise Sollhöhe ist auf diesem Raster exakt bilinear darstellbar. Der separate Tie-Break minimiert die Bewegung gegenüber dem p3d16-Profil und dem p3d16-GB-Mesh, ohne die Untergrenze zu verändern.

Eingaben, Modell und vollständige Lösung liegen in `codex_jobs/tools/p3d17_transfer/`. Die Variante mit ±0,02-m-Achsstütze ergibt 0,071926045 m; die strengere exakte Achsstütze wird für Variante 21 verwendet.

## Abweichungen am p3d16-Mesh

Die Tabellen vergleichen das p3d16-Prüffeld mit der neuen gemeinsamen Lösung. `Differenz` bedeutet `Mesh − LP`. Stationspunkte nutzen bilineare Mesh-Auswertung. Die Rasterpunkt-Tabelle enthält die 0,5-Map-Einheiten-Stützen innerhalb des lokalen 8×8-Map-Einheiten-Fensters.

| Bereich | Probe | Soll LP (m) | Mesh p3d16 (m) | Differenz (m) | Zugehörige Transferstufe |
|---|---|---:|---:|---:|---|
| Achse, alle D1-Stationen | rampe_11, s=34,5 m, 155,2205\|23,2433 | 5,589353 | 6,396444 | +0,807091 | Das ist überwiegend eine andere gemeinsame Profil-LP-Lösung; p3d16s eigenes Profil-Soll wird entlang der Achse bis auf 0,020001 m getroffen. |
| Achse, Kern r≤2 m | rampe_2, s=33,3 m, 154,0557\|28,2596 | 4,015930 | 3,972459 | −0,043470 | Im Kern ist die Ebenenabdeckung voll. Die Abweichung setzt sich aus geändertem LP-Profil und dem p3d16-Rasterfit zusammen. |
| Achse, Ring 2<r≤4 m | rampe_11, s=37,8 m, 153,9218\|25,6674 | 4,658741 | 5,143424 | +0,484683 | Gemeinsames Profil-Soll plus radialer Ebenen- und Terrainübergang; p3d16 trifft sein eigenes Profil-Soll hier auf 0,020000 m. |
| Bandrand, Ring 2<r≤4 m | 152,5\|31,5, lateral 1,796 m, r=3,600 m | 3,515640 | 3,329083 | −0,186557 | RBF-Querfeld, projiziertes Bandprofil und Ringübergang. |
| Wegband, Ring 2<r≤4 m | 154,5\|26,0, lateral 0,800 m, r=3,842 m | 4,558543 | 5,097634 | +0,539091 | Bandquerprofil plus Mischung im Ring. |
| Kernraster r≤2 m | 151,0\|28,0 | 4,067094 | 4,015893 | −0,051201 | Gemeinsame LP-Stütze und Ebenenkern; kein radialer Auslauf innerhalb r=2 m. |

Am kritischen R8-Paar 155,25\|25,75 → 155,25\|26,00 fällt die Stufe in der gemeinsamen Rasterlösung von p3d16 **0,158765 m** (5,038628 → 4,879863 m) auf **0,074183 m** (4,526572 → 4,452388 m). Das Worst-Pair der neuen Lösung liegt bei 149,75\|31,25 → 150,00\|31,25 und misst ebenfalls 0,074183 m.

## Zuordnung der Abweichungen und R3-Treffer

- **Achse:** p3d16 interpoliert ein Thin-Plate-Spline-Feld durch Achs- und Ebenenstützen. Auf der Achse ist die Profilabdeckung 1; der Mischfaktor fügt dort keinen zusätzlichen Höhenfehler hinzu. Der nachfolgende Rasterfit erlaubt ±0,02 m und erreicht in p3d16 bis zu 0,020000375 m Stationsfehler. Die größere Abweichung zum neuen LP-Profil entsteht zusätzlich durch die gemeinsame Neuoptimierung der Route.
- **Bandquerprofil:** Der RBF-Wert zwischen Achsen- und Ebenenstützen wird mit dem projizierten Profil entlang des Wegbands gemischt. Der anschließende Raster-LP ließ Bandstützen mit Slack zu; p3d16 meldet maximal 0,585955 m Slack bei 155\|27. Das erklärt, warum Rand und Querprofil nicht direkt aus den machbaren Stützen übernommen werden.
- **Ring 2–4 m:** `plane_cover` läuft dort per Smoothstep in das Terrain aus. Im selben Ring wirken RBF-Querfeld und projizierte Bandstützen. Der gemessene Mesh-LP-Abstand beträgt bis zu 0,539091 m innerhalb des Wegbands.
- **R3 längs:** Das p3d16-Profil-Soll erzeugt mit dem Gate-Operator 4 D1-Abschnitte; das fertige p3d16-Mesh meldet 17 Treffer. Die neue gemeinsame LP-Profillösung erzeugt 5 D1-Gate-Abschnitte (rampe_2: 2, rampe_11: 3), bei sechs internen MILP-Abschnitten. Der enge Rasterfit am Achs-Soll ist damit ein gemessener Verstärker der p3d16-Treffer. Variante 21 muss die gemeinsamen Achsstützen direkt treffen.
- **R3 quer/Wölbung:** p3d16 meldet 22/15 D1-Treffer. Die größten Werte liegen bei rampe_2 s=24,0 m (146,4\|29,2; 30,7 %) und s=33,6 m (154,3\|28,2; 0,434 m). Diese Messungen hängen von den ±1,5-Map-Einheiten-Querproben ab und treffen damit RBF-Querprofil, Bandstützen-Slack und Ringmischung. Die neue gemeinsame Lösung liefert hier noch keinen Gate-Nachweis; das muss der Build zeigen.

Die Termzuordnung folgt den gemessenen Zwischenstützen und dem p3d16-Transfercode. Es wurde noch keine kontrafaktische Einzelterm-Abtragung gebaut; die Tabelle weist deshalb keine erfundenen Einzelterm-Anteile aus.

## Entscheidung

Die nachgerechnete Rasteruntergrenze liegt unter 0,116 m und die gemeinsame Lösung hält R3 D1 intern bei sechs Abschnitten. Der Variantenbau wird fortgesetzt. Das beweist noch nicht, dass der vollständige Build alle R3-, Endpunkt-, Bild- und Regressionstore besteht.
