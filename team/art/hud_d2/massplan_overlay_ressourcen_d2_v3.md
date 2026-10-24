# Maßplan Ressourcen v3 – Lagerkern im Dorf-HUD

Stand: 2026-10-23  
Status: umgesetzt

## Leitidee

Statt einer Ressourcenliste zeigt v3 drei eigenständige Speicherkacheln in einer horizontalen Kontrollmatrix. Jede Kachel kombiniert Füllstand-Ring, Bestand, Mini-Sparkline der laufenden Produktion, verfügbaren Kisten-/Fass-Stapel und einen kantigen Einsetzen-CTA. Der Fußbereich fasst die stündliche Produktion separat zusammen.

Look: D2 Obsidian mit Glut-Akzenten, klare Kontraste und harte Lesbarkeit. Die HUD-Kiste bleibt der Auslöser; das Panel liegt im Dorf-HUD, ohne Lager-Vollbild oder Bottom-Sheet.

## Geometrie

| Element | Position / Maß | Aufbau |
|---|---:|---|
| HUD-Chrome | 1080 × 1920 | Basis `vorschau_hud_d2_v7_3_lvl12.png`; Top-Ressourcen, Avatar/Level und Dock sichtbar |
| Scrim | Spielfeld x=150..1079, y=292..1707 | Schwarz/Obsidian mit 68% Deckkraft; HUD-Top und Dock bleiben ungedimmt |
| Kisten-Trigger | HUD-Kiste bei (252, 200), 88 × 88 px | Vier Glut-Eckmarken statt eines Kreisrings |
| Lagerkern-Panel | x=150, y=304, 900 × 690 px | Opaque Obsidian-Kontrollfläche mit Bronze-Feinrahmen |
| Header | innerhalb Panel, obere 70 px | LAGER, Dorfreserven und Live-Depot-Status |
| Speicherkacheln | x=170/462/754, y=390, je 276 × 400 px | Holz, Stein, Nahrung; radialer Füllstand, Bestand, Rate/Sparkline, Stapel und CTA |
| Produktionsfuß | x=170, y=812, 860 × 160 px | Gesamt +1.560/h plus drei Ressourcenkarten |
| Einsetzen-CTA | je 248 × 96 px | Abgeschrägte Glut-/Stein-Fläche mit Hex-Sigil und Plus-Glyphe |

## Inhalte

| Ressource | Bestand / Kapazität | Füllstand | Stapel und einmaliger Ertrag | Laufende Produktion |
|---|---:|---:|---|---:|
| Holz | 12.480 / 20.000 | 62% | ×3 · KISTE → +2.500 | +420/h |
| Stein | 8.215 / 20.000 | 41% | ×0 · FASS → +0, CTA deaktiviert | +180/h |
| Nahrung | 14.900 / 20.000 | 75% | ×1 · FASS → +5.000 | +960/h |
| **Gesamt** | | | | **+1.560/h** |

Einsetzen-Ertrag ist pro Aktion; Produktion/h ist der separate laufende Zufluss und erscheint sowohl in den Ressourcenkacheln als auch im Summenfuß.

## Neue Dateien

- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v3.py`
- PNG: `vorschau_overlay_ressourcen_d2_v3.png` (1080 × 1920)
- Bericht: `BERICHT_ressourcen_v3_komplett_neu_2026-10-23.md`
