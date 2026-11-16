# QA P4: Stichprobe G6_facette / G5_beule_klippe, Ausgangsstand 8e374b0

Stand 16.11.2026, QA (Epochen QA). Basis `art/dorfmap-fertig` @ 8e374b0. Schwellen und Prüfer sind unverändert.
Urteil „ja“ heißt: in der Spielansicht als echter Fehler sichtbar. „nein“ heißt: unsichtbar, verdeckt oder Prüfartefakt.
Urteilsgrundlage ist Bild A (Spielkamera flach, aus Süden wie die Startansicht „schräg“, 35°, 35 m, Textur). B (60°, 16 m, Textur) und C (60°, 16 m, Clay) zeigen die Form, `_nah` (35°, 15 m) gibt es nur für Zweifelsfälle.

## Fazit

**Sichtbar: 13 von 43 Stichproben (30 %).** G6: 5/25 (20 %), G5: 8/18 (44 %).

| Regel | gesamt | C5 | C3 | C4 | D4 | B4 |
|---|---|---|---|---|---|---|
| G6_facette | **5/25** | 0/5 | 1/5 | 4/5 | 0/5 | 0/5 |
| G5_beule_klippe | **8/18** | 2/5 | 1/5 | 3/4 | 2/4 | – |

Die 13 „ja“-Treffer sind **8 physische Stellen**, weil mehrere Treffer dieselbe Stelle markieren:
1. **C4 Plateauränder mit Treppenstufen neben Häusern**, 4 Stellen: (112,7–120,5 | 165,5–168) mit G6_C4_1 und G5_C4_1/3/4, dazu (96,3 | 164,4) G6_C4_3, (116,4 | 136,7) G6_C4_4 und (120,4 | 156,6) G6_C4_5. Das ist die klar häufigste sichtbare Fehlerart. Dieselben Treppenränder sind auch in den C5-Bildern sichtbar (z. B. G6_C5_1/4, linke Bildhälfte), dort allerdings nicht am Trefferpunkt.
2. **C5 Horn/Zacken an der Klippenkante** neben dem Baum (123,5–124 | 186–189): G5_C5_2/3.
3. **C3 scharfe Gratfinne** (114,8 | 120,7): G6_C3_2.
4. **C3 runder Buckel mit Ringmulde im Dorfplatz** (125,5 | 96,2): G5_C3_1.
5. **D4 senkrechte Wandfalte** am gerundeten Felsblock (135 | 139): G5_D4_2/4.

**Unsichtbar/Prüfartefakt (30):**
- Glatte Hänge, Kuppen und Domflanken ohne erkennbare Kante: G6_C5_1–4, G6_C3_1/3/5, G6_D4_1–5, G6_B4_1/4, G5_C5_1/4/5, G5_C3_2/4/5, G5_C4_2, G5_D4_1/3. G6 auf weichen Hängen und G5 an runden Kuppen bzw. auf Grat-Wegen (G5_C5_1, Wert 2,63) wirken wie Prüfartefakte. Hohe Werte bedeuten nicht automatisch Sichtbarkeit: Der höchste G6-Wert (B4_1, 48) ist unsichtbar.
- **Nur verdeckt (7):** G6_C5_5, G6_C3_4, G6_C4_2, G6_B4_2, G6_B4_3, G6_B4_5 (Haus), G5_C3_3. Diese Fälle gelten nur, solange Baum oder Haus dort stehen. **G6_C4_2 nicht in die Ausnahmeliste:** Unter dem Baum liegt ein harter Wandfußknick (B/C).

**Empfehlung Priorisierung (L1/L2):**
1. Treppenstufen an Plateaurändern im Dorf (C4, C5) zuerst, weil sie die meisten sichtbaren Treffer bündeln und auch neben den Treffern auffallen.
2. Spitzen und Zacken an Klippenkronen bzw. Graten (C5-Horn, C3-Finne), danach die D4-Wandfalte und den C3-Buckel.
3. B4 und D4 haben bei G6 keinen sichtbaren Treffer. Dort keine L1-Zeit für G6 einsetzen.

**Empfehlung Ausnahmeliste (Antrag, P5 muss die Messwerte nachrechnen):** die 23 „nein“-Treffer ohne Verdeckung. Die 6 nur verdeckten Fälle ohne Problemform (alle außer G6_C4_2) bitte nur mit dem Vermerk „verdeckt durch Objekt“, weil sie beim Umsetzen von Bäumen oder Häusern wieder sichtbar werden. Die Stichprobe deckt 43 der 288 Treffer ab (15 %). Eine Hochrechnung auf alle Treffer ist nur grob möglich. Für C5/C3/C4 ist ein voller Durchgang sinnvoll.

**Nebenbefunde (andere Familien, sichtbar):**
- Zackige „Pfeil“-Wegenden auf dem D4-Felsblock (x ≈ 128–134, z ≈ 130–138): G6_D4_1/4, G5_D4_3, zu R8a/R1.
- Punktierte Texturlinie entlang des Hangfußes C3 (x ≈ 85, z 105–112): G6_C3_3_nah, eher T-Familie.

## Zahlenprüfung
- `regeln_letzter_lauf.json`: G6_facette **220**, G5_beule_klippe **68**, wie im Auftrag. Keine Abweichung.
- Gegenprobe: `pruefe_regeln.py` frisch auf `relief_daten.json.gz` @ 8e374b0 ergibt G6 220 und G5 68 mit identischen Einzeltreffern. Die Gesamtsumme ist 571 statt 570, nur wegen `G1_lochscan_fehlt` ohne LOCHSCAN, wie im FERTIGPLAN beschrieben.
- Je Kachel: G6 C5 17, C3 15, C4 16, D4 6, B4 15. G5 C5 14, C3 18, C4 **4**, D4 **4**, B4 **0**. G5 hat in C4 und D4 also nur je 4 Treffer, alle wurden genommen. In B4 gibt es keinen G5-Treffer.
- Auswahl: die schlimmsten Werte zuerst, mit mindestens 3 m Abstand zwischen den Stichproben (damit nicht fünfmal derselbe Cluster gezogen wird). Bei zu wenigen Treffern wurde mit den nächstschlimmsten aufgefüllt. Der Rang des Werts steht in `bilder_8e374b0/stichprobe.json` (`rang_wert`).

## Methode / Hinweise
- Das eingecheckte `relief3d/index.html` ist der RELIEF_NEU-Prototyp mit **nur D1/G1/D2**. C3/C4/C5/D4/B4 sind dort leer und für P4 unbrauchbar. Deshalb baut `baue_vollansicht.py` den Voll-Viewer (main.js + relief_daten.json.gz, ganze Karte) mit dem unveränderten Quelltext von `baue_html.py` nach `/tmp`, ohne `/tmp/w3/bundle_r.js` oder das Repo anzufassen. Gerendert wird mit dem unveränderten `pruefung/o18/render_t119u.js` (`?manual=1&nosh=1`, Swiftshader, Licht Standard az 315/el 45). Nicht geprüft, aber möglicherweise relevant: Auch der Lochscan im Gate nutzt `index.html`.
- Die G6-Koordinate ist der Schwerpunkt eines Clusters. Bei langgezogenen Clustern liegt der sichtbare Fehler 1–3 m neben der Bildmitte. Rote Eckmarken zeigen den Trefferpunkt.
- Der FERTIGPLAN nennt für P4 den Pfad `relief3d/pruefung/sichtfilter/`. Die Ablage liegt laut Auftrag unter `qa_p4/`.

## Wiederholung auf L1
```
cd team/art/dorfmap_grundgeruest/relief3d/pruefung/qa_p4
NODE_PATH=/tmp/w3/node_modules python3 stichprobe_p4.py \
  --relief3d /PFAD/L1-worktree/team/art/dorfmap_grundgeruest/relief3d \
  --label L1_<commit> --out bilder_L1_<commit> --neu-pruefen [--nah]
```
`--neu-pruefen` rechnet `pruefe_regeln.py` auf den L1-Höhendaten neu (optional `--daten pfad.json.gz`, `--treffer eigene.json`). Ausgabe: Kompositbilder, `stichprobe.json`, `TABELLE_ROH.md` (Urteile leer, Sichtung von Hand). Laufzeit ca. 4 min für 43 Stichproben.

## Tabelle

| Treffer | Kachel | x | z | Wert | sichtbar ja/nein | Bild | Begründung |
|---|---|---|---|---|---|---|---|
| G6_C5_1 | C5 | 115.4 | 181.6 | 17 | nein | [G6_C5_1.jpg](bilder_8e374b0/G6_C5_1.jpg) | Klippenkrone an der Trefferstelle weich gerundet, keine Facettenkante. Treppenstufen am Plateaurand links im Bild liegen außerhalb des Treffers. |
| G6_C5_2 | C5 | 86.8 | 203.7 | 13 | nein | [G6_C5_2.jpg](bilder_8e374b0/G6_C5_2.jpg), [nah](bilder_8e374b0/G6_C5_2_nah.jpg) | In A eine weiche Rinne im Hang. Erst im 15-m-Nahbild (_nah) eine feine Absatzkante, grenzwertig. |
| G6_C5_3 | C5 | 93.5 | 172.6 | 13 | nein | [G6_C5_3.jpg](bilder_8e374b0/G6_C5_3.jpg) | Hangrücken mit Weg, im Clay weicher Grat. Teilweise von Baum verdeckt. |
| G6_C5_4 | C5 | 120.5 | 185.0 | 13 | nein | [G6_C5_4.jpg](bilder_8e374b0/G6_C5_4.jpg) | Kleine Kuppe an der Klippenkrone, wirkt natürlich. Im Clay weich. |
| G6_C5_5 | C5 | 84.8 | 179.0 | 11 | nein | [G6_C5_5.jpg](bilder_8e374b0/G6_C5_5.jpg) | In der Spielansicht A komplett von einem Baum verdeckt. Im Clay ein weicher Grat. |
| G6_C3_1 | C3 | 85.7 | 105.4 | 31 | nein | [G6_C3_1.jpg](bilder_8e374b0/G6_C3_1.jpg), [nah](bilder_8e374b0/G6_C3_1_nah.jpg) | Hangfuß neben Haus, im Clay weich. Im Nahbild (_nah) nur Texturgrenze Fels/Schnee. |
| G6_C3_2 | C3 | 114.8 | 120.7 | 25 | ja | [G6_C3_2.jpg](bilder_8e374b0/G6_C3_2.jpg) | Schmaler, scharfer Grat (Finne) mit Spitze direkt am Treffer, in A deutlich. Im Clay harte Kante. |
| G6_C3_3 | C3 | 85.0 | 111.9 | 20 | nein | [G6_C3_3.jpg](bilder_8e374b0/G6_C3_3.jpg), [nah](bilder_8e374b0/G6_C3_3_nah.jpg) | Hangfuß 6,5 m neben G6_C3_1, Form im Clay weich. Sichtbar ist aber eine punktierte Texturlinie entlang des Hangfußes (_nah), eher T-Familie. |
| G6_C3_4 | C3 | 106.5 | 116.3 | 18 | nein | [G6_C3_4.jpg](bilder_8e374b0/G6_C3_4.jpg) | In A von Bäumen verdeckt. Im Clay ein weicher, welliger Hang. |
| G6_C3_5 | C3 | 110.6 | 111.7 | 14 | nein | [G6_C3_5.jpg](bilder_8e374b0/G6_C3_5.jpg) | Hügelkuppe weich, Baum teilweise davor. |
| G6_C4_1 | C4 | 112.7 | 167.3 | 26 | ja | [G6_C4_1.jpg](bilder_8e374b0/G6_C4_1.jpg) | Treppenstufen am Plateaurand neben dem Haus (senkrechte weiße Stufenwände), in A deutlich. Im Clay klare Stufen. |
| G6_C4_2 | C4 | 86.4 | 169.5 | 17 | nein | [G6_C4_2.jpg](bilder_8e374b0/G6_C4_2.jpg) | In A von großem Baum verdeckt. B/C zeigen aber einen harten Wandfußknick, aus anderem Blickwinkel sichtbar. Nicht in die Ausnahmeliste. |
| G6_C4_3 | C4 | 96.3 | 164.4 | 15 | ja | [G6_C4_3.jpg](bilder_8e374b0/G6_C4_3.jpg) | Treppenstufen am Plateaurand neben dem Haus, in A deutlich. |
| G6_C4_4 | C4 | 116.4 | 136.7 | 13 | ja | [G6_C4_4.jpg](bilder_8e374b0/G6_C4_4.jpg) | Gezackter, gestufter Plateaurand hinter dem Haus läuft durch die Trefferstelle. |
| G6_C4_5 | C4 | 120.4 | 156.6 | 13 | ja | [G6_C4_5.jpg](bilder_8e374b0/G6_C4_5.jpg) | Stufenkerben am Plateaurand neben den Häusern. Im Clay gestuft. |
| G6_D4_1 | D4 | 133.9 | 130.2 | 22 | nein | [G6_D4_1.jpg](bilder_8e374b0/G6_D4_1.jpg) | Plateaukante gerundet, Form weich. Sichtbar ist aber das zackige Wegende (Pfeilform) auf dem Block, eher R8a/Weg. |
| G6_D4_2 | D4 | 139.5 | 168.2 | 12 | nein | [G6_D4_2.jpg](bilder_8e374b0/G6_D4_2.jpg) | Glatter Schneehang am See, nichts erkennbar. |
| G6_D4_3 | D4 | 132.0 | 147.0 | 9 | nein | [G6_D4_3.jpg](bilder_8e374b0/G6_D4_3.jpg) | Wegende am Felsfuß, Formübergang weich. |
| G6_D4_4 | D4 | 131.4 | 133.9 | 7 | nein | [G6_D4_4.jpg](bilder_8e374b0/G6_D4_4.jpg), [nah](bilder_8e374b0/G6_D4_4_nah.jpg) | Plateaudecke an der Trefferstelle weich (_nah). 2–3 m daneben liegen eine senkrechte Wandfalte (= G5_D4_2) und das zackige Wegende. |
| G6_D4_5 | D4 | 140.8 | 162.0 | 6 | nein | [G6_D4_5.jpg](bilder_8e374b0/G6_D4_5.jpg) | Glatter Schneehang, nichts erkennbar. |
| G6_B4_1 | B4 | 78.6 | 151.9 | 48 | nein | [G6_B4_1.jpg](bilder_8e374b0/G6_B4_1.jpg) | Breite Hügelkuppe, weich, keine Kante (trotz Wert 48). |
| G6_B4_2 | B4 | 64.1 | 161.0 | 42 | nein | [G6_B4_2.jpg](bilder_8e374b0/G6_B4_2.jpg) | In A von Baum verdeckt. Im Clay weicher Übergang Schnee/Fels. |
| G6_B4_3 | B4 | 82.2 | 160.1 | 18 | nein | [G6_B4_3.jpg](bilder_8e374b0/G6_B4_3.jpg) | In A von Baum verdeckt. Im Clay eine weiche Rinne. |
| G6_B4_4 | B4 | 56.7 | 150.9 | 16 | nein | [G6_B4_4.jpg](bilder_8e374b0/G6_B4_4.jpg) | Flacher Hang vor Haus, Textur unauffällig. Im Clay nur eine feine Linie. |
| G6_B4_5 | B4 | 58.9 | 141.6 | 13 | nein | [G6_B4_5.jpg](bilder_8e374b0/G6_B4_5.jpg) | Von einem Haus verdeckt. |
| G5_C5_1 | C5 | 113.5 | 200.5 | 2.63 | nein | [G5_C5_1.jpg](bilder_8e374b0/G5_C5_1.jpg), [nah](bilder_8e374b0/G5_C5_1_nah.jpg) | Weg auf schmalem Grat zwischen zwei Klippen. Keine Beule erkennbar, auch nicht im Nahbild (_nah). Vermutlich Prüfartefakt (Grat/Wegdamm als Kante gewertet). |
| G5_C5_2 | C5 | 123.5 | 185.8 | 0.91 | ja | [G5_C5_2.jpg](bilder_8e374b0/G5_C5_2.jpg), [nah](bilder_8e374b0/G5_C5_2_nah.jpg) | Zackige Spitzen an der Klippenkante neben dem Baum, im Nahbild (_nah) deutlich. |
| G5_C5_3 | C5 | 124.0 | 189.2 | 0.88 | ja | [G5_C5_3.jpg](bilder_8e374b0/G5_C5_3.jpg) | Gleiche Stelle wie G5_C5_2 (3,4 m): Horn an der Klippenkante. Im Clay V-Kerbe. |
| G5_C5_4 | C5 | 120.8 | 189.0 | 0.87 | nein | [G5_C5_4.jpg](bilder_8e374b0/G5_C5_4.jpg) | Krone an der Trefferstelle weich gerundet. Die Spitze liegt 3 m östlich (= G5_C5_2/3). |
| G5_C5_5 | C5 | 91.0 | 210.0 | 0.8 | nein | [G5_C5_5.jpg](bilder_8e374b0/G5_C5_5.jpg) | Kleine Hangschulter, weich. |
| G5_C3_1 | C3 | 125.5 | 96.2 | 2.27 | ja | [G5_C3_1.jpg](bilder_8e374b0/G5_C3_1.jpg), [nah](bilder_8e374b0/G5_C3_1_nah.jpg) | Runder Buckel mit Ringmulde mitten im flachen Dorfplatz, im Nahbild (_nah) deutlich. Keine Klippe: G5 trifft hier eine Fehlform-Kuppe. |
| G5_C3_2 | C3 | 108.9 | 107.4 | 1.29 | nein | [G5_C3_2.jpg](bilder_8e374b0/G5_C3_2.jpg) | Hügelkuppe weich, wirkt natürlich. |
| G5_C3_3 | C3 | 113.1 | 106.1 | 1.25 | nein | [G5_C3_3.jpg](bilder_8e374b0/G5_C3_3.jpg) | In A/B von Baum verdeckt. Im Clay nur eine kleine Kerbe an der Krone. |
| G5_C3_4 | C3 | 103.5 | 114.2 | 1.04 | nein | [G5_C3_4.jpg](bilder_8e374b0/G5_C3_4.jpg) | Hang unter leicht höckriger Krone, an der Trefferstelle weich. |
| G5_C3_5 | C3 | 101.0 | 99.5 | 0.96 | nein | [G5_C3_5.jpg](bilder_8e374b0/G5_C3_5.jpg) | Kronenlinie weich. Feine Linie nur im Clay, in der Textur nicht sichtbar. |
| G5_C4_1 | C4 | 118.8 | 166.1 | 1.18 | ja | [G5_C4_1.jpg](bilder_8e374b0/G5_C4_1.jpg) | Gestufter Plateaurand mit Lippe neben dem Haus, in A sichtbar. |
| G5_C4_2 | C4 | 124.5 | 150.5 | 0.65 | nein | [G5_C4_2.jpg](bilder_8e374b0/G5_C4_2.jpg) | Flanke einer glatten Felskuppe. |
| G5_C4_3 | C4 | 117.5 | 168.0 | 0.86 | ja | [G5_C4_3.jpg](bilder_8e374b0/G5_C4_3.jpg) | Gleiche Stelle wie G5_C4_1 (1,9 m). Im Clay zusätzlich eine nadelartige Spitze am Rand. |
| G5_C4_4 | C4 | 120.5 | 165.5 | 0.69 | ja | [G5_C4_4.jpg](bilder_8e374b0/G5_C4_4.jpg) | Gleiche Stelle wie G5_C4_1 (1,8 m), Stufen/Lippe sichtbar. |
| G5_D4_1 | D4 | 127.2 | 147.5 | 1.4 | nein | [G5_D4_1.jpg](bilder_8e374b0/G5_D4_1.jpg) | Glatte Kuppenflanke. |
| G5_D4_2 | D4 | 135.0 | 139.0 | 1.01 | ja | [G5_D4_2.jpg](bilder_8e374b0/G5_D4_2.jpg), [nah](bilder_8e374b0/G5_D4_2_nah.jpg) | Senkrechte Falte/Knick in der Wandfläche des gerundeten Felsblocks, im Nahbild (_nah) deutlich. |
| G5_D4_3 | D4 | 126.0 | 137.5 | 0.61 | nein | [G5_D4_3.jpg](bilder_8e374b0/G5_D4_3.jpg) | Plateaudecke weich. |
| G5_D4_4 | D4 | 135.5 | 139.5 | 0.78 | ja | [G5_D4_4.jpg](bilder_8e374b0/G5_D4_4.jpg) | Gleiche Stelle wie G5_D4_2 (0,7 m), senkrechte Wandfalte. |
