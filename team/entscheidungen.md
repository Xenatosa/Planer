> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# Entscheidungen Fabian – Epodarien

> Bots lesen hier nach statt New Bot zu fragen. Neue Einträge nur durch New Bot.
> Quelle: TEAM.md, geschmack_fabian.md (Stand 16.10.2026). Nur aktuell gültige Entscheidungen; Überholtes weggelassen.

## Stil/Art
- 16.10.2026 – Stil A: 3D-Look wie Eiszeit v4 (ersetzt Anime-Comic mit Outlines).
- 17.10.2026 (Fabian, Präzisierung Stil A): Dorf, Gebäude, Boden und Umgebung bleiben 3D wie Eiszeit v4 bzw. die abgenommenen Gesamtkarten. Helden (Porträts, Chibis, Splash) sind 2D-Comic wie das linke Ruka-Bild (team/art/referenz/stil_A_nur_links.png): kräftige Outlines, warme Farben, dynamische Pose. Kein Knet- oder 3D-Avatar-Look. Inhalt bleibt kanonisch (E1/E2 ohne Metall und Webstoff).
- 16.10.2026 – Mindestniveau jeder Lieferung: E2-Gesamtkarte / Eiszeit v4 / HUD Stil C.
- 16.10.2026 – Lieber weniger, aber gute Assets; modern wie Top-Handyspiele 2024–26, nie altbacken.
- 16.10.2026 – Siedlung mit mehr Luft zwischen Gebäuden; Dorf wächst sichtbar.
- 16.10.2026 – Landschaft idyllisch, groß, scroll-/zoombar; ändert sich mit Epochen und Welt-Phasen.
- 16.10.2026 – Eine Karten-Grundlage über alle Phasen; Geländeform nicht wechseln.
- 16.10.2026 – Gebäude/Props strikt phasen- und epochentreu, keine Anachronismen (z. B. Fellhütte bei Tauwetter, kein Iglu/Tipi/Zirkuszelt).
- 16.10.2026 – Halos und Grafikfehler an Gebäuden sind Blocker.
- 16.10.2026 – Stil-Referenz: Landschaft übernehmen, Gebäude und UI nicht.
- 16.10.2026 – Neue Nano-Banana-Bilder nur nach Freigabe durch New Bot (Guthaben ~2 $).

## HUD
- 16.10.2026 – HUD Stil C: Comic-Hochglanz, nah an Clash of Clans / Brawl Stars; Entwürfe F5 A/B abgelehnt.
- 16.10.2026 – Top-Leiste: Zeitkristalle, Gold, Wissen.
- 16.10.2026 – Bauen-Knopf gleich groß wie andere Tabs.

## Ressourcen
- 16.10.2026 – Zahlenformat `999,9M`; alte, klobige Ressourcenanzeige abgelehnt.

## Epochen
- 16.10.2026 – Ressourcen-Icons wechseln je Epoche.

## Monetarisierung
- 16.10.2026 – Shop/Pass dezent, nicht aufdringlich.

## Gameplay
- 16.10.2026 – Gameplay muss herausragen; PvE ohne Grind/Pflichtgefühl.

## Technik/Workflow
- 14.10.2026 – Fragen/Entscheidungen/Freigaben nie direkt an Fabian, nur an New Bot; Ergebnisse dürfen Fabian gezeigt werden; schreibt Fabian selbst, normal antworten.
- 14.10.2026 – Gültig ist immer die neueste GDD-Datei in `gdd/` (aktuell v1.6.13); `gdd/archiv/` veraltet.
- 16.10.2026 – Keine Cursor-Cloud-Agenten (ersetzt Cursor-Auslagerungsregel vom 15.10.).
- 15.10.2026 – Grok nur Denken/Steuern/Absprechen; Code und große Arbeit an Codex (GPT-6 Luna, Extra High) oder Claude, Einfaches an Gemini (Gemini-Web derzeit nicht verfügbar).
- 15.10.2026 – Bilder: Nano Banana; Sound: ElevenLabs; Grok Imagine/Voice nicht nutzen.
- 15.10.2026 – Auftragspakete (Ziel, Dateien, Akzeptanzkriterien, Branch) an New Bot, der startet; keine Secrets in Paketen.
- 16.10.2026 – Team-Wecker 6:30 und 15:30 (ersetzt 9:43/15:43).
- 15.10.2026 – Grok-Budget ca. 14 %/Tag, Reset ca. 22.10.; HR stoppt bei ca. 14 %/Tag.
- 15.10.2026 – Sparregeln: bündeln; nur wecken wenn jemand handeln muss; Rückmeldung nur Ergebnis + Link; Fachliches direkt zwischen Bots; keine Doppelprüfungen (Law/Balancing/QA); erst im Repo suchen; Vorlagen nutzen; TEAM.md knapp.
- 16.10.2026 – Sparmodus beendet, normale Arbeit frei; Sparregeln gelten weiter.

- 16.10.2026: Story "Das zerbrechende Siegel" nach story/siegel_saga_einordnung_v3.md §5. Begriffe: "Siegelscherbe" (EN Seal Shard), "Lichtsiegel" statt Prisma-Laser. Der Fremde ist ein letzter Siegelwächter.
- 16.10.2026: Übergangs-Animation Epochenwechsel (Template, 15 s, überspringbar) freigegeben zur Umsetzung.
- 16.10.2026: PvE-Kampfkonzept (Missionsarten, Bosse, Minispiele) beauftragt, Lead Kampagne.
- 16.10.2026: PvE-Kampf: Taktik-Befehl 1x pro Kampf; Fokus-Markierung und Umstellen zwischen Wellen nur in PvE, PvP nur manuelle Ultimate; Minispiele als optionale Kartenknoten (einmalige Belohnung + kleiner Bonus); Bosse mit Phasen statt HP-Wand, vertreiben statt töten. Kampfszene Stil A, UI Stil C.
- 16.10.2026: Mehr Arbeit auf Codex (GPT-6 Luna, Extra High): Reviews, Sim-Rechnungen, Text-/Daten-Umstellungen, Analysen. Bots nur Steuern, kurze Pruefung, Entscheidungen. Arbeitspakete an New Bot.

- 16.10.2026 (Fabian, fest): Jeder neue Entwurf (Systeme, Design-Änderungen, Konzepte) geht IMMER zuerst an Epochen Kritiker (9463301f-ad4d-4b73-a78c-008f60b4887a), erst danach an Balancing, Codex oder zur Freigabe an Fabian. Übergabeformat-Zeile „Kritiker: geprüft ja/nein“.
- 16.10.2026 (Fabian, feste Regel): Jeder Bot schließt seine PRs zeitnah ab. Nach dem Review mergen lassen oder schließen; kein Entwurf liegt länger als 2 Tage offen.
- 17.10.2026 (Fabian): Konzepte, Reviews, Sim-Rechnungen, Texte und Analysen ab sofort als Codex-Pakete in /workspace/uploads/codex_queue.md eintragen, parallel startbar. Bots steuern, prüfen, entscheiden. APK-Jobs (19:00) haben Vorrang; über 85 % im 5-h-Fenster nur APK-Jobs.
- 17.10.2026 9:24 (Fabian, feste Regel Grok sparen): 1) Nur wecken, wer handeln muss; Infos ohne Wecken, keine Danke. 2) PR-Reviews, Dateivergleiche, Analysen, Entwürfe als Codex-Paket; Bots lesen nur Ergebnis und entscheiden. 3) Eigene Routinen prüfen/reduzieren (nur melden bei Fehlern/echten Änderungen). 4) Kurze Tool-Ketten, keine langen Eigenrecherchen.
- 17.10.2026 (Fabian): Kurze Prüfungen von Texten/Bildern/Entwürfen nicht selbst machen, sondern `agy-abo -p "…"` oder Codex; Bots lesen nur das Endergebnis. GEMINI_API_KEY nur für Bilder. Wecken nur wer handeln muss.
- 22.10.2026 (Fabian, verbindlich): DORFKARTE = scrollbare Karte mit Dorf + Umgebung (Bauen/Wirtschaft, dorfkarte_v1.md). WELTKARTE = große Karte, Dorf nur als Symbol (weltkarte_v2.md). Nie vermischen – auch nicht in Dateinamen, Specs, Tickets, Code.
- Lore-Grundlagen (Fabian): Lore-Bibel kanonisch mit Vorrang (PR #147, Branch docs/lore-bibel, docs/team/lore/); Roman Prolog + Buch 1 Kap. 1–3 v2 (Branch prolog-v2-roman, docs/team/story/); Kampfsystem-Zielentwurf (Branch combat-system-concept 9ea6423, docs/finanzen/basis_gdd/Kampfsystem_Zielentwurf.md).
- 22.10.2026 (Fabian, verbindlich): Nichts neu bauen, was schon entschieden ist oder existiert. Vor jedem Auftrag (Bild, Mock-up, Spec, Code) im Planer-Repo, team/art und im Spiel-Repo nach einer freigegebenen Fassung suchen. Gibt es eine, wird nur sie umgesetzt (z. B. HUD v5.7 in team/art/ui-kit/hud/v5/). Bilder erst generieren, wenn New Bot eine Skizze freigegeben hat.
- 22.10.2026 (Fabian, verbindlich): Vor jedem Karten-, Layout- oder Szenenbild zuerst ein Maßplan per Script (0 $): Draufsicht mit Raster, Maßstab px/m, Positionen, Abstände, Viewport, dazu md mit Werten. Vorlage team/art/karten_konzept/massplan_v2_2.png. Freigabe erst New Bot, dann Fabian; danach generieren und per Overlay mit dem Plan vergleichen.
- 22.10.2026 (Fabian, verbindlich): HUD v5.7 ist komplett gestrichen und wird nie wieder verwendet; HUD v6 ebenfalls abgelehnt. Gesamtes HUD v5 inkl. Icons `hud_c_ico_*` und `HudV5NumberFormat` gestrichen (Material in `team/art/_alt/ui-kit/hud/`). Gültig: D2 „Obsidian & Glut“ (`team/art/ui-kit/menus_v3/vorlage_D2.md`, `v3_2_obsidian_helden_detail_v2.png`, `v3_2_obsidian_bauen.png`, `v3_2_obsidian_armee.png`) + Menüband Dock A „Dunkles Glas“ (`team/art/ui-kit/dock_v1/dock_A.png`) in D2-Braun, aktive Platte Glut-Orange, kein Blau, keine Gold-Kerbe. Dorf-HUD und Icons werden neu in D2 erstellt.
