# Ergebnis p3d33

Stand 14.11.2026 · Worktree `/workspace/wt_dorfmap_p3d33` · Branch `art/dorfmap-p3d33` · Basis `origin/art/dorfmap-p3d32` @ `b8b9364` · Kosten 0 EUR.

Marker: `[S]` direkt gemessen · `[R]` Modell-/Gruppenfilterbefund · `[A]` Annahme oder Grenze · `[F]` Entscheidung. Laufzeitnachweis: `/workspace/codex_jobs/log_p3d33.txt` (`gpt-6-luna`, reasoning effort `xhigh`).

## Ergebnis

`[F]` Keine der beiden erlaubten Fenster-Varianten ergab ein primal zulässiges Hart-LP. Nach dem geforderten All-Familien-Gruppenfilter für beide infeasiblen Modelle stoppt p3d33; es gab keine Float32-Probe und keinen Mesh-Bau.

`[S]` Variante 1 (`P3D33_VARIANT=1`, Station 25–50 m) endete mit HiGHS `Infeasible`, Code 8, bei 20.411 Variablen, 76.458 Zeilen und 0 Integer-Variablen. Variante 2 (`P3D33_VARIANT=2`, Station 20–55 m) endete ebenfalls `Infeasible`, Code 8, mit 20.411 Variablen, 76.388 Zeilen und 0 Integer-Variablen. Beide Solves und die Gruppenfilter liefen seriell mit einem Thread und einem Zeitlimit von 600 s; der Gruppenfilter war jeweils `Optimal`, aber ist ausdrücklich kein zeilenweises IIS.

`[R]` In beiden All-Familien-Filtern war ausschließlich `variable_bounds_extra_m` positiv: **0,00165552907 m nach unten** bei rampe_2 Station 0 m, Koordinate `126,51000021|31,62000173`. Das festgesetzte Band ist `[12,46980953217; 12,46980953217] m`, der diagnostische Wert `12,46815400310 m`. Alle anderen aktivierten Familien benötigten laut Filter keinen Schlupf. Die Stelle liegt außerhalb beider Fenster und betrifft damit den unveränderten rampe_2-Start.

`[F]` Das Ziel wurde verfehlt. Eine weitere Variante oder ein anderes Fenster wird nicht gestartet; es wird kein Mesh gebaut.

## Konstruktion und offizielle Bedingungen

`[R]` Variante 1 gibt 83 Höhenwerte zwischen den Rasterstationen 25,2 und 49,8 m frei; Variante 2 gibt 117 Werte von 20,1 bis 54,9 m frei. Alle anderen rampe_2-Werte und rampe_11 bleiben auf p3d31 V3 Runde 3 festgesetzt. Die Plattform bei `[152,5|28,5]`, ihr 1,5-%-Quergefälle und Auslauf, der rampe_2-Start, Grundriss, Quellzellen und übrige Wege bleiben wie p3d32. Ein Warmstart aus p3d31 Runde 3 wurde nicht verwendet: er kann einen bewiesenen linearen Feasibility-Konflikt nicht beheben und die LPs sind klein genug, dass kein MIP-Start nötig war.

`[R]` Der offizielle R3-Code wurde als Stencil übernommen: Rampenabstand 0,25 map-Einheiten; Längsresiduum `h − gaussian_filter1d(h, sigma=8, mode="nearest")`; Querwert `(h(+1,5)−h(−1,5))/3 × 100`; Wölbung `|h(0)−(h(+1,5)+h(−1,5))/2|`; gezählt wird der Maximalwert je Abschnitt der 16 Stichproben. Modellbudgets sind R3 D1 `6/7/7` und die offiziellen Grenzwerte `0,08 m`, `3,5 %`, `0,08 m`. R8-Sicherheitsgrenzen bleiben bei Stufe `0,116 m`, Gitter `0,020 m`, Quergefälle `3 %`, Einzelquer `20 %`; Wegendstufe `0,054 m`; R8a `0,10 m`, nur rampe_2-Start `[126,51|31,62]` erhält `0,18 m`. Die Prüferdateien selbst wurden nicht geändert.

`[R]` C0 ist durch die stückweise lineare Profilinterpolation stetig. An beiden Fensterrändern erzwingen zwei LP-Gleichungen gleiche einseitige Steigungen; die lokale Profil-Zweitdifferenz am Join ist damit 0. Der offizielle R3-Wölb-Stencil am Join ist zusätzlich auf `0,08 m` begrenzt. Die Zahlen unten stammen aus dem elastischen Gruppenfilterpunkt, der **kein** zulässiger Hart-LP-Kandidat ist.

| Fenster/Join | Station | Höhe alt (m) | Höhe Diagnosepunkt (m) | Steigung links (m/m) | Steigung rechts (m/m) | lokale 2. Differenz (m/m²) | offizieller R3-Wölbwert nach Float32 (m) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 25–50 m, links | 25,2 | 5,247491 | 5,195892 | -0,500000 | -0,500000 | 0 | 0,080000039 |
| 25–50 m, rechts | 49,8 | 1,990185 | 1,937004 | -0,067465 | -0,067465 | 0 | 0,080000005 |
| 20–55 m, links | 20,1 | 7,151310 | 7,129675 | -0,500000 | -0,500000 | 0 | 0,080000068 |
| 20–55 m, rechts | 54,9 | 0,878158 | 0,823361 | 0 | 0 | 0 | 0,027083458 |

`[S]` Die Float32-Diagnosewerte am linken Join beider elastischen Punkte überschreiten `0,08 m` um rund `4–7 × 10⁻⁸ m`; diese Punkte wurden nicht als offizielle Probe gewertet. Die p3d33-Hart-LPs waren infeasible, daher gibt es keinen Float32-Prüferlauf, der die Stetigkeit oder die R3-Budgets auf einem zulässigen Kandidaten bestätigen könnte.

`[R]` Die komplette Fenster-Profil-Tabelle (Station, p3d31-Höhe, Diagnosehöhe, Steigung und lokale Zweitdifferenz) für die Standardvariante steht in [p3d33_variant1_profile_group_filter_diagnostic.json](../../../../../codex_jobs/tools/p3d33/results/p3d33_variant1_profile_group_filter_diagnostic.json). Sie ist ausdrücklich ein Diagnosepunkt. Ihre maximale Abweichung außerhalb des Fensters ist `0,00165552907 m` am Start; damit ist auch für diese elastische Lösung keine Bitgleichheit außerhalb des Fensters nachweisbar. Für einen zulässigen Kandidaten gibt es keinen Bitgleichheitsnachweis.

`[S]` Vollständige Profil-Tabelle der Standardvariante 25–50 m. „Höhe Diagnosepunkt“ stammt aus dem elastischen Gruppenfilter und ist kein zulässiger Endstand.

| Station (m) | Höhe alt (m) | Höhe Diagnosepunkt (m) | Steigung (m/m) | 2. Differenz (m/m²) |
|---:|---:|---:|---:|---:|
| 25.2 | 5.24749 | 5.19589 | -0.50000 | 0.00000 |
| 25.5 | 5.14992 | 5.04589 | -0.46912 | 0.20587 |
| 25.8 | 5.05905 | 4.91442 | -0.29937 | 0.92582 |
| 26.1 | 4.94798 | 4.86627 | -0.28769 | -0.84797 |
| 26.4 | 4.81395 | 4.74181 | -0.27607 | 0.92543 |
| 26.7 | 4.71642 | 4.70063 | -0.18577 | -0.32344 |
| 27.0 | 4.65809 | 4.63035 | -0.31632 | -0.54691 |
| 27.3 | 4.58883 | 4.51084 | -0.31125 | 0.58071 |
| 27.6 | 4.51657 | 4.44359 | -0.15249 | 0.47767 |
| 27.9 | 4.44428 | 4.41934 | -0.19891 | -0.78708 |
| 28.2 | 4.37198 | 4.32425 | -0.25663 | 0.40229 |
| 28.5 | 4.29433 | 4.26537 | -0.21050 | -0.09475 |
| 28.8 | 4.22383 | 4.19795 | -0.25979 | -0.23390 |
| 29.1 | 4.15945 | 4.10949 | -0.25046 | 0.29616 |
| 29.4 | 4.11156 | 4.04768 | -0.11423 | 0.61201 |
| 29.7 | 4.07649 | 4.04095 | -0.01121 | 0.07476 |
| 30.0 | 4.07649 | 4.04095 | 0.00000 | 0.00000 |
| 30.3 | 4.07649 | 4.04095 | 0.00000 | 0.00000 |
| 30.6 | 4.07649 | 4.04095 | 0.00000 | 0.00000 |
| 30.9 | 4.07649 | 4.04095 | 0.00000 | 0.00000 |
| 31.2 | 4.07649 | 4.04095 | 0.00000 | 0.00000 |
| 31.5 | 4.07180 | 4.04095 | -0.00278 | -0.01852 |
| 31.8 | 4.07180 | 4.03928 | -0.00278 | 0.01852 |
| 32.1 | 4.07166 | 4.03928 | 0.00201 | 0.01341 |
| 32.4 | 4.06949 | 4.04049 | 0.01256 | 0.05693 |
| 32.7 | 4.06525 | 4.04682 | 0.01055 | -0.07035 |
| 33.0 | 4.06524 | 4.04682 | 0.00000 | 0.00000 |
| 33.3 | 4.06303 | 4.04682 | 0.00000 | 0.00000 |
| 33.6 | 4.04543 | 4.04682 | 0.00000 | 0.00000 |
| 33.9 | 4.02679 | 4.04682 | -0.04670 | -0.31130 |
| 34.2 | 4.01694 | 4.01881 | -0.05730 | 0.24063 |
| 34.5 | 4.01694 | 4.01245 | -0.01060 | 0.07067 |
| 34.8 | 3.99844 | 4.01245 | -0.00121 | -0.00806 |
| 35.1 | 3.97229 | 4.01172 | -0.03968 | -0.24842 |
| 35.4 | 3.96365 | 3.98864 | -0.14682 | -0.46585 |
| 35.7 | 3.96155 | 3.92363 | -0.10835 | 0.72234 |
| 36.0 | 3.96155 | 3.92363 | -0.09326 | -0.62173 |
| 36.3 | 3.96155 | 3.86767 | -0.25773 | -0.47475 |
| 36.6 | 3.93652 | 3.76899 | -0.16447 | 1.09649 |
| 36.9 | 3.93321 | 3.76899 | 0.00000 | 0.00000 |
| 37.2 | 3.93321 | 3.76899 | -0.06108 | -0.40717 |
| 37.5 | 3.93321 | 3.73234 | -0.06108 | 0.40717 |
| 37.8 | 3.93321 | 3.73234 | -0.13381 | -0.89210 |
| 38.1 | 3.93321 | 3.65205 | -0.13381 | 0.89210 |
| 38.4 | 3.92811 | 3.65205 | -0.13763 | -0.91752 |
| 38.7 | 3.91800 | 3.56948 | -0.14455 | 0.87137 |
| 39.0 | 3.88454 | 3.56532 | -0.17723 | -1.08924 |
| 39.3 | 3.84565 | 3.46314 | -0.41901 | -0.52263 |
| 39.6 | 3.81217 | 3.31391 | -0.24870 | 1.65802 |
| 39.9 | 3.78940 | 3.31391 | 0.00000 | 0.00000 |
| 40.2 | 3.77467 | 3.31391 | -0.25000 | -1.66667 |
| 40.5 | 3.76367 | 3.16391 | -0.32149 | 1.19007 |
| 40.8 | 3.74648 | 3.12102 | -0.07149 | 0.47660 |
| 41.1 | 3.72455 | 3.12102 | -0.07906 | -0.52705 |
| 41.4 | 3.69635 | 3.07359 | -0.07906 | 0.52705 |
| 41.7 | 3.66476 | 3.07359 | -0.17475 | -1.16498 |
| 42.0 | 3.62865 | 2.96874 | -0.17475 | 1.16498 |
| 42.3 | 3.59035 | 2.96874 | -0.05438 | -0.36254 |
| 42.6 | 3.54964 | 2.93611 | -0.30438 | -1.30413 |
| 42.9 | 3.50703 | 2.78611 | -0.25000 | 1.66667 |
| 43.2 | 3.46166 | 2.78611 | 0.00000 | 0.00000 |
| 43.5 | 3.41470 | 2.78611 | -0.22914 | -1.52760 |
| 43.8 | 3.36507 | 2.64863 | -0.32054 | 0.91829 |
| 44.1 | 3.31350 | 2.59379 | -0.09140 | 0.60931 |
| 44.4 | 3.25887 | 2.59379 | -0.19209 | -1.28060 |
| 44.7 | 3.20218 | 2.47853 | -0.26143 | 0.81835 |
| 45.0 | 3.13873 | 2.43693 | -0.07064 | 0.45360 |
| 45.3 | 3.07042 | 2.43615 | -0.06804 | -0.43626 |
| 45.6 | 3.00003 | 2.39611 | -0.06674 | 0.44491 |
| 45.9 | 2.92806 | 2.39611 | -0.19519 | -1.30124 |
| 46.2 | 2.85613 | 2.27900 | -0.19519 | 1.30124 |
| 46.5 | 2.78395 | 2.27900 | 0.00000 | 0.00000 |
| 46.8 | 2.71318 | 2.27900 | 0.00000 | 0.00000 |
| 47.1 | 2.64703 | 2.27900 | 0.00000 | 0.00000 |
| 47.4 | 2.57544 | 2.27900 | -0.06106 | -0.40709 |
| 47.7 | 2.50195 | 2.24236 | -0.06235 | 0.39853 |
| 48.0 | 2.42850 | 2.24159 | -0.13769 | -0.90083 |
| 48.3 | 2.35526 | 2.15974 | -0.14156 | 0.87502 |
| 48.6 | 2.28219 | 2.15665 | -0.14595 | -0.90429 |
| 48.9 | 2.20922 | 2.07217 | -0.15074 | 0.87240 |
| 49.2 | 2.13629 | 2.06621 | -0.19155 | -1.14447 |
| 49.5 | 2.06292 | 1.95724 | -0.21534 | 0.98585 |
| 49.8 | 1.99019 | 1.93700 | -0.06747 | 0.00000 |

## Einordnung des 0,051546-m-Schlupfs

`[S]` p3d32-korrigierter Gruppenfilter meldete maximal `0,05154638898 m` an rampe_2 Station 37,5 m (`157,43153097|27,42298231`), festes Band `3,93320513879 m`, diagnostisch `3,88165874981 m`. Der verworfene p3d32-Vorversuch mit variablen Rampen meldete denselben Maximalbetrag bei Station 14,7 m (`138,68964|30,34365`), dort gegen ein anderes Unterband. Im p3d32-korrigierten elastischen Punkt lag rampe_2-Start bereits `0,02000007 m` unter seinem p3d31-Festwert; das ist ein weiterer, kleinerer Bounds-Verstoß, der vom maximalen 0,051546-m-Verstoß überdeckt wurde.

`[R]` Der identische Maximalbetrag belegt keine identische Ursache: die beiden p3d32-Modelle hatten unterschiedliche Weghöhenbindungen, und ein Gruppenfilter berichtet den maximalen Schlupf einer Gruppe, nicht die verursachende Zeilenmenge. p3d33 öffnet den 37,5-m-Punkt und senkt den maximalen gruppenweiten Bounds-Schlupf auf 1,656 mm; danach bleibt der Startpunkt als Engpass. Beide erlaubten Fenster liefern denselben Startschlupf. Das spricht für eine gemeinsame Spannung zwischen rampe_2-Festprofil/Start und den übrigen Modellbedingungen, bestimmt aber keine einzelne R8a-, Endpunkt- oder Familienzeile; ein row-IIS wurde nicht erzeugt.

`[A]` Das Fenster 25–50 m war groß genug, den vorherigen dominanten Bounds-Schlupf aus dem Gruppenmaximum zu entfernen, aber nicht groß genug, die LP insgesamt machbar zu machen. Die 20–55-m-Erweiterung hilft nicht, weil der verbleibende Befund bei Station 0 m liegt.

## Zahlen je Prüfer und Kachel

`[S]` Vorher/Nachher je Regel: Eine p3d33-Probe existiert nicht; deshalb ist jede p3d33-Nachherzahl `n/a` und keine Regel wird als bestanden behauptet. Zum Vergleich stehen der aktuelle p3d17-Replay (600 Treffer einschließlich G11, Grundlage der +5-Schranke) und p3d31 V3 Runde 3.

| Prüfer | Ausgang 9d3f8fc (vom Auftrag) | p3d17-Replay | p3d31 Runde 3 | p3d33 |
|---|---:|---:|---:|---:|
| `pruefe_regeln` gesamt | 596 | 600 | 576 | n/a |
| R8 gesamt (`Stufe/Gitter/Quer/R8a`) | 48 (`9/10/5/24`) | 46 (`9/10/4/23`) | 42 (`9/9/4/20`) | n/a |
| R9 gesamt (`R8b/Sägezahn/R9w`) | 334 (`25/34/275`) | 344 (`23/34/287`) | 340 (`23/34/283`) | n/a |

### pruefe_regeln je Regel

| Regel | p3d17-Replay | p3d31 V3 Runde 3 | p3d33 |
|---|---:|---:|---:|
| `G11_objekt_schwebt_sinkt` | 4 | 4 | n/a |
| `G2_spitze_oben` | 3 | 3 | n/a |
| `G2_spitze_oben_fein` | 8 | 8 | n/a |
| `G3_spitze_unten` | 4 | 3 | n/a |
| `G3_spitze_unten_fein` | 2 | 2 | n/a |
| `G5_beule_klippe` | 69 | 71 | n/a |
| `G6_facette` | 219 | 218 | n/a |
| `G7_wand_glatte_flaeche` | 1 | 1 | n/a |
| `G7b_wandkontur_feld` | 25 | 25 | n/a |
| `G7b_wandkontur_kantenschaerfe` | 1 | 1 | n/a |
| `G7b_wandkontur_rauheit` | 1 | 1 | n/a |
| `G8_fluss_nicht_bis_rand` | 1 | 1 | n/a |
| `R1_blind` | 24 | 24 | n/a |
| `R2_getrennt` | 15 | 15 | n/a |
| `R3_laengs_m` | 35 | 35 | n/a |
| `R3_quer_pct` | 29 | 19 | n/a |
| `R3_woelb_m` | 31 | 19 | n/a |
| `R4_rand` | 1 | 0 | n/a |
| `R5_loch` | 25 | 24 | n/a |
| `R6_wasser_schnee` | 4 | 4 | n/a |
| `T1_fleckrand` | 94 | 94 | n/a |
| `T2_textur_abgeschnitten_bildpruefung_offen` | 1 | 1 | n/a |
| `T3_streifen_ringe_bildpruefung_offen` | 1 | 1 | n/a |
| `T4_graue_flussstreifen_bildpruefung_offen` | 1 | 1 | n/a |
| `T5_textur_vs_clay_bildpruefung_offen` | 1 | 1 | n/a |

### R8 je Regel

| Regel | p3d17-Replay | p3d31 V3 Runde 3 | p3d33 |
|---|---:|---:|---:|
| `R8_gitter` | 10 | 9 | n/a |
| `R8_quer` | 4 | 4 | n/a |
| `R8_stufe` | 9 | 9 | n/a |
| `R8a_wegende` | 23 | 20 | n/a |

### R9 je Regel

| Regel | p3d17-Replay | p3d31 V3 Runde 3 | p3d33 |
|---|---:|---:|---:|
| `R8b_delle` | 23 | 23 | n/a |
| `R9_saegezahn` | 34 | 34 | n/a |
| `R9w_wellen` | 287 | 283 | n/a |

[S] Kachelsummen D1/G1/D2:

| Prüfer | p3d17 Replay D1/G1/D2 | p3d31 Runde 3 D1/G1/D2 | p3d33 D1/G1/D2 |
|---|---:|---:|---:|
| pruefe_regeln | 63/13/8 | 39/13/8 | n/a / n/a / n/a |
| R8 | 7/0/0 | 3/0/0 | n/a / n/a / n/a |
| R9 | 29/13/0 | 25/13/0 | n/a / n/a / n/a |

`[S]` Die beste p3d31-Runde-3-Probe hatte G5 `71/4` gesamt/D1, R5_loch `24/7`, G6 D1 `2`, R5_spitze D1 `0`, R8b D1 `1`, G3 D1 `0`, R4-Schlucht D1 `0`, R3 D1 `6/7/7`, R9w gesamt `283`, Kreuzungsstufe `0,073 m` und Gitter `0,019 m`. Die p3d33-Tabellen sind durchweg `n/a`, da kein zulässiger Hart-LP-Punkt vorlag; eine p3d33-Trefferliste mit Orten wurde nicht erzeugt. D2-R8/R9 bleibt in der p3d31-Referenz bei `0/0`, aber ein D2-Nachhergate wurde nicht ausgeführt.

## Unverändertes, Prüferdiff und Hashes

`[S]` Vor-Ort berechnete SHA-256:

| Datei | SHA-256 |
|---|---|
| `zellen_relief.csv` | `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa` |
| `vektor.json` | `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e` |
| `felder.json` | `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435` |
| G1-Höhenkanal Soll (p3d17/p3d31) | `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb` |
| D2-Höhenkanal Soll (p3d17/p3d31) | `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6` |

`[S]` Der p3d33-Probe-Hash für G1/D2 und die p3d33-Bitgleichheit zu den Referenzkanälen sind mangels Probe nicht gemessen. Zellquellwerte, `vektor.json`, `felder.json`, Overlay und `../referenz/*` blieben unverändert.

`[S]` Prüfer-Python-Diff gegen `89c61ce` (geerbter, freigegebener Stand): `M pruefung/r8_kreuzung.py`, `A pruefung/r8a_policy.py`, `A pruefung/test_r8a_policy_p3d26.py`. p3d33 hat keine dieser Dateien geändert; `pruefe_regeln.py`, `r9_form.py` und `relief_o18n.py` sind ebenfalls unverändert.

`[S]` JSON-Belege liegen unter `codex_jobs/tools/p3d33/results/`: je Variante Hart-LP, All-Familien-Gruppenfilter, Checkerloop-Zusammenfassung und Diagnose-Profil. Es gab 0 Priority-Flood-Cuts und 0 offizielle Prüfer-Lazy-Cuts, weil kein Hart-LP-Kandidat den Probe-Schritt erreichte.

## Mesh-Gate, Grenzen und offene Punkte

`[F]` Wegen der Infeasibilität wurden `gen_relief.py`, `baue_html.py`, das vollständige Gate, pytest, `delta.py`, `t42u`, lod1 und Bildaufnahme nicht ausgeführt. Es gibt kein p3d33-Mesh, keine Lod1-Dreieckzahl, keine gemessene t42u-Summe, keine Vorher-/Nachherbilder und keinen Mesh-Delta-Bericht. Die fünf bekannten roten Bestandstests wurden weder verändert noch ausgeführt. Der letzte gebaute Mesh-Stand bleibt p3d18 @ `ee46fe5`.

`[A]` Offene Grenzen: Der Gruppenfilter ist keine row-IIS-Diagnose; die 1,656-mm-Startspannung bleibt ohne einzelne ursächliche Zeile. R9w, G5, R5_loch, G6 und die übrigen Float32-Regeln sind mangels zulässiger Oberfläche nicht gemessen. Für p3d33 sind weder harte Regelziele noch die +5-Schranke oder D2-Regressionsfreiheit nachgewiesen.

## Selbstprüfung Anforderungen 1–8

1. `[R]` Beide erlaubten Fenster wurden implementiert; Variante 1 und die nur nach Infeasibilität gestartete Variante 2 sind jeweils infeasible. Außenhöhen sind in der Konstruktion fest; der elastische Diagnosepunkt verletzt sie am Start um 1,656 mm.
2. `[R]` Offizielle R3-Stationsabstände/Stencils und geforderte Grenzwerte sind implementiert; R8/R8a-Sicherheitsgrenzen ebenfalls. Kein finaler Float32-Nachweis möglich.
3. `[R]` C0/C1 und Rand-R3-Wölbbedingungen sind implementiert. Übergangswerte aus elastischen Punkten stehen oben; wegen Gruppenfilter-Schlupf sind sie kein gültiger Reliefnachweis.
4. `[R]` Reines kontinuierliches LP, p3d32-Lokalität/Familien/Klippenform/Flood/Lazy-Cut-Konstruktion, feste Plattform und feste übrige Wege; keine R9w-Pins/Gleichheitslocks. Prüfer und Quellwerte unverändert.
5. `[S]` Erfüllt: beide Fenster-Hart-LPs sind bewiesen infeasible; beide All-Familien-Filter zeigen den Bounds-Schlupf am rampe_2-Start. Danach Stopp.
6. `[F]` Harte Ziele und +5-Schranke wurden nicht gelockert, aber mangels Float32-Probe nicht nachgewiesen.
7. `[F]` Nicht ausgelöst: kein Probe-Ergebnis hält alle Ziele, deshalb kein Mesh und keine Bilder.
8. `[F]` Erfüllt: beide infeasiblen Varianten mit Schlupf-Ort/Betrag dokumentiert; kein Mesh und keine weitere Fenster-Variante.

## Schluss

`[F]` Die p3d33-Variante 25–50 m ist infeasible; der Gruppenfilter senkt den vorherigen dominanten 5,155-cm-Schlupf, lässt aber am unveränderten rampe_2-Start 1,656 mm Bounds-Schlupf. Das Fenster 20–55 m ändert diesen Restkonflikt nicht, und die identischen 5,155 cm aus den älteren Modellen beweisen wegen unterschiedlicher Bounds und fehlendem row-IIS keine gemeinsame Zeilenursache. Es gab deshalb keine Float32-Probe und keinen Mesh-Bau; Prüferzahlen, D2-Regressionsgate, t42u und LOD1 bleiben für p3d33 ungemessen.
