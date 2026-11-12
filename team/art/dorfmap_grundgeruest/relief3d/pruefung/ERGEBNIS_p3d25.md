# Ergebnis p3d25 — gemeinsame Startabschnitte rampe_2 und rampe_11

Stand 12.11.2026 · Worktree `/workspace/wt_dorfmap_p3d25` · Branch `art/dorfmap-p3d25` · Basis `56bfab8` · Kosten **0 EUR**.

Zwischenstand nach Vermessung und R3-Kalibrierung. Es wurden keine Quellgeometrien geändert, keine Kandidaten-Solves gestartet und kein Mesh gebaut.

Marker: `[S]` direkt gemessen oder ausgeführter unveränderter Prüfer · `[R]` Modellbefund oder daraus abgeleitete Diagnose · `[A]` Annahme.

## Vermessung beider Startbereiche

`[S]` Die Reliefquelle ist weiterhin bytegleich zum p3d18-Ausgang `5e8fdb51c3f3f...`; `vektor.json` ist `aac6afff...`, `zellen_relief.csv` ist `99d30e55...`. Gemessen wurde das p3d18/V24-Profil mit `r=2,00 m`.

| Größe | rampe_2 | rampe_11 |
|---|---:|---:|
| Start `x|z` | `126,51|31,62` | `148,5|2,5` |
| GB-Höhe am Start | 12,46981 m | 12,90509 m |
| GB-Abfall 0–4 m | 0,41619 m | 0,46654 m |
| V24-Zielhöhenabfall 0–4 m | 0,34384 m | 0,38205 m |
| GB-Abfall 0–10 m | 1,44315 m | 1,44736 m |
| V24-Zielhöhenabfall 0–10 m | 1,37212 m | 1,26799 m |
| größtes absolutes Profilgefälle 0–10 m | 34,62 % bei 9,3–9,6 m | 40,38 % bei 9,0–9,3 m |
| Abstand Start zur Wandmittellinie | 6,050 m | 1,149 m |
| Abstand Start zum Wasser | 13,846 m | 1,800 m |
| Abstand Start zur Bauzone | 18,925 m | 33,266 m |
| 4-m-Auslauf: Wand / Wasser / Bauzone | 1,191 / 10,303 / 15,713 m | 0 / 0 / 30,036 m |
| 4-m-Auslauf außerhalb Karte / Wasser-/Bauzonenschnitt | nein / nein | ja / Wasserschnitt, kein Bauzonenschnitt |

`[S]` Der `rampe_11`-Startpunkt selbst ist innerhalb der Karte und liegt außerhalb der Wasser- und Bauzonenpolygone. Sein angenäherter Auslauf-Footprint mit voller 4-m-Auslaufzone, 3-m-Seitenhalbbreite und 1,2-m-Innenbereich reicht jedoch 1,942 m über den Kartenrand hinaus, schneidet Wasser und berührt eine Wandmittellinie. Diese Startgeometrie ist deshalb kein zulässiges gemeinsames Kandidatenziel.

`[S]` Das p3d24-V1-R8a-Paar an `rampe_11`, `148,0|2,25`–`148,0|2,5`, hat laut gespeichertem Modell einen Höhenunterschied von 0,172813 m bei 0,10-m-Grenze; das gleich hohe endpoint-only-Maximum liegt an `rampe_2` bei `128,0|30,25`–`128,0|30,5`. Auf der unveränderten Quell-GB-Oberfläche betragen die Höhenunterschiede dieser Paare nur 0,012154 m beziehungsweise 0,019335 m. Der Modellrest entsteht damit nicht durch einen entsprechenden Sprung der Zellquellwerte.

`[R]` Beide Starts liegen räumlich weit auseinander; es gibt keinen Beleg für gemeinsame lokale Rasterzellen. Im Familienmodell laufen beide R8a-Auslauf-Paarmengen in dieselbe globale Höhenfeldoptimierung und dieselbe skalare `endpoint_r8a_extra_m`-Lockerung ein. R3-, Achs-, Ebenenkern-, Kreuzungs-, Wegneigungs- und Variablen-Grenzen gelten ebenfalls in diesem gemeinsamen Solve. Wird `rampe_2` verbessert, kann daher das unveränderte R8a-Maximum am `rampe_11`-Start den globalen Schlupf übernehmen; das ist der dokumentierte Wechsel des Engpasses, keine lokale Kopplung der beiden Starts durch Nachbarschaft.

`[R]` Die p3d24-V1-Modellfilterdiagnose zeigt 0,072813 m endpoint-R8a-Schlupf sowohl im all-open- als auch im endpoint-only-Solve; ohne die Endpunktfamilie ist der Familienfilter-Solve infeasible. Der Modelloutput lokalisiert im all-open-Lauf das Maximum am `rampe_11`-Paar oben. Eine Zeilen-IIS liegt nicht vor; die genaue einzelne Höhenfeldzeile, die das Paar auf 0,172813 m hält, ist daher nicht belegt. Die p3d24-Kandidaten ließen `rampe_11` unverändert und erklären den Wechsel zu diesem Paar durch das stehengebliebene globale Maximum.

## Kalibrierung

`[S]` Die offizielle R3-Kalibrierung auf der p3d17-Referenz stimmt bytegenau überein: D1-Höhenhash `26b849f6…`, R3 D1 längs/quer/Wölbung `6/17/19`. Beleg: [`p3d25_R3_calibration.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_R3_calibration.json).

## Belege und nächster Stand

- `[S]` Startprofile, GB-Höhen, Abstände, Footprints, Quellhashes und die drei bekannten p3d24-R8a-Paare: [`p3d25_startmessung.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_startmessung.json). Reproduktion: [`measure_start_coupling.py`](../../../../../codex_jobs/tools/p3d25/measure_start_coupling.py).
- `[R]` Das 4-m-Auslaufpolygon ist eine Messnäherung; Wandabstände sind Mittellinienabstände, nicht Wandflächenabstände.
- `[A]` Der erste zulässige `rampe_11`-Startkandidat muss so weit in die Karte hineinrücken, dass der ganze Auslauf-Footprint trocken, wandfrei und innerhalb des Kartenrands liegt.
- Noch offen: höchstens drei gemeinsame lokale Varianten, Familien-IIS/Schlupf je Variante, offizielle Float32-Proben für machbare Kandidaten, Gatezahlen, Mesh, Delta, Tests, t42u und Bilder.
