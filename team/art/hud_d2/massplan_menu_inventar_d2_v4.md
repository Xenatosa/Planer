# Maßplan · Inventar D2 v4b

Leinwand: **1080 × 1920 px**, Hochformat. Das UI nutzt feste Pixelmaße wie der Beschwören-v16-Mock; Kartenbereich und Suchfeld bleiben im HTML bedienbar.

| Bereich | Position / Größe | Aufbau |
|---|---:|---|
| Ressourcenleiste | x38, y16 · 1004 × 100 | Kristall, Plus, Wissen, Gold-Muschel |
| Kopf | x30, y126 · 1020 × 102 | Zurück, Inventar, Schließen; Belegung 28/40 |
| Kategorien | x30, y244 · 1020 × 126 | fünf gleich große Tabs mit Symbol und Anzahl |
| Suche / Sortierung | x38, y386 · 1004 × 76 | Suche 708 px, Sortierung 284 px |
| Kartenraster | x35, y510 · 1010 × 1002 | vier Spalten, Karten 242 × 190 px, fünf Reihen sichtbar, vertikal scrollbar; Icons 60 px |
| Kapazität | x42, y1544 · 996 × 76 | Belegung 28/40, Glut-Füllstand 70 % |
| Übersicht | — | Tabs, Suche, Sortierung, Raster und Kapazität; keine feststehende Detailfläche |
| Detailsheet (modal) | x38, y688 · 1004 × 946 | nur nach Tipp auf Gegenstand; großes Itembild, Werte und typabhängige Aktion; X, Zurück, Außentipp oder Escape schließt |
| Dock A | x0, y1664 · 1080 × 256 | sechs Bereiche, Inventar aktiv, Home-Leiste |

Seltenheitsrahmen unterscheiden **Grob**, **Geschliffen**, **Meisterstück** und **Artefakt** über Farbe, Innenlinie und Lichtsaum. Die kompakteren Karten zeigen Gegenstandsbild, Seltenheit, Namen und Typ. Ausrüstung zeigt **Anlegen**, Ressourcen und Verbrauchsgüter **Verwenden**; Fragmente zeigen Sammelfortschritt ohne Aktionsknopf. Der Hallen-Hintergrund wird auf 1080 × 1920 beschnitten und leicht in den Schatten angehoben; ein dunkler Scrim mit mindestens **65 %** Deckung und zwei weiche Vignettenebenen halten ihn zurück. Gemessener Randmittelwert (je 20 px außen, y100–1663): **15,4**, Beschwören v16: **18,4**, Differenz **3,0**.

Die PNG-Keyframes zeigen Alle mit ausgewähltem Knochenhelm, Ausrüstung sowie das geöffnete Detailsheet. Suchfeld, Sortierknopf, Tabs, Kartenklick und Sheet-Schließen arbeiten im HTML-Mock.
