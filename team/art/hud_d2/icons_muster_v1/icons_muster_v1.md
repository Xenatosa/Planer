# HUD D2 Icons — Muster v1 (zur Stil-Freigabe)

Stand: 23.10.2026 (Europe/Berlin). Stil D2 „Obsidian & Glut“.  
**Nur 6 Muster** — nicht die volle Liste (60). Nach Freigabe durch Fabian folgen die restlichen Icons.

## Ablage

Ordner: `team/art/hud_d2/icons_muster_v1/`

| Datei | Motiv | Kosten USD |
|---|---|---|
| `d2_ico_zeitkristall.png` | Facettierter Obsidian-Splitter, Glutkern, Funken | 0.0463 |
| `d2_ico_kiste.png` | Weidenkiste mit Fell, Stein/Holz, Glut-Spalt | 0.0523 |
| `d2_ico_beschwoeren.png` | Schamanen-Trommel, Spiralmuster, Glutrauch | 0.0478 |
| `d2_ico_dock_helden.png` | Schädel-Helm mit Hörnern/Federn, Glutaugen | 0.0483 |
| `d2_ico_bauen.png` | Steinhammer Lederbindung, Glutfunken, schräg | 0.0479 |
| `d2_ico_mail.png` | Birkenrinde-Rolle, Lederband, Feder-Siegel | 0.0461 |
| `uebersicht_muster_v1.png` | 6 Icons nebeneinander auf `#1A120C` | — |
| `*_crop200.png` | 512×512 nearest-Upscale je Icon (QA) | — |

**Gesamtkosten Generierung:** 0.2887 USD (Nano Banana 1K, Bot „New Bot“).  
Monatsbudget danach: siehe `python3 tools/nanobanana/nb.py status`.

## Technik

- Master: 256×256 PNG RGBA, Motiv ~85 %, 8 % Padding
- Generiert mit Magenta-Chromakey `#FF00FF`, freigestellt via `_src/freistell_magenta_icon.py` (OpenCV/NumPy-Key, Feather 1–2 px)
- Refs: `d2_btn_primaer_normal.png`, `v3_2_obsidian_helden_detail_v2.png`, `e1_bld_hut_bp04_v002_frei.png`
- Prompt-Logs: `team/art/prompt-logs/d2_ico_*_20261023-*.json`
- Raws: `icons_muster_v1/_raw/` (lokal)

## Hinweis

Muster zur Freigabe, Stil D2. Keine weiteren Icons erzeugen, bis Fabian ok sagt oder Korrekturen nennt.
