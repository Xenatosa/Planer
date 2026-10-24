# Codex — Ressourcen v2d: v2b-Style auf HUD-Sheet (23.10.2026 ~22:35)

**Absender:** New Bot · **Fabian** (Reply auf v2b-Screen):
„vom style fande ich besser also übernehme den style in den hud“

## Ziel
HUD-Aufklappen bleibt (wie v2c: Chrome `vorschau_hud_d2_v7_3_lvl12.png` + Bottom-Sheet über Dorf).
**Visueller Style** von v2b übernehmen: Kartenzeilen, Typo, Plus-Buttons, Item-Zeilen (`×N · KISTE/FASS`, `+X.XXX NAME`), Farben/Gradient, Abstände — nicht das flache v2c-Panel.

## Repo
`/workspace/handygame-plan-ressourcen-v2b` · Branch `art/hud-d2-ressourcen-plus-v2b`

## Referenzen
- Style: `render_vorschau_overlay_ressourcen_d2_v2b.py` + `vorschau_overlay_ressourcen_d2_v2b.png`
- HUD-Struktur: `render_vorschau_overlay_ressourcen_d2_v2c.py` + Chrome

## MUSS
1. Basis = HUD Chrome, Bottom-Sheet, Dorf/Dock sichtbar (kein Extra-Vollbild-BG).
2. Sheet-Innenraum im v2b-Look (dunkle Kartenzeilen, Bronze/Glut, große Plus-Buttons 96px, Item+Ertrag-Text rechts der Werte).
3. Mock unverändert: Holz ×3 aktiv, Stein ×0 grau, Nahrung ×1 aktiv.
4. PNG: `vorschau_overlay_ressourcen_d2_v2d.png`. Renderer `…_v2d.py`. Kurzer Massplan/Bericht `BERICHT_ressourcen_v2d_style_2026-10-23.md` DONE.
5. Commit+Push. Enqueue: `python3 /home/box/bin/job-fertig-enqueue.py ressourcen-v2d "Ressourcen v2d: v2b-Style auf HUD-Sheet" team/art/hud_d2/vorschau_overlay_ressourcen_d2_v2d.png --commit $(git rev-parse --short HEAD) --branch art/hud-d2-ressourcen-plus-v2b`

## Nicht ändern
Inventar/Mail/andere Screens. Unity nein.
