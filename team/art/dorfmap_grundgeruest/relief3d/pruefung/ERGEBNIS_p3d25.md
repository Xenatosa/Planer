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

## Variante 1 — p3d24-V1-Konturanlauf plus rampe_11 nach innen

`[S]` Kandidatenquelle `132e70af…`; nur `rampenwege[2]` und `[11]` unterscheiden sich semantisch. Alle übrigen Quellfelder und elf anderen Rampen sind unverändert. rampe_2 behält den Start `126,51|31,62` und erhält den p3d24-V1-45°-Konturanlauf bis zur 10,8-m-Einfügung; die größte lokale Verschiebung beträgt 1,600 m bei 3,602 m Station. rampe_11 wird auf den vorhandenen Achspunkt bei 8,0 m gesetzt: `148,5|2,5` → `145,3581|8,3798`, Verschiebung 8,000 m; die verbleibende Achse bleibt unverändert. Ihre Länge sinkt von 57,023 auf 49,023 m. Transferprofilwerte werden über die nächstgelegene p3d18/V24-Achsstation übernommen, sodass die unveränderten Achsabschnitte ihre bisherigen Höhenstützen behalten.

`[S]` Der rampe_11-Start liegt danach 3,987 m von der Wandmittellinie, 6,430 m vom Wasser und 28,407 m von einer Bauzone entfernt. Sein gemessener 4-m-Auslauf liegt vollständig in der Karte und schneidet weder Wasser noch Bauzone; Mindestabstände: Wand 1,964 m, Wasser 2,209 m, Bauzone 26,200 m. rampe_2 bleibt trocken und in der Karte; sein 4-m-Footprint schneidet keine Wasser-/Bauzone und liegt 1,286 m von der Wandmittellinie entfernt.

`[S]` Das all-hart Familienmodell meldet HiGHS 8 / Infeasible mit bewiesener Unlösbarkeit (7.857 Variablen, 24.116 Zeilen). Der serielle Familienfilter zeigt im all-open-Solve ausschließlich `endpoint_r8a_extra_m = 0,072813 m`; das Maximum liegt am rampe_2-Start bei `128,0|29,75`–`128,0|30,0`, gemessener Modellunterschied `0,172813 m` bei Grenze `0,10 m`. Der endpoint-only-Solve bestätigt denselben minimalen Schlupf; all-except-endpoint ist ebenfalls infeasible. `[R]` Die minimale bindende Familie ist damit R8a-Auslauf; nach dem nach innen verlegten rampe_11-Start übernimmt rampe_2 den Engpass. Eine offizielle Float32-Probe wurde nicht gestartet, da der vorgeschaltete All-Families-Hard-Solve nicht machbar ist.

Belege: [`p3d25_v1_manifest.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_manifest.json), [`p3d25_v1_start_context.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_start_context.json), [`p3d25_v1_all_hard.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_all_hard.json), [`p3d25_v1_family_iis.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_family_iis.json), Transferbasis [`p3d25_start_v1_transfer.json`](../neu/p3d25_start_v1_transfer.json). Reproduktion: `P3D25_START_VAR=1 python3 codex_jobs/tools/p3d25/apply_start_variant.py`, danach `prepare_transfer.py` und `run_family_diagnosis.py` aus `codex_jobs/tools/p3d25/`.

## Variante 2 — beide Starts entlang der Achse versetzt

`[S]` Kandidatenquelle `93c74242…`; wiederum änderten sich nur die Startabschnitte von `rampenwege[2]` und `[11]`. rampe_2 wird nach p3d24-V3 um 1,200 m entlang seiner ursprünglichen Achse nach `127,5027|31,4997` versetzt und mit 45° nach Süden bis 10,8 m zurückgeführt; die größte Verschiebung beträgt 1,830 m bei 3,602 m. rampe_11 wird wie V1 bei 8,0 m auf seiner ursprünglichen Achse neu gestartet (`145,3581|8,3798`). Beide Start-Footprints liegen trocken und in der Karte; Mindestabstände der 4-m-Ausläufe zur Wandmittellinie sind 3,490 m (rampe_2) und 1,964 m (rampe_11), zum Wasser 11,042 m beziehungsweise 2,209 m.

`[S]` All-hart: HiGHS 8 / Infeasible, bewiesen (7.853 Variablen, 23.868 Zeilen). All-open und endpoint-only benötigen jeweils mindestens **0,183073 m** R8a-Zusatzschlupf; all-except-endpoint ist infeasible. Das all-open-Maximum liegt am neuen rampe_2-Start, Paar `126,0|30,0`–`126,25|30,0`, Differenz `0,283073 m`; die endpoint-only-Maxima liegen ebenfalls am rampe_2-Start. `[R]` Der p3d24-V3-artige Startversatz verschlechtert den R8a-Auslauf gegenüber V1, obwohl der Start-Footprint sicher und trocken liegt. Eine offizielle Float32-Probe wurde nicht gestartet.

Belege: [`p3d25_v2_manifest.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_manifest.json), [`p3d25_v2_start_context.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_start_context.json), [`p3d25_v2_all_hard.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_all_hard.json), [`p3d25_v2_family_iis.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_family_iis.json), Transferbasis [`p3d25_start_v2_transfer.json`](../neu/p3d25_start_v2_transfer.json).
