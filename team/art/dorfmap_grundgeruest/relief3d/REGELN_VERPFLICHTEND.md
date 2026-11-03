
## O18s Regression-Basis und G6-Ursache (pruefung/o18/regression_o18s.json)
- Basis: Gate 1055, t42u 0, bergauf 0 (max 0,02), Bandrand-Stufe 0, Loecher 0 (Index und 56 Felder), lod1 1 175 138 Dreiecke, Ladezeit Median 9,0 s.
- Raycast ist auf der Basis ROT (Baeume 20 schwebend/105 versunken). Ursache: Block O18m G11 setzt Objekte auf G_ANZ statt auf das sichtbare Feinnetz. Fix (Raycast-Cache hat Vorrang) macht Raycast gruen, aber Gate G11 +162, weil G11 gegen G_ANZ misst -> nicht uebernommen. Messflaeche von G11 und G6 muss auf die Anzeige-Flaeche umgestellt werden (Entscheidung offen).
- G6: Ursache ist die Wandformung Gs (Rippen-fBm RIB, Simse, Schuttfuss) im Grobnetz, nicht Zellraster/Bilinear. Bikubisch statt bilinear verschlechtert G6 (492->521).

## O18t Messkorrektur G6/G11: sichtbare Flaeche
- Grund: Im Feinband rendert der Viewer das Feinnetz (FW, 0,25 m), die Grobquads werden dort ausgelassen. Das Gate hat G6 und G11 auf dem Grobnetz GB gemessen, also teils auf einer unsichtbaren Flaeche. Dadurch widersprachen sich Raycast (gegen das sichtbare Netz) und G11.
- Neu: G6 auf GV = Feinnetz (jeder 2. Feinpunkt, 0,5 m) wo vorhanden, sonst GB; G11 gegen bilineare Feinnetz-Hoehe wo alle 4 Ecken vorhanden, sonst GB. Schwellen unveraendert. Alte Messung: GATE_GROB=1.
- Zahlen gleicher Stand (6e7dfff): G6 alt 592 -> sichtbar 676; G11 alt 0 -> sichtbar 107; Gesamt 1055 -> 1246. Alle anderen Regeln gleich. Neue Basis fuer Vergleiche: 1246.
