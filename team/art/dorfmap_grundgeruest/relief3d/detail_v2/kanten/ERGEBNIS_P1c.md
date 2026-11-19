# Ergebnis P1c – Grat-, Klippen- und Zonenvektoren

**Stand:** 19.11.2026 · Branch `art/dv2-vektor-kanten` · Basis `d2d48248bda33e8d78c86f8e4afb6f1e70934e9e`

Kosten: 0 EUR · Laufzeit Start 19.11.2026 14:48, Ende 19.11.2026 15:31 (Europe/Berlin)

## Gelieferte Dateien

- `../vektor/kanten.geojson` – 57 Linien: 13 `klippe_oben`, 17 `klippe_unten`, 27 `steil55`.
- `../vektor/grat.geojson` – 30 Linien: 2 `G3H3`, 1 `B3C3`, 20 `Ostgrat`, 7 `Kraterring_G1`.
- `../vektor/zonen.geojson` – 256 Flächentyp-Polygone, 10 Bauzonen-Polygone und 859 Slot-Features (233 Bau-, 626 Deko; darin 136 Erweiterungsplätze als Punkte).
- Skript, Test und Bildskript liegen in diesem Ordner. GeoJSON-Linien führen ihre GB-Höhen je Stützpunkt als `hoehen_m`; Zonenflächen tragen `untergrund` und `untergrund_anteile`.

## Koordinaten und Verfahren

- [S] `neu.mesh.tile_mesh()` setzt Viewer-X/Z auf Rasterindex geteilt durch `rs`; `GB` hat `rs=2` und 673×607 Werte für 336×303 m. Die Viewer-Gitterpunkte liegen auf `x=0…336`, `z=0…303`. Der Extraktor liest `GB` aus `relief_daten.json.gz`, das auch `index.html` speist.
- [A] Eine CSV-Zelle `(cx,cy)` belegt `[cx,cx+1]×[cy,cy+1]`; ihr Mittelpunkt ist `(cx+0,5, cy+0,5)`. GeoJSON verwendet `[x,z]` in Metern und lässt Höhe als eigene Property stehen. Die drei Fabian-Anker werden unverändert an ihren vorgegebenen Viewer-Koordinaten gehalten.
- Klippen: Konturen der Zellmasken `KLIPPE_WAND/KANTE`, DP 0,1 m, Catmull-Rom und gleichmäßige Ausgabe ≤0,1 m. Die Quellspalte `klippe` enthält im aktuellen Stand nur `WAND`/`KANTE`; Ober-/Unterkante wurden deshalb anhand der GB-Höhenlage relativ zum Median des jeweiligen `wand_name` abgeleitet. Fünf kurze Konturen unter 3 m wurden ausgelassen.
- Steilheit: Neigung aus GB bei 0,5-m-Abstand, geglättetes Neigungsfeld, direkte 55°-Isolinien, danach DP/Catmull-Rom. Die Höhenwerte werden bikubisch interpoliert und auf die umgebenden 2×2 GB-Werte begrenzt.
- Grate: Hessian-Eigenrichtungen, Ridge-Maske, Skelett und Polylinien. Es entstanden 692 Skelettpfade, davon 298 Kandidaten für benannte Gratbereiche. [F] Die drei Pflichtstellen sind enthalten. Die Ankerlinien laufen als lokale Hessian-Tangentenspuren; der nächste rohe Ridge-/Klippenpfad liegt dazu 1,50 m, 3,54 m und 3,35 m entfernt. Das ist eine explizite Anpassung an die Pflichtkoordinaten, keine Messung, dass dort bereits ein natürlicher Kronenridge verläuft.
- Zonen: Zellklassen nach Wasser > Brücke > Weg > Ufer > Fels > Grund; `coverage_simplify`, gemeinsame Liniengeometrie, Catmull-Rom und Polygonisierung. 90 isolierte 1–3-Zell-Specks aus den Klassen Grund/Fels wurden vor dem Glätten der Nachbarklasse zugeordnet [A]. Bau-/Deko-Slots kommen aus dem Overlay; Erweiterungsplätze aus `overlay_plaetze_erweiterung.json` sind Punkte mit Stand/ID.

## Messwerte

### Q3 Glättung

Die Abweichung ist die maximale Distanz zur gleitenden 1-m-Mittelung der ausgegebenen Linie bzw. Polygonringe. Knicke zählen alle inneren Segmentwinkel über 15°; für Zonen sind echte Tripunkt-/Kartenecken zusätzlich gezählt, aber nicht von der Roh-Maximalzahl abgezogen.

| Datei | max. Abweichung | max. Knick | Knicke >15° | Ergebnis |
|---|---:|---:|---:|---|
| `kanten.geojson` | 0,211 m | 69,40° | 169 | **Q3 verfehlt** |
| `grat.geojson` | 0,166 m | 37,45° | 3 | **Q3 verfehlt** |
| Zonen-Flächentypen | 0,254 m | 152,33° | 1 423 roh | **Q3 verfehlt** |

Bei den Zonen wurden 238 Tripunkt-Koordinaten sowie 4 Kartenecken gefunden. 657 der Winkel über 15° liegen an diesen Ecken; 766 bleiben außerhalb davon. Die drei Q3-Messwerte liegen über den Grenzwerten 0,03 m/15°. `test_kanten.py` markiert diesen Abnahmepunkt deshalb als `xfail`; er ist nicht bestanden.

### Flächen und Pflichtstellen

| Flächentyp | GeoJSON-Fläche | Quellzellen | Abweichung |
|---|---:|---:|---:|
| Grund | 68 791,91 m² | 68 491 | +0,44 % |
| Weg | 2 813,67 m² | 2 825 | −0,40 % |
| Ufer | 2 759,21 m² | 2 902 | −4,92 % |
| Fels/Klippe | 20 699,63 m² | 20 875 | −0,84 % |
| Wasser | 6 732,23 m² | 6 695 | +0,56 % |
| Brücke | 11,35 m² | 20 | −43,25 % |

- Bauzone: CSV-Zählung 31 893 Zellen; GeoJSON 31 893,000006 m²; Abweichung <0,0001 %. Die Plan-Referenz im Plantext nennt 31 927; die aktuelle Quell-CSV enthält 31 893.
- Pflichtstellen: `300|90` → 0,00 m; `290|98` → 0,00 m; `84|129` → 0,00 m.
- Flächentyp-Deckung: 256 gültige Polygone, paarweise keine Überlappung; Union ist exakt `0..336 × 0..303` (Flächenfehler 0 m²). Alle Polygongeometrien sind gültig.

### Prüfungen und Regression

- `python3 -m pytest -q detail_v2/kanten/test_kanten.py`: **5 passed, 1 xfailed**. Determinismus geprüft: zwei erneute Extraktionen stimmen für alle drei Dateien bytegenau mit den eingecheckten GeoJSON-SHAs überein.
- SHA-256: `kanten.geojson` `44001e280f8f44352b3c91c597bceb4524e70cf4e61508d86777971b6f1c3df1`; `grat.geojson` `3cd4e4bb52d6d23bc43e3473c8568c08ecf6416fe3987914238e3d0cab130c2f`; `zonen.geojson` `0c13658404aebec974975f79f71e5c45cf5795dcbe02f84be821a83339911d9c`.
- Legacy-Gate unverändert: 359 / 31 / 321, W1 = 0, Loch = 0. Ausgabe `GATE ROT: kein Export/ZIP` ist für diesen Regressionstest erwartbar. Gate-seitig geänderte Datei `pruefung/w1_alle56_letzter_lauf.json` wurde zurückgesetzt; der Arbeitsbaum enthält sonst nur neue P1c-Pfade.
- Bildkontrolle: [Übersicht](uebersicht_kanten.jpg), [G3/H3-Nahbild](nahbild_g3h3.jpg), [B3/C3-Nahbild](nahbild_b3c3.jpg). JPGs: 1008×963 / 229 383 B, 450×486 / 41 166 B, 450×486 / 42 179 B; Qualität 85.

## Annahmen, Risiken und offene Punkte

- [F] Die drei Anker bleiben exakt bei den beauftragten Koordinaten.
- [A] Zellmittelpunktkonvention `(cx+0,5,cy+0,5)` folgt dem 1-m-Zellpolygonraster; GB-Gitterpunkte selbst liegen auf ganzzahligen Weltkoordinaten.
- [A] Da `klippe` nicht `WAND_OBEN/WAND_FUSS` ausweist, ersetzt die Höhenmedian-Heuristik deren Quellunterscheidung nur näherungsweise.
- [R] Q3 ist klar verfehlt; die Kanten/Grate/Zonengrenzen benötigen eine weitere Glättungsrunde, ohne Bauzonen- oder Wasserflächen zu verschieben.
- [R] Die kleine Brückenklasse schrumpft bei der gemeinsamen Linienglättung um 43,25 %; Wasser bleibt mit +0,56 % innerhalb ±3 %, Ufer liegt bei −4,92 %.
- [R] Die Pflichtankerlinien laufen durch Hessian-Tangenten an den vorgegebenen Punkten, obwohl die nächstliegenden detektierten Quellpfade 1,50–3,54 m entfernt liegen. Die Bild-Nahansichten zeigen diese Stelle zur späteren Freigabe.
- [S] Es wurden keine bestehenden Relief-, Viewer-, Gate-, D2- oder Prüferdateien geändert. Keine Texturen oder Splat-Masken wurden erzeugt.
