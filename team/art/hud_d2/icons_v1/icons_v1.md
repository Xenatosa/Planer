# HUD D2 Icons v1 — vollständig (60)

Stand: 23.10.2026 Europe/Berlin. Stil D2 „Obsidian & Glut“, von Fabian freigegeben (Muster v1).

## Ablage

`team/art/hud_d2/icons_v1/`

- **60 Masters** `d2_ico_*.png` — 256×256 PNG RGBA, 8 % Padding
- **Übersicht** `uebersicht_icons_v1.png` (Raster 10×6 auf `#1A120C`)
- **Raws** `_raw/*_raw.png` (48 Batch-Ergebnisse; 6 Muster ohne neuen Raw)
- **Refs** `_refs/d2_helden_style_512.png` (Stil-Crop für Batch-Payload)

Quelle der Motiveliste: `../icon_liste_hud_d2_v1.md`.

## Herstellung

| Quelle | Anzahl | Kosten USD |
|---|---|---|
| Muster v1 (freigegeben, kopiert) | 6 | 0.2887 (früher) |
| Batch Nano Banana 1K (−50 %) | 48 | 1.1952 |
| Dock-inaktiv abgeleitet (entsättigt/gedämpft) | 6 | 0 |
| **Summe API** | **54 Gen** | **1.4839** |

Batches:
- `batches/iastxlvdv4b6uwekzgpumsymxewom5xhm9fb` (24)
- `batches/4fpti50j6yf78x9yjw9hd7rdfykgwoya4cnp` (24)

Bot: `New Bot`. Freistellen: `_src/freistell_magenta_icon.py`. Inaktiv: `_src/derive_dock_inaktiv.py`. Post: `_src/postprocess_icons_v1.py`.

Muster übernommen (nicht neu generiert):
`zeitkristall`, `kiste`, `beschwoeren`, `dock_helden`, `bauen`, `mail`.

Dock-inaktiv abgeleitet von aktiv: `dorf`, `helden`, `karte`, `armee`, `gilde`, `inventar`.

## QA

- Alle 60 Dateinamen der Liste vorhanden
- Ecken alpha 0, keine Magenta-Reste (Skript-Check)
- SynthID nicht entfernt (nur Keying)

## Hinweis

PNGs oft von `.gitignore` ausgeschlossen — lokal unter dem Pfad oben. Metadaten/Skripte auf `main` committen.
