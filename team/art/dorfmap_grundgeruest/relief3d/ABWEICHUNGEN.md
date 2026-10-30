# Relief t41u – Messungen, Annahmen, Abweichungen

## Messungen [S]/[R]
- Wandhöhe = Bandbreite px / 25 [R]: Nord 14 m, Suedgrat 16 m, Krater 11 m, Ostgrat 12 m (vorher 8,6/7,6/7,7/6,7 m).
- Sichtbarer Fels Nordwand ca. 230 px [S], Band 350 px → Perspektivfaktor k ≈ 1,5 [R].
- See 38×35 Zellen → Boden fast von oben gezeichnet; Spanne 9 m (k=1) bis 22 m (67°) [R]. Gewählt: Mitte [A].
- Details: pruefung/klippen_messung_t40u.csv.

## Annahmen [A]
- HANG/SIMS skaliert: positiv ×1,7, negativ ×16/7,6.
- Kraterboden 1 m, Gipfel 14 m, Flussbett 1,5 m, See 3 m tief, Wasserspiegel Boden −0,3 m.
- Sprung > 2,5 m = Felswand, kleiner = Böschung. Sockel bis −30 m.
- Suedgrat + unbenannte Bänder: Höhe per Nachbar-Propagation (Median Suedgrat 14,1 statt gemessen 16).

## Abweichungen von c20 [F]
- Wand steht am Bandfuß; Bandzellen gehören zur oberen Ebene (18752 Zellen umgedeutet).
- Krater-Außenhang senkrecht.
- Zellraster sichtbar: 1-m-Treppen im Grundriss, Wasser als flache Stufen, keine Überhänge.
- E40: 112 Stellen außerhalb der Senke (alter Hinweis, nicht korrigiert).

## t42u – Glättung + c20-Textur
- Höhenfeld G auf 0,5-m-Gitter (673×607 Punkte) [R]: Hänge Gauß σ 1,5 m [A]; an Sprüngen > 2,5 m steile Wand per Smoothstep, Kontur mit Rauschen ±~0,4 m [A].
- Dreieck steiler 55° = Wand (Wandtextur 4×8 m, Box-Projektion), sonst Boden mit c20-Draufsicht [A].
- Bodentextur textur_relief_t42u.jpg: c20 (8 px/Zelle), gemaltes Wandband + Schatten (20524 Zellen) mit Farbe der eigenen Ebene aufgefüllt (unscharf) [A]. c20 unverändert.
- Wandhöhe im Modell (max−min G im 5×5-Fenster an steilen Zellen, Median) [R]: Nord 15,45, Suedgrat 15,0, Krater 11,2, Ostgrat 12,0 m. Nord inkl. Hang am Fuß; Suedgrat 1 m unter Messung 16 (Bandhöhe per Nachbar-Ausbreitung).
- Zellen: hoehe_m = Mittel 3×3 G-Punkte, ecke_* = G, klippe WAND/WAND_OBEN/WAND_FUSS, skin_slot wand_fels bei WAND. Abgleich pruefung/abgleich_t42u.json: 0 Abweichungen.
- OBJ entfällt (nur GLB); alter Stand: ../_alt/relief3d_t41u/.

## t43u
- Suedgrat [R]: Talboden TAL_SUED/untere Bandzellen bis 15 Zellen vom Band um bis zu 16,8 m unter Oberkante abgesenkt, Median klippe_hoehe 16,04 m. 11150 Zellen (Reihen 218–276) mit neuen Hoehenwerten, sonst unveraendert. pruefe_t42u: 0 Abweichungen.
- Bodenfarbe: Material-Gewichte (untergrund, Nass am Wasser, Geroell am Wandfuss) je Vertex, c20 nur 12 % Toenung [A]. Fels per Neigung (smoothstep 0,42–0,74 cos) triplanar [A].
- Bekannte Maengel: Waende wirken noch wie gestempelt (Textur gleichmaessig), Schneeboden flach/eintoenig, Wege-Overlay sehr blass, Haeuser/Baeume sind Platzhalter, Kamera "Am Nordwand-Fuss" hat einen Felsen direkt vor der Linse.
