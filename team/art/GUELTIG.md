# Gültige Vorlagen (Stand 22.10.2026, gepflegt von Epochen Archiv)

Nur diese Fassungen werden umgesetzt. Alles unter `_alt/` ist überholt (Protokoll: `_alt/VERSCHOBEN.txt`).
Regel: Vor jedem Auftrag hier prüfen, nichts doppelt bauen.
Begriffe: **Dorfkarte** = scrollbares Dorf mit Umgebung. **Weltkarte** = große Karte, Dorf nur als Symbol.

| Bereich | Gültige Datei(en) | Status |
|---|---|---|
| UI D2 „Obsidian & Glut“ | `ui-kit/menus_v3/vorlage_D2.md`, `ui-kit/menus_v3/vorlage_D2_export/`, `ui-kit/menus_v3/vorlage_D2_layout_helden.csv` | verbindlich |
| Helden-Detail v2 | `ui-kit/menus_v3/v3_2_obsidian_helden_detail_v2.png` (Quelle `_src/html/v3_2_obsidian_helden_detail_v2.html`) | maßgeblich |
| Bauen / Armee | `ui-kit/menus_v3/v3_2_obsidian_bauen.png`, `ui-kit/menus_v3/v3_2_obsidian_armee.png` | verbindlich |
| Menüband (Dock A) | `ui-kit/dock_v1/dock_A.png` in D2-Tönung: braun, aktive Platte Glut-Orange, kein Blau | verbindlich |
| HUD (Dorf: Top-Leiste, Quest-Leiste, Dock) | `ui-kit/menus_v3/vorlage_D2.md`, `ui-kit/menus_v3/v3_2_obsidian_helden_detail_v2.png`, `ui-kit/menus_v3/v3_2_obsidian_bauen.png`, `ui-kit/menus_v3/v3_2_obsidian_armee.png` + `ui-kit/dock_v1/dock_A.png` (D2 warmes Dunkelbraun, aktive Platte Glut-Orange, kein Blau, keine Gold-Kerbe). Dorf-HUD und Icons werden neu in D2 erstellt | verbindlich |
| ~~HUD v5 / v5.7 inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`~~; HUD v6 | `_alt/ui-kit/hud/` | **gestrichen** (Fabian 22.10.2026), nie wieder verwenden |
| Karten-Konzept E1 (einzig gültig für Dorf- und Weltkarte) | `karten_konzept/karte_e1_schema.png`, `karten_konzept/dorfplan_e1_schema.png`, `karten_konzept/gelaende_dorf_e1.md` | verbindlich |
| Weltkarte im Spiel | `weltkarte/bg_v2/` (im Spielcode als e1_seg) | veraltet, wird ersetzt |
| Gebäude freigestellt (ohne Boden, Regel 22.10.) | `gebaeude_frei/ui/buildings/*_frei.png` (50 Dateien; hut bp07/bp10 und storage bp04/bp10 nur **v002**; Canvas je Typ einheitlich, Silhouette mittig, 8 px Rand unten, Pivots `gebaeude_frei/pivots.csv`; siehe `gebaeude_frei/befundliste.md`) | gültig |
| Gebäude freigestellt, v001-Dubletten | `_alt/gebaeude_frei_v001_ueberholt_20261022/` (hut_bp07/bp10_v001, storage_bp04/bp10_v001) | überholt |
| Gebäude freigestellt, alter Lauf | `_alt/cx_geb_frei_ueberholt_20261022/` (früher `/workspace/cx/geb_frei/`) | überholt |

## Hinweis
Alle früheren Dorf- und Weltkarten-Bilder (u. a. dorfkarte_e1_v4, weltkarte_b1_v4, mockup_b1_v1, Nebel-Layer, mockup_e1_v1) liegen seit 22.10.2026 in `_alt/`.


## Rule: decorations and buildings without ground (Fabian, 22.10.2026)
ALL decorations and buildings are always made WITHOUT ground: no base plate, no plinth, no patch of earth or snow, cut out with a transparent background. The ground is separate (village map or its own ground tiles). Check by script (0 $) before every delivery: alpha edge without a ground patch.

## Regel Dorfkarte: organisch, kein NW-Gletscher (Fabian via New Bot, 22.10.2026 17:33)
- Die Dorfkarte darf keinen quadratischen oder rechteckigen Eindruck machen; die Ränder lösen sich organisch auf (Wald, Gelände, Nebel), kein Rahmen, keine harte Kante.
- Felsen sind organisch (Vorsprünge, Buchten, Geröll), keine Blöcke und keine geraden Kanten.
- Kein Gletscher und kein blaues Eis im Nordwesten.
- Maßplan in Arbeit: karten_konzept/massplan_v3_7 (noch nicht freigegeben).
