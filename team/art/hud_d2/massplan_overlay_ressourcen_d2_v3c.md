# Maßplan Ressourcen v3c – 12 Kacheln gleichzeitig

Stand: 2026-10-24  
Status: umgesetzt

## Zweck

Statischer UI-Kapazitätstest: das Lagerpanel zeigt zwölf Slots gleichzeitig in einem festen 3×4-Raster. Keine Scrollfläche, kein Diagramm, keine Sparkline. Dieser Mock ändert keine Gameplay-Regel und erhöht nicht das normale Acht-Slot-Limit.

## Geometrie

| Element | Position / Maß | Darstellung |
|---|---:|---|
| HUD-Chrome | 1080 × 1920 | Dorf-HUD mit Top-Leiste, Avatar/Level und Dock |
| Spielfeld-Scrim | x=150..1079, y=292..1707 | Obsidian, Alpha 170/255 (66,7%); HUD-Kopf/Dock bleiben klar |
| Kisten-Trigger | (252, 200), 88 × 88 px | Glutfarbene Eckmarken am HUD-Quick-Icon |
| Lagerpanel | x=150, y=304, 900 × 960 px | Opaque Obsidian-Kontrollfläche mit feinem Bronze-Rahmen |
| Slot-Raster | 3 Spalten × 4 Reihen | x=170/460/750, y=382/580/778/976; Kacheln je 280 × 188 px |
| Bestand | pro gefüllter Kachel | Bestand/Kapazität und schlanker Füllbalken |
| Einsetzen-CTA | pro gefüllter Kachel, 256 × 54 px | Abgeschrägte Glut-Leiste mit Hex-Plus; Stein bei ×0 grau |
| Produktionsfuß | x=170, y=1188, 860 × 62 px | Kompakte Gesamtproduktion /h |

## Zwölf Mock-Slots

| Slot | Bestand / Kapazität | Einsetzen-Stack → Ertrag | Produktion/h | Zustand |
|---|---:|---|---:|---|
| Nahrung | 14.900 / 20.000 | ×1 FASS → +5.000 | +960/h | gefüllt, aktiv |
| Holz | 12.480 / 20.000 | ×3 KISTE → +2.500 | +420/h | gefüllt, aktiv |
| Stein | 8.215 / 20.000 | ×0 FASS → +0 | +180/h | gefüllt; CTA grau/deaktiviert |
| Muscheln (Gold-Skin) | 3.270 / 8.000 | ×2 BEUTEL → +100 | +12/h | gefüllt, aktiv |
| Wissen | 930 / 5.000 | ×1 FOLIANT → +250 | +75/h | gefüllt, aktiv |
| Bernstein | 1.820 / 5.000 | ×2 AMPULLE → +120 | +35/h | gefüllt, Demo-Daten |
| Metall | 6.250 / 12.000 | ×2 BARREN → +400 | +210/h | gefüllt, Demo-Daten |
| Epochenmarken | 760 / 3.000 | ×1 SIEGEL → +50 | +24/h | gefüllt, Demo-Daten |
| Runen | — | — | — | Platzhalter, gesperrt |
| Artefakte | — | — | — | Platzhalter, gesperrt |
| Reliquien | — | — | — | Platzhalter, gesperrt |
| Essenz | — | — | — | Platzhalter, gesperrt |

Gesamtproduktion für die gefüllten Mock-Slots: **+1.916/h**.

## Ausgabe

- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v3c.py`
- Vorschau: `vorschau_overlay_ressourcen_d2_v3c.png` (1080 × 1920)
- Bericht: `BERICHT_ressourcen_v3c_12kacheln_2026-10-24.md`

