# Codex — Ressourcen v2c: HUD-Aufklappen (23.10.2026 ~22:23)

**Absender:** New Bot · **Fabian:**
„Das Aufklappen ist aber vom Hud In Main Screen und nicht Extra“

v2b ist falsch als Extra-Screen/Lager-Hintergrund gebaut. Es muss wie v2 ein **Bottom-Sheet auf dem Dorf-HUD** sein (öffnet von der Kiste), plus die neuen **+**-Buttons.

## Repo
`/workspace/handygame-plan-ressourcen-v2b` · Branch `art/hud-d2-ressourcen-plus-v2b`

## MUSS
1. Basis = freigegebenes Chrome `vorschau_hud_d2_v7_3_lvl12.png` (Dorf sichtbar darunter).
2. Bottom-Sheet „LAGER“ wie v2 (`overlay_d2_common` / `overlay_d2_v2_common` / `render_vorschau_overlay_ressourcen_d2_v2.py` als Vorlage) — Kiste hervorgehoben als Opener.
3. Pro Zeile die v2b-Features behalten: **+** (aktiv Glut / grau disabled), Text `×N · KISTE/FASS` und `+X.XXX HOLZ/…`.
4. Mock unverändert: Holz ×3 aktiv, Stein ×0 grau, Nahrung ×1 aktiv.
5. **Kein** Vollbild-Lager-BG, kein Extra-Menü-Chrome, kein eigener Tab „RESSOURCEN“ außerhalb HUD.
6. Neue PNG: `vorschau_overlay_ressourcen_d2_v2c.png` (v2b optional behalten als Alt). Renderer `render_vorschau_overlay_ressourcen_d2_v2c.py`. Massplan kurz `massplan_overlay_ressourcen_d2_v2c.md`.
7. Bericht `BERICHT_ressourcen_v2c_hud_sheet_2026-10-23.md` DONE.
8. Commit+Push. Enqueue: `python3 /home/box/bin/job-fertig-enqueue.py ressourcen-v2c "Ressourcen v2c: HUD-Sheet + Einsetzen" team/art/hud_d2/vorschau_overlay_ressourcen_d2_v2c.png --commit $(git rev-parse --short HEAD) --branch art/hud-d2-ressourcen-plus-v2b`

## Nicht ändern
Inventar, Mail, andere Screens. Kein Unity.
