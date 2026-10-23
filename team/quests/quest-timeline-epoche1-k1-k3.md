# Epodarien – Spiel-Timeline Epoche 1, Kapitel 1–3 (v2.1)
**Status: Entwurf für Fabian** · 23.10.2026 · Reihenfolge, wie ein Spieler die 86 Quests im Spiel abschließt. Basis: `quests-epoche1-k1-k3.md`.

**v2.1 — Umgesetzte Kritik (23.10.2026, Epochen Kritiker, 5/10). v2.2 — Recheck 1 (7/10). v2.3 — Recheck 2 (8/10). v2.4 — Recheck 3 (9/10). v2.5 — Recheck 4 (9/10 → Ziel 10/10):**

**v2.5-Recheck-Fixes:** S11 Reihenfolge der 12 Tut-Schritte korrekt aufgelistet (009/018/020 fehlen wegen Streichung, Nummerierung 1–12 explizit). S12 Spiegel bereitgestellt unter docs/team/kritik/spiegel/quest-timeline-epoche1-k1-k3.md mit Ziel-Pfad-Hinweis für handygame-plan.

**v2.4-Recheck-Fixes:** S8 vollständiger maschinenlesbarer Annex (alle 86 IDs mit prequest, Pflicht?, Belohnung, Parallel-Slot, Position; Lücken 55/77 dokumentiert). S11 Tut-Mathe korrekt: 20 − 5 Merges − 3 Streichungen = 12, Reihenfolge benannt. S12 Spiegel nach handygame-plan: Datei liegt hier bereit; Mirror-Verantwortung laut Kritik-Konvention beim Kritiker.

**v2.3-Recheck-Fixes:** M6 Regeln-Zeile an Wahrheitstabelle angeglichen (Mini-Bosse 25+40 = Ticket, 5/10/20/35 = Kristalle). M10 Q_BAU_005 hat eigene Zeile (70a, Jagdplatz-Einleitung). S4 Ticket-Mathematik (6 Tickets bis K3-Ende, Tabelle) + Soft-Gates-Block. S8 Pflicht?/Parallel-Slot-Legende in den Regeln. S11 Tut-Streichliste konkret (12 Schritte).

**v2.2-Recheck-Fixes:**

**v2.2-Recheck-Fixes:** M1 vervollständigt (alle Bau- und Asch-Ketten mit Hinweis, 21 Markierungen gesamt). M6 Wahrheitstabelle korrigiert (Tickets nur Stufen 25+40, K1-Minis Kristalle). M7 [Annahme]-Restzeile entfernt, Mapping verbindlich, Migrationsaufgabe CSVs/GDD 30→45 benannt. M9 Basis-Spec (quests-epoche1-k1-k3.md) angeglichen: K2_025 heißt dort jetzt Die Weißgewandete. M10 Q_BAU_006 hat eigene Position (70b), Lücke 77 markiert. S1 Sitzungsplan ergänzt. S5 Basis-Spec Olm 3→2.

**v2.1-Fixes (Recheck 0):**
- **M1** Ketten mit „bewusste Reihenfolge Fabian; Basis-Prequest weich“ gekennzeichnet (Spalte Hinweis).
- **M6** Belohnungs-Wahrheitstabelle ergänzt — Timeline folgt der Basis.
- **M7** 45 Stufen sind verbindlich (keine [Annahme] mehr); Mapping k1_s01→e1_camp_01 … k3_s45→e1_camp_45. Die alte 30er-Kampagne ist überholt (Migrationsaufgabe: CSVs/GDD auf 45 nachziehen).
- **M8** Tutorial-Schnitt definiert: Q_TUT_001–020 (~10–12 Schritte nach Kürzung, überspringbar), **keine doppelte Mission 1** — Stufe 1 (k1_s01) startet NACH Tutorial-Abschluss.
- **M9** Titel-Kollision gelöst: Mini-Boss K2_025 heißt jetzt **„Die Weißgewandete“**; Brakka behält „Die, die zählt“.
- **M10** ID-Checkliste aller 86 Quests am Dateiende (jede ID genau eine Position; Meta-Zeilen klar markiert).
- **M11** Kein Login-FOMO: Kiko-1 wird zu **Spielzeit-Ziel** (3× 10-min-Sitzungen, optional, nur Kosmetik) — kein Gate.
- **M12** Koop-Block: K1–K3 Hauptstory bewusst koop-frei; Kooperation kommt über Gilde (Zeichenfels, E2), Events und Nebenquests.
- **S1** Sitzungsplan pro Phase (nach jedem Mini-/Endboss ein Dorf-/Helden-Moment).
- **S2** Kiko „50× Feuer“ → **10× Feuer pflegen**.
- **S3** „Sidequests leeren“ gestrichen — offene Sidequests bleiben freiwillig offen.
- **S4** F2P-Block: K1–K3 100 % F2P spielbar; IAP nur Komfort, kein Content-Gate.
- **S5** Olm-Helden-Quest: Formationstypen = **2** (eine Zahl).
- **S6** Helden-Tabelle mit Debüt + Korrekturen (Olm kein Boss, Terwish nicht in E1, Ruka nicht im Tutorial).
- **S7** „Kristalle im Fell“ = Äther-Kristalle (Story), NICHT Zeitkristalle (Shop) — Begriffsblock ergänzt.
- **S8** Tabellenspalten: quest_id | prequest | Pflicht? | Belohnung | Parallel-Slot/Hinweis.
- **S9** Parallel-Sides „bis 3“; bei Überlauf wird die älteste nicht gestartete ersetzt, läuft später weiter.
- **S10** Next-Hooks nach Abschluss (K3 → Epoche-2-Ausblick).
- **S11** Tutorial auf max. 10–12 Schritte kürzen (Tut-CSV hat 20 — Migrationsaufgabe).
- **S12** Spiegel nach handygame-plan: bereitgestellt unter `docs/team/kritik/spiegel/quest-timeline-epoche1-k1-k3.md` (Kopie 1:1) mit Ziel-Pfad-Hinweis `/workspace/handygame-plan/team/quests/quest-timeline-epoche1-k1-k3.md` — der Workspace selbst liegt außerhalb dieses Repos und wird beim nächsten Sync des Kritikers übernommen.

**Legende:** ⚔ = Kampf (Kampagnenstufe) · 🔨 = Baukunst · ⭐ = Sidequest · 🧑 = Helden-Quest · 📖 = Story-Moment

---

## Phase 1 – Ankommen (Tutorial → Stufe 5)

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 0 | Tutorial Q_TUT_001–020 (auf 10–12 Schritte kürzen, überspringbar) | Tutorial | Bau-Basics, erster Kampf, erste Beschwörung; **keine doppelte Mission 1** — danach startet k1_s01 |
| 1 | 🔨 **Winzige Feuerstelle** (Q_BAU_001) | Bau | Feuerstelle bauen (St. 1)  · *Hinweis: bewusste Reihenfolge Fabian; Slot-Freischaltung ist Gate, kein Story-Prequest* |
| 2 | 🔨 **Reisig-Halde** (Q_BAU_002) | Bau | Sammler bauen  · *Hinweis: bewusste Reihenfolge Fabian; Slot-Freischaltung ist Gate, kein Story-Prequest* |
| 3 | ⚔ **Q_MAIN_K1_001** Rauch über dem Tal | Haupt | Stufe 1 gewinnen |
| 4 | ⭐ **Der Mann, der sich nicht ablösen lässt** (Kiko 1, Q_SIDE_B1_101) | Side | 3× 10-min-Sitzungen (Spielzeit, optional, nur Kosmetik — kein Gate) |
| 5 | 🧑 **Die, die zählt** (Brakka) | Held | 2 Nächte ohne Hunger |
| 6 | ⚔ **Q_MAIN_K1_002** Hungrige Nachbarn | Haupt | Stufe 2 |
| 7 | ⚔ **Q_MAIN_K1_003** Die Jäger vom Fluss | Haupt | Stufe 3 |
| 8 | ⭐ **Nasse Felle** (Bako 1, Q_SIDE_B1_111) | Side | 300 Holz sammeln |
| 9 | 🧑 **Die Reihe hält** (Olm) | Held | 2 Formationstypen gewinnen *(Basis-Spec angeglichen: 2, nicht 3)* |
| 10 | ⚔ **Q_MAIN_K1_004** Fährten im Neuschnee | Haupt | Stufe 4 |
| 11 | ⚔ **Q_MAIN_K1_005** ⚠ Schattenpfote *(Mini-Boss)* | Haupt | Stufe 5 |

---

## Phase 2 – Erste Schrift (Stufe 6–10)

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 12 | ⚔ **Q_MAIN_K1_006** Der Kreis am Fels | Haupt | Stufe 6 |
| 13 | 🔨 **Der Zeichenfels** (Q_BAU_004) | Bau | Zeichenfels bauen (schaltet frei nach K1_006)  · *Hinweis: bewusste Reihenfolge Fabian; erscheint mit K1_006, Prequest weich* |
| 14 | ⭐ **Elf Zeichen** (Tala 1, Q_SIDE_B1_121) | Side | 5 Marker · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (K1_006) gleichzeitig* |
| 15 | ⚔ **Q_MAIN_K1_007** Schnee-Brecher | Haupt | Stufe 7 |
| 16 | ⚔ **Q_MAIN_K1_008** Nächte des Diebstahls | Haupt | Stufe 8 |
| 17 | ⭐ **Alle Richtungen, gleich lange** (Gorm 1, Q_SIDE_B1_141) | Side | 5 Kämpfe · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (K1_008) weich* |
| 18 | ⭐ **Der gebrochene Schaft** (Hulf 1, Q_SIDE_B1_131) | Side | 5 Speerträger · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (K1_003) weich* |
| 19 | ⚔ **Q_MAIN_K1_009** Am Eisbach | Haupt | Stufe 9 |
| 20 | 🔨 **Kuhlen für drei** (Q_BAU_013, Wohnraum St. 2) | Bau | Ausbau  · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Q_BAU_003) weich* |
| 21 | ⚔ **Q_MAIN_K1_010** ⚠ Die Meute *(Mini-Boss)* | Haupt | Stufe 10 |

---

## Phase 3 – Knirsch (Stufe 11–15) + K1-Abschluss

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 22 | ⚔ Q_MAIN_K1_011 Kalte Fährten | Haupt | Stufe 11 |
| 23 | ⚔ Q_MAIN_K1_012 Eisbach-Furt | Haupt | Stufe 12 |
| 24 | ⚔ Q_MAIN_K1_013 Der Asche-Fels | Haupt | Stufe 13 |
| 25 | ⭐ **Drei Windsteine** (Kiko 3, Q_SIDE_B1_103) | Side | Feuerstelle St. 2 · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Kiko-2) weich* |
| 26 | 🔨 **Feuer, das heller ruft** (Q_BAU_011) | Bau | Feuerstelle St. 2  · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Q_BAU_001) weich* |
| 27 | ⚔ Q_MAIN_K1_014 Nacht des Bären | Haupt | Stufe 14 |
| 28 | ⚔ **Q_MAIN_K1_015** ⚠⚠ **Der Lehrboss (Knirsch)** | Haupt | Stufe 15 = **Kapitel-1-Endboss** |
| 29 | 📖 Story: Kapitel-1-Abschluss (Brakka zählt wieder) | — | automatisch |
| 30 | ⭐ **Der Pfosten hält** (Gorm 3, Q_SIDE_B1_143) | Side | Kampf mit ★2 · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Gorm-2, K3_033) weich* |
| 31 | 🔨 **Schlafkuhlen** (Q_BAU_003) | Bau | Wohnraum bauen (E2-Freischaltung)  · *Hinweis: bewusste Reihenfolge Fabian; E2-Gate, Story-Prequest weich* |

---

## Phase 4 – Naras Paste (Stufe 16–20)

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 32 | ⚔ **Q_MAIN_K2_016** Naras Paste | Haupt | Stufe 16 |
| 33 | 🧑 **Zweimal kam etwas** (Nara) | Held | Bindung 2 |
| 34 | ⚔ **Q_MAIN_K2_017** Der Handabdruck | Haupt | Stufe 17 |
| 35 | ⭐ **Eine Kuhle zur Probe** (Bako 2, Q_SIDE_B1_112) | Side | Wohnraum ausbauen |
| 36 | ⚔ **Q_MAIN_K2_018** Hasenspur | Haupt | Stufe 18 |
| 37 | ⚔ **Q_MAIN_K2_019** Der beobachtete Rückweg | Haupt | Stufe 19 |
| 38 | ⭐ **Kikos Warnung** (Tala 2/Kiko, Q_SIDE_B1_122) | Side | Gefahr-Zeichen lesen |
| 39 | ⚔ **Q_MAIN_K2_020** ⚠ Der wartende Bock *(Mini-Boss)* | Haupt | Stufe 20 |

---

## Phase 5 – Die drei vom Kamm (Stufe 21–25)

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 40 | ⚔ **Q_MAIN_K2_021** Drei am Kamm | Haupt | Stufe 21 |
| 41 | 🧑 **Die Stelle unter dem Westfeld** (Tala) | Held | Landmark besuchen |
| 42 | ⚔ **Q_MAIN_K2_022** Zeichen im Schnee | Haupt | Stufe 22 |
| 43 | ⭐ **Ein fremder Kreis** (Tala 3, Q_SIDE_B1_123) | Side | Zeichenfels besuchen |
| 44 | 🔨 **Zeichen, die antworten** (Q_BAU_014) | Bau | Zeichenfels St. 2  · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Q_BAU_004) weich* |
| 45 | ⚔ Q_MAIN_K2_023 Der gemusterte Weg | Haupt | Stufe 23 |
| 46 | ⚔ Q_MAIN_K2_024 Kalter Vorstoß | Haupt | Stufe 24 |
| 47 | ⚔ **Q_MAIN_K2_025** ⚠ Die Weißgewandete *(Mini-Boss)* | Haupt | Stufe 25 |

---

## Phase 6 – Vask (Stufe 26–30) + K2-Abschluss

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 48 | ⚔ Q_MAIN_K2_026 Nebel am Südhang | Haupt | Stufe 26 |
| 49 | ⭐ **Der Rauch legt sich** (Kiko 2, Q_SIDE_B1_102) | Side | 5 Nächte |
| 50 | ⚔ Q_MAIN_K2_027 Gelöschte Glut | Haupt | Stufe 27 |
| 51 | 🧑 **Feuerwache** (Kiko) | Held | 10× Feuer pflegen |
| 52 | ⚔ Q_MAIN_K2_028 Die Spur des Stillen | Haupt | Stufe 28 |
| 53 | ⚔ Q_MAIN_K2_029 An der Felskante | Haupt | Stufe 29 |
| 54 | ⚔ **Q_MAIN_K2_030** ⚠⚠ **Der Stumme (Vask)** | Haupt | Stufe 30 = **Kapitel-2-Endboss** |
| 55 | 📖 Story: Vask lässt fremde Zeichen zurück | — | automatisch |
| 56 | ⭐ **Drei übrig** (Bako 3, Q_SIDE_B1_113) | Side | Wohnraum St. 3 · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Bako-2) weich* |
| 57 | 🔨 **Die Halde trägt** (Q_BAU_012) | Bau | Sammler St. 2  · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Q_BAU_002) weich* |
| 58 | ⭐ **Wieder eingesetzt** (Hulf 3, Q_SIDE_B1_133) | Side | Jagdplatz · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Hulf-2, K3_034) weich* |

---

## Phase 7 – Das Jaulen (Stufe 31–35)

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 59 | ⚔ **Q_MAIN_K3_031** Das erste Jaulen | Haupt | Stufe 31 |
| 60 | ⚔ **Q_MAIN_K3_032** Verlorene Beutel | Haupt | Stufe 32 |
| 61 | ⚔ **Q_MAIN_K3_033** Die durchgebissene Leine | Haupt | Stufe 33 |
| 62 | ⭐ **Die falsche Richtung** (Gorm 2, Q_SIDE_B1_142) | Side | Formation anführen |
| 63 | ⚔ **Q_MAIN_K3_034** Knochenspitzen | Haupt | Stufe 34 |
| 64 | ⭐ **Beide Hände, tief gehalten** (Hulf 2, Q_SIDE_B1_132) | Side | 3 Kämpfe |
| 65 | ⚔ **Q_MAIN_K3_035** ⚠ Die Schattenwölfin *(Mini-Boss)* | Haupt | Stufe 35 |

---

## Phase 8 – Ruka (Stufe 36–40)

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 66 | ⚔ **Q_MAIN_K3_036** Die Dunkle auf dem Grat | Haupt | Stufe 36 |
| 67 | ⭐ **Der Wolf, der den Plan kennt** (Asch 1, Q_SIDE_B1_151) | Side | Ruka-Bindung 1 · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (K3_036) gleichzeitig* |
| 68 | ⚔ **Q_MAIN_K3_037** Der Hase am Fels | Haupt | Stufe 37 |
| 69 | 🧑 **Asch** (Ruka) | Held | Bindung 2 |
| 70 | ⚔ **Q_MAIN_K3_038** Wo der Geruch hingeht | Haupt | Stufe 38 |
| 70a | 🔧 **Der Jagdplatz** (Q_BAU_005) | Bau | Jagdplatz bauen (E3-Freischaltung) · *Hinweis: bewusste Reihenfolge Fabian; Story-Prequest weich (Rukas Windregel, K3_038)* |
| 70b | 🔧 **Der Werkplatz** (Q_BAU_006) | Bau | Werkplatz bauen (E3-Freischaltung nach K3_039) · *Hinweis: bewusste Reihenfolge Fabian; Story-Prequest weich* |
| 71 | 🔨 **Der Platz, an dem gejagt wird** (Q_BAU_015) | Bau | Jagdplatz St. 2  · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Q_BAU_005) weich* |
| 72 | ⚔ **Q_MAIN_K3_039** Erste Zusammenarbeit | Haupt | Stufe 39 |
| 73 | ⭐ **Zwei Schritte hinter ihr** (Asch 2, Q_SIDE_B1_152) | Side | 3 Kämpfe · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (K3_039) weich* |
| 74 | ⚔ **Q_MAIN_K3_040** ⚠ Die Wadenbeißer-Brut *(Mini-Boss)* | Haupt | Stufe 40 |

---

## Phase 9 – Eisfang (Stufe 41–45) + Epoche-Abschluss

| # | Was | Typ | Aufgabe |
|---|---|---|---|
| 75 | ⚔ Q_MAIN_K3_041 Rudelruf in der Ferne | Haupt | Stufe 41 |
| 76 | ⚔ Q_MAIN_K3_042 Die Umzingelung | Haupt | Stufe 42 |
| 78 | ⚔ Q_MAIN_K3_043 Kristalle im Fell | Haupt | Stufe 43 · *Position 77 bewusst leer (gestrichene Zeile, S3); Nummern bleiben stabil* |
| 79 | 🔨 **Werkzeug, das hält** (Q_BAU_016, Werkplatz St. 2) | Bau | Ausbau  · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (Q_BAU_006) weich* |
| 80 | ⚔ Q_MAIN_K3_044 Vor dem Sturm | Haupt | Stufe 44 |
| 81 | ⭐ **Die kahle Narbe** (Asch 3, Q_SIDE_B1_153) | Side | Ruka-Bindung 3 · *Hinweis: bewusste Reihenfolge Fabian; Basis-Prequest (K3_045) weich, vor dem Endboss startbar* |
| 82 | 🧑 **Dreißig und drei** (Bako) | Held | Alle E1-Gebäude St. 2 |
| 83 | ⚔ **Q_MAIN_K3_045** ⚠⚠ **Die Leitwölfin (Eisfang)** | Haupt | Stufe 45 = **Kapitel-3-Endboss** |
| 84 | 📖 Story: Ruka treibt sie ab; „sieben Winter verrückt" | — | automatisch |
| 85 | 🏆 Titel „Rudelfreund" + Slot 4 (Jagdplatz) aktiv | Abschluss | Epoche 1, Kapitel 1–3 komplett |
| 86 | 📖 **Next-Hook:** Talas Fährte im Schlamm ist zu gerade für ein Tier — sie führt nach unten. Epoche 2 („Die Knochen-Zelte", Skalde-Gegner) kündigt sich an; Koop-Felder (Zeichenfels-Gilde) öffnen parallel | Abschluss | Übergang E2 |

---

## Sitzungsplan (S1)

Ziel: 4 Sessions à 5 min pro Tag (GDD-Pacing). Eine Phase = ca. 2–3 Sessions.

| Phase | Stufen | Sessions | Abschluss-Moment |
|---|---|---|---|
| 1 Ankommen | Tut + 1–5 | 3 | Mini-Boss Schattenpfote → Dorf-Moment: Brakka zählt abends |
| 2 Erste Schrift | 6–10 | 2–3 | Mini-Boss Die Meute → Helden-Moment: Olms Reihe hält allein |
| 3 Knirsch | 11–15 | 2 | Endboss Knirsch → Dorf-Moment: Kapitel-Abschluss-Szene |
| 4 Naras Paste | 16–20 | 2 | Mini-Boss Der wartende Bock → Helden-Moment: Naras zweite Berührung |
| 5 Drei am Kamm | 21–25 | 2 | Mini-Boss Die Weißgewandete → Dorf-Moment: die drei sind weg, Zeichen bleiben |
| 6 Vask | 26–30 | 2–3 | Endboss Vask → Dorf-Moment: fremde Zeichen am Fels |
| 7 Das Jaulen | 31–35 | 2 | Mini-Boss Schattenwölfin → Helden-Moment: Olms tiefe Haltung |
| 8 Ruka | 36–40 | 2–3 | Mini-Boss Brut → Dorf-Moment: Ruka bleibt, Kuhle am Rand |
| 9 Eisfang | 41–45 | 2–3 | Endboss Eisfang → Abschluss: sieben Winter verrückt + Fährte nach unten |

Regel: Nach jedem Mini-/Endboss folgt in derselben oder nächsten Session ein Dorf-/Helden-Moment (30–60 s Szene, kein Kampf).

---

## Annex (S8): vollständige Quest-Tabelle, maschinenlesbar

Alle 86 Quests mit den erweiterten Spalten. Quelle der Wahrheit bleibt die Basis-Spec (`quests-epoche1-k1-k3.md`); diese Tabelle ist der Index. Format: `quest_id | prequest | Pflicht? | Belohnung (Hauptkürzel) | Parallel-Slot | Position`.

| quest_id | prequest | Pflicht? | Belohnung | Parallel-Slot | Pos. |
|---|---|---|---|---|---|
| Q_BAU_001 | – | Soft-Gate (Slot 1) | Baustoff | Bau: Slot 1 | 1 |
| Q_BAU_002 | – | Soft-Gate (Slot 2) | Baustoff | Bau: Slot 2 | 2 |
| Q_MAIN_K1_001 | Tutorial-Abschluss | **Pflicht** | hero_xp 50 | – | 3 |
| Q_SIDE_B1_101 | – (weich) | optional | hero_xp 80 | Side 1/3 | 4 |
| Q_HERO_BRAKKA | – | optional | hero_xp 100 | Held: Brakka | 5 |
| Q_MAIN_K1_002 | Q_MAIN_K1_001 | **Pflicht** | res_wood 100 | – | 6 |
| Q_MAIN_K1_003 | Q_MAIN_K1_002 | **Pflicht** | hero_xp 80 | – | 7 |
| Q_SIDE_B1_111 | – (weich) | optional | res_wood 200 | Side 2/3 | 8 |
| Q_HERO_OLM | Q_MAIN_K1_003 | optional | hero_xp 100 | Held: Olm | 9 |
| Q_MAIN_K1_004 | Q_MAIN_K1_003 | **Pflicht** | hero_xp 80 | – | 10 |
| Q_MAIN_K1_005 | Q_MAIN_K1_004 | **Pflicht** | hero_xp 100 + gems 3 | – | 11 |
| Q_MAIN_K1_006 | Q_MAIN_K1_005 | **Pflicht** | hero_xp 80 + echo 5 | – | 12 |
| Q_SIDE_B1_121 | – (gleichzeitig) | optional | hero_xp 120 + echo 5 | Side 3/3 | 14 |
| Q_BAU_004 | – (weich, mit K1_006) | Soft-Gate (Slot 13) | ticket 1 | Bau: Slot 13 | 13 |
| Q_MAIN_K1_007 | Q_MAIN_K1_006 | **Pflicht** | res_stone 100 | – | 15 |
| Q_MAIN_K1_008 | Q_MAIN_K1_007 | **Pflicht** | hero_xp 80 | – | 16 |
| Q_SIDE_B1_141 | – (weich, K1_008) | optional | hero_xp 80 | Side 1/3 (Rückkehr) | 17 |
| Q_SIDE_B1_131 | – (weich, K1_003) | optional | hero_xp 80 | Side 2/3 (Rückkehr) | 18 |
| Q_MAIN_K1_009 | Q_MAIN_K1_008 | **Pflicht** | res_food 150 | – | 19 |
| Q_BAU_013 | – (weich, Q_BAU_003) | optional | res_food 150 + xp 50 | Bau: Slot 3 | 20 |
| Q_MAIN_K1_010 | Q_MAIN_K1_009 | **Pflicht** | hero_xp 120 + gems 5 | – | 21 |
| Q_MAIN_K1_011 | Q_MAIN_K1_010 | **Pflicht** | hero_xp 80 | – | 22 |
| Q_MAIN_K1_012 | Q_MAIN_K1_011 | **Pflicht** | res 100+100 | – | 23 |
| Q_MAIN_K1_013 | Q_MAIN_K1_012 | **Pflicht** | hero_xp 80 | – | 24 |
| Q_SIDE_B1_103 | – (weich, Kiko-2) | optional | hero_xp 100 + echo 5 | Side 1/3 (Rückkehr) | 25 |
| Q_BAU_011 | – (weich, Q_BAU_001) | optional | res_food 100 + xp 50 | Bau: Slot 1 | 26 |
| Q_MAIN_K1_014 | Q_MAIN_K1_013 | **Pflicht** | hero_xp 100+100 | – | 27 |
| Q_MAIN_K1_015 | Q_MAIN_K1_014 | **Pflicht** (Endboss) | xp 200 + ticket 1 | – | 28 |
| Q_SIDE_B1_143 | – (weich, Gorm-2) | optional | hero_xp 100 | Side (Rückkehr) | 30 |
| Q_BAU_003 | – (weich, E2-Gate) | Soft-Gate (Slot 3) | res_food 100 | Bau: Slot 3 | 31 |
| Q_MAIN_K2_016 | Q_MAIN_K1_015 | **Pflicht** | hero_xp 80 | – | 32 |
| Q_HERO_NARA | – | optional | hero_xp 100 | Held: Nara | 33 |
| Q_MAIN_K2_017 | Q_MAIN_K2_016 | **Pflicht** | xp 80 + echo 5 | – | 34 |
| Q_SIDE_B1_112 | Q_SIDE_B1_111 | optional | hero_xp 100 | Side (Kette) | 35 |
| Q_MAIN_K2_018 | Q_MAIN_K2_017 | **Pflicht** | res_food 150 | – | 36 |
| Q_MAIN_K2_019 | Q_MAIN_K2_018 | **Pflicht** | hero_xp 80 | – | 37 |
| Q_SIDE_B1_122 | Q_SIDE_B1_121 | optional | xp 80+80 | Side (Kette) | 38 |
| Q_MAIN_K2_020 | Q_MAIN_K2_019 | **Pflicht** | xp 120 + gems 5 | – | 39 |
| Q_MAIN_K2_021 | Q_MAIN_K2_020 | **Pflicht** | xp 100 + gems 5 | – | 40 |
| Q_HERO_TALA | Q_MAIN_K2_021 | optional | xp 150 + echo 10 | Held: Tala | 41 |
| Q_MAIN_K2_022 | Q_MAIN_K2_021 | **Pflicht** | xp 100 + echo 5 | – | 42 |
| Q_SIDE_B1_123 | Q_SIDE_B1_122 | optional | xp 150 + gems 5 | Side (Kette) | 43 |
| Q_BAU_014 | – (weich, Q_BAU_004) | optional | echo 5 + xp 50 | Bau: Slot 13 | 44 |
| Q_MAIN_K2_023 | Q_MAIN_K2_022 | **Pflicht** | hero_xp 80 | – | 45 |
| Q_MAIN_K2_024 | Q_MAIN_K2_023 | **Pflicht** | res 100+100 | – | 46 |
| Q_MAIN_K2_025 | Q_MAIN_K2_024 | **Pflicht** (Mini) | xp 120 + ticket 1 | – | 47 |
| Q_MAIN_K2_026 | Q_MAIN_K2_025 | **Pflicht** | hero_xp 80 | – | 48 |
| Q_SIDE_B1_102 | Q_SIDE_B1_101 | optional | xp 80 + wood 100 | Side (Kette) | 49 |
| Q_MAIN_K2_027 | Q_MAIN_K2_026 | **Pflicht** | hero_xp 100 | – | 50 |
| Q_HERO_KIKO | Q_SIDE_B1_101 | optional | hero_xp 120 | Held: Kiko | 51 |
| Q_MAIN_K2_028 | Q_MAIN_K2_027 | **Pflicht** | xp 100 + wood 100 | – | 52 |
| Q_MAIN_K2_029 | Q_MAIN_K2_028 | **Pflicht** | stone 100 + xp 80 | – | 53 |
| Q_MAIN_K2_030 | Q_MAIN_K2_029 | **Pflicht** (Endboss) | xp 200 + ticket 1 + echo 10 | – | 54 |
| Q_SIDE_B1_113 | Q_SIDE_B1_112 | optional | xp 120 + Titel | Side (Kette) | 56 |
| Q_BAU_012 | – (weich, Q_BAU_002) | optional | wood 200 + stone 100 | Bau: Slot 2 | 57 |
| Q_SIDE_B1_133 | Q_SIDE_B1_132 | optional | xp 100 + echo 5 | Side (Kette) | 58 |
| Q_MAIN_K3_031 | Q_MAIN_K2_030 | **Pflicht** | hero_xp 80 | – | 59 |
| Q_MAIN_K3_032 | Q_MAIN_K3_031 | **Pflicht** | res_food 150 | – | 60 |
| Q_MAIN_K3_033 | Q_MAIN_K3_032 | **Pflicht** | hero_xp 80 | – | 61 |
| Q_SIDE_B1_142 | Q_SIDE_B1_141 | optional | hero_xp 80 | Side (Kette) | 62 |
| Q_MAIN_K3_034 | Q_MAIN_K3_033 | **Pflicht** | xp 100 + stone 100 | – | 63 |
| Q_SIDE_B1_132 | Q_SIDE_B1_131 | optional | hero_xp 100 | Side (Kette) | 64 |
| Q_MAIN_K3_035 | Q_MAIN_K3_034 | **Pflicht** (Mini) | xp 120 + gems 5 | – | 65 |
| Q_MAIN_K3_036 | Q_MAIN_K3_035 | **Pflicht** | xp 100 + gems 5 | – | 66 |
| Q_SIDE_B1_151 | Q_MAIN_K3_036 | optional | hero_xp 80 | Side (Kette) | 67 |
| Q_MAIN_K3_037 | Q_MAIN_K3_036 | **Pflicht** | xp 100 + food 100 | – | 68 |
| Q_HERO_RUKA | Q_MAIN_K3_037 | optional | hero_xp 150 | Held: Ruka | 69 |
| Q_MAIN_K3_038 | Q_MAIN_K3_037 | **Pflicht** | xp 100 + wood 100 | – | 70 |
| Q_BAU_005 | – (weich, E3-Gate) | Soft-Gate (Slot 4) | res_food 200 | Bau: Slot 4 | 70a |
| Q_BAU_015 | – (weich, Q_BAU_005) | optional | food 200 + xp 50 | Bau: Slot 4 | 71 |
| Q_MAIN_K3_039 | Q_MAIN_K3_038 | **Pflicht** | xp 100+100 | – | 72 |
| Q_SIDE_B1_152 | Q_SIDE_B1_151 | optional | hero_xp 80 | Side (Kette) | 73 |
| Q_MAIN_K3_040 | Q_MAIN_K3_039 | **Pflicht** (Mini) | xp 120 + ticket 1 | – | 74 |
| Q_MAIN_K3_041 | Q_MAIN_K3_040 | **Pflicht** | hero_xp 80 | – | 75 |
| Q_MAIN_K3_042 | Q_MAIN_K3_041 | **Pflicht** | res 150+150 | – | 76 |
| Q_MAIN_K3_043 | Q_MAIN_K3_042 | **Pflicht** | xp 100 + echo 5 | – | 78 |
| Q_BAU_006 | – (weich, E3) | Soft-Gate (Slot 5) | stone 200 + xp 100 | Bau: Slot 5 | 70b |
| Q_BAU_016 | – (weich, Q_BAU_006) | optional | stone 200 + xp 100 | Bau: Slot 5 | 79 |
| Q_MAIN_K3_044 | Q_MAIN_K3_043 | **Pflicht** | res 100+100+100 | – | 80 |
| Q_SIDE_B1_153 | Q_SIDE_B1_152 | optional | hero_xp 100 | Side (Kette) | 81 |
| Q_HERO_BAKO | Q_SIDE_B1_113 | optional | xp 120 + wood 200 | Held: Bako | 82 |
| Q_MAIN_K3_045 | Q_MAIN_K3_044 | **Pflicht** (Endboss) | xp 300 + ticket 1 + Titel | – | 83 |

*(Positionen 55, 77 bewusst leer: 55 = Story-Moment ohne eigene Quest, 77 = gestrichene Zeile S3. Q_BAU_007/008/009 und Q_HERO_MIRA sind E4+-Platzhalter und nicht Teil der 86 aktiven — Summe: 86 wie in M10.)*

---

## Regeln, die die Timeline regelt

- **Hauptquest ist linear:** Jede Quest hat genau einen Prequest, 1 aktiv gleichzeitig.
- **Sidequests blockieren nie den Faden (S8/S9):** Ihre Prequests sind immer bereits erledigte Hauptquests oder eigene Kettenglieder; bis 3 parallel sichtbar. **Pflicht?**: Nur Hauptquests sind Pflicht (Content-Gate); Bau-Einleitungen sind Pflicht für Slot-Bau (Soft-Gate), Ausbauten/Side/Helden-Quests sind optional. **Parallel-Slot:** Side 1 von 3 (Regel S9), Bau max. 1 aktiv pro Slot, Helden-Quest 1 pro Held.
- **Baukunst dockt an Slots:** Einleitungen erscheinen mit der Slot-Freischaltung, Ausbauten sobald die Zielstufe ausbaubar ist.
- **Helden-Quests starten mit Debüt/Freischaltung:** Brakka/Nara sofort, Kiko nach Kiko-1, Tala nach K2_021, Ruka nach K3_037, Mira später (E4+).
- **Belohnungsrhythmus:** Mini-Bosse 25 + 40 → 1 Ticket; Mini-Bosse 5/10/20/35 → 3–5 Kristalle; Endbosse (15/30/45) → 1 Ticket (+ Titel bei K3); Baukunst → Baustoff, Ticket nur bei Slot-Einleitungen (Q_BAU_004, Q_BAU_009); Sidequests → Echosplitter/keine Kristalle. Maßgeblich: Wahrheitstabelle unten.

**Mapping verbindlich (M7):** Stufe n = e1_camp_n (01–45). CSVs/GDD sind noch auf 30 Level — Migrationsaufgabe: campaign_levels.csv/campaign_waves.csv auf 45 erweitern, GDD §8 anpassen. Bis dahin ist die Timeline die Spec, die CSVs folgen.

---

## Belohnungs-Wahrheitstabelle (M6)

Maßgeblich ist die Quest-Basis (`quests-epoche1-k1-k3.md`); diese Tabelle fasst den Rhythmus zusammen.

| Stufe | Kampf-Typ | Belohnung (Hauptquest) |
|---|---|---|
| 1–4, 6–9, 11–14 (K1) · 16–19, 21–24, 26–29 (K2) · 31–34, 36–39, 41–44 (K3) | Normale Stufe | Heldenerfahrung klein (50–100) oder Ressourcen (100–200) |
| 5, 10, 20, 35 | Mini-Boss | Heldenerfahrung 120 + 3–5 Kristalle (kein Ticket) |
| 25, 40 | Mini-Boss | Heldenerfahrung 120 + 1 Ticket |
| 15, 30, 45 | Endboss | Heldenerfahrung 200–300 + 1 Ticket; K3: + Titel „Rudelfreund" |
| Story-Momente (17, 22, 36, 37, 43) | Stufe mit Story-Beat | + 5–10 Echosplitter zusätzlich |

Sidequests: **keine Kristalle** (Echosplitter, kleine Ressourcen, Titel). Baukunst: Baustoff, Ticket nur bei Slot-Einleitung. Helden-Quests: Heldenerfahrung groß, Kristalle nur bei Kettenabschluss.

---

## Tutorial-Schnitt (M8/S11)

- Tut-CSV hat Q_TUT_001–020 (= 20 Schritte); **Migrationsaufgabe (konkret, Rechenweg):** Ziel 12 Schritte = 20 − 8.
  - 5 Merges (−5): (001+002) → 1 Schritt Holz/Sammler-Basis · (003+004) → 1 Schritt Lager/Kreis · (011+012) → 1 Schritt Vorrat+Mauer · (013+014) → 1 Schritt Speicher+Schutz · (016+017) → 1 Schritt Sammel-Block
  - 3 Streichungen (−3): Q_TUT_009 (redundant zu 008) · Q_TUT_018 (redundant zu 017) · Q_TUT_020 fällt (Armee-Bau geht in k1_s01 über)
  - Ergebnis: 20 − 5 − 3 = **12 Schritte**. Überspringbar ab Schritt 4.
  - Reihenfolge der 12 Schritte: (1) 001+002 · (2) 003+004 · (3) 005 · (4) 006 · (5) 007 · (6) 008 · (7) 010 · (8) 011+012 · (9) 013+014 · (10) 015 · (11) 016+017 · (12) 019
  - *(009 und 018 gestrichen, 020 entfällt — deshalb fehlen sie in der Reihenfolge.)*
- Tutorial deckt Bau-Basics + ersten Gefechts-Tutorialkampf ab; **keine Kampagnen-Mission** darin.
- Danach startet **k1_s01** (= e1_camp_01) als Mission 1. Keine doppelte Mission.
- Tut-Abschluss-Prequest der Hauptquest bleibt: „Tutorial-Abschluss" (letzte Tut-ID nach Kürzung).

---

## Koop-Abgrenzung (M12)

Die Hauptstory von K1–K3 bewusst **ohne Koop** — sie ist Brakkas Geschichte. Koop-Elemente (Zeichenfels/Gilde ab E2, Events, PvP) existieren parallel und werden über **Neben- und Baukunst-Quests** angedockt, nie über die Hauptkette.

---

## Ticket-Mathematik und Soft-Gates (S4)

**Ticket-Quellen in K1–K3 (verbindlich):**
| Quelle | Tickets |
|---|---|
| Endboss K1_015 (Knirsch) | 1 |
| Mini-Boss K2_025 (Die Weißgewandete) | 1 |
| Endboss K2_030 (Vask) | 1 |
| Mini-Boss K3_040 (Die Wadenbeißer-Brut) | 1 |
| Endboss K3_045 (Eisfang) | 1 |
| Bau-Einleitung Q_BAU_004 (Zeichenfels) | 1 |
| Bau-Einleitung Q_BAU_009 (Kaserne, E4+-Platzhalter) | 1 (zählt erst ab Bau) |
| **Summe bis K3-Ende** | **6** (5 sofort erreichbar + 1 bei E4-Bau) |

Beschwörung kostet Kristalle, keine Tickets (GDD-Regel). 6 Tickets reichen für die freigespielten Züge der E1-Banner-Reihenfolge [Annahme: Bannerplan GDD §9]. F2P-Defizit gibt es nicht — Tickets sind Bonus-Züge, kein Gate.

**Soft-Gates (kein Hard-Gate im Content):**
- Slot-Freischaltungen (Feuerstelle, Sammler, Wohnraum E2, Jagdplatz E3) blockieren Bauen, nie die Story-Kette.
- Sidequests/Helden-Quests sind optional; ihre Belohnungen (Echosplitter, Titel) sind kosmetisch/sammlerisch.
- Kiko-1-Spielzeit-Ziel: Kosmetik-Bonus, kein Fortschritts-Gate.
- Keine IAP-Voraussetzung für eine der 86 Quests.

## F2P-Block (S4)

K1–K3 sind **100 % F2P spielbar**. IAP in Epoche 1: nur Komfort (Bau-Beschleunigung, Slots), kein Content-Gate, keine Kampf-Balance-Items. Beschwörung nur mit verdienten Kristallen (GDD-Regel).

---

## Begriffsblock (S7)

- **Äther-Kristalle** = Story-Element (wachsen an Frostwölfen/Eisfang; Vorläufer der Tiefenschwärme). Kein Shop-Bezug.
- **Zeitkristalle** (`cur_gems_free`) = Shop-/Belohnungswährung. In Questtexten heißen sie „Kristalle" nur im Belohnungs-Kontext.

---

## Helden-Tabelle (S6)

| Held | Debüt in der Timeline | Helden-Quest-Start | Korrektur-Hinweise |
|---|---|---|---|
| Brakka | ab Stufe 1 (Anführerin) | sofort | zählt, entscheidet; E-157 |
| Nara | ab Stufe 1 | sofort | Heilerin, KEIN Boss |
| Olm | ab Stufe 1 | nach K1_003 | Truppen-Ausbilder, KEIN Boss |
| Kiko | ab Stufe 1 | nach Kiko-1-Side | Feuerwächter |
| Tala | ab Stufe 1 | nach K2_021 | beobachtet, zeichnet |
| Ruka | **Stufe 36** (Die Dunkle auf dem Grat) | nach K3_037 | **nicht im Tutorial** (kein Tut-Beschwörungs-Moment in v2) |
| Bako | ab Stufe 1 | nach Bako-3-Side | Baumeister der Kuhlen |
| Mira | **E4+** (Grauvater) | Platzhalter | noch nicht in K1–K3 |
| Terwish | — | — | **nicht in E1** (stürzt erst E17) |

---

## ID-Checkliste: alle 86 Quests (M10)

**Hauptquest (45):** Q_MAIN_K1_001–015 · Q_MAIN_K2_016–030 · Q_MAIN_K3_031–045 *(jede = genau eine Kampagnenstufe k*_s01–45 = e1_camp_01–45)*

**Sidequests (18, 6 Ketten à 3):** Q_SIDE_B1_101–103 (Kiko) · 111–113 (Bako) · 121–123 (Talas Zeichen) · 131–133 (Hulf) · 141–143 (Gorm) · 151–153 (Asch)

**Baukunst (15):** Q_BAU_001, 002, 003, 004, 005, 006 (Einleitungen: Feuerstelle, Reisig, Schlafkuhlen, Zeichenfels, Jagdplatz, Werkplatz) · Q_BAU_007, 008, 009 (Platzhalter E4+: Totem, Wall, Kaserne) · Q_BAU_011, 012, 013, 014, 015, 016 (Ausbauten St. 2)
*(Hinweis: Q_BAU_010 existiert nicht — Nummernlücke zwischen Einleitungen und Ausbauten, bewusst zur Gruppierung.)*

**Helden-Quests (8):** Q_HERO_BRAKKA · Q_HERO_NARA · Q_HERO_KIKO · Q_HERO_TALA · Q_HERO_RUKA · Q_HERO_OLM · Q_HERO_BAKO · Q_HERO_MIRA *(Platzhalter E4+)*

**Summe: 45 + 18 + 15 + 8 = 86** ✔

**Parallel-Regel (S9):** bis 3 Sidequests gleichzeitig sichtbar. Bei Überlauf wird die älteste **nicht gestartete** Sidequest aus der Sichtbarkeit genommen und erscheint wieder, sobald ein Slot frei ist. Gestartete Ketten laufen immer weiter.

**Mapping (M7):** k1_s01–15 → e1_camp_01–15 · k2_s16–30 → e1_camp_16–30 · k3_s31–45 → e1_camp_31–45. Die jetzige 30er-CSV wird auf 45 erweitert (Migrationsaufgabe, nicht Teil dieses Docs).
