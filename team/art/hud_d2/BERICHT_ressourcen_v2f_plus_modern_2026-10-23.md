# Ressourcen v2f – moderne Plus-Buttons und Produktion pro Stunde

**Status: DONE**  
Datum: 2026-10-23

Das v2e-HUD-Layout bleibt erhalten: das LAGER-Panel klappt oben unter der markierten Kiste auf; Top-Leiste, Seiten-Icons, Dorfhintergrund und aktives Dorf-Dock bleiben sichtbar. Die drei Ressourcen-Karten und ihre Einsetzen-Mengen/Erträge bleiben unverändert.

Die Plus-Flächen sind jetzt 96 × 96 px große abgerundete Quadrate mit Glut-Verlauf, leichter Tiefenkante und klarer Plus-Glyphe. Holz und Nahrung sind aktiv, Stein ist bei `×0` in derselben Form grau/deaktiviert.

Unter den Einsetzen-Zeilen ist die laufende Produktion getrennt ausgewiesen: **GESAMT +1.560 /h**, aufgeschlüsselt als Holz `+420/h`, Stein `+180/h` und Nahrung `+960/h`. Die einmaligen Erträge bleiben separat bei Holz `+2.500`, Stein `+0` und Nahrung `+5.000`.

## Dateien

- Vorschau: `vorschau_overlay_ressourcen_d2_v2f.png` (1080 × 1920)
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v2f.py`
- Maßplan: `massplan_overlay_ressourcen_d2_v2f.md`

## Prüfung

Renderer erfolgreich ausgeführt und PNG visuell geprüft: Plus-Flächen abgerundet und modernisiert, Produktionsbereich klar lesbar, Panel oben im HUD, Dock sichtbar, Stein-Plus grau. v2b–v2e-Dateien wurden nicht verändert.
