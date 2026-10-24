# Maßplan Ressourcen-Overlay D2 v3e

## Ziel

v3e übernimmt die Fensterstruktur und die zwölf Ressourcen-Kacheln aus v3d. Geändert ist die Hintergrundbehandlung: Zwischen HUD-Kopf und Dock liegt ein grauer, transparenter Obsidian-Scrim, durch den die Dorfszene sichtbar bleibt.

## Leinwand und Flächen

- Vorschaugröße: 1080 × 1920 px.
- HUD-Chrome: `vorschau_hud_d2_v7_3_lvl12.png`; Top-Leiste samt Avatar und der Dorf-Dock unten bleiben sichtbar.
- Grauer Scrim: x=0–1079, y=292–1707, Farbe `#2B2F32`, Alpha 170/255 (ca. 67 %). Szene und HUD-Elemente im Hintergrund bleiben erkennbar.
- Lagerfenster: x=12, y=304, 1056 × 960 px; nur 12 px Seitenrand.
- Titel: „LAGER“, ohne Raster-/Test-Untertitel.
- Kachelraster: 3 Spalten × 4 Reihen, je 334 × 188 px; horizontale und vertikale Kachel-Lücke 10 px. Kein Scrollbereich.

## Kachel-Inhalte

Aktive Ressourcen: Nahrung 14.900/20.000, Holz 12.480/20.000, Stein 8.215/20.000, Muscheln 3.270/8.000 (Gold-Skin), Wissen 930/5.000, Bernstein 1.820/5.000, Metall 6.250/12.000 und Epochenmarken 760/3.000. Jede aktive Kachel zeigt Bestand/Kapazität, Balken, Einsetzen-Menge und Ertrag sowie Produktion pro Stunde. Stein zeigt ×0 und bleibt deaktiviert/grau.

Runen, Artefakte, Reliquien und Essenz sind gesperrt. Die Summe der aktiven Produktionsraten ist +1.916/h.

## Gestaltung

D2-Obsidian-Karten, Bronze-Konturen, Baloo-/Lilita-Typografie und moderne Glut-CTAs bleiben wie in v3d. Es gibt kein Diagramm und keine Sparkline. Panel- und Kachelkontrast halten Werte lesbar, während der Hintergrund außerhalb des Fensters durchscheint.
