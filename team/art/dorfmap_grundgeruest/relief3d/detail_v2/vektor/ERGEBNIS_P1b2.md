# ERGEBNIS P1b2 – Uferlinien ausrunden (Branch art/dv2-vektor-wasser2)

Kosten: 0 € · Codex: nein · Laufzeit: 15:48–15:58

Basis: art/dorfmap-fertig 8a38922 (#54 P1b ist dort schon gemergt, #56 P1a ebenso). Anlass: QA misst Q3 einheitlich mit dem
**gleitenden 1-m-Mittel**; die SG-Freigabe aus P1b ist zurückgezogen. Geändert sind nur eigene Dateien in detail_v2/vektor/:
wasser/ufer/bach_mitte.geojson, extrahiere_wasser.py, extrahiere_wasser_bericht.json, test_wasser.py, uebersicht_wasser.jpg, dieses ERGEBNIS.

## Ursache und Methode
Ein Kreis mit Radius R weicht vom gleitenden 1-m-Mittel um ≈ 1/(24·R) ab: bei R 1,5 m 2,8 cm, bei R 1,6 m 2,6 cm. In P1b hatten Bachenden, Tropfenspitzen und Zipfel Radien von 0,3–0,6 m. Daher 6,6–13,6 cm.
Neu (Funktion `ausrunden()`): je Gewässer Krümmungsradius **≥ 1,6 m** (Reserve zu 1,5 m). Wasser wird nur hinzugefügt, das Original bleibt Teilmenge (Union):
1. **Konkave Engstellen** (Buchten, Innenkurven): morphologisches Schließen Buffer(+1,6)·Buffer(−1,6), je Gewässer einzeln. Global würden Teiche mit verschiedenem Spiegel verschmelzen.
2. **Konvexe Engstellen** (Bachenden, Spitzen; Umkreisradius über ±0,5 m < 1,7 m): ein Kreis R 1,6 m, der die Stelle sicher enthält. Die Mittelpunktsrichtung wird ±75° um die Innennormale gewählt, nach der kleinsten überdeckten Landfläche.
   - Erster Versuch (Kreis symmetrisch tangential): Er ragte am schrägen Bachkopf E2-Nordrand weit übers Gegenufer, das Schließen füllte die Ecke. Ergebnis E2 +3,9 % und eine Überlappung zweier Teiche (0,31 m²). Daher wurde die Methode gewechselt, statt zu flicken.
3. **Nasse Rasterpunkte > 0,27 m außerhalb** (1 Punkt breite Zipfel): kleinste runde Beule R 1,6 m, die den Punkt bis 0,25 m erreicht. Ersetzt die 0,3-m-Kapseln aus P1b, die selbst Spitzen erzeugten.
4. Danach Resampling 5 cm. Uferbänder (2,5 m landseitig) und Mittellinien (Skelett, breite_m, spiegel_m) werden aus den neuen Polygonen neu abgeleitet. Mittellinien werden längs geglättet, bis gleitendes Mittel ≤ 2,5 cm.

Schmale Bäche verschwinden nicht, weil das Original per Union erhalten bleibt. Die Flächenzunahme bleibt unter 3 %.

## Messwerte (test_wasser.py 5/5 OK, Messung = gleitendes 1-m-Mittel über Bogenlänge, Trapezgewichte)
| Uferlinie | Zacke (gleitendes Mittel) | Knick |
|---|---|---|
| W01_U0 | 2,65 cm | 3,80° |
| W01_U1 | 2,65 cm | 3,69° |
| W01_U2 | 1,84 cm | 3,80° |
| W01_U3 | 2,64 cm | 3,74° |
| W01_U4 | 2,65 cm | 3,75° |
| W02_U0 | 2,64 cm | 3,73° |
| W03_U0 | 2,64 cm | 4,01° |
| W04_U0 | 2,64 cm | 3,76° |
| W05_U0 | 2,64 cm | 3,86° |
| W06_U0 | 2,64 cm | 3,87° |
| W07_U0 | 2,62 cm | 3,74° |

| Prüfung | Wert | Schwelle |
|---|---|---|
| Uferlinien max Zacke | 2,65 cm (zum Vergleich mit 21 gleichgewichteten Punkten: 2,89 cm) | ≤ 3 cm |
| Mittellinien (23) max Zacke | 2,47 cm (gleichgewichtet 2,70 cm) | ≤ 3 cm |
| Knick max (alle Linien) | 4,01° | ≤ 15° |
| Fläche gesamt | 6630,17 zu 6461,25 m² = **+2,61 %** | ±3 % |
| Fläche E2 | 105,50 zu 102,50 m² = **+2,93 %** | ±3 % |
| Fläche E3 | 151,55 zu 148,25 m² = **+2,22 %** | ±3 % |
| max Abstand nasser Rasterpunkt außerhalb | 0,27 m (99,31 % liegen innen) | ≤ 0,3 m |
| is_valid | alle 7 Wasser- und 7 Bandpolygone | alle |
| Überlappung von Gewässern | 0 m² | 0 |
| SG-Zacke (nur Info) | 1,12 cm | – |
| E2-Nordrand ~191–207/37–51 | vorher 12,0 cm, nachher 2,64 cm | ≤ 3 cm |

Bestand: 7 Polygone, 11 Uferlinien, 7 Uferbänder, 23 Mittellinien. Gegenüber P1b sind 90,7 m² hinzugekommen. 8,4 m² der alten P1b-Kapseln sind entfallen; deren nasse Rasterpunkte liegen trotzdem ≤ 0,27 m vom Wasser.
Knappste Reserve: E2 mit +2,93 %, verursacht durch den runden Bachkopf am Nordrand.

## Bild
uebersicht_wasser.jpg: Gesamt, E2, E3 und das Nahbild des E2-Nordrands vorher (grün gestrichelt, P1b) und nachher (rot) über der alten Draufsicht.
Erzeugen: `python3 detail_v2/vektor/extrahiere_wasser.py --vorher <altes ufer.geojson>` (Paket aus `pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/dv2_wasser`).

## Regression
- `git diff --stat origin/art/dorfmap-fertig`: nur die eigenen Dateien oben. Keine Viewer-Datei und keine P1a-/P1c-Datei angefasst.
- p2_d2_referenz.npz bitgleich (sha256 d8d5d9eebb4fbba4…). Keine Texturen, kein Codex, 0 €. Scratch /tmp/dv2_wasser aufgeräumt.
