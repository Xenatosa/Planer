# Anschluss t139u / t140u (Neubau)

## Ursache p3d (576080b) — Wirkung gegen Null
1. `neu/mesh.py` Variante 2: `weight *= 0.02` nach allen Profilen → max Δh D1 **0,59 mm**, G1 **1,44 mm**; Nahbilder pixelgleich zu VAR=0.
2. Legacy-Gates + `test_beanstandungen.py` lesen **`relief_daten.json.gz` / GB**, nicht `neu_mesh_tiles`. R8=48/R9=334 unverändert ist **kein** Mesh-Beweis.
3. Wand-Abstandsschutz (`wall_weight` ab 1,2 m) hält Terrain am Wandfuß auf GB → sichtbare Stufen trotz gezeichneter Wandmeshes.
4. Viewer **zeichnet** neues Mesh (`RELIEF_NEU_VIEWER=1` → `neu/viewer.js`); gemessen wurde größtenteils Legacy-GB.

## Baseline neues Mesh (p3d Standard VAR=2) — zum Vergleichen, kein Erfolg
- D1: 84 Vertices geändert, max|Δ| 0,000588 m; G1: 209 / 0,001436 m; D2: 0
- LOD1 168600 Dreiecke; Lochscans 0; t42u 0; D2 bytegleich
- Beanstandungen (noch am Legacy-Gate gemessen): Kreuzungsstufe 1,389 m; R8a 24; Delle G1 0,42 m; Sägezahn D1 41; Wandkante 2,24; F1 0,17 m; Schatten 0,307 — alle rot
- VAR=1: größere Profile, aber 6 Clay-Metrikanstiege G1 — verworfen

## Läuft jetzt
- **p3d2** Worktree `/workspace/wt_dorfmap_p3d2`, Branch `art/dorfmap-p3d2` (Basis p3d 576080b)
- Log `/workspace/codex_jobs/log_p3d2.txt`, Ende `ende_p3d2.txt`
- Modell-Log: gpt-6-luna / xhigh (verifiziert)

## Nach ende_p3d2.txt
1. ERGEBNIS_p3d2.md: Ursache-Fix, Mesh-Baseline vor/nach (max|Δ|, Kreuzungsstufe am **neuen** Feld)
2. Prüfen: Tests/Gates lesen neues Mesh; Schwellen unverändert; D2 + Klippe 140|35 erhalten
3. Xvfb-Nahbilder persönlich ansehen (Kreuzung D1, Wandfuss, G1-Anschluss, D2, Wegende)
4. Nur bei sichtbarer+messbarer Verbesserung einzeln mergen; sonst Zahlen, kein Fabian-Kontakt
5. p3d selbst nicht als Mesh-Erfolg nach grundgeruest mergen (Infrastruktur ok, Wirkung Null)

## Nicht tun
Keine globalen Minimalgewichte, keine Schwellenlockerung, keine Legacy-Flicken, keine Löschung, keine Nachricht an Fabian.
