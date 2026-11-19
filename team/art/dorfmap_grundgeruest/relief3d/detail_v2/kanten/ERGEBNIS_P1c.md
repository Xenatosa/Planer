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
