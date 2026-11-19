# Ergebnis P1c – Nacharbeit ohne Codex: Zonen konstruktiv aus Vektoren

**Stand:** 19.11.2026 · Branch `art/dv2-vektor-kanten` · PR #57 → `art/dorfmap-fertig`

Kosten: 0 EUR, Codex 14:48-16:28 (1 h 40), Nacharbeit ohne Codex 16:30-17:42 (Europe/Berlin)

## Warum die Methode gewechselt wurde

Der Codex-Lauf C1 hat die Zonen-Q3 zweimal verfehlt (Flächentyp 21,2 cm / 112°, Untergrund 21,8 cm / 112°). Die Ursache: Die Zonen wurden aus dem 1-m-Zellraster polygonisiert und danach geglättet. Treppenkanten, 1-Zell-Specks und Zwei-Label-Ecken lassen sich so nicht auf 3 cm glätten, ohne die Partition zu zerstören. Neu werden die Flächentypen **konstruktiv aus den gemergten Vektoren** aufgebaut: Wasser aus #58, Wege und Kreuzungen aus #59 @ 9ce6ac3. Fels, Untergrund und Kanten kommen aus geglätteten Distanzfeldern statt aus Zellpolygonen. Für die Nacharbeit gab es keinen weiteren Codex-Lauf.

## Lieferstand

- `../vektor/zonen.geojson`: 998 Features.
  - 68 Flächentyp-Polygone, 46 Untergrund-Polygone, 25 Bauzonen-Polygone, 859 Slots.
  - Bauzone und Slots wurden wie bisher erzeugt.
  - Beide Flächenebenen sind gültige, lücken- und überlappungsfreie Partitionen von `0..336 × 0..303`.
- `../vektor/kanten.geojson`: 20 Linien (8 `klippe_oben`, 8 `klippe_unten`, 4 `steil55`). Zwei Stücke unter 3 m wurden weggelassen.
- `../vektor/grat.geojson`: unverändert (Byte-gleich zu ed6e935).
- Code:
  - `zonen_konstruktiv.py` (neu)
  - `extrahiere_kanten.py` (Zonen und Kanten auf die neue Methode umgestellt)
  - `test_kanten.py`
  - `render_vektoren.py` (neu)
- Bilder (alle < 1 MB, angesehen):
  - [Zonen-Übersicht](uebersicht_zonen.jpg)
  - [Nahbild 72|154](nahbild_72_154.jpg)
  - [E2 vorher/nachher](e2_vorher_nachher.jpg)
  - [`../tag1_vektoren.jpg`](../tag1_vektoren.jpg): alle Vektoren über der alten Draufsicht
  - neu gerendert: [Übersicht Kanten](uebersicht_kanten.jpg), [G3/H3](nahbild_g3h3.jpg), [B3/C3](nahbild_b3c3.jpg)

## Verfahren

1. **Flächentyp**, Priorität Wasser > Brücke > Weg > Ufer > Fels > Grund:
   - **Wasser** = `wasser.geojson` (Typ `wasser`), unverändert.
   - **Ufer** = Schließen(Uferbänder ∪ Wasser) ∖ Wasser. Das Schließen nutzt r = 2 m und ein Außenband, damit am Kartenrand nichts abgerundet wird. [A] Es füllt numerische Spalten zwischen Band und Wasser.
   - **Weg** = Schließen(`wege.geojson` Rolle `netz`, r = 2 m, mit Außenband). [A] Konkave Ecken des Netzes werden auf r = 2 m ausgerundet, denn ein Kreis mit r = 2 m ergibt ein 1-m-Mittel von ~2,1 cm. Kreuzungen sind im Netz enthalten.
   - **Brücke** [A]: Die Platzhalter-Rechtecke E2 (x186-197, z73-75) und E3-West (x174-186, z126-128) dienen nur als Auswahlfenster.
     - Brückenfläche = die Komponenten von (Weg ∩ Ufer ∖ Wasser), die ein Rechteck schneiden. So enden die Brückenränder an Schnitten glatter Bögen statt an 90°-Ecken. Reine Rechtecke würden 2-Label-Knicke von 90° erzeugen.
     - Die westliche Komponente am E3 läuft durch die Weg-Ausrundung am Ufer entlang bis z 137. Sie wird bei z = 129,682 waagrecht gekappt, und zwar so, dass ihre Fläche der Quellkonstruktion (8,92 m²) entspricht.
     - Der abgeschnittene Rest liegt im Uferband und wird Ufer. Beide Schnittenden sind dadurch Tripelpunkte.
   - **Fels**:
     - Ausgangsmaske: Untergrund FELS/KLIPPE_WAND/KLIPPE_KANTE.
     - Glättung: SDF auf einem 0,1-m-Raster, Gauss σ = 1,0 m, Kontur bei 0, ohne 7-m-Opening.
     - Nachbearbeitung: [A] Öffnen und Schließen mit r = 2,5 m gegen Spitzen und Taschen, danach eine adaptive Ringglättung. Felsstücke < 4 m² gehen an Grund. Es wurde kein Fels-Ring verworfen.
     - Der Fels wird über den Kartenrand hinaus geglättet und erst danach beschnitten.
   - **Grund** = Rest.
   - **Knoten**: [A] Snap-Rounding (`grid_size` 1 mm) und `polygonize`. Stützpunkte, die weniger als 2 cm vom vorigen Punkt entfernt liegen, werden entfernt, weil sonst Mikro-Haken entstehen.
2. **Untergrund**:
   - Wasser- und Felszellen übernehmen den nächstgelegenen Untergrund.
   - Glättung je Label mit Gauss σ = 3,5 m, danach Argmax. [A] Mit σ 1,5 m blieben Zungen mit Q3 > 3 cm.
   - Inseln < 12 m² gehen an den Nachbarn. [A] Bei 4 m² blieben nicht Q3-fähige Mini-Ringe.
   - Danach exakte Pixelkanten-Partition, und je Bogen eine adaptive Gauss-Glättung mit festen Knoten.
   - Eine Insel mit 18,3 m² bei 162,5|208 war nicht Q3-fähig und ist entfallen.
   - Labels: SCHNEE, WALD, SCHATTEN, BODEN, SAND. SCHATTEN bleibt ein eigenes Label.
3. **Kanten**:
   - Wandmaske per SDF-Glättung (wie Fels) statt 7-m-Opening, danach Öffnen und Schließen mit 2,5 m und eine Ringglättung.
   - Die Linien werden am Kartenrechteck geschnitten. Linien < 3 m entfallen.
   - Oben/unten wird nach der GB-Medianhöhe bestimmt. `steil55` ist unverändert.
4. **Grat**: unverändert. Die Abstände der echten Krone sind `300|90` 1,500 m, `290|98` 3,536 m und `84|129` 3,509 m; die Forderung ≤ 1 m ist damit verfehlt. Die Abstände stehen als `anker_abstaende_m` im GeoJSON, und der Test prüft, dass diese Angabe stimmt.
5. **Bauzone und Slots**: wie bisher.

## Q3 – beide Messarten (Grenze 3,0 cm, Knick 15°)

QA-Messart ist `glaettung_abw` aus origin/art/dv2-qa @ 38fa7ec (`dv2qa/geom.py`). Sie mittelt über die Stützpunkte im Fenster ±0,5 m und ist wörtlich in `test_kanten.py` übernommen. Die feine Messart tastet in 0,05-m-Schritten ab und mittelt über 21 Punkte. Bogenenden (Tripelpunkte, Randübergänge) sind ausgenommen, mit einem Schutzabstand von 0,5 m.

| Ebene | QA (Stützpunkte) | fein (0,05 m) | max. Knick | Verstöße außerhalb Tripelpunkte |
|---|---:|---:|---:|---|
| `kanten.geojson` (20 Linien) | 2,37 cm | 2,20 cm | 7,6° | 0 |
| `grat.geojson` (4 Linien) | 2,82 cm | 2,62 cm | 3,4° | 0 |
| Untergrund (gemeinsame Bögen) | 2,94 cm | 2,73 cm | 3,5° | 0 |
| Flächentyp (gemeinsame Bögen) | 9,01 cm* | 5,63 cm* | 44,1°* | 0 außerhalb bekannter Quellen |

\* Diese Maxima liegen ausschließlich an **bekannten Quellen**, die der Generator nicht verändert. Sie sind im Test einzeln aufgezählt und werden exakt verglichen. Außerhalb davon halten alle Flächentyp-Bögen beide Messarten ≤ 3,0 cm und ≤ 15°.

- **Wegenden (52, `wege.geojson` #59)**: Die runden Wegkappen sind schmaler als 3,2 m. Ein Kreis mit r < 1,6 m kann das 3-cm-Maß des 1-m-Mittels geometrisch nicht halten; mit der QA-Messart braucht es r ≥ 2 m. **Einzige Fassung (19.11. 17:50):** vorläufiger Ausnahme-Kandidat in `detail_v2/AUSNAHMEN_DV2.md` (A-DV2-01). Er gilt nur, wenn die Wegenden in der P6-Sichtprüfung bei 1,7 m unsichtbar sind; dann mit Messwert und Nahbild. Sind sie sichtbar, müssen sie weg: Dann bekommen die Wegenden eine andere Endgeometrie (Aufweitung auf ≥ 4 m oder auslaufendes Ende in P2), keine Ausnahme.
- **Wasserumriss (52 Messpunkte, `wasser.geojson` #58)**: Die Uferlinien der Quelle verletzen die QA-Messart selbst (`ufer.geojson` Uferlinien bis 3,44 cm; QA-P6 meldet 9 Befunde in `ufer.geojson`). In den Zonen treten bis 3,30 cm auf, höchstens 2 cm neben dem Quellumriss. Der Test verlangt dazu, dass die Quelle selbst > 3 cm misst. **Einzige Fassung:** Zweites Scheitern des Wasserumrisses → nach t2027u kein drittes Nachglätten auf demselben Weg. Neu als P1b3 mit benannter Ursache, neuer Methode und Frist, siehe `DETAIL_V2_PLAN.md` Abschnitt P1b3.

**QA-P6 Q3 direkt auf den Dateien** (Regel `q3` aus dv2qa @ 38fa7ec mit `konfig.json`):

| Datei | Befunde |
|---|---|
| `kanten.geojson` | 0 |
| `grat.geojson` | 0 |
| `wege.geojson` | 0 (2,70 cm) |
| `ufer.geojson` (Quelle #58) | 9 (bis 3,44 cm) |
| `zonen.geojson` | 31 Befunde in Flächentyp-Ringen, 0 in Untergrund-Ringen |

QA misst Zonen als rohe Polygonringe. Damit gehen Tripelpunkte, Kartenecken und die Ringe um Wegenden mit in die Messung ein; deshalb trennt `test_kanten.py` nach gemeinsamen Bögen.

## Flächen

| Typ | GeoJSON | Referenz | Abweichung |
|---|---:|---:|---:|
| Wasser | 6.630,19 m² | `wasser.geojson` 6.630,17 m² | 0,00 % |
| Ufer | 5.165,44 m² | Uferbänder ∖ Wasser 5.198,90 m² | −0,64 % |
| Brücke | 33,74 m² | Quell-Weg ∩ Band ∖ Wasser 33,65 m² | +0,29 % (gegen Rechtecke ∖ Wasser 33,96 m²: −0,63 %) |
| Weg | 5.360,93 m² | Netz 5.313,83 m² | +0,89 % (nur berichtet) |
| Fels | 19.698,60 m² | 20.875 Zellen | −5,6 % (nur berichtet: Ausrundung r 2,5 m; keine Toleranz vorgegeben) |
| Bauzone | 31.893,000 m² | 31.893 Zellen | < 0,0001 % |

Die alte Kalibrierung auf Zellzählungen (z. B. Brücke 20 Zellen, Ufer 2.902 Zellen) gilt nicht mehr. Referenz ist jetzt die Vektorquelle.

## Tests und Gate

- `pytest test_kanten.py`: **7 passed**, ohne xfail und ohne skip.
  - Partition und Format
  - Flächen ±3 % bzw. ±1 %
  - Grat-Abstände wie angegeben
  - Determinismus (2 Läufe, identische SHA-256)
  - Q3 nach beiden Messarten
  - Tripelpunkt-Ausnahmen
- SHA-256:
  - `kanten.geojson` `f57c0d80b72c7205b71ba90f80fa39e933ce713b2f4551ffff1280d5c706c69f`
  - `grat.geojson` `5e130f8b7c7a39ef4d0b2705175a3487182ff773e52b297b5985a055e2a1cfb4`
  - `zonen.geojson` `b88a045f60f9e2e8f18a422e4919fdc3c2f93808d22fad05a3f1e89950b60198`
- Altes Gate über `pruefung/export_gate.sh` mit Lochscan `loch_o18g.js` (RAND 0,6): **359 / R8 31 / R9 321, W1 0, Loch 0** (`offen_innen` 0, `punkte` 0). Die Meldung „GATE ROT: kein Export/ZIP“ ist erwartet. Das Artefakt `pruefung/w1_alle56_letzter_lauf.json` wurde danach wiederhergestellt.

## Offene Punkte / Risiken

- [R] Wegenden (Ausnahme-Kandidat A-DV2-01, Entscheid in P6 bei 1,7 m) und der Wasserumriss (P1b3, neue Methode) sind Quellthemen. Solange sie offen sind, bleiben die Flächentyp-Maxima an diesen Stellen über 3 cm. Nach einer Quellkorrektur einfach neu generieren; die Ausnahmeliste im Test muss dann kürzer werden.
- [R] Grat-Anker 1,5 / 3,54 / 3,51 m > 1 m (siehe oben).
- [A] Die Brücken bleiben Platzhalter-Ableitungen (Auswahlfenster plus Schnitt bei E3-West) und sind keine modellierten Brückendecks.
- [S] Es wurden keine Altdateien außerhalb von `detail_v2/kanten/` und `detail_v2/vektor/{kanten,zonen}.geojson` geändert. Neu ist nur `detail_v2/tag1_vektoren.jpg` (wie beauftragt).

## Appendix: einzeln enumerierte zulässige Ausnahmen

Echte 3+-Label-Knoten und Zonenwechsel am Kartenrand. Die Kartenrand-Bögen selbst werden nicht gemessen; die vier Kartenecken liegen auf dem Rahmen. Angaben in Viewer-Metern `x|z`.

### Flächentyp-Grenzen (71 Punkte)

`0|2`, `0|26.006`, `0|33.973`, `0|44.487`, `0|236.104`, `0|240.654`, `0|253.354`, `0|257.906`, `0|268.56`, `0|273.123`, `0|278.381`, `0|283.034`, `0|301`, `2|0`, `2|303`, `21.395|0`, `31.28|199.586`, `31.3|194.958`, `173.585|137.342`, `175.432|129.682`, `176.793|126.132`, `178.203|129.451`, `179.315|126.507`, `181.598|129.5`, `184.281|129.909`, `185.746|122.979`, `187.018|76.207`, `187.824|73.289`, `188.072|123.98`, `189.682|76.112`, `190.141|74.317`, `192.371|112.324`, `192.815|110.546`, `193.795|76.914`, `193.974|76.261`, `202.903|225.577`, `208.341|192.363`, `209.585|6.603`, `209.622|0`, `209.933|192.844`, `211.158|190.662`, `213.686|248.04`, `214.795|0`, `216.801|199.226`, `217.824|201.292`, `218.779|0`, `220.322|9.382`, `220.943|201.911`, `222.986|0`, `223.35|235.02`, `226.232|219.172`, `240.7|0`, `295.035|166.829`, `296.063|168.458`, `334|0`, `334|303`, `336|2`, `336|4.159`, `336|11`, `336|36.521`, `336|60.957`, `336|65.585`, `336|82.021`, `336|97.096`, `336|259.074`, `336|263.33`, `336|268.176`, `336|274.046`, `336|285.515`, `336|289.75`, `336|301`

### Untergrund-Grenzen (56 Punkte)

`0|12`, `0|30.4`, `0|39.3`, `0|49.2`, `0|71.8`, `0|84.8`, `0|89.3`, `0|99.9`, `0|106`, `0|252.3`, `0|288.4`, `2.8|39.4`, `9.1|44`, `9.2|36.5`, `17.6|31`, `20.1|41.7`, `24.7|33.2`, `56.5|39.1`, `62.7|36.5`, `64.6|34.1`, `66.6|42.7`, `92|129.3`, `104.8|109.2`, `114.6|245.6`, `116.4|133.2`, `119.1|34.5`, `123.6|118.7`, `123.9|243.3`, `140.1|19.1`, `143.4|29.2`, `153|26.1`, `162.2|22.5`, `170.5|25.5`, `211.5|231.1`, `217.3|235.8`, `222|29.2`, `226|21.7`, `233.5|41.3`, `238.4|32`, `240.8|20`, `256.6|27.8`, `267.8|15.1`, `268.8|17.5`, `277.6|241.7`, `289|228.1`, `296.2|226.2`, `301.7|232.8`, `336|10`, `336|21.5`, `336|69.8`, `336|85.9`, `336|89.8`, `336|181.4`, `336|207.7`, `336|250.2`, `336|277.5`

### Bekannte Quelle Wasserumriss (52 Messpunkte, 52 Orte)

`13.14|51.1`, `15.63|54.8`, `19.93|41.99`, `20.25|44.67`, `20.3|44.75`, `20.42|42.06`, `20.66|45.1`, `20.74|43.54`, `23.2|44.27`, `23.75|44.04`, `24.26|43.57`, `24.39|43.36`, `30.94|55.97`, `31.51|58.45`, `31.82|54.86`, `32.54|54.66`, `33.61|54.88`, `33.71|54.89`, `34.03|59.41`, `35.38|53.67`, `35.41|52.78`, `70.91|263.22`, `71|263.16`, `71.07|263.1`, `74.09|47.18`, `166.89|259.96`, `166.92|259.86`, `166.94|259.77`, `172|156.54`, `172.04|156.63`, `172.64|258.42`, `172.74|258.42`, `172.94|153.1`, `174.91|262.21`, `174.95|262.01`, `174.97|261.72`, `174.97|261.82`, `199.59|40.84`, `205.66|224.69`, `215.26|2.13`, `216.17|5.46`, `216.24|5.7`, `216.49|6.13`, `217.7|229.07`, `217.89|228.84`, `218.63|0.82`, `219.58|232.69`, `220.68|232.22`, `220.69|227.03`, `220.73|232.07`, `324.67|271.79`, `324.68|271.59`

### Bekannte Quelle Wegenden (52)

`G001#0:ende`, `G001_anb#0:ende`, `G002#0:anfang`, `G002#0:ende`, `G003#0:anfang`, `G003#0:ende`, `G003_anb#0:anfang`, `G003_anb#0:ende`, `G004#1:ende`, `G004_anb#0:anfang`, `G004_anb#0:ende`, `G005#1:ende`, `G006#0:anfang`, `G006#0:ende`, `G006_anb#0:ende`, `G007#0:anfang`, `G007#1:anfang`, `G008#1:ende`, `G008_anb#0:anfang`, `G008_anb#0:ende`, `G009#1:anfang`, `G009#1:ende`, `G010#0:anfang`, `G011#0:ende`, `G011#1:anfang`, `G012#0:anfang`, `G012#0:ende`, `G013#0:ende`, `G014#0:ende`, `G015#0:ende`, `G015#1:ende`, `G016#1:ende`, `G017#0:ende`, `G018_anb#0:ende`, `G019_anb#0:anfang`, `G902a#0:ende`, `G903b#0:anfang`, `G903b#0:ende`, `haus_A11#0:anfang`, `haus_A11#0:ende`, `haus_A25#0:anfang`, `haus_A25#0:ende`, `haus_A31D#0:anfang`, `haus_B28#0:anfang`, `haus_B29D#0:anfang`, `haus_B29D#0:ende`, `haus_D02#0:anfang`, `haus_D02#0:ende`, `haus_D08#0:anfang`, `haus_E04D#0:anfang`, `haus_E07#0:anfang`, `haus_E07#0:ende`

---

## P1c2 – Zonen auf Basis #60, q3-Fundgruppen (Branch `art/dv2-zonen2`)

Kosten: 0 EUR, ohne Codex, 18:06-18:23 (Europe/Berlin)

Basis ist `art/dv2-vektor-wasser-q3` @ d563688 (PR #60, Wasser/Ufer gleichmäßig auf 0,05 m abgetastet, Geometrie wie #58); der Branch enthält #57.

### 1) Ausnahme „Wasserumriss“ entfällt

Nach dem Neugenerieren gibt es auf den Flächentyp-Bögen 0 Verstöße am Wasserumriss (vorher 52 Messpunkte, bis 3,30 cm). Der Test verlangt jetzt hart, dass diese Gruppe leer ist. Die Uferlinien messen nach der QA-Messart 2,90 cm. Als Ausnahme bleiben nur die 52 Wegenden (A-DV2-01, unverändert).

### 2) q3-Funde in `zonen.geojson`, Gruppen a–d

Messart (QA, verbindlich ab 18:08): Jeder Polygonring wird nach Bogenlänge auf 0,05 m abgetastet, dann folgt ein gleitendes 1-m-Mittel (Ring zyklisch); Grenze 3 cm, Knick 15°. Ein „Ort“ fasst alle Messpunkte zusammen, die zum selben Tripelpunkt, Wegende oder Randpunkt gehören.

Zuordnung:
- c = höchstens 0,75 m vom Kartenrand
- sonst a = höchstens 0,75 m von einem Knoten mit ≥ 3 Zonen
- sonst b = in einer Wegende-Zone
- sonst d

| Ebene | Gruppe | Orte | max. Abweichung | max. Knick |
|---|---|---:|---:|---:|
| Flächentyp | a Tripelpunkt | 33 | 25,6 cm | 166,6° |
| Flächentyp | b Wegende (A-DV2-01) | 51 | 4,77 cm | – |
| Flächentyp | c Kartenrand | 28 | 22,1 cm | 116,6° |
| Untergrund | a Tripelpunkt | 36 | 24,6 cm | 147,2° |
| Untergrund | c Kartenrand | 20 | 23,6 cm | 134,2° |
| Bauzone, Slots | – | 0 | – | – |
| **alle** | **d Sonstiges** | **0** | – | – |

Zum Vergleich das alte Stützpunktmittel: `q3` aus #55 @ 38fa7ec findet jetzt 77 Ringe mit Funden, max. 27,0 cm.

Korrektur zu meinem P1c-Bericht: Dort hatte ich „31 Funde“ genannt. Das war falsch, denn ich hatte nur die ersten 40 Einträge der Befundliste gezählt. Tatsächlich waren es 832 Befunde, davon die meisten Slot- und Bauzonen-Ringe. Die „bis 25 cm“ von Art Umgebung stimmen.

Was ich konstruktiv behoben habe (Gruppe d war vorher 780 Ringe):
- **Slots** (723 Treppenpolygone aus 1-m-Zellen) werden jetzt als **Punkte** ausgegeben: Flächenschwerpunkt plus `zellen` (vollständige Zellliste) und `flaeche_m2`. Es geht keine Information verloren, und es entsteht keine Linie mehr.
- **Bauzone** (vorher Treppen-/Pufferpolygon) ist jetzt glatt.
  - Verfahren: SDF mit σ 1 m, Öffnen und Schließen mit r 2,5 m, adaptive Ringglättung, Fläche per runder Pufferung auf 31 893 Zellen kalibriert (−0,00005 %).
  - [R] Dabei sind 22 kleine Quellteile entfallen: 17 mit 1–2 m² sowie 20 m² bei 133,7|127,7, 71 m² bei 139,2|151,6, 12 m² bei 251,4|234,4 und 7 m² bei 254,6|239,1. Außerdem sind 38 von 41 Löchern entfallen.
  - Die symmetrische Differenz zu den Zellen beträgt 5,6 %. Die Fläche bleibt durch die Kalibrierung bei ±1 %.
  - Mit r 2,0 oder 1,6 m waren Löcher nicht q3-fähig.
- **Kartenecken und Randkeile**: Das Schließen von Weg und Ufer mit Außenband hat die vier Kartenecken mit Weg gefüllt und an Uferbändern zum Rand tangentiale Keile erzeugt (Knick 178,9°). Ersatz: Die Fläche wird an den Kartenkanten gespiegelt. Ecken bleiben dadurch frei, und Grenzen treffen den Rand ohne Keil. Danach gibt es 63 statt 68 Flächentyp-Polygone.

Sichtprüfung:
- **Gruppe a**: [`nahbild_tripelpunkte.jpg`](nahbild_tripelpunkte.jpg) zeigt Ausschnitte von 16 m (~19 px/m) an den vier größten a-Orten (193,97|76,26, 220,94|201,91, 192,82|110,54, 267,8|15,1). Dort entstehen keine Zacken. Es sind echte Ecken von Flächengrenzen: Ein ausgerundetes Wegende oder eine Wegflanke trifft unter einem Winkel auf den Uferbandrand, bzw. drei glatte Untergrundbögen treffen sich in einem Y-Knoten. Die großen Werte entstehen, weil die 1-m-Mittelung des Rings über die Ecke läuft.
- **Gruppe c**: [`nahbild_kartenrand.jpg`](nahbild_kartenrand.jpg) zeigt die Kartenecke 0|0 (jetzt frei) und drei Randübergänge. Zonengrenzen enden schräg am Rand, Knick ≤ 134°, ohne Keile.

### 3) Tests, Gate

- `pytest test_kanten.py`: **8 passed**, ohne xfail und ohne skip.
  - Neu: `test_zonen_q3_fein_alle_ringe_nur_gruppen_a_b_c` prüft alle Ringe von `zonen.geojson` mit der feinen Messart und verlangt Gruppe d = 0, Bauzone und Slots ohne Funde.
  - Die Ausnahme Wasserumriss muss leer sein.
- Q3 der gemeinsamen Bögen (QA / fein):
  - kanten 2,37 / 2,20 cm, 7,6°
  - grat 2,82 / 2,62 cm, 3,4°
  - Untergrund 2,94 / 2,73 cm, 3,5°
  - Flächentyp außerhalb der Wegenden ≤ 3,0 cm; Maximum an Wegenden 9,01 / 5,61 cm
- Flächen:
  - Wasser 0,00 %
  - Ufer −0,80 %
  - Brücke +0,29 % (gegen Rechtecke −0,63 %)
  - Weg +0,71 % (nur berichtet)
  - Bauzone −0,00005 %
- SHA-256:
  - `zonen.geojson` `0a67f16bcf2bbb6cc957fda3b4650935e3dd53ff0d23ab1c0453f6e598a88c75`
  - `kanten.geojson` und `grat.geojson` unverändert
- Gate über `export_gate.sh` mit Lochscan: **359 / R8 31 / R9 321, W1 0, Loch 0**. Die O17-Referenz `/tmp/o18m/o17.json.gz` wurde nach dem Box-Reset nach den Anweisungen in `pruefe_regeln.py` aus `f65298b` neu erzeugt; G7b-Werte unverändert. Schwellen wurden nicht geändert.

### 4) Bilder

- `../tag1_vektoren.jpg`
- `uebersicht_zonen.jpg`
- `nahbild_72_154.jpg`
- `nahbild_tripelpunkte.jpg`
- `nahbild_kartenrand.jpg`
- `uebersicht_kanten.jpg`
- `nahbild_g3h3.jpg`
- `nahbild_b3c3.jpg`

Alle sind kleiner als 1 MB und wurden angesehen. `e2_vorher_nachher.jpg` stammt unverändert aus P1c.

## P1c3 – Bauzone als Zellliste, QA F11, Messung gegen QA 33d0d86

### 1) Bauzone verlustfrei

Korrektur zu P1c2: Die dort geglättete Bauzonen-Kontur hat Löcher (Hindernisse) eingeebnet. Das ist zurückgenommen. Die Karte bleibt unverändert.

- Die Bauzone ist jetzt eine unsichtbare Logikschicht auf dem 1-m-Raster, genau wie die Slots.
- `zonen.geojson` enthält je Zusammenhangskomponente (4er-Nachbarschaft) ein `Point`-Feature am Schwerpunkt der Zellmitten. Properties:
  - `layer=bauzone_plan`, `typ=bauzone`
  - `zellen`: sortierte Liste von [x, z]
  - `flaeche_m2` = Anzahl der Zellen
  - `mittelpunkt`
  - `quelle="zellen_relief.csv: bauzone_plan"`
- Ergebnis: **31.893 Zellen** (Soll 31.893) in 25 Komponenten. Die Zellmenge ist identisch mit `neu/zellen_relief.csv`, alle 41 Löcher bleiben erhalten. Eine Kontur wird nicht gemessen und auch nicht als `vorschau=true` ausgegeben.
- Eine eigene Bauzonen-Maske gibt es in `daten/` nicht; `baue_masken.py` erzeugt nur Flächentyp-, Untergrund- und Höhenraster.
- Die Glättungshilfen (`glatte_maske`, `ring_fein`, `_ringe_ok`) wurden aus `zonen_konstruktiv.py` entfernt.
- Q3 gilt nur für sichtbare Geometrie: Flächentyp, Untergrund, Kanten, Grat und Linien.

### 2) P4-Datenschicht

- `query.mjs` liest `zonen.geojson` nicht.
- `baue_masken.py` (`lies_features`) liest die Datei und brach bisher ab (`untergrund 'WASSER_EIS'`). Außerdem wären Untergrund-Polygone mit `klasse` ins Flächenraster geflossen.
- Lösung ohne Änderung an `daten/` durch ein angepasstes Property-Schema:
  - **Flächentyp-Polygone:** `klasse` (0–5), dazu `untergrund_mehrheit` nur informativ, kein `untergrund`.
  - **Untergrund-Polygone:** `untergrund` ∈ {Schnee, Wald, Boden, Sand}, dazu `klasse_mehrheit` nur informativ, keine `klasse`.
  - `SCHATTEN` wird nach `gen_relief.py` (`ug2[ug=='SCHATTEN']='SCHNEE'`) als `Schnee` ausgegeben. `typ` behält das Quelllabel, die Partition ist unverändert.
- `baue_masken.py` rasterisiert nur Polygone, daher stören die Bauzonen- und Slot-Punkte nicht.
- Neuer Test `test_p4_datenschicht_liest_zonen` ruft `daten/baue_masken.lies_features` direkt auf.
- P4-Tests:
  - `node --test`: 23 Tests, 19 bestanden, 3 übersprungen, 1 todo, **0 fehlgeschlagen**
  - `baue_masken.py --selbsttest`: ok

### 3) QA F11 und Messung gegen QA 33d0d86

Verbindlich (QA F11): **Von Q3 ausgenommen sind nur Kartenrand und ±0,5 m um Stoßpunkte von ≥3 Zonen.** Die Ecken der Brückenrechtecke sind nicht ausgenommen.

Gemessen wurde mit `form_abw` aus `origin/art/dv2-qa` @ 33d0d86: Abtastung 0,05 m, gleitendes 1-m-Mittel, Sehnenknick. Die Funktion ist wortgleich nach `kanten/qa_form_abw.py` kopiert und wird von `test_kanten.py` direkt benutzt.

Ausnahmeradius in den Tests jetzt 0,5 m (`R_AUSNAHME`). Gruppen:
- a: Stoßpunkt von ≥3 Zonen
- b: Wegende A-DV2-01 (P1a)
- c: Kartenrand
- d: sonstige

| Schicht | a | b | c | d | max. Abweichung |
|---|---:|---:|---:|---:|---|
| Flächentyp | 1.143 | 4.554 | 930 | **0** | a 25,58 cm · b 5,5 cm · c 22,11 cm |
| Untergrund | 1.435 | – | 650 | **0** | a 23,25 cm · c 23,59 cm |

Die Werte sind Verstoßpunkte (Abweichung > 3 cm oder Knick > 15°).

- Kanten, Grat und Untergrund-Bögen nach QA 33d0d86:
  - Kanten 2,18 cm / 7,7°
  - Grat 2,61 cm / 6,2°
  - Untergrund 2,73 cm / 6,9°
  - alle innerhalb der Grenzen
- Das q3-Werkzeug von QA meldet nur die Flächentyp-Ringe von `zonen.geojson`; Wege, Ufer, Bach, Kanten und Grat haben 0 Funde.
- Gruppe b (Wegenden) ist nach F11 **nicht ausgenommen** und bleibt als bekannte Quelle P1a offen.
- **Brückenecken:** 8 Rechteckecken (E2 x186–197 z73–75, E3-West x174–186 z126–128), Umkreis 1 m: **0 Funde**. Kein P5-Platzhalter nötig. Die Brückengeometrie entsteht konstruktiv aus Wegnetz × Uferband und hat dort keine Rechteckecken.

Hinweise an QA:
- **Q14** in 33d0d86 liest die Bauzone als Polygone (`ctx.polygone`, Layer `bauzone_plan`). Mit der Zellliste würde Q14 „ohne bauzone_plan“ melden. Q14 sollte `zellen`/`flaeche_m2` der Punkt-Features lesen; es lief hier nicht, weil `mesh/manifest.json` fehlt.
- Der echte P4-Build (`baue_masken.py --out … --ohne-mesh`) bricht schon vorher an `vektor/wege.geojson` ab (`klasse 'GASSE' nicht 0-5`). Die Datei stammt nicht aus P1c.

### 4) Tests, Gate, Bilder

- `test_kanten.py`: **11 bestanden**, darunter:
  - `test_bauzone_exakt_31893_zellen_verlustfrei`
  - `test_p4_datenschicht_liest_zonen`
  - `test_qa33d0d86_q3_kanten_grat_untergrundboegen`
  - Gruppentest mit d = 0
- Gate (`export_gate.sh` mit Lochscan RAND 0,6): **359 / R8 31 / R9 321, W1 0, Loch 0**. „GATE ROT: kein Export/ZIP“ ist erwartet. `pruefung/w1_alle56_letzter_lauf.json` wurde wiederhergestellt.
- `zonen.geojson`:
  - 63 Flächentyp-Polygone, 46 Untergrund-Polygone, 25 Bauzonen-Punkte, 859 Slot-Punkte
  - SHA-256 `1c7e5d8ac2356279074895f250673f2bb6cf84277068ddb10238ad933eecaa90`
- Die Bilder wurden neu gerendert. Die sichtbare Geometrie ist unverändert, die Bilder sind bytegleich.

Kosten: 0 EUR, ohne Codex, 18:23–18:45 (Europe/Berlin).
