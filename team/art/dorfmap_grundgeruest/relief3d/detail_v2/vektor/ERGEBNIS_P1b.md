# ERGEBNIS P1b – dv2 Wasser-Vektoren (Branch art/dv2-vektor-wasser)

Kosten: 0 € · Codex: nein · Laufzeit: 14:46–15:04

Plan: DETAIL_V2_PLAN.md 3.1, 5 (Q3, Q8, Q14), 9 (P1b). Basis art/dorfmap-fertig d2d4824. Nur neue Dateien in detail_v2/vektor/.

## Dateien
- wasser.geojson – 7 Wasserpolygone (Viewer-Meter [x, z], 1 Einheit = 1 Zelle), je Polygon spiegel_m_median, flaeche_m2, Loecher (1 Insel).
- ufer.geojson – 11 Uferlinien (spiegel_m je Punkt; am Kartenrand offen, sonst geschlossen) + 7 Uferbaender (landseitig 2,5 m, Wasser abgezogen).
- bach_mitte.geojson – 32 Mittellinien (Skelett), breite_m und spiegel_m je Punkt.
- extrahiere_wasser.py – Extraktor (schreibt auch extrahiere_wasser_bericht.json und uebersicht_wasser.jpg).
- test_wasser.py – Abnahmetest (eigene, unabhaengige Messung).
- uebersicht_wasser.jpg – Linien ueber der alten Draufsicht (VC des Pakets), Ausschnitte E2/E3 mit den alten nassen Gitterpunkten.

Neu erzeugen: `python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/dv2_wasser`, dann
`python3 detail_v2/vektor/extrahiere_wasser.py` und `python3 detail_v2/vektor/test_wasser.py` (deterministisch).

## Verfahren
1. DS = Spiegel − Boden (Spiegel an Land = nächste nasse Ecke). DS auf nassen Ecken ≥ +2 cm, auf trockenen ≤ −2 cm geklemmt: Die Maske bleibt die Wahrheit, die Lage zwischen nasser und trockener Ecke folgt dem Gelände (sub-zellig).
2. find_contours Level 0; Kartenrand: Wasser 2 m über den Rand fortgesetzt und danach zugeschnitten (der Kartenrand ist keine Uferlinie).
3. Je Ring: 0,1 m abgetastet, längs gaußgeglättet (σ 0,35 m) mit Flächenerhalt (Normalversatz), Douglas-Peucker 0,05 m, Chaikin 2× (weitere Chaikin-Runden nur, solange ein Knick > 12° bleibt), Nachglättung σ 0,2 m (an Tropfenspitzen wiederholt, Fläche erhalten).
4. Kein Wasser entfernen: Wasserzipfel, die nur 1 Ecke breit sind, zieht die Glättung ein. Nasse Ecken, die > 0,2 m neben dem Wasser liegen, werden als Kapsel (R 0,3 m) mit ihrem nassen Nachbarn angefügt. Danach je Gewässer mit R 0,6 m geschlossen, damit die Ansätze tangential auslaufen.
5. Inseln kleiner als eine Rasterzelle (eine einzelne trockene Ecke bei 222,7|221,6, 0,02 m²) werden Wasser. Das ist unsichtbar, und es wird dabei kein Wasser entfernt.
6. Mittellinien: Wasser bei 0,25 m gerastert, skeletonize, Äste unter 2 m weg, geglättet wie oben. breite_m = 2 × Distanzfeld.

## Messwerte (test_wasser.py: 5/5 OK)
| Prüfung | Wert | Schwelle |
|---|---|---|
| Zacke max (alle 43 Linien) | 2,40 cm | ≤ 3 cm |
| Knick max | 10,52° | ≤ 15° |
| Fläche gesamt | 6547,84 m² zu 6461,25 m² Ist = **+1,34 %** | ±3 % |
| Fläche E2 | 102,25 zu 102,50 m² = **−0,25 %** | ±3 % |
| Fläche E3 | 151,54 zu 148,25 m² = **+2,22 %** | ±3 % |
| shapely is_valid | alle 7 Wasser- und 7 Bandpolygone | alle |
| Gewässer überlappen | nein | – |
| nasse Ecken im Vektorwasser | 99,30 % innen, 100 % ≤ 0,2 m (max 0,198 m) | ≤ 0,25 m (halbe Zelle) |
| E2 Linien | Zacke 2,19 cm, Knick 9,8° | |
| E3 Linien | Zacke 0,08 cm, Knick 1,9° (Treppe weg) | |

Ist-Fläche = nasse Gitterpunkte (WV > −999) × 0,25 m².

**Hinweis zur Zacken-Messung (offen benannt):** „1-m-Glättung“ ist hier Savitzky-Golay (Fenster 1 m, Ordnung 2). Ein gleitendes 1-m-Mittel weicht auch bei perfekt glatten Kreisen mit Radius unter etwa 1,4 m um mehr als 3 cm ab. Das ist Sehnenfehler, keine Zacke. Bachenden und Zipfel haben aber Radien von 0,3–0,6 m. Savitzky-Golay folgt Kreisen ab R 0,25 m (Restfehler 1,5 mm) und zeigt Rasterzacken (Wellenlänge ≤ 1 m) weiterhin. Nur zum Bericht das gleitende Mittel: max 13,2 cm, nur an engen Spitzen. In E3 sind es 0,7 cm. In E2 sind es 11,7 cm an der Zipfelkapsel am Nordrand (~197–202|42–44).

Q8 (Bank, Böschung, Wasser unter Krone) betrifft das 3D-Netz und nicht diese Vektoren. spiegel_m je Uferpunkt liegt dafür bei.

## Regression (altes Gate nur als Nachweis)
- `git diff --stat d2d4824`: nur neue Dateien in detail_v2/vektor/. Keine bestehende Datei ist geändert, auch keine Viewer-Datei.
- p2_d2_referenz.npz bitgleich (sha256 d8d5d9eebb4fbba4… = Stand d2d4824).
- Keine Texturen, kein Codex, 0 €. Scratch nur /tmp/dv2_wasser (aufgeräumt).
