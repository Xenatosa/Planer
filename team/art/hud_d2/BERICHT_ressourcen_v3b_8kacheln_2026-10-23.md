# Ressourcen v3b – acht Slots ohne Scrollen

**Status: DONE**  
Datum: 2026-10-23

Das Ressourcenlager zeigt jetzt alle acht Slots in einem festen 2×4-Raster im Dorf-HUD. Es ist keine Scrollfläche vorhanden; Sparklines und Diagramme sind entfernt. Top-Währungsleiste, Avatar/Level, Seiten-Icons und Dorf-Dock bleiben sichtbar. Die Kiste im oberen HUD ist markiert.

Die fünf gefüllten Slots zeigen Bestand/Kapazität, schlanken Füllbalken, Produktionsrate pro Stunde sowie Einsetzen-Stack und Ertrag. Nahrung, Holz, Muscheln (Gold-Skin) und Wissen haben aktive Glut-CTAs. Stein zeigt `×0 FASS`, `+0` und einen grauen/deaktivierten CTA. Bernstein, Metall und Epoche sind klar als gesperrte/leer markiert.

Gesamtproduktion: **+1.647/h** (Nahrung +960, Holz +420, Stein +180, Muscheln +12, Wissen +75). Der Scrim auf dem Spielfeld liegt bei 66,7% Deckkraft; HUD-Kopf und Dock sind nicht abgedunkelt.

## Dateien

- Vorschau: `vorschau_overlay_ressourcen_d2_v3b.png` (1080 × 1920)
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v3b.py`
- Maßplan: `massplan_overlay_ressourcen_d2_v3b.md`

## Prüfung

Renderer erfolgreich ausgeführt und PNG visuell geprüft: alle acht Karten sind gleichzeitig sichtbar; es gibt kein Scrollen, kein Sparkline/Diagramm und keinen Extra-Screen. HUD-Top, Avatar und Dock bleiben sichtbar; die Einsetzen-Aktion für Stein ist grau/deaktiviert.
