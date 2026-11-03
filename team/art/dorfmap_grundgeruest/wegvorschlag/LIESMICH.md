# Wegvorschlag O18l-C (t112u) – nur Vorschau, Overlay unveraendert, nichts versendet
`python3 wegvorschlag.py ../relief3d/relief_daten.json.gz` (deterministisch) → `wegvorschlag.json`, `feld_XX.png` (Draufsicht 12 px/m: rot = bestehende Wege/Rampen, gruen = vorgeschlagene Anschluesse, blau Wasser, dunkel = Wand >0.45).
Kostenweg: Gelaende-Neigung ≤0.25 normal, 0.25–0.45 teuer, >0.45 gesperrt; Wasser = Bruecke.
Ergebnis: 24 von 26 Rampenenden + 4 Dorfweg-Inseln angeschlossen. Offen: rampe_4 (H6/G6) liegt beidseitig in einer Wandtasche, kein Anschluss ohne Wand → Rampe muss neu trassiert werden. Wege mit `max_steigung` >0.25 brauchen Serpentine/Treppe; `anteil_auf_eigener_rampe` >0.5 heisst: die Rampe selbst ist der Weg ins Freie, das Ende muss verlaengert/umgelegt werden.
