# Ergebnisbericht – Regelwerk Landschaft (regelwerk)

Stand: 03.11.2026 · Vergleichsbasis: `9d3f8fc` · Branch: `art/dorfmap-regelwerk`

## Änderung

- Neu: `REGELWERK_LANDSCHAFT_VOLLSTAENDIG.md` mit Sollformen, Kartenmaßen `[S]/[R]`, Platzhaltern `[A]`, messbaren Grenzwerten, Messskript-Zuordnung, Ist-Verteilungen und 56 Kachelzeilen A1–H7.
- Neu: `pruefung/regelwerk_messung.py`, ein reproduzierbares, lesendes Python-Messskript für Gelände-, Übergangs-, Weg-, Wasser- und Objektverteilungen sowie die Kachelbelegung.
- Ergänzt: ein Verweis am Ende von `REGELN_VERPFLICHTEND.md`.
- Keine Höhen-, Zell-, Overlay- oder Reliefdaten geändert. Kein bestehendes Prüfskript geändert. Das neue Skript schreibt nur seine angeforderte JSON-Ausgabe.

## Regelzahlen vorher/nachher

Die Prüfungen wurden auf Datenstand `9d3f8fc` und auf dem unveränderten Relief dieses Branches ausgeführt. Alle Werte sind identisch; Δ = 0 je Regel. `pruefe_regeln.py`, `r8_kreuzung.py` und `r9_form.py` liefern wegen ihrer gezählten Treffer Exitcode 1. Die Trefferzahlen sind der dokumentierte Ausgangsbefund, keine Bestätigung der Soll-Einhaltung.

| Prüfgruppe | Regel | Vorher (`9d3f8fc`) | Nachher (`regelwerk`) | Δ |
|---|---|---:|---:|---:|
| Regeln | `R1_blind` | 24 | 24 | +0 |
| Regeln | `R1_wand` | 0 | 0 | +0 |
| Regeln | `R1_wasser` | 0 | 0 | +0 |
| Regeln | `R2_getrennt` | 15 | 15 | +0 |
| Regeln | `R3_laengs_m` | 35 | 35 | +0 |
| Regeln | `R3_quer_pct` | 23 | 23 | +0 |
| Regeln | `R3_woelb_m` | 22 | 22 | +0 |
| Regeln | `R4_rand` | 0 | 0 | +0 |
| Regeln | `R4_schlucht` | 0 | 0 | +0 |
| Regeln | `R5_loch` | 17 | 17 | +0 |
| Regeln | `R5_spitze` | 0 | 0 | +0 |
| Regeln | `R6_objekt_auf_weg` | 0 | 0 | +0 |
| Regeln | `R6_wasser_schnee` | 4 | 4 | +0 |
| Regeln | `R7_trennung` | 0 | 0 | +0 |
| Regeln | `G1_loch_offen` | 0 | 0 | +0 |
| Regeln | `G1_lochscan_fehlt` | 0 | 0 | +0 |
| Regeln | `G2_spitze_oben` | 3 | 3 | +0 |
| Regeln | `G3_spitze_unten` | 3 | 3 | +0 |
| Regeln | `G2_spitze_oben_fein` | 8 | 8 | +0 |
| Regeln | `G3_spitze_unten_fein` | 2 | 2 | +0 |
| Regeln | `G4_delle_beule` | 0 | 0 | +0 |
| Regeln | `G5_beule_klippe` | 66 | 66 | +0 |
| Regeln | `G6_facette` | 249 | 249 | +0 |
| Regeln | `G7_wand_glatt_gesamt` | 0 | 0 | +0 |
| Regeln | `G7_wand_glatte_flaeche` | 1 | 1 | +0 |
| Regeln | `G8_fluss_nicht_bis_rand` | 1 | 1 | +0 |
| Regeln | `G8_fluss_flach` | 0 | 0 | +0 |
| Regeln | `G11_objekt_schwebt_sinkt` | 0 | 0 | +0 |
| Regeln | `G11_baum_an_wand` | 0 | 0 | +0 |
| Regeln | `T1_harte_farbkante` | 0 | 0 | +0 |
| Regeln | `T1_harte_farbkante_gerade` | 0 | 0 | +0 |
| Regeln | `T1_fleckrand` | 94 | 94 | +0 |
| Regeln | `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | +0 |
| Regeln | `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | +0 |
| Regeln | `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | +0 |
| Regeln | `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | +0 |
| Regeln | `T6_wasser_in_schnee_farbe` | 0 | 0 | +0 |
| Regeln | `T_VC_format` | 0 | 0 | +0 |
| Regeln | `G7b_wandkontur_rauheit` | 1 | 1 | +0 |
| Regeln | `G7b_wandkontur_kantenschaerfe` | 1 | 1 | +0 |
| Regeln | `G7b_wandkontur_feld` | 23 | 23 | +0 |
| Alias | `G9 (= R6_wasser_schnee)` | 4 | 4 | +0 |
| Alias | `G10 (= R5_loch)` | 17 | 17 | +0 |
| **Regeln Summe** |  | **596** | **596** | **+0** |
| R8 | `R8_stufe` | 9 | 9 | +0 |
| R8 | `R8_gitter` | 10 | 10 | +0 |
| R8 | `R8_quer` | 5 | 5 | +0 |
| R8 | `R8a_wegende` | 24 | 24 | +0 |
| **R8 Summe** |  | **48** | **48** | **+0** |
| R9 | `R8b_delle` | 25 | 25 | +0 |
| R9 | `R9_saegezahn` | 34 | 34 | +0 |
| R9 | `R9w_wellen` | 275 | 275 | +0 |
| **R9 Summe** |  | **334** | **334** | **+0** |

G9/G10 sind im vorhandenen Prüfskript als Aliasregeln für R6/R5 dokumentiert; ihre Zeilen wiederholen dieselben Treffer und sind nicht zusätzlich zur Gruppensumme zu zählen. Nicht ausgegebene Regeln stehen mit 0 Treffern.

## D1, G1 und D2

| Prüfgruppe | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
|---|---:|---:|---:|
| Regeln | 36 → 36 | 13 → 13 | 8 → 8 |
| R8 | 8 → 8 | 1 → 1 | 0 → 0 |
| R9 | 26 → 26 | 8 → 8 | 0 → 0 |

D2-Regeln: `pruefe_regeln.py` enthält weiterhin 8 Treffer (1 × `R2_getrennt`, 7 × `T1_fleckrand`); `r8_kreuzung.py` und `r9_form.py` enthalten weiterhin 0 Treffer. In D2 ist kein Treffer hinzugekommen. Keine Regel steigt; damit bleibt jede Änderung deutlich innerhalb der zulässigen +5.

## Bau und Prüfungen

| Schritt | Ergebnis |
|---|---|
| `python3 gen_relief.py && python3 baue_html.py` | Erfolgreich, Exitcode 0 |
| `loch_o18g.js` mit `RAND=0.6` | Exitcode 0; 7 Meshes, 1 700 454 Dreiecke, `offen_innen=0`, `punkte=0` |
| LOD1-Dreieckszähler | 1 174 328 Dreiecke; Grenzwert <1 300 000 erfüllt |
| `pruefe_regeln.py` | 596 Treffer; 0 Ausnahmen; Werte wie oben |
| `r8_kreuzung.py` | 48 Treffer: Stufe 9, Gitter 10, quer 5, Wegende 24 |
| `r9_form.py` | 334 Treffer: Delle 25, Sägezahn 34, Wellen 275 |
| `pruefe_t42u.py` | Summe 0 |
| `regelwerk_messung.py` | Erfolgreich; 56 Kacheln, Verteilungen nach JSON ausgegeben |

Die Loch-, R8- und R9-Zahlen stimmen mit dem vorgegebenen Ausgangswert überein. Die bestehenden Regel-Treffer bleiben offen; dieser Dokumentationsauftrag ändert keine Geometrie und beseitigt keine Treffer.

## Annahmen, Grenzen und offene Punkte

- Das Messskript wertet das sichtbare Höhenfeld `GB`, das Wasserfeld `WV`, `zellen_relief.csv` und serialisierte Wege/Objekte aus `relief_daten.json.gz` aus. Verteilungen sind P5/Median/P95. Der Krümmungsradius wird nur für `|Krümmung| ≥ 0,02 1/m` ausgewiesen.
- Die Master-Dorfkarte-PNG fehlt im Worktree. Bildmaße wurden aus den dokumentierten Rechnungen in `SPEC.md` und `ABWEICHUNGEN.md` übernommen; neue Bildmessungen sind offen. Der ältere SPEC-Stand (+8,6/+6,7 m) widerspricht dem späteren Relief-/Wandhöhenstand (+14/+12 m); das Regelwerk verwendet den späteren Stand und dokumentiert den Konflikt. `GB`-Mediane der unmarkierten Plateauzellen: Nord 13,9995 m (9 917 Zellen), Ost 11,9993 m (4 227 Zellen).
- Kreuzungen, Gabelungen und Kehren werden für die Kachelmatrix über feste geometrische Kandidatendetektoren (Linienabstand, 4-Nachbargrad und Richtungsänderung ≥90°) zugeordnet. Ohne Master-PNG ist das keine fachliche Sichtklassifikation.
- Objektparameter im JSON sind nicht durchgängig Mesh-Bounding-Boxen. Baum-, Deko-, Fels-, Findlings- und Gebäudemaße sind deshalb teils Soll-Platzhalter; Größen- und Kontaktgates sind im Bericht als noch erforderlich ausgewiesen. Felsblöcke haben aktuell 0 Instanzen.
- Der Südfluss hat einen Kartenmaß-Widerspruch: 7,4–10 m aus der Zeichnung gegenüber 2,5 m aus der Schutzmaske. Das Regelwerk verwendet das Kartenmaß und markiert die Messabweichung.
- Das Regelwerk setzt Grenzwerte; viele der neuen Grenzwerte besitzen noch kein ausführbares Prüfgate. Der Bericht erfindet keine Einhaltung: aktuelle Ist-Werte überschreiten unter anderem Hang-Neigungs-P95 39°, Ufer-Neigungs-P95 35° und den Findlings-Kartendurchmesser. Die zuständigen fehlenden Gates sind je Element genannt.
- T1–T6 sind keine Formregeln und bleiben wegen der Vorgabe „nur Form, Geometrie und Masse“ außerhalb des Formkatalogs.
