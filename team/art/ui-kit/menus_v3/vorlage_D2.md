# Vorlage D2 „Obsidian & Glut“ – UI-System für alle Menüs (Dev UI)

**Stand:** 17.10.2026, nachts. **Entscheidung Fabian (21:32):** D2 wird die Vorlage für ALLE Menüs. Es ersetzt die alten Menüs im Build (dunkelviolett, lila Rahmen, Cremekacheln). Reihenfolge der Umsetzung: **Helden → Bauen → Armee**, danach alle weiteren Menüs.
**Abnahme:** Art Director und Kritiker haben diese Vorlage noch nicht abgenommen. Laut Modern-Gate geht vor beiden Haken nichts in die APK.

**Referenzen (alle in `team/art/ui-kit/menus_v3/`):**
- Mocks: `v3_2_obsidian_helden_detail_v2.png` (Helden-Detail im D4-Layout, maßgeblich), `v3_2_obsidian_bauen.png`, `v3_2_obsidian_armee.png`. `v3_2_obsidian_helden_detail.png` ist der alte Stand und nur Referenz.
- Quellen: `_src/d2_dark.py` (CSS = Single Source dieser Werte), `_src/d2v2_helden.py`, `_src/common.py` (Dock).
- Sprites: `vorlage_D2_export/` mit `manifest_9slice.json` (Slice-Ränder), erzeugt von `_src/export_9slice_d2.py`.
- Layout Helden-Detail: `vorlage_D2_layout_helden.csv`.
- Texte und Werte (Mock): `config/menus_v3_mock_strings.json`.

---
## 1. Grundsätze
- **Look:** warmschwarzer Obsidian, Bronze-Ränder, Glut-Orange nur für Aktionen, Auswahl und Hervorhebung. Seltenheitsfarben an Slots und Tooltips. Tooltip im Diablo-Stil (Rand in Seltenheitsfarbe, Rauten an den oberen Ecken). Runde Comic-Schrift (Lilita One / Baloo 2) statt Serifen.
- **Keine Glas-Optik** in den Inhalten. Glas gibt es nur im Dock („Dunkles Glas“, Fabians Wahl).
- **Kein Halo:** hinter Figuren nie Ringe, Strahlen oder Leuchtscheiben, nur `d2_schatten_boden`.
- **Vollbild-Screens:** Sichtbar sind nur Top-Ressourcenleiste, Screen-Inhalt und Dock. Keine Quest-Leiste, keine Seiten-Icons, das Dorf ist nicht zu sehen.
- **Alle Texte** kommen aus `ui_strings.csv`, alle Werte aus der Config bzw. den gdd-CSVs. Nichts ist ins Bild gebacken (Sprites sind textfrei).
- **Regel B – Inhalte bleiben in ihrer Box (Fabian 22:15, fest):**
  - Jedes Bild, Icon und jeder Text liegt vollständig innerhalb seiner Box (Panel, Karte, Slot, Tooltip, Leiste, Träger, Kachel). **Nichts ragt über einen Rahmen.**
  - **Innenabstand mindestens 12 px** vom Außenrand der Box bis zur Inhaltskante (Bild-Rect bzw. Text-Glyphenbox) in allen Containern.
  - Kompakt-Steuerelemente bis 80 px Höhe (Pill, Chip, Tab, Knopf, Plus-Knopf): mindestens 6 px vertikal und 12 px horizontal (Text) bzw. 8 px (Icon in der Pill).
  - **Einzige Ausnahmen sind definierte Badges** (im Code `data-badge`): Stufen-Badge im Slot, Zähler-Badge am Tab, Sperr-Chip im Slot, Stufenzahl/Schloss in der Skill-Kachel. Auch sie liegen in diesem Mock innen (4 px vom Slotrand). Ein Badge darf höchstens 8 px überstehen, und nur wenn das in Abschnitt 7 so steht. Auswahlring (`d2_slot_auswahl_ring`) und die aktive Dock-Platte sind Overlays, kein Inhalt.
  - Unsichtbare Hitboxen dürfen größer als das sichtbare Element sein (z. B. Plus-Knopf 80 sichtbar / 120 Hitbox). Sie zählen nicht als Überstand.
  - Prüfung: `_src/check_boxes.py <html>` meldet `UEBERSTAND` und `PAD<12`. Stand 17.10. 22:30: 0 Befunde in Helden-Detail v2, Helden-Detail, Bauen und Armee.

## 2. Canvas, Safe Area, Raster
- Referenz-Canvas **1080×1920**, Canvas Scaler „Scale With Screen Size“, Match 0.5 (wie HUD v5).
- **Safe Area:**
  - Top-Anker zählen ab der oberen Safe-Kante, Bottom-Anker (Dock) ab der unteren.
  - Hintergrund (`d2_bg_screen_1080x1920`) und Dock-Hintergrund füllen den Bereich außerhalb der Safe Area mit.
  - Die Gestenleiste liegt im Dock (y 188 ab Dock-Oberkante).
- **Vertikale Zonen** (ab Safe-Top):

| Zone | y von–bis | Höhe |
|---|---|---|
| Top-Ressourcenleiste | 0–132 | 132 |
| Kopf (Zurück, Titel/Name, Chips, Kennzahl rechts) | 138–290 | ca. 152 |
| Inhalt (scrollbar) | 290–1676 | 1386 |
| Freiraum über dem Dock (aktive Platte ragt 26 px hoch) | 1676–1708 | 32 |
| Dock (bottom-anchored) | 1708–1920 | 212 |

- **Raster:**
  - Außenrand links und rechts **28 px**, nutzbare Breite **1024 px**.
  - 12 Spalten à 72 px mit 16 px Gutter (12×72 + 11×16 = 1016, Rest 8 px als zusätzlicher Rand).
  - Zweispaltig: 2 × 504 bzw. 584 + 422 (Werte und Tooltip).
- **Abstände (Tokens):** 4 · 8 · 10 · 12 · 16 · 24 · 28 · 32.
  - Abstand zwischen Elementen in einer Zeile: 10–16.
  - Abstand zwischen Blöcken: 16.
  - Innenabstand in Panels: 20–24.
  - Abstand in Listen: 8 (Karte 150, Zeilenhöhe 158).
- **Listenende:** Am Ende jeder Scroll-Liste mindestens **220 px** Padding (Kritiker K6). Keine Karte darf vom Dock abgeschnitten werden.
- **Touch-Ziele:** mindestens **120×120 px** (Knöpfe, Tabs, Slots 150, Mengenwähler, Plus, Zurück/Schließen). Die ganze Listenkarte ist antippbar.

## 3. Farbpalette (Hex aus den CSS-Quellen)
| Token | Hex | Verwendung |
|---|---|---|
| `bg.base.top` / `bg.base.bottom` | #120E0C / #0B0908 | Grundverlauf unter der Höhlentextur |
| `bg.dim` | #0A0807, Alpha 55 % → 35 % (bei 40 %) → 60 % | Abdunkelung über dem Hintergrund |
| `panel.top` / `panel.bottom` | #2C201A / #120D0B, Alpha 94 % | Panel-Verlauf (`d2_panel_frame`) |
| `line.bronze` | #C98A4A | Panelrand, Porträtrand |
| `line.bronze.light` | #C9A96E | Rauten an Panel-Ecken (Füllung #1A1310) |
| `line.muted` | #8A7656 | Pills, Chips, Fragmentträger, Dock-Linie in D2-alt |
| `line.dark` | #7A664E (Kritiker K6, vorher #5A4A36) | inaktive Tabs, Listenkarten, gesperrt, Balkenrand |
| `text.counter` | #A89674 (K6) | Zähler, Kategorie-Anzahl, Text gesperrt, Scrollbar-Daumen, Checkbox-Rand |
| `line.secondary` | #7A5A3A | Sekundärknopf |
| `glut` | #FF8A2A | Auswahl, aktiver Tab, Rand der Aufwerten-Leiste, Artefakt |
| `glut.grad` | #FFC06A → #FF7A1F (55 %) → #D84E0E | Primärknopf |
| `glut.deep` | #E0601A | Zähler-Badge, Balken-Start |
| `glut.light` | #FFB15A | Sterne, Labels Artefakt, Balken-Ende |
| `glut.text` | #FFD9A8 | hervorgehobener Text, aktiver Tab, Kennzahlen |
| `glut.plus` | #FFB35A (Rand) / #FFD27A (Glyph), Füllung #5A2A14 → #1C0F0A | Plus-Knopf |
| `text.main` | #F3E7CF | Fließtext, Zahlen |
| `text.muted` | #B9A988 | Labels, inaktive Tabs, Untertitel |
| `text.chip` | #D6C7A6 | Chips, Material-Zeile |
| `text.bone` | #EADFC6 | Glyph-Icons, Quadrat-Knöpfe |
| `ink` | #0B0908 | Badges, Balken-Hintergrund |
| `ink.brown` | #2A1206 | Knopf-Outline, Chip-Outline auf Glut |
| `ink.btnshadow` | #6A2208 | Textschatten im Primärknopf |
| `accent.moon` | #3FE0D0 | Info-Akzent (Deckel-Hinweis, Bonus-Info), Rolle Fern |
| `accent.frag` | #B57BFF → #E7D4FF | Fragment-/Sternbalken |
| `state.plus` | #9BE37A | Zuwachs (+96, +7,8 %) |
| `state.missing` | #FF6A5A | fehlende Kosten (Zahl rot) |
| `title.grad` | #FFF1D6 → #FFB15A (55 %) → #FF6A1A | Screen-Titel, Heldenname |

**Seltenheitsfarben**
| Gruppe | Stufe | Hex | Quelle |
|---|---|---|---|
| Ausrüstung | Grob (`gr_common`, color_key grey) | #A9A296 | gdd/gear_rarities.csv |
| Ausrüstung | Geschliffen (`gr_fine`, green) | #5FD16A | gdd/gear_rarities.csv |
| Ausrüstung | Meisterstück (`gr_master`, blue) | #4AA8FF | gdd/gear_rarities.csv |
| Artefakt | alle | #FF8A2A | artifacts.csv |
| Held | R / SR / SSR / UR | #A9A296 / #4AA8FF / Glut-Verlauf (#FFC06A → #FF7A1F) / #FF4A6A | R/SR/SSR laut Kanon; der UR-Farbwert ist ein Vorschlag |
| Truppen (keine Seltenheit, nur Rolle) | Nahkampf / Fern + Belagerung / Reiter / Unterstützer | #D9CCB0 / #3FE0D0 / #B57BFF / #FF8A2A | linker Akzent der Listenkarte |

**Dock-Tönung D2 (Stand 22.10.2026, Entscheidung Fabian: kein Blau, gilt auch fürs Dorf-Dock):** Sprite `d2_dock_bg.png` 1080×212, 9-Slice 4/8/4/8. Verlauf rgba(24,16,12,.80) → rgba(24,16,12,.96) bei 45 % → rgba(8,6,4,.98). Oberkante 1,5 px Weiß mit Alpha 22 % ist im Sprite enthalten. `dock.bottom` (#080604) füllt nur die Safe Area unter dem Dock. Dock-Labels inaktiv #BFAE8E, aktiv #FFF3D6. Aktive Platte rgb(255,150,60) mit Alpha 55 % → 22 %, Rand Alpha 85 %, Innenlicht oben 2 px Weiß mit Alpha 35 %.

## 4. Verläufe, Schatten, Glow
- **Screen-Hintergrund:**
  - Höhlentextur `cover`.
  - Glut-Schein unten: radial, Ellipse bei 50 %/105 %, rgba(255,110,30,.45) → 0 bei 55 %.
  - Mondlicht oben: radial bei 50 %/−5 %, rgba(63,224,208,.18) → 0 bei 50 %.
  - Abdunkelung `bg.dim`.
  - Fertig gerendert als `d2_bg_screen_1080x1920.png`.
- **Panel:**
  - Verlauf `panel.top` → `panel.bottom`.
  - Innenlicht oben 3 px rgba(255,220,170,.28), Innenschatten unten 6 px rgba(0,0,0,.4).
  - Glow 24 px rgba(255,120,30,.18), Schlagschatten 0 12 30 rgba(0,0,0,.6).
- **Primärknopf:**
  - Innenlicht oben 5 px Weiß mit Alpha 45 %, unten −8 px Schwarz mit Alpha 20 %.
  - Glow 28 px rgba(255,120,30,.55), Stufe 0 6 0 #2A1206.
- **Slot:** Glow 16 px in Seltenheitsfarbe (55 %), Innenschatten 24 px Schwarz mit Alpha 85 %, innerer Rand 6 px Schwarz mit Alpha 55 %.
- **Figur:** Drop-Shadow 0 14 10 Schwarz mit Alpha 60 % plus `d2_schatten_boden`. **Kein farbiger Glow hinter Figuren.**
- **Text:**
  - Lilita-Zahlen: Schatten 0 3 0 #000.
  - Titel: zusätzlich Glow 0 0 18 rgba(255,120,30,.25–.45).
  - In Unity mit TMP-Material: Underlay Offset (0, −3), Dilate 0, Farbe #000, optional Glow-Preset.

## 5. Materialien und Texturen
| Datei | Pfad | Verwendung |
|---|---|---|
| Höhlen-Hintergrund | `team/art/ui-kit/menus_v3/_assets/bg_dark_hoehle.png` (941×1672) | Grund aller Menüs, als `d2_bg_screen_1080x1920.png` komplett gerendert |
| Panel, Slot, Tooltip, Knöpfe | `vorlage_D2_export/d2_*.png` | 9-Slice-Sprites (Abschnitt 9) |
| HUD-Icons (Ressourcen, Dock) | `team/art/ui-kit/hud/v5/export/hud_c_ico_*.png` | Kosten, Top-Leiste, Dock (Iconset je Epoche laut HUD-Handoff) | ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.
| Ausrüstungs-Icons E1 | `team/art/ui-kit/menus_v3/_assets/equip/eq_*.png` (256 px) | Slots, derzeit auch Platzhalter für Werte-Icons |
| Skill-Icons | `team/art/ui-kit/skill_icons/icon_skill_<held>_<pas/ult>.png` | Skills-Tab |
| Heldenerfahrung | `team/art/ui-kit/menus_v3/_assets/ico_heldenxp.png` (256 px) | Aufwerten-Kosten |
| Held Ganzkörper | Ruka: `team/art/ui-kit/menus_v3/_assets/ruka_fullbody_alpha_v4.png` (1696×2350, Ränder weich ausgeblendet) | Helden-Detail |
| Porträts | `team/art/ui/heroes/hero_<id>_portrait_alpha.png` | Fragmentbalken, Listen |
| Gebäude / Truppen | `team/art/ui/buildings/e1_bld_*_bp04_*.png`, `team/art/heroes/troops/_typA/e1_trp_*_typA_v002.png` | Bauen, Armee |

Materialanmutung: Obsidian (glatt, warmschwarz), Bronze-Ränder (#C98A4A), Glut. Ausrüstung selbst nur aus Stein, Knochen, Leder, Fell, Holz und Muscheln (E1-Kanon). Bronze ist reine UI-Rahmenfarbe und zeigt kein Metall-Item.

## 6. Typografie
Schriften: `team/art/ui/fonts/LilitaOne-Regular.ttf` (OFL) und `Baloo2-Variable.ttf` (OFL, Gewichte 700/800). Als TMP-SDF-Assets (Atlas 4096, inklusive ★ → ‹ ✕ − ä ö ü ß).
| Rolle | Schrift | Größe px | Gewicht / Sperrung | Farbe / Effekt |
|---|---|---|---|---|
| Screen-Titel (BAUEN, ARMEE) | Lilita | 76 | Sperrung 2 | `title.grad`, Schatten 0 4 0 #000 + Glow |
| Heldenname | Lilita | 84 | Sperrung 2 | `title.grad` |
| Untertitel unter dem Titel | Baloo | 28 | 700, Sperrung 2 | `text.muted` |
| Abschnitts-Label (MACHT, KOSTEN, HELDENSTUFE) | Baloo | 20–24 | 700, Sperrung 3–4, Großbuchstaben | `text.muted` |
| Karten-/Panel-Titel | Lilita | 34–46 | Sperrung 1 | `text.main` oder `glut.text`, Schatten 0 3 0 #000 |
| Kennzahl (Macht, Stufe) | Lilita | 44–58 | – | `glut.text` |
| Werte / Kosten | Lilita | 32–42 (Liste 32, Detail 42–48) | – | `text.main`, fehlend `state.missing` |
| Bonus | Lilita | 24 | – | `state.plus` |
| Fließtext / Tooltip | Baloo | 21–28, Zeilenhöhe 1,25 | 700 | `text.main` / `text.chip` |
| Tab | Lilita | 40 | – | inaktiv `text.muted`, aktiv `glut.text` + Glow |
| Primärknopf | Lilita | 38–46 (Listen-Aktion 30) | Sperrung 1, Großbuchstaben | #FFF, Schatten 0 3 0 #6A2208 |
| Sekundärknopf / Filter | Baloo | 27–30 | 800 | `text.main`, aktiv `glut.text` |
| Chip | Baloo | 26 (Seltenheit: Lilita 28) | 700 | `text.chip` |
| Slot-Stufe / Badges | Lilita | 24–26 | – | `text.main` |
| Dock-Label | Lilita | inaktiv 30, aktiv 36 | – | #BFAE8E / #FFF3D6 |
| **Minimum** | | **20** (Slotnamen 26) | | |

TMP Auto-Size: Kosten min 22 / max 42. Top-Leiste 28–40 (HUD-Regel). Zahlenformat aus `HudV5NumberFormat` (ab 10.000 die Kurzform K/M/B). ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.

## 7. Komponenten (Maße auf 1080×1920)
Zustände generell:
- **Normal**
- **Gedrückt:** um 4 px nach unten versetzt, Helligkeit 88 %, Stufenschatten 2 px statt 6 px
- **Gesperrt:** Graustufen 85 %, Helligkeit 60 % (Bilder und Icons: Graustufen 100 %, Helligkeit **55 %**), plus `d2_ico_schloss` (hell, nie Emoji) und Bedingungstext in #EADFC6 bzw. #A89674
- **Aktiv:** Rand und Text in Glut, unterlegter Glut-Schein mit Alpha 18 %

Animation: Druck 0,08 s, Tab-Wechsel 0,15 s.

| Komponente | Maße / Position | Radius | Sprite | Zustände und Regeln |
|---|---|---|---|---|
| **Top-Ressourcenleiste (Menüs)** | Höhe 132, zentriert: Pill 280×80 · Plus 80×80 · Pill 280×80 · Pill 280×80 bei y 26, x 54 / 346 / 446 / 746 (Abstand Pill→Plus 12, sonst 20). Icon 64 px **innen** (x+8, y+8). Wert Lilita 40 ab x+84 | 40 | `d2_pill_ressource` | Gilt nur für Vollbild-Menüs. Die **Dorf-Top-Leiste bleibt unverändert (Paket F6)**. Die ganze Pill ist antippbar (öffnet das Ressourcen-Sheet). Keys und Regeln wie im HUD-Handoff (`hud.currency_1..3`) | ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.
| **Pill-Plus** (Fabian 22:16) | sichtbar **80×80 = Pill-Höhe, nie höher**, rechts neben der Kristall-Pill (Abstand 12), Glyph „+“ Lilita 44 #FFD27A. Unsichtbare Hitbox 120×120 zentriert (326/6) | 40 | `d2_btn_plus_pill` | Nur an Kristallen. Dezent: gleicher Rand/Grund wie die Pill (#8A7656 auf rgba(20,15,12,.85)), kein Glut-Verlauf. Gedrückt: Helligkeit 88 % |
| **Kopfleiste (Screen)** | Zurück 120×120 bei 28/148. Titel zentriert y 140 (Lilita 76), Untertitel y 226. Rechts Schließen 120×120 bei rechts 28 / y 150 **oder** Kennzahl-Panel 270×124 | Quadrat 28 | `d2_btn_quadrat_*` + `d2_ico_zurueck` / `d2_ico_schliessen` | Nur Zurück **oder** Schließen, wenn der Screen aus dem Dock kommt (Kritiker-Hinweis Doppelnavigation). Vorschlag: Zurück nur bei Unterseiten |
| **Kopf Helden-Detail (D4)** | Name links ab x 174 / y 138, Chips darunter y 232 (Höhe 50, Abstand 10), Macht-Panel 270×124 rechts oben | – | `d2_chip`, `d2_chip_seltenheit_*`, `d2_panel_frame` | siehe Abschnitt 8 |
| **Tabs** | Leiste über die volle Breite (28 … 1052), Höhe **124** (überall: Vorlage, CSV, Sprite, Mocks), gleich breit | 0 | `d2_tab_aktiv` / `d2_tab_inaktiv` | Aktiv: Unterstrich 5 px Glut + Verlauf Glut 0 → 18 %. Inaktiv: Unterstrich 3 px `line.dark`. Badge `d2_badge_zaehler` 48×38 rechts oben (16/14) |
| **Filter- und Sortierleiste** | Höhe 120, Abstand 10–14: Suchknopf 120×120, Filter-Chips (flexibel, mindestens 150 breit), Sortierung 150–300 rechts mit `d2_ico_sortieren` | 28 | `d2_btn_sekundaer_*`, aktiv `d2_btn_filter_aktiv` | Aktiv: Rand Glut, Text `glut.text`. Kategorie mit Anzahl („Wirtschaft 7“, Zahl Baloo 24 #8A7656). Zu viele Chips: horizontal scrollen, letzter Chip angeschnitten + Fade 48 px |
| **Suchfeld** | aufgeklappt 120 hoch, flexibel breit (mindestens 500), Lupe 56 px links (Innenabstand 32), Platzhaltertext Baloo 30 `text.muted` | 28 | `d2_btn_sekundaer_normal` + `d2_ico_suche` | Fokus: Rand Glut. Löschen-X 120×120 rechts innen |
| **Listenkarte** | volle Breite 1024 × **150** (Bauen) bzw. **144** (Armee, Minimum für alle Listen), Abstand 8. Bilder liegen innen mit 12 px Abstand (Regel B). Armee: Bild 120×120 bei 12/11, Titel x 146 / y 22, Unterzeile y 76, Kosten rechts y 44. Bauen: Bild 126×124 bei 12/12, Titel Lilita 36 bei x 156 / y 12, Unterzeile Baloo 26 y 60, Kosten y 96 (Icon 40, Lilita 30, Abstand 24). Aktion **immer 120×120** rechts (12–16 vom Rand, vertikal zentriert) | 0 (eckig, bewusst „Gear-Panel“) | `d2_listenkarte_*` + `d2_aktion_kachel` | Hintergrund rgba(20,15,12,.82). Linker Akzent 6 px nach Rolle (nur Armee). Gesperrt: Bild in Graustufen, Unterzeile Schloss-Sprite + Bedingung, Aktion mit Schloss, Rand `line.dark`. Zu wenig Rohstoffe: fehlende Zahl #FF6A5A, Aktion „FEHLT STEIN“ |
| **Detail-Sheet / Detail-Panel** | volle Breite, 480–520 hoch. Bildfeld 400–420 × 436–476 links (Innenabstand 20). Rechts Titel Lilita 44–46, Chips, Kernwert, Kosten, Knopf 120 hoch | 26 | `d2_panel_frame` (9-Slice 44) | Bildfeld-Hintergrund für Gebäude erlaubt: radial Glut 35 % (kein Halo, da Gebäudebild ohne Figur). Für Truppen besser `d2_schatten_boden`. Sheet unten (falls gebraucht): Griff 110×10 oben mittig, Ende über dem Dock (y ≤ 1676) |
| **Kostenzeile** | Icon + Zahl, Abstand Icon–Zahl 6, zwischen Posten 24–30. Größen: Liste Icon 44 / Lilita 32, Detail 58–66 / 42–48 | – | Icons `hud_c_ico_*`, `ico_heldenxp` | Fehlend: Zahl #FF6A5A. Mehr als 3 Posten: zweite Zeile (UISliceTable, wie Paket F6). **Nie eine Zeit** | ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.
| **Primärknopf** | Höhe **120** (einheitlich, auch `btn_upgrade`), Breite flexibel (mindestens 240), Text in Großbuchstaben | 28 | `d2_btn_primaer_normal / _gedrueckt / _gesperrt` | Gesperrt bei fehlenden Kosten oder Cap, Text bleibt lesbar. Pro Screen genau **ein** Primärknopf |
| **Sekundärknopf** | Höhe 120, Breite flexibel | 28 | `d2_btn_sekundaer_*` | Filter, Sortierung, „Nur baubare“ (Checkbox 56 `d2_haekchen_box_an/aus` links, Abstand 16) |
| **Quadrat-Knopf** | 120×120 | 28 | `d2_btn_quadrat_*` | Zurück, Schließen, Mengenwähler |
| **Mengenwähler** | − 120×120 · Zahl Lilita 52, 70 breit · + 120×120, Abstand 10, rechts daneben Primärknopf (mindestens 200 breit) | 28 | `d2_btn_quadrat_*` + `d2_ico_minus/plus` | Gedrückt halten = Schnellzählen. Max. durch freie Plätze, Rohstoffe und Kasernen-Cap. Zeile darüber: Gesamtkosten + „+10 Plätze“ |
| **Seltenheitsrahmen** | Slot 140×140 (Rand 3 px), Tooltip-Rand 3 px, Chip | Slot 24 | `d2_slot_grob/geschliffen/meister/artefakt`, `d2_tooltip_*`, `d2_chip_seltenheit_*` | Farben Abschnitt 3. Truppen nie mit Seltenheit |
| **Sperrzustand** | Element in Graustufen + Schloss 40–56 px + Bedingung in Kurzform (Baloo 24–26), z. B. „ab 4★“, „Kampagne 5“, „Kriegerlager St. 4“ | – | `d2_slot_gesperrt`, `d2_ico_schloss` | Das Schloss verdeckt nie Werte oder Knöpfe anderer Elemente. Gesperrter Slot ohne Stufen-Badge, stattdessen der Sperr-Chip 128×44 innen im Slot (x+6 / y+90, definiertes Badge) |
| **Tooltip (Diablo)** | Breite 420–640, Höhe nach Inhalt (mindestens 190). Titel Lilita 27, Unterzeile Baloo 21 in Seltenheitsfarbe, Trenner 1,5 px (`d2_trenner_tooltip`, getönt), Hauptwert Lilita 34 #9BE37A, Material Baloo 21, Hinweis Max.-Stufe Baloo 20 #3FE0D0 („Max. St. 9 (Häuptlingsfeuer St. 10)“, nie Regeltext wie „Feuer − 1“). Innenabstand 18 | 20 | `d2_tooltip_<seltenheit>` | Erscheint im Inhaltsbereich und verdeckt nie die Figur (K9). Auswahl über Tippen auf den Slot, der gewählte Slot bekommt `d2_slot_auswahl_ring` |
| **Ausrüstungsslot** | 140×140, Icon 108 (16/12; ausgewählt mit Rand 5: 14/10), Stufen-Badge „St. 7“ (Höhe 40, mindestens 48 breit, Lilita 26) **innen** rechts unten 4/4 (definiertes Badge), Slotname **Baloo 800 26** (Zeilenhöhe 24, #E6D8B8, Schatten 0 2 0 #000 + Kontur 3 px #000) darunter bei y+146, Raster 176 (≥ 12 px Luft zu ARTEFAKT-Label und Tabs, K8) | 24 | `d2_slot_*`, `d2_badge_stufe` (Rand getönt) | Leer: Slot-Sprite + Silhouette mit Alpha 25 % + „+“. Stufe ≤ Häuptlingsfeuer − 1 (`gear_level_cap_rule`) |
| **Fragmentbalken** | Träger 688×68 bei 196/1112 (zwischen den Slot-Spalten), Innenabstand 18 horizontal / 12 vertikal, Inhalt zentriert mit Abstand 12: Porträt 40 (Radius 12, Rand Bronze), Balken 210×20, Text „96/240 bis 4★“ Lilita 28 #E7D4FF, Sterne 26 (Zeilenhöhe 30). Porträt und Sterne liegen **innerhalb** des Trägers (Fix Fabian 22:15) | 34 / 10 | `d2_pill_fragment`, `d2_bar_bg`, `d2_bar_fill_fragment`, `d2_ico_stern` | Füllung = frag/frag_next. Bei 5★: „Max.“, Balken voll |
| **Werte-Balken** | Höhe 16–22 | 11 | `d2_bar_bg`, `d2_bar_fill_glut` | Armee-Detail |
| **Chip** | Höhe 50, Innenabstand 18 horizontal | 25 | `d2_chip` | Info, nicht antippbar |
| **Scrollbar** (K3) | Spur 8 × Listenhöhe bei x 1058 (14 px rechts neben der Liste), Daumen 8 breit, Länge = sichtbar/gesamt (min. 60) | 4 | `d2_scrollbar_spur`, `d2_scrollbar_daumen` | Spur rgba(234,223,198,.10), Daumen #A89674. Erscheint beim Scrollen, blendet 1,2 s danach auf Alpha 40 % ab. Nicht antippbar (Touch-Ziel ist die Liste) |
| **Sortier-Dropdown** (K3) | Auslöser = Sekundärknopf 120 hoch mit Text „Sortieren: Kosten“ + `d2_ico_sortieren` 40 px rechts. Liste klappt darunter auf: Panel 360 breit, Einträge 120 hoch (Baloo 800 30), Trenner 2 px #7A664E | Panel 26, Option 18 | `d2_dropdown_liste`, `d2_dropdown_option_aktiv`, `d2_dropdown_trenner`, `d2_ico_haekchen` | Gewählte Option: Glut-Fläche 18 % + Rand Glut + Häkchen rechts. Tippen außerhalb schließt. Optionen aus Config (`sort.options`) |
| **Sheet-Griff** (K3) | 110×10 oben mittig, 14 px unter der Sheet-Kante; Touch-Fläche 240×60 | 5 | `d2_sheet_griff` | #B9A988. Ziehen nach unten schließt das Sheet |
| **Häkchen / Checkbox** (K3) | Box 56×56 links in der Zeile, Text daneben (Abstand 16). Die ganze Zeile (mindestens 120 hoch) ist antippbar | 14 | `d2_haekchen_box_aus`, `d2_haekchen_box_an` | Aus: #0B0908, Rand #A89674. An: Glut-Verlauf, Häkchen #2A1206. Für „Nur baubare“ |
| **Fade-Kante** (K3) | rechts an horizontal scrollbaren Leisten 48 × Leistenhöhe; am Listenende über dem Dock 1080×96 | – | `d2_fade_rechts` (links gespiegelt), `d2_fade_unten` | Verlauf rgba(14,10,9,0) → .96. Nur sichtbar, wenn noch Inhalt folgt. Ersetzt nie das 220-px-Padding am Listenende |
| **Dock „Dunkles Glas“** | 1080×212, bottom-anchored, 5 Tabs à 216. Inaktiv: Icon 96×88 bei x+60 / y 14, Label y 106. Aktiv: Platte 192×196 bei x+12 / y −26, Icon 140×124 bei x+38 / y −22, Label 36 bei y 104, Strich 60×8 bei x+78 / y 152. Gestenleiste 300×10 bei 390/188 | Platte 30 | `d2_dock_bg`, `d2_dock_platte_aktiv`, `d2_dock_indikator`, Icons `hud_c_ico_*` | Kein Holzkasten, keine Kacheln. Optional UI-Blur 18 px. Reihenfolge `tabs.order` | ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.

## 8. Helden-Detail-Variante (Stil D2, Layout D4) – Vorlage für alle Helden
Mock: `v3_2_obsidian_helden_detail_v2.png`. Exakte Rechtecke: `vorlage_D2_layout_helden.csv`.
- **Kopf:**
  - Zurück 120 bei 28/148.
  - Name (Lilita 84, Verlauf) ab x 174.
  - Chips: Seltenheit (Glut-Chip für SSR) · Klasse · „St. 15/20“ · Epoche.
  - Rechts das Macht-Panel 270×136 bei y 146 (Innenabstand 24/14).
- **Figur:** frei stehend, 680×820 bei 200/300, mit Bodenschatten.
  - Optional dahinter der Name riesig (Lilita 290) als Kontur mit Alpha 7–14 %. Das ist Typografie, kein Leuchten.
  - **Kein Halo.**
  - Ganzkörper-Art mit weich ausgeblendeten Bildrändern (Alpha-Fade 90 px seitlich, 70 px unten), damit keine harten Schnittkanten entstehen.
- **Slots (D4-Anordnung):**
  - **Entschieden (Fabian 22:15):** 10 Slots = Helm, Schultern, Waffe, Rüstung, Beine, Schuhe, 2 Ringe, 2 heldengebundene Artefakte. Die Slotliste kommt aus der Config (`gear_slots`), nicht hart verdrahtet.
  - Slots 140×140. Links x 32: Helm, Schultern, Rüstung, Beine. Rechts x 908: Waffe, Ring, Ring, Schuhe.
  - y = 296 + 176 × Reihe. In Reihe 5 je ein Artefakt (y 1042, Label „ARTEFAKT“ Baloo 800 26, Zeilenhöhe 24, bei y 1006). Abstände (K8): Beine-Label (Ende 994) → ARTEFAKT 12 px, ARTEFAKT-Label (Ende 1030) → Artefakt-Slot 12 px, Artefakt-Slot (Ende 1182) → Tabs 12 px.
  - Rechtes Artefakt gesperrt „ab 4★“.
  - Slotname unter jedem Slot (mindestens 26 px, mit Kontur), Stufe mit „St.“.
- **Fragmentbalken** 688×68 bei 196/1112, alles innen (Regel B).
- **Tabs** bei y 1194, Höhe 124: Werte · Skills · Lore · Inventar (Badge).
- **Tab Werte:**
  - Links der Werte-Block 584×218 bei y 1330: Kopfzeile „WERTE“ (y 1348) und über jeder Bonus-Spalte das Label „auf St. 16“ (`hero.detail.stats_next_fmt`, #9BE37A). Darunter 2 × 3 Werte ab y 1380, Raster 52 (Icon 48, Label Baloo 20, Wert Lilita 30, Bonus rechtsbündig in fester Spalte = +8 % laut GDD). Innenabstand ≥ 12.
  - Rechts der Tooltip des gewählten Slots 422×218.
- **Tab Skills:** gleiche Fläche 1330–1548. Icon-Reihe (4 × 150×130, Abstand 16) und darunter bzw. daneben ein Detail-Panel im Tooltip-Stil. Gesperrter Skill mit Schloss + „ab 4★“.
- **Tab Lore:** Panel mit Herkunft (Epoche), Zitat und Freischalt-Hinweisen, kein Fließtextblock über 4 Zeilen.
- **Aufwerten-Leiste** 1024×130 bei y 1560 (Rand Glut, 18 px über dem Dock):
  - Label „HELDENSTUFE“, „St. 15 → 16“ (Lilita 44).
  - Kosten 770 Muschel-Gold + 391 Heldenerfahrung (hero_levels.csv).
  - Primärknopf 300×120 rechts.
  - Bei St. = E1-Cap (20) zeigt der Knopf „Max. St. 20“ (gesperrt).
- **Dock** mit aktivem Tab Helden.

## 9. Export: 9-Slice-Sprites und Icons
**Regel Rect und 9-Slice (Kritiker K2, verbindlich):**
1. Jedes Sprite enthält das Element **plus Glow- bzw. Schattenrand `pad_ltrb`** (Manifest; bei Knöpfen unten +8 für den Stufenschatten).
2. Die Layout-CSV nennt immer das **Element-Rect** (= Hitbox und Inhalt, z. B. Aufwerten-Knopf 300×120).
3. Das Image-RectTransform ist das Element-Rect, **erweitert um `pad_ltrb`**: x − l, y − t, w + l + r, h + t + b. Fertig berechnet in der CSV-Spalte `bild_rect_xywh`. Umsetzung in Unity: Kind-Objekt „Bild“ mit Anchors stretch und Offsets −l/−b/+r/+t unter dem Element-Objekt.
4. `slice_ltrb` gilt für das Sprite **inklusive** pad. Pixels per Unit Multiplier 1, Canvas 1080×1920. So werden Ecken und Rauten nie gestaucht.
5. Höhen sind einheitlich: Primär- und Sekundärknopf 120, Quadrat-Knopf 120×120, Tabs 124, Listenkarte min. 144, Slot 140.

Alle Dateien in `vorlage_D2_export/`, lokal aus den CSS-Quellen gerendert (`python3 _src/export_9slice_d2.py`, Chrome headless, transparent). Ränder (L, T, R, B) stehen in `manifest_9slice.json` und enthalten den Glow-Rand (pad). Feld `hinweis_slice`: „nur horizontal dehnen“ = Höhe fix (Pills, Chips, Balken, Badges), sonst echtes 9-Slice. Das Skript prüft, dass die Ränder kleiner als das Sprite sind. In Unity: Sprite Mode Single, Mesh Full Rect, Border laut Manifest, Image Type Sliced, Pixels per Unit Multiplier 1. Atlas „D2_Frames“ (2048, kein Rotate, Padding 4, kein Tight Packing), Icons im Atlas „D2_Icons“.

| Datei(en) | Element / Pad | Slice L/T/R/B (inkl. Pad) | Zweck |
|---|---|---|---|
| `d2_panel_frame.png`, `_glut`, `_muted` | 240×240 / 28 | 72/72/72/72 | Panel, Detail, Aufwerten-Leiste, Werte-Block |
| `d2_tooltip_grob/geschliffen/meister/artefakt.png` | 240×200 / 28 | 64/64/64/64 | Diablo-Tooltip |
| `d2_slot_grob/geschliffen/meister/artefakt/gesperrt.png` | 140×140 / 26 | 66/66/66/66 | Ausrüstungsslot |
| `d2_slot_auswahl_ring.png` | 140×140 / 26 | 66/66/66/66 | Auswahl-Overlay |
| `d2_btn_primaer_normal/_gedrueckt/_gesperrt.png` | 300×120 / 34 (+8 unten) | 78/78/78/92 | Primärknopf |
| `d2_btn_sekundaer_*.png` | 300×120 / 20 (+8 unten) | 60/60/60/72 | Sekundärknopf, Suchfeld |
| `d2_btn_quadrat_*.png` | 120×120 / 20 | 60/60/60/72 | Zurück, Schließen, −/+ |
| `d2_btn_filter_aktiv.png` | 300×120 / 20 | 60/60/60/72 | aktiver Filter |
| `d2_pill_ressource.png` | 280×80 / 12 | 64/12/64/12 (nur horizontal) | Top-Leiste (Menüs) |
| `d2_btn_plus_pill.png` | 80×80 / 12 | – (fest) | Pill-Plus, sichtbar 80, Hitbox 120 im Code |
| `d2_tab_aktiv.png`, `d2_tab_inaktiv.png` | 240×124 | 8/8/8/12 bzw. 8/8/8/10 | Tabs |
| `d2_chip.png`, `d2_chip_seltenheit_r/sr/ssr/ur.png` | 160×50 bzw. 120×50 / 4 | 33/4/33/4 (nur horizontal) | Chips |
| `d2_badge_stufe.png`, `d2_badge_zaehler.png` | 60×40 / 4, 48×38 / 2 | 20/4/20/4, 20/2/20/2 (nur horizontal) | Badges |
| `d2_bar_bg.png`, `d2_bar_fill_glut.png`, `d2_bar_fill_fragment.png`, `d2_pill_fragment.png` | siehe Manifest | nur horizontal, siehe Manifest | Balken |
| `d2_listenkarte_neutral/nah/fern/reiter/unterstuetzer.png` | 400×150 | 12/8/8/8 | Listenkarte |
| `d2_aktion_kachel.png` | 120×120 | 8/8/8/8 | Listen-Aktion |
| `d2_dock_bg.png`, `d2_dock_platte_aktiv.png`, `d2_dock_indikator.png` | 1080×212, 192×196, 60×8 | 4/8/4/8, 36/36/36/36, – | Dock |
| `d2_trenner_tooltip.png`, `d2_schatten_boden.png` | 300×2, 580×100 | – | Tooltip-Linie, Bodenschatten |
| `d2_ico_zurueck/schliessen/plus/minus/stern/sortieren/suche/schloss.png` | 96×96 | – | Glyph-Icons (ersetzen Unicode und Emoji aus dem Mock) |
| `d2_bg_screen_1080x1920.png` | 1080×1920 | – | Screen-Hintergrund |
| `d2_scrollbar_spur.png`, `d2_scrollbar_daumen.png` | 8×120 | 0/4/0/4 | Scrollbar |
| `d2_dropdown_liste.png`, `d2_dropdown_option_aktiv.png`, `d2_dropdown_trenner.png` | 360×400 / 28, 320×120, 300×2 | 72/72/72/72, 20/20/20/20, – | Sortier-Dropdown |
| `d2_sheet_griff.png` | 110×10 | – | Sheet-Griff |
| `d2_haekchen_box_aus.png`, `d2_haekchen_box_an.png`, `d2_ico_haekchen.png` | 56×56 / 4, 96×96 | – | Checkbox und Häkchen |
| `d2_fade_rechts.png`, `d2_fade_unten.png` | 48×120, 64×96 | gestreckt | Fade-Kanten |

Maßgeblich sind die Werte im Manifest. Die Tabelle ist gerundet.

**Vorhanden, wird weiterverwendet:** `hud_c_ico_*` (Ressourcen, Dock), `eq_*` (8 Slots + 2 Artefakte + Werte/Lore), `icon_skill_*_pas/ult`, `ico_heldenxp.png`, Porträts, Gebäude bp04, Truppen Typ A, `ruka_fullbody_alpha_v4.png`. ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.

**Fehlt noch (Art-Aufgaben):**
1. Werte-Icons `ico_stat_hp/atk/def/speed/crit/lead`. Der Mock nutzt Ausrüstungs-Icons als Platzhalter.
2. Skill-Icons für den Angriffs-Skill je Held und für den gesperrten 4. Skill. Ruka nutzt `eq_waffe` und `eq_artefakt2` als Platzhalter.
3. Ganzkörper-Art (Alpha, Typ A) für alle Helden außer Ruka.
4. Talisman-Icon (GDD-Slot `slot_charm`), falls die Slotliste an das GDD angepasst wird (Abschnitt 12).
5. Leere-Slot-Silhouetten je Slot (Alpha 25 %).
6. Kategorie-Icons für Bauen-Filter (optional, Text reicht).
7. Lore-Panel-Illustration (optional).

## 10. Config- und ui_strings-Keys
Mock-Werte: `config/menus_v3_mock_strings.json` (Abschnitte `hero`, `hero_detail_v2`, `buildings`, `troops`, `army`). Vorschlag für `ui_strings.csv`; Platzhalter `{0}` bleiben im String:
- **Allgemein:** `menu.common.back`, `menu.common.close`, `menu.common.search_placeholder` („Suchen …“), `menu.common.sort_by` („Sortieren: {0}“), `menu.common.sort.cost/power/level`, `menu.common.filter_buildable` („Nur baubare“), `menu.common.locked_fmt` („🔒 {0}“ → Schloss-Sprite + Text), `menu.common.max` („Max.“), `menu.common.new` („Neu“).
- **Helden:**
  - Kopf und Tabs: `hero.detail.power` („Macht“), `hero.detail.level_fmt` („St. {0}/{1}“), `hero.detail.tab.stats/skills/lore/inventory`.
  - Aufwerten: `hero.detail.upgrade` („Aufwerten“), `hero.detail.upgrade_level_label` („Heldenstufe“), `hero.detail.upgrade_level_fmt` („St. {0} → {1}“), `hero.detail.stats_next_fmt` („auf St. {0}“), `hero.detail.stats_header` („Werte“), `hero.detail.max_fmt` („Max. St. {0}“).
  - Fragmente und Seltenheit: `hero.detail.fragments_fmt` („{0}/{1} bis {2}★“), `hero.rarity.r/sr/ssr/ur`.
  - Stammdaten: `hero.class.<id>`, `hero.<id>.name/title/lore`, `epoch.<id>.name`.
- **Ausrüstung:**
  - Slots: `gear.slot.helm/shoulders/armor/legs/weapon/ring/boots/artifact` (bzw. GDD-Slots `slot_weapon/armor/charm/artifact`), `gear.slot_level_fmt` („St. {0}“).
  - Seltenheit, Sperre: `gear.rarity.gr_common/gr_fine/gr_master`, `gear.lock.stars_fmt` („ab {0}★“).
  - Tooltip: `gear.tooltip.sub_fmt` („{0} · {1} · St. {2}“), `gear.tooltip.material`, `gear.tooltip.cap_fmt` („Max. St. {0} (Häuptlingsfeuer St. {1})“, {1} = {0} + 1).
  - Werte: `stat.hp/atk/def/speed/crit/lead`.
- **Bauen:**
  - Titel, Zähler, Kategorien: `build.title`, `build.counter_label` („Gebaut“), `build.counter_fmt` („{0}/{1}“), `build.instant` („Aufbau sofort“), `build.cat.all/economy/housing/military/defense/knowledge`.
  - Knöpfe: `build.btn.build` („Bauen“), `build.btn.upgrade_fmt` („Auf St. {0}“), `build.btn.missing_fmt` („Zu wenig {0}“).
  - Max., Sperre, Ertrag: `build.max_fmt` („Max. · {0}“), `build.lock.campaign_fmt` („Kampagne {0}“), `build.lock.fire_fmt` („Häuptlingsfeuer St. {0}“), `build.yield_fmt` („+{0}/h“).
- **Armee:**
  - Titel, Plätze, Tabs: `army.title`, `army.cap_label` („Truppenplätze“), `army.cap_fmt` („{0}/{1}“), `army.tab.troops/formation/counter`.
  - Ausbilden: `army.train` („Ausbilden“), `army.pop_per_unit_fmt` („{0} Plätze je Einheit“), `army.cap_add_fmt` („+{0} Plätze“).
  - Bestand, Rollen: `army.stock_fmt` („Bestand {0}“), `army.role.melee/ranged/cavalry/siege/support`, `army.lock.building_fmt` („{0} St. {1}“).
- **Config:**
  - Theme und UI: `ui.theme` = `d2_obsidian`, `ui.list_bottom_padding` = 220, `ui.touch_min` = 120, `ui.dock.overhang` = 26.
  - Seltenheitsfarben: `ui.rarity_color.<gear_rarity_id>` (Hex wie Abschnitt 3, Basis `gear_rarities.color_key`), `ui.hero_rarity_color.<r>`, `ui.role_color.<role>`.
  - Daten: `hero_levels.csv` (Kosten), `heroes.csv` (Seltenheit), `units.csv` (`pop_cost`, Kosten), `building_levels.csv` / `buildings.csv` (Kosten, Freischaltung), `gear_rarities.csv`, `game_config.csv` (`gear_level_cap_rule`, `norm_gear_level`), `artifacts.csv`.
  - Truppenzähler = Summe(Bestand × `pop_cost`) wird berechnet, nie als Text gepflegt.

**Mock-Texte der D2-Screens:** Bauen und Armee holen ihre Texte jetzt aus `UI` in `_src/common.py`, exportiert als `ui_d2` in `config/menus_v3_mock_strings.json` (K7). Die Keys von oben gelten für Unity.

## 11. Kanonregeln (Pflicht bei jedem Screen)
1. **Keine Bau- und Ausbildungszeiten:** kein Timer, kein Zeit-Chip, kein „Bauarbeiter frei“. Aufbau und Ausbildung sind sofort (GDD). Gezeigt werden Kosten, Stufe (St. x → x+1) und die Freischaltbedingung.
2. **Ruka ist SSR.** Seltenheitsleiter R/SR/SSR/UR (heroes.csv). Truppen haben **keine** Seltenheit, nur eine Rolle.
3. **Helden-Aufwertung** kostet nur Muschel-Gold + Heldenerfahrung (hero_levels.csv), nie Holz oder Nahrung. Die Obergrenze in E1 ist Stufe 20. Jede Stufe gibt +8 % Werte.
4. **Sterne über Fragmente:** 40/40/40/240/240 (gesamt 600). Anzeige „x/y bis n★“.
5. **Ausrüstung:**
   - Stufe ≤ Häuptlingsfeuer − 1, die E1-Norm ist St. 9. Stufen 10–20 erst ab E2.
   - Seltenheiten Grob/Geschliffen/Meisterstück.
   - Material nur Stein, Knochen, Leder, Fell, Holz, Muscheln.
6. **E1-Kanon:** kein Metall, kein Webstoff, Gold nur als Muscheln/Handelsgut, keine bunten Federn, kein Tipi/Iglu/Totem, kein Getreide, Bernstein erst ab E4.
7. **Truppenzähler** = Summe der Bestände × Plätze. Kosten vollständig laut units.csv.
8. **Keine Halos** hinter Figuren oder Gebäuden, keine harten Bildkanten (Alpha auf hellem und dunklem Grund prüfen).

## 12. Offene Punkte / Entscheidungen
- ~~Slotliste vs. GDD~~ **geschlossen (Fabian 17.10. 22:15):**
  - Die Slots sind entschieden: Helm, Schultern, Waffe, Rüstung, Beine, Schuhe, 2 Ringe und 2 heldengebundene Artefakte, wie im Mock.
  - Die Slotliste kommt weiterhin aus der Config (`gear_slots`), Dev verdrahtet keine Slots fest.
  - `gear_slots.csv` aktualisiert **Game Design**. Art hat die Datei nicht angefasst.
- ~~Top-Leiste~~ **geschlossen (Fabian 17.10. 22:15):**
  - Die **Dorf-Top-Leiste bleibt unverändert** (Paket F6: „Nichts an HUD-Top-Leiste ändern“), Stil C Holz. ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.
  - Der D2-Skin der Top-Leiste (dunkle Pills, Pill-Plus 80) gilt nur in den Vollbild-Menüs.
  - Zahlenformat und Keys bleiben wie im HUD-Handoff.
- **UR-Farbe** #FF4A6A ist ein Vorschlag.
- **Stilabstand:** D2 ist bewusst matter und dunkler als HUD C (Codex: Stil „mittel“). Fabian hat D2 trotzdem gewählt, deshalb nicht nachschärfen, ohne ihn zu fragen.

## 13. Modern-Gate-Checkliste für den Einbau (kurz)
- [ ] Screen sieht aus wie der Mock (Emulator 1080×1920, Screenshot im PR), Dock „Dunkles Glas“, nur Top-Leiste + Dock
- [ ] Listen haben Filter, Sortierung, Suche und eine eigene Detailansicht. Ein Primärknopf pro Screen
- [ ] Alle Touch-Ziele ≥ 120 px. Listenende mit 220 px Padding, nichts hinter dem Dock
- [ ] Alle Texte aus `ui_strings.csv`, alle Werte aus Config/gdd. Keine Texte in Sprites. Zahlen über `HudV5NumberFormat` ⛔ GESTRICHEN (Fabian 22.10.2026): Dorf-HUD wird neu in D2 erstellt, Icons neu in D2; `hud_c_ico_*` und `HudV5NumberFormat` nicht mehr verwenden.
- [ ] Kanonregeln Abschnitt 11 erfüllt (keine Zeiten, SSR, Kosten, Zähler, Material, Stufen-Deckel)
- [ ] Regel B: nichts ragt über Rahmen (außer definierten Badges), Innenabstand ≥ 12 (`check_boxes.py` = 0 Befunde)
- [ ] Kein Halo, keine Kantenfehler, keine grauen oder weißen Platzhalter. Gesperrtes mit Schloss + kurzer Bedingung
- [ ] 9-Slice-Ränder laut Manifest (keine verzerrten Ecken oder Rauten). Kostenzeile bleibt im Knopf (EditMode-Test mit 1/3/5 Posten)
- [ ] Abnahme-Reihenfolge: Art Director → Kritiker („geprüft ja/nein“) → Dev-Einbau
