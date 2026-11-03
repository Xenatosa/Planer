# Verpflichtende Regeln Dorfmap-Relief (Fabian t109u–t111u)

Pruefskript: `relief3d/pruefung/pruefe_regeln.py` (kartenweit, aus `relief_daten.json.gz`; Trefferliste mit Feld, x|z m, Wert; `LISTE=1` druckt alle).
**Pflicht-Gate:** `sh relief3d/pruefung/export_gate.sh` vor jedem Export (`dorfmap_3d_runde_*.html`), jeden Feldbau und jedes ZIP. Kein Export/ZIP, solange Treffer > 0, ausser der Treffer ist hier unter "begruendet" mit Koordinate eingetragen.

| Regel | Messung | Schwelle | Status O18k (Commit siehe runde_o_status) |
|---|---|---|---|
| R1 Wegenden nicht an Wand/Wasser/blind | Steilheit 0.5–3 m vor Ende, Wasser ≤1.5 m, Anschluss ≤2 m an anderes Wegstueck/Rand | >1.0 m/m (45°) | 9 Wand, 24 blind (Overlay-Daten, s. UEBERGABE.md) |
| R2 Abzweige verbunden | Zusammenhangskomponenten Wegmaske | 0 Nebenkomponenten | 15 |
| R3 Laengs glatt, quer eben | je 4 m: Quergefaelle ±1.5 m, Laengs-Hochpass (Gauss 2 m), Woelbung | quer >3.5 %, laengs >0.08 m, Woelb >0.08 m | 24 / 35 / 22 |
| R4 Rand / Schlucht | Gefaelle Weg→Kartenrand; Gelaende 4 m seitlich beidseitig hoeher | >15 %; >1.5 m | 4 / 13 |
| R5 Loecher/Spitzen | abflusslose Senke (Sink-Fill) auf trockenem Land; Spitzen ausser Wand | >1.0 m; >0.5 m | 49 / 4 |
| R6 Objekte auf Weg, Wasser im Schnee | Objekt in Wegzelle; Wasser mit h>10 m | 0 | 1 / 4 |
| R7 Geometrie getrennt | FW traegt Typkanal t (Wand/Boden/Weg) | vorhanden | ok |
| G1 Loecher/Durchsicht | Lochscan `loch_o18g.js` offen_innen | 0 | 0 |
| G2/G3 Spitzen oben/unten | Punkt vs. 3x3-Nachbarmittel, grob+fein, ausser Wand | >0.35 m | 156+134 / 101+168 |
| G4 Dellen/Beulen | Laplace-Ausreisser ggue. Umgebung (6x, min 0.15) | ≥4 Punkte | 0 |
| G5 Beulen an Klippenoberkante | Hochpass 2 m im 3-m-Saum oben an Wand | >0.6 m | 393 |
| G6 Facetten | Normalensprung auf 15–80 % Hang | >0.25, ≥6 Punkte | 692 |
| G7 Wandkontur echt | Wandrauheit mittel; glatte Wandflaechen | <0.40 / >40 Punkte | 0.46 ok / 1 Flaeche |
| G8 Fluesse durchgehend, eingeschnitten | Wasserkomponente erreicht Rand; Median-Einschnitt | >0.6 m | 1 nicht bis Rand |
| G9 Wasser nicht im Schnee | = R6 | 0 | 4 |
| G10 keine tiefen Loecher | = R5 | 0 | 49 |
| G11 Objekte auf Boden, nicht an Wand | |y−Boden| ; Baum auf Steilheit | >0.6 m; >0.9 | 176 / 4 |
| T1 weiche Textur-Uebergaenge | Anzeige-Farbe VC Sprung (ausser Wand), gerade Kanten | >70, ≥8 Punkte | 97 |
| T2 Textur abgeschnitten | Bildpruefung (Vollbild je Feld) | 0 | offen |
| T3 Streifen/Ringe (D1) | Bildpruefung Clay | 0 | offen |
| T4 graue Flussstreifen | Bildpruefung | 0 | offen |
| T5 Textur = Clay-Form | Bildvergleich Clay/Textur | 0 | offen |
| T6 Wasser/Schnee-Masken | helle Farbe auf Wasser | 0 | 0 |

Schwellen G5/G6/G2/G3/G11 sind Erstkalibrierung (O18k) und muessen an Bildern geprueft werden; Aenderung nur mit Begruendung hier.

## Begruendete Ausnahmen
(keine)
