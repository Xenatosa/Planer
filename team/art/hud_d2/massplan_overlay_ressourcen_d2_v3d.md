# Maßplan Ressourcen-Overlay D2 v3d

## Ziel

Das Ressourcenfenster klappt aus der hervorgehobenen Kiste im Dorf-HUD auf. Der vorhandene HUD-Chrome bleibt sichtbar. Zwischen Top-Leiste und Dock liegt eine deckende, flächige Obsidian-Graufläche; das Lagerfenster nutzt nahezu die gesamte Bildschirmbreite.

## Leinwand und Bereiche

- PNG: 1080 × 1920 px.
- HUD-Chrome: `vorschau_hud_d2_v7_3_lvl12.png`; oberer Bereich einschließlich Avatar und Ressourcenleiste sowie der Dorf-Dock unten bleiben unverändert sichtbar.
- Overlay-Grundfläche: x=0–1079, y=292–1707, deckendes Obsidian-Grau `#2B2F32`. Die Dorfszene scheint in diesem Bereich nicht durch.
- Lagerfenster: x=12, y=304, Breite=1056 px, Höhe=960 px. Damit bleiben 12 px seitlicher Sicherheitsabstand.
- Titelzeile: ausschließlich „LAGER“; keine Raster-, Test- oder Kapazitätsnotiz.
- Raster: 3 Spalten × 4 Reihen. Kacheln sind jeweils 334 px breit und 188 px hoch; horizontale Lücke 10 px, vertikale Lücke 10 px. Alle zwölf Kacheln und die Gesamtproduktion passen in das Fenster.

## Kachel-Inhalte

Aktive Mock-Ressourcen: Nahrung 14.900/20.000, Holz 12.480/20.000, Stein 8.215/20.000, Muscheln 3.270/8.000 (Gold-Skin), Wissen 930/5.000, Bernstein 1.820/5.000, Metall 6.250/12.000 und Epochenmarken 760/3.000. Jede aktive Kachel zeigt Bestand/Kapazität, Füllbalken, laufende Produktion pro Stunde und Einsetzen-Menge samt Ertrag. Stein bleibt bei ×0 deaktiviert und grau.

Die vier übrigen Kacheln heißen Runen, Artefakte, Reliquien und Essenz und sind gesperrt. Für die acht aktiven Ressourcen summiert sich die Mock-Produktion auf +1.916/h.

## Gestaltung und Ausschlüsse

- D2-Obsidian-Karten mit Bronze-Konturen, Baloo-/Lilita-Typografie und modernen, breiten Glut-CTAs.
- Kein Scrollen, keine Sparkline, kein Diagramm und kein Extra-Vollbildscreen.
- Maßpläne, Renderer und Vorschauen früherer Versionen bleiben unverändert.
