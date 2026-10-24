# Bericht · Bau-Menü D2 v2

**Status: DONE · 24.10.2026**

## Ausgabe

- vorschau_menu_bau_d2_v2.png — Bau-Shop, 1080 × 1920 px
- vorschau_menu_bau_d2_v2_platzieren.png — Stammesfeuer im Platzierungsmodus, 1080 × 1920 px
- _src/menu_bau_d2_v2.html — eigenständiger Renderer mit Kategorie-, Scroll- und Platzierungszustand
- _src/render_vorschau_menu_bau_d2_v2.py — prüft benötigte Assets und rendert beide Keyframes

## Entwurf

Das Menü ist eine untere Bau-Leiste ab y=1080. Vier runde Kategorie-Reiter wechseln zwischen Wirtschaft (9), Militär (7), Forschung (4) und Deko (5); zusammen sind 25 Einträge hinterlegt. Die Reihe scrollt horizontal, zeigt rund 3,3 Kacheln und hat einen Positionsindikator.

Jede Kachel stellt das Gebäude groß auf einem Glut-Sockel mit Lichtkegel dar. Darunter stehen Steinzeit-Name und eine kompakte Kostenzeile mit höchstens zwei Ressourcen. Anzahl und Limit stehen in der Ecke. Fehlende Mittel werden rot gezeigt. Gesperrte Gebäude sind entsättigt und tragen Schloss sowie „Rathaus 3“. Baubare Gebäude erhalten einen leichten Glutschein.

Ein Kacheltipp öffnet den Platzierungsmodus: Das Gebäude erscheint halbtransparent auf einem grünen Raster-Bauplatz. Ein Kosten-Tooltip zeigt alle Kosten, ✓ bestätigt und zählt den Bau direkt, ✕ schließt den Modus. Bauzeit, Warteschlange und Sofort-Aktion kommen nicht vor.

Die freigegebene D2-Top-Leiste und das Dock stammen aus vorschau_hud_d2_v7_3_lvl12.png. Der Scrim auf dem Dorf bleibt leicht; das Dock wird im Bau- und Platzierungsmodus abgedunkelt.

## Gebäudeabbildungen

Alle Gebäudeabbildungen kommen aus team/art/gebaeude_neu_b/. Die vorhandenen alpha-transparenten Ränder werden im Browser auf ein einheitliches Bildfeld normalisiert, ohne die Motive zu spiegeln oder zu verzerren. Dadurch erreichen auch Stammesfeuer und Muschelsammler die gleiche Bildhöhe wie die übrigen Motive.

Aus dem optionalen Ursprungsordner wurden die benötigten bp01/bp04-Dateien für Baracke, Palisade, Schamanenhütte, Stammesfeuer und die verwendeten bp04-Varianten nach team/art/gebaeude_neu_b/ kopiert. Die 25 Katalogeinträge verwenden die 12 freigegebenen Gebäude-Grundtypen; für die Kategorien ohne eigenes Motivset werden diese zulässigen Motive passend zum Steinzeit-Namen kombiniert.

## Selbstprüfung

Der Renderer erzeugt beide 1080 × 1920-PNGs erfolgreich. Beide wurden visuell geprüft: Größenverhältnisse der drei auffälligen Gebäude, 3,3-Kachel-Anschnitt, Reiter, Kosten, Anzahl/Limit, D2-Kopf und Dock sowie grünes Raster, Geisterbild, Tooltip und ✓/✕ sind sichtbar.
