# ERGEBNIS P1a – dv2 Weg- und Kreuzungsvektoren (Branch art/dv2-vektor-wege)

Kosten: 0 € · Codex: nein · Laufzeit: 14:45–15:23 (Europe/Berlin, 19.11.2026)

Plan: DETAIL_V2_PLAN.md 3.1, 5, 9 (P1a). Basis art/dorfmap-fertig d2d4824. Nur neue Dateien in detail_v2/vektor/, keine bestehende Datei geändert.

## PLAN (vorab, mit Zwischenzielen)
1. [S] Quelle lesen: neu/vektor.json (wege, kreuzungen) /1,2 → Zellen = Viewer-Meter; WEGA ≥ 0,5 als Gegenprobe; Lage prüfen (Versatz 0 passt am besten).
2. [S] Mittellinien: DP 0,05 m → zentripetaler Catmull-Rom → 0,25 m abgetastet. Zwischenziel: Knick/Zacken/Abweichung messen.
3. [S] Ränder als Offset ±Breite/2 (shapely-Band), Kreuzungen ins Bandnetz einpassen, Chaikin 2×. Zwischenziel: alle Ränder ≤ 3 cm / ≤ 15°.
4. [S] Wegenden an Plätze/Kreuzungen anschließen, Netz gegen WEGA auf Lücken prüfen. Zwischenziel: keine offenen Enden, ein Netzteil je WEGA-Komponente.
5. [R] test_wege.py (unabhängige Messung) + Übersichtsbild, altes Gate als Regressionsnachweis, PR.

## Gescheiterte Ansätze → Ursache → Methodenwechsel [A]
| Ansatz | Ursache | Wechsel |
|---|---|---|
| DP + CR direkt auf der Quelle: Zacken 0,17 m, Knick 78° | Quelle ist ein Zellmitten-Polygonzug mit 45°-Stufen und ~100°-Wenden auf 3 m; CR interpoliert die Treppe | Gauß-Vorglättung längs der Bogenlänge vor DP+CR, σ = größter Wert aus 1,5…0 m, bei dem die **fertige** Linie ≤ 0,25 m vom alten Verlauf bleibt |
| Reiner Offset ±b/2: Spitzen am Innenrand enger Kurven | Krümmungsradius < b/2 | Band schließen (r 2,2 m) + zyklische Ringglättung σ 0,3 m |
| Schließen bei U-/Schleifenwegen (G015, G018): Band wird Klumpen, Innenrand fehlt | Schließen füllt den Innenraum bzw. die Mündung zwischen Wegende und eigenem Schenkel | Füllflächen breiter als 2·1,7 m und Mündungsfüllungen an der eigenen Endkappe wieder freigeben; je Weg größtes r/kleinstes σ mit Eigenprüfung |
| Kreuzung = P ∩ Netz, Runden r 2 m, Rückfall „P + 2 m“: 26/88 im Rückfall, Überstand bis 2,4 m | vektor.json-Polygone oft schmaler als 2r (z. B. 1 m-Rechtecke), Runden löscht sie | Suche über Erweiterung e 0–2 m, Saum 0–1 m, r 2,0/1,85 m: kleinster Überstand bei ≥ 90 % Abdeckung von P ∩ Netz |
| Kreuzung mit r 1,5 m (weniger Überstand) | Zacken 3,37 cm > 3 cm (Kreisbogen r gegen 1-m-Mittel ≈ 5 cm/r) | r ≥ 1,85 m behalten, Überstand als Restrisiko melden |

## Dateien
- wege.geojson – 61 Wegteile (58 aus vektor.json + 3 WEGA-Ergänzungen) je mit mittellinie, rand_links, rand_rechts, band; dazu 1 Feature netz (Union Bänder + Kreuzungen). Einheit Viewer-Meter, Achsen [x Ost, z Süd].
- kreuzungen.geojson – 88 Kreuzungsplatten (50 weg_platz, 38 weg_kreuzung) mit weg_ids, platz_ids, hoehe_m_quelle, einpassung {r, erweiterung, saum, ueberstand_m}.
- extrahiere_wege.py – Extraktor (`python3 detail_v2/vektor/extrahiere_wege.py` aus relief3d/, ~2,5 min, deterministisch).
- test_wege.py – Abnahmetest (`python3 detail_v2/vektor/test_wege.py --json detail_v2/vektor/test_wege_ergebnis.json`, Exit 0 = bestanden; `--bild …jpg` zeichnet die Übersicht).
- test_wege_ergebnis.json – Messwerte des letzten Laufs.
- uebersicht_wege.jpg – links ganze Karte, rechts Dorfkern 180–240 | 95–140; Hintergrund alte Draufsicht (VC, WEGA ≥ 0,5 rot), Ränder schwarz, Mitte gelb, Kreuzungen blau, Ergänzungen magenta.

## Messwerte (test_wege.py: bestanden)
| Prüfung | Wert | Schwelle |
|---|---|---|
| Zacken max, 122 Randlinien | **2,89 cm** (G018/0 rand_rechts), p95 2,39 cm | ≤ 3 cm |
| Knick max, Randlinien | **8,59°** (G018/0), p95 7,21° | ≤ 15° |
| Zacken / Knick max, 88 Kreuzungsumrisse | 2,74 cm (K024) / 7,86° (K046) | ≤ 3 cm / ≤ 15° |
| sichtbarer Teil (außerhalb anderer Bänder/Kreuzungen) | 2,73 cm / 8,05° | |
| Mittellinie zum alten Verlauf (Hausdorff, beidseitig) | **0,246 m** (G018/0) | ≤ 0,3 m |
| WEGA-Ergänzungen: Abstand zu WEGA-Knoten | max 0,333 / 0,25 / 0,315 m | – |
| Lücken: offene Wegenden | **0** | 0 |
| Netzteile / WEGA-Komponenten | **2 / 2**, keine WEGA-Komponente mit > 1 Netzteil | 1 je Komponente |
| WEGA-Knoten außerhalb Netz (+0,25 m) | 194 von 14 258 (Abdeckung 98,64 %), größter Cluster 19 Knoten | – |
| Platzanschluss (Wegende ≤ 1,5 m an Platz) | 30/30 angeschlossen, min Überlappung 0,087 m² | ≥ 0,05 m² |
| Randvollständigkeit | je Weg genau 1 Rand links + 1 rechts, min Randlänge/Mittellinie 0,49 (Innenrand enger Kurve), Bandfläche ≤ 1,044 × Soll | ≥ 0,4, ≤ 1,15 |
| Kreuzungs-Überstand über Netz/Platz | max 1,39 m (K063), Median 0,60 m | ≤ 1,5 m |
| Rand gegen Offset ±b/2 | Median 0,3 cm, p95 6,8 cm, max 1,17 m (Innenrundung) | – |
| shapely is_valid | alle | alle |

## Gate-Regression (alte Prüfer, Ausgabe nach /tmp)
| Prüfer | Lauf | Basis d2d4824 | Repo-Referenz |
|---|---|---|---|
| pruefe_regeln.py | 360 | 360 (Treffer identisch) | 359 |
| r8_kreuzung.py | 31 (21 Kreuzungen) | – | 31 |
| r9_form.py | 321 | – | 321 |

**Korrektur (19.11., Aufseher):** Die 360 stammen aus dem direkten Aufruf von pruefe_regeln.py ohne LOCHSCAN. Über export_gate.sh mit GATE_LOCH_JSON ergeben d2d4824 und dieser Stand 359. Siehe ERGEBNIS_P1a2.md. Ursprünglicher Text: Die +1 bei pruefe_regeln ist `G1_lochscan_fehlt` (Umgebungsprüfung, Lochscan-Datei fehlt in /tmp) und tritt auf der unveränderten Basis d2d4824 genauso auf. `git diff d2d4824 --stat`: nur neue Dateien unter detail_v2/vektor/.

## Entscheidungen Dorfmap (19.11., nach Review #56)
- Kreuzungsüberstand bis 1,5 m ok (R8 eben gilt darin); E2-Lücke → Brückenmodul P5; Wegenden bleiben ungekürzt; ERG01–03 ok.
- QA Q3 (gleitendes 1-m-Mittel über die Stützpunkte) fand Zacken > 3 cm → Nachbesserung siehe ERGEBNIS_P1a2.md (dort auch neue Messwerte; die Werte oben sind Stand #56).

## Vereinfachungen / Restrisiken
- WEGA aus relief_daten.json.gz (Gitter rs = 2, A ≥ 128), nicht aus index.html: index.html trägt nur D1/D2/G1-Payload. Gleicher Datenstand.
- 4 Ein-Punkt-Teilstücke ausgelassen (G002_anb/0, G008/2, G010/2, G014/1, < 0,5 m Skelettreste); abgedeckt über Kreuzungen.
- 3 WEGA-Ergänzungen (ERG01 HAUSWEG 19,2 m bei 189–197 | 113–126, ERG02 GASSE 6,5 m E3-Brücke, ERG03 ANBINDUNG 6,1 m bei G002_anb) schließen WEGA-Verbindungen, die vektor.json nicht hat (Netz hatte sonst 5 Teile). Breite = nächste Klassenbreite.
- E2-Brücke: über dem Wasser ist WEGA = 0, deshalb 2 Netzteile wie 2 WEGA-Komponenten; Lückenschluss gehört zum Brückenmodul.
- Kreuzungsplatten stehen bis 1,39 m (Median 0,60 m) über Bandnetz/Platz: Eckradius ≥ 1,85 m ist nötig für Zacken ≤ 3 cm, die Wege sind 2–3 m breit.
- Einige Wegenden laufen wie in vektor.json bis ~5 m über WEGA hinaus in Plätze/Häuser (Quelle übernommen, nicht gekürzt).
- Zacken-Reserve klein (2,89 cm bei G018/0); die Zacken-Messung erfasst auch echte Krümmung (Kreisbogen r gegen 1-m-Mittel ≈ 5 cm/r), deshalb Innenradien ≥ ~1,7 m.
- Keine Texturen, keine Höhen (Kreuzungshöhe nur als hoehe_m_quelle durchgereicht).
