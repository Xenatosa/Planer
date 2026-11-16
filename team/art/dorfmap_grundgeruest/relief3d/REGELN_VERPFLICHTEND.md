
### R8a Wegende / Wegabschluss (verbindlich ab t122u)
- Jedes Wegende (Rampe, Dorfweg, Abzweig) laeuft mit weichem Auslauf ueber >=4 m in Gelaende, Wand, Kreuzung oder Platz.
- Kein Absatz >0,10 m am Wegende (Nachbarpunkt 0,25 m), Bandrand-Uebergang stufenfrei; Band springt nicht aus Schnee/Gelaende.
- Gate kartenweit: R8_ende (Liste je Feld). Nahbilder vorher/nachher Pflicht (G1).

### R8b Delle neben Wegen (verbindlich ab t122u)
- Lokales Minimum, das >0,30 m tiefer liegt als sein Rand, innerhalb 6 m neben Weg/Kreuzung und nicht auf Fels/Wand = Treffer R8_delle.
- Ursache je Delle per Zahl benennen; G1-Delle (unter Plateaukante) beheben.

### W1 Wandkoerper am Gelaende (verbindlich ab P10d, nur Verschaerfung)
Prueft die gerenderten Wandkoerper (`neu/wand.py`) gegen das gerenderte Gelaende-Mesh, Skript `pruefung/w1_wand.py`
(Gate-Aufruf in `export_gate.sh`, Ergebnis `pruefung/w1_letzter_lauf.json`). Ein Treffer = eine Zelle je Teilpruefung und Kachel.
- W1a: Wandvertex ausserhalb der Karte (x 0–336, z 0–303 Zellen). Schwelle 0 (hart): Geometrie ausserhalb der Karte ist nie richtig.
- W1b: Wandvertex > **0,5 m [A]** ueber der lokalen Gelaendekrone (hoechster Gelaendepunkt im Kreis **1,5 Zellen [A]**).
  Begruendung: Die Wand bildet eine Gelaendestufe nach und darf nicht frei darueber stehen; 0,5 m liegt deutlich ueber der
  Einbettung (Oberkante = Krone − 0,15 m) und der Kappenrundung (≤ 0,12 m), ist aber kleiner als jede sichtbare Mauer
  (≥ 1 m auf Nahbildern). 1,5 Zellen = halbe Wandbreite (0,5) + 1 Zelle Rand fuer Kappenrundung und Interpolation.
- W1c: Unterkante (tiefster Vertex je x|z-Saeule) > **0,5 m [A]** ueber dem Gelaende direkt darunter = schwebend.
  Begruendung: Der Fuss ist auf Gelaende − 0,15 m gebunden; 0,5 m ist auf Nahbildern als Spalt unter der Wand sichtbar.
- W1d: Wandlinie > **1 Zelle [A]** von ihren Quellzellen (`vektor.json waende[].quellzellen`); geprueft je Vertex gegen
  das naechste Quellzellen-Quadrat mit Grenze 1 + halbe Wandbreite (+0,02 Kappenzugabe). Begruendung: Die Mittellinie
  liegt per Bau in den Quellzellen (Median 0,23 Zellen); mehr als 1 Zelle heisst Einheiten-/Lagefehler (vor P10c 53 Zellen).
- Positivkontrolle: Stand 7944b33 (vor P10c) ergibt W1b 140 / W1d 461 Treffer.

Das vollständige, messbare Formregelwerk für alle Landschaftselemente mit Sollmaßen, Ist-Verteilungen und der Kachelmatrix A1–H7 steht in [REGELWERK_LANDSCHAFT_VOLLSTAENDIG.md](../REGELWERK_LANDSCHAFT_VOLLSTAENDIG.md).
