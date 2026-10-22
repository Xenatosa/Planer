> ⛔ HUD v5.7 ist gestrichen (Fabian 22.10.2026), gültig ist D2 Obsidian & Glut + Dock A braun. Gesamtes HUD v5 (inkl. Icons `hud_c_ico_*`, `HudV5NumberFormat`) ist gestrichen; Dorf-HUD und Icons werden neu in D2 erstellt. Vorlage: `team/art/GUELTIG.md`.

# U18-Shop-Regel (Finanzen, 17.10.2026; Law Jugendschutz & Kauf: Grün mit Auflagen)
Ersetzt „U18 ganz ohne Shop“ aus HUD v5.7.

## Shop und Limit
- U18 hat einen Shop. Das harte Limit von 50 €/Monat wird serverseitig geprüft (PR #67, PR #136 passt).
- Für U18 gesperrt:
  - Chronisten-Abo
  - Ewige Chronik (immer gesperrt, `minorBlocked: always`, PR #73)
  - Event-Token-Pakete
  - Kauf-Treue und Kauf-Meilensteine
  - Helden-Startpaket mit Fragmenten

## Anzeige
- Keine Countdowns, keine Pushs, keine direkten Kaufaufforderungen (kein „Kauf jetzt!“).
- Die Anzeige „diesen Monat ausgegeben / Rest“ ist sichtbar.
- Ist das Limit erreicht, erscheint ein Sperrdialog ohne Ersatzangebot.
- Eine Erstattung gibt das Monatslimit nicht wieder frei.

## Beschwörung für U18
- Erlaubt, mit Länder-Whitelist (BE nie, AT/NL bleiben Anwaltspunkt).
- Chancen je Seltenheit und je Held sowie die Pity sind vor jedem Zug sichtbar. Die Pity verfällt nie.
- Kein Kaufhinweis „noch X Züge bis Pity“.
- Kristallkäufe zählen ins Limit.
- Spezial-Banner für U18 nur mit verdienten Kristallen (`special_banner_u18_earned_only` = true).

## Planung
- Erstattungen nach §108 BGB werden eingeplant. Annahme: 5 % des U18-Umsatzes.
- Tutorial-Abschluss: ein einmaliges Starterangebot, ohne Pop-up, als Karte im Abschluss-Screen. Für U18 ohne Kaufaufforderungstext.

## Antworten an Art UI (17.10., 22:45)
1. `starter_hero_pack` steht in `config_kaufanreize_v2.json` jetzt auf `u18_visible: false`.
2. Auf die Starterkarte kommt `starter_first_step` (0,99 €), für alle Spieler. Das ist die niedrigste Einstiegshürde. `starter_1` gibt es in der Config nicht. Gemeint ist wohl `starter_server` (2,99 €), und das bleibt im Reiter.
3. Reiter „Angebote“ für U18: Er bleibt, unauffällig und nur im Shop gelistet.
   - Inhalt: nur Starterangebote mit `u18_visible: true` (`starter_first_step`, `starter_server`).
   - Ohne Hervorhebung, ohne Banner und ohne „Neu“-Punkt. Leer heißt ausgeblendet.
   - `minor_ads_and_offers = off` gilt für Werbung, Banner und Pushs außerhalb des Shops.
   - Die Angleichung von GDD 19.x ist beim Game Designer angefragt.
4. Das Plus an den Kristallen für U18 bleibt aus, bis Law antwortet. Gewünscht ist: Es öffnet den Kristall-Reiter, ohne Text und ohne Animation.
5. Das feste Datum für den Limit-Reset ist bei Law zur Bestätigung angefragt. Bis dahin bleibt es drin, weil es kein laufender Zähler ist.

## Law-Freigabe zu 4 und 5 (17.10., 22:32): beides Grün
- Feste Datumsanzeige, neutral formuliert: „Limit wird am 1.11. zurückgesetzt (Serverzeit)“. Keine Formulierungen wie „Bald wieder kaufen!“.
- Das Plus an den Kristallen ist für U18 frei, ohne Text, Animation oder Badge, ohne roten Punkt und ohne Pulsieren.
- Auflage zum Reiter „Angebote“:
  - `starter_first_step` und `starter_server` werden für U18 ohne Ablaufzeit, ohne Countdown und ohne „nur für kurze Zeit“ angezeigt.
  - Keine Pop-ups, die Starterpakete einblenden.
  - Beide zählen ins 50-€-Limit.

## Kritiker S1/S2 (17.10.): Finanzen einverstanden
- S1: Kristallpakete bekommen im ganzen Shop keine Seltenheits-Badges (R/SR/SSR). Erwachsene sehen stattdessen den Hinweis „Bester Wert“ am Paket mit den meisten Kristallen pro Euro, U18 sieht ihn nicht.
- S2: Für U18 werden Pakete ausgeblendet, die über dem Restlimit des Monats liegen, mindestens aber alle über 50 €.
