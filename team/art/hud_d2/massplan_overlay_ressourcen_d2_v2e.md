# Massplan: Ressourcen v2e – Lagerpanel oben im Dorf-HUD

Stand: 2026-10-23  
Status: umgesetzt

## Zielbild

Das Ressourcenlager klappt von der hervorgehobenen Kiste im Dorf-HUD auf. Der vorhandene v2b-Kartenstil mit Bronze-Rahmen, Baloo/Lilita-Typografie und großen Plus-Buttons bleibt erhalten. Das Panel sitzt oben direkt unter den HUD-Quick-Icons. Top-Ressourcenleiste, Avatar/Level, Seiten-Icons und aktives Dorf-Dock bleiben sichtbar.

## Quellen

- HUD-Chrome: `vorschau_hud_d2_v7_3_lvl12.png`
- Kartenstil und Inhalt: `vorschau_overlay_ressourcen_d2_v2b.png` sowie `render_vorschau_overlay_ressourcen_d2_v2b.py`
- v2b/v2c/v2d-Masspläne wurden nur als Referenz gelesen.

## Geometrie und Ebenen

| Element | Position / Maß | Darstellung |
|---|---:|---|
| HUD-Chrome | 1080 × 1920 | Vollständig als Hintergrund |
| Kisten-Auslöser | Mittelpunkt (296, 244), Ø 88 px | Glut-oranger Ring um HUD-Kiste |
| Spielfeld-Scrim | x=150, y=300 bis Dock-Oberkante | Leicht abgedunkelt; HUD-Leisten und Dock bleiben unverändert |
| Lagerpanel | x=172, y=304, 600 × 448 px | v2b-Bronze-Verlauf, Doppelrahmen, weicher Schatten |
| Kopfbereich | Panel-Innenkante, Höhe 64 px | „LAGER“ und „VORRÄTE UND EINSETZEN“ |
| Drei Karten | je 576 × 116 px, Reihenabstand 120 px | Holz, Stein und Nahrung; Bestand/Kapazität/Balken |
| Plus-Buttons | 96 × 96 px | Holz und Nahrung Glut-Orange; Stein grau/deaktiviert |

Der Panel-Abstand zur Quick-Icon-Reihe beträgt 16 px. Das Panel endet bei y=752 und liegt damit weit oberhalb des unteren HUD-Docks. Es gibt weder Vollbild-Lagerhintergrund noch Bottom-Sheet.

## Zeileninhalt

| Ressource | Bestand / Kapazität | Kisten/Fässer | Ertrag | Aktion |
|---|---:|---:|---:|---|
| Holz | 12.480 / 20.000 | ×3 · KISTE | +2.500 HOLZ | aktiv |
| Stein | 8.215 / 20.000 | ×0 · FASS | +0 STEIN | grau/deaktiviert |
| Nahrung | 14.900 / 20.000 | ×1 · FASS | +5.000 NAHRUNG | aktiv |

## Ausgabe

- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v2e.py`
- Vorschau: `vorschau_overlay_ressourcen_d2_v2e.png` (1080 × 1920)
- Bericht: `BERICHT_ressourcen_v2e_oben_hud_2026-10-23.md`

