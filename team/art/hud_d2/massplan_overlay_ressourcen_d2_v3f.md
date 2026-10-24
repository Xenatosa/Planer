# Maßplan Ressourcen-Overlay D2 v3f

## Ziel

v3f übernimmt das HUD-Fenster und die Ressourceninhalte aus v3e. Der Scrim ist dunkles Obsidian statt Mid-Gray und wird zum Dock hin weicher, damit die freiliegende Dorfszene sichtbar und lebendig bleibt.

## Leinwand und Flächen

- PNG: 1080 × 1920 px.
- HUD-Chrome: `vorschau_hud_d2_v7_3_lvl12.png`; Top-Leiste, Avatar und Dock bleiben außerhalb des Scrim-Bereichs.
- Scrim-Fläche: x=0–1079, y=292–1707. Farbton `#04070A` (RGB 4, 7, 10), keine graue Deckfarbe.
- Scrim-Alpha: 168/255 (ca. 66 %) vom oberen Overlay-Rand bis y=1280. Anschließend gleichmäßig auf 105/255 (ca. 41 %) bei y=1707 ausblenden. Das dunkelt die Umgebung des Fensters ab, lässt die sichtbaren Bereiche darunter aber differenziert durchscheinen.
- Lagerfenster: x=12, y=304, 1056 × 960 px (12 px Seitenrand). Titel ausschließlich „LAGER“.
- Raster: 3 × 4 Kacheln, je 334 × 188 px, ohne Scrollen. Kein Diagramm und keine Sparkline.

## Kachel-Inhalte

Nahrung 14.900/20.000, Holz 12.480/20.000, Stein 8.215/20.000, Muscheln 3.270/8.000 (Gold-Skin), Wissen 930/5.000, Bernstein 1.820/5.000, Metall 6.250/12.000 und Epochenmarken 760/3.000 sind aktiv. Die Kacheln zeigen Bestand/Kapazität, Füllbalken, Produktion/h und Einsetzen-Menge samt Ertrag. Stein bleibt bei ×0 grau/deaktiviert.

Runen, Artefakte, Reliquien und Essenz sind gesperrt. Gesamtproduktion der aktiven Ressourcen: +1.916/h.

## Gestaltung

D2-Obsidian-Karten, Bronze-Konturen, Baloo-/Lilita-Typografie und moderne Glut-CTAs wie in v3e. Der dunkle Scrim bewahrt den Szenenkontrast; der untere Verlauf vermeidet eine gleichmäßige Platte unter dem Fenster.
