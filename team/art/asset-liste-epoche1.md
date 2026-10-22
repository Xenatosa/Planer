> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# Asset-Liste Prototyp & Vertical Slice – Epoche 1 (Steinzeit)

**Projekt:** EPOCHA (Arbeitstitel) · **Für:** Fabian Schwegler · **Stand:** 13.10.2026 · v0.1
**Grundlage:** `../../Planungsdokument_Handygame.md` v1.1 · Formate und Benennung siehe `styleguide.md`

> **Lesart:** Die Spalte „Bezug“ zeigt, woher ein Eintrag kommt (Kapitel im Planungsdokument) oder ob er eine **[Annahme]** des Art-Teams ist. Der Plan nennt für Epoche 1 nur Thema („Höhlen, Feuer, Mammuts“), Mechanik (Winter/Nahrung), die 6 Truppenvarianten und allgemeine Gebäudefunktionen. **Gebäude-Namen, Gegner und Heldenbesetzung sind daher Annahmen** und müssen mit dem Game Design abgeglichen werden. **Aufwand** wird in **Personentagen (PT)** einer erfahrenen Fachkraft angegeben, inkl. einer Korrekturrunde und ohne Art-Direction-/Review-Zeit **[Schätzung]**.

## Prioritäten

| Priorität | Bedeutung | Zeitraum laut Roadmap |
|---|---|---|
| **P0** | Notwendig für Art-Style-Tests (3 Helden, 1 Gebäude, 1 Chibi-Truppe) und den spielbaren Prototyp: Bauen, Einsammeln, Ausbilden, Auto-Kampf, Formation. Darf zuerst in Style-Test-Qualität entstehen. | Q4 2026 – Q1 2027 |
| **P1** | Notwendig für den **Vertical Slice** „Epoche 1 komplett in finaler Qualität“ (Kampagne ~20 Missionen, Stadt, Truppen, 6–8 Helden, Onboarding, erste Monetarisierungs-Hooks) | Q2 2027 |
| **P2** | Wertsteigernd, aber nicht blockierend. Kann nach dem Vertical Slice oder bis Alpha/Soft Launch nachgezogen werden. | ab Q3 2027 |

## Aufwand-Übersicht [Schätzung]

| Kategorie | P0 (PT) | P1 (PT) | P2 (PT) | Summe (PT) |
|---|---|---|---|---|
| A. Helden | 51 | 48 | 32 | 131 |
| B. Chibi-Truppen Epoche 1 | 32,5 | 2 | 1,5 | 36 |
| C. Gegner & Boss Epoche 1 | 2 | 23 | 7 | 32 |
| D. Stadt-Gebäude Epoche 1 | 19,5 | 47,5 | 15 | 82 |
| E. Umgebung, Terrain, Karten | 12,5 | 23 | 4 | 39,5 |
| F. UI & Icons | 32,5 | 21,5 | 7 | 61 |
| G. VFX & Comic-Effekte | 6 | 7,5 | 0 | 13,5 |
| H. Story, Cutscene & Marketing | 0 | 23,5 | 11 | 34,5 |
| **Gesamt** | **156** | **196** | **77,5** | **429,5** |

Kumuliert: **bis Prototyp (P0) ≈ 156 PT**, **bis Vertical Slice (P0+P1) ≈ 352 PT**. Grob gerechnet sind das für P0+P1 bei 2 parallel arbeitenden Grafikern plus 1 Animator etwa 5,9 Monate reine Produktionszeit **[Schätzung]**. Dazu kommen Art Direction, Feedback und Integration (+15–25 %).
Für Kosten in Euro gelten die Spannen aus Plan Kap. 9.5 (z. B. Splash-Art 300–1.500 €, Chibi-Truppe inkl. Animation 150–600 €, Gebäude je Stufe 80–400 €, UI-Kit 3.000–15.000 €). Sie müssen mit Freelancer-Angeboten aus den Testaufträgen validiert werden.

---

## A. Helden (Vertical Slice: 6–8 Helden)

Laut Roadmap gibt es in Q4 2026 3 Helden-Testillustrationen und im Vertical Slice (Q2 2027) 6–8 Helden. Die Formation hat 3×2 Plätze (Kap. 7.4), für einen vollen Slot-Test sind also mindestens 6 Helden nötig. Nach dem Tutorial ist ein legendärer Held garantiert (Kap. 11.1). **Verbindlich ist `gdd/heroes.csv` (GDD v0.7):** 8 Epoche-1-Helden. Namen, Rarity, Klasse, geführter Truppentyp und `art_ref` (= Dateinamen-Präfix) stammen von dort.

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E1-HER-00 | Helden-Konzeptbogen (Moodboard, 3 Gesichtsschemata, Kostümregeln Steinzeit) | Held/Konzept | 2 Boards à 3000×2000 px | P0 | 3 | Plan Kap. 9.2, 18.2 (Moodboard) |
| E1-HER-01 | `hero_ruka` Ruka Wolfsherz – SSR · assassin · führt Kavallerie · art_ref `e1_her_ruka` – Komplettpaket · Style-Test 1 | Held | Paket | P0 | 16 | heroes.csv; Tutorial-Beschwörung (Kap. 11.1) |
| E1-HER-02 | `hero_mira` Mira Glutlied – SR · healer · führt Unterstützung · art_ref `e1_her_mira` – Komplettpaket · Style-Test 2 | Held | Paket | P0 | 16 | heroes.csv; Roadmap Q4 2026 |
| E1-HER-03 | `hero_tala` Tala Schleuderauge – SR · marksman · führt Fernkampf · art_ref `e1_her_tala` – Komplettpaket · Style-Test 3 | Held | Paket | P0 | 16 | heroes.csv; Roadmap Q4 2026 |
| E1-HER-04 | `hero_nara` Nara Mammutruferin – SSR · warrior · führt Infanterie · art_ref `e1_her_nara` – Komplettpaket | Held | Paket | P1 | 16 | heroes.csv; Featured-Banner |
| E1-HER-05 | `hero_kiko` Kiko Funkenflug – SR · tactician · führt Unterstützung · art_ref `e1_her_kiko` – Komplettpaket | Held | Paket | P1 | 16 | heroes.csv; Standard-Banner |
| E1-HER-06 | `hero_bako` Bako Hüttenbauer – R · builder · führt Belagerung · art_ref `e1_her_bako` – Komplettpaket (Startheld) | Held | Paket | P1 | 16 | heroes.csv; Startheld/Gouverneur |
| E1-HER-07 | `hero_gorm` Gorm Felsenfaust – R · warrior · führt Infanterie · art_ref `e1_her_gorm` – Komplettpaket | Held | Paket | P2 | 16 | heroes.csv; e1_camp_01 |
| E1-HER-08 | `hero_olm` Olm Speerwacht – R · warrior · führt Speerträger · art_ref `e1_her_olm` – Komplettpaket | Held | Paket | P2 | 16 | heroes.csv; Standard-Banner |

**Inhalt eines Helden-Komplettpakets** (gilt für E1-HER-01 bis -08; Formate siehe Styleguide Kap. 4.1):

| Teil-ID | Bestandteil | Größe / Frames | Aufwand (PT) |
|---|---|---|---|
| …-SPL | Splash-Art Ganzkörper inkl. Effekt-BG, Layer getrennt, Crop-Guides | 3000×4000 Master → 1536×2048 / 768×1024 | 5 |
| …-CRD | Heldenkarte (Crop) + Avatar (Crop) | 512×768 · 256×256 | 0,5 |
| …-VN | VN-Büste + 6 Emotionen + Mund offen/zu | 1500×2000 → 750×1000 | 2,5 |
| …-SD | Kampf-Figur SD (3–3,5 Köpfe), Teile-PSD | ca. 1024 px Figurhöhe | 2 |
| …-ANI | Spine-Rig + Animationen Idle, Laufen, Angriff, Fähigkeit/Ultimate, Treffer, Sieg, KO (Kap. 9.3) | 7 Anim., Atlas ≤ 2048² | 5 |
| …-ICO | Skill-Icons: Ultimate + 1–2 passive | 512 → 128/96 | 1 |
| | **Summe je Held** | | **16** |

Optional (P2, nicht in der Summe): Live-Splash (Spine-Idle der Splash-Art) +3–5 PT je Held. Ultimate-Cut-In-Crop siehe E0-VFX-07.

## B. Chibi-Truppen Epoche 1 (6 Typen, Plan Kap. 6.3)

Die Namen der Epoche-1-Varianten stammen aus dem Plan. Jeder Typ bekommt ein eigenes Spine-Rig, das in späteren Epochen per Skin wiederverwendet wird **[Annahme, Styleguide 5.3]**. Standard-Animationen: Idle, Laufen, Angriff, Treffer, KO, Sieg (6). Bei Sprite-Fallback wären es 6/8/8/3/6/6 Frames @12 fps.

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E1-TRP-00 | Truppen-Silhouetten-Sheet (alle 6 Typen, Schwarzflächen-Test) | Truppe/Konzept | 1 Sheet 4000×2000 | P0 | 1,5 | Kap. 9.2 Silhouetten-Regel |
| E1-TRP-01 | Keulenträger (Infanterie) · Style-Test „1 Chibi-Truppe“ | Truppe | Canvas 512², 6 Anim. | P0 | 5 | Roadmap Q4 2026 |
| E1-TRP-02 | Speerjäger (Speerträger) | Truppe | 512², 6 Anim. | P0 | 4,5 | Kap. 6.3 |
| E1-TRP-03 | Steinschleuder (Fernkampf) + Projektil-Sprite | Truppe | 512², 6 Anim. + 1 Sprite | P0 | 4,5 | Kap. 6.3 |
| E1-TRP-04 | Wolfsreiter (Kavallerie) | Truppe | 768×512, 6 Anim. (Lauf = Galopp) | P0 | 6 | Kap. 6.3 „Fantasy-Twist“ |
| E1-TRP-05 | Felsenwerfer (Belagerung) + Fels-Projektil | Truppe | 768×512, 6 Anim. + 1 Sprite | P0 | 6 | Kap. 6.3 |
| E1-TRP-06 | Schamane (Unterstützung) + Anim. „Heilen/Buff“ | Truppe | 512², 7 Anim. | P0 | 5 | Kap. 6.1 Heilung/Buffs |
| E1-TRP-07 | Animation „Spawn/Ausbildung“ für alle 6 Typen (Sofort-Ausbildung) | Truppe/Anim. | 6 × 0,4 s | P2 | 1,5 | Kap. 3.1 Ausbildung sofort |
| E1-TRP-08 | Truppen-Porträts für Ausbildungs- und Formations-UI (6) | Truppe/UI | 6 × 256² | P1 | 2 | Kap. 7.4 Truppenblock je Held |

## C. Gegner & Boss Epoche 1

Im Plan stehen 15–25 Gegner/Bosse bis zum Launch (Kap. 9.4) und ein Kampagnen-Boss als Bedingung für den Epochen-Aufstieg (Kap. 4.3). Wer die Gegner in Epoche 1 konkret sind, legt der Plan nicht fest. **Alle Einträge sind [Annahme]**, abgeleitet aus dem Thema „Höhlen, Feuer, Mammuts“.

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E1-ENM-01 | Feindlicher Stamm: 6 Truppentypen als Palettentausch + Gegner-Bodenring | Gegner | 6 Skins auf vorhandenen Rigs | P0 | 2 | Kostenhebel Paletten-Tausch Kap. 9.5 |
| E1-ENM-02 | Wildtier-Gegner 1 [Annahme: Säbelzahnkatze] | Gegner | 768×512, 6 Anim. | P1 | 5 | Annahme |
| E1-ENM-03 | Wildtier-Gegner 2 [Annahme: Höhlenbär] | Gegner | 768×512, 6 Anim. | P2 | 5 | Annahme |
| E1-ENM-04 | Mini-Boss [Annahme: rivalisierender Häuptling, Held-Look in SD] | Gegner/Boss | SD 3–3,5 Köpfe, 7 Anim. + VN-Porträt (3 Emotionen) | P1 | 8 | Annahme |
| E1-ENM-05 | Epochen-Boss [Annahme: Riesen-Mammut] inkl. Spezialangriff + Phasenwechsel-Look | Boss | 1024×1024, 8 Anim. | P1 | 10 | Kap. 4.3 Kampagnen-Boss |
| E1-ENM-06 | Boss-Intro-Splash (Comic-Panel) | Boss/Story | 1080×1920 | P2 | 2 | Annahme |

## D. Stadt-Gebäude Epoche 1 (isometrisch 2:1, 3 visuelle Stufen)

Die Gebäudefunktionen sind aus Kap. 4 abgeleitet (Ressourcenquellen, Lager, Zentrum, Wohnhäuser, Markt, Wissen). **Die Steinzeit-Namen und Footprints sind [Annahme].** Prototyp (P0) = Stufe 1. Stufen 2–3 = P1. Ausnahme: Für das Zentrum werden alle 3 Stufen in P0 gebaut, weil es als Style-Test „1 Gebäude“ (Roadmap Q4 2026) die Stufenlogik zeigen soll.

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E1-BLD-01 | Zentrum/Rathaus [Annahme: „Häuptlingsplatz mit Lagerfeuer“] Stufe 1–3 · Style-Test | Gebäude | 4×4 · 1024×1152 · 3 Stufen + Feuer-Loop 8 Fr. | P0 | 7 | Kap. 4.3 Zentrum-Level |
| E1-BLD-02 | Wohnhaus [Annahme: Fellhütte → Höhlenwohnung] Stufe 1 | Gebäude | 2×2 · 512×576 | P0 | 1,5 | Kap. 4.2 Wohnhäuser |
| E1-BLD-03 | Jagdhütte (Nahrung) Stufe 1 | Gebäude | 2×2 | P0 | 1,5 | Kap. 4.2 Jagd |
| E1-BLD-04 | Fischerhütte am Ufer (Nahrung) Stufe 1 | Gebäude | 2×2 | P1 | 1,5 | Kap. 4.2 Fischerei |
| E1-BLD-05 | Sammel-/Beerenfeld [Annahme: Steinzeit-„Farm“] Stufe 1 | Gebäude | 2×2, flach | P0 | 1,5 | Kap. 4.2 Farmen |
| E1-BLD-06 | Holzfäller Stufe 1 | Gebäude | 2×2 | P0 | 1,5 | Kap. 4.2 |
| E1-BLD-07 | Steinbruch Stufe 1 | Gebäude | 3×3 | P0 | 2 | Kap. 4.2 |
| E1-BLD-08 | Lager [Annahme: Vorratshöhle] Stufe 1 + Zustand „Lager voll“ | Gebäude | 3×3 | P0 | 2 | Kap. 4.3 Lagerkapazität |
| E1-BLD-09 | Wissensgebäude [Annahme: Ältestenhöhle mit Höhlenmalerei] Stufe 1 | Gebäude | 3×3 | P1 | 2 | Kap. 4.2 Wissen |
| E1-BLD-10 | Tauschplatz/Markt (Gold, Handel) Stufe 1 | Gebäude | 3×3 | P1 | 2 | Kap. 4.2 Gold/Handel, 4.4 Markt |
| E1-BLD-11 | Ausbildungsgebäude [Annahme: Kriegerlager] Stufe 1 | Gebäude | 3×3 | P0 | 2 | Kap. 3.1 Truppen ausbilden (Gebäude nicht benannt) |
| E1-BLD-12 | Helden-/Beschwörungsort [Annahme: Ahnenstein/Totemkreis] Stufe 1 | Gebäude | 3×3 + Glow | P1 | 2,5 | Kap. 7.6 Beschwörung |
| E1-BLD-13 | Verteidigung: Palisade (Autotile-Segmente) + Wachturm Stufe 1 | Gebäude | 1×1-Segmente ×16 + 2×2 Turm | P2 | 3 | Kap. 4.2 Stein → Verteidigung; Raids optional (Kap. 8.1) |
| E1-BLD-14 | Stufe 2 + 3 für BLD-02 bis BLD-12 (11 Gebäude × 2 Stufen) | Gebäude | 22 Varianten | P1 | 33 | Kap. 9.4: 3–5 visuelle Stufen |
| E1-BLD-15 | Idle-Animationen Stufe 3 (Rauch, Fahne, Arbeiter-Loop) für 11 Gebäude | Gebäude/Anim. | je 8–12 Fr. oder Spine | P2 | 8 | Styleguide 6.3 |
| E1-BLD-16 | Winter-Overlays (Schnee auf Dach/Boden) für alle Gebäude & Stufen | Gebäude/Overlay | ca. 37 Overlays | P1 | 6 | Kap. 5 Epoche 1: Winter |
| E1-BLD-17 | Gesperrt-/Bauvorschau-Darstellung (Shader-Lösung + Platzierungsraster grün/rot) | Gebäude/UI | Shader + 2 Tiles | P0 | 0,5 | Sofortbau Kap. 3.1 |
| E1-BLD-18 | Deko-Set Steinzeit (6 Objekte, z. B. Menhir, Knochenzaun, Feuerstelle) | Deko | 1×1–2×2 | P2 | 4 | Kap. 4.4 Dekorationen |
| E1-BLD-19 | Gouverneur-Badge-Anker (Position Avatar je Gebäude) | Gebäude/Daten | Pivot-Liste | P1 | 0,5 | Kap. 7.3 Gouverneur |

## E. Umgebung, Terrain, Karten

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E1-ENV-01 | Terrain-Tileset Sommer: Gras, Erde, Steppe, Ufer/Sand, Wasser + Übergänge (Autotile 16) | Terrain | Tile 256×128 HD, ca. 60 Tiles | P0 | 5 | Styleguide 6.1/6.4 |
| E1-ENV-02 | Wasser-Animation (Loop) | Terrain/Anim. | 8 Fr. | P1 | 1 | Fischerei am Ufer |
| E1-ENV-03 | Terrain-Tileset Winter (Variante von ENV-01) | Terrain | ca. 60 Tiles | P1 | 3 | Kap. 5 Winter |
| E1-ENV-04 | Props: Bäume (3), Büsche (3), Felsen (4), Knochen (2), fällbar/abbaubar-Zustand | Props | 1×1–2×2 | P0 | 3 | Annahme |
| E1-ENV-05 | Kartenrand/Hintergrund-Panorama (Wald, Klippen, Höhleneingang) | Umgebung | Modular, 4 Teile à 1024² | P1 | 3 | Annahme |
| E1-ENV-06 | Gesperrte Bauflächen: Nebel/Wolken + Freischalt-Effekt | Umgebung/VFX | Tiles + 12 Fr. | P1 | 2 | Kap. 4.3 Platz/Grundstück |
| E1-ENV-07 | Ambient-Leben: Mammut-Herde, Vögel, Lagerfeuer-Rauch | Umgebung/Anim. | 3 Loops | P2 | 4 | Thema Mammuts (Kap. 5) |
| E1-ENV-08 | Kampagnen-Weltkarte Epoche 1 (vertikal scrollend) für ca. 20 Missionen + Boss | Karte | 1080×5760 (3 Bildschirme), modular | P1 | 6 | Kap. 5: 20–30 Missionen + Boss; VS ~20 |
| E1-ENV-09 | Missionsknoten-Set: gesperrt, offen, 1–3 Sterne, Boss-Knoten, Pfad-Segmente | Karte/UI | 8 Elemente | P0 | 1 | Kap. 3.1 Sterne |
| E1-ENV-10 | Schlachtfeld-Hintergrund 1: Steppe | Kampf-BG | 1080×1920 + Parallax 3 Ebenen | P0 | 2,5 | Kap. 6.4 Auto-Kampf |
| E1-ENV-11 | Schlachtfeld-Hintergrund 2: Wald/Fluss | Kampf-BG | 1080×1920, 3 Ebenen | P1 | 2,5 | Annahme |
| E1-ENV-12 | Schlachtfeld-Hintergrund 3: Winter/Höhle | Kampf-BG | 1080×1920, 3 Ebenen | P1 | 2,5 | Kap. 5 Winter |
| E1-ENV-13 | Boss-Arena Epoche 1 | Kampf-BG | 1080×1920, 3 Ebenen | P1 | 3 | Kap. 4.3 Boss |
| E1-ENV-14 | Formations-Raster 3×2 auf dem Schlachtfeld (Slots, Highlight, Drag-Feedback) | Kampf/UI | 6 Slot-Sprites + States | P0 | 1 | Kap. 7.4 |

## F. UI & Icons

Die UI-Grundsysteme werden einmalig gebaut und gelten epochenübergreifend (`e0`). Was Epoche-1-spezifisch ist, trägt das Präfix `e1`. Bildschirme ohne Grafik-Abnahme (Wireframes) sind nicht enthalten.

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E0-UI-01 | UI-Kit Basis: Panels (9-Slice), Buttons 5 Typen × 4 Zustände, Tabs, Toggles, Slider, Schließen-/Zurück-Buttons | UI | 9-Slice-Set | P0 | 8 | Styleguide 7.3/7.5 |
| E0-UI-02 | Ressourcen-HUD (Leiste oben, Zähler, Lager-voll-Zustand) | UI | 1080×200 | P0 | 1,5 | Kap. 4.2/4.3 |
| E0-ICO-01 | Ressourcen-Icons: Nahrung, Holz, Stein, Gold, Wissen, Einwohner/Arbeiter | Icon | 6 × 512 → 128/96/64 | P0 | 3 | Kap. 4.2 |
| E0-ICO-02 | Helden-Ressourcen-Icons: Heldenerfahrung, Heldenfragmente, Aufstiegsmaterial | Icon | 3 × 512 | P1 | 1,5 | Kap. 4.2 |
| E0-ICO-03 | Premium-Währung-Icon (Edelsteine/Kristalle – Name offen) inkl. Mengen-Stapel (3 Größen) | Icon | 4 × 512 | P1 | 1,5 | Kap. 4.2 „Name offen“ |
| E0-ICO-04 | Soldatentyp-Icons (6) + Konter-Ring-Grafik | Icon | 6 × 512 + 1 Grafik 1024² | P0 | 3 | Kap. 6.2, 9.2 Farbcode |
| E0-ICO-05 | Heldenklassen-Icons: Krieger, Schütze, Taktiker, Heiler, Assassine, Baumeister | Icon | 6 × 512 | P1 | 2,5 | Kap. 7.3 |
| E0-ICO-06 | Formations-Typ-Icons: Keil, Schildwall, Zange | Icon | 3 × 512 | P1 | 1 | Kap. 7.4 |
| E0-ICO-07 | Status-Icons: Winter, Lager voll, Bereit zum Einsammeln, Vorteil/Nachteil-Pfeil, Sterne | Icon | 8 × 256 | P0 | 1,5 | Kap. 4.3, 5, 6.2 |
| E0-ICO-08 | Navigations-Icons: Stadt, Kampagne, Helden, Formationen, Shop, Events, Einstellungen, Post/Aufgaben | Icon | 8 × 256 | P0 | 2 | Kap. 3 |
| E0-UI-03 | Rarity-Rahmen Heldenkarte N/R/SR/SSR + Sterne + Typ-/Klassen-Badge | UI | 4 Rahmen 512×768 | P0 | 2,5 | Kap. 7.2 |
| E0-UI-04 | Screen Formationen/Layouts (3×2, gespeicherte Layouts PvP-Angriff/-Verteidigung/Events/Bosse) | UI-Screen | 1080×1920 | P0 | 2 | Kap. 7.4 |
| E0-UI-05 | Screen Heldenübersicht + Heldendetail (Level, Aufstieg, Fähigkeiten) | UI-Screen | 2 × 1080×1920 | P1 | 2,5 | Kap. 7.5 |
| E0-UI-06 | Screen Gebäude-Info/Upgrade (Kosten, sofort bauen) + Arbeiterzuweisung | UI-Screen | 2 Screens | P0 | 2 | Kap. 3.1, 4.3 Arbeiter |
| E0-UI-07 | Screen Truppenausbildung (Kosten, Bevölkerung) | UI-Screen | 1 Screen | P0 | 1 | Kap. 3.1 |
| E0-UI-08 | Kampf-HUD: Lebensbalken (Freund/Feind), Auto, 2×, Ultimate-Buttons, Pause | UI | Set | P0 | 2 | Kap. 6.4 |
| E0-UI-09 | Kampf-Ergebnis Sieg/Niederlage inkl. Sterne + Beute | UI-Screen | 2 Screens | P0 | 1,5 | Kap. 3.1 |
| E0-UI-10 | Missions-Vorbereitung (Gegner-Vorschau, Konter-Hinweis) | UI-Screen | 1 Screen | P1 | 1 | Kap. 6.2 |
| E0-UI-11 | Offline-Ertrag-Popup | UI | 1 Popup | P1 | 0,5 | Kap. 3.1, 11.1 |
| E0-UI-12 | Dialog-/VN-Box, Namensschild, Sprechblasen (rund/gezackt) | UI/Story | Set | P0 | 1,5 | Kap. 9.1 VN-Dialoge |
| E0-UI-13 | Tutorial-Elemente: Zeigehand, Pfeile, Fokus-Maske | UI | Set + 6 Fr. Hand-Anim. | P0 | 1 | Kap. 11.1 Onboarding |
| E1-UI-14 | Epochen-Ornament-Set Steinzeit (Kopfzeilen, Ecken, Banner) | UI | Set | P1 | 2 | Styleguide 7.5 |
| E1-UI-15 | Winter-Ankündigung (Banner + Jahreszeiten-Indikator) | UI | 2 Elemente | P1 | 0,5 | Kap. 5 Winter |
| E0-UI-16 | Beschwörung (Gacha): Banner-Rahmen, Ziehen-Animation, Wahrscheinlichkeiten-Panel, Pity-Zähler | UI-Screen | Screen + Anim. | P1 | 4 | Kap. 7.6, 10.3 Offenlegung; Gacha noch offen (Frage 2) |
| E0-UI-17 | Shop-Grundlayout + Angebotskarte (Testkäufe) | UI-Screen | 1 Screen + Karte | P1 | 2 | Roadmap Q2 2027 Monetarisierungs-Hooks |
| E0-UI-18 | Battle-Pass-Screen (kostenlose + Premium-Spur) | UI-Screen | 1 Screen | P2 | 2,5 | Kap. 10.2; Roadmap Q3 2027 |
| E0-UI-19 | Rewarded-Ad-Button + Belohnungs-Popup | UI | 2 Elemente | P2 | 0,5 | Kap. 10.2 |
| E0-UI-20 | Tägliche Aufgaben + 7-Tage-Login-Kalender | UI-Screen | 2 Screens | P2 | 2 | Kap. 11.1 |
| E0-UI-21 | Einstellungen, Konto/Login, Sprache DE/EN | UI-Screen | 1 Screen | P1 | 1 | Kap. 12.4/12.5 |
| E0-UI-22 | Arena-Screen (Gegnerliste, Versuche) | UI-Screen | 1 Screen | P2 | 2 | Kap. 8.1; Roadmap Q3 2027 |
| E0-UI-23 | Ladebildschirm + Splash-Screen | UI | 1080×1920 | P1 | 1,5 | Kap. 15.3 Ladezeit |

## G. VFX & Comic-Effekte

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E0-VFX-01 | Treffer-Funke normal + Krit mit Soundword „BAM!“ | VFX | 6–8 Fr. je | P0 | 1,5 | Kap. 9.1 |
| E0-VFX-02 | Sofortbau/Upgrade „Puff“: Staubwolke + Speedlines + „ZACK!“ | VFX | 10 Fr. | P0 | 1 | Keine Bauzeiten (Kap. 2) |
| E0-VFX-03 | Ressourcen-Einsammeln: fliegende Icons + Zähler-Pop | VFX | Partikel + 4 Fr. | P0 | 1 | Kap. 3.1 |
| E1-VFX-04 | Projektil-Einschläge: Schleuderstein, Felsbrocken (Flächenschaden) | VFX | 2 × 8 Fr. | P0 | 1 | Kap. 6.1 Flächenschaden |
| E1-VFX-05 | Heilen/Buff Schamane (Aura, Zahlen grün) | VFX | 10 Fr. | P0 | 1 | Kap. 6.1 |
| E0-VFX-06 | KO-Wolke (Comic-Rauch, Sterne) | VFX | 6 Fr. | P0 | 0,5 | Styleguide 5.3 kein Blut [Annahme] |
| E0-VFX-07 | Helden-Ultimate-Cut-In (Gesichtsausschnitt + Speedlines-Rahmen) – Vorlage, Bild pro Held | VFX/UI | Vorlage + 1 Crop je Held | P1 | 2 | Kap. 6.4 Ultimate |
| E0-VFX-08 | Level-up / Aufstieg Held (Glow, Sterne) | VFX | 12 Fr. | P1 | 1 | Kap. 7.5 |
| E0-VFX-09 | Beschwörungs-Effekte je Rarity (4 Stufen) | VFX | 4 × 12–16 Fr. | P1 | 3 | Kap. 7.2/7.6 |
| E1-VFX-10 | Winter-Einbruch: Schneefall-Partikel + Übergang | VFX | Partikel | P1 | 1 | Kap. 5 |
| E0-VFX-11 | Konter-Vorteil-Popup im Kampf (Pfeil + Typ-Icons) | VFX/UI | 6 Fr. | P1 | 0,5 | Kap. 6.2 |

## H. Story, Cutscene & Marketing

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) | Bezug |
|---|---|---|---|---|---|---|
| E1-STY-01 | VN-Hintergründe Epoche 1 (z. B. Lagerfeuer, Höhle, Steppe, Winterlager) | Story-BG | 4 × 2160×3840 → 1080×1920 | P1 | 8 | Kap. 9.4: 20–40 Szenen bis Launch |
| E1-STY-02 | Tutorial-/Intro-Comicpanels (Kampagnen-Einstieg) | Story | 3–4 Panels | P1 | 4 | Kap. 11.1 Onboarding |
| E1-STY-03 | Epochen-Aufstiegs-Cutscene Steinzeit → Bronzezeit (animierte Standbilder, teilbarer Clip) | Cutscene | 4–6 Standbilder + Spine/Kamera-Anim., 1080×1920 | P1 | 10 | Kap. 5: großer Belohnungsmoment; Kap. 9.4 |
| E1-STY-04 | Bindungsszene Helden-Paar (1 Beispielszene) | Story | 1 Illustration 1080×1920 | P2 | 4 | Kap. 7.5 Bindungs-Stufen |
| E0-MKT-01 | App-Icon (adaptive Icon: Vorder-/Hintergrundebene) | Marketing | 512×512 + adaptive Layer 432×432 [Stand prüfen] | P1 | 1,5 | Kap. 12.4 Play Console |
| E0-MKT-02 | Key-Art / Play-Store-Feature-Grafik | Marketing | Key-Art 4000×2250 → 1024×500 [Stand prüfen] | P2 | 5 | Kap. 1.2 Marketing |
| E0-MKT-03 | Store-Screenshot-Rahmen (Hochformat) | Marketing | 8 × 1080×1920 | P2 | 2 | Kap. 1.2 |

---

## Abhängigkeiten & Reihenfolge

1. **Styleguide-Tests zuerst:** E1-HER-00, E1-TRP-00, dann die Style-Tests E1-HER-01–03, E1-TRP-01 und E1-BLD-01. Freigabe „Art-Stil“ ist Go/No-Go für Q1 2027 (Roadmap).
2. **Technik-Spike parallel** (Plan Kap. 18.2): E1-TRP-01 als Spine-Testfigur auf einem günstigen Android-Gerät. Das Ergebnis entscheidet, ob die Truppen in Spine oder als Sprite-Sheet produziert werden (Aufwand Truppen ±30 %) **[Annahme]**.
3. **UI-Kit (E0-UI-01) vor allen Screens.** Die Icon-Familien folgen danach im selben Stil.
4. **Terrain (E1-ENV-01) vor Gebäuden**, damit Footprints, Pivot und Licht direkt auf echtem Boden geprüft werden.
5. **Stufen 2–3 (E1-BLD-14) erst nach Wirtschafts-Simulation**, weil dort festgelegt wird, welche Level welche Optik bekommen.
6. **Winter-Assets (BLD-16, ENV-03, VFX-10)** erst, wenn die Jahreszeiten-Mechanik im Prototyp bestätigt ist.
7. **Gacha-UI (E0-UI-16)** hängt an der offenen Frage 2 (Gacha ja/nein). Bei „nein“ entfällt sie, und stattdessen kommt ein Direkt- oder Fragment-Erwerb-Screen.

## Mengen-Check gegen Plan (Kap. 9.4, bis Global Launch)

| Plan-Mengengerüst (4 Epochen) | Anteil Epoche 1 in dieser Liste |
|---|---|
| Helden 25–35 | 6–8 (VS) |
| Truppen 24 (6 × 4) | 6 Rigs (Basis für alle Epochen) |
| Gebäude 15–20 Typen × 3–5 Stufen × 4 Epochen | 13 Typen, 3 Stufen für 11 Kerngebäude |
| Gegner/Bosse 15–25 | 6 Einträge (davon 1 Palettentausch-Set) |
| UI-Elemente/Icons 300–600 | ca. 120–180 Einzelelemente (UI-Basis gilt epochenübergreifend) **[Schätzung]** |
| Story-Szenen/Hintergründe 20–40 | 4 VN-BGs + 3–4 Panels + 1 Bindungsszene |
| Epochen-Aufstiegs-Cutscenes 4 | 1 (Steinzeit → Bronzezeit) |

*Ende Asset-Liste v0.1. IDs bleiben stabil. Neue Assets werden fortlaufend angehängt und nicht umnummeriert.*

---

## I. Ergänzung 13.10.2026: Beschwörung, Rarity, Helden-Karten (Helden über Fortschritt **und** Beschwörung)

| ID | Asset | Kategorie | Größe / Frames | Prio | Aufwand (PT) [Schätzung] | Bezug |
|---|---|---|---|---|---|---|
| E0-UI-SUM-01 | Beschwörungs-Screen: Hintergrund (Totemkreis/Ahnenstein bei Nacht, epochenneutral überlagerbar), Banner-Slot 1032×560, Buttons „1×“ / „10×“ mit Kosten (Kristalle/Ticket), Pity-Zähler, Raten-Info-Button, Gratis-Badge | UI | BG 1080×1920 (+ Safe-Bleed 1242×2688), Layout-Mock | P0 | 3 | Kap. 7.6, summon_banners.csv |
| E0-UI-SUM-02 | Banner-Artworks je Banner (Held-Splash + Titel) | UI/Illustration | 1032×560 | P1 | 1 je Banner | summon_banners.csv |
| E0-UI-SUM-03 | Ergebnis-Screen: 1er-Reveal (Vollbild-Karte) + 10er-Raster (2×5 Karten), „NEU!“-Stempel, Duplikat → Splitter-Umrechnung | UI | 1080×1920 | P0 | 2 | Kap. 7.6 |
| E0-VFX-SUM-01 | Beschwörungs-Animation: Totem lädt auf → Lichtsäule → Karte dreht sich; Farbe der Säule = Rarity (grau/blau/violett/gold), Legendär mit Extra-Phase (Screen-Flash, Speedlines, Soundword „ZAAAP!“) | VFX | 3–4 s, Spine oder Particle + 12–16 Fr. Sprites, Skip ab 0,5 s | P0 | 4 | Styleguide 5 VFX |
| E0-VFX-SUM-02 | Rarity-Glanz-Loop für Rahmen Episch/Legendär (UI-Shader Sweep) | VFX/Shader | Shader + Maske 256 | P1 | 1 | Styleguide Rarity |
| E0-UI-RAR-01 | Rarity-Rahmen Gewöhnlich/Selten/Episch/Legendär (9-Slice, Fill-Center aus) – **Placeholder vorhanden** `ui/cards/ui_rarity_*.png` | UI | 256×256, Border 40 | P0 | 1 (final) | ui-kit.md 4.6 |
| E0-UI-RAR-02 | Rarity-Edelstein-Icons + Sterne (1–6) für Stufen/Aufstieg | UI/Icon | 64 + 128 | P0 | 0,5 | Kap. 7 |
| E0-UI-HER-01 | Helden-Karte (Sammlung): Portrait-Crop im Rarity-Rahmen, Name, Typ-Icon (6 Typfarben), Sterne, Level, Gesperrt/Splitter-Fortschritt | UI | 300×420 (Liste 3 Spalten), groß 720×1000 | P0 | 2 | heroes.csv |
| E0-UI-HER-02 | Helden-Kartenportraits (Crop aus Splash) je Held | Illustration | 300×420 je Held (6–8 VS-Helden) | P0 | 0,5 je Held | Abschnitt A |
| E0-UI-HER-03 | Helden-Detail-Screen (Splash, Skills aus hero_skills.csv, Ausbau-Button, Herkunft „Fortschritt“ vs. „Beschwörung“-Label) | UI | 1080×1920 | P1 | 2 | heroes.csv, hero_skills.csv |
| E0-UI-HER-04 | Fortschritts-Freischaltung: Popup „Held schließt sich an!“ nach Kampagnen-Meilenstein (gleiche Karte, Ribbon statt Säule) | UI/VFX | Popup 1032×1300 | P0 | 1 | Kap. 7 |

---

## UI-Art Lieferung 1 (14.10.2026, Placeholder v001, Dev-IDs = Dateiname)

| ID (Datei `<id>.png`) | Ordner `ui-kit/` | Zuordnung | Prio | Status |
|---|---|---|---|---|
| ui_quest_banner | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_quest_banner_done | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_ico_quest | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_ico_chest | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_progressbar_bg | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_progressbar_fill | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_siedlerfeuer_pill | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_ico_siedlerfeuer | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_tag_siedlerfeuer_x4 | quest/ | E0-UI-QST (Quest/Siedlerfeuer, UI-Plan §5) | P0 | Placeholder geliefert |
| ui_unitcard_header | army/ | E0-UI-04/Army (Unit-Header) | P0 | Placeholder geliefert |
| ui_resbar_gradient | resbar/ | E0-UI-01 Resbar | P0 | Placeholder geliefert |
| ui_summon_bg_bleed | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| ui_summon_bg | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| ui_summon_banner_frame | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| ui_btn_rates_info | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| ui_stamp_new | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| ui_ico_shard | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| ui_badge_free | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| ui_pity_fill | summon/ | E0-UI-SUM-01 | P0 | Placeholder geliefert |
| vfx_summon_pillar_common_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_cardflip_common_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_pillar_rare_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_cardflip_rare_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_pillar_epic_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_cardflip_epic_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_pillar_legendary_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_cardflip_legendary_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_summon_legendary_zaaap_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_rarity_shine_epic_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_rarity_shine_legendary_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| ui_rarity_shine_mask | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| vfx_instant_build_sheet | vfx/ | E0-VFX-SUM-01/02, E0-VFX-02 | P0 | Placeholder geliefert |
| ui_ico_lock | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_btn_close | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_ico_plus | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_ico_menu | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_badge | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_avatar_frame | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_ico_arrow | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_ico_skull | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_ico_star | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_path_dot | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_btn_fab_build | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_ribbon | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_ribbon_white | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_filter_chip_active | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| ui_filter_chip | common/ | E0-UI-01 fehlende Sprites (UI-Plan §2/§7) | P0 | Placeholder geliefert |
| unit_inf | units/ | E0-ICO-04 (Platzhalter-Portraits) | P0 | Placeholder geliefert |
| unit_spear | units/ | E0-ICO-04 (Platzhalter-Portraits) | P0 | Placeholder geliefert |
| unit_ranged | units/ | E0-ICO-04 (Platzhalter-Portraits) | P0 | Placeholder geliefert |
| unit_cav | units/ | E0-ICO-04 (Platzhalter-Portraits) | P0 | Placeholder geliefert |
| unit_siege | units/ | E0-ICO-04 (Platzhalter-Portraits) | P0 | Placeholder geliefert |
| unit_support | units/ | E0-ICO-04 (Platzhalter-Portraits) | P0 | Placeholder geliefert |
| unit_locked | units/ | E0-ICO-04 (Platzhalter-Portraits) | P0 | Placeholder geliefert |
| ui_campaign_node_done | campaign/ | Kampagnen-Karte | P0 | Placeholder geliefert |
| ui_campaign_node_current | campaign/ | Kampagnen-Karte | P0 | Placeholder geliefert |
| ui_campaign_node_locked | campaign/ | Kampagnen-Karte | P0 | Placeholder geliefert |
| ui_campaign_node_boss | campaign/ | Kampagnen-Karte | P0 | Placeholder geliefert |
| ui_mission_reinforce_banner | mission/ | Missions-Screen „Armee verstärken“ (GDD Olm-Boss-Moment) | P0 | Placeholder geliefert |
| ui_ico_reinforce | mission/ | Missions-Screen „Armee verstärken“ (GDD Olm-Boss-Moment) | P0 | Placeholder geliefert |
| ui_power_fill | mission/ | Missions-Screen „Armee verstärken“ (GDD Olm-Boss-Moment) | P0 | Placeholder geliefert |
| ui_power_marker | mission/ | Missions-Screen „Armee verstärken“ (GDD Olm-Boss-Moment) | P0 | Placeholder geliefert |
| vfx_reinforce_speedlines_sheet | mission/ | Missions-Screen „Armee verstärken“ (GDD Olm-Boss-Moment) | P0 | Placeholder geliefert |
| ui_reinforce_speedlines_mask | mission/ | Missions-Screen „Armee verstärken“ (GDD Olm-Boss-Moment) | P0 | Placeholder geliefert (ersetzt _overlay) |

Details/9-Slice: `ui-kit/lieferung-ui-art.md`. Rarity-Mapping bestätigt: R = Selten (blau), SR = Episch (lila), SSR = Legendär (gold); Gewöhnlich nur Items.

## UI-Art Lieferung 3 (14.10.2026)

| ID | Ordner `ui-kit/` | Zuordnung | Prio | Status |
|---|---|---|---|---|
| ui_ico_winter | resbar/ | E1-UI-15 / E0-ICO-07 Status (Winter/Hunger) | P0 | Placeholder geliefert |
| ui_ico_hunger | resbar/ | E1-UI-15 / E0-ICO-07 Status (Winter/Hunger) | P0 | Placeholder geliefert |
| ui_tag_winter | resbar/ | E1-UI-15 / E0-ICO-07 Status (Winter/Hunger) | P0 | Placeholder geliefert |
| ui_tag_hunger | resbar/ | E1-UI-15 / E0-ICO-07 Status (Winter/Hunger) | P0 | Placeholder geliefert |
| ui_tag_winter_bg | resbar/ | E1-UI-15 / E0-ICO-07 Status (Winter/Hunger) | P0 | Placeholder geliefert |
| ui_tag_hunger_bg | resbar/ | E1-UI-15 / E0-ICO-07 Status (Winter/Hunger) | P0 | Placeholder geliefert |
| banner_tutorial | summon/ | E0-UI-SUM-02 banner_tutorial | P0 | geliefert (Komposition aus AD-Splash) |

## UI-Art v002 Leitbild-Anpassung (14.10.2026)

| ID | Pfad | Änderung | Status |
|---|---|---|---|
| ui_avatar_frame_v002 | ui-kit/common/ui_avatar_frame_v002.png | Holz #C98B4B statt Gold, kein Glanzstern (Gold nur SSR) | v002 geliefert, v001 bleibt |
| ui_btn_fab_build_v002 | ui-kit/common/ui_btn_fab_build_v002.png | Glanzstern entfernt | v002 geliefert, v001 bleibt |
| ui_ico_chest_v002 | ui-kit/quest/ui_ico_chest_v002.png | Glanzstern entfernt | v002 geliefert, v001 bleibt |
| ui_ico_siedlerfeuer_v002 | ui-kit/quest/ui_ico_siedlerfeuer_v002.png | Glanzstern entfernt | v002 geliefert, v001 bleibt |
| ui_panel_light_v002 | ui/panels/ui_panel_light_v002.png | ohne Nieten (Standard) | v002 geliefert, v001 bleibt |
| ui_panel_light_rivets_v002 | ui/panels/ui_panel_light_rivets_v002.png | dezente Nieten (klein, Ton-in-Ton, ohne Outline) – nur große Panels ≥ ca. 800 px | v002 geliefert, v001 bleibt |
| ui_panel_dark_v002 | ui/panels/ui_panel_dark_v002.png | ohne Nieten (Standard) | v002 geliefert, v001 bleibt |
| ui_panel_dark_rivets_v002 | ui/panels/ui_panel_dark_rivets_v002.png | dezente Nieten – nur große Panels | v002 geliefert, v001 bleibt |

## UI-Art Lieferung 5 – HUD-Icons F5 (16.10.2026)

| ID | Ordner | Zuordnung | Prio | Status |
|---|---|---|---|---|
| ui_ico_event | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_shop | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_pass | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_vip | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_mail | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_guild | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_daily | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_modes | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_more | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_collapse | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_settings | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_arena | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_worldboss | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |
| ui_ico_tower | ui-kit/hud/icons/ | E0-ICO-08 Navigation / F5 HUD | P0 | Pillow geliefert |


## UI-Art Lieferung 7 – F5 HUD v5.4 Stil C (freigegeben, 2026-10-16)
- Mockups: `hud/v5/mock_hud_f5_v5_4_C.png`, `hud/v5/mock_hud_f5_v5_4_C_ressourcen.png`. Vorschau: `previews/contact_hud_f5_v5.png`.
- Export: `hud/v5/export/` mit 36 Sprites `hud_c_*`, `hud_layout.csv` und `HANDOFF_DEV_UI.md`.
- IDs: Rahmen `hud_c_frame_{panel,pill,pill_slim,sheet,tile}`, `hud_c_sheet_handle`, `hud_c_tab_{normal,active}`, `hud_c_btn_{plus,close}`, `hud_c_badge_{dot,level}`, `hud_c_avatar_ring`, `hud_c_bar_{track,fill}`, `hud_c_evt_mammutjagd`, Icons `hud_c_ico_{kristall,gold,slot3,ressourcen,events,shop,pass,mehr,dorf,armee,bauen,helden,karte,holz,stein,nahrung,einwohner,vorrat,felle,fackel}`.
- 9-Slice: pill 190/170/190/170, pill_slim 85/75/85/75, panel und sheet 65, tile 100, bar_track 8/6/8/6, bar_fill 6/0/6/0.
- Quellen: 5 Nano-Banana-Gens (`e0_ui_hud_v5_*` im Register), Skripte `tools/ui_art_hud_v5*.py`. Bauen ist ein normaler Tab.


## UI-Art Lieferung 7.1 – F5 HUD v5.5 (2026-10-16, nur Skript)
- Dritter Top-Slot = Wissen: `hud/v5/export/hud_c_ico_wissen.png` (Skript `tools/ui_art_hud_v5_wissen.py`: Steintafel aus der ico_slot3-Textur, leuchtende Rune, Verlauf, Kontur, Glanz). `hud.currency_3 = wissen`.
- Badges nur am Events-Einstieg und an den Tabs Armee/Helden, kein Badge am Pass (CSV, Handoff, Mock).
- Pillen 262 px, Auto-Size 30–40, Messwerte im Handoff.
- Mockups: `hud/v5/mock_hud_f5_v5_5_C.png`, `hud/v5/mock_hud_f5_v5_5_C_ressourcen.png`. Vorschau: `previews/contact_hud_f5_v5.png`.
- UI-Art 7.1 Nachtrag: hud_c_ico_wissen (NB), Pillenformat K/M/B, Iconset-Plan hud/v5/ICONSET_EPOCHEN.md.
- 7.1 Nachtrag 2: hud_c_ico_quest, hud_c_ico_forschung, hud_c_ico_einstellungen (1 Gen), Basis-Set eiszeit vollständig.

- Lieferung 7.2 (v5.6, nur Skript, Kosten 0 $): Mockups `hud/v5/mock_hud_f5_v5_6_C_{frueh,spaet,ressourcen}.png`, Vorschau `previews/contact_hud_f5_v5.png` (3 Zustände). Unlock-Schema `unlock.<element_id>` in CSV und Handoff, Shop/Pass auf 64 px zurückgenommen, Beispielwerte statt ###, Gold als Epochen-Skin (Muschel-Gen offen).

- Lieferung 7.3 (v5.7, 1 Gen, ca. 0,07 $): Tooltip-Mock Währungen, Event-Kachel einklappbar (`hud.event_tile.collapsed`), Kerbe und Unterstrich am aktiven Tab. Neue Icons `hud_c_ico_{gold_eiszeit,gold_e2,bauen,armee}` (alte als `_alt`). Mockups `hud/v5/mock_hud_f5_v5_7_C_{frueh,spaet,tooltip,ressourcen}.png`, `hud/v5/tooltips_topbar_v5_7.png`, Vorschau `previews/contact_hud_f5_v5.png`.

- Lieferung 7.4 (17.10., v5.7 final, nur Skript, 0 $): Shop, Pässe/VIP und Angebote als ein Rand-Icon mit dezentem Punkt; Login-Kalender und Gratis gleich groß (Skript-Icons; Gen erledigt in 7.5); keine Login-Pop-ups, keine blinkenden Countdowns, max. 1 Angebots-Banner, U18 ohne Countdown. Mockups `hud/v5/mock_hud_f5_v5_7_C_final_{frueh,spaet,tooltip,ressourcen}.png`, Vorschau `previews/contact_hud_f5_v5.png`.

- Lieferung 7.5 (17.10., v5.7 final mit Auflagen, 1 Gen, ca. 0,064 $): Dock mit 96-px-Platten, 60-px-Icons, Label 24 px, Trefferfläche 144×144 (= 48 dp); Login, Gratis und Shop gleich groß. Mock früh mit Spielerlevel 3. Grünes Plus an Kristallen nur bei `unlock.hud_dock_shop` erfüllt und nicht U18. Event-Kachel mit neutralem Platzhalter `export/hud_c_evt_platzhalter.png` (ohne Mammut). Neue Icons `export/hud_c_ico_{login_kalender,gratis}.png` aus Gen `e0_ui_hud_v5_7_login_gratis` (Kerbholz, Vorratstopf; kein Metall, kein Stoff); Skriptfassungen als `_alt`. Mocks `hud/v5/mock_hud_f5_v5_7_C_final_{frueh,spaet,tooltip,ressourcen}.png`, Vorschau `previews/contact_hud_f5_v5.png`.

- Lieferung 7.6 (17.10., AD-Abnahme, nur Skript, 0 $): `hud_c_ico_gratis` ohne Getreideähren (kein Ackerbau in E1; `tools/ui_art_fx_gratis_ohne_aehren.py`), Event-Platzhalter mit grau-braunen Federn (`tools/ui_art_fx_naturfedern.py`). Die alten Fassungen liegen in `hud/v5/backup_v75/`. Login, Gratis und Platzhalter sind abgenommen AD. Lieferung 1–3 (17 Dateien) ist als Stil-alt, Redo F7+ markiert. Übergabe an Dev UI: `team/producer/apk_1710/uebergabe_art_ui_dev_ui.md`.
- Lieferung 7.7 (17.10., nur Skript, 0 $): `hud_c_ico_events` mit grau-braunen Federn (`tools/ui_art_fx_naturfedern.py`), vorher in `hud/v5/backup_v75/hud_c_ico_events_v001_federn.png`. Mocks und Vorschau neu.
