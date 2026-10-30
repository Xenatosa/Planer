# BAUPLAN_E100 – Gebäude- und Platzbedarf bis Epoche 100 (t16u, ersetzt t14u-Fassung → `_alt/BAUPLAN_E100_t14u.md`)

Marker: [S] Quelle, [A] Annahme/Hochrechnung, [R] berechnet (Skript genannt), [F] Fabian.
Quellen (nur gelesen):
- `…/zonen_c20/groessen_25slots/layout_v8_neu/wachstum/WACHSTUM.md` + `_zahlen.json` (E1–E16)
- `…/layout_v8_neu/ausbau_e40/AUSBAU_E40.md` + `zahlen_ausbau.json`, `bruecken_villen/BRUECKEN_VILLEN.md` (E17–E40)
- `team/gdd/GDD_v1.7.11.md` (neueste Fassung, mit `_OFFEN.md`), `team/gdd/uebernahme_2026-10-28/GEBAEUDE_SLOTS_GUELTIG.md`

Freigabe: Laut AD t726u hat Fabian die Wachstumsplanung freigegeben. GEBAEUDE_SLOTS_GUELTIG.md §3 (29.10.) nennt die Hauszahl 103 dagegen noch „gilt nicht“. Hier gilt die AD-Freigabe; siehe Offene Entscheidung 1.

## 1 Warum 99 / 116 / 64–70 / 140 / 233? (alle Zählungen erklärt)

| Zahl | Was wird gezählt | Quelle | Status |
|---|---|---|---|
| 99 | Plätze im Zonenplan v8/v9: 78 W (Wohnen) + 21 D (Deko) | BEFUNDE_ZONEN_c20_v8.md [S] | Grundlage, aber nur 75 davon werden genutzt |
| 116 | Plätze bei E16 | WACHSTUM.md [S] | gültig (E16-Plan) |
| 64 / 70 | Gebäude-IDs v2.7 (E1–E16) bzw. Simulationszahl bis E18 | 13_gebaeude_stufen.csv, sim_1500 [S] | **überholt**. Meine Zahl in BAUPLAN_ABGLEICH.md → `_alt/` |
| 140 | Gebäude bei E16 | WACHSTUM.md [S] | gültig |
| 233 | Gebäude bei E40 | AUSBAU_E40.md [S] | Vorschlag; mit Villen 225 |
| 30 | Funktionsslots (je 1 Gebäude) | GDD Kap. 4, GÜLTIG [S/F] | gültig |

Aufschlüsselung 116 [S]:
- 75 v8-Plätze + 41 neue Plätze.
- 24 v8-Plätze entfallen: 16 werden von Funktionsslots überbaut, auf 8 passt kein Haustyp.

Aufschlüsselung 140 [S]:
- 103 Wohnhäuser (nach 13d-Formel nur 17).
- 13 Deko.
- 24 Funktionsflächen (Funktion 25 inkl. Palisade, die nur gezählt und nicht gezeichnet wird).

Aufschlüsselung 233 [S]:
- 194 Wohn (116 Bestand + 91 neue Schnee-Plätze, Bestand inkl. 19 Turmhäuser), 15 Deko, 24 Funktionsflächen.
- Mit Villen 225: 3 Villen verdrängen 11 Hütten-Plätze.

Gültige Zählweise: **Gebäude = Wohnhäuser + Deko + Funktionsflächen.**
- Funktion = Slots (jedes Gebäude einmal, Ausbau über 55 Stufen auf demselben Platz).
- Wohnhäuser sind Deko-Instanzen von Slot 23 (Hütte). Sie haben keine eigene Funktion, belegen aber Plätze.

### Korrigierte eigene Annahmen (t13u/t14u)
1. **Deckel 18 Deko-Häuser:** Ich hatte ihn als Bedarf angesetzt. **Falsch** für die freigegebene Planung, dort sind es 103 (E16) bzw. 194 (E40).
2. **„52 Flur-Deko“ bei E100:** Das war meine Hochrechnung der 13d-Regel. **Überholt**, die Quellen zählen 13–15 Deko.
3. **Eigene Standortvorschläge** in overlay_plaetze_erweiterung (t14u): **zurückgezogen**, liegen jetzt in `_alt/`. Die Plätze stammen aus den Quellen.
4. **Maße für E17+:** Ich hatte „wie E12–E16“ angenommen. **Überholt**: Die Größen kommen aus `groessen_25_slots_E17_E40.csv` / `haustypen_E17_E40.csv` [A, abgeleitet ×1,2/×1,4/×1,6].

### Fehler/Lücke in den Quellen (Befund)
- **AUSBAU_E40 zählt nur 25 Funktionsslots.**
  - Laut GDD Kap. 4 kommen bis E40 aber schon die Slots 26 Glashütte (E17), 27 Saline (E21) und 28 Pigment (E24) dazu [S]. Bei E51/E53 folgen 29 Module und 30 Äther-Destille.
  - Diese **5 Slots haben in WACHSTUM/AUSBAU keinen Platz**.
- **Footprints 26–30 widersprechen sich:**
  - GDD Z.112/353: 16/36/24/36/48 m² [A/R].
  - GÜLTIG: 16/25/20/36/48 m².
  - Unterschiedlich sind Slot 27 und 28.

## 2 Gebäude je Epoche

| Epoche | Gebäude | Wohn | Deko | Funktion (Slots) | Plätze | Quelle/Marker |
|---|---|---|---|---|---|---|
| E1 | 27 | 14 | 1 | 13 | 15 | [S] WACHSTUM |
| E4 | 54 | 30 | 5 | 20 | 35 | [S] |
| E8 | 79 | 46 | 9 | 25 | 55 | [S] |
| E12 | 107 | 71 | 12 | 25 | 83 | [S] |
| E16 | 140 | 103 | 13 | 25 | 116 | [S] |
| E24 | 178 | 140 | 14 | 25 (+2 lt. GDD fehlen) | 153 | [S] AUSBAU (Plätze [R] 116+37) |
| E32 | 210 | 172 | 14 | 25 (+3 fehlen) | 185 | [S] |
| E40 | 233 | 194 | 15 | 25 (+3 fehlen) | 207 + 2 Quartiersplätze | [S] |
| E41–E50 | – | – | – | 28 | – | Funktion [S] GDD, Rest keine Quelle |
| E51 | – | – | – | 29 | – | [S] GDD |
| E53–E100 | – | – | – | 30 | – | [S] GDD |

**Hochrechnung E100 [A]:** Es gibt keine Quelle. Zwei Varianten; der Trend kommt aus der Tabelle oben [R]:
- Zuwachs Wohnhäuser je Epoche: E16–24 4,6, E24–32 4,0, E32–40 2,75.
- Deko: +1 je ~8 Epochen.

| Variante | Wohn E100 | Deko E100 | Funktionsflächen | Gebäude E100 | neue Plätze nach E40 |
|---|---|---|---|---|---|
| H1 linear weiter (2,75/Epoche) [A] | 194 + 165 = 359 | 15 + 7 = 22 | 29 (30 ohne Palisade-Fläche) | **410** | ≈165 Hütten 5×5 + 5 Slots + 7 Deko |
| H2 Sättigung (nur noch Höhe/Typwechsel wie E32→E40-Bestand) [A] | 194 | 22 | 29 | **245** | 5 Slots + 7 Deko |

## 3 Prüfung Quellplätze gegen Geländeraster [R `pruef_plaetze_quellen.py`]

- Umrechnung: Pixel px = (Plan-m + 200)·30 → Zelle = px/25, also Plan-m × 1,2 = echte m.
- „Innerhalb“ heißt: ≥95 % der Zellen sind bebaubar [A].

| Stand | Plätze/Flächen | innerhalb bebaubar | außerhalb Senke | Abstand Wand/Wasser <2 m | Wand/Wasser/Schatten als Hauptgrund |
|---|---|---|---|---|---|
| E16 | 140 | **118** | 20 | 2 | 0 |
| E40 | 233 | **119** | 112 | 2 | 0 |

Fehlstellen nach Gebiet [R `gen_bauzone_befund.py`]:

| Gebiet | E16 | E40 |
|---|---|---|
| Nordwest-Ebene | 16 | 39 |
| West-Tal | 1 | 27 |
| Süd (Flussband) | 0 | 42 |
| Nordost-Rand | 4 | 5 |
| Senke-Rand | 1 | 1 |

- Von den 114 E40-Fehlstellen liegen **96 zu ≥95 % auf freiem, begehbarem Schnee/Boden**. Das Gelände trägt sie; es fehlt nur die Bauzonen-Maske.
- 8 liegen bei 80–95 %, 10 unter 80 %. Bei diesen Plätzen liegt Wald/Eis/Wand im Platz, zusammen 181 Zellen. Meist ist es der Bach im West-Tal (rote Kante im Bild).
- **Ergebnis: Die Bauzone muss größer werden.**
  - Für E16: +988 m², vor allem Nordwest-Ebene und Nordost-Rand.
  - Für E40: +4 515 m², zusätzlich West-Tal und Süd-Flussband.
  - Die Karte bleibt dabei unverändert.
- Bilder:
  - `pruefung/t16u_plaetze_E16_gegen_bebaubar.png`, `pruefung/t16u_plaetze_E40_gegen_bebaubar.png` (blau = Treffer, rot = Fehlstelle)
  - `overlay_plaetze_erweiterung.png` (magenta = nötige Erweiterung E16, orange = E40, rot = Hindernis im Platz)
- Tabellen: `pruefung/t16u_plaetze_gegen_bebaubar.csv`, `overlay_plaetze_erweiterung.csv/.json` (Befund je Platz, keine neuen Standorte).

## 4 Platzbedarf E100 gegen Gelände [R grob, [A] Hochrechnung]

- **bebaubar heute:** 27 140 m². Davon sind nach E40 (mit 2-m-Puffer) noch 10 488 m² frei.
- **Schnee außerhalb bebaubar:** 33 665 m², davon 23 262 m² frei.
- **Grobe Kapazität:** Hütten 5×5 m auf einem 8-m-Raster, also mit Weg.
  - Rest-bebaubar ≈ 50.
  - Schnee ≈ 108.
  - Zusammen **≈158**, grob [R].
- AUSBAU_E40 hat eine strengere Schneemaske und kommt auf **höchstens 92–98 neue Schnee-Plätze insgesamt**; 91 sind bei E40 schon belegt [S].
- **H1 (≈165 neue Hütten + 5 Slots + 7 Deko) passt nicht.** Nach meiner Maske fehlt knapp etwas, nach der AUSBAU-Maske fehlt fast alles.
- **H2 passt**, wenn die Bauzone wie in §3 erweitert wird und die 5 Slots je 16–48 m² Platz bekommen.

## 5 Was Game Designer/Producer noch liefern müssen (E41–E100; nichts davon steht im GDD)
1. Wohnhauszahl bzw. Wachstumsregel für E41–E100 (H1/H2 oder andere). Das GDD hat nur Hütte = 8×1,08^(L−1) Einwohner und keine Hauszahl.
2. Deko-Zahl und -Arten ab E41.
3. Haustyp-Maße und -Höhen ab E41. Die Tabelle endet bei E33–40.
4. Slot-Maße ab E41 und eine verbindliche Footprint-Liste 26–30 (GDD und GÜLTIG widersprechen sich bei 27/28). Dazu deren Plätze im Dorfplan, die in WACHSTUM/AUSBAU fehlen.
5. Wann welche Schnee-Plätze geöffnet werden. In AUSBAU ist die Zuordnung zu Epochen nur Reihenfolge [A].
6. Ob die Bauzone über Brücken (11 Teilgebiete) ins Spiel kommt und wann.

## 6 Offene Entscheidungen (Abstand/Zusammenlegen aus t14u ruhen)
1. **Gültige Hauszahl:**
   - a) 140/233 laut AD-Freigabe. Dann muss GÜLTIG §3 angepasst werden.
   - b) 13d-Formel 17. Dann reichen die 99 Plätze fast ohne Erweiterung.
2. **Bauzonen-Maske erweitern:**
   - a) Nur E16 (+988 m²): kleinste Änderung, E17+ bleibt offen.
   - b) E40 (+4 515 m²): deckt den ganzen AUSBAU-Plan, braucht 11 Brücken.
   - c) Alle freien Schneeflächen als Ausbauringe (23 262 m²): Reserve für E41+.
3. **E41–E100:**
   - a) H2 Sättigung: passt aufs Gelände.
   - b) H1 linear: Platz reicht nicht, es bräuchte eine Kartenänderung.
   - c) Mittelweg: eine Obergrenze vom GD.
