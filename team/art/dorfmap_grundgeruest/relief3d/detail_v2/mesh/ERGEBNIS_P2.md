# Ergebnis P2-C (C2c) – Terrain-Mesh detail_v2

**Status: teilweise, Abbruch nach wiederholtem E2-Fehler.** Branch `art/dv2-mesh`, Basis `57a79f4`. Es wurden nur D3, E3 und E2 exportiert; 53 Kacheln fehlen. Das Manifest ist ausdrücklich ein 3-Kachel-Pilot und keine lieferfertige Gesamtkarte.

## Methodenverlauf

| Ansatz | Messung / Ergebnis | Entscheidung |
|---|---|---|
| C2 – SciPy Delaunay | Die Quelllinien waren nicht zuverlässig als Mesh-Kantenzüge enthalten; die Zahlen des abgebrochenen Laufs sind im damaligen Ergebnisprotokoll nicht vollständig erhalten. | Abgelöst. |
| C2b – 0,25-m-Gitter mit Snapping | 56 Kacheln gebaut. Q3: Abweichung 0,257 m, Knick 173,8°. Q8: Spalt 4,07 cm bei 18.843 Punkten, Überlappung 4,10 m, p95 0,225 m. Q9: 8 entartet, 8 Normalen unten, Winkelminimum 0°, 474 Winkel <20°, 302.273 zu lange Kanten. Q7: dh max 3e-5 m; Q14: Wegefehlend 0, Hausdorff 0,249 m. | Verworfen; Snapshot liegt unter `/workspace/codex_jobs/c2b_snapshot/`. |
| C2c – Shewchuk Triangle CDT, lokale PSLG je Kachel | D3 q30: 28.824 Dreiecke; E3 q30: 31.566. E2 q30 endete in zwei getrennten Läufen mit Speichermangel. E2 q28 exportierte 140.364 Dreiecke, q25 119.888. | Nach q25 keine weiteren Triangulierungsversuche gemäß Abbruchregel. E2 liegt 59.888 Dreiecke über dem Tile-Limit. |

## Pilot-QA

QA `ec77356` lief gegen das partielle Manifest. Die vollständige angeforderte Runde wurde beim Q10-Lauf vom System beendet (Exit 137); eine zweite Runde mit Q3/Q8/Q9/Q14 erreichte Q3 und Q8, Q9 lief noch beim Ablauf der 14:15-Frist. Zahlen aus den abgeschlossenen Läufen:

| Regel | Status / Messung | Einordnung |
|---|---|---|
| Q1 | Fehler: 6.697 Kanten mit >2 Dreiecken, 9.670 innere Randkanten, 1 abweichende Naht (3-Kachel-Runde). | Unvollständiger Ausschnitt; keine geschlossene Gesamtfläche. |
| Q2 | Fehler: Hausdorff max 9,99 m. | Durch fehlende Kacheln nicht abnahmefähig. |
| Q3 | Fehler: Mesh-Abweichung max 0,3472 m, Knick max 121,3546°; 39 Mesh-Kantenzüge (3-Kachel-Runde). Vektor max 0,03 m / 9,3663°. | Auch im Pilot nicht grün. Diagonale Weg-/Uferabschnitte wurden nicht separat ausgewertet. |
| Q4 | Fehler: Gefälle max 0,9394, Höhenrest max 13,2097 m. | Pilot deckt Kreuzungen/Plätze nicht vollständig. |
| Q5 | Fehler: 10 Kandidaten, Tiefe max 8,1741 m. | Pilotmesh ist nicht flächendeckend. |
| Q6 | Fehler: 0 Stationen. | Keine auswertbare vollständige Wegabdeckung. |
| Q7 | Fehler: 7.383/7.395 Altvertices nicht abgedeckt; dh max 0 m an den 12 abgedeckten Punkten. | D2-Kachel fehlt im Pilot. |
| Q8 | Fehler: 11 Uferlinien; 0 Spaltpunkte, Spalt max 0 m, Überlappung max 0 m; 115 Stationen ohne Schnitt, 20.963 ohne Spiegel; Ufer-Kontur max 9,99 m (2-Kachel-Runde). | Die Nullwerte sind kein positives Gate: Das Gelände ist unvollständig. |
| Q9 | Fehler (3-Kachel-Runde): 223.250 Dreiecke inkl. Wassermodelle; max Tile 119.888; 49.423 Normalen unten, 75.873 entartete Dreiecke, 1 zu lange Kante, Minimum 0°, 25.144 Winkel <20°. | Budgetüberschreitung E2; Winkel- und Degenerationsfehler. |
| Q10 | Fehler im abgeschlossenen D3/E3-Lauf: 111 gespiegelte UV0, 117 UV1-Flips, max UV0-Verzerrung 111,5833 %, 3.070 Wegband-Dreiecke >10 % UV2-Abweichung. | E2-Q10 nicht vollständig ausgewertet; Gesamt-QA beim Q10-Lauf wegen Exit 137 beendet. |
| Q14 | Im ersten D3/E3-Pilotlauf: ok, Wegefehlend 0, Hausdorff max 0,249 m. | E2 war in diesem QA-Lauf noch nicht enthalten. |

## Export, Grenzen und offene Punkte

- Im Manifest stehen D3 (28.824), E2 (119.888) und E3 (31.566) sowie sieben Wassermodelle. Terrain-Dreiecke: **180.278**; die 1,6-Mio.-Gesamtgrenze ist damit nicht das Problem. Das E2-Tile-Limit von 60.000 ist um 59.888 überschritten.
- Die Clay-Bilder zeigen die ungeschönte, lückenhafte Pilotgeometrie. Die Bodenabfrage an den gewählten Kamerastandpunkten lieferte `null`; die Ansichten sind daher kein Sichtnachweis für eine fertige Oberfläche.
- Ursache für den Abbruch: E2s dichtes/nodiertes Constraint-Netz lässt q30 zweimal den verfügbaren Speicher ausschöpfen; q28 und q25 bleiben trotz Abschluss über dem Tile-Budget. Die vorgeschriebenen Winkel-Fallbacks sind ausgeschöpft. Es wurde kein Vollausbau begonnen.
- Die geforderte separate Q3-Auswertung diagonaler Weg-/Ufersegmente fehlt. D2, vollständige Wasserbett-/Uferabdeckung, Wegprofile, Klassenbelegung und 53 Kacheln bleiben offen.
- Brückenbohlen, Geländer, Auflager und Brückenringe bleiben P5. Fels-/Begehbarkeitsabweichungen wurden nicht vollständig ausgewertet.
- `triangle` / Shewchuk Triangle war nur lokales Build-Werkzeug und ist nicht Teil des Spiels. **Offener Punkt für Fabian:** Triangle ist nicht-kommerziell weitergebbar; Lizenz- und Weitergabebedingungen vor einer kommerziellen Nutzung prüfen.
- Clay: acht JPGs, Qualität 90, unter `/workspace/dorfmap_final/detail_v2/tag2_clay/`, erzeugt von `render_c2c_clay.js` aus den exportierten GLBs.
- Kosten: **0 EUR**. Laufzeit: **20.11.2026, ca. 12:15–14:14 Europe/Berlin**.

## Liefergrenze

Kein Merge. Der Commit enthält ausschließlich den C2c-Pilot, QA-Berichtsdaten, Render-Skript und die drei erzeugten Kacheln. Er ist nicht als Gesamtmesh verwendbar.
