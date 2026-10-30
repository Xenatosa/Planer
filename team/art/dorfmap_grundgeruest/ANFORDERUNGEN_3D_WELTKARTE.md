# Anforderungen an eine echte 3D-Weltkarte (Dorfmap c20)

Entscheidung [F] (Fabian, t32u): Die Kamera im Spiel lässt sich frei in jeden Blickwinkel drehen.
Daraus folgt: Die Karte darf nicht nur von oben gut aussehen. Sie muss von allen Seiten stimmen.

Marker: [S] gemessen/Quelle · [A] Annahme · [R] gerechnet · [F] Entscheidung.

## 1. Höhenkarte je Zelle
- Quelle heute: `raster_c20_z25_zellen.csv`, Feld `hoehe_m` [S Datei]. Die Werte selbst sind [A].
- Auflösung: z25 = 336 × 303 Zellen, 1 Zelle = 1 m = 25 px in c20 [S]. z50 = 168 × 152 [S].
- Heute [A]:
  - Stufen: SENKE 0, PLATEAU_NORD +8,6, GIPFEL +7,7, OSTPLATEAU +6,7, TAL_SUED −7,6, KRATER 0.
  - HANG: Höhe nur gerechnet (Laplace) zwischen den Stufen [R] auf Basis von [A].
  - SIMS: Mittel der Umgebung [A].
  - Wasser hat keine Tiefe im Modell.
- Muss gemessen oder gemalt werden:
  - eine Höhen-Graustufenkarte (gemalt vom Art-Team), mindestens 1 Wert pro m, besser 0,5 m;
  - echte Wandhöhen je Wandabschnitt (statt drei Werte);
  - Hangverlauf West, Ostwald, Waldterrasse (Befunde B1–B5 in `pruefung/t34u_fehlerliste.csv`);
  - Flusstiefe und Ufer-Höhe.

## 2. Maßgrundlage
- 1 Zelle = 1 m [F aus Raster-Festlegung].
- Wandhöhen heute: Nord 8,6 m, Krater/Südgrat 7,6 m, Ostgrat 6,7 m [A] (aus KL_M und Verhältnissen geschätzt).
- Mensch-Verhältnis: Eine Figur von ca. 1,8 m wäre in c20 ca. 45 px hoch [R aus 25 px/m]. Das muss an einer Figur/Tür/Baum in c20 nachgemessen werden. Noch nicht gemacht [A].
- Bäume, Felsen, Häuser brauchen feste Höhen in m [A, offen].

## 3. Flächen, die von allen Seiten sichtbar sind
- **Wandflächen:** eigene Fels-Textur, die nach unten läuft. Nicht c20 nach unten ziehen (heute gestreift).
- **Rückseiten und Kartenränder:** rund um die Karte ein Sockel ("Skirt") bis unter die tiefste Stelle (−7,6 m minus Puffer). Kein Blick ins Leere, keine offenen Kanten.
- **Wasser:** eigene Wasserfläche mit Tiefe und Ufer. Eis/Schollen als eigene Ebene.
- **Hang-Normalen:** aus der Höhenkarte gerechnet [R], damit Licht auf Hängen stimmt.
- Oberseiten (Plateaus) aus c20 sind von oben gemalt; von schräg sind gemalte Schatten und Lichter falsch [A]. Für freie Kamera: Schatten aus c20 entfernen oder neu malen (Art-Frage).

## 4. Folgen der frei drehbaren Kamera [F]
- **Verdeckung:** Wände verdecken Figuren und Plätze. Nötig: Wand ausblenden/durchsichtig, wenn sie zwischen Kamera und Spieler steht.
- **Sprites und Gebäude:** Flache 2D-Sprites haben keine Rückseite. Nötig: 3D-Modelle oder Sprites aus mehreren Winkeln (z. B. 8 Richtungen).
- **Licht und Schatten:** Gemalte Schatten in c20 passen nur zu einer Richtung. Nötig: echtes Licht in der Engine und neutrale Textur.
- **Zoom-Grenzen:** Mindest- und Höchstabstand und ein Mindest-Neigungswinkel festlegen [A, offen], damit man nicht unter die Karte schaut.
- **Kartenrand:** Kamera am Rand begrenzen, außen Kulisse (Berge/Nebel) zeigen.

## 5. Engine-Format für Unity
- Weg A: Unity Terrain mit Heightmap (16-bit RAW, z. B. 337 × 337 oder 513 × 513). Gut für Hänge, schlecht für senkrechte Wände.
- Weg B: GLB-Mesh (Gelände inkl. Wände als echte Geometrie). Gut für Wände. Empfehlung [A]: Mesh für Wände, Terrain nur wenn Hänge viel Detail brauchen.
- Getrennte Ebenen (Layer):
  1. Gelände (Höhen, Wände, Wasser),
  2. Overlay Plätze (bebaubar, Bauzonen),
  3. Wege,
  4. Deko (Bäume, Felsen) als einzelne Objekte.
- Koordinaten: 1 Unity-Einheit = 1 m, y nach oben, cx → x, cy → z [A].

## 6. Was `modell3d/` heute kann
- OBJ + MTL + Textur aus z25, 150 146 Ecken, 139 745 Vierecke [R].
- Jede Zelle flach in ihrer Höhe, Sprünge als senkrechte Wände.
- 6 Vorschaubilder (Überhöhung ×3 [F]).
- Bekannte Mängel (angesehen):
  - Wände gestreift (c20 nach unten gezogen);
  - Nord-Ansicht: Streifen unten und dünne Spitzen;
  - kein Sockel/Rand, kein Wasser, keine Normalen, keine Deko-Objekte;
  - stufige Hänge (1-m-Treppen);
  - in keinem echten 3D-Programm geöffnet.

## 7. Offene Fragen (noch NICHT versendet)
- **Art Director:**
  - Wird eine Höhenkarte gemalt? In welcher Auflösung?
  - Stimmen die Wandhöhen 8,6 / 7,6 / 6,7 m?
  - Sollen die gemalten Schatten aus c20 heraus?
  - Wer malt die Wand-Texturen und den Kartenrand?
- **Wege-Bot:**
  - Laufen die Wege auf der Höhe der Zellen oder als eigenes Mesh?
  - Wie gehen Wege über Hänge und Stufen (Treppen/Rampen)?
- **Game Designer:**
  - Zoom-Grenzen und Mindestwinkel der Kamera?
  - Ausblenden von Wänden ja/nein?
  - Bauen außerhalb der Senke erlaubt?
  - 3D-Gebäude oder Sprites aus mehreren Winkeln?
