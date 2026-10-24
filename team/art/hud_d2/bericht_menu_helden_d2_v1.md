# Helden-Fenster D2 v1

## Dateien

- `vorschau_menu_helden_d2_v1.png` — einspaltige, scrollbare Heldenliste.
- `vorschau_menu_helden_d2_v1_detail.png` — Helden-Detail mit Portrait, Werten, Fähigkeiten, Ausrüstungsplätzen und Aktionen.
- Renderer und HTML: `_src/render_vorschau_menu_helden_d2_v1.py`, `_src/menu_helden_d2_v1.html`.

## Gestaltung und Inhalt

Das Fenster verwendet das vollflächige HUD-Bild aus dem freigegebenen D2-Bundle, den durchscheinenden Vollbild-Scrim, die warme Obsidian-Bronze-Glut-Palette und das volle Panel-Raster des Bau-Menüs v1e. Die D2-Ressourcenleiste und das Dock bleiben unter dem Scrim sichtbar.

Die Liste ist eine echte Einspaltenliste mit Suche, Seltenheitsfiltern, Klassenfiltern, drei Sortieroptionen, Scrollbar, Seltenheitsrahmen und Aufwertungs-Punkt. Es sind nur die acht E1-Helden mit Daten in der GDD-Heldenübersicht enthalten. Namen, Klassen, Seltenheiten, Basiswerte und Fähigkeiten stammen aus der GDD v1.6.13; Stärke nutzt `power_l1` aus `team/ausruestung/sim/data/heroes.csv`. Für normale Helden zeigt die Fragmentanzeige den belegten Freischaltwert von 40 Fragmenten. Ruka und Bako sind als besessen dargestellt; Bako startet laut GDD, Ruka ist die garantierte Tutorial-Beschwörung.

Das D2-Bundle enthielt weder `team/gdd/GDD_v1.6.13.md` noch die Portrait-PNGs. Die GDD wurde aus dem kanonischen Haupt-Checkout gelesen; vorhandene Portrait-PNGs sowie Rukas freigestelltes Ganzkörperbild wurden von dort unter `team/art/heroes/` für diesen Renderer mitgeführt.

Der Zähler „12 von 80“ entspricht der gewünschten Rosterdarstellung. Die aktuell im Checkout belegbaren GDD-E1-Helden ergeben acht konkrete Zeilen; es wurden keine zusätzlichen Namen oder Heldenattrappen ergänzt.

Das Detail verwendet Rukas vorhandene Vollkörpergrafik und die zehn Ausrüstungsplätze der verbindlichen Helden-Detail-Referenz. LP/ATK/DEF sind Rukas Basiswerte aus der GDD-Tabelle. Skillnamen und Beschreibungen sind die dortigen Ultimate- und Passivtexte. Die Slots bleiben leer, damit keine Ausrüstung oder Seltenheit erfunden wird.

## Prüfung

- Renderer prüft benötigte Assets, Screenshot-Abmessungen (1080×1920), nichtleere Ausgabe und Mindestdateigröße.
- Beide Screenshots wurden nach dem Rendern visuell geprüft: ganze HUD-Fläche abgedunkelt, D2-Ressourcenleiste sichtbar, Panel-Rahmen innerhalb der Safe-Zone, Liste einspaltig und scrollbar, Detail- und Aktionsbereiche vollständig innerhalb des Panels.
- Keine Platzhalter- oder Testnamen im sichtbaren Inhalt.

Rendern:

```bash
python3 team/art/hud_d2/_src/render_vorschau_menu_helden_d2_v1.py
```
