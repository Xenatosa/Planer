# Helden-Menü D2 v1b

**Status: DONE**

v1b lässt die Heldenliste aus v1 unverändert. Im sechsteiligen D2-Dock ist „Helden“ aktiv.

Das Detail übernimmt den freigegebenen Aufbau aus `team/art/ui-kit/menus_v3/v3_2_obsidian_helden_detail_v2.png` und dessen HTML-Quelle. Es zeigt Ruka als großen Fullbody-Held mit Namens-Wasserzeichen, Machtfeld, Sternenfortschritt, fünf Ausrüstungsplätzen je Seite mit Stufen-Badges, den Reitern Werte/Skills/Lore/Inventar, Werte- und Gegenstand-Panel sowie die Heldenstufe mit „AUFWERTEN“.

Für die D2-Anpassung verwendet das Detail die Kopfzone aus dem v3g-HUD und das aktuelle Dock in der Reihenfolge Dorf, Helden, Karte, Armee, Gilde, Inventar. Die freigegebene Höhlenfläche bleibt erhalten. Das Detailraster ist proportional auf 91 % skaliert und unter der 292 px hohen D2-Kopfzone ausgerichtet, damit alle Referenzbereiche bis zur Dockkante sichtbar bleiben.

## Dateien

- `vorschau_menu_helden_d2_v1b.png` — Liste, Dock „Helden“ aktiv.
- `vorschau_menu_helden_d2_v1b_detail.png` — freigegebenes Detail v2 mit D2-Kopfzone und Dock.
- `_src/menu_helden_d2_v1b.html` und `_src/render_vorschau_menu_helden_d2_v1b.py` — Quelle und Renderer.
- `_src/assets/` — lokale Höhlen- und Ausrüstungsassets für reproduzierbares Rendern.

## Prüfung

Beide Vorschauen wurden mit dem v1b-Renderer erzeugt und visuell geprüft. Beide Dateien haben das Zielformat 1080 × 1920 px.
