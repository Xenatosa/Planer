# Ergebnis p3d25 — gemeinsame Startabschnitte rampe_2 und rampe_11

Stand 12.11.2026 · Worktree `/workspace/wt_dorfmap_p3d25` · Branch `art/dorfmap-p3d25` · Basis `56bfab8` · Kosten **0 EUR**.

Abschlussstand nach Vermessung und drei gemeinsamen Startvarianten. Die offizielle Reliefquelle wurde nicht geändert; Kandidatenreliefs lagen nur unter `/tmp`. Kein Kandidat war all-hart machbar, deshalb gab es keine offizielle Float32-Probe und keinen Meshbau.

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
- Die drei erlaubten Varianten, Familienfilter-Ergebnisse, Regel-/Kachel-Ausgangsstände und bewusst nicht ausgeführten Folgeschritte stehen unten.

## Variante 1 — p3d24-V1-Konturanlauf plus rampe_11 nach innen

`[S]` Kandidatenquelle `132e70af…`; nur `rampenwege[2]` und `[11]` unterscheiden sich semantisch. Alle übrigen Quellfelder und elf anderen Rampen sind unverändert. rampe_2 behält den Start `126,51|31,62` und erhält den p3d24-V1-45°-Konturanlauf bis zur 10,8-m-Einfügung; die größte lokale Verschiebung beträgt 1,600 m bei 3,602 m Station. rampe_11 wird auf den vorhandenen Achspunkt bei 8,0 m gesetzt: `148,5|2,5` → `145,3581|8,3798`, Verschiebung 8,000 m; die verbleibende Achse bleibt unverändert. Ihre Länge sinkt von 57,023 auf 49,023 m. Transferprofilwerte werden über die nächstgelegene p3d18/V24-Achsstation übernommen, sodass die unveränderten Achsabschnitte ihre bisherigen Höhenstützen behalten.

`[S]` Der rampe_11-Start liegt danach 3,987 m von der Wandmittellinie, 6,430 m vom Wasser und 28,407 m von einer Bauzone entfernt. Sein gemessener 4-m-Auslauf liegt vollständig in der Karte und schneidet weder Wasser noch Bauzone; Mindestabstände: Wand 1,964 m, Wasser 2,209 m, Bauzone 26,200 m. rampe_2 bleibt trocken und in der Karte; sein 4-m-Footprint schneidet keine Wasser-/Bauzone und liegt 1,286 m von der Wandmittellinie entfernt.

`[S]` Das all-hart Familienmodell meldet HiGHS 8 / Infeasible mit bewiesener Unlösbarkeit (7.857 Variablen, 24.116 Zeilen). Der serielle Familienfilter zeigt im all-open-Solve ausschließlich `endpoint_r8a_extra_m = 0,072813 m`; das Maximum liegt am rampe_2-Start bei `128,0|29,75`–`128,0|30,0`, gemessener Modellunterschied `0,172813 m` bei Grenze `0,10 m`. Der endpoint-only-Solve bestätigt denselben minimalen Schlupf; all-except-endpoint ist ebenfalls infeasible. `[R]` Die minimale bindende Familie ist damit R8a-Auslauf; nach dem nach innen verlegten rampe_11-Start übernimmt rampe_2 den Engpass. Eine offizielle Float32-Probe wurde nicht gestartet, da der vorgeschaltete All-Families-Hard-Solve nicht machbar ist.

Belege: [`p3d25_v1_manifest.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_manifest.json), [`p3d25_v1_start_context.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_start_context.json), [`p3d25_v1_all_hard.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_all_hard.json), [`p3d25_v1_family_iis.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v1_family_iis.json), Transferbasis [`p3d25_start_v1_transfer.json`](../neu/p3d25_start_v1_transfer.json). Reproduktion: `P3D25_START_VAR=1 python3 codex_jobs/tools/p3d25/apply_start_variant.py`, danach `prepare_transfer.py` und `run_family_diagnosis.py` aus `codex_jobs/tools/p3d25/`.

## Variante 2 — beide Starts entlang der Achse versetzt

`[S]` Kandidatenquelle `93c74242…`; wiederum änderten sich nur die Startabschnitte von `rampenwege[2]` und `[11]`. rampe_2 wird nach p3d24-V3 um 1,200 m entlang seiner ursprünglichen Achse nach `127,5027|31,4997` versetzt und mit 45° nach Süden bis 10,8 m zurückgeführt; die größte Verschiebung beträgt 1,830 m bei 3,602 m. rampe_11 wird wie V1 bei 8,0 m auf seiner ursprünglichen Achse neu gestartet (`145,3581|8,3798`). Beide Start-Footprints liegen trocken und in der Karte; Mindestabstände der 4-m-Ausläufe zur Wandmittellinie sind 3,490 m (rampe_2) und 1,964 m (rampe_11), zum Wasser 11,042 m beziehungsweise 2,209 m.

`[S]` All-hart: HiGHS 8 / Infeasible, bewiesen (7.853 Variablen, 23.868 Zeilen). All-open und endpoint-only benötigen jeweils mindestens **0,183073 m** R8a-Zusatzschlupf; all-except-endpoint ist infeasible. Das all-open-Maximum liegt am neuen rampe_2-Start, Paar `126,0|30,0`–`126,25|30,0`, Differenz `0,283073 m`; die endpoint-only-Maxima liegen ebenfalls am rampe_2-Start. `[R]` Der p3d24-V3-artige Startversatz verschlechtert den R8a-Auslauf gegenüber V1, obwohl der Start-Footprint sicher und trocken liegt. Eine offizielle Float32-Probe wurde nicht gestartet.

Belege: [`p3d25_v2_manifest.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_manifest.json), [`p3d25_v2_start_context.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_start_context.json), [`p3d25_v2_all_hard.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_all_hard.json), [`p3d25_v2_family_iis.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v2_family_iis.json), Transferbasis [`p3d25_start_v2_transfer.json`](../neu/p3d25_start_v2_transfer.json).

## Variante 3 — V1-Konturanlauf verlängert, rampe_11 8,5 m nach innen

`[S]` Kandidatenquelle `93b2e850…`. rampe_2 behält den p3d24-V1-Start `126,51|31,62`, den 45°-Konturanlauf und den weichen Anschluss, verlängert auf 12,0 m; maximale lokale Verschiebung 1,764 m bei 3,602 m. rampe_11 wird auf `145,1593|8,7460` neu gestartet, 8,500 m entlang seiner bestehenden Achse; der Rest der Achse bleibt unverändert. Alle übrigen Rampen, Quellfelder und der Abschnitt von rampe_2 nach 12 m bleiben semantisch unverändert.

`[S]` Beide 4-m-Ausläufe bleiben trocken, innerhalb der Karte und außerhalb von Bauzonen. Die rampe_11-Footprintabstände betragen 1,978 m zur Wandmittellinie und 1,965 m zum Wasser; der Kartenrandabstand ist 5,690 m. Der rampe_2-Footprint bleibt 1,324 m von der Wandmittellinie und 8,856 m vom Wasser entfernt.

`[S]` All-hart: HiGHS 8 / Infeasible, bewiesen (7.855 Variablen, 23.962 Zeilen). All-open und endpoint-only benötigen jeweils **0,072813 m** R8a-Zusatzschlupf; all-except-endpoint ist infeasible. Das all-open-Maximum liegt am rampe_2-Start, Paar `127,75|31,0`–`127,75|31,25`, Differenz `0,172813 m`; endpoint-only findet denselben Maximalwert bei `128,25|30,0`–`128,25|30,25`. `[R]` Die längere V1-Führung verbessert die Schlupfzahl gegenüber V2, erreicht aber nicht null. Eine offizielle Float32-Probe wurde nicht gestartet.

Belege: [`p3d25_v3_manifest.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v3_manifest.json), [`p3d25_v3_start_context.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v3_start_context.json), [`p3d25_v3_all_hard.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v3_all_hard.json), [`p3d25_v3_family_iis.json`](../../../../../codex_jobs/tools/p3d25/results/p3d25_v3_family_iis.json), Transferbasis [`p3d25_start_v3_transfer.json`](../neu/p3d25_start_v3_transfer.json).

## Gemeinsame Variantentabelle und Gatewerte

| Variante | rampe_2 Start vorher → nachher; Verschiebung | rampe_11 Start vorher → nachher; Verschiebung | beide Start-Footprints | All-Families-Hard | minimale R8a-Lockerung und Ort | offizielle Float32-Probe |
|---|---|---|---|---|---|---|
| 1 | `126,51|31,62` → gleich; 0 m; V1-Konturanlauf, max. lokale Verschiebung 1,600 m | `148,5|2,5` → `145,3581|8,3798`; 8,000 m | trocken, innerhalb Karte, keine Bauzone; Wand/Wasser min. 1,286/2,209 m | infeasible, HiGHS 8 bewiesen | **0,072813 m**; `128,0|29,75`–`128,0|30,0`; delta 0,172813 m | nicht ausgeführt |
| 2 | `126,51|31,62` → `127,5027|31,4997`; 1,200 m; V3-Südturn, max. lokale Verschiebung 1,830 m | `148,5|2,5` → `145,3581|8,3798`; 8,000 m | trocken, innerhalb Karte, keine Bauzone; Wand/Wasser min. 1,964/2,209 m | infeasible, HiGHS 8 bewiesen | **0,183073 m**; `126,0|30,0`–`126,25|30,0`; delta 0,283073 m | nicht ausgeführt |
| 3 | `126,51|31,62` → gleich; 0 m; V1-Konturanlauf bis 12 m, max. lokale Verschiebung 1,764 m | `148,5|2,5` → `145,1593|8,7460`; 8,500 m | trocken, innerhalb Karte, keine Bauzone; Wand/Wasser min. 1,324/1,965 m | infeasible, HiGHS 8 bewiesen | **0,072813 m**; `127,75|31,0`–`127,75|31,25`; delta 0,172813 m | nicht ausgeführt |

`[S]` Für alle drei Kandidaten ist im Familienfilter ausschließlich `endpoint_r8a_extra_m` positiv; der endpoint-only-Solve erreicht denselben Wert, und der Solve ohne endpoint-R8a-Familie bleibt infeasible. Die Wegende-Stufenfamilie bleibt im all-open-Modell bei 0 Zusatzschlupf gegen `≤0,054 m`; die R8a-Grenze `≤0,10 m` wird bei keinem Kandidaten gehalten. Die Gatezahlen zu G5, R5-Loch, R4, R3, R8/R9 und den übrigen offiziellen Regeln sind für alle Kandidaten **nicht gemessen**, weil die vorgeschaltete All-Families-Hard-Bedingung scheiterte.

`[S]` Unverändert im Modell waren R8-Stufe `≤0,116 m`, Gitter `≤0,019 m`, Quergefälle `≤2,95 %`, Einzelquerung `≤19,5 %`, R3 D1 `≤6/≤7/≤7`, Achs- und Ebenenstützen `±0,02 m`, Ebenenkern `r=2,00 m`, Wegende `≤0,054 m` und R8a `≤0,10 m`. Das Familienmodell enthielt zusätzlich die unveränderten Zählergrenzen G5 gesamt/D1 `≤69/≤2`, R5-Loch gesamt/D1 `≤22/≤5` und R4-Schlucht D1 `0`; alle 22 p3d23-Familien waren im All-Hard-Lauf aktiv.

`[R]` Die R8-Kreuzung bleibt nach offizieller Clusterrekonstruktion bei allen drei Kandidaten in der Anzeige `152,5|28,5`; ungerundete Zentren sind V1 `152,544096|28,491539`, V2 `152,543887|28,489836`, V3 `152,542343|28,498905`. Sie wurde nicht verschoben; die Maximalabweichung zum ursprünglichen ungerundeten Zentrum beträgt unter 0,008 Karten-Einheiten.

## Regel- und Kachelzahlen vorher / nachher

`[S]` Die Spalte „9d3f8fc vorher“ verwendet den archivierten Ausgangsstand. `p3d25 V1/V2/V3 nachher` ist überall **nicht gemessen**: Der offizielle Gate-Probelauf wurde nach den bewiesenen infeasiblen All-Families-Hard-Solves korrekt nicht gestartet. D1/G1/D2 in der vierten Spalte sind der letzte vollständige p3d17-Referenzreplay im aktuellen Prüferschema und dienen nur als Kachelkontext; dieser Replay zählt `600` statt historisch `596`, weil G11 darin mit 4 Treffern (D1=2, G1=2) enthalten ist.

| Regel | 9d3f8fc vorher gesamt | letzter Referenzreplay D1/G1/D2 | p3d25 V1/V2/V3 nachher |
|---|---:|---|---|
| R1_blind | 24 | 2 / 1 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R2_getrennt | 15 | 1 / 0 / 1 | nicht gemessen / nicht gemessen / nicht gemessen |
| R3_laengs_m | 35 | 6 / 1 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R3_quer_pct | 29 | 17 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R3_woelb_m | 31 | 19 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R4_rand | 1 | 1 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R4_schlucht | 0 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R5_loch | 25 | 8 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R5_spitze | 0 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R6_wasser_schnee | 4 | 0 / 3 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G2_spitze_oben | 3 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G2_spitze_oben_fein | 8 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G3_spitze_unten | 4 | 1 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G3_spitze_unten_fein | 2 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G5_beule_klippe | 69 | 2 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G6_facette | 219 | 3 / 3 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G7_wand_glatte_flaeche | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G7b_wandkontur_feld | 25 | 1 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G7b_wandkontur_kantenschaerfe | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G7b_wandkontur_rauheit | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G8_fluss_nicht_bis_rand | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| G11_objekt_schwebt_sinkt | 0* | 2 / 2 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| T1_fleckrand | 94 | 0 / 3 / 7 | nicht gemessen / nicht gemessen / nicht gemessen |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| T3_streifen_ringe_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| **pruefe_regeln Summe** | **596** | **D1/G1/D2 nicht direkt vergleichbar; aktueller Replay gesamt 600** | **nicht gemessen** |
| R8_stufe | 9 | 2 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R8_gitter | 10 | 2 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R8_quer | 5 | 0 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R8a_wegende | 24 | 3 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| **R8 Summe** | **48** | **D1=7 / G1=0 / D2=0 im p3d17-Replay (dessen Gesamt 46)** | **nicht gemessen** |
| R8b_delle | 25 | 1 / 0 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R9_saegezahn | 34 | 1 / 1 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| R9w_wellen | 275 | 27 / 12 / 0 | nicht gemessen / nicht gemessen / nicht gemessen |
| **R9 Summe** | **334** | **D1=29 / G1=13 / D2=0 im p3d17-Replay (dessen Gesamt 344)** | **nicht gemessen** |

`*` Das archivierte 596er-Prüferschema enthielt keinen G11-Zähler; der aktuelle Replay zählt G11=4. D2 blieb als Quell-/Meshbasis unverändert: Höhenhash `749d3c4b…` im letzten gebauten p3d18-V24-Stand. Weil kein p3d25-Mesh und keine offizielle Probe erzeugt wurden, kann ich weder „keine neuen D2-Treffer“ aus einem Nachher-Prüferlauf noch `t42u=0` oder `lod1<1,3 Mio.` neu bestätigen. Der Ergebnisstatus ist **nicht erreicht / nicht verifiziert**, nicht bestanden.

Für neue Läufe setzt `P3D25_START_VAR` die Varianten `1`, `2` oder `3`; der Standard `1` ist die beste getestete Auswahl, weil V1 und V3 gleich viel Schlupf benötigen, V1 aber die kleinere Gesamtverschiebung beider Starts hat.

## Was nicht ausgeführt wurde

`[S]` Da keine Geometrievariante die R8a-Hartgrenze erfüllt, gab es keine offizielle Float32-Checker-in-the-loop-Runde, keine Mesh-Erzeugung, keinen Build mit `python3 gen_relief.py && python3 baue_html.py`, keine Mesh-Gate-Probe, keine Delta-Vergleiche, keinen `pytest`-Lauf, keinen xvfb-Lochscan, keinen `t42u`-Lauf, keine LOD1-Zählung und keine Bilder unter `bilder_p3d25/`. Diese Schritte waren laut Auftrag nur nach einem machbaren Kandidaten und bestandener offizieller Probe zulässig. `mesh.py`, Prüfer, Schwellen, Zellen, Overlay, `vektor.json`, Felder, Wände, Wasser, Bauzonen, G1/D2-Quellbereiche und alle Rampen außerhalb der beiden Startabschnitte blieben unverändert.

## Annahmen, Grenzen und offene Punkte

- `[A]` Die Auslauf-Footprintmessung nutzt ein Rechteck entlang des Endpunkttangenten mit `−1,2…+4,0 m` und `±3,0 m`; das ist eine Näherung des vollen 4-m-Gewichtskerns. Wandabstände messen Mittellinien, nicht Wandflächen.
- `[A]` Für die Varianten wurden die p3d18-Höhenprofile auf die nächstgelegene unveränderte Achsstation projiziert; dadurch bleiben Höhenstützen auf unveränderten Geometrieabschnitten stationstreu. Das ist keine offizielle Meshhöhe.
- `[R]` Familienfilter und all-open Restwerte sind Gruppen-IIS-Diagnosen, keine Zeilen-IIS. Der genaue einzelne Transferkoeffizient bzw. Modellrow, der das 0,172813-m-Paar hält, ist daher nicht identifiziert.
- `[R]` Das p3d24-Paar am `rampe_11`-Start (`148,0|2,25`–`148,0|2,5`) unterscheidet sich auf Quell-GB nur um 0,012154 m, während der p3d24-V1-Modelloutput 0,172813 m ausweist. Zusammen mit dem gemessenen alten Auslauf, der Wasser, Wand und Kartenrand schneidet, spricht das für die Interaktion des lokalen Endpunkt-Auslaufs mit dem festen Rand-/Wand-/Wasserhintergrund und dem gemeinsamen Höhenfeldmodell, nicht für einen Quellzellen-Sprung. Ohne Zeilen-IIS bleibt diese konkrete Constraint-Zuordnung eine Diagnose, kein bewiesener Einzelursachenbeleg.
- `[S]` Der Engpasswechsel ist im p3d24-Modell direkt sichtbar: V1 hat gleich hohe R8a-Maxima an beiden Starts (`0,172813 m` Paarunterschied); V3 lässt rampe_11 unverändert und das all-open-Maximum steigt dort auf `0,283073 m` (`0,183073 m` Schlupf). Ein globales `endpoint_r8a_extra_m`-Maximum wird durch den jeweils größten Startpaarrest bestimmt; wenn rampe_2 verbessert wird, bleibt der unveränderte rampe_11-Rest als Maximum stehen. p3d25-V1/V3 bestätigen den umgekehrten Wechsel: nach sicherem Zurücksetzen von rampe_11 liegt das Maximum wieder an rampe_2.
- Ergebnis und offene Folge: Das Ziel ist mit den drei erlaubten Startvarianten nicht erreicht; es gibt keinen Nachweis für die offiziellen Gate-/Meshziele. Eine weitere Geometrievariante oder Schwellenänderung wurde nicht vorgenommen.

## Drei-Satz-Schluss

`[S]` Alle drei gemeinsamen Startvarianten sind im all-hart p3d23-Familienmodell bewiesen infeasible; der minimale R8a-Schlupf beträgt 0,072813 m, 0,183073 m und 0,072813 m. `[S]` Die rampe_11-Verschiebungen bringen beide 4-m-Ausläufe in trockene, wandfreie und kartengültige Bereiche, doch der Engpass liegt danach wieder am rampe_2-Start; deshalb wurden keine offiziellen Proben oder ein Mesh gebaut. `[A]` Das p3d25-Ziel ist unerreicht und die Regel-/Kachel-Nachherzahlen, D2-Regression, `t42u` und LOD1 sind mangels zulässigem Probe-/Meshschritt nicht neu verifiziert.
