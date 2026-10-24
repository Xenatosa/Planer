# Ressourcen v3c – 12 Kacheln ohne Scrollen

**Status: DONE**  
Datum: 2026-10-24

Das Lagerpanel zeigt zwölf Ressourcen-Kacheln gleichzeitig in einem festen 3×4-Raster im Dorf-HUD. Alle vier Reihen sind im 1080×1920-Bild sichtbar. Es gibt keine Scrollfläche, kein Sparkline/Diagramm und keinen Extra-Screen. Das ist ein statischer UI-Kapazitätstest; die normale Acht-Slot-Regel bleibt unverändert.

Die gefüllten Mock-Slots zeigen Bestand/Kapazität, schlanken Füllbalken, Einsetzen-Stack/-Ertrag und Produktion pro Stunde: Nahrung, Holz, Stein, Muscheln (Gold-Skin), Wissen, Bernstein, Metall und Epochenmarken. Die vier weiteren Plätze Runen, Artefakte, Reliquien und Essenz sind als gesperrte Platzhalter dargestellt. Stein hat Bestand, aber `×0 FASS`; sein Einsetzen-CTA ist grau/deaktiviert.

Gesamtproduktion: **+1.916/h**. HUD-Top-Leiste, Avatar/Level, markierte Kiste, Seiten-Icons und Dorf-Dock bleiben sichtbar. Der Scrim liegt im Spielfeld bei 66,7% Deckkraft.

## Dateien

- Vorschau: `vorschau_overlay_ressourcen_d2_v3c.png` (1080 × 1920)
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v3c.py`
- Maßplan: `massplan_overlay_ressourcen_d2_v3c.md`

## Prüfung

Renderer erfolgreich ausgeführt und PNG visuell geprüft: alle zwölf Kacheln sichtbar, kein Scrollen, keine Diagramme/Sparklines; aktive Mengen/Erträge und Produktionsraten lesbar; Stein-CTA grau; HUD-Kopf und Dock sichtbar.
