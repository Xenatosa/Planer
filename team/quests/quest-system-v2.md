# Epodarien – Quest-System v2
**Status: Entwurf für Fabian** · 23.10.2026 · Basis: Lore-Bibel (00–17), Storybuch Buch 1, Romanfassung v2 (Prolog, Kap. 1–3), Quest-System v1 (Zieltypen und Ökonomie bleiben gültig).

## 1. Was v2 ändert

v1 hatte fünf Typen (tutorial, main, side, daily, weekly) plus Achievements. v2 gliedert die erzählten Quests in **vier Arten mit klarer Rolle** und behält tutorial/daily/weekly/achievement unverändert bei:

| Typ | ID-Präfix | Rolle | Sichtbar | Quelle |
|---|---|---|---|---|
| **Hauptquest** | `Q_MAIN_Bx_` | Der Story-Faden. Folge der Romanfassung: jede Hauptquest erzählt einen Story-Beat und schaltet den nächsten frei. Linear, 1 aktiv. | 1 aktiv | Romanfassung + Storybuch |
| **Sidequest** | `Q_SIDE_Bx_` | Nebenstränge der Charaktere und des Dorflebens. Berühren die Story, widersprechen ihr nie. Optionale Ketten, bis 3 parallel. | bis 3 parallel | Romanfassung + Figuren |
| **Baukunst** | `Q_BAU_` | Bau-Quests an den Gebäude-Slots. Jede erzählt, warum dieses Gebäude gerade jetzt gebaut wird (Slot-Lore aus `05-gebaeude-slots.md`). | 1 pro neuem Slot, dann Stufen-Ziele | Slot-Tabelle |
| **Helden-Quest** | `Q_HERO_` | Bindung an einen Helden: Herkunft, Charaktermoment, Freischaltung. 1 Kette pro Held. | nach Helden-Freischaltung | Heldenkompendium `04-helden.md` |

Tutorial, Tages-, Wochenquests und Erfolge laufen wie in v1 weiter — sie sind die mechanische Schicht; v2 ist die erzählte Schicht.

## 2. Prequest-Regeln

- Jede Quest hat **maximal einen Prequest** (Vorgänger). Ketten, keine Bäume — sonst verliert der Spieler den Faden.
- Hauptquests additionally verlangen das zugehörige Kampagnen-Ziel, wenn der Beat einen Boss/Kampagnenabschnitt erzählt (Zustandsziel `campaign_cleared`/`campaign_stars`).
- Sidequests hängen immer an **einer** Hauptquest oder Baukunst-Quest als Prequest, nie an anderen Sidequests über Ebene 3 hinaus (Ketten kurz halten).
- Helden-Quests werden durch Freischaltung des Helden (Beschwörung oder Story-Moment) aktiviert; die Kette beginnt mit der Debüt-Quest.
- Eine Quest mit Prequest erscheint erst, wenn der Prequest **abgeholt** (nicht nur erfüllt) ist — Belohnungsmoment bleibt.

## 3. Aufgaben (Zieltypen)

Es gelten die v1-Zieltypen unverändert (siehe quest-system-v1.md §2). Neue Typen für die erzählte Schicht:

| ziel_typ | ziel_parameter | ziel_menge | Verwendung |
|---|---|---|---|
| `story_seen` | story_id (z. B. `prolog_v2`, `b1_k3`) | 1 | Zwischensequenz/Roman-Kapitel gesehen |
| `nights_survived` | no_hunger / any | Nächte | Winterphasen ohne Hunger (v1 `winter_survived`, hier verallgemeinert) |
| `visit_landmark` | landmark_id | 1 | Stelle auf der Weltkarte anlaufen (Felskante, Westfeld, Asche-Fels) |
| `read_marker` | marker_id | 1 | Asche-Zeichen lesen/interagieren (an Talas Schrift angelehnt) |
| `hero_bond_level` | hero_id | Stufe | Bindungsstufe des Helden |

Alle übrigen Aufgaben nutzen bestehende Typen: `building_level`, `building_upgrade`, `campaign_cleared`, `campaign_stars`, `train_units`, `collect_resource`, `spend_resource`, `formation_*`, `use_ultimate`, `army_pop` usw.

## 4. Belohnungsrichtlinien (übernimmt v1)

- Hauptquests: Heldenerfahrung, Kristalle (klein), Tickets — **bewusst wenig Baustoff** (v1 §3).
- Sidequests: Echosplitter, kleine Ressourcen, Titel an markanten Stellen. Keine Kristalle in Sidequests (f2p_income bleibt unangetastet).
- Baukunst: Baustoff passend zum Slot + ein Mal ein Ticket (nur bei Slot-Fertigstellung, nicht bei Stufen).
- Helden-Quests: Heldenerfahrung groß, Bindungspunkte, bei Kettenabschluss einmalig Kristalle (Höhe: [Annahme], Config).
- Abholen immer manuell per Tipp.

## 5. Queststruktur (Schema jeder Quest im Doc)

```
### Q_TYP_Bx_nnn „Titel"
- Prequest: …
- Aufgabe: ziel_typ | ziel_parameter | ziel_menge
- Belohnung: typ;typ / menge;menge
- Text: <Questtext im Roman-Ton>
- Hinweis (optional): <Spielerhinweis, nüchtern>
```

## 6. Ton der Questtexte

Der Roman (v2-Fassung) ist nüchtern, knapp, ohne Pathos. Die Questtexte folgen ihm:

- Figuren sprechen nur, wenn sie etwas Entscheidendes sagen (Brakka zählt, Nara sagt wenig, Kiko beobachtet, Tala stellt Fragen, Ruka redet mit dem Wolf).
- Keine Erklärungen durch den Erzähler, die die Figuren nicht kennen können (Lore-Regel aus der Kritik: zeigen statt erklären).
- Jeder Text nennt den Beat aus der Romanfassung beim Namen (z. B. die Schale, die drei Gestalten, Eisfangs Kristalle).
- DE/EN: Texte hier sind DE-Kanon; EN folgt über `ui_strings.csv`-Workflow bei der Umsetzung.

## 7. Umsetzung später

- CSVs auf das v1-Schema mappen: `quest_config.json` bekommt pro Typ eine Liste; neue Zieltypen in `validate_quests.py` ergänzen.
- `story_seen`/`visit_landmark`/`read_marker` brauchen Zähler im Spiel (serverseitig, wie alle Zähler — Anti-Cheat v1 §2).
- Prequest-Ketten als einfaches `prequest_id`-Feld; Zyklen werden durch die Kette ausgeschlossen.
- Umfang Buch 1: 20 Haupt + 12 Side + 16 Baukunst (9 Einleitungen + 9 Ausbau, Feuerstelle/Reisig doppelt gezählt in der Summe) + 8 Helden = **56 Quests** (siehe `quests-buch1-v2.md`).
- **Fabian-Vorgaben (23.10.2026):** Baukunst deckt Neubau UND Ausbau (Stufen-Quests mit eigenem Story-Text) ab. Hauptquest nicht zu kurz: 20 Quests, davon 14 mit Kampfauftrag (Kampfsystem v2 aktiv: Slots, Tokens, General-Button, Sterne-Ziele). Ergänzungen über der Lore sind markiert **[Ergänzung]** und dürfen der Lore nicht widersprechen.

## 8. Offene Punkte für Fabian

1. „Baukunst" als Name — gemeint ist die Bau-/Slot-Questreihe. Alternativ: „Baukunst" nur für Schmuck-/Ausbau-Quests (Deko), Bau-Quests weiterhin tutorial? [Annahme hier: Baukunst = Bau-Quests an den Slots]
2. Helden-Quests: Freischaltung über Beschwörung oder über Story-Moment erzwingen? Roman legt nahe: Ruka/Mira kommen über die Story, Brakka/Nara sind von Anfang an da.
3. Sidequest-Parallelität: 3 gleichzeitig (v1) oder nur 1 pro Charakterkette?
