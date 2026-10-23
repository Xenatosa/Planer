# HUD-Fenster Scope D2 v1 (Dorf-HUD + Vollbild-Menüs)

Stand: 23.10.2026 (Europe/Berlin). Erzeugt für New Bot / Art-Pipeline.
Stil: D2 „Obsidian & Glut“. Chrome Dorf = v7.3b (Art-Kritiker 10/10).
Vollbild-Regel (Fabian 17.10.): nur Top-Ressourcenleiste + Inhalt + Dock — kein Dorf, keine Quest-Leiste, keine Seiten-Icons.
Visual-first (Fabian 23.10.): Wow über Illustration/Icons/Szenen; Text nur Titel, Zahlen, 1 kurze Zeile. Kein Dokument-UI.

Status-Legende:
- **fertig** = freigegebene Vorschau/Chrome, Maßplan + Kritik 10/10 (oder ausdrücklich abgenommen)
- **in Prüfung** = Maßplan + Vorschau unter `team/art/hud_d2/`, Freigabe offen
- **v1 verworfen** = Quick-PIL / Konzept verworfen, siehe `_alt_verworfen_20261023/`
- **fehlt** = noch kein D2-Maßplan + Vorschau unter `team/art/hud_d2/`

| Screen / Fenster | Typ | Status | Quelle / Notiz |
|---|---|---|---|
| Dorf-HUD Chrome (Top, Schienen, Quest, FAB Bauen, Dock) | Overlay auf Dorf | **fertig** | `vorschau_hud_d2_v7_3_lvl12.png`, Script `_src/render_vorschau_hud_d2_v7_3.py`, Kiste x=252 |
| Helden (Detail) | Vollbild | **v2b Lesbarkeit · in Prüfung** | `bg_menu_helden_comic_v1.png` unverändert; Vorschau `vorschau_menu_helden_d2_v2b.png`, Renderer `_src/render_vorschau_menu_helden_d2_v2b.py`; v2 bleibt erhalten, Layout basiert weiter auf v1-Maßplan |
| Bauen | Vollbild | **v2b Lesbarkeit · in Prüfung** | `bg_menu_bauen_comic_v1.png` unverändert; Vorschau `vorschau_menu_bauen_d2_v2b.png`, Renderer `_src/render_vorschau_menu_bauen_d2_v2b.py`; Gebäudebilder aus bestehendem Bauen-Mock |
| Armee | Vollbild | v1b freigegeben; **v2b Lesbarkeit · in Prüfung** | `bg_menu_armee_comic_v1.png` unverändert; Vorschau `vorschau_menu_armee_d2_v2b.png`, Renderer `_src/render_vorschau_menu_armee_d2_v2b.py`; v1b bleibt freigegebene Referenz |
| Beschwören | Vollbild | **v4 flach verworfen → Standard v8 + Featured v10 · Reveal in Prüfung** | Ritualhallen-BGs unverändert: `bg_menu_beschwoeren_std_comic_v2.png` / `bg_menu_beschwoeren_featured_comic_v2.png`; Standard `vorschau_menu_beschwoeren_d2_v8.png`, Featured Keyframes `vorschau_menu_beschwoeren_d2_featured_v10_closed.png` + `_open.png`; Karten-Draw über dem Portal, CTAs im unteren Drittel; Featured-Porträts Nara/Olm/Kiko bleiben klein und antippbar; Renderer `_src/render_vorschau_menu_beschwoeren_reveal_d2_v10.py`; PNGs in `menus_v3/` gespiegelt |
| Gilde (Stamm) | Vollbild (Dock) | **Innen v4b freigegeben / Außen v8 freigegeben** (Fabian 23.10.) | **Innenhalle + Außengelände**; innen ohne Icons=`vorschau_menu_gilde_d2_v4b_ohne_icons.png`; außen ohne Icons=`vorschau_menu_gilde_aussen_d2_v8_ohne_icons.png`; `massplan_menu_gilde_d2_v3.*` |
| Inventar | Vollbild (Dock) | v2 freigegeben; **v3b Lesbarkeit · in Prüfung** | `bg_menu_inventar_comic_v1.png` unverändert; Vorschau `vorschau_menu_inventar_d2_v3b.png`, Renderer `_src/render_vorschau_menu_inventar_d2_v3b.py`; Inventar-Layout aus v2 |
| Karte (Weltkarte) | Vollbild (Dock) | Maßplan/Vorschau v1 (Freigabe offen) | `massplan_menu_karte_d2_v1.*`, `vorschau_menu_karte_d2_v1.png` |
| Ressourcen / Lager-Liste | Overlay-Sheet | **in Prüfung · v2** | Bottom-Sheet auf Chrome v7.3b; `massplan_overlay_ressourcen_d2_v2.*`, `vorschau_overlay_ressourcen_d2_v2.png`; öffnet von Kiste |
| Mail | Vollbild-Menü | **v7 gültig; v1–v6 verworfen/alt** | `vorschau_overlay_mail_d2_v7.png`, `_spieler.png`, `_gelesen.png`; neues Vollbild-Postfach mit System-Siegelkarten und Spieler-Chatkarten; Alles gelesen nimmt System-Belohnungen an, Löschen nur ohne ungelesene Post/offene Belohnung; HTML `menus_v3/_src/html/v3_2_obsidian_mail_v7_interaktiv.html`, Renderer `_src/render_vorschau_overlay_mail_d2_v7.py`; frühere Mail-PNGs bleiben als Alt-Referenz erhalten |
| Mehr | Overlay-Sheet / Menü | **in Prüfung · v2** | 2×4 Bildkacheln auf Chrome v7.3b; `massplan_overlay_mehr_d2_v2.*`, `vorschau_overlay_mehr_d2_v2.png` |
| Shop-Sidebar | Sidebar links | Maßplan/Vorschau v1 (offen) | `vorschau_overlay_shop_sidebar_d2_v1.png` |
| Events-Sidebar | Sidebar links | Maßplan/Vorschau v1 (offen) | `vorschau_overlay_events_sidebar_d2_v1.png` |
| PvP-Sidebar | Sidebar links | Maßplan/Vorschau v1 (offen) | `vorschau_overlay_pvp_sidebar_d2_v1.png` |
| Angebote / Pass / Abo | Sheet / Vollbild | **fehlt** | aus Shop-Sidebar |
| Events (Detail) / Arena / Forschung / Einstellungen | div. | **fehlt** | Icons teils in `icons_v1` |

## Reihenfolge (empfohlen)
1. **Bauen v2b / Helden v2b / Armee v2b** mit eigenen Szenen — Lesbarkeit in Prüfung. Karte bleibt unverändert auf v1.
2. **Beschwören Standard v8 / Featured v10** (Reveal-Keyframes, Featured mit antippbarer Heldenwahl) — in Prüfung. **Gilde Innen v4b + Außen v8 bleiben unangetastet; Inventar v2 und Armee v1b bleiben freigegebene Referenzen.**
3. **Inventar v3b und Mail v7** — Mail v7 ist aktuell; die früheren Mail-Stände v1–v6 sind verworfen/alt. Ressourcen- und Mehr-Overlay v2 sowie Sidebar-Shop/Events/PvP bleiben auf den bisherigen Fassungen.

## Lesbarkeitspass 23.10.2026

Für die Lesbarkeitspass-Vorschauen gelten Inventar v3b sowie Helden/Armee/Bauen v2b. Beschwören wurde mit v8/v10 auf Karten-Reveal und untere CTAs umgebaut. Die frühere Mail v5 mit System-Briefpost und Spieler-Chatblasen ist durch Mail v7 abgelöst; alte PNGs bleiben nur als Referenz. Die Comic-Hintergründe bleiben unverändert; vorherige Vorschauen bleiben erhalten. Details: `BERICHT_beschwoeren_reveal_mail_tabs_2026-10-23.md`.

## Mail-Stand 23.10.2026

- **Aktuell:** Mail v7 unter `vorschau_overlay_mail_d2_v7*.png`, interaktives HTML und Renderer `render_vorschau_overlay_mail_d2_v7.py`.
- **Verworfen/alt:** Mail v1–v6; ihre PNGs bleiben unberührt und dienen nur der Historie, nicht als gültige Layout-Referenz.
- V7 ist ein eigenständiger Neuaufbau mit Vollbild-Tabs, automatischer System-Belohnungsannahme über „Alles gelesen“ und Löschsperre bis keine ungelesene Post/offenen Belohnungen verbleiben.

## Nicht anfassen
- `_alt/` (überholt, siehe `team/art/GUELTIG.md`)
- HUD v5 / `hud_c_ico_*` / `HudV5NumberFormat` (gestrichen 22.10.2026)
- Dorf-Chrome v7.3b neu bauen
- Unity-Code/PR ohne Vorschau-Freigabe (Fabian 23.10.)

## Dock (Vollbild, Stand HUD v7)
Tabs: Dorf · Helden · Karte · Armee · Gilde · Inventar. Icons: `icons_v1/d2_ico_dock_*.png`.
Bauen öffnet über FAB (Dorf-HUD); Dock-Tab **Dorf** aktiv.
Beschwören öffnet über Shop-Sidebar; Dock-Tab **Dorf** aktiv.
Armee / Helden / Inventar / Gilde / Karte: jeweiliger Dock-Tab aktiv.

## Verworfen 23.10.2026 ~09:55 (Fabian)
- `vorschau_menu_beschwoeren_d2_v1.png`, `vorschau_menu_inventar_d2_v1.png`, `vorschau_menu_gilde_d2_v1.png` → `_alt_verworfen_20261023/`
- Gründe: Quick-PIL ohne menus_v3-Qualität; altbacken; Beschwören „Platzhalter“-Label; Gilde flaches Listen-/Tab-Menü + Buchstaben-Avatare; zu textig/Dokument-UI.
- Neu: v2 HTML-Mocks (Chrome) + Maßplan v2; Gilde = scrollbare Hallen-Szene mit Hotspots; visual-first.

## Feedback Beschwören 23.10.2026 (Fabian)
- v2 mit großem Held/Ruka-Fullbody als Hauptmotiv **verworfen**.
- v3 (~10:09): zentraler legendary Idle-Lichtpfeiler wirkte wie **„eine Banane“** → **verworfen**.
- v4 (~10:20): PIL-Ritualkreis/Portal flach/technisch → **verworfen**; „Geht das nicht mehr 3D Comic die Beschwörung“ (wie Gildenhalle innen).
- v5: **3D-Comic-Ritualhalle** (`bg_ritualhalle_comic_v1`, Stil wie `bg_gildenhalle_innen_comic_v2`); Altar/Portal/Kreis+Trommel *im Raum*; Featured nur kleine Portrait-Avatare; kein Fullbody, kein Banane-Pfeiler.
- v2/v3/v4-Dateien bleiben als Referenz (`*_v2.*`–`*_v4.*`); Fullbody-, Banane- und flachen PIL-Ritual-Look nicht wiederholen.

## Feedback Gilde 23.10.2026 (Fabian)
- Gilde = **Innenraum der Gildenhalle**, 3D-Comic — nicht Außen/Wiese als alleiniges Hauptmotiv.
- **Beides nötig:** Innenhalle **und** Außengelände (vor/um die Halle), Umschalter Halle|Außen.
- v2 Außen-Vorschau (reine Wiese / Panorama-als-Hauptmotiv) verworfen — nicht wiederverwenden als Hauptmotiv.
- Inventar und Armee erstmal i.O.
- v3: Innen = `bg_gildenhalle_innen_comic_v2.jpg` + Hotspots (unverändert).
- v3b Außen (Fabian 23.10. ~10:15): Außengelände ebenfalls 3D-Comic — `bg_gildenhalle_aussen_comic_v1.png` (Composite, 0$); Vorschau `vorschau_menu_gilde_aussen_d2_v3b.png`. Platzhalter-panorama nur Fallback.
- v7 Außen (Fabian 23.10. ~10:38): v4–v6 verworfen. Spec >10 Gebäude + Gebirge. BG=`bg_gildenhalle_aussen_comic_v4`; Vorschau `vorschau_menu_gilde_aussen_d2_v7.png`; Kosten `kosten_gilde_aussen_v7.md`.
- v8 Außen (Fabian 23.10. ~10:43): v7 verworfen (Viewport nur ~3–5 Gebäude). Neu BG 3:4 densify `bg_gildenhalle_aussen_comic_v6b`; Vorschau `vorschau_menu_gilde_aussen_d2_v8.png`; Kosten `kosten_gilde_aussen_v8.md`. Viewport-Zählung: **12** Gebäude.
- v4 Innen (Fabian Art-Kritik 23.10. Note 7/10): Muss Hotspot-Glow ≫140², BG 720p-Upscale weich, Default-Scroll clippt Jagd/Peeks → behoben in `vorschau_menu_gilde_d2_v4.png` / `bg_gildenhalle_innen_comic_v3` (2K, 0,0598 USD). Erneut Art-Check Ziel 10/10.
