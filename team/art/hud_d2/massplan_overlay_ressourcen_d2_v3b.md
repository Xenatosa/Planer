# Maßplan Ressourcen v3b – acht Slots ohne Scrollen

Stand: 2026-10-23  
Status: umgesetzt

## Komposition

Das Lager bleibt eine Öffnung im Dorf-HUD, ausgelöst von der markierten Kiste. Ein festes 2×4-Raster zeigt alle acht Ressourcen-Slots gleichzeitig. Es gibt keine Scrollfläche, keinen Sparkline-/Diagramm-Bereich und keinen Vollbild-Lagerscreen.

## Geometrie und Lesbarkeit

| Element | Position / Maß | Darstellung |
|---|---:|---|
| HUD-Chrome | 1080 × 1920 | Top-Währungen, Avatar/Level, Seiten-Icons und Dock bleiben sichtbar |
| Spielfeld-Scrim | x=150..1079, y=292..1707 | Obsidian, Alpha 170/255 (66,7%); obere Leiste und Dock bleiben unverändert |
| Kisten-Trigger | (252, 200), 88 × 88 px | Glutfarbene Eckmarken um die Kiste |
| Lagerpanel | x=150, y=304, 900 × 906 px | Opaque Obsidian-Panel, fein gerahmt in Bronze |
| Slot-Raster | x=170/607, y=384/570/756/942 | 2 Spalten × 4 Zeilen, Karten je 423 × 174 px, 12 px Zeilenabstand |
| Bestandsanzeige | links in aktiver Karte | Bestand/Kapazität plus schlanker Füllbalken |
| Aktionsfläche | rechts in aktiver Karte | Vertikaler Facetten-CTA, 116 × 132 px; Glut aktiv, Stein grau bei ×0 |
| Summenfuß | x=170, y=1124, 860 × 62 px | Gesamtproduktion pro Stunde |

## E1-Mock-Slots

| Slot | Bestand / Kapazität | Einsetz-Stack → Ertrag | Produktion/h | Zustand |
|---|---:|---|---:|---|
| Nahrung | 14.900 / 20.000 | ×1 FASS → +5.000 | +960/h | aktiv |
| Holz | 12.480 / 20.000 | ×3 KISTE → +2.500 | +420/h | aktiv |
| Stein | 8.215 / 20.000 | ×0 FASS → +0 | +180/h | Einsetzen-CTA grau/deaktiviert |
| Muscheln (Gold-Skin) | 3.270 / 8.000 | ×2 BEUTEL → +100 | +12/h | aktiv |
| Wissen | 930 / 5.000 | ×1 FOLIANT → +250 | +75/h | aktiv |
| Bernstein | — | — | — | gesperrt/leer |
| Metall | — | — | — | gesperrt |
| Epoche | — | — | — | gesperrt |

Gesamtproduktion: **+1.647/h**. Die fünf gefüllten Ressourcenraten summieren sich auf diesen Wert. Die drei gesperrten Slots belegen feste Rasterplätze und benötigen keine Scrollaktion.

## Ausgabe

- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v3b.py`
- Vorschau: `vorschau_overlay_ressourcen_d2_v3b.png` (1080 × 1920)
- Bericht: `BERICHT_ressourcen_v3b_8kacheln_2026-10-23.md`

