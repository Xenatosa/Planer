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
