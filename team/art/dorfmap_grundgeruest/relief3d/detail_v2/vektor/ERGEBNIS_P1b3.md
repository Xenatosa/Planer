# ERGEBNIS P1b3 – Ufer Q3 in beiden Messarten (Branch art/dv2-vektor-wasser-q3)

Kosten: 0 € · Codex: nein · Laufzeit: 17:43–18:05

Basis: art/dorfmap-fertig 6e1f9d5. Entscheidung Grundgerüst: „ja 0,05“. Die Geometrie aus #58 bleibt unverändert. Sie wird nur gleichmäßig auf 0,05 m abgetastet, ohne DP-Ausdünnung und ohne Nachglätten. Die Prüfung ist nicht gelockert.

## Ursache
- In #58 wurden die Linien nach dem 5-cm-Resampling noch per **1-mm-Douglas-Peucker ausgedünnt**. Dadurch sind die Stützpunkte ungleich verteilt: in Kurven dicht, auf Geraden bis 0,3 m auseinander.
- QA q3 (#55 @38fa7ec, `geom.glaettung_abw`) bildet das **ungewichtete Mittel der Stützpunkte im ±0,5-m-Fenster**. Dichte Punkte in der Kurve ziehen dieses Mittel weiter nach innen als ein Mittel über die Bogenlänge.
- Folge: 9 Funde, max 3,44 cm. Mit dem importierten q3 exakt nachvollzogen. Meine 2,65 cm aus #58 galten für die feine 0,05-m-Abtastung.

## Spline-Versuch (verworfen, kein PR)
- Vorgabe war ein glättender Spline mit r ≥ 2 m, abgetastet auf 0,25 m.
- Bei 0,25 m mittelt q3 nur 5 Stützpunkte. Ein Kreis mit r 2,0 m misst dann schon **3,11 cm**, nötig wären r ≥ ~2,1 m.
- Mit r 2,3 m (gemessen):
  - Fläche +2,96 % zu #58 (6826,52 m²) und +5,65 % zum Ist.
  - **E2 +12,26 %**.
  - **Überlappung 7,93 m²** (W02/W06 bei ~22|44).
  - **q3 noch 5 Funde**, bis 4,34 cm; Knick 18,9°.
- Abgebrochen nach Vorgabe. Nachtrag im Plan ist ergänzt (DETAIL_V2_PLAN.md, Abschnitt P1b3, „Nachtrag 17:55“, nur diese Zeile).

## Methode (neu: abtasten_gleichmaessig.py, läuft am Ende von extrahiere_wasser.py)
- Jede Linie und jeder Ring wird entlang seines #58-Polygonzugs exakt gleichmäßig abgetastet: Abstand L/n mit n = round(L/0,05).
  - Offene Linien behalten ihre Endpunkte.
  - Ringe behalten feste Ecken (Kartenrand, Knick > 20°).
- spiegel_m und breite_m werden nach Bogenlänge übertragen.
- Uferbänder: Nach dem Abtasten wird das neue Wasser abgezogen. So trägt die Bandinnenkante exakt die Wasser-Stützpunkte, ohne Sehnenkreuzung.
- Gleich behandelt: wasser.geojson, ufer.geojson (Linien und Bänder), bach_mitte.geojson.
- Der Lauf von extrahiere_wasser.py vor der Abtastung erzeugt bitgleich die #58-Dateien. Das ist geprüft: Die direkte Abtastung der #58-Dateien und der Gesamtlauf liefern identische sha256.

## Messwerte (test_wasser.py 8/8 OK)
**QA q3 importiert aus #55 @38fa7ec (nicht nachgebaut, nicht geändert), Quelle ufer.geojson: 0 Funde, abw max 2,90 cm, Knick max 4,0°.**

| Uferlinie | Stützpunkte #58 → neu | q3 #58 | q3 neu | fein (1 m Bogenlänge) | Knick |
|---|---|---|---|---|---|
| W01_U0 | 5496 → 28797 | 3,44 | **2,89** | 2,64 | 2,90° |
| W01_U1 | 279 → 1170 | 3,16 | **2,60** | 2,65 | 2,76° |
| W01_U2 | 1198 → 7247 | 1,94 | **2,01** | 1,84 | 2,70° |
| W01_U3 | 152 → 504 | 3,16 | **2,89** | 2,64 | 2,76° |
| W01_U4 | 163 → 440 | 3,33 | **2,90** | 2,65 | 3,98° |
| W02_U0 | 477 → 1298 | 3,40 | **2,89** | 2,65 | 3,74° |
| W03_U0 | 452 → 1395 | 3,16 | **2,89** | 2,64 | 2,87° |
| W04_U0 | 294 → 532 | 3,16 | **2,89** | 2,64 | 3,85° |
| W05_U0 | 164 → 301 | 3,20 | **2,88** | 2,64 | 3,85° |
| W06_U0 | 157 → 287 | 2,73 | **2,37** | 2,64 | 3,85° |
| W07_U0 | 138 → 259 | 3,12 | **2,86** | 2,62 | 3,78° |
(Werte in cm)

| Prüfung | Wert | Schwelle |
|---|---|---|
| q3-Methode (QA-Funktion) Mittellinien (23) | max 2,70 cm, Knick 3,44° | ≤ 3 cm / 15° |
| q3-Methode Wasserringe (Punkte > 1 m vom Kartenrand) | max 2,89 cm, Knick 3,94° | ≤ 3 cm / 15° |
| fein Mittellinien | max 2,47 cm | ≤ 3 cm |
| Fläche zu #58 | 6630,175 zu 6630,174 m² = **±0,00 %** | ±1 % |
| Hausdorff zu #58 | Ufer/Wasser **0,89 mm**, Mittellinien 0,61 mm, Bänder 3,45 mm | < 1 cm |
| Fläche Ist gesamt | 6630,17 zu 6461,25 m² = **+2,61 %** | ±3 % |
| Fläche Ist E2 | 105,50 zu 102,50 m² = **+2,93 %** | ±3 % |
| Fläche Ist E3 | 151,55 zu 148,25 m² = **+2,22 %** | ±3 % |
| nasse Rasterpunkte außen | max 0,27 m | ≤ 0,3 m |
| is_valid | alle Wasser- und Bandflächen | alle |
| Überlappung Gewässer | 0 m² | 0 |

Die Wasserringe haben an den Kartenecken echte 90°-Ecken (Kartenrand, kein Ufer). Die Uferlinien enden dort, q3 bewertet nur ufer.geojson.

Stützpunkte und Dateigrößen:

| Datei | Stützpunkte | Größe |
|---|---|---|
| wasser.geojson | 8 972 → 42 992 | 351 → 821 kB |
| ufer.geojson | 30 152 → 129 028 | 1,07 → 2,78 MB |
| bach_mitte.geojson | 8 840 → 20 275 | 289 → 664 kB |

## Gate (Regressionsnachweis, export_gate.sh)
- **359 / 31 / 321, W1 0 (Ansicht) und 0 (alle 56 Kacheln), Loch 0** (Lochscan gelaufen, kein G1_loch_offen, kein G1_lochscan_fehlt). „GATE ROT: kein Export/ZIP“ ist lokal normal.
- Lauf mit O17REF=/tmp/dv2_wasser/o17.json.gz: pruefe_regeln.py legt die O17-Referenz sonst unter /tmp/o18m an, den Ordner gibt es nach dem Box-Reset nicht. Prüfer und Schwellen sind unverändert.
- Toolchain /tmp/relief3d_bau_node war vorhanden.
- Vom Gate geschriebene `pruefung/*_letzter_lauf.json` wurden zurückgesetzt. p2_d2_referenz.npz ist bitgleich (d8d5d9eebb4fbba4…).
- Geändert: nur eigene Dateien in detail_v2/vektor/ plus die eine Plan-Zeile. Das Übersichtsbild ist unverändert, weil die Geometrie gleich ist.

## Hinweis
Ein voller q3-Lauf über alle Quellen zeigt viele Funde in **zonen.geojson (P1c, #57)**, bis 25 cm (u. a. an Kartenrand-Ecken). Das ist nicht meine Datei. Laut Plan werden die Zonen nach P1b3 neu erzeugt.
