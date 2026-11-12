# Ergebnis p3d24 — Vermessung des Starts von rampe_2

Stand 12.11.2026 · Worktree `/workspace/wt_dorfmap_p3d24` · Branch `art/dorfmap-p3d24` · Basis `328c8f7` (`origin/art/dorfmap-p3d23`) · Kosten **0 EUR**.

Zwischenstand nach der angeforderten Vermessung; Varianten-Solves und Gate-Proben folgen. Es wurde kein Mesh gebaut.

Marker: `[S]` direkt gemessen oder ausgeführter Prüfer-/Modellwert · `[R]` Diagnosemodell oder daraus abgeleitet · `[A]` Annahme bzw. Interpretation.

## Vermessung

`[S]` Für V29, V30 und V3 wurde `rampenwege[2]` unverändert aus den p3d21-Replays rekonstruiert. Die Startkoordinate ist jeweils `126,5100|31,6200`; Achskoordinaten und sichtbares GB-Geländeprofil stimmen in den ersten 10 m überein. `GB` am Start ist **12,469810 m**. Die gemessenen Relief-SHA-256 lauten V29 `9683b9fe…`, V30 `3a2e81dc…`, V3 `b1e347e0…`; Zellquelle, Vektorquelle und Felder wurden nicht verändert.

`[R]` Die passende p3d23-Übertragungsbasis reparametriert das Höhenprofil über die jeweilige Gesamtlänge. Darum weichen die Zielhöhen in den ersten 10 m leicht voneinander ab, obwohl Start und Gelände identisch sind.

| Geometrie | GB Start | GB-Abfall 0–4 m | Zielhöhe bei 4 m | GB-Abfall 0–10 m | Zielhöhe bei 10 m | größtes Zielgefälle im 0–10-m-Fenster |
|---|---:|---:|---:|---:|---:|---:|
| V29 | 12,46981 m | 0,41619 m | 12,14208 m | 1,44325 m | 11,14174 m | 29,93 % bei 9,3–9,6 m |
| V30 | 12,46981 m | 0,41619 m | 12,12596 m | 1,44319 m | 11,09769 m | 34,62 % bei 9,3–9,6 m |
| V3 | 12,46981 m | 0,41619 m | 12,12596 m | 1,44342 m | 11,09769 m | 34,62 % bei 9,3–9,6 m |

`[S]` Der Start ist 6,05 m von der nächsten Wand-Mittellinie Nord, 13,85 m vom nächsten Wasserpolygon und 18,93 m von der nächsten Bauzone entfernt. Das 4-m-Auslaufkern-Rechteck mit 3 m seitlicher Halbbereite liegt **nicht** in Wasser oder Bauzone; seine Mindestabstände betragen 1,19 m zur Wand-Mittellinie, 10,30 m zum Wasser und 15,71 m zur Bauzone. Die Wandabstände sind Mittellinienabstände, keine Abstände zur Wandfläche.

`[R]` Das jeweilige p3d23-Modellpaar liegt innerhalb des modellierten Start-Auslaufbereichs. An den Paarorten ist der unveränderte sichtbare Quellhöhenunterschied nur 0,00372 m (V29), 0,00032 m (V30) und 0,00185 m (V3), während das Diagnosemodell 0,172285 m gegenüber 0,10 m zulässt. Der Quellhöhen-Sprung erklärt die Modellverletzung daher nicht direkt.

| Geometrie | p3d23-Paar `x|z` | Abstand der Punkte vom Start | GB-Höhendifferenz | Modellrest über 0,10 m |
|---|---|---:|---:|---:|
| V29 | `127,25|31,25`–`127,25|31,50` | 0,99 / 0,90 m | 0,00372 m | 0,072285 m |
| V30 | `127,00|29,25`–`127,00|29,50` | 2,90 / 2,61 m | 0,00032 m | 0,072285 m |
| V3 | `126,50|29,25`–`126,50|29,50` | 2,84 / 2,54 m | 0,00185 m | 0,072285 m |

`[A]` Der Befund passt zu einem Start auf einem sich rasch versteilenden Hang: GB fällt in den ersten 4 m um 0,416 m (durchschnittlich 10,4 %), und die p3d23-Paarverletzung entsteht erst im übertragenen Rampenband/Auslauf. Wahrscheinliche Ursache ist eine ungünstige Ausrichtung bzw. zu kurze lokale Führung des Startanlaufs über dem Hangknick, nicht ein Sprung der Zellquellwerte. Das wird mit den neuen Kandidaten-Solves geprüft.

### Basiswahl

`[R]` Die p3d23-Familienfilter zeigen für V29, V30 und V3 dieselbe einzige bindende Familie: Wegende-R8a-Auslaufpaare, maximal 0,072285 m Schlupf; alle übrigen Familien haben Nullschlupf. `[S]` V3 lässt `rampe_11` unverändert und hat laut p3d21-Dokumentation die kleinsten lokalen Geometrieänderungen an `rampe_2`. Deshalb ist V3 die Arbeitsbasis. Der Kreuzungsbereich und die Achse von `rampe_11` bleiben auf dieser V3-Basis.

## Belege und Grenzen dieses Zwischenstands

- `[S]` Vollständige 0,3-m-Achsprofile, Quellhashes, Paarprojektionen und Abstände: [`p3d24_startmessung.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_startmessung.json). Reproduktionsskript: [`measure_start_profiles.py`](../../../../../codex_jobs/tools/p3d24/measure_start_profiles.py).
- `[R]` Paarorte und Modellrest stammen aus dem p3d23-Familienmodell und dem p3d23-Bericht. Die Abstände der Paarorte zum Start sowie GB-Höhendifferenzen wurden hier neu berechnet.
- `[A]` Das 4-m-Auslaufkern-Rechteck approximiert den physischen Vollgewichtbereich. Der Prüfer verwendet ein eigenes Raster; seine seitliche Geometrie ist in der Messung separat am p3d23-Diagnosekorridor dokumentiert.
- Noch nicht ausgeführt: p3d24-Varianten, Solver-IIS je Kandidat, offizielle Float32-Proben, kompletter Gate-Lauf, Mesh, `delta.py`, Tests, LOD1, `t42u` und Bilder.

## Kalibrierung und Variante 1

`[S]` Vor den Varianten wurde die offizielle R3-Kalibrierung mit der unveränderten p3d17-v22-Referenz wiederholt. Das rekonstruierte D1-Höhenfeld ist bytegleich (SHA-256 `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`); der offizielle Prüfer zählt D1 R3 `6/17/19` (längs/quer/Wölbung). Beleg: [`p3d24_R3_calibration.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_R3_calibration.json).

Variante 1 hält den Startpunkt `126,5100|31,6200` fest. Die Achse wird bis 10,8 m mit einem 45°-Konturanlauf geführt und weich an die V3-Achse angeschlossen. `[S]` Größte Verschiebung: bei Altstation 3,603 m von `129,4900|31,2601` nach `129,6504|32,5838`, **1,600 m**; die veränderten Quellpunkte reichen von 1,197 bis 10,796 m. Die lokale Achslänge wächst von 10,796 auf 11,436 m. Nur `rampenwege[2]` änderte sich; `rampe_11` und alle übrigen Reliefquellfelder blieben gleich. Neuer Quellrelief-SHA-256: `0a84ecc8faea80cb73ec941438e054990e6361dd8ff96ea64d4732a843d512e2`.

| Variante | Start vorher → nachher | größte Verschiebung | alle Familien hart | bindende Familie / minimaler Schlupf | offizielle Probe |
|---|---|---:|---|---|---|
| 1 — Konturanlauf am selben Start | `126,5100|31,6200` → `126,5100|31,6200` | 1,600 m bei `129,4900|31,2601` → `129,6504|32,5838` | infeasible, HiGHS 8 (`7.887` Variablen / `25.782` Zeilen) | `{endpoint_r8a}`; all-open und endpoint-only optimal, **0,072813 m**; all-except-endpoint infeasible | nicht ausgeführt, harte Machbarkeit verfehlt |

`[R]` Der all-open-Schlupf betrifft weiterhin nur `endpoint_r8a`. Das all-open-Maximum liegt bei `148,00|2,25`–`148,00|2,50` (Rest `0,072813 m`, nächster Endpunkt `rampe_11` Start); die endpoint-only-Gegenprobe lokalisiert ein gleich großes Paar am neuen Start von `rampe_2`, `128,00|30,25`–`128,00|30,50` (`0,172813 m` statt `0,10 m`). Gegenüber V3 p3d23 steigt der erforderliche Schlupf um `0,000528 m`; Variante 1 erfüllt das R8a-Ziel nicht.

Belege: [`p3d24_start_v1_manifest.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_start_v1_manifest.json), [`p3d24_v1_all_hard.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_v1_all_hard.json), [`p3d24_v1_family_iis.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_v1_family_iis.json). Das angeforderte offizielle Float32-Gate wurde nicht gestartet, weil der all-families-hart Solve infeasible ist.

### Variante 2

Variante 2 versetzt den Start 1,2 m entlang der linken Achsnormalen nach Norden und führt über die ersten 10,8 m zurück auf die unveränderte V3-Achse. `[S]` Start `126,5100|31,6200` → `126,6303|32,6127`, Verschiebung 1,200 m; die lokale Achslänge wächst von 10,796 auf 10,873 m. GB am Start: 12,47564 m. Startabstände: Wand-Mittellinie 6,989 m, Wasser 15,002 m, Bauzone 17,732 m. Im 4-m-Auslaufkern liegen die Mindestabstände bei 2,211 m zur Wand-Mittellinie, 11,715 m zum Wasser und 14,588 m zur Bauzone; kein Schnitt mit Wasser oder Bauzone.

| Variante | Start vorher → nachher | größte Verschiebung | alle Familien hart | bindende Familie / minimaler Schlupf | offizielle Probe |
|---|---|---:|---|---|---|
| 2 — seitlich nach Norden | `126,5100|31,6200` → `126,6303|32,6127` | 1,200 m am Start | infeasible, HiGHS 8 (`7.885` Variablen / `25.879` Zeilen) | `{endpoint_r8a}`; all-open und endpoint-only optimal, **0,415122 m**; all-except-endpoint infeasible | nicht ausgeführt, harte Machbarkeit verfehlt |

`[R]` Das all-open- und endpoint-only-Maximum liegt am neuen Start von `rampe_2`: `127,75|33,25`–`127,75|33,50`, Höhendifferenz `0,515122 m` statt `0,10 m`. Gegenüber V3 p3d23 steigt der minimale Schlupf um `0,342837 m`; Variante 2 verfehlt R8a deutlich.

Belege: [`p3d24_start_v2_manifest.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_start_v2_manifest.json), [`p3d24_v2_start_context.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_v2_start_context.json), [`p3d24_v2_all_hard.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_v2_all_hard.json), [`p3d24_v2_family_iis.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_v2_family_iis.json). Eine offizielle Float32-Probe wurde nicht gestartet.


## Variante 3 und Abschluss der drei Kandidaten

Variante 3 kombiniert einen Startversatz von 1,2 m entlang der ursprünglichen Achse mit einem 45°-Anlauf nach Süden und dem weichen Anschluss an die unveränderte Achse spätestens bei Altstation 10,8 m. `[S]` Start `126,5100|31,6200` → `127,5027|31,4997`; größte Verschiebung **1,830 m** an Altstation 3,602 m (`129,4900|31,2601` → `130,0647|29,8474`). Die Länge der ersten 10,8 m Achse sinkt von 10,796 auf 10,295 m; die Gesamtlänge von `rampe_2` sinkt von 58,878 auf 58,377 m. Nur `rampenwege[2]` wurde geändert, `rampe_11` bleibt byte-/semantisch unverändert. Quellrelief-SHA-256: `be8d02133deeb9f8a49a5707c06d88c40f10fef64ee7b8e1f52857490cf614f1`.

`[S]` Der Start liegt auf GB-Höhe 12,37637 m; im ersten 4-m-Achsenabschnitt fällt das Quellgelände 0,46589 m, und über 10 m fällt das Zielprofil 1,41186 m. Startabstände: Wand-Mittellinie 6,790 m, Wasser 14,225 m, Bauzone 18,531 m. Der näherungsweise 4-m-Auslaufbereich schneidet weder Wasser noch Bauzone; seine Mindestabstände betragen 3,490 m zur Wand-Mittellinie, 11,042 m zum Wasser und 14,306 m zur Bauzone. Wandabstände beziehen sich auf Vektor-Mittellinien, nicht Wandflächen.

| Variante | Start vorher → nachher | größte Verschiebung / lokaler Verlauf | alle Familien hart | bindende Familie und minimaler Schlupf | offizieller Float32-Probelauf |
|---|---|---|---|---|---|
| 1 — Konturanlauf am selben Start | `126,5100|31,6200` → gleich | 1,600 m bei Altstation 3,602 m; erste 10,8 m Achse 10,796 → 11,436 m; volle Route 58,878 → 59,518 m | infeasible, HiGHS 8; 7.887 Variablen / 25.782 Zeilen | `{endpoint_r8a}`, **0,072813 m** Zusatzschlupf; `all_open`-Maximum an `rampe_11`, `endpoint_only`-Maximum gleich hoch an `rampe_2` | nicht ausgeführt |
| 2 — Start 1,2 m seitlich nach Norden | `126,5100|31,6200` → `126,6303|32,6127` | 1,200 m am Start; erste 10,8 m Achse 10,796 → 10,873 m; volle Route 58,878 → 58,955 m | infeasible, HiGHS 8; 7.885 Variablen / 25.879 Zeilen | `{endpoint_r8a}`, **0,415122 m**; maximales Paar am neuen `rampe_2`-Start: `127,75|33,25`–`127,75|33,50`, Differenz 0,515122 m | nicht ausgeführt |
| 3 — 1,2 m entlang der Achse plus Anlauf nach Süden | `126,5100|31,6200` → `127,5027|31,4997` | 1,830 m bei Altstation 3,602 m; erste 10,8 m Achse 10,796 → 10,295 m; volle Route 58,878 → 58,377 m | infeasible, HiGHS 8; 7.883 Variablen / 25.539 Zeilen | `{endpoint_r8a}`, **0,183073 m**; maximales Paar liegt nun am unveränderten `rampe_11`-Start: `147,50|2,50`–`147,50|2,75`, Differenz 0,283073 m | nicht ausgeführt |

`[R]` Für jede Variante ist die Familien-IIS-Diagnose dieselbe: `all_open` und `endpoint_only` sind optimal mit R8a-Schlupf; `all_except_endpoint` ist infeasible. Damit ist im p3d23-Familienmodell ausschließlich die Endpunkt-R8a-Familie bindend, aber die Lage ihres Maximums wechselt je nach Variante. Die kleinste p3d24-Schlupfzahl hat Variante 1; sie liegt dennoch 0,000528 m über dem V3-p3d23-Wert 0,072285 m und erfüllt die 0,10-m-Paargrenze nicht. Alle R8a-Solverreste stehen in [`p3d24_variantenvergleich.json`](../../../../../codex_jobs/tools/p3d24/results/p3d24_variantenvergleich.json) und den je Variante gespeicherten `all_open`, `endpoint_only`, `all_except_endpoint`, `all_hard`- und `family_iis`-JSONs.

### Offizielle Gatezahlen, Mesh und Kachelstand

`[S]` Keine Variante besteht den vorgeschriebenen Vorab-Solve mit allen Familien hart. Daher wurde für keine Variante die offizielle Float32-Probe gestartet. Das ist ein bewusster Abbruchpunkt der Auftragslogik, keine fehlende Probe nach einer machbaren Variante.

| Messgröße | letzter verfügbarer offizieller Vergleich (p3d23 V24, Runde 2) | p3d24 Varianten 1/2/3 |
|---|---:|---|
| `pruefe_regeln` gesamt | 614; historischer Stand `9d3f8fc` 596, aktueller p3d17-Replay 600 | nicht gemessen — keine offizielle Probe |
| R8 gesamt `Stufe/Gitter/Quer/Wegende` | `9/11/7/21`, Summe 48 | nicht gemessen |
| R9 gesamt `Delle/Sägezahn/Wellen` | `35/34/275`, Summe 344 | nicht gemessen |
| R3 D1 `längs/quer/Wölbung` | `6/7/7` | nicht gemessen |
| G5 gesamt / D1 | `75/8` (Ziel `≤69/≤2`) | nicht gemessen |
| R5-Loch gesamt / D1 | `46/29` (Ziel `≤22/≤5`) | nicht gemessen |
| R4-Schlucht D1 | `0` | nicht gemessen |
| G11-Objekt gesamt / D1 | `4/2` | nicht gemessen |
| G11-Baum/Wand gesamt / D1 | `11/11` | nicht gemessen |

Die rechte Spalte ist ausdrücklich **kein p3d24-Ergebnis**. Die linke Spalte ist nur der p3d23-V24-Vergleich und belegt bereits Überschreitungen der alten Plus-5-Grenzen für G5 und R5-Loch sowie von R9-Delle; sie wird nicht als p3d24-Probe ausgegeben. Der komplette verfügbare Vergleich je Regel (historisch, letzter p3d23-Stand und Annahmen für neue Kategorien) ist in [`ERGEBNIS_p3d23.md`](ERGEBNIS_p3d23.md) aufgeführt; p3d24 hat mangels offizieller Probe für **jede** dieser Regeln keinen Nachher-Zähler. Damit sind weder „höchstens +5 je Regel“ noch die übrigen offiziellen Ziele für eine p3d24-Variante verifiziert.

| Kachel / Werte | letzter verfügbarer offizieller Vergleich p3d23 Runde 2 | p3d24 Varianten 1/2/3 |
|---|---|---|
| D1 | R8 `2/3/3/1`; R9 `13/1/13`; R3 `6/7/7`; `pruefe_regeln`: u. a. G11 Baum/Wand 11, G11-Objekt 2, G5 8, G6 2, R5 29 | keine D1-Kachelprobe |
| G1 | R8 `0/0/0/0`; R9 `0/1/12`; `pruefe_regeln`: G11-Objekt 2, G6 3, R1-blind 1, R3-längs 1, R6 3, T1 3 | keine G1-Kachelprobe |
| D2 | R8 `0/0/0/0`; R9 `0/0/0`; `pruefe_regeln`: R2 1, T1 7; Höhenhash `749d3c4b…` | keine D2-Kachelprobe; D2-Nulländerung ist nicht offiziell nachgemessen |

`[S]` Alle drei Kandidatenmanifeste bestätigen, dass nur `rampenwege[2]` geändert wurde; die übrigen Quellfelder, alle anderen Rampen und `rampe_11` sind unverändert. Die D2-Quelle wurde nicht geändert, aber mangels Probe kann ich keine unveränderten D2-Prüferzähler behaupten. Es wurde kein Mesh gebaut; folglich gibt es für p3d24 keine Mesh-Gatewerte, kein `delta.py`, keinen LOD1-Zähler, keine `pytest`-/xvfb-/Lochscan-Ausgabe, keine `t42u`-Neuberechnung und keine geforderten Vergleichsbilder. `t42u=0` und `lod1<1,3 M` sind in diesem Ergebnis nicht neu bestätigt.

### Annahmen, Grenzen und offene Punkte

- `[A]` Der 4-m-Auslaufabstand nutzt den in den Messartefakten dokumentierten Näherungs-Footprint; Wandabstände sind zu Mittellinien. Das ersetzt keine gerenderte Mesh- oder offizielle Prüfermessung.
- `[R]` Die Modell-IIS ist eine Gruppenlöschdiagnose (p3d23-Familienmodell mit Round00-leerer Ereignisschnittliste), keine row-level IIS und kein offizieller Höhenfeld-Gatebeweis. Ihre Minimalitätsaussage gilt für diese Modellformulierung und diese drei Quellgeometrien.
- `[R]` Die p3d23-Ausgangsdiagnose ordnete das größte 0,172285-m-Paar dem Startauslauf von `rampe_2` zu. In den p3d24-Neuberechnungen liegt das maximale R8a-Paar bei Variante 1 zugleich an `rampe_2` und `rampe_11`, bei Variante 3 an `rampe_11`, obwohl `rampe_11` unverändert ist. Diese Abweichung muss vor einer nächsten lokalen Änderung an `rampe_2` im Modell-/Paarumfang geklärt werden; eine vierte Variante wurde nicht angelegt.
- `[S]` Erlaubt waren höchstens drei Varianten. Alle wurden erzeugt und mit 600-s-Solverlimit seriell diagnostiziert. Kein offizieller Prüfer, Schwellwert, Zellquellwert, Overlay, Referenz, Ebenenkern, G1- oder D2-Quellfeld wurde geändert. Es wurden keine Kosten verursacht.
- Offene Punkte: End-to-end-Erreichbarkeit der R8a-Paargrenze ist nicht nachgewiesen; offizielle p3d24-Probezahlen, D1/G1/D2-Nachherzähler, Mesh-Bildvergleich, `delta.py`, LOD1, `t42u` und `pytest` fehlen absichtlich, weil alle Kandidaten im vorgeschalteten Modell infeasible waren.

## Drei-Satz-Schluss

`[S]` Alle drei erlaubten lokalen Startvarianten sind im gemeinsamen harten Familienmodell infeasible; ihre minimalen R8a-Schlupfe betragen 0,072813 m, 0,415122 m und 0,183073 m, sodass keine offizielle Float32-Probe oder ein Meshbau zulässig wurde. `[R]` Variante 1 ist nach Schlupf die beste getestete Geometrie, verfehlt aber die offizielle 0,10-m-Grenze, und die p3d24-Modelle lokalisieren zusätzlich ein maximales R8a-Paar am unveränderten Start von `rampe_11`, abweichend von der p3d23-Lokalisierung. `[A]` Deshalb bleibt das Ziel unerreicht; vor einer weiteren, separat freigegebenen Wegänderung müssen Paarumfang und R8a-Diagnose geklärt werden, und p3d24 besitzt keine offiziellen Nachher-, Mesh-, Kachel- oder Bildwerte.
