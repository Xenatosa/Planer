# Bericht · BAU-MENÜ D2 v1b

**Status: DONE · 24.10.2026**

## Ausgabe

- `vorschau_menu_bau_d2_v1b.png` — Übersicht mit Kategorie-Reitern, vier Gebäudekarten und Bauschlange
- `vorschau_menu_bau_d2_v1b_detail.png` — Detail-Sheet Holzfällerlager mit **BAUEN** und **SOFORT**
- `_src/menu_bau_d2_v1b.html` — Layout und Komponenten
- `_src/render_vorschau_menu_bau_d2_v1b.py` — Renderer für beide Ansichten

Beide Vorschauen sind 1080×1920 px.

## Korrekturen zu v1

- Die vier ImageGen-Gebäude wurden aus `team/art/gebaeude_neu_b/` entfernt. Der Ordner enthält nun das gültige README und nur die benötigten Gebäude aus dem freigegebenen Variante-B-Set: `woodcutter_bp01`, `woodcutter_bp04`, `quarry_bp01`, `gatherer_bp01` und `hunter_bp01`.
- Die Karten zeigen **Holzfällerlager**, **Steinbruch**, **Sammlerlager** und **Jägerlager**. Das Detail-Sheet zeigt die höhere Holzfäller-Variante.
- Die erfundene Dorf-Überschrift, eigene Ressourcenleiste und nachgebaute Dock-Leiste wurden entfernt. Als Hintergrund dient das echte D2-HUD-Chrome `vorschau_hud_d2_v7_3_lvl12.png`, einschließlich Avatar, Ressourcen, Kiste und Menüleiste.
- Der Scrim folgt v3g: über den oberen 1300 px mit 168/255 Deckkraft, danach linear bis 105/255 am unteren Bildrand. HUD, Dorf und Menüleiste bleiben sichtbar und gedimmt.
- Reiter, Kostenkacheln, Statuszustände, Bauschlange, Baukosten und das Detail-Sheet aus v1 bleiben erhalten.

## Sichtprüfung

Beide Ansichten wurden neu gerendert und visuell geprüft. Die Karten und Bauschlange liegen vollständig unterhalb des HUDs und oberhalb der Menüleiste. Das Detail-Sheet zeigt Gebäude, Werte, Kosten, Bauzeit und beide Aktionen ohne abgeschnittene Elemente.
