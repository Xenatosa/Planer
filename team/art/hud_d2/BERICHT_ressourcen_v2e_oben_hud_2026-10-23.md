# Ressourcen v2e – oben im Dorf-HUD

**Status: DONE**  
Datum: 2026-10-23

Das Lager klappt in der Vorschau von der markierten Kiste im Dorf-HUD auf. Das Panel sitzt direkt unter den oberen Quick-Icons und verwendet den Karten-, Bronze-, Typografie- und Plus-Button-Stil aus v2b. Die Top-Ressourcenleiste, Avatar/Level, Seiten-Icons und das aktive Dorf-Dock bleiben sichtbar. Der Dorfhintergrund bleibt um das Panel herum sichtbar.

Holz zeigt `×3 · KISTE` und `+2.500 HOLZ` mit aktivem Glut-Plus. Stein zeigt `×0 · FASS` und `+0 STEIN` mit grauem deaktiviertem Plus. Nahrung zeigt `×1 · FASS` und `+5.000 NAHRUNG` mit aktivem Glut-Plus.

## Dateien

- Vorschau: `vorschau_overlay_ressourcen_d2_v2e.png` (1080 × 1920)
- Renderer: `_src/render_vorschau_overlay_ressourcen_d2_v2e.py`
- Maßplan: `massplan_overlay_ressourcen_d2_v2e.md`

## Prüfung

Renderer erfolgreich ausgeführt und PNG visuell geprüft: vollständiger HUD-Chrome mit sichtbarer Top-Leiste und Dock, Lagerpanel oben unter der Kiste, Hintergrund sichtbar, kein Lager-Vollbild und kein Bottom-Sheet. Der Stein-Plus-Button ist grau/deaktiviert.
