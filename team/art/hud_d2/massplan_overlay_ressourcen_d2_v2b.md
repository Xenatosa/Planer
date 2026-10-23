# Massplan Ressourcen-Overlay D2 – v2b

Stand: 23.10.2026 · baut auf der Ressourcenliste aus HUD D2 v2 auf.

## Änderung

Jede der drei Lagerzeilen erhält rechts einen runden `+`-Knopf zum Einsetzen vorhandener Kisten/Fässer. Der Bestand und der beispielhafte Ertrag stehen direkt links davon. Der `+`-Knopf ist 96×96 px groß und damit vollständig als Touchfläche nutzbar. Bei 0 Items ist er grau und deaktiviert.

## Vorschau und Quelle

- Vorschau: `vorschau_overlay_ressourcen_d2_v2b.png` (1080×1920)
- Elementdaten: `massplan_overlay_ressourcen_d2_v2b_elemente.json`
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v2b.py`
- Der ältere Ressourcen-Massplan v2 und eine v2-PNG werden nicht verändert.

## Positionen (px, 1080×1920)

| ID | Element | x | y | w | h | Hitbox / Hinweis |
|---|---|---:|---:|---:|---:|---|
| BG | Gedimmter, weichgezeichneter Lager-Hintergrund | 0 | 0 | 1080 | 1920 | Kontext für das Overlay |
| RB | Ressourcen-Schaltfläche, geöffnet | 172 | 194 | 300 | 120 | 300×120 |
| RBI | Ressourcen-Icon | 188 | 222 | 64 | 64 | Kiste-Asset |
| RBC | Chevron nach oben | 430 | 245 | 24 | 15 | Offener Zustand |
| P0 | Lagerliste | 172 | 326 | 600 | 448 | D2 dunkles Panel, Bronze-Kontur |
| P0H | Kopf „LAGER“ und Unterzeile | 196 | 339 | 552 | 40 | Baloo 25 / 15 |
| L1 | Zeile Holz | 184 | 390 | 576 | 120 | Inhalt 456×120, rechts eigener Plus-Hitbereich |
| L1I | Icon Holz | 196 | 414 | 72 | 72 | Vorhandenes D2-Inventar-Asset |
| L1N | Name Holz | 284 | 403 | 136 | 32 | Baloo 25 |
| L1Q | Lagerbestand / Kapazität Holz | 284 | 436 | 136 | 24 | 12.480 / 20.000 |
| L1B | Lagerbalken Holz | 284 | 472 | 136 | 12 | 62,4 % gefüllt |
| L1U | Item-Menge und Ertrag Holz | 436 | 418 | 200 | 52 | `×3 · KISTE` / `+2.500 HOLZ` |
| L1P | Plus Holz | 652 | 402 | 96 | 96 | Aktiv, orange |
| L2 | Zeile Stein | 184 | 510 | 576 | 120 | Inhalt 456×120, rechts eigener Plus-Hitbereich |
| L2I | Icon Stein | 196 | 534 | 72 | 72 | Vorhandenes D2-Inventar-Asset |
| L2N | Name Stein | 284 | 523 | 136 | 32 | Baloo 25 |
| L2Q | Lagerbestand / Kapazität Stein | 284 | 556 | 136 | 24 | 8.215 / 20.000 |
| L2B | Lagerbalken Stein | 284 | 592 | 136 | 12 | 41,1 % gefüllt |
| L2U | Item-Menge und Ertrag Stein | 436 | 538 | 200 | 52 | `×0 · FASS` / `+0 STEIN` |
| L2P | Plus Stein | 652 | 522 | 96 | 96 | Deaktiviert, grau |
| L3 | Zeile Nahrung | 184 | 630 | 576 | 120 | Inhalt 456×120, rechts eigener Plus-Hitbereich |
| L3I | Icon Nahrung | 196 | 654 | 72 | 72 | Vorhandenes D2-Inventar-Asset |
| L3N | Name Nahrung | 284 | 643 | 136 | 32 | Baloo 25 |
| L3Q | Lagerbestand / Kapazität Nahrung | 284 | 676 | 136 | 24 | 14.900 / 20.000 |
| L3B | Lagerbalken Nahrung | 284 | 712 | 136 | 12 | 74,5 % gefüllt |
| L3U | Item-Menge und Ertrag Nahrung | 436 | 658 | 200 | 52 | `×1 · FASS` / `+5.000 NAHRUNG` |
| L3P | Plus Nahrung | 652 | 642 | 96 | 96 | Aktiv, orange |

## Darstellung und Zustände

- Hintergrund, Panels, Konturen und Textfarben folgen D2 „Obsidian & Glut“.
- Ressourcensymbole und Schriftdateien stammen aus dem vorhandenen Inventar-v4-Asset-Set.
- Item-Zeile 1: 3 Kisten, Ertrag +2.500 Holz; Plus aktiv.
- Item-Zeile 2: 0 Fässer, Ertrag +0 Stein; Plus grau/deaktiviert.
- Item-Zeile 3: 1 Fass, Ertrag +5.000 Nahrung; Plus aktiv.
- Zeileninhalt und Plus-Fläche haben getrennte Hitboxen: Zeileninhalt 456×120, Plus 96×96.

## Umsetzung

Die v2b-Dateien ergänzen die bestehende Lagerliste. Alle vorhandenen v2-Dateien bleiben unberührt.
