# Ressourcen v3 – neuer Lageraufbau im Dorf-HUD

**Status: DONE**  
Datum: 2026-10-23

v3 ersetzt die Listen-/Soft-Square-Anmutung durch eine neue horizontale Speichermatrix: drei große Obsidian-Kacheln mit radialem Bestandsring und Produktions-Sparkline, jeweils eigenem Kisten-/Fass-Stapel und kantigem Einsetzen-CTA mit Hex-Plus. Ein separater Live-Fuß zeigt die Gesamtproduktion und die Raten pro Ressource.

Das Lager wird weiterhin von der hervorgehobenen HUD-Kiste geöffnet. Top-Währungsleiste, Avatar/Level, Side-Icons, Dorfhintergrund und Dock bleiben sichtbar. Die Vorschau verwendet ausschließlich den HUD-Chrome; es gibt keinen Extra-Screen und kein Warehouse-Hintergrundbild.

## Mock-Inhalte

- Holz: 12.480 / 20.000, ×3 · KISTE, Einsetzen +2.500, Produktion +420/h.
- Stein: 8.215 / 20.000, ×0 · FASS, Einsetzen +0; CTA grau/deaktiviert, Produktion +180/h.
- Nahrung: 14.900 / 20.000, ×1 · FASS, Einsetzen +5.000, Produktion +960/h.
- Gesamtproduktion: **+1.560/h**.

## Dateien

- Vorschau: `vorschau_overlay_ressourcen_d2_v3.png` (1080 × 1920)
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v3.py`
- Maßplan: `massplan_overlay_ressourcen_d2_v3.md`

## Prüfung

Renderer erfolgreich ausgeführt und PNG visuell geprüft: neuer Kachel-Aufbau klar verschieden von v2f; HUD-Chrome mit Top-Leiste, Avatar und Dock sichtbar; Scrim hinter dem Text stark abgedunkelt; Einsetzen-Menge und einmaliger Ertrag pro Ressource lesbar; stündliche Raten und Gesamt ausgewiesen; Stein-Aktion grau/deaktiviert.
