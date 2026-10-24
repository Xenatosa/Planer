# Maßplan Ressourcen v2f – moderne Aktionen und Produktion pro Stunde

Stand: 2026-10-23  
Status: umgesetzt

## Ziel und Basis

v2f behält den Dorf-HUD-Aufklappzustand aus v2e bei. Aktualisiert werden ausschließlich die Plus-Steuerflächen; zusätzlich zeigt das Lagerpanel die laufende Produktion pro Stunde getrennt von den einmaligen Einsetzen-Erträgen.

- HUD-Chrome und Panelposition: wie v2e, Basis `vorschau_hud_d2_v7_3_lvl12.png`
- Karten und Ressourcenzeilen: wie v2e
- Neue Plus-Optik: Obsidian-Rahmen, Glut-Verlauf, dezenter Glow, klare Vektor-Plus-Glyphe

## Geometrie

| Element | Position / Maß | Spezifikation |
|---|---:|---|
| Vollständiges Dorf-HUD | 1080 × 1920 | Top-Ressourcenleiste, Avatar/Level, Quick-Icons, Side-Icons und Dock bleiben sichtbar |
| Kisten-Auslöser | (252, 200), 88 × 88 px | Glut-Ring wie v2e |
| Lagerpanel | x=172, y=304, 600 × 506 px | v2e-Verankerung und v2b-Bronze-Kartenstil |
| Ressourcen-Karten | drei Karten, je 576 × 116 px | Reihen und Einsetzen-Werte wie v2e |
| Plus-Touchflächen | 96 × 96 px je Zeile | Abgerundetes Quadrat mit Glut-Verlauf oder desaturiertem Stein-Grau |
| Produktionsfuß | unter den drei Karten | Gesamtwert und drei Ressourcenraten pro Stunde |

## Daten

| Ressource | Bestand | Einsetzen | Laufende Produktion |
|---|---:|---|---:|
| Holz | 12.480 / 20.000 | ×3 · KISTE, +2.500 HOLZ, aktiv | +420/h |
| Stein | 8.215 / 20.000 | ×0 · FASS, +0 STEIN, deaktiviert | +180/h |
| Nahrung | 14.900 / 20.000 | ×1 · FASS, +5.000 NAHRUNG, aktiv | +960/h |
| Gesamt | | | **+1.560/h** |

Die Produktionsraten beschreiben den laufenden Ertrag. Sie stehen im separaten Panel-Fuß und sind nicht Teil des einmaligen Kisten-/Fass-Ertrags pro Zeile.

## Neue Dateien

- `_src/render_vorschau_overlay_ressourcen_d2_v2f.py`
- `vorschau_overlay_ressourcen_d2_v2f.png` (1080 × 1920)
- `BERICHT_ressourcen_v2f_plus_modern_2026-10-23.md`

