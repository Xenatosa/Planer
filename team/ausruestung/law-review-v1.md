# Law-Review v1 – Item- & Ausrüstungssystem (Epodarien)
Stand 14.10.2026 · Basis: `ausruestung/item_system_v1.md`, `ausruestung_konzept_v1.md`, `items.csv`, `equipment.csv`, `artifacts.csv`, `cosmetic_products_vorschlag.csv`; `law/Rechts-Checkliste_Epodarien.md`, `law/Ampel-Review_GDD_v0.5.md`, `ranking/law-review-v1.md`; `gdd/events.csv`, `event_scoring.csv`, `iap_products.csv`, `validate.py`.

> **Keine Rechtsberatung.** Interne Ersteinschätzung für die Planung. Normen und Leitlinien wurden für dieses Review nicht neu im Wortlaut abgerufen; alle Fundstellen gelten als **[Stand prüfen]**, sofern nicht in den Vor-Reviews als geprüft markiert. Vor Soft Launch anwaltlich bestätigen lassen.

## 0. Verifikation „kein Zufall, keine Kauf-Truhen mit Zufall“
| Prüfung | Ergebnis |
|---|---|
| `items.csv` `random_content` | überall `no`, außer `itm_ticket_summon` = `yes(on use)` (Zufall erst am Banner, Chancen dort) – konsistent mit Konzept |
| Truhen | `itm_chest_campaign_fixed` (fester, vorab angezeigter Inhalt), `itm_chest_choice` (Wahl) – kein Zufall, nicht kaufbar |
| Ausrüstung/Artefakte | feste Werte, keine Drop-Chancen, `tradeable=no`, Artefakte `purchasable=no`; keine separate Schmiedewährung; Gear-Kosten nur Gold/Stein/Holz |
| Kaufbare Items | `itm_karawane_box` (feste Ressourcenmenge), Skins, Wahl-Fragment über `starter_2` – alle ohne Zufall; `iap_products.csv` durchgehend `random_content=no`; Gear-Skin-Vorschläge ohne Zufall, power_bonus 0 |
| validate.py | läuft, **Exit-Code 1** mit Meldung „Shop as_art_wolf_fang“ (Artefakt-Quelle Arena-Shop nicht in `arena_shop.csv` gefunden) – Datenfehler, kein Rechtsproblem, aber vor Freigabe beheben |
**Fazit:** Aussage des Autors bestätigt. Einzige Zufallsmechanik bleibt die Beschwörung (inkl. Tickets).

## Frage 1 – Ausrüstung als feste Belohnung für Event-Meilensteine — 🟢 grün (mit Auflagen)
**Befund:** Feste, vorab sichtbare Belohnungen sind kein „glücksspielähnlicher Mechanismus“ und keine „zufälligen Objekte“ (§ 10b Abs. 3 JuSchG); Lootbox-Bezug (BE/NL) entfällt. In den Daten erhält nur `art_e1_ancestor_drum` eine Event-Quelle: **Mammutjagd-Gemeinschaftsmeilenstein 100 %**, Versuche nicht kaufbar, für alle gleich → kein Kaufanreiz. Risiko entsteht erst, wenn Gear an **kaufbar beschleunigte Meilensteine** gekoppelt wird: Im Stammeswettstreit zählen gekaufte Ahnenzeichen (bis 1.500 voll, dann ×0,6) und Karawanen-Ressourcen (Tagesdeckel) zu Punkten; Meilensteine 2k–30k sind damit teilweise kaufbar erreichbar. Gear dort wäre mittelbar gekaufte Spielstärke → Widerspruch zur eigenen Hard Rule „Gear nie indirekt gegen Geld“, Kaufappell-/Pay-to-win-Thema (§ 10b Abs. 3 „Kauffunktionen“, § 5/5a UWG bei Aussagen „kein Pay-to-win“).
**Empfehlungen:**
1. Gear/Artefakte nur aus Meilensteinen, deren Fortschritt **nicht** durch Käufe beschleunigt wird (Mammutjagd, Baumeister relativ, Aufgaben) – nicht aus Stammeswettstreit-Meilensteinen und nie aus Ranglisten-Platzbelohnungen (Konzept sieht das bereits vor; als Hard Rule in validate.py prüfen).
2. Falls doch an Stammeswettstreit: nur über Punkte aus Aufgaben/Ahnenprüfung („free/any ohne Kaufbezug“), nicht aus `spend_mark_paid`/Ressourcen.
3. Meilenstein-Belohnung vorab im Event sichtbar, kein Shop-Link auf Event-/Ergebnis-Screens (GDD Kap. 15).
4. Artefakt im Arena-Shop (Wettbewerbswährung, nie kaufbar): vertretbar, Wochenlimit beibehalten.
**Quellen:** § 10b JuSchG https://www.gesetze-im-internet.de/juschg/__10b.html · UWG Anhang Nr. 28 https://www.gesetze-im-internet.de/uwg_2004/anhang.html · § 5a UWG https://www.gesetze-im-internet.de/uwg_2004/__5a.html [Stand prüfen]

## Frage 2 – Verfall von Event-Items 3 Tage nach Event-Ende mit Umtausch — 🟢 verdiente / 🔴 gekaufte (derzeit nicht vorgesehen)
**Befund (Daten):** Nur Kategorie `event` verfällt (`itm_event_token_mammut`, `itm_event_token_baumeister`), beide `obtainable_purchase=no`. Ahnenzeichen (inkl. gekaufter) verfallen nicht. Umtauschwert Mammut-Trophäe: 1 Trophäe = 1 Produktionsstunde Nahrung; Rest beim Verfall in Nahrungskisten.
- **Verdiente Items:** Event-gebundene, kostenlos verdiente Marken mit Verfall sind üblich und bei klarer Regel vertretbar. Der automatische Umtausch (kein Totalverlust) ist verbraucherfreundlich. AGB-Kontrolle (§ 307 BGB, Transparenzgebot Abs. 1 S. 2) betrifft vor allem Gegenleistungen, für die bezahlt wurde; trotzdem Regel klar in Spiel/FAQ/AGB.
- **Gekaufte Items:** Verfall gekaufter Inhalte ist das Hochrisiko-Feld: CPC-Grundsätze (21.03.2025) verlangen Transparenz über Wert/Bedingungen virtueller Währungen und keine Klauseln, die gekaufte Inhalte einseitig entwerten; eine Verfallsklausel für Bezahltes wäre AGB-rechtlich (§ 307 BGB, unangemessene Benachteiligung) angreifbar. Die eigene Regel „gekaufte Inhalte verfallen nie“ ist richtig – beibehalten. Auch **mittelbar** gekaufte Event-Items (z. B. per Kristallen/Paket erhaltene Event-Marken) zählen als gekauft.
**Auflagen:**
1. Hard Rule in validate.py: `expires=yes` ⇒ `obtainable_purchase=no` und keine Quelle aus IAP/Kristallen.
2. Hinweis auf Verfall + Umtauschkurs **vor** Erhalt/Einsatz sichtbar (Event-Info, Item-Tooltip), Countdown nur im Event, ohne Shop-Link (wie geplant).
3. Umtausch fair und fest: Kurs vorab veröffentlichen, nicht nachträglich verschlechtern; Wert orientiert am Event-Shop-Wert (Vorschlag: ≥ Durchschnittswert pro Marke im Event-Shop, nicht nur symbolisch). Mammut-Kurs festlegen.
4. Sollte je ein Kaufprodukt Event-Marken enthalten: Marken nicht verfallen lassen oder Restwert in gleichwertige dauerhafte Währung + Hinweis vor Kauf (Preis in €, „verfällt am …“) – dann Law-Review vorher.
**Quellen:** CPC Key Principles https://commission.europa.eu/document/download/8af13e88-6540-436c-b137-9853e7fe866a_en?filename=Key%2520principles%2520on%2520in-game%2520virtual%2520currencies.pdf · § 307 BGB https://www.gesetze-im-internet.de/bgb/__307.html [Stand prüfen]

## Frage 3 – Ablauf eines künftigen Reviews für eine Zufallstruhe (Checkliste)
Vor **Implementierung** (nicht erst vor Release) an Law vorlegen; ohne Freigabe kein Merge.
1. **Spezifikation einreichen:** Inhalt, Wahrscheinlichkeiten je Item (Summe 100 %), Quelle (verdient/kaufbar/Paket/Ticket), Preis in € und Währung, Pity/Garantie, Limits, Länder, Zielgruppe.
2. **Nur verdiente Währung?** Bevorzugt ja (keine kaufbare Zufallstruhe, Empfehlung v1). Kaufbar oder über gekaufte Währung = Lootbox → volle Prüfung Punkte 3–9.
3. **Google Play:** Wahrscheinlichkeiten **vor dem Kauf** offenlegen (Play-Richtlinie Zahlungen/Lootboxen) – am Kauf-/Öffnen-Knopf, auch bei kostenlosen Truhen empfohlen.
4. **Belgien:** Lootbox mit Geldbezug gesperrt (Länder-Flag BE aus, Store-Land serverseitig); Soft Launch ohne BE.
5. **Niederlande:** Lage beobachten (Raad van State 2022, ACM-Leitlinien, Verbotsinitiative) [Stand prüfen]; Flag vorbereitet.
6. **USK/IARC:** Fragebogen ehrlich, Deskriptor „In-Game-Käufe (+ zufällige Objekte)“; Auswirkung auf Alterskennzeichen nach § 10b Abs. 3 JuSchG bewerten.
7. **Pity/Garantie:** offenlegen, serverseitig, nicht resetbar durch Bannerwechsel ohne Hinweis; keine „nur noch X bis…“-Kaufbuttons.
8. **Minderjährige:** keine Kaufappelle (UWG Anhang Nr. 28), Ausgabenlimit u18 greift, keine Pushs mit Shop-Link, ggf. Truhe für u18 ohne Kaufoption.
9. **Glücksspielrecht:** kein Echtgeld-/Sachgewinn, kein Handel/Auszahlung (GlüStV) – sonst Stopp.
10. **Dokumentation:** Raten versioniert (`odds_disclosed_required`, `random_content`), Ziehungen geloggt, Changelog, Screenshots der Anzeige, validate.py-Check, Entscheidungseintrag in ENTSCHEIDUNGEN.
11. **Ergebnis:** Ampel + Auflagen → Fabian entscheidet → Umsetzung → Abnahme-Check durch Law vor Release.
**Quellen:** Play-Richtlinie https://support.google.com/googleplay/android-developer/answer/9858738?hl=de [Stand prüfen] · Kansspelcommissie https://gamingcommission.be/sites/default/files/2021-08/onderzoeksrapport-loot-boxen-Engels-publicatie.pdf · Raad van State https://uitspraken.rechtspraak.nl/details?id=ECLI%3ANL%3ARVS%3A2022%3A690 · USK/IARC https://usk.de/fuer-unternehmen/spiele-und-apps-pruefen-lassen/spiele-und-apps-im-iarc-system/ · § 10b JuSchG (s. o.) · GlüStV https://gluecksspiel-behoerde.de/de/rechtliche-grundlagen [Stand prüfen]

## Offene Punkte
- Umtauschkurs Mammut-Trophäe festlegen.
- validate.py-Fehler „Shop as_art_wolf_fang“ beheben.
- Hard Rules „Verfall nur unkaufbar“ und „kein Gear aus kaufbar beschleunigten Meilensteinen“ in validate.py ergänzen.
