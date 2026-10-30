# Bauplan-Abgleich Platz-Overlay (99 Plätze) gegen Epochenplan, Stand 30.10.2026 (t13u)

Gelände/Karte unverändert. Es wurden keine Standorte hinzugefügt. Grund: Es gibt bisher keine Bauplatzliste für E17 und später (siehe Lücken).

## Herkunft der 99 Plätze
- Die 99 Plätze stammen aus `zonen_c20_v9.json` (Zonenplan v8, GO Fabian t557u, in v9 unverändert) [S].
  - 78 W + 21 D, verteilt auf die Zonen A 29 / B 39 / C 12 / D 15 / E 4 [S] (`ZONEN_TABELLE_c20_v8.md`).
  - Die Zahl ergibt sich geometrisch aus dem Packen von Plätzen. Sie wurde nicht aus einer Gebäudeliste abgeleitet.
- Die Plätze haben **kein Feld „Epoche“** [S]. Eine Zuordnung Platz → Epoche gibt es im Overlay nicht.
- Herkunft von „bis Epoche 16“: Die Gebäudeliste `team/producer/spielkette/13_gebaeude_stufen.csv` (v2.7) enthält 64 Gebäude-IDs. Alle sind E1–E16 zugeordnet; E17 und später fehlen dort [S].
  - Dazu passt Paket W1-2: „E1–E8 voll, E9–E16 Gerüst, E17/E18 Platzhalter“ [S].

## Tabelle (neue Gebäude je Epoche, kumuliert gegen 99 Plätze)
| Epoche | Tage [S] | neue Gebäude laut Plan | kumuliert | im Overlay | fehlt | Quelle |
|---|---|---|---|---|---|---|
| E1 | 0–9 | 12 | 12 | 99 Plätze gesamt, ohne Epochenzuordnung | – | 13_gebaeude_stufen.csv [S] |
| E2–E8 | 9–194 | je 4 = 28 | 40 | ″ | – | dto. [S] |
| E9–E16 | 194–1204 | je 3 = 24 | 64 | ″ | – | dto. [S], W1-2 „Gerüst“ |
| E17–E18 | 1204–1504 | je 3 = 6 | 70 | ″ | **Lücke: keine IDs, keine Größen** | ergebnis_sim_1500_tage.md (nur Anzahl) [S] |
| E19–E40 | nach dem Horizont | E21–30: 1–2/Ep., E31–40: 1/Ep. | 81 (E40) | ″ | Lücke: nur Schätzung | aufbau/dorf-flaechenbedarf-e1-e40-v1.md [A in Quelle] |
| Deko/Frei | – | ~130 bis E40 | – | 17 baum_brunnen + plaetze_frei | nicht abgeglichen | dto. [A] |

Rechnung [R]: Bis zum Horizont von 1.500 Tagen (Ende E18 bei Tag 1.504) braucht der Plan 70 Gebäude. Das Overlay hat 99 Plätze, die Anzahl reicht also.
- Die Größen passen aber nicht sicher. 99 Plätze sind fast alle klein: 63 sind 4×4 m und nur 6 sind „groß“ (≥8×8 m) [S].
- Laut Paket W1-2 gibt es für die Gebäude nur Größenklassen, keine Maße. Ob die 64/70 Gebäude in die vorhandenen Platzgrößen passen, ist deshalb **nicht prüfbar**.

## Welche Datei ist aktuell
- Gebäudeliste: `team/producer/spielkette/13_gebaeude_stufen.csv` v2.7 (laut W1-2-Zusatz pt1513u). Sie ist auf origin/main und auf grundlagen-abgleich-v14 nicht vorhanden; gefunden in handygame-plan [S].
- Epochen/Tage: `ergebnis_sim_1500_tage.md` (v3, ohne Hartende) [S].
- Flächenbedarf bis E40: `aufbau/dorf-flaechenbedarf-e1-e40-v1.md` (22.10.2026). Sie ist älter als die Spielkette, und ihre Zahlen ab E2 sind dort selbst als [A] markiert.
- Layout Z1 mit 29 Gebäuden: `aufbau/ergebnis_bauzone_layout_v1.md` (P09). Das ist ein eigenes Layout und nicht das 99-Plätze-Overlay [S].

## Lücken (offen, nicht erfunden)
1. Es gibt keine Gebäudeliste für E17 und später (nur Anzahl 3 je Epoche) und keine für E19–E40 außer der groben Schätzung.
2. Es gibt keine Zuordnung Platz → Epoche oder Gebäude → Platz.
3. Die Footprints der Gebäude fehlen (nur Größenklasse). Ein Größenabgleich ist damit unmöglich.
4. Zu klären: Was meint Fabian mit „geht noch weiter“: E18 (Horizont 1.500 Tage) oder E40 (Flächenbedarf)?

Wer liefern muss: der Epochen Game Designer bzw. der Producer (Gebäudeliste E17 und später, Paket W1-2) und der Art Director (Footprints). Ohne diese Daten kommen keine neuen Standorte hinzu.
