# Bericht · BAU-MENÜ D2 v1c

**Status: DONE · 24.10.2026**

**Basis:** `3a821f5` · gleicher Branch/Worktree

## Ausgabe

- `vorschau_menu_bau_d2_v1c.png` — Übersicht mit vier vergrößerten Gebäudekarten
- `vorschau_menu_bau_d2_v1c_detail.png` — Detail-Sheet Holzfällerlager mit vollbreitem **AUSBAUEN**-Button
- `_src/menu_bau_d2_v1c.html` — Layout und Komponenten
- `_src/render_vorschau_menu_bau_d2_v1c.py` — Renderer für beide Ansichten

Beide Vorschauen sind 1080×1920 px.

## Umsetzung

Gemäß GDD v1.6.13 und Fabian F3 (14.10.2026) erfolgt Bauen sofort. Entfernt wurden sämtliche Bauzeit- und Uhranzeigen, die Baumeister-/Bauschlangen-Leiste sowie der **SOFORT**-Button mit Zeitkristallkosten. Im Detail-Sheet steht die Bauzeit nicht mehr bei den Kosten oder auf der Aktion.

Der frei gewordene Platz vergrößert die vier vorhandenen Gebäudekarten samt Art-Wells und Kostenkacheln. Die Karten füllen das Panel ohne leere Fläche am unteren Rand. Im Detail-Sheet ist **AUSBAUEN** die einzige Aktion und belegt die volle verfügbare Breite.

Kategorie-Reiter, Gebäudedaten, Kosten, Statuszustände, Hintergrund-HUD, Scrim und Stil folgen v1b.

## Sichtprüfung

Beide Vorschauen wurden neu gerendert und visuell geprüft. Liste und Detail-Sheet liegen vollständig innerhalb des Panels; die Dock-Leiste bleibt sichtbar.
