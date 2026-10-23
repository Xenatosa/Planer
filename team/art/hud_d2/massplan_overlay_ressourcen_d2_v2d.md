# Ressourcen-HUD-Sheet – v2d

Stand: 23.10.2026 · HUD-Struktur wie v2c, Kartenstil, Typografie und Plus-Zustände wie v2b.

## Struktur und Stil

- Basis ist der HUD-Chrome `vorschau_hud_d2_v7_3_lvl12.png`; der Glut-Ring markiert die Kiste als Opener.
- Bottom-Sheet: x=28, y=1108, 1024×580 px. Es endet 20 px über dem Dock; HUD und Dorf bleiben erkennbar.
- Dunkle Karten mit Bronze-Kontur, warme Verläufe und v2b-Typografie (Baloo/Lilita) für die drei Ressourcenzeilen.
- Pro Karte bleiben Bestand, Kapazität und Balken links; `×N · KISTE/FASS` und `+X.XXX RESSOURCE` stehen daneben.
- 96×96 px Plus-Kreis mit Glut-Verlauf bei Item-Bestand >0; grauer Plus-Kreis bei 0 Items.

## Positionen (1080×1920)

| Element | x | y | w | h |
|---|---:|---:|---:|---:|
| Sheet | 28 | 1108 | 1024 | 580 |
| Kopf / Füllstand / Schließen | 58 | 1126 | 962 | 96 |
| Holzkarte | 44 | 1228 | 992 | 130 |
| Stein-Karte | 44 | 1370 | 992 | 130 |
| Nahrungskarte | 44 | 1512 | 992 | 130 |
| Plus je Zeile | 920 | je Karte +17 | 96 | 96 |

## Mock-Daten

| Ressource | Bestand | Item-Menge / Ertrag | Zustand |
|---|---:|---|---|
| Holz | 12.480 / 20.000 | ×3 · KISTE / +2.500 HOLZ | aktiv |
| Stein | 8.215 / 20.000 | ×0 · FASS / +0 STEIN | grau, deaktiviert |
| Nahrung | 14.900 / 20.000 | ×1 · FASS / +5.000 NAHRUNG | aktiv |

## Dateien

- Vorschau: `vorschau_overlay_ressourcen_d2_v2d.png`
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v2d.py`
- Bericht: `BERICHT_ressourcen_v2d_style_2026-10-23.md`

DONE · 2026-10-23
