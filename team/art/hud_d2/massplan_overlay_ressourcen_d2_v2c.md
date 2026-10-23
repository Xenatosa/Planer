# Ressourcen-Sheet auf dem Dorf-HUD – v2c

Stand: 23.10.2026 · Bottom-Sheet auf dem freigegebenen HUD-Chrome v7.3b. v2b wird durch die Sheet-Darstellung korrigiert; dessen Item- und Ertragsdaten bleiben erhalten.

## Layout

- Basis: `vorschau_hud_d2_v7_3_lvl12.png`, 1080×1920. Die Kiste im HUD bleibt der hervorgehobene Opener.
- Scrim liegt über dem Hauptscreen; HUD und Dorf bleiben darunter sichtbar.
- Sheet: x=28, y=1108, 1024×580 px. Es endet bei y=1688, 20 px vor dem Dock.
- Kopf: „LAGER“ und Füllstand-Ring; Schließen oben rechts.
- Drei Zeilen starten bei y=1228, Abstand 142 px, Höhe 130 px. Ressourcen-Icon, Bestand/Kapazität und Balken bleiben links; Item-Menge/Ertrag und Plus-Schaltfläche stehen rechts.
- Plus-Hitfläche: je 96×96 px. Bei Item-Bestand >0 orange/aktiv, sonst grau/deaktiviert.

## Mock

| Ressource | Lager | Item / Ertrag | Plus |
|---|---:|---|---|
| Holz | 12.480 / 20.000 | ×3 · KISTE / +2.500 HOLZ | aktiv |
| Stein | 8.215 / 20.000 | ×0 · FASS / +0 STEIN | grau, deaktiviert |
| Nahrung | 14.900 / 20.000 | ×1 · FASS / +5.000 NAHRUNG | aktiv |

## Dateien

- Vorschau: `vorschau_overlay_ressourcen_d2_v2c.png`
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v2c.py`
- Bericht: `BERICHT_ressourcen_v2c_hud_sheet_2026-10-23.md`

Die v2b-Vorschau bleibt als ältere Fassung erhalten. Keine weiteren Screens oder Unity-Dateien geändert.
