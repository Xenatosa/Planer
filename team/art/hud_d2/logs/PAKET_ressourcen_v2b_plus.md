# Codex — Ressourcen Overlay v2b: + zum Einsetzen (23.10.2026 ~22:08)

**Absender:** New Bot · **Fabian:**
Pro Ressourcen-Zeile (Holz/Stein/Nahrung) ein **+**-Button zum Einsetzen von Kisten/Fässern o.ä.:
- sichtbar: wie viele Items man hat + wieviel die Ressource bringt
- **+ grau / disabled**, wenn man keine Items hat

## Repo
`/workspace/handygame-plan-ressourcen-v2b` · Branch `art/hud-d2-ressourcen-plus-v2b` (von Inventar v4g)

## Basis
- Renderer: `team/art/hud_d2/_src/render_vorschau_overlay_ressourcen_d2_v2.py`
- Massplan: `massplan_overlay_ressourcen_d2_v2.md` (+ elemente.json)
- PNG: `vorschau_overlay_ressourcen_d2_v2.png`
- Stil: D2 Obsidian & Glut, Chrome v7.3b, Sheet wie v2

## MUSS
1. Pro Zeile rechts (oder neben der %-Anzeige) ein runder **+**-Button (Touch ≥96 px ideal, mind. klar tippbar).
2. Neben/unter dem +: kurze Info **Item-Bestand × Ertrag**, z. B. `×3  · +2.500` oder `3× Fass · +2.500 Holz`. Layout muss lesbar bleiben, nicht gequetscht.
3. Mock-Daten (Beispiel, klar unterscheidbar):
   - Holz: **hat** Kisten/Fässer (z. B. 3×, +2.500) → + **aktiv** (Glut/Orange)
   - Stein: **0** Items → + **grau / disabled**
   - Nahrung: **hat** Items (z. B. 1×, +5.000) → + aktiv
4. Visuell: graues + = keine Items; aktives + = hat Items. Kein Fake-„Shop“-Text.
5. Massplan v2b aktualisieren (`massplan_overlay_ressourcen_d2_v2b.md` + elemente + Renderer `render_vorschau_overlay_ressourcen_d2_v2b.py` **oder** v2 in-place erweitern und Dateien als v2b speichern). Neue PNG: `vorschau_overlay_ressourcen_d2_v2b.png` (v2-PNG nicht überschreiben).
6. Optional zweite PNG `…_v2b_leer.png` nur wenn sinnvoll — sonst reicht eine Vorschau mit gemischtem Zustand (Holz/Nahrung aktiv, Stein grau).
7. Bericht `BERICHT_ressourcen_v2b_plus_2026-10-23.md` mit DONE.
8. Commit + Push Branch `art/hud-d2-ressourcen-plus-v2b`.
9. Am Ende: `python3 /home/box/bin/job-fertig-enqueue.py ressourcen-v2b "Ressourcen v2b: + Einsetzen (grau wenn leer)" team/art/hud_d2/vorschau_overlay_ressourcen_d2_v2b.png --commit $(git rev-parse --short HEAD) --branch art/hud-d2-ressourcen-plus-v2b`

## Nicht ändern
Inventar, Mail, Gilde, Reveal, Chrome, andere Overlays. Kein Unity-Code/PR.
