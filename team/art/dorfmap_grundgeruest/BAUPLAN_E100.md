# BAUPLAN_E100 – Platzbedarf bis Epoche 100 (t14u)

Quellen: `team/gdd/uebernahme_2026-10-28/GEBAEUDE_SLOTS_GUELTIG.md` (gültig, 29.10.) §1/§3, `groessen_25_slots.csv` (Maße, durchgehend „Annahme“), F2-Abstand (4 m, 6 m bei Großbauten).
Marker: [S] Quelle, [A] Annahme/Hochrechnung, [R] berechnet, [F] Fabian.

## 1 Funktionsgebäude je Epoche (jedes Slot genau 1×, Ausbau über 55 Stufen auf demselben Platz)

| Epoche | Gebäudezahl kumuliert | Quelle/Marker |
|---|---|---|
| E1–E8 | 25 (Slots 1–25, inkl. Palisade als Ring) | [S] GÜLTIG §1 |
| E9–E16 | 25 | [S] |
| E17 | 26 (+Glashütte) | [S] |
| E21 | 27 (+Saline) | [S] |
| E24 | 28 (+Pigment) | [S] |
| E25–E50 | 28 | [S] |
| E51 | 29 (+Module) | [S] |
| E53–E100 | 30 (+Äther-Destille) | [S] |

Maße: E12–E16-Werte aus groessen_25_slots.csv [A]. Für E17–E100 gibt es keine Maße; ich nehme an, dass sie nicht weiter wachsen [A]. Slots 26–30 erhalten das Maß eines verwandten Slots [A]: Glashütte→Faser, Saline→Lehm, Pigment→Zeichenfels, Module→Metall, Äther→Köhler.

## 2 Deko bei E100

| Art | Anzahl | Platz | Marker |
|---|---|---|---|
| Deko-Häuser | 18 (Deckel der 13d-Formel) | 9,6×7,2 m | [A] |
| Flur-/Weg-Deko | 2+E/2 → 52 | 3×3 m | [A] Hochrechnung über E16 hinaus |
| Anbau-Deko | 3–4 gleichzeitig | am Slot, kein eigener Platz | [A] |

## 3 Abgleich mit den 99 Plätzen [R]

- **Bedarf an eigenen Plätzen:** 99 = 29 Funktionsplätze (ohne Palisade) + 18 Deko-Häuser + 52 Flur-Deko.
- **Was in die 99 passt:**
  - Alle 52 Flur-Deko-Stücke.
  - 6 Funktionsgebäude.
  - Danach bleiben 41 kleine Bestandsplätze leer.
- **Was nicht passt:**
  - 23 Funktionsgebäude und alle 18 Deko-Häuser.
  - Grund: Die Bestandsplätze sind meist 4×4 bis 10×8 m groß. Die E12-Maße reichen bis 20×20 m (Arena) und 17×17 m (Zentrum).
- **Neue Standorte in `overlay_plaetze_erweiterung.*` mit 4/6 m Abstand:**
  - 26 Standorte gesetzt (19 Funktion + 7 Deko-Haus).
  - Ringe um das Feuer, je 40 m breit: Ring 1: 8, Ring 2: 3, Ring 3: 3, Ring 4: 12.
  - **15 Plätze lassen sich nicht unterbringen** (11 Deko-Häuser, Hütte, Zeichenfels, Glashütte, Pigment).
  - Mit 2/4 m Abstand passen alle 41 (Variante gerechnet, nicht übernommen).
- **Flächen:**
  - Frei nutzbar: 19 277 m² (bebaubar, in der Senke, ohne Bestand, Wege, Hof, Feuer und Brücken).
  - Neuer Bedarf: 4 143 m².
  - Es fehlt also nicht an Fläche, sondern an zusammenhängenden Rechtecken, sobald der Abstand gilt.

## 4 Was Game Designer/Producer noch liefern müssen

1. Maße der Slots ab E17 (wachsen sie weiter?) und Footprints der Slots 26–30.
2. Eine verbindliche Deko-Häuserzahl für E17–E100. Der Deckel 18 ist [A].
3. Die Flur-Deko-Regel nach E16 und die Maße für klein/mittel.
4. Die Zuordnung Slot→Platz (welches Gebäude steht wo) und die Freigabe, ob große Gebäude Bestandsplätze zusammenlegen dürfen.
5. Den Abstand: F2 mit 4/6 m oder ein kleinerer Wert für Deko.
6. Bilder für 13 Slots (laut GÜLTIG).
