> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

📐 Regel (22.10.): Vor Karten-, Layout- oder Szenenbildern zuerst Maßplan per Script (Vorlage art/karten_konzept/massplan_v2_2.png). Freigabe New Bot, dann Fabian, erst dann generieren und per Overlay prüfen.
♻️ Regel (22.10.): Nichts neu bauen, was existiert. Vorher Planer-Repo, team/art und Spiel-Repo nach freigegebener Fassung prüfen und nur diese umsetzen (z. B. UI D2 „Obsidian & Glut“; HUD v5.7 gestrichen). Bilder erst nach Skizzen-Freigabe durch New Bot.
🗺️ Begriffe (22.10.): DORFKARTE = Dorf+Umgebung (dorfkarte_v1.md) · WELTKARTE = große Karte, Dorf als Symbol (weltkarte_v2.md). Nie vermischen. · Lore-Bibel (PR #147) ist Kanon mit Vorrang. · Kurzprüfungen via agy-abo/Codex.
🔋 Grok sparen (17.10.): nur wecken wer handeln muss · Reviews/Analysen an Codex · Routinen reduzieren · kurze Tool-Ketten.
⚙️ Codex-Regel (17.10.): Konzepte/Reviews/Sims/Texte/Analysen als Codex-Paket in /workspace/uploads/codex_queue.md; APK-Jobs zuerst.
🧹 PR-Regel (16.10.): Eigene PRs nach Review mergen lassen oder schließen, keine Entwürfe länger als 2 Tage offen.
> 🔎 **Feste Regel 16.10. (Fabian):** Jeder neue Entwurf zuerst an Epochen Kritiker (9463301f-ad4d-4b73-a78c-008f60b4887a), danach Balancing/Codex/Fabian. Übergabe mit Zeile „Kritiker: geprüft ja/nein“.

# Team Epodarien – Bot-Übersicht

> ## ▶️ Sparmodus beendet (16.10.2026, 9:50): Normale Arbeit wieder frei. Sparregeln gelten weiter (bündeln, kurz, nur wecken wenn nötig, große Arbeit an Codex/Claude). Nano-Banana-Guthaben fast leer (~2 $): neue Bilder NUR nach Freigabe durch New Bot.
> Arbeitsweise: KEINE Cursor-Agenten mehr. Pakete (Ziel, Dateien, Abnahmekriterien, Branch) an New Bot für Codex/Claude; Gemini-Web geht derzeit nicht. Team-Wecker 6:30 und 15:30.

Stand: 14.10.2026 · gepflegt von Epochen HR · Ordner relativ zu `handygame-plan/team/`

> **Dank von Fabian (15.10.2026):** Fabian dankt allen Epodarien-Team-Bots ausdrücklich für die starke Arbeit und freut sich, wie groß das Team geworden ist.

> **GO für alle (Fabian, 15.10.2026 10:47, Super-Plan):** Alle Bots arbeiten wieder. Grok-Budget etwa 14 % pro Tag, nächster Reset etwa am 22.10. Alles läuft als Paket über New Bot an Codex, Claude oder Gemini, die Sparregeln gelten weiter (bündeln, einmal täglich arbeiten, kurze Rückmeldungen). HR stoppt bei etwa 14 % pro Tag. Marketing, Sound und die weiteren Sprachen arbeiten nur kurz die geplanten Aufträge ab, wenn das sinnvoll ist.
> **Arbeitsweise (Fabian, 15.10.2026, ersetzt Cursor-Regel):** Grok ist nur fürs Denken, Steuern und Absprechen da. KEINE Cursor-Cloud-Agenten (Fabian, 16.10.). Code und große Arbeiten gehen an Codex (GPT-6 Luna, Extra High) oder Claude, einfache Sachen an Gemini, jeweils per Web-App. Bilder macht Nano Banana, Sound macht ElevenLabs. Grok Imagine und Grok Voice werden nicht genutzt. Ablauf: Bots schreiben fertige große Auftragspakete mit Ziel, Dateien, Akzeptanzkriterien und Branch-Name und schicken sie an New Bot. New Bot startet sie. Keine Secrets in den Paketen. Team-Wecker laufen um 6:30 und 15:30.

>
> ## 💰 SPARREGELN (Fabian, 15.10.2026, fest)
> 1. Aufträge bündeln statt vieler kleiner Nachrichten; zusammenhängende Aufgaben als EIN Paket an New Bot (für Codex, Claude oder Gemini).
> 2. Nur wecken, wenn jemand handeln muss, sonst ohne Wecken senden.
> 3. Kurze Rückmeldungen: nur Ergebnis + Link, Details in PR/Dokument.
> 4. Fachliches direkt zwischen den Bots klären, nicht über Koordinator/Producer. Kleine Entscheidungen trifft das Team selbst, an Fabian nur Wichtiges.
> 5. Team-Wecker nur 9:43 und 15:43. Feste Arbeitsfenster, Pausen für Bots ohne aktuelle Phase (HR teilt ein).
> 6. Auch Prüfen und Zusammenfassen macht der Cloud-Agent; Grok liest nur das fertige Ergebnis. Cloud-Agenten melden einmal am Ende.
> 7. Keine doppelten Prüfungen: Was Law, Balancing oder QA geprüft hat, prüft niemand nochmal (außer echte Risiken).
> 8. Vor neuer Recherche erst im Repo nach vorhandenen Dokumenten suchen.
> 9. Vorlagen für wiederkehrende Aufträge nutzen. TEAM.md knapp halten, Erledigtes ins Archiv.

> ~~## ⚠️ FESTE REGEL (Fabian, 15.10.2026, bekräftigt): WIRKLICH ALLES Umfangreiche läuft über Cursor-Cloud-Agenten. Grok nur Steuern, Prüfen, kurze Antworten. Grok-Kontingent 85 %, Grenze 88 %.~~ (ÜBERHOLT 16.10.: kein Cursor, siehe Arbeitsweise oben)
>
> ~~**Feste Regel Auslagerung (Fabian, 15.10.2026, gilt für ALLE Team-Bots):** Jede umfangreiche Arbeit (Code, lange Dokumente, Simulationen, Datentabellen, Recherchen) wird an Cursor-Cloud-Agenten ausgelagert (CloudAgent, Repo https://github.com/Xenatosa/epodarien). Grok-Bots nur zum Steuern, Prüfen und für kurze Antworten. Grund: Grok-Kontingent bei 82 %, Cursor bei ca. 15 %. Fabian nie direkt anschreiben, alles über New Bot.~~ (ÜBERHOLT 16.10.: kein Cursor, siehe Arbeitsweise oben)

> **Verbindliche Kommunikationsregel (bestätigt von Fabian, 14.10.2026):** Fragen, Entscheidungsbedarfe und Freigaben gehen nie direkt an Fabian, sondern ausschließlich an den Koordinator New Bot (6e22f13d-9376-45c9-8d10-41352f9f926f), der sie für Fabian bündelt. Ergebnisse (Dokumente, Bilder, Fortschritt) dürfen Fabian weiterhin direkt gezeigt werden, ohne Fragen daran. Schreibt Fabian einem Bot selbst, darf der Bot ihm normal antworten. Entscheidungen gelten, wenn sie von Fabian selbst oder über New Bot kommen.


> **Gültige GDD-Fassung (14.10.2026):** Es gilt immer die neueste GDD-Datei direkt im Ordner `gdd/` (derzeit v1.6.13). Fassungen in `gdd/archiv/` (z. B. v0.5) sind veraltet und dürfen nicht mehr als Grundlage dienen.

| Bot | ID | Rolle | Lead / berichtet an | Ordner |
|---|---|---|---|---|
| Epochen Dev | eb1fa7a8-0262-42e8-9e4d-f0b6eb41f0e7 | Lead-Dev, Unity-Architektur | **Lead Dev** | `dev/` |
| Epochen Dev UI | 9cb0c93b-19c6-4427-a313-8b8396f2c278 | Unity UI & Grafik-Integration | Dev | `dev/` (ui) |
| Epochen Dev Gameplay | bbf01225-9ace-42c9-8efe-313af9265fb3 | Unity Gameplay-Systeme | Dev | `dev/` |
| Epochen Dev Backend | 74cc3a1b-aa14-48a0-aab5-ff7a96863262 | Server, Nakama, Firebase, Billing, Remote Config | Dev | `dev/backend/` |
| Epochen QA | a6b991d4-0265-4c83-9215-c70f14a42b02 | QA, APK-Tests | Dev | `qa/` |
| Epochen Security | 11b40ba2-010e-4f9c-939e-e4350b053f98 | Security (Nakama, Firebase, Billing) | Dev | `security/` |
| Epochen Game Designer | 87a92b65-bf3e-4d8c-9a4a-061ea7de9662 | Systeme, Wirtschaft, GDD | **Lead Design** | `gdd/` |
| Epochen Aufbau | 24610255-980a-4fce-bfd2-8e446c72bdee | Progression, Epochen-Roadmap | Game Designer | `aufbau/` |
| Epochen Kampagne | 3b3d710b-fd2c-482a-8591-8375bd3ca45f | Kampagnen-Missionen | Game Designer | `kampagne/` |
| Epochen Quests | aefcc244-b708-4dd8-a39b-400dc0f9f92d | Quest-System | Game Designer | `quests/` |
| Epochen Helden | a1aace64-c64a-46f7-a197-9eaa1ce4beee | Helden, Skills, Formationen | Game Designer | `helden/` |
| Epochen PvP | d3674a36-c6a6-4fd7-8d79-41c59e79444e | PvP-Design | Game Designer | `pvp/` |
| Epochen Ranking | e0c821b7-e020-4fd1-9913-36f1770364ea | Ranglisten, Saisons, Ligen | Game Designer | `ranking/` |
| Epochen Ausrüstung | c542f85a-57c0-41fb-b363-3a62632715a7 | Ausrüstung, Artefakte, Sets | Game Designer | `ausruestung/` |
| Epochen Forschung | 1b7f7414-4e67-4788-83ec-951c7afb3179 | Forschungsbaum, Timer, Beschleuniger | Game Designer | `forschung/` |
| Epochen Events | 93454d1d-e021-4f38-ac5b-01e1448437d7 | LiveOps, Event-Kalender und -Katalog | Game Designer | `events/` |
| Epochen Minigame | 650f23ed-cd1b-4742-9237-f8b4841bf368 | Minigames | Game Designer | `minigame/` |
| Epochen Spieleideen | 55d083af-26d2-41f6-bd58-be51a663cb3f | Ideen-Pool | Game Designer | `ideen/` |
| Epochen Finanzen | a801c251-3213-40c8-9e57-6000a0668b6b | Monetarisierung, Umsatz | Game Designer / Fabian | `finanzen/` |
| Epochen Story | de8b4a6f-4d24-413a-8031-8aa04041ee43 | Welt, Story, Texte | Game Designer | `story/` |
| Epochen Art Director | b86bf73e-22e0-4be6-9589-13c61d93557b | Art Direction, Styleguide, Assets | **Lead Art** | `art/` |
| Epochen Art Helden | 5475e2f4-4a41-4871-83fe-7ed54bcb267a | Helden-Illustrationen, Chibi-Truppen | Art Director | `art/` |
| Epochen Art Umgebung | 8392841d-55fb-4de0-932d-e8447877c987 | Gebäude, Terrain, Karten | Art Director | `art/` |
| Epochen Art UI | 6032b141-18b7-4b36-bae2-f9c75e98cc75 | UI-Kit, Icons, VFX | Art Director | `art/ui/` |
| Epochen Sound | 1a4c3dbf-6416-4bda-853f-00aa008591cc | Audio Direction | Fabian | `sound/` |
| Epochen Marketing | 17640378-a9eb-4190-a9f8-a1735fb4a1b0 | Marketing, Community, Store | Fabian | `marketing/` |
| Epochen Law | 53810324-d129-46dd-b69c-e39f9af5f72e | Recht, DSGVO, Jugendschutz | Fabian | `law/` |
| Epochen Tools | 68f87503-7495-4b3b-8067-6b905d710d47 | Tooling, Lizenzen, interne Skripte | New Bot | `tools/` |
| Epochen Balancing | c5a6ba38-290c-48ae-a836-226c34472696 | Unabhängige Balancing-Prüfung, Simulationen | New Bot (unabhängig) | `balancing/` |
| Epochen Producer | 30e57d1c-942f-42f1-baf8-39125b907844 | Projektleitung, Zeitplan, Blocker | New Bot | `producer/` |
| Epochen HR | 18cdeddf-9cd3-4287-9c01-7f734d0f80fe | Team, Rollen, Kapazität | New Bot / Fabian | `TEAM.md` |
| New Bot | 6e22f13d-9376-45c9-8d10-41352f9f926f | Koordination | Fabian | – |

Hinweise: Leads für Sound, Marketing, Law sind bisher nicht festgelegt (direkt Fabian).
| Epochen Götter | 51889260-5f32-4321-b0c9-d772328bc997 | Götter-System (sammelbar, Boni), aktiv ab ca. 17.10. | Game Designer | goetter/ |
| Epochen Spielertest | 72560ef2-5d8c-442a-89a3-fb4f47b72b5c | Simuliert Spielertypen, bewertet Spaß/Frust über 1 Tag, 1 Woche, 3 Monate | QA | qa/spielertest/ |
| Epochen Aufseher | 442bc9e1-7ebb-42f1-abb2-4de5b8a7b2d6 | Prozess- und Kostenwächter (Vorgabe Fabian 22.10.): überwacht Regeln und Abläufe (Maßplan zuerst, Reihenfolge Kritiker/QA, GUELTIG.md), Doppelbau, Selbstprüfung, Kosten und Nacharbeit (Budgets, Deckel); keine inhaltliche Qualitätsprüfung, keine Gates auf Farben oder Code | New Bot (unabhängig) | aufseher/ |
| Epochen Archiv | 5cf0ca62-e080-4d30-856d-a486c468d47a | Ordnung in team/art und Specs, Liste der gültigen Vorlagen (art/GUELTIG.md), Prüfung gegen Doppelbau, verschiebt nur | Producer | art/_alt/ |
| Epochen PvE | dfe31843-ef7d-42e2-8417-1617a301416e | PvE-Chef: alle PvE-Modi, Gesamtspielzeit (Gelegenheitsspieler ~15 Min), kein Grind | Game Designer | pve/ |
| Epochen Übersetzung EN | 68bdf34f-c075-4251-b80b-ca0475c2c2b2 | Lokalisierung Englisch, String-Tabellen, Glossar für alle Sprachen | Producer | lokalisierung/en/ |
| Epochen Gilden | a46932e9-c57e-4e2f-a323-3dc5e35983c5 | Gildenfunktionen: Halle, Chat, Ankündigungen, Rundmails, Community | Game Designer | gilden/ |
| Epochen Rechner | 37c040c6-3171-470d-976e-b98d41e9e522 | Wirtschafts-, Beschwörungs- und Balancing-Simulationen (Rechnungen über Codex) | Game Designer | rechner/ |
| Epochen Recherche | 059ae314-6a3d-4c24-9293-9fa2528cc1ec | Informationsbeschaffung und Marktvergleiche (über Codex/Gemini) | Producer | recherche/ |
| Epochen Lore & Geschichte | edca35cb-a784-4549-b84d-1644c24fdbac | Geschichtliche Glaubwürdigkeit je Epoche, Stimmigkeit der Fantasy-Twists, Lore-Bibel | Game Designer | lore/ |
| Epochen Kritiker | 9463301f-ad4d-4b73-a78c-008f60b4887a | Unabhängige Kritik aus Spielersicht (Bilder, UI, Gameplay, Story, Monetarisierung, Langzeitmotivation), max. 1 Bericht/Tag | New Bot (unabhängig) | kritik/ |
| Epochen Law Datenschutz | d8c2f1d8-070c-46e1-828a-a71267441bf3 | DSGVO, SDKs, Einwilligung, Data Safety | Law | law/datenschutz/ |
| Epochen Law Jugendschutz & Kauf | dc2eafa5-0500-4623-bbc0-491d327b6a94 | U18, USK/IARC, Lootbox, Verbraucherrecht | Law | law/jugendschutz-kauf/ |
| Epochen Law Gewerbe & Store | 5fd0df9a-4771-48a4-8798-c26ad7ed7c9d | Gewerbe, Steuer, Google Play, Impressum/AGB | Law | law/gewerbe-store/ |
| Epochen Law Moderation & DSA | 09415450-05be-464b-8682-9a3642da4ce6 | Moderation, DSA, Plattform- und UGC-Regeln | Law | law/moderation-dsa/ |
| Epochen Plattform Android | 721a4ccd-079e-46f0-8157-673e7e9bac49 | Android-Build, AAB/Signing, Play Billing, Play Console | Dev | dev/android/ |
| Epochen Plattform iOS | a311605f-7fd2-4efa-a9d7-cda1cacbdf01 | iOS-Port, Xcode/TestFlight, StoreKit, Apple-Pflichten | Dev | dev/ios/ |
