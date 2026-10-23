# Maßplan · Inventar D2 v4

Leinwand: **1080 × 1920 px**, Hochformat. Das UI nutzt feste Pixelmaße wie der Beschwören-v16-Mock; Kartenbereich und Suchfeld bleiben im HTML bedienbar.

| Bereich | Position / Größe | Aufbau |
|---|---:|---|
| Ressourcenleiste | x38, y16 · 1004 × 100 | Kristall, Plus, Wissen, Gold-Muschel |
| Kopf | x30, y126 · 1020 × 102 | Zurück, Inventar, Schließen; Belegung 28/40 |
| Kategorien | x30, y244 · 1020 × 126 | fünf gleich große Tabs mit Symbol und Anzahl |
| Suche / Sortierung | x38, y386 · 1004 × 76 | Suche 708 px, Sortierung 284 px |
| Kartenraster | x35, y510 · 1010 × 500 | drei Spalten, Karten 242 px hoch, vertikal scrollbar |
| Kapazität | x42, y1026 · 996 × 76 | Belegung 28/40, Glut-Füllstand 70 % |
| Detailfläche | x38, y1117 · 1004 × 514 | große Ausrüstungskarte, Seltenheit, zwei Werte, Aktion |
| Offenes Detailsheet | x38, y688 · 1004 × 946 | überlagert Raster; großes Itembild und 120-px-Aktion |
| Dock A | x0, y1664 · 1080 × 256 | sechs Bereiche, Inventar aktiv, Home-Leiste |

Seltenheitsrahmen unterscheiden **Grob**, **Geschliffen**, **Meisterstück** und **Artefakt** über Farbe, Innenlinie und Lichtsaum. Der Hallen-Hintergrund wird auf 1080 × 1920 beschnitten und leicht in den Schatten angehoben; ein dunkler Scrim mit mindestens **65 %** Deckung und zwei weiche Vignettenebenen halten ihn zurück. Gemessener Randmittelwert (je 20 px außen, y100–1663): **15,4**, Beschwören v16: **18,4**, Differenz **3,0**.

Die PNG-Keyframes zeigen Alle mit ausgewähltem Knochenhelm, Ausrüstung sowie das geöffnete Detailsheet. Suchfeld, Sortierknopf, Tabs und Kartenklick arbeiten im HTML-Mock.
