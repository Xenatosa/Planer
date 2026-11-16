# FERTIGPLAN Dorfmap (Stand 16.11.2026, 07:30 Uhr MEZ)

Branch `art/dorfmap-fertig` (Basis eb2cd86 = p3d36). Marker: [S] gemessen, [A] Annahme, [R] gerechnet, [F] Fabian.

## Lieferregel [F] (Fabian, 16.11. 07:15, Variante A)
> „Wenn man es nicht sieht ist es mir egal. Aber hier geht es prinzipiell um Optik ist alles.“

1. Maßstab ist die Optik. Was mit bloßem Auge nicht sichtbar ist, kommt mit Messwert und Nahbild in die Ausnahmeliste und blockiert die Lieferung nicht. Die Ausnahmeliste gilt ab sofort.
2. Sichtbare Fehler müssen weg: Facetten, Kanten, Klippenbeulen, Flecken, Streifen.
3. Priorität hat, was im Nahbild auffällt. P4 (QA: echt oder Prüfartefakt) ist der Hauptfilter.
4. Abnahme ist die Sichtprüfung aller 56 Kacheln (P8/P9), nicht die Trefferzahl allein.
5. Schwellen und Prüfer werden nicht geändert. Eine Ausnahme ersetzt keinen Prüfer, sie dokumentiert nur einen unsichtbaren Treffer.

## Ausgangsstand [S]
- Gate-Befehl (Ordner `team/art/dorfmap_grundgeruest/relief3d`):
  `NODE_PATH=/tmp/w3/node_modules HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js && sh pruefung/export_gate.sh`
  Laufzeit: Lochscan 2,8 s, Gate 10,4 s (gemessen 16.11. 07:2x Uhr MEZ). Ohne `NODE_PATH` scheitert der Lochscan (playwright fehlt) und das Gate zählt 571 statt 570 (`G1_lochscan_fehlt`). `export_gate.sh` nutzt eine vorhandene `/tmp/gate_loch.json` ungeprüft weiter; nach jeder Reliefänderung vorher löschen oder pro Lauf eigene Datei (`LOCHSCAN=…`) verwenden.
- Reproduziert: pruefe_regeln **570** (identisch zu `regeln_letzter_lauf.json` aus 31d2c97, alle Einzeltreffer gleich), r8 **48** (R8_stufe 9, R8_gitter 10, R8_quer 5, R8a_wegende 24), r9 **334** (R8b_delle 25, R9_saegezahn 34, R9w_wellen 275). r8-JSON hat nur neue Felder `limit_m`/`ausnahme`, Zählung gleich.
- Geschützte Eingaben (SHA-256): `neu/zellen_relief.csv` 99d30e55…, `neu/vektor.json` aac6afff…, `neu/felder.json` e4e2ec8f…, D2-Höhe 749d3c4b… (seit p3d25 89c61ce unverändert).
- Ohne Treffer in pruefe_regeln: A4, A5, A6, F3, G7. Auch ohne r8/r9-Treffer: nur A4, A5, F3, G7 (A6 hat 5× R9w).
- Kartenweit ohne Kachelbezug (6): T2–T5 Bildprüfung offen (je 1), G7b Rauheit 1, G7b Kantenschärfe 1.

## Kacheln (56) [S]
Spalten = Treffer je Regelfamilie aus dem Gate (pruefe_regeln; R8/R8a aus r8, R8b/R9/R9w aus r9). „Zahl 0, Sicht offen“ = keine Treffer, Sichtprüfung P8 steht aus. Bestanden ist eine Kachel erst nach P8.

| Kachel | G2/G3 | G5 | G6 | G7/G7b/G8 | R3 | R5 | R1 | R2 | R6 | T1 | R8/R8a | R8b/R9/R9w | Summe Gate | Status | Zuständig |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 0 | 0 | 4 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 9 | offen | Grundgerüst |
| B1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 3 | 8 | offen | Grundgerüst, Wege & Deko |
| C1 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 5 | 12 | offen | Grundgerüst, Wege & Deko |
| D1 | 0 | 1 | 5 | 0 | 27 | 0 | 2 | 1 | 0 | 0 | 8 | 26 | 70 | offen, vorläufig gesetzt | Grundgerüst, Wege & Deko |
| E1 | 0 | 0 | 7 | 1 | 2 | 0 | 1 | 0 | 0 | 2 | 1 | 8 | 22 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| F1 | 1 | 4 | 4 | 0 | 2 | 0 | 1 | 1 | 1 | 2 | 1 | 7 | 24 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| G1 | 1 | 0 | 4 | 0 | 1 | 0 | 1 | 0 | 3 | 3 | 1 | 8 | 22 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| H1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 9 | offen | Grundgerüst |
| A2 | 0 | 2 | 2 | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 7 | 16 | offen | Grundgerüst |
| B2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 8 | offen | Grundgerüst |
| C2 | 0 | 0 | 3 | 1 | 0 | 0 | 1 | 0 | 0 | 2 | 1 | 4 | 12 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| D2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7 | 0 | 0 | 8 | offen (bitgleich gesperrt) | Wege & Deko, Art Umgebung |
| E2 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 14 | offen | Grundgerüst, Art Umgebung |
| F2 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 3 | 9 | offen | Grundgerüst, Art Umgebung |
| G2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 3 | 0 | 0 | 4 | offen | Wege & Deko, Art Umgebung |
| H2 | 2 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 6 | 15 | offen | Grundgerüst, Art Umgebung |
| A3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | offen | Art Umgebung |
| B3 | 0 | 0 | 7 | 1 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 7 | 20 | offen | Grundgerüst, Art Umgebung |
| C3 | 0 | 18 | 15 | 1 | 8 | 1 | 1 | 1 | 0 | 0 | 4 | 19 | 68 | offen | Grundgerüst, Wege & Deko |
| D3 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 3 | 0 | 2 | 13 | offen | Grundgerüst, Art Umgebung |
| E3 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 3 | 0 | 12 | 21 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| F3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Zahl 0, Sicht offen | Kritiker (P8) |
| G3 | 0 | 1 | 7 | 0 | 1 | 0 | 1 | 0 | 0 | 4 | 3 | 11 | 28 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| H3 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 9 | 13 | offen | Grundgerüst, Art Umgebung |
| A4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Zahl 0, Sicht offen | Kritiker (P8) |
| B4 | 3 | 0 | 15 | 1 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 12 | 34 | offen | Grundgerüst, Art Umgebung |
| C4 | 0 | 4 | 16 | 1 | 2 | 4 | 2 | 2 | 0 | 1 | 2 | 15 | 49 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| D4 | 0 | 4 | 6 | 1 | 10 | 0 | 2 | 0 | 0 | 0 | 2 | 7 | 32 | offen | Grundgerüst, Wege & Deko |
| E4 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 8 | 17 | offen | Grundgerüst, Art Umgebung |
| F4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 3 | offen | Wege & Deko, Art Umgebung |
| G4 | 0 | 7 | 8 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 6 | 22 | offen | Grundgerüst, Wege & Deko |
| H4 | 0 | 0 | 3 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 4 | 6 | 17 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| A5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Zahl 0, Sicht offen | Kritiker (P8) |
| B5 | 0 | 0 | 13 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 11 | 26 | offen | Grundgerüst, Art Umgebung |
| C5 | 1 | 14 | 17 | 1 | 4 | 6 | 3 | 1 | 0 | 1 | 5 | 12 | 65 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| D5 | 0 | 0 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11 | 15 | offen | Grundgerüst |
| E5 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | offen | Grundgerüst |
| F5 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 14 | offen | Grundgerüst, Art Umgebung |
| G5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 4 | offen | Art Umgebung |
| H5 | 0 | 0 | 10 | 1 | 1 | 0 | 2 | 1 | 0 | 4 | 5 | 12 | 36 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| A6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 5 | offen | Grundgerüst |
| B6 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 | 7 | offen | Grundgerüst, Art Umgebung |
| C6 | 0 | 0 | 6 | 1 | 0 | 0 | 1 | 0 | 0 | 3 | 3 | 19 | 33 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| D6 | 1 | 0 | 4 | 0 | 8 | 2 | 0 | 1 | 0 | 0 | 4 | 12 | 32 | offen | Grundgerüst, Wege & Deko |
| E6 | 0 | 0 | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 5 | 11 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| F6 | 0 | 1 | 3 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 8 | 16 | offen | Grundgerüst, Wege & Deko |
| G6 | 2 | 0 | 6 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 8 | 19 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| H6 | 0 | 1 | 9 | 1 | 1 | 0 | 1 | 0 | 0 | 5 | 1 | 11 | 30 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| A7 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 6 | offen | Grundgerüst |
| B7 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | offen | Grundgerüst |
| C7 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 3 | 7 | offen | Grundgerüst, Wege & Deko, Art Umgebung |
| D7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | offen | Grundgerüst |
| E7 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | offen | Grundgerüst |
| F7 | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | offen | Grundgerüst |
| G7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Zahl 0, Sicht offen | Kritiker (P8) |
| H7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 | offen | Grundgerüst |
| **Summe** | 16 | 68 | 220 | 26 | 80 | 17 | 24 | 15 | 4 | 94 | 48 | 334 | 946 | | |

D2: Höhen bleiben bitgleich gesperrt (Regressionsbasis). R2 1 und T1 7 in D2 nur über Weg-/Texturdaten lösen, ohne D2-Höhen zu ändern; geht das nicht, Ausnahmeliste.

## D1-Regel
D1 bleibt **vorläufig** im aktuellen Relief (`neu/zellen_relief.csv` 99d30e55) gesetzt. Vermerk: „vorläufig, Reststellen 4,5 mm Stufe rampe_11-Start 0,0585 statt 0,054 m und 57 mm festes Randpaar E1 [171,25|24,75]–[171,5|24,75], p3d36/p3d37“. D1 läuft im globalen Lauf normal mit, ohne Sonderbehandlung. Das Feinrechnen p3d16–p3d38 ist beendet (Fabian t172u). Beide Reststellen sind Millimeterstufen und gehen nach Lieferregel 1 mit Nahbild in die Ausnahmeliste, wenn P4 sie als unsichtbar bestätigt [A].

## Arbeitspakete
| Nr | Inhalt | Pfad | Abnahmekriterium | Zuständig |
|---|---|---|---|---|
| P1 | Höhen global, Codex-Läufe L1 (heute) und L2 (18./19.11.), je ≤ 2 h, ein Ziel, kein Feinrechnen je Punkt. Gewichtung: zuerst sichtbar (G6 Facetten, G5 Klippenbeulen, G2/G3 Spitzen, R5 Löcher), dann R3/G7b/R9w. | `relief3d/`, Bericht `relief3d/pruefung/ERGEBNIS_L1.md`, `ERGEBNIS_L2.md`, Branch `art/dorfmap-L1`/`-L2` | Keine Familie mehr Treffer als vorher, G6/G5/G2/G3/R5 deutlich gesenkt, D2 bitgleich (749d3c4b), Grundriss/Wege/Wasser/Klippenkonturen unverändert. Scheitert eine Stelle zweimal: einfachere Geometrie oder Ausnahme. | Dorfmap-Grundgerüst (Codex) |
| P2 | Wegnetz: R1 blind 24, R2 getrennt 15, R6 Wasser/Schnee 4 | `relief3d/neu/vektor.json` | R1 = R2 = R6 = 0, keine neuen R3/R8/R8a-Treffer, D2-Höhen bitgleich | Wege & Deko |
| P3 | Texturen: T1 Fleckrand 94 plus Bildprüfungen T2–T5 | `relief3d/gen_textur.py`, `relief3d/neu/` (Texturteil) | T1 = 0, T2–T5 bestanden mit Nahbild je betroffener Kachel, Höhen unberührt | Art Umgebung |
| P4 | Hauptfilter Sichtbarkeit: G6/G5 je 5 Treffer in C5, C3, C4, D4, B4 mit Nahbild, Urteil „sichtbar“ / „unsichtbar“ / „Prüfartefakt“; danach alle übrigen Familien nach gleichem Muster | `relief3d/pruefung/sichtfilter/` | Je Treffer Nahbild + Urteil + Messwert; Schwellen unverändert. Unsichtbare gehen als Antrag in die Ausnahmeliste | QA |
| P5 | Unabhängige Nachzählung des Gate-JSON nach jedem Lauf; Prüfrechnungen für jede Ausnahme | `relief3d/pruefung/nachzaehlung/` | Eigene Zählung = Gate-Zählung je Regel und Kachel; Messwert jeder Ausnahme nachgerechnet | Rechner |
| P6 | Trefferkarte 8×7 mit Treffern je Kachel aus den Gate-JSONs | `relief3d/pruefung/trefferkarte/` (Skript + HTML/PNG) | Zahlen = Tabelle oben; nach jedem Lauf neu erzeugbar mit einem Befehl | Dev UI |
| P7 | Gate-Beschleunigung, z. B. nur betroffene Kacheln | `relief3d/pruefung/gate_schnell/` | Gleiche Zählung wie volles Gate. Niedrige Priorität: volles Gate dauert nur ~13 s [S] | Tools |
| P8 | Sichtprüfung aller 56 Nahbilder nach L2 | `relief3d/pruefung/sicht_p8/` | Je Kachel „sauber“ oder Liste sichtbarer Fehler mit Ort | Kritiker |
| P9 | Endabnahme: volles Gate kartenweit, Ausnahmeliste vollständig, P8 alle sauber, Lieferung an Fabian | `relief3d/pruefung/ERGEBNIS_ENDE.md` | Alle sichtbaren Fehler weg; jeder Resttreffer steht mit Nahbild in der Ausnahmeliste | Dorfmap-Grundgerüst |

## Ausnahmeliste (gilt ab 16.11. 07:15 [F])
Nur Treffer, die P4 als mit bloßem Auge unsichtbar belegt. Messwert von P5 nachgerechnet.

| Stelle | Regel | Messwert | Schwelle | Nahbild | Begründung |
|---|---|---|---|---|---|

## Zeitplan
| Datum | Schritt |
|---|---|
| 16.11. | L1 (≤ 2 h), Start P2–P7 parallel |
| bis 18.11. | P2–P7 fertig, PRs auf `art/dorfmap-fertig` |
| 18./19.11. | L2 (≤ 2 h) auf dem Stand nach P2/P3/L1 |
| 20.11. | P8 Sichtprüfung, P9 Gate |
| **21.11.2026** | **Zieldatum gesamte Karte [A]** |

Begründung [S/A]: Das Gate läuft in ~13 s, also sind viele Prüfdurchläufe pro Tag möglich; der Engpass ist nicht die Prüfung, sondern Codex-Zeit (ein Exec gleichzeitig) und Sichtprüfung. Darum bleibt 21.11. realistisch. Risiko: P2 (Wegänderung) kann R3/R8 verschieben; deshalb läuft L2 nach P2.

## Arbeitsregel für andere Bots
- Eigener Branch von `art/dorfmap-fertig`, Lieferung als PR auf `art/dorfmap-fertig`. Nichts nach main.
- Gate-Zahlen (pruefe_regeln, r8, r9 je Regel und Kachel, vorher/nachher) liegen jeder PR bei.
- Keine neuen Treffer in fremden Familien. D2-Höhen bitgleich, Schwellen und Prüfer unverändert.
- Nichts löschen, alte Dateien per `git mv` nach `_alt/`. Keine Secrets.
- Nur ein Codex-Exec gleichzeitig auf der Box; Vorrang hat P1.
