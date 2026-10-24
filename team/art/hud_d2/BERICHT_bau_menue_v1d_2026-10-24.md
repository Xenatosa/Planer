# Bericht · BAU-MENÜ D2 v1d

**Status: DONE · 24.10.2026**

**Basis:** `a00e951` · gleicher Branch/Worktree

## Ausgabe

- `vorschau_menu_bau_d2_v1d.png` — Wirtschaft, acht Karten im 2×4-Raster; der angeschnittene Rand zeigt die neunte Karte an
- `vorschau_menu_bau_d2_v1d_scroll.png` — Wirtschaft leicht gescrollt; Zähler 9 von 9
- `vorschau_menu_bau_d2_v1d_detail.png` — Gebäude-Detail wie v1c mit **AUSBAUEN** als einziger Aktion
- `_src/menu_bau_d2_v1d.html` — Layout und Komponenten
- `_src/render_vorschau_menu_bau_d2_v1d.py` — Renderer für alle drei Ansichten

Alle Vorschauen sind 1080×1920 px.

## Umsetzung

Die Karten stehen in zwei Spalten. Acht Karten sind vollständig sichtbar; die Wirtschaftskategorie enthält neun Gebäude und der angeschnittene untere Rand macht den Scrollbereich sichtbar. Die schmale Filterzeile zeigt die aktive Sortierung **Baubar zuerst** sowie den Trefferzähler. Für insgesamt 25 geplante Gebäude zeigen die Reiter die Verteilung Wirtschaft 9, Militär 7, Forschung 4 und Deko 5.

Jede Karte zeigt Variante-B-Gebäudeart, Steinzeit-Namen, Stufe, vier Ressourcenicons mit Kosten und einen Status-Chip. Fehlende Ressourcen sind rot hervorgehoben; gesperrte Gebäude tragen ein Schloss. Im zweiten Listenbild ist die Wirtschaftskategorie leicht nach unten gescrollt.

Die fünf zusätzlich benötigten Variante-B-Gebäude wurden aus `/workspace/handygame-plan/team/art/gebaeude_neu_b/` nach `team/art/gebaeude_neu_b/` kopiert. Alle Gebäudeabbildungen der Vorschauen kommen aus `team/art/gebaeude_neu_b/`.

Bauzeiten, Bauschlange und **SOFORT** kommen nicht vor. Das Detail-Sheet entspricht v1c; **AUSBAUEN** bleibt seine einzige Aktion. Dorf-HUD, D2-Top-Leiste und der vollflächige Scrim folgen der bestehenden v1c/v3g-Referenz.

## Sichtprüfung

Alle drei Bilder wurden mit dem v1d-Renderer neu erzeugt und visuell geprüft. Kartenraster, Kosten, Statuszustände, angeschnittener Listenrand, Scrollposition und Detail-Sheet sind in den Vorschauen erkennbar.
