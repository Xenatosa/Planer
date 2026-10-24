# Bericht · BAU-MENÜ D2 v1e

**Status: DONE · 24.10.2026**

**Basis:** ausschließlich v1c (`a00e951`) und dessen Renderer. Das v1c-Menü wurde für eine scrollbare Einspaltenliste umgebaut. Das 2-Spalten-Raster aus v1d und die horizontalen Kacheln aus v2 sind nicht in v1e eingeflossen.

## Ausgabe

- `vorschau_menu_bau_d2_v1e.png` — Wirtschaft, Listenanfang mit Filterzeile und angeschnittener Folgezeile
- `vorschau_menu_bau_d2_v1e_scroll.png` — Militär-Reiter mit gescrollter Liste
- `_src/menu_bau_d2_v1e.html` — v1c-basierte Oberfläche und Inhalte
- `_src/render_vorschau_menu_bau_d2_v1e.py` — Renderer für beide Ansichten

Beide Vorschaubilder sind 1080×1920 px.

## Umsetzung

Die v1c-Gebäudezeile wurde von 278 auf 170 px (61 %) verkleinert. Jede Zeile bleibt einzeln und einspaltig: Gebäudeabbildung links, Name und Stufe mit Kurzinfo daneben, vier Kostenwerte darunter und der Status-Chip rechts. Fehlende Ressourcen sind rot markiert. Ein schmaler Scrollbereich mit dezenter Scroll-Leiste zeigt weitere Einträge unterhalb der angeschnittenen letzten Zeile.

Unter den Reitern stehen „Baubar zuerst“ und der sichtbare Zähler „7 von 9“. Die 25 Einträge verteilen sich auf Wirtschaft, Militär, Forschung und Deko (9/9/3/4). Der zweite Screen zeigt den Militär-Reiter in einer tieferen Scrollposition.

Gebäudebilder stammen ausschließlich aus `team/art/gebaeude_neu_b/`; Namen und Kurzinfos verwenden Steinzeit-Begriffe. Die D2-Top-Leiste und der vollflächige Scrim folgen v1c bzw. dem Scrim-Verlauf aus v3g. Das Detail-Sheet und seine einzige Aktion **AUSBAUEN** sind aus v1c beibehalten.

Es gibt keine Bauzeiten, Bauschlange oder **SOFORT**-Aktion.

## Sichtprüfung

Beide Ansichten wurden neu gerendert und visuell geprüft. Die Kostenreihe bleibt innerhalb der Zeile; die Scrollposition im Militär-Screen, der Scrollbalken und das angeschnittene Listenende sind sichtbar.
