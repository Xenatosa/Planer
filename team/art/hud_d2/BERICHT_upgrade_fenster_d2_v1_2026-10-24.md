# Bericht · Upgrade-Fenster D2 v1

**Status: DONE · 24.10.2026**

**Basis:** Bau-Menü v1e (`907a691`), Stilregeln und Detail-Sheet aus v1c. Das Fenster übernimmt die D2-Top-Leiste und den vollflächigen Scrim aus v3g. Inhalte und Raster aus v1d/v2 wurden nicht übernommen.

## Ausgabe

- `vorschau_menu_upgrade_d2_v1.png` — Ausbau möglich: Voraussetzung erfüllt, Ressourcen ausreichend
- `vorschau_menu_upgrade_d2_v1_gesperrt.png` — Ausbau gesperrt: Häuptlingsfeuer-Voraussetzung nicht erfüllt, zu wenig Stein
- `_src/menu_upgrade_d2_v1.html` — beide Zustände
- `_src/render_vorschau_menu_upgrade_d2_v1.py` — Renderer

Beide Vorschaubilder sind 1080×1920 px.

## Umsetzung

Das Fenster zeigt das Holzfällerlager auf Stufe 2 → 3. Darunter stehen der Wertevergleich für Produktion/h und Lagerkapazität, die erfüllte oder fehlende Voraussetzung sowie vier Ausbaukosten in einer Reihe. Der neue Wert ist grün; fehlender Stein und die nicht erfüllte Voraussetzung sind rot. Der breite **AUSBAUEN**-Button ist im gesperrten Screen deaktiviert und zeigt den Hinweis „Zu wenig Stein“. Die Maximalstufe steht als kleine Schlusszeile.

Es gibt keine Bauzeit, **SOFORT**-Aktion oder Bauschlange.

## Gebäudevorschau

Im freigegebenen Verzeichnis `team/art/gebaeude_neu_b/` liegt für das Holzfällerlager `bp01` und `bp04`, aber keine `bp07`-Grafik. Das aktuelle große Bild und die kleine Zielstufen-Vorschau verwenden deshalb vorläufig beide `e1_bld_woodcutter_bp04.png`. Sobald `bp07` vorliegt, kann nur die kleine Vorschau ersetzt werden.

## Sichtprüfung

Beide Screens wurden neu gerendert und visuell geprüft. Die D2-Top-Leiste und der untere Dock bleiben unter dem v3g-Scrim erkennbar. Alle Inhalte einschließlich Kosten, Button, Sperrhinweis und Maximalstufe liegen innerhalb des Panels.
