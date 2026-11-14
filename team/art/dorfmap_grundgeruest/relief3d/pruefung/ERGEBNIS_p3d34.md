# Ergebnis p3d34

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d34` · Branch `art/dorfmap-p3d34` · Basis `origin/art/dorfmap-p3d33` @ `af9c86a` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen · `[R]` Modell-/Diagnosebefund · `[A]` Annahme oder Grenze · `[F]` Entscheidung. Laufzeitnachweis: `/workspace/codex_jobs/log_p3d34.txt` (`gpt-6-luna`, reasoning effort `xhigh`).

## Ergebnis

`[F]` Der p3d33-V1-Hart-LP bleibt auch nach Ersetzung der Start-Bestandsfixierung durch die offiziellen Startbedingungen infeasible. Der gültige HiGHS-IIS liegt unabhängig davon an rampe_11-Station 83,4 m und der festgehaltenen Kreuzungsplattform; gemäß B3 stoppt p3d34 hier. Es gibt keine zulässige Float32-Probe, keine Regel-Nachherzahlen und keinen Meshbau.

`[R]` Der ursprüngliche 1,655529-mm-Befund stammt aus der internen Gleichsetzung der rampe_2-Profilhöhe mit p3d31 V3, nicht aus der offiziellen R8a-Paarbedingung: Im p3d33-All-Familien-Filter liegt der Diagnosewert an Station 0 bei 12,4681540031 m gegenüber dem festen Wert 12,4698095322 m. Zusätzlich fixierte p3d33 die finale Meshhöhe am selben Startpunkt auf den Bestand. Nach Freigabe beider Bestandsgleichsetzungen wandert derselbe maximal notwendige Bounds-Schlupf im All-Familien-Filter zur ersten weiterhin festgesetzten Stützstelle bei Station 0,3 m.

## A. Diagnose

### A1. IIS und gezielte Lockerungen

`[S]` Das originale V1-Modell mit Fenster 25–50 m wurde als reines LP mit 20.411 Variablen, 76.458 Zeilen, null Integer-Variablen, einem Thread und 600 s Zeitlimit gerechnet. HiGHS 1.15.1 meldete `Infeasible` (Code 8). Die LP-IIS-Suche wurde mit `iis_strategy=6` ausgeführt (Elasticity-Filter, danach Reduktion auf ein IIS, wie p3d31 Schritt 0); sie lieferte ein gültiges IIS mit 9 Zeilen und 10 Spalten. JSON und exportiertes IIS stehen unter [p3d34_V1_step_objective_iis.json](../../../../../codex_jobs/tools/p3d34/results/p3d34_V1_step_objective_iis.json) und [p3d34_V1_step_objective_iis.iis.lp](../../../../../codex_jobs/tools/p3d34/results/p3d34_V1_step_objective_iis.iis.lp).

`[R]` Dieses IIS enthält keine rampe_2-Startzeile. Es bindet rampe_11-Profilstation 83,4 m an eine minimale Profilhöhe von 4,07532125397 m, die Achsstützung mit ±0,02 m, den auf 4,05450512283 m fixierten Endmeshwert bei `[152,5|28,5]` sowie die Ebenenkern-Stützzeilen. Nach Abzug der maximalen Achsstützung muss der angrenzende Meshwert mindestens 4,05532125397 m betragen; das sind rund 0,000816131 m mehr als der fest fixierte Kreuzungsanker. Das ist ein unabhängiger Konflikt, der weder die rampe_2-Höhe noch deren R8a-Schwelle enthält.

`[S]` Die separat gezielten Einzel-Lockerungen wurden auf dem ursprünglichen V1-LP gerechnet. Jeweils 0,00165552907 m nach unten nur an der rampe_2-Profiluntergrenze oder nur an der finalen Mesh-Startankerzeile zu erlauben, ergab weiter `Infeasible` und dasselbe gültige 9-Zeilen-IIS am Kreuzungsanker. Die einzeln aktivierten R8a- und Endpunktstufen-Slackgruppen ließen den LP ebenfalls infeasible; sie liefern daher keinen zulässigen Punkt und keinen tatsächlichen Lockerungswert. Belege: [Profilgrenze](../../../../../codex_jobs/tools/p3d34/results/p3d34_A1_start_profile_bound_only.json), [Meshanker](../../../../../codex_jobs/tools/p3d34/results/p3d34_A1_start_mesh_anchor_only.json), [R8a-Gruppe](../../../../../codex_jobs/tools/p3d34/results/p3d34_A1_only_endpoint_r8a.json), [Endstufengruppe](../../../../../codex_jobs/tools/p3d34/results/p3d34_A1_only_endpoint_stage.json).

| Lauf / gelockerte Familie | Status | Schlupf / Ort | Aussage |
|---|---|---|---|
| p3d33-V1, alle Familien elastisch | Optimal | `variable_bounds_extra_m = 0,00165552907 m`, rampe_2 Station 0, `[126,51000021|31,62000173]`; fest `12,46980953217 m`, Diagnose `12,46815400310 m` | einziger positiver Gruppenfilter-Schlupf; kein Hart-LP-Punkt |
| nur Profiluntergrenze am Start um 1,655529 mm geöffnet | Infeasible, gleiches IIS | kein zulässiger Schlupfpunkt | behebt den globalen LP-Konflikt nicht |
| nur finalen Meshanker am Start um 1,655529 mm nach unten geöffnet | Infeasible, gleiches IIS | kein zulässiger Schlupfpunkt | behebt den globalen LP-Konflikt nicht |
| nur R8a-Slackgruppe / nur Endstufen-Slackgruppe | jeweils Infeasible, gleiches IIS | kein zulässiger Schlupfpunkt | die offiziellen Schwellen sind nicht die IIS-Ursache |
| p3d34-V1, vollständige offizielle Startpolitik, alle Familien elastisch | Optimal, `objective_mode=diagnostic` | einziger positiver Schlupf wieder `variable_bounds_extra_m = 0,00165552907 m`, jetzt rampe_2 Station 0,3, `[126,75818383|31,58992031]`; fest `12,44815635681 m`, Diagnose `12,44650082774 m` | Startpin entfernt; nächster außerhalb des 25–50-m-Fensters festgesetzter Profilpunkt bindet |
| p3d34-V1, vollständige offizielle Startpolitik, Hart-LP | Infeasible | 20.411 Variablen, 76.454 Zeilen, 0 Integer-Variablen | STOPP nach B3 |

`[R]` Der All-Familien-Filter im letzten Lauf hatte an der Startausnahme null zusätzlichen R8a-Schlupf. Sein gemessenes Maximum war `0,1800000000000015 m` bei der Paarung `[126,5|29,25]`–`[126,5|29,5]` gegenüber `0,18 m`; der Überschuss von `1,5 × 10⁻¹⁵ m` ist Float64-Rundungsrest des LP, keine 1,655-mm-Abweichung. Die separate Endstufenbedingung lag bei `0,05400000000000038 m` am Paar `[153,25|36,75]`–`[153,5|36,75]` und ebenfalls ohne positiven Gruppen-Slack. JSON: [p3d34_B3_V1_official_full_start_all_family_filter.json](../../../../../codex_jobs/tools/p3d34/results/p3d34_B3_V1_official_full_start_all_family_filter.json). Der korrigierte Hart-LP und sein IIS sind [hier](../../../../../codex_jobs/tools/p3d34/results/p3d34_B2_V1_official_full_start_hard_lp.json) und [hier](../../../../../codex_jobs/tools/p3d34/results/p3d34_B2_V1_official_full_start_iis.json) abgelegt.

`[S]` Ein zusätzlicher gemeinsamer elastischer Solve mit `objective_mode=step` ist als [p3d34_B2_V1_official_full_start_lp.json](../../../../../codex_jobs/tools/p3d34/results/p3d34_B2_V1_official_full_start_lp.json) erhalten. Er ist `Optimal` nur mit vielen gleichzeitig erlaubten Familien-Slacks und kein Hart-LP-/Float32-Kandidat: unter anderem `variable_bounds_extra_m=0,926494 m` bei rampe_11 Station 3,9 m, `grade_same_extra_m=0,535739 m`, `endpoint_stage_extra_m=0,078885 m` und `endpoint_r8a_extra_m=0,078341 m`. Für den entscheidenden Gruppenbefund wird der getrennte `objective_mode=diagnostic`-Filter oben verwendet.

### A2. Einordnung gegen die unveränderten Prüfer

| Bedingung im Modell | Modellformulierung / Befund | Offizielle Prüferdefinition | Urteil |
|---|---|---|---|
| `P3D20_ENDPOINT_R8A_LOCK=1`, rampe_2 Anfang | Im p3d20-Ursprungsmodell schaltete dieses Flag symmetrische Paargrenzen `|h(a)-h(b)| ≤ 0,10 m` für alle Endpunkte ein; es fixierte keine absolute Starthöhe. p3d23–p3d33 verwenden inzwischen `r8a_pair_limit_m`; am benannten rampe_2-Start wird damit `0,18 m`, sonst `0,10 m` angesetzt. | `r8_kreuzung.py` prüft im 4-m-Auslauf benachbarte Höhenpaare; `r8a_policy.py` wählt `0,18 m` ausschließlich für `rampe_2_anfang` bei `[126,51|31,62]` (Koordinatentoleranz `1e-5` Map-Einheiten). | Ursprünglicher einheitlicher 0,10-m-Modellwert wäre am Start strenger. **Im p3d33/p3d34-Modell ist die Paarbedingung gleich offiziell**, und im Filter bindet sie bei 0,18 m. Sie erzwingt die 1,655 mm nicht. |
| Endpunktstufe `0,054 m` | Symmetrischer benachbarter Paar-Cap; p3d34 lässt ihn unverändert. Der beobachtete bindende Paarpunkt liegt nicht am rampe_2-Start. | Der offizielle R8-Stufenprüfer meldet erst bei `>0,20 m`; das Nutzerziel setzt Wegendstufe separat auf `≤0,054 m`. | Strenger als der allgemeine R8-Schwellenwert, aber explizites Projektziel und **nicht Ursache am rampe_2-Start**. |
| p3d31-V3-Profilpin bei rampe_2 Station 0 | `lo=hi=12,469809532165527 m`; Gruppenfilter fordert `12,468154003095497 m`. | Kein offizieller Prüfer verlangt, dass die absolute Rampenhöhe am Start dem p3d31-Bestand entspricht. R3 zählt Abschnittsresiduen/Quergefälle/Wölbung; R8/R8a begrenzen lokale Differenzen. | **Strenger als offiziell.** |
| p3d33 finaler Meshanker bei rampe_2-Start | Zwei Gleichheitszeilen hielten die finale Terrainhöhe auf dem p3d31-Bestandswert. Einzel-Lockerung nur dieser Zeilen ließ das globale LP wegen des unabhängigen Kreuzungs-IIS infeasible. | R8a begrenzt Nachbarpaare im benannten Auslauf, keine absolute Höhe. | **Strenger als offiziell.** Mit der Profilpin-Gleichheit ist dies dieselbe interne Bestandsfixierung auf zwei Modellrepräsentationen. |
| Außerhalb Fenster fixierte p3d31-V3-Höhen | p3d33 hielt auch Station 0,3 m und die übrigen Außenpunkte exakt fest. Nach Freigabe des Starts erscheint derselbe `1,655529 mm`-Bounds-Schlupf bei Station 0,3 m. | Kein offizieller Höhen-Gleichheits-Pin auf diesen Profilpunkten; maßgeblich sind lokale R3/R8/R8a-Regeln. | **Strenger als offiziell**, soweit Profilhöhe betroffen. Keine weitere Stützstelle wurde geöffnet, weil der korrigierte V1-Hart-LP bereits infeasible war und B3 STOP anordnet. |
| Quellzelle / Plateau / Anschlusszellen | Quellwerte und Transferhintergrund blieben fest. Eine separate Lockerung einzelner Quellzellwerte wurde nicht vorgenommen; sie sind ausdrücklich geschützt. Der finale Meshanker ist separat wie oben getestet. | Prüfer bewerten das ausgegebene Höhenfeld; sie schreiben keine Quelldateiwerte vor. | Als eigenständige Ursache **nicht belegt**. Keine Quellwerte geändert. |
| Rundung / Float32 / Epsilon | Modell und IIS rechnen Float64; die beobachteten Cap-Reste sind etwa `10⁻¹⁵ m`, der Gruppenfilter-Schlupf `1,66 × 10⁻³ m`. | Offizielle Probe würde nach Float32-Transfer entscheiden. | Rundung ist als Ursache des LP-Bounds-Schlupfs **nicht plausibel**, aber Float32-Prüfung am Endrelief mangels zulässiger Lösung nicht ausgeführt. |

`[R]` Offizielle Details wurden aus [r8_kreuzung.py](r8_kreuzung.py), [r8a_policy.py](r8a_policy.py), [pruefe_regeln.py](pruefe_regeln.py), [relief_o18n.py](../relief_o18n.py) und [r9_form.py](r9_form.py) übernommen; diese Prüfer wurden in p3d34 nicht geändert. R8 meldet Stufe bei `>0,20 m`, Gitter bei `>0,15 m` (1-m-Residuenebenen-Differenz), Quergefälle bei `>3 %`; Quergefälle an reinen Wegenden wird quer zur Achse berechnet. Die p3d34-Kreuzungsbudgets `0,116 m / 0,020 m / 3 % / 20 %` sind Modell-/Projektbudgets und nicht die allgemeinen Treffergrenzen des Prüfers. R3 in `pruefe_regeln.py` verwendet 4-m-Abschnitte aus 16 Samples bei 0,25 m: Querwert `>3,5 %`, Längsresiduum `>0,08 m`, Wölbung `>0,08 m`. Die 0,18-m-Ausnahme bleibt ausschließlich am genannten Anfangspunkt; weder Toleranz noch Ausnahme wurden ausgeweitet. Der R8a-Policy-Test wurde gelesen, aber nicht ausgeführt.

## B. Ersatzpolitik und V1-Lauf

`[R]` `P3D34_START_POLICY` ist der neue Schalter in den p3d34-Werkzeugen: Standard `official`, Rückfall `legacy` reproduziert p3d33. `official` ersetzt die eine logische interne Bedingung „rampe_2-Start gleich p3d31-Bestand“: Es öffnet die Profilhöhe an Station 0 und entfernt die finale Bestandsanker-Gleichheit an `[126,51|31,62]`; Achsstützung, offizielle R8a-Ausnahme `0,18 m`, Endstufen-Cap `0,054 m`, R8 und R3 bleiben aktiv. Fenster, Geometrie, p3d31-V3-Außenhöhen ab Station 0,3 m, Transfer, Kreuzung und übrige Konstruktion bleiben gleich. Die alte/unvollständige Diagnose [p3d34_B2_V1_official_start_lp.json](../../../../../codex_jobs/tools/p3d34/results/p3d34_B2_V1_official_start_lp.json) ließ noch den Meshanker stehen; maßgeblich ist der oben verlinkte vollständige `official_full_start_hard_lp`-Lauf.

`[S]` Der vollständige offizielle V1-Hart-LP ist `Infeasible` (HiGHS Code 8). Sein gültiges IIS enthält wieder dieselben 9 inhaltlichen Zeilen und dieselben 10 Spalten: eine `variable_bounds`-Zeile bei `route_11_height_station_83.4m`, eine `axis_supports`-Zeile, drei `p3d33_fixed_anchors`-Zeilen am Kreuzungsanker/Profil und vier `plane_core_supports`-Zeilen. Der exportierte IIS liegt unter [p3d34_B2_V1_official_full_start_iis.iis.lp](../../../../../codex_jobs/tools/p3d34/results/p3d34_B2_V1_official_full_start_iis.iis.lp). Keine andere Variante wurde nach diesem B2-Ergebnis gestartet.

`[R]` Die V1-Konstruktion behielt die 25–50-m-Variable-Fensterpunkte (83 Samples von 25,2 bis 49,8 m), p3d31-V3-Fixierung außerhalb dieses Fensters mit der genannten Startausnahme, reine kontinuierliche Variablen, Lokalität/Familien/Klippenform, R8/R3 und die feste Kreuzungsplattform. Warmstart aus p3d31 Runde 3 wurde nicht verwendet: der Lauf war ein reines LP ohne Integer-Variablen, und das IIS weist einen linearen Machbarkeitskonflikt aus. Priority-Flood- und Checker-Lazy-Cut-Schleifen wurden nicht gestartet; im Hart-LP stehen 0 neue Flood-Cuts und 0 Event-Cuts. Die 20–50-m-Zusatzvariante, weitere Fenster, Float32-Transfer, Prüferloop und weitere Probe-Solves entfallen durch den vorgeschriebenen STOPP.

### rampe_2-Profil, verfügbare Diagnosewerte

`[S]` Es gibt keine vollständige Vorher/Nachher-Tabelle eines zulässigen p3d34-Profils: der Hart-LP lieferte keine Lösung. Die nachstehenden Diagnosewerte stammen aus elastischen Filterpunkten und sind keine Prüferproben.

| Station (m) | p3d31 V3 Höhe alt (m) | Elastische Diagnosehöhe (m) | Steigung / 2. Differenz | R8a am Start / Endstufe |
|---:|---:|---:|---|---|
| 0,0 | 12,469809532 | 12,468154003 (p3d33-Filter; kein offizieller Output) | für ein zulässiges p3d34-Profil n/a | Modellpaar max `0,1800000000000015 m` / separates 0,054-m-Endstufenziel nicht am Start |
| 0,3 | 12,448156357 | 12,446500828 (p3d34 offizieller All-Familien-Filter; kein offizieller Output) | für ein zulässiges p3d34-Profil n/a | Start-Ausnahme gilt nur für den Endpunkt, nicht als Höhenpin für diese Stütze |
| 25,2 | 5,247490980 | 5,195892386 (p3d33 elastischer Filter) | Join-Steigung `−0,500000 / −0,500000 m/m`; lokale 2. Differenz `0 m/m²` | nicht am Weganfang |
| 49,8 | 1,990185000 | 1,937004000 (p3d33 elastischer Filter) | Join-Steigung `−0,067465 / −0,067465 m/m`; lokale 2. Differenz `0 m/m²` | nicht am Weganfang |

`[A]` Die p3d33-Diagnosewerte für die Fensterjoins sind nur Modellwerte; Float32-R3-Wölbwerte an diesen elastischen Punkten lagen teils um `4–7 × 10⁻⁸ m` über `0,08 m`. Sie sind nicht als bestanden gewertet. Vollständige p3d33-Fensterdiagnose: [p3d33_variant1_profile_group_filter_diagnostic.json](../../../../../codex_jobs/tools/p3d33/results/p3d33_variant1_profile_group_filter_diagnostic.json).

### Vergleich zu p3d31 Runde 3

`[S]` p3d31 V3 Runde 3 bleibt die letzte gültige Float32-Modellprobe: G5 `71/4` (gesamt/D1), R5_loch `24/7`, G6 D1 `2`, R5_spitze D1 `0`, R8b D1 `1`, G3 D1 `0`, R4-Schlucht D1 `0`, R3 D1 `6/7/7`, R9w `283`; Kreuzungsstufe/Gitter `0,073/0,019 m`. Schon diese Referenz verfehlte G5, R5_loch und R9w. p3d34 hat keine Float32-Probe und daher keine neuen Trefferorte oder Ergebnisse gegen diese Runde.

## Regelzahlen und Kachelzahlen

`[S]` p3d34-Nachherwerte sind `n/a`: kein Mesh/Float32-Relief und kein offizieller Prüferlauf. Vorwerte sind der p3d17-Replay im aktuellen Prüferschema (600) und die p3d31 Runde 3 aus dem bestehenden Bericht. Der im Auftrag genannte historische Ausgangswert 9d3f8fc bleibt separat `596`, R8 `48 (9/10/5/24)`, R9 `334 (25/34/275)`.

| `pruefe_regeln` | p3d17 vorher gesamt | D1 | G1 | D2 | p3d34 nachher gesamt / D1 / G1 / D2 |
|---|---:|---:|---:|---:|---:|
| R1_blind | 24 | 2 | 1 | 0 | n/a / n/a / n/a / n/a |
| R2_getrennt | 15 | 1 | 0 | 1 | n/a / n/a / n/a / n/a |
| R3_laengs_m | 35 | 6 | 1 | 0 | n/a / n/a / n/a / n/a |
| R3_quer_pct | 29 | 17 | 0 | 0 | n/a / n/a / n/a / n/a |
| R3_woelb_m | 31 | 19 | 0 | 0 | n/a / n/a / n/a / n/a |
| R4_rand | 1 | 1 | 0 | 0 | n/a / n/a / n/a / n/a |
| R5_loch | 25 | 8 | 0 | 0 | n/a / n/a / n/a / n/a |
| R6_wasser_schnee | 4 | 0 | 3 | 0 | n/a / n/a / n/a / n/a |
| G2_spitze_oben | 3 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| G2_spitze_oben_fein | 8 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| G3_spitze_unten | 4 | 1 | 0 | 0 | n/a / n/a / n/a / n/a |
| G3_spitze_unten_fein | 2 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| G5_beule_klippe | 69 | 2 | 0 | 0 | n/a / n/a / n/a / n/a |
| G6_facette | 219 | 3 | 3 | 0 | n/a / n/a / n/a / n/a |
| G7_wand_glatte_flaeche | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| G7b_wandkontur_feld | 25 | 1 | 0 | 0 | n/a / n/a / n/a / n/a |
| G7b_wandkontur_kantenschaerfe | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| G7b_wandkontur_rauheit | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| G8_fluss_nicht_bis_rand | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| G11_objekt_schwebt_sinkt | 4 | 2 | 2 | 0 | n/a / n/a / n/a / n/a |
| T1_fleckrand | 94 | 0 | 3 | 7 | n/a / n/a / n/a / n/a |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| T3_streifen_ringe_bildpruefung_offen | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| **Summe** | **600** | **63** | **13** | **8** | **n/a** |

| Prüfer / Regel | p3d17 vorher gesamt | D1 | G1 | D2 | p3d34 nachher gesamt / D1 / G1 / D2 |
|---|---:|---:|---:|---:|---:|
| R8_stufe | 9 | 2 | 0 | 0 | n/a / n/a / n/a / n/a |
| R8_gitter | 10 | 2 | 0 | 0 | n/a / n/a / n/a / n/a |
| R8_quer | 4 | 0 | 0 | 0 | n/a / n/a / n/a / n/a |
| R8a_wegende | 23 | 3 | 0 | 0 | n/a / n/a / n/a / n/a |
| **R8 gesamt** | **46** | **7** | **0** | **0** | **n/a** |
| R8b_delle | 23 | 1 | 0 | 0 | n/a / n/a / n/a / n/a |
| R9_saegezahn | 34 | 1 | 1 | 0 | n/a / n/a / n/a / n/a |
| R9w_wellen | 287 | 27 | 12 | 0 | n/a / n/a / n/a / n/a |
| **R9 gesamt** | **344** | **29** | **13** | **0** | **n/a** |

`[A]` D1/G1/D2 nachher je Regel, R8-/R9-Trefferorte, neue D2-Trefferfreiheit und die +5-Schranke sind nicht gemessen. Keine Treffer werden als neu oder behoben behauptet.

## Unveränderte Dateien, Prüferdiff und Hashes

`[S]` Direkt berechnete SHA-256 der geschützten Eingaben:

| Datei | SHA-256 |
|---|---|
| `relief3d/neu/zellen_relief.csv` | `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa` |
| `relief3d/neu/vektor.json` | `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e` |
| `relief3d/neu/felder.json` | `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435` |
| G1-Bestandsmesh Sollhash | `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` |
| D2-Bestandsmesh Sollhash | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` |

`[S]` G1/D2-Sollhashes entsprechen den gespeicherten p3d17/p3d31-Referenzen. Ein p3d34-Ausgabehash wurde nicht erzeugt, weil kein Mesh gebaut wurde. D2-Regressionszahlen nach p3d34 wurden deshalb nicht gemessen; die Eingangszellwerte, der Relief-Overlay, `../referenz/*`, G1, D2 und `t42u` wurden nicht verändert.

`[S]` Prüfer-/Testquell-Diff gegen `89c61ce`: geerbtes `M pruefung/r8_kreuzung.py`, `A pruefung/r8a_policy.py`, `A pruefung/test_r8a_policy_p3d26.py`; p3d34 fügt keinen Prüferdiff hinzu. `pruefe_regeln.py`, `r9_form.py` und `relief_o18n.py` bleiben unverändert.

## Gates, Annahmen und offene Punkte

`[F]` Wegen der bewiesenen Infeasibilität wurden `gen_relief.py`, `baue_html.py`, der Lochscan, `pruefe_regeln.py`, `r8_kreuzung.py`, `r9_form.py`, pytest, `delta.py`, `t42u`, die Klippenmessung, LOD1 und Bilder nicht ausgeführt. Damit sind LOD1 `<1,3 M`, `t42u=0`, vollständiges Mesh-Gate, D2-Regressionsgate, Bitgleichheit außerhalb des Fensters, Float32-R8a, R3- und Übergangsnachweis an einer gültigen Oberfläche ungemessen. Der letzte gebaute Stand bleibt p3d18 @ `ee46fe5`. Die fünf bekannten roten Bestandstests (R8a gesamt, R9-Sägezahn D1, D1-Wandkante, F1/C1-Wegende, Schattenbild) wurden nicht angefasst und nicht ausgeführt.

`[A]` Der All-Familien-Filter ist ein elastischer Modellpunkt, kein Relief und kein offizieller Prüferlauf. Der IIS belegt den Kreuzungs-/rampe_11-Konflikt, aber nicht, welche einzelne dieser 9 Zeilen bei einer geänderten Kreuzungsplattform zuerst gelockert werden müsste; solche Änderungen waren verboten. Die fest fixierte Station 0,3 m bleibt der nächste beobachtete Profil-Bounds-Konflikt, aber wegen B3 wurde kein 0–50-m-Fenster gerechnet. Die absoluten Start-Höhenänderungen können daher nicht als bestanden bewertet werden.

`[S]` Neue Dateien liegen nur unter `codex_jobs/tools/p3d34/` und diesem Ergebnisbericht. Keine Zellquellwerte, Tests, Prüfer, Schwellen, Wegeführung, Grundriss, Overlay, Referenzen oder Mesh-Standardwerte wurden geändert. Es wurden keine Nachrichten versandt.

## Selbstprüfung A1, A2, B1–B3 und Mesh

1. `[S]` A1: IIS-Strategie 6 dokumentiert; startbezogener Bounds-Schlupf, Einzel-Lockerungen und unabhängiges Kreuzungs-IIS belegt.
2. `[R]` A2: aktuelle R8a-Ausnahme ist exakt die offizielle 0,18-m-Paarbedingung; Bestands-Höhenpins sind strenger; 0,054 m betrifft eine separate Endstufenbedingung.
3. `[R]` B1: `official` ersetzt beide Zeilenrepräsentationen derselben Start-Bestandsfixierung und erhält R8a/R8/R3/Endstufen-/Achsstützbedingungen. Float32-Probe nicht möglich.
4. `[S]` B2/B3: V1-Vollpolitik-Hart-LP infeasible; All-Familien-Filter und gültiges IIS abgelegt; danach STOPP ohne Fenster-Erweiterung oder weiteres Solve.
5. `[F]` Harte Zielwerte, D2-Gate und +5-Regel sind nicht verifiziert; sie wurden nicht gelockert.
6. `[F]` Kein Mesh, keine Bilder, kein HTML-Bau und kein vollständiges Mesh-Gate.

## Schluss

`[F]` Die 1,655529 mm wurden im p3d33-Filter durch die interne p3d31-Bestandsfixierung der rampe_2-Profil- und finalen Start-Höhe erzwungen; R8a selbst liegt am Start bei der offiziellen 0,18-m-Grenze. `[S]` Nach Ersatz dieser Fixierung bleibt V1 wegen eines unabhängigen IIS an rampe_11-Station 83,4 m und der fixierten Kreuzungsplattform infeasible; der All-Familien-Filter zeigt den gleichen Bounds-Schlupf nun an Station 0,3 m. `[F]` Deshalb endet p3d34 vor Float32-Prüfung und Meshbau, und sämtliche p3d34-Regel-, Kachel- und Mesh-Nachherwerte bleiben offen.
