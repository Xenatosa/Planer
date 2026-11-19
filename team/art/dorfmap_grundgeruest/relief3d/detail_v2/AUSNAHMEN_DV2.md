# AUSNAHMEN_DV2 – Ausnahmeliste detail_v2 (Bodenkamera 1,7 m)

Regel (Fabian 16.11.2026, t2029u): Eine Ausnahme gilt nur, wenn die Stelle mit bloßem Auge unsichtbar ist. Dann wird sie mit Messwert und Nahbild geführt und blockiert die Lieferung nicht. Sichtbare Fehler müssen weg. Entschieden wird in der P6-Sichtprüfung.

| ID | Stelle | Prüfung | Messwert | Status | Nahbild |
|---|---|---|---|---|---|
| A-DV2-01 | 52 runde Wegenden (`wege.geojson` #59), Flächentyp-Grenze Weg/Grund | Q3 (1-m-Mittel ≤ 3,0 cm) | bis 9,01 cm (QA) / 5,63 cm (fein) [S]; ein Wegende mit 2,3 m Breite kann Q3 rechnerisch nicht halten: Für r ≥ 1,6 m (fein) bzw. ≥ 2 m (QA) braucht es eine Breite von 3,2 m bzw. 4 m [R] | **Kandidat**: Entscheid in P6 bei 1,7 m. Sichtbar → andere Endgeometrie statt Ausnahme | folgt in P6 |
| A-DV2-01 (F15) | 98 Abschnitte an Wegenden in 10 Zonenringen (`zonen` @ bf9f62d), Gruppe „sonst“ | Q3 Zonenringe | 3,0–4,8 cm, Knick ≤ 15°, ganzer Abschnitt ≤ 3 m vor einem Wegende [S] (QA R6/R7, `qa/gegenprobe/R6_zonen_bf9f62d.md`) | **Kandidat**: gleiche Ursache wie A-DV2-01; Entscheid in P6 bei 1,7 m | folgt in P6 |
| A-DV2-01 (F16) | 13 Abschnitte `stoss_nah` in 6 Zonenringen (00011, 00012, 00015, 00018, 00037, 00052), außerhalb ±0,5 m um Stoßpunkte | Q3 Zonenringe | 3,0–4,8 cm, Knick ≤ 10,1°, 0,96–1,48 m vor einem Wegende [S]; Ursache: Wegendkurve beginnt direkt am Stoßpunkt, bei 2,3 m Breite nicht rundbar [R]; Liste mit Koordinaten in `qa/gegenprobe/R6_zonen_bf9f62d.md` (Runde 7) | **Kandidat**: Entscheid in P6 bei 1,7 m. Sichtbar → P2 bekommt andere Endgeometrie | folgt in P6 |

Nicht in dieser Liste, weil Mess-Ausschluss statt Ausnahme: Kartenrand und ±0,5 m um Stoßpunkte (F11/F13) sowie das P5-Eckfenster der Brücken (F17: ±0,5 m um die 4 Deckend-Ecken je Brücke, Knick und Abweichung frei, Längsseiten hart, Regel aus bis P5). Die Brückenzonen (F14, 13 Ringe) sind offener Befund „P5“, keine Ausnahme.
