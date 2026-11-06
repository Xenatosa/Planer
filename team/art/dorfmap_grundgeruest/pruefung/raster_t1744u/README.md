# Raster-Methode t1744u (Phase 1 + Geruest Phase 2)

Stand: Snapshot-Commit 7fe23bf (Branch art/dorfmap-grundgeruest), Viewer-Banner „Ansicht: NEU (Relief t67u, Runde O17)“.
Karte und Zellwerte unveraendert (nur gelesen). Eigener Worktree /workspace/wt_raster.

## Raster
8 Spalten (A–H) × 7 Reihen (1–7) = 56 Felder, je 42 m × 43–44 m (Grenzen x: 0,42,…,336; y: 0,43,87,130,173,216,260,303).
Begruendung: ~42 m entspricht einem Handy-Bildausschnitt, in dem Haeuser (5–16 m), Baeume, Wege, Wandstufen noch erkennbar sind;
feiner (z. B. 12×10 = 120 Felder) waere fuer passt/falsch zu viel Klickarbeit, groeber (6×6 = 56 m) zu klein dargestellt.

## Dateien
- `uebersicht_raster.jpg` – Draufsicht 1080×1355, Raster + Labels.
- `felder/feld_XY.jpg` – 56 Feldbilder 900×809: Schraegansicht von Sueden (?lod=1 → Handy-Stufe LS=2), Textur, gelber Feldumriss, Insetkarte.
- `gruppen/gruppe_Gnn.jpg` – 10 Kontaktboegen (2×3), G10 nur G7+H7.
- `RASTER_INDEX.md/.json` – Feld → Zellbereich, Meterbereich, Bild, Kamera, Commit/Banner. `RASTER_GRUPPEN.json` – Gruppen.
- Erzeugung: `gen_kameras.py` → `kameras_*.json`; `render_kameras.js` (Playwright/SwiftShader, Rohbilder nach /tmp/rr); `gen_raster_bilder.py /tmp/rr`.
- `pruefe_regeln.py` – Kandidaten-Regeln R01–R11 [A], Ausgabe `regeln_lauf/` (treffer.csv/json, zusammenfassung.md/json).

## Grenzen
- Gelber Umriss ist nachtraeglich projiziert (Gelaendehoehe leicht geglaettet), ohne Verdeckung: vor dem Feld stehende Haeuser/Baeume koennen Teile verdecken (z. B. F3).
- Reihe 1: obere Bildhaelfte ist Himmel/Hintergrund (Kartenrand Nord).
- Rohbilder (PNG) nicht eingecheckt (in /tmp/rr, reproduzierbar).
- pruefe_regeln.py: alle Regeln/Schwellen ungeeicht [A]; Objekthoehen ohne Browser-Feinband-Korrektur (t59u); R03 zaehlt auch Stuecke von WASSER_FARBE; R11 zaehlt Einzelzellen bebaubar/Bauzone. Kein Ersatz fuer Fabians Urteil.
