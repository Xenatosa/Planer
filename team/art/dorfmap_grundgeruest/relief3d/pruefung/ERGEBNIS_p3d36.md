# ERGEBNIS_p3d36

Stand 2026-11-15 · Worktree /workspace/wt_dorfmap_p3d36 · Branch art/dorfmap-p3d36 · Startbasis origin/art/dorfmap-p3d35 @ f15bf9c · Kosten 0 EUR.

Laufzeitnachweis: /workspace/codex_jobs/log_p3d36.txt. Marker: [S] gemessen · [R] Code-/Modellbefund · [A] Annahme oder Grenze · [F] Entscheidung.

## Ergebnis

[F] **STOPP ohne Mesh.** Der abschließend korrigierte LP-Lauf mit Stufenzeilen an allen vier Rampenenden war bereits in Runde 1 infeasible; der elastische Filter fand 4,526635 mm Überschreitung am rampe_11-Startband. Es gibt deshalb keine Float32-Probe für dieses vollständige Modell und das Mesh-Gate wurde nicht erreicht. Die unten als „vorläufig“ markierte Float32-Probe stammt aus der vorherigen, unvollständigen Endpunktkulisse und ist nur ein Diagnosevergleich.

## Abschließender Modelllauf nach Korrektur aller Endpunktbänder

[S] Der zuletzt ausgeführte Standardlauf `P3D36_POLICY=official`, `P3D36_DRAINAGE_POLICY=official`, `P3D36_R3_POLICY=official_hard`, `P3D36_R8A_POLICY=lazy_official` ergänzte die 0,054-m-Stufenzeilen für Start und Ende von rampe_2 und rampe_11. Das LP hatte 20.413 Variablen, 75.287 Zeilen, null Integer-Variablen und endete in Runde 1 mit `Infeasible`; es wurde daher kein Checker-Relief erzeugt.

[S] Der einzelne All-Familien-Filter war optimal und benötigte nur `endpoint_stage_extra_m=0,00462663517 m` (einschließlich 0,0001-m Float32-Puffer). Das maßgebliche Paar liegt im rampe_11-Startband bei [147,5|5,0]–[147,5|5,25]: 0,058526635 m statt höchstens 0,054 m, also 0,004526635 m tatsächliche Überschreitung. Die übrigen ausgewiesenen Familienmaxima hatten keine positive Verletzung; Querabflussmessung: 0,0899 m über 3 m (2,996667 %), unter dem verwendeten 3%-Cap samt 0,0001-m Guard. Kein IIS wurde gestartet.

[R] Der frühere LP-/Float32-Beleg deckte nur 460 Endpunkt-Nachbarpaare ab und ist deshalb nicht als Abschlussprobe zu werten. Der korrigierte Lauf erweitert die Abdeckung auf alle vier Rampenenden; sein Ergebnis ersetzt die früheren Aussagen, wonach Runde 1 des offiziellen Modells eine gültige Abschlussprobe geliefert habe. Die 24-Cut-Folge und die zugehörigen Filter in den folgenden Abschnitten dokumentieren ausschließlich den vorläufigen Kandidatenpfad.

## 1. rampe_11-Festhöhe, offizielle Regeln und Profilfenster

[R] p3d35 setzte die Profilgrenzen zunächst vollständig auf das gespeicherte p3d31-V3-Profil und öffnete nur rampe_2 0–50 m sowie rampe_11 70–90 m. Die feste Höhe 7,923292889 m an rampe_11 Station 20,7 m stammt aus p3d31 V3 Runde 3, Profilindex 69, Koordinate [152,298075|14,991086]; die Nachbarwerte sind 8,016995071 m bei 20,4 m und 7,831298000 m bei 21,0 m. Der p3d35-Code hatte für rampe_11 einen Stationsfaktor 2,4 aus alten IIS-Benennungen übernommen; p3d36 korrigiert die physische Weglänge auf CELL_M=1,2 m. Das exportierte rampe_11-Profil ist 57,0 m lang, deshalb macht das angeforderte Fenster 0–90 m alle 191 Profilpunkte variabel.

| Interne Zeile / Befund | Offizielle Definition | Urteil |
|---|---|---|
| Festes absolutes Profil h(20,7)=7,923292889 m durch p3d31-V3-Kopie außerhalb des p3d35-Fensters | pruefe_regeln.py: R3 wird auf 0,25-m-Stationen in 16-Sample-Sektionen geprüft; längs ≤0,08 m, quer ≤3,5 %, Wölbung ≤0,08 m. Keine absolute Höhenbindung. | Die Gleichheit bindet die absolute Höhe stärker als R3. Die Float32-Probe änderte h(20,7) auf 8.363479 m (Δ +0.440186 m) und hatte in D1 null R3-Treffer. |
| Dieselbe absolute Höhe am inneren Rampenpunkt | r8_kreuzung.py bildet R8-Gruppen an Kreuzungen, Rampenenden und Weganschlüssen; Schwellen 0,20 m Stufe, 0,15 m Gitter, 3 % quer. | An [152,298075|14,991086] liegt kein R8-Kreuzungs- oder Wegendpunkt; die lokale R8-Definition verlangt dort keinen absoluten Wert. |
| Dieselbe absolute Höhe am inneren Rampenpunkt | r8a_policy.py und r8_kreuzung.py: 0,10 m im 4-m-Auslaufband hinter Rampenenden, WAND-Zellen mit Gradient >1 ausgeschlossen; 0,18 m nur bei rampe_2_anfang [126,51|31,62] innerhalb 1e-5. | Station 20,7 m liegt im Innenprofil von rampe_11, außerhalb des Endpunktauslaufs. R8a pinnt diese Höhe nicht. |
| p3d35-Fenster rampe_11 70–90 m | p3d31-Profilstationen belegen physische Stationsweite CELL_M=1,2 m; p3d35 verwendete intern 2,4 m. | Die alte Stationszuordnung war doppelt so groß. p3d36 verwendet 1,2 m und öffnet 0–90 m; der reale Weg endet bei 57,0 m. |

[F] Der innere p3d31-Höhenpin ist damit nachweislich stärker als die offiziellen Prüfungen und wurde durch die offiziellen R3-Zeilen sowie die harten R8/R8a-Zeilen ersetzt; die Rampenachse und der Grundriss blieben unverändert. Der unabhängige Float32-Probe-Lauf änderte die Höhe an 20,7 m um 0,440186 m, ohne an dieser Stelle einen R3-Treffer zu erzeugen. rampe_11 hat im geöffneten Profil keine innere feste/variable Naht (191/191 Punkte variabel); für rampe_2 liegt die C1-Naht bei Station 49,8 m: Höhe 1.998156 m, alte Höhe 1.990185 m, linke/rechte Steigung -0.265785174874/-0.265785174874 m/m, Differenz 6.273e-15 m/m, zweite Differenz 0.000 m/m², offizieller R3-Wölbwert 0.030425 m. Die folgenden vollständigen Profile stammen aus dem vorläufigen Float32-Diagnosekandidaten (mit unvollständiger Endpunktkulisse), nicht aus dem abschließend infeasiblen Modell; rampe_11 hat tatsächlich nur Stationen 0,0–57,0 m, danach existiert kein Wegprofil bis zum angefragten Tabellenende 95 m.

### rampe_11, Station 0–95 m (Route endet bei 57,0 m)

| Station (m) | Höhe alt (m) | Höhe Probe (m) | Steigung (m/m) | 2. Differenz (m/m²) |
|---:|---:|---:|---:|---:|
| 0.0 | 12.905089 | 12.706167 | -0.050261 | -0.010829 |
| 0.3 | 12.873007 | 12.691089 | -0.053509 | -0.017730 |
| 0.6 | 12.840296 | 12.674062 | -0.060899 | -0.022635 |
| 0.9 | 12.812773 | 12.654550 | -0.067090 | -0.043433 |
| 1.2 | 12.792789 | 12.633807 | -0.086959 | -0.135100 |
| 1.5 | 12.764262 | 12.602375 | -0.148150 | -0.091689 |
| 1.8 | 12.743932 | 12.544917 | -0.141972 | 0.086909 |
| 2.1 | 12.715954 | 12.517191 | -0.096005 | 0.064852 |
| 2.4 | 12.684733 | 12.487314 | -0.103061 | -0.023051 |
| 2.7 | 12.652833 | 12.455355 | -0.109835 | -0.021925 |
| 3.0 | 12.617188 | 12.421413 | -0.116216 | -0.020432 |
| 3.3 | 12.580020 | 12.385625 | -0.122094 | -0.018590 |
| 3.6 | 12.539977 | 12.348156 | -0.127370 | -0.016433 |
| 3.9 | 12.497537 | 12.309203 | -0.131954 | -0.059709 |
| 4.2 | 12.452740 | 12.268984 | -0.163195 | -0.069190 |
| 4.5 | 12.398803 | 12.211286 | -0.173468 | -0.126922 |
| 4.8 | 12.356324 | 12.164903 | -0.239348 | -0.249239 |
| 5.1 | 12.301162 | 12.067677 | -0.323012 | -0.071126 |
| 5.4 | 12.251425 | 11.971096 | -0.282024 | 0.215136 |
| 5.7 | 12.196094 | 11.898463 | -0.193930 | 0.230396 |
| 6.0 | 12.139040 | 11.854738 | -0.143786 | 0.158066 |
| 6.3 | 12.065541 | 11.812191 | -0.099091 | 0.146304 |
| 6.6 | 12.020420 | 11.795283 | -0.056004 | 0.118780 |
| 6.9 | 11.940252 | 11.778589 | -0.027823 | -0.274639 |
| 7.2 | 11.896936 | 11.778589 | -0.220787 | -0.434360 |
| 7.5 | 11.746936 | 11.646117 | -0.288440 | 0.254012 |
| 7.8 | 11.624545 | 11.605525 | -0.068380 | 0.479520 |
| 8.1 | 11.545345 | 11.605089 | -0.000727 | 0.113966 |
| 8.4 | 11.517957 | 11.605089 | 0.000000 | -0.005870 |
| 8.7 | 11.496419 | 11.605089 | -0.004250 | -0.123480 |
| 9.0 | 11.448132 | 11.602539 | -0.074088 | -0.252882 |
| 9.3 | 11.347443 | 11.560636 | -0.155979 | -0.120896 |
| 9.6 | 11.251246 | 11.508952 | -0.146626 | 0.035509 |
| 9.9 | 11.222122 | 11.472660 | -0.134673 | -0.010318 |
| 10.2 | 11.190181 | 11.428148 | -0.152817 | -0.042742 |
| 10.5 | 11.156636 | 11.380971 | -0.160318 | -0.023147 |
| 10.8 | 11.096844 | 11.331957 | -0.166705 | -0.022108 |
| 11.1 | 11.024651 | 11.280948 | -0.173583 | -0.023604 |
| 11.4 | 10.951055 | 11.227807 | -0.180868 | -0.024825 |
| 11.7 | 10.872237 | 11.172427 | -0.188478 | -0.025789 |
| 12.0 | 10.797924 | 11.114720 | -0.196341 | -0.026527 |
| 12.3 | 10.720711 | 11.054622 | -0.204395 | -0.027074 |
| 12.6 | 10.637001 | 10.992084 | -0.212586 | -0.027462 |
| 12.9 | 10.553894 | 10.927071 | -0.220872 | -0.027726 |
| 13.2 | 10.466211 | 10.859561 | -0.229221 | -0.027894 |
| 13.5 | 10.374084 | 10.789538 | -0.237609 | -0.027979 |
| 13.8 | 10.283016 | 10.716995 | -0.246008 | -0.027993 |
| 14.1 | 10.187383 | 10.641933 | -0.254404 | -0.027956 |
| 14.4 | 10.083424 | 10.564353 | -0.262782 | -0.027844 |
| 14.7 | 9.977950 | 10.484264 | -0.271111 | -0.027634 |
| 15.0 | 9.879534 | 10.401686 | -0.279362 | -0.027314 |
| 15.3 | 9.787748 | 10.316647 | -0.287499 | -0.026849 |
| 15.6 | 9.696688 | 10.229187 | -0.295472 | -0.026197 |
| 15.9 | 9.609547 | 10.139364 | -0.303217 | -0.025318 |
| 16.2 | 9.520350 | 10.047256 | -0.310663 | -0.024176 |
| 16.5 | 9.429215 | 9.952966 | -0.317723 | -0.023011 |
| 16.8 | 9.336291 | 9.856623 | -0.324469 | -0.020977 |
| 17.1 | 9.241750 | 9.758284 | -0.330309 | -0.018334 |
| 17.4 | 9.145799 | 9.658437 | -0.335470 | -0.016461 |
| 17.7 | 9.048666 | 9.557003 | -0.340186 | -0.014004 |
| 18.0 | 8.950605 | 9.454326 | -0.343872 | -0.101582 |
| 18.3 | 8.829225 | 9.350679 | -0.401135 | -0.224197 |
| 18.6 | 8.679225 | 9.213645 | -0.478390 | -0.108480 |
| 18.9 | 8.529225 | 9.063645 | -0.466223 | 0.020279 |
| 19.2 | 8.434872 | 8.933911 | -0.466223 | 0.043195 |
| 19.5 | 8.306341 | 8.783911 | -0.440306 | 0.170980 |
| 19.8 | 8.208747 | 8.669727 | -0.363635 | 0.162005 |
| 20.1 | 8.112218 | 8.565730 | -0.343103 | 0.044250 |
| 20.4 | 8.016995 | 8.463866 | -0.337085 | 0.018306 |
| 20.7 | 7.923293 | 8.363479 | -0.332120 | 0.017729 |
| 21.0 | 7.831298 | 8.264594 | -0.326448 | 0.020291 |
| 21.3 | 7.741169 | 8.167610 | -0.319945 | 0.032142 |
| 21.6 | 7.653036 | 8.072627 | -0.307162 | 0.023674 |
| 21.9 | 7.570561 | 7.983313 | -0.305741 | 0.005280 |
| 22.2 | 7.483159 | 7.889183 | -0.303994 | 0.025854 |
| 22.5 | 7.401559 | 7.800916 | -0.290228 | 0.036380 |
| 22.8 | 7.322250 | 7.715046 | -0.282166 | 0.027088 |
| 23.1 | 7.245263 | 7.631616 | -0.273975 | 0.028190 |
| 23.4 | 7.170621 | 7.550660 | -0.265252 | 0.027692 |
| 23.7 | 7.098335 | 7.472465 | -0.257360 | 0.026436 |
| 24.0 | 7.028410 | 7.396244 | -0.249391 | 0.027918 |
| 24.3 | 6.960844 | 7.322830 | -0.240610 | 0.028977 |
| 24.6 | 6.895628 | 7.251878 | -0.232005 | 0.027894 |
| 24.9 | 6.832744 | 7.183628 | -0.223874 | 0.026960 |
| 25.2 | 6.772164 | 7.117554 | -0.215829 | 0.027632 |
| 25.5 | 6.713844 | 7.054131 | -0.207295 | 0.027782 |
| 25.8 | 6.657730 | 6.993177 | -0.199159 | 0.026872 |
| 26.1 | 6.603743 | 6.934635 | -0.191172 | 0.027449 |
| 26.4 | 6.551783 | 6.878474 | -0.182690 | 0.025556 |
| 26.7 | 6.501727 | 6.825021 | -0.175838 | 0.029279 |
| 27.0 | 6.453422 | 6.772972 | -0.165122 | 0.023200 |
| 27.3 | 6.406688 | 6.725948 | -0.161918 | 0.024162 |
| 27.6 | 6.363824 | 6.675821 | -0.150625 | 0.019711 |
| 27.9 | 6.327103 | 6.635573 | -0.150091 | 0.022118 |
| 28.2 | 6.281917 | 6.585766 | -0.137354 | 0.015099 |
| 28.5 | 6.273711 | 6.553160 | -0.141032 | 0.081810 |
| 28.8 | 6.273711 | 6.501147 | -0.088269 | 0.232418 |
| 29.1 | 6.218143 | 6.500199 | -0.001581 | 0.147115 |
| 29.4 | 6.157728 | 6.500199 | 0.000000 | 0.002635 |
| 29.7 | 6.060348 | 6.500199 | 0.000000 | -0.110560 |
| 30.0 | 6.038732 | 6.500199 | -0.066336 | -0.224475 |
| 30.3 | 5.973803 | 6.460397 | -0.134685 | -0.112791 |
| 30.6 | 5.908878 | 6.419388 | -0.134011 | -0.001403 |
| 30.9 | 5.841333 | 6.379991 | -0.135527 | -0.018574 |
| 31.2 | 5.772443 | 6.338072 | -0.145155 | -0.025886 |
| 31.5 | 5.701976 | 6.292898 | -0.151059 | -0.011166 |
| 31.8 | 5.628841 | 6.247437 | -0.151855 | -0.063517 |
| 32.1 | 5.553763 | 6.201785 | -0.189169 | -0.182397 |
| 32.4 | 5.476745 | 6.133935 | -0.261293 | -0.182253 |
| 32.7 | 5.399203 | 6.045009 | -0.298521 | -0.002048 |
| 33.0 | 5.318817 | 5.954823 | -0.262522 | 0.197804 |
| 33.3 | 5.232402 | 5.887496 | -0.179839 | 0.239725 |
| 33.6 | 5.139748 | 5.846920 | -0.118687 | 0.082947 |
| 33.9 | 5.045464 | 5.816284 | -0.130071 | -0.036741 |
| 34.2 | 4.954071 | 5.768877 | -0.140731 | 0.027259 |
| 34.5 | 4.823442 | 5.731845 | -0.113715 | 0.042341 |
| 34.8 | 4.673442 | 5.700648 | -0.115327 | 0.051157 |
| 35.1 | 4.523442 | 5.662649 | -0.083021 | 0.020279 |
| 35.4 | 4.404452 | 5.650835 | -0.103159 | -0.077410 |
| 35.7 | 4.274776 | 5.600753 | -0.129467 | 0.021631 |
| 36.0 | 4.191081 | 5.573155 | -0.090181 | 0.075130 |
| 36.3 | 4.137136 | 5.546645 | -0.084389 | 0.042005 |
| 36.6 | 4.113860 | 5.522522 | -0.064978 | 0.082197 |
| 36.9 | 4.100060 | 5.507658 | -0.035071 | 0.073726 |
| 37.2 | 4.100060 | 5.501479 | -0.020742 | 0.008235 |
| 37.5 | 4.100060 | 5.495213 | -0.030130 | -0.038665 |
| 37.8 | 4.100060 | 5.483401 | -0.043941 | -0.030635 |
| 38.1 | 4.100060 | 5.468848 | -0.048511 | -0.007616 |
| 38.4 | 4.100060 | 5.454295 | -0.048511 | 0.012949 |
| 38.7 | 4.100060 | 5.439741 | -0.040742 | 0.053252 |
| 39.0 | 4.100060 | 5.429850 | -0.016560 | 0.062963 |
| 39.3 | 4.100060 | 5.429806 | -0.002964 | 0.011437 |
| 39.6 | 4.100060 | 5.428071 | -0.009697 | -0.017966 |
| 39.9 | 4.100060 | 5.423987 | -0.013743 | -0.006973 |
| 40.2 | 4.092111 | 5.419825 | -0.013881 | -0.000241 |
| 40.5 | 4.083911 | 5.415659 | -0.013888 | -0.000012 |
| 40.8 | 4.080261 | 5.411492 | -0.013888 | 0.000000 |
| 41.1 | 4.075349 | 5.407326 | -0.013888 | -0.000000 |
| 41.4 | 4.072651 | 5.403160 | -0.013888 | 0.000023 |
| 41.7 | 4.075321 | 5.398993 | -0.013874 | 0.000077 |
| 42.0 | 4.067432 | 5.394835 | -0.013842 | 0.011294 |
| 42.3 | 4.054987 | 5.390688 | -0.007098 | 0.022761 |
| 42.6 | 4.050919 | 5.390577 | -0.000186 | 0.011829 |
| 42.9 | 4.050919 | 5.390577 | 0.000000 | 0.000309 |
| 43.2 | 4.049386 | 5.390577 | 0.000000 | 0.000000 |
| 43.5 | 4.045132 | 5.390577 | 0.000000 | 0.000000 |
| 43.8 | 4.031384 | 5.390577 | 0.000000 | 0.000000 |
| 44.1 | 3.957879 | 5.390577 | 0.000000 | -0.011282 |
| 44.4 | 3.858984 | 5.390577 | -0.006769 | -0.016236 |
| 44.7 | 3.760090 | 5.386515 | -0.009741 | -0.006834 |
| 45.0 | 3.661332 | 5.384732 | -0.010870 | -0.015999 |
| 45.3 | 3.568195 | 5.379994 | -0.019341 | -0.009572 |
| 45.6 | 3.478928 | 5.373128 | -0.016613 | 0.023390 |
| 45.9 | 3.383099 | 5.370026 | -0.005307 | 0.014440 |
| 46.2 | 3.272857 | 5.369943 | -0.007949 | -0.052258 |
| 46.5 | 3.140282 | 5.365257 | -0.036662 | -0.099787 |
| 46.8 | 2.990282 | 5.347946 | -0.067821 | -0.051789 |
| 47.1 | 2.842267 | 5.324564 | -0.067735 | -0.005860 |
| 47.4 | 2.748346 | 5.307305 | -0.071337 | -0.023709 |
| 47.7 | 2.644783 | 5.281762 | -0.081961 | -0.024222 |
| 48.0 | 2.591121 | 5.258129 | -0.085870 | -0.024448 |
| 48.3 | 2.531670 | 5.230240 | -0.096630 | -0.030035 |
| 48.6 | 2.444417 | 5.200151 | -0.103892 | -0.023888 |
| 48.9 | 2.351584 | 5.167905 | -0.110963 | -0.023061 |
| 49.2 | 2.262518 | 5.133574 | -0.117728 | -0.021846 |
| 49.5 | 2.151725 | 5.097268 | -0.124070 | -0.021197 |
| 49.8 | 2.049578 | 5.059132 | -0.130446 | -0.018247 |
| 50.1 | 1.979023 | 5.019000 | -0.135018 | -0.028090 |
| 50.4 | 1.930753 | 4.978121 | -0.147300 | -0.058889 |
| 50.7 | 1.862853 | 4.930620 | -0.170352 | -0.096157 |
| 51.0 | 1.792269 | 4.875910 | -0.204994 | -0.138552 |
| 51.3 | 1.708733 | 4.807624 | -0.253483 | -0.136215 |
| 51.6 | 1.618028 | 4.723820 | -0.286723 | 0.024566 |
| 51.9 | 1.479137 | 4.635590 | -0.238743 | 0.159961 |
| 52.2 | 1.399934 | 4.580574 | -0.190746 | 0.090988 |
| 52.5 | 1.326399 | 4.521143 | -0.184151 | 0.062834 |
| 52.8 | 1.251564 | 4.470083 | -0.153045 | 0.081343 |
| 53.1 | 1.176222 | 4.429315 | -0.135345 | 0.036498 |
| 53.4 | 1.101256 | 4.388876 | -0.131147 | 0.018159 |
| 53.7 | 1.027409 | 4.350628 | -0.124450 | 0.022384 |
| 54.0 | 0.954838 | 4.314206 | -0.117716 | 0.021891 |
| 54.3 | 0.899731 | 4.279998 | -0.111315 | 0.021889 |
| 54.6 | 0.839401 | 4.247417 | -0.104583 | 0.024106 |
| 54.9 | 0.771908 | 4.217248 | -0.096852 | 0.030242 |
| 55.2 | 0.716475 | 4.189306 | -0.086437 | 0.024872 |
| 55.5 | 0.673302 | 4.165386 | -0.081928 | 0.014900 |
| 55.8 | 0.646241 | 4.140149 | -0.077497 | 0.026029 |
| 56.1 | 0.614113 | 4.118888 | -0.066311 | 0.028648 |
| 56.4 | 0.583640 | 4.100363 | -0.060308 | 0.019516 |
| 56.7 | 0.546556 | 4.082703 | -0.054602 | 0.016618 |
| 57.0 | 0.510542 | 4.067601 | -0.050338 | 0.014214 |

### rampe_2, Station 0–55 m

| Station (m) | Höhe alt (m) | Höhe Probe (m) | Steigung (m/m) | 2. Differenz (m/m²) |
|---:|---:|---:|---:|---:|
| 0.0 | 12.469810 | 12.023638 | -0.050272 | -0.010873 |
| 0.3 | 12.448156 | 12.008556 | -0.053534 | -0.016598 |
| 0.6 | 12.426416 | 11.991518 | -0.060231 | -0.022866 |
| 0.9 | 12.401412 | 11.972418 | -0.067254 | -0.023884 |
| 1.2 | 12.376370 | 11.951165 | -0.074561 | -0.024764 |
| 1.5 | 12.347944 | 11.927681 | -0.082112 | -0.025507 |
| 1.8 | 12.319518 | 11.901898 | -0.089865 | -0.026119 |
| 2.1 | 12.287682 | 11.873762 | -0.097783 | -0.026609 |
| 2.4 | 12.255834 | 11.843228 | -0.105831 | -0.026989 |
| 2.7 | 12.255834 | 11.810263 | -0.113977 | -0.027274 |
| 3.0 | 12.255834 | 11.774842 | -0.122195 | -0.027480 |
| 3.3 | 12.244160 | 11.736946 | -0.130464 | -0.027621 |
| 3.6 | 12.229111 | 11.696564 | -0.138768 | -0.027713 |
| 3.9 | 12.198521 | 11.653686 | -0.147092 | -0.027770 |
| 4.2 | 12.167258 | 11.608308 | -0.155430 | -0.027801 |
| 4.5 | 12.132547 | 11.560428 | -0.163773 | -0.027811 |
| 4.8 | 12.097841 | 11.510044 | -0.172116 | -0.027807 |
| 5.1 | 12.059124 | 11.457158 | -0.180457 | -0.027799 |
| 5.4 | 12.020291 | 11.401770 | -0.188796 | -0.027790 |
| 5.7 | 11.977301 | 11.343881 | -0.197131 | -0.027781 |
| 6.0 | 11.934136 | 11.283491 | -0.205464 | -0.027776 |
| 6.3 | 11.886566 | 11.220602 | -0.213796 | -0.027774 |
| 6.6 | 11.839030 | 11.155214 | -0.222129 | -0.027777 |
| 6.9 | 11.787178 | 11.087325 | -0.230463 | -0.027787 |
| 7.2 | 11.734756 | 11.016936 | -0.238801 | -0.027802 |
| 7.5 | 11.678319 | 10.944045 | -0.247144 | -0.027824 |
| 7.8 | 11.621193 | 10.868649 | -0.255495 | -0.027849 |
| 8.1 | 11.560750 | 10.790748 | -0.263854 | -0.027875 |
| 8.4 | 11.498291 | 10.710337 | -0.272220 | -0.027896 |
| 8.7 | 11.432297 | 10.627416 | -0.280591 | -0.027901 |
| 9.0 | 11.366035 | 10.541983 | -0.288961 | -0.027876 |
| 9.3 | 11.295639 | 10.454039 | -0.297317 | -0.027802 |
| 9.6 | 11.224427 | 10.363592 | -0.305642 | -0.027653 |
| 9.9 | 11.149366 | 10.270654 | -0.313909 | -0.027400 |
| 10.2 | 11.073474 | 10.175247 | -0.322082 | -0.027006 |
| 10.5 | 10.991237 | 10.077405 | -0.330113 | -0.026435 |
| 10.8 | 10.907963 | 9.977179 | -0.337942 | -0.025643 |
| 11.1 | 10.820650 | 9.874640 | -0.345499 | -0.024593 |
| 11.4 | 10.732512 | 9.769880 | -0.352698 | -0.023249 |
| 11.7 | 10.639165 | 9.663021 | -0.359448 | -0.021583 |
| 12.0 | 10.543779 | 9.554212 | -0.365648 | -0.019580 |
| 12.3 | 10.442234 | 9.443632 | -0.371196 | -0.017237 |
| 12.6 | 10.339087 | 9.331494 | -0.375990 | -0.062620 |
| 12.9 | 10.242306 | 9.218038 | -0.408768 | -0.156141 |
| 13.2 | 10.146814 | 9.086233 | -0.469675 | -0.152053 |
| 13.5 | 10.041532 | 8.936233 | -0.500000 | -0.050542 |
| 13.8 | 9.933838 | 8.786233 | -0.500000 | -0.000000 |
| 14.1 | 9.822822 | 8.636233 | -0.500000 | 0.082930 |
| 14.4 | 9.710628 | 8.486233 | -0.450242 | 0.181976 |
| 14.7 | 9.595002 | 8.366088 | -0.390815 | 0.118213 |
| 15.0 | 9.478292 | 8.251744 | -0.379315 | 0.026000 |
| 15.3 | 9.357597 | 8.138499 | -0.375214 | 0.015055 |
| 15.6 | 9.235619 | 8.026616 | -0.370282 | 0.017670 |
| 15.9 | 9.105719 | 7.916330 | -0.364612 | 0.019955 |
| 16.2 | 8.973414 | 7.807848 | -0.358309 | 0.021899 |
| 16.5 | 8.839964 | 7.701345 | -0.351473 | 0.023507 |
| 16.8 | 8.706290 | 7.596965 | -0.344204 | 0.024798 |
| 17.1 | 8.571890 | 7.494822 | -0.336594 | 0.025801 |
| 17.4 | 8.437761 | 7.395008 | -0.328724 | 0.026552 |
| 17.7 | 8.297050 | 7.297588 | -0.320663 | 0.027089 |
| 18.0 | 8.153484 | 7.202610 | -0.312470 | 0.027455 |
| 18.3 | 8.005455 | 7.110106 | -0.304190 | 0.027687 |
| 18.6 | 7.855455 | 7.020096 | -0.295858 | 0.027820 |
| 18.9 | 7.707975 | 6.932591 | -0.287499 | 0.027883 |
| 19.2 | 7.560441 | 6.847597 | -0.279128 | 0.027902 |
| 19.5 | 7.419894 | 6.765114 | -0.270758 | 0.027894 |
| 19.8 | 7.281330 | 6.685142 | -0.262392 | 0.027874 |
| 20.1 | 7.151310 | 6.607679 | -0.254033 | 0.027850 |
| 20.4 | 7.024110 | 6.532722 | -0.245682 | 0.027827 |
| 20.7 | 6.899746 | 6.460270 | -0.237337 | 0.027810 |
| 21.0 | 6.778757 | 6.390320 | -0.228996 | 0.027798 |
| 21.3 | 6.659922 | 6.322872 | -0.220658 | 0.027791 |
| 21.6 | 6.540496 | 6.257925 | -0.212322 | 0.027788 |
| 21.9 | 6.421535 | 6.195479 | -0.203986 | 0.027786 |
| 22.2 | 6.301968 | 6.135534 | -0.195650 | 0.027781 |
| 22.5 | 6.182906 | 6.078089 | -0.187317 | 0.027770 |
| 22.8 | 6.063112 | 6.023143 | -0.178988 | -0.083363 |
| 23.1 | 5.945836 | 5.970696 | -0.237335 | -0.083401 |
| 23.4 | 5.831002 | 5.880742 | -0.229029 | 0.138760 |
| 23.7 | 5.726366 | 5.833278 | -0.154079 | 0.138667 |
| 24.0 | 5.633417 | 5.788295 | -0.145829 | 0.027419 |
| 24.3 | 5.541686 | 5.745781 | -0.137627 | 0.027235 |
| 24.6 | 5.445037 | 5.705719 | -0.129488 | 0.026999 |
| 24.9 | 5.347548 | 5.668088 | -0.121428 | 0.026701 |
| 25.2 | 5.247491 | 5.632862 | -0.113467 | 0.026331 |
| 25.5 | 5.149916 | 5.600007 | -0.105629 | 0.025885 |
| 25.8 | 5.059055 | 5.569484 | -0.097937 | 0.025356 |
| 26.1 | 4.947978 | 5.541245 | -0.090415 | 0.024742 |
| 26.4 | 4.813953 | 5.515235 | -0.083091 | 0.057329 |
| 26.7 | 4.716424 | 5.491390 | -0.056018 | 0.078145 |
| 27.0 | 4.658087 | 5.481624 | -0.036204 | 0.025263 |
| 27.3 | 4.588834 | 5.469668 | -0.040860 | -0.009356 |
| 27.6 | 4.516572 | 5.457108 | -0.041818 | -0.001506 |
| 27.9 | 4.444276 | 5.444577 | -0.041763 | 0.000102 |
| 28.2 | 4.371976 | 5.432050 | -0.041757 | 0.000011 |
| 28.5 | 4.294335 | 5.419523 | -0.041757 | 0.028176 |
| 28.8 | 4.223831 | 5.406996 | -0.024851 | 0.062974 |
| 29.1 | 4.159449 | 5.404612 | -0.003973 | 0.041418 |
| 29.4 | 4.111556 | 5.404612 | 0.000000 | 0.006621 |
| 29.7 | 4.076493 | 5.404612 | 0.000000 | 0.000000 |
| 30.0 | 4.076493 | 5.404612 | 0.000000 | -0.000000 |
| 30.3 | 4.076493 | 5.404612 | -0.000000 | -0.000000 |
| 30.6 | 4.076493 | 5.404612 | 0.000000 | 0.000000 |
| 30.9 | 4.076493 | 5.404612 | 0.000000 | 0.000000 |
| 31.2 | 4.076493 | 5.404612 | 0.000000 | 0.000000 |
| 31.5 | 4.071804 | 5.404612 | 0.000000 | -0.000000 |
| 31.8 | 4.071804 | 5.404612 | -0.000000 | 0.003353 |
| 32.1 | 4.071661 | 5.404612 | 0.002012 | 0.020940 |
| 32.4 | 4.069486 | 5.405820 | 0.012564 | 0.014233 |
| 32.7 | 4.065246 | 5.412151 | 0.010552 | -0.020940 |
| 33.0 | 4.065243 | 5.412151 | 0.000000 | -0.017586 |
| 33.3 | 4.063035 | 5.412151 | 0.000000 | 0.000000 |
| 33.6 | 4.045427 | 5.412151 | 0.000000 | -0.020802 |
| 33.9 | 4.026791 | 5.412151 | -0.012481 | -0.045754 |
| 34.2 | 4.016937 | 5.404662 | -0.027453 | -0.038575 |
| 34.5 | 4.016937 | 5.395679 | -0.035626 | -0.023918 |
| 34.8 | 3.998436 | 5.383287 | -0.041803 | -0.011132 |
| 35.1 | 3.972291 | 5.370597 | -0.042305 | -0.000849 |
| 35.4 | 3.963651 | 5.357904 | -0.042313 | -0.000013 |
| 35.7 | 3.961552 | 5.345210 | -0.042313 | 0.000080 |
| 36.0 | 3.961552 | 5.332516 | -0.042264 | -0.030593 |
| 36.3 | 3.961552 | 5.319851 | -0.060668 | -0.067542 |
| 36.6 | 3.936517 | 5.296115 | -0.082789 | -0.049267 |
| 36.9 | 3.933205 | 5.270177 | -0.090229 | -0.025110 |
| 37.2 | 3.933205 | 5.241978 | -0.097855 | -0.025685 |
| 37.5 | 3.933205 | 5.211464 | -0.105640 | -0.026165 |
| 37.8 | 3.933205 | 5.178594 | -0.113554 | -0.026562 |
| 38.1 | 3.933205 | 5.143332 | -0.121577 | -0.026885 |
| 38.4 | 3.928109 | 5.105648 | -0.129685 | -0.027142 |
| 38.7 | 3.918000 | 5.065520 | -0.137862 | -0.027342 |
| 39.0 | 3.884541 | 5.022931 | -0.146091 | -0.027494 |
| 39.3 | 3.845652 | 4.977866 | -0.154359 | -0.027608 |
| 39.6 | 3.812169 | 4.930316 | -0.162655 | -0.027692 |
| 39.9 | 3.789403 | 4.880273 | -0.170974 | -0.027755 |
| 40.2 | 3.774670 | 4.827732 | -0.179308 | -0.027804 |
| 40.5 | 3.763668 | 4.772688 | -0.187656 | -0.027845 |
| 40.8 | 3.746477 | 4.715138 | -0.196015 | -0.027879 |
| 41.1 | 3.724547 | 4.655079 | -0.204384 | -0.027907 |
| 41.4 | 3.696350 | 4.592508 | -0.212759 | -0.027924 |
| 41.7 | 3.664757 | 4.527423 | -0.221138 | -0.027920 |
| 42.0 | 3.628655 | 4.459825 | -0.229511 | -0.027882 |
| 42.3 | 3.590352 | 4.389717 | -0.237867 | -0.027788 |
| 42.6 | 3.549642 | 4.317105 | -0.246184 | -0.027612 |
| 42.9 | 3.507030 | 4.242006 | -0.254434 | -0.027321 |
| 43.2 | 3.461655 | 4.164445 | -0.262577 | -0.026879 |
| 43.5 | 3.414695 | 4.084460 | -0.270561 | -0.026244 |
| 43.8 | 3.365068 | 4.002108 | -0.278323 | -0.025374 |
| 44.1 | 3.313495 | 3.917466 | -0.285786 | -0.024232 |
| 44.4 | 3.258865 | 3.830637 | -0.292862 | -0.022784 |
| 44.7 | 3.202180 | 3.741749 | -0.299456 | -0.021004 |
| 45.0 | 3.138729 | 3.650963 | -0.305464 | -0.018880 |
| 45.3 | 3.070417 | 3.558470 | -0.310784 | -0.016415 |
| 45.6 | 3.000029 | 3.464493 | -0.315313 | -0.013630 |
| 45.9 | 2.928065 | 3.369282 | -0.318962 | -0.021718 |
| 46.2 | 2.856129 | 3.273116 | -0.328344 | -0.165175 |
| 46.5 | 2.783953 | 3.172276 | -0.418067 | -0.286093 |
| 46.8 | 2.713181 | 3.022276 | -0.500000 | -0.128389 |
| 47.1 | 2.647029 | 2.872276 | -0.495100 | 0.157306 |
| 47.4 | 2.575444 | 2.725215 | -0.405616 | 0.292581 |
| 47.7 | 2.501948 | 2.628906 | -0.319552 | 0.149115 |
| 48.0 | 2.428499 | 2.533484 | -0.316147 | 0.012742 |
| 48.3 | 2.355263 | 2.439217 | -0.311906 | 0.015354 |
| 48.6 | 2.282194 | 2.346341 | -0.306935 | 0.017592 |
| 48.9 | 2.209220 | 2.255056 | -0.301351 | 0.019432 |
| 49.2 | 2.136293 | 2.165530 | -0.295275 | 0.037322 |
| 49.5 | 2.062919 | 2.077891 | -0.278958 | 0.049151 |
| 49.8 | 1.990185 | 1.998156 | -0.265785 | 0.045237 |
| 50.1 | 1.918420 | 1.918420 | -0.251816 | 0.047648 |
| 50.4 | 1.847066 | 1.847066 | -0.237196 | 0.027001 |
| 50.7 | 1.776102 | 1.776102 | -0.235615 | 0.005592 |
| 51.0 | 1.705697 | 1.705697 | -0.233841 | 0.006337 |
| 51.3 | 1.635798 | 1.635798 | -0.231813 | 0.007309 |
| 51.6 | 1.566609 | 1.566609 | -0.229456 | 0.008372 |
| 51.9 | 1.498124 | 1.498124 | -0.226790 | 0.009426 |
| 52.2 | 1.430535 | 1.430535 | -0.223800 | 0.010475 |
| 52.5 | 1.363844 | 1.363844 | -0.220505 | 0.011698 |
| 52.8 | 1.298232 | 1.298232 | -0.216781 | 0.012961 |
| 53.1 | 1.233775 | 1.233775 | -0.212729 | 0.014259 |
| 53.4 | 1.170595 | 1.170595 | -0.208226 | 0.015525 |
| 53.7 | 1.108840 | 1.108840 | -0.203414 | 0.016900 |
| 54.0 | 1.048547 | 1.048547 | -0.198086 | 0.018223 |
| 54.3 | 0.989988 | 0.989988 | -0.192480 | 0.019506 |
| 54.6 | 0.933059 | 0.933059 | -0.186383 | 0.020682 |
| 54.9 | 0.878158 | 0.878158 | -0.180071 | 0.021859 |

## 2. Querabfluss-Schutz

[R] pruefe_regeln.py enthält keine eigenständige Prüfung „Querabfluss über das Wegband“. r8_kreuzung.py hat R8_quer mit einer offiziellen 3%-Grenze an Kreuzungs-/Weggruppen; diese vorhandene Entsprechung wurde entlang des D1-Wegbands als lineare ±1,5-m-Seitenhöhenbedingung umgesetzt: |h_plus−h_minus| ≤ 0,03·3,0−0,0001 m. Die linearen ±1,5-m-Seitenhöhenzeilen setzen diese vorhandene 3%-Schwelle im D1-Wegband um; je Station begrenzen zwei lineare Ungleichungen die Höhendifferenz auf höchstens 0,0899 m und lassen die Prüfschwelle unverändert.

[R] Zusätzlich wurde p3d30s interne Formulierung „kein Quergefälle quer über die Wegachse“ als exakte lineare Gleichheit h_plus=h_minus getestet. Die Nullquer-Variante war infeasible; ihr elastischer All-Familien-Filter benötigte 0,052155291 m Seitendifferenz am Mittelpunkt [150,479827|13,665811], also 1,738510 % über 3 m. Diese Differenz liegt unter dem offiziellen 3%-Limit von 0,09 m. Damit ist die Nullquer-Zeile nachweislich strenger als die offizielle R8-Entsprechung.

[F] Die Nullquer-Zeile wurde als ein weiterer nachgewiesen strenger interner Blocker durch die offizielle 3%-Zeile ersetzt; `P3D36_DRAINAGE_POLICY=zero` hält die strengere Probe reproduzierbar. Der Standard `official` verwendet nach dieser Prüfung nur die unveränderte 3%-Grenze. Es wurde keine neue Schwelle festgelegt.

## 3. R3-, R8a- und Wegendstufen-Zeilen

[R] R3 wurde ohne Binärvariablen durch harte Einzelstichproben-Zeilen nach der Prüferformel abgebildet: Gauß-Glättung längs (σ=8 Prüfsamples), Seitenwerte bei ±1,5 m quer zur Achse, Wölbung zur Mittelhöhe der Seitenwerte, 16 Samples pro offizieller Sektion. Die verwendeten Schwellen sind exakt 0,08 m / 3,5 % / 0,08 m; Float32-Puffer 0,0001 m und 0,01 Prozentpunkte. Diese reine LP-Formulierung erzwingt konservativ null überschrittene R3-Sektionen in D1; die erlaubten Zählbudgets 6/7/7 werden nicht ausgeschöpft.

| R3-Regel | LP-Doppelpräzision: größter D1-Sektionswert | Float32: größter D1-Sektionswert | Offizieller D1-Treffer | Zählung identisch |
|---|---:|---:|---:|---|
| R3_laengs_m | 0.079900001 | 0.079900304 | 0 | True |
| R3_quer_pct | 3.431475100 | 3.431475140 | 0 | True |
| R3_woelb_m | 0.079900001 | 0.079900253 | 0 | True |

[S] Der offizielle Float32-Prüfer und die unabhängige Formelprobe stimmen für alle drei R3-Regeln bei D1 0/0/0 Treffern überein. R8a verwendet dieselbe lineare Höheninterpolation wie der Export, den offiziellen wall mask (Gradient >1 ausgeschlossen), die offizielle 0,10/0,18-m-Paargrenze und 0,0001-m Float32-Puffer; sobald der offizielle Checker Treffer meldet, werden die maßgeblichen Paare als harte Lazy-Cut-Zeilen ergänzt. Für den vorläufigen Diagnosekandidaten wurden drei Lazy-Cuts abgeleitet: rampe_2_anfang, rampe_11_anfang und rampe_11_ende. Die R8a-Maske wurde nicht durch eine pauschale Zeile über WAND-Zellen ersetzt.

[R] Der abschließende Modellcode legt den Endpunktstufen-Cap 0,054 m mit 0,0001-m-Puffer auf benachbarte Paare im 4-m-Band an allen vier Rampenenden. Die folgende R8a-Liste gehört nur zum vorläufigen Float32-Diagnosekandidaten; der abschließende infeasible LP erreichte keinen Float32-Export:

| Wegende | Karte | Checkerwert | Grenze | Ergebnis |
|---|---|---:|---:|---|
| rampe_2_anfang | 126,5|31,6 | 0,23 m | 0,18 m Ausnahme | überschritten |
| rampe_11_anfang | 148,5|2,5 | 0,21 m | 0,10 m | überschritten |
| rampe_11_ende | 156,5|37,5 | 0,13 m | 0,10 m | überschritten |

Im vorläufigen Kandidaten maß die offizielle R8-Kreuzungsgruppe bei [152,6|28,4] Stufe 0,011 m, Gitter 0,020 m (Prüferausgabe auf 0,001 m gerundet) und meldete keinen R8_quer-Treffer; die Kreuzungsziele werden in Probe 1 erfüllt. An den Rampenstarts blieben dagegen R8-Treffer: rampe_2_anfang Stufe 0,94 m, Gitter 1,68 m, Quer 23,3 %; rampe_11_anfang Stufe 0,57 m, Gitter 0,38 m, Quer 3,8 %. Drei neue R8-Hitrecords gegenüber dem p3d17-Replay lagen bei rampe_2_anfang (Gitter/Quer) und rampe_11_anfang (Quer). R8a hatte keine neue D1-Signatur gegenüber dem Replay, überschritt aber die expliziten Startgrenzen oben.

## 4. Machbarkeit, Filter und Stopp

[S] Alle Solve-Aufrufe waren reine LPs mit einem Thread, 20.413 Variablen und null Integer-Variablen; pro Solve galt 600 s. Ein HiGHS-IIS-Lauf wurde nicht gestartet. Das Modell übernimmt die p3d31/p3d33-p3d35-Konstruktion: D1-Fenster mit p3d17-festen Außenwerten, harte Lokalität und Klippenform außerhalb der ausgeschlossenen Bänder, sowie die offizielle Plattform-/Profilbedingung am Kreuzungspunkt [152,5|28,5]. Der p3d17-Referenzkörper wurde für die Bewegungsstrafe verwendet; es gab keinen MIP-Warmstart.

[S] Priority-Flood lief deterministisch mit 1-mm-Epsilon, 8er-Nachbarschaft und den geschützten Weg-/Klippen-/Fenster-/Ankerbereichen. Im ersten Float32-Kandidaten waren keine Flood-Floor-Cuts nötig; 18 tiefe Spill-Punkte blieben wegen des lokalen LP-Schutzes unangetastet. Die 24 nach der Probe abgeleiteten lokalen Cuts waren G5 6, G6 3, R5-Loch 7, R8a 3 und R9w 5. Runde 2 mit diesen 24 Cuts war strukturell infeasible.

[A] Das LP exportiert 34 Solver-Zeilenfamilien einschließlich Stütz-, Event- und Prüfzeilen. Wie schon p3d35 dokumentiert, ist keine belastbare 1:1-Gruppierung in die angeforderten 22 übergeordneten Familien nachgewiesen; dieser Familien-Auditpunkt bleibt offen.

| Lauf | Modell / Cuts | Ergebnis | Diagnostik |
|---|---|---|---|
| p3d36-Vorlauf mit p3d35-kompatiblen R3-Selektoren | LP optimal, Float32-Probe; vor der harten R3- und korrigierten Stationsfassung | Nur Diagnose, kein freizugebender Entwurf | D1 R3 12/1/20; Gesamtzahlen siehe Probevergleich. Runde danach infeasible. |
| Nullquer-Hardtest | exakte p3d30-Gleichheit plus offizielle 3%-Zeile | infeasible | All-Familien-Filter: Nullquer braucht 0,052155291 m am Ort [150,479827|13,665811] (1,738510 %). |
| Vorläufige offizielle Ersatzfassung, Probe 1 | R3 hard, R8 3 %, R8a lazy; alte Endpunktkulisse mit 460 Paaren; 0 Event-Cuts | LP optimal; Float32-Diagnosekandidat | Gateziele nicht erreicht; 24 lokale Schnitte erzeugt. |
| Vorläufige offizielle Ersatzfassung, Runde 2 | 24 deduplizierte/sortierte Checker-Cuts | infeasible | All-Familien-Filter benötigt Endpunktstufen-Slack 0,003951981 m und Quellmonotonie-Slack 0,017337715 m. |
| Abschließender Vier-Endpunkt-Lauf, Runde 1 | 0 Event-Cuts; Start und Ende beider Rampen | infeasible | All-Familien-Filter: tatsächliche Endpunktstufen-Überschreitung 0,004526635 m bei [147,5|5,0]–[147,5|5,25]; sonst keine positive Familienverletzung. |
| Nur 3%-Querfamilie elastisch, Runde 2 | derselbe Cut-Satz | infeasible | Das Lockern allein der offiziellen Querfamilie macht die LP nicht lösbar. |

[R] Der reproduzierte Runde-2-Filter lokalisierte die Endpunktstufe am Paar [156,5|38,25]–[156,5|38,5]: 0,057851981 m statt höchstens 0,054 m, also 0,003851981 m über der Projektgrenze. Die Quellmonotonie-Abweichung war am rampe_2-Segment Station 0,3–0,6 m, [126,758184|31,589920]–[127,006367|31,559921]: das Ausgangsprofil fällt von 12,448156 m auf 12,426416 m, die elastische Lösung steigt von 12,058781 m auf 12,076119 m, Differenz 0,017337715 m.

[A] Ein früher automatisch ausgegebener All-Familien-Filter zu Runde 2 enthielt zusätzlich 0,0148 m Quer-Slack. Die Wiederholung mit exakt sortiertem 24-Cut-Katalog war optimal ohne Quer-Slack und benötigte nur Endpunktstufen- und Quellmonotonie-Slack; ein Einzel-Querfilter blieb infeasible. Deshalb wird der erste Quer-Slack nicht als nachgewiesene Einzelursache gewertet. Die harten Endpunktziele und die Runde-2-Infeasibilität bleiben davon unberührt.

[F] Keine weitere interne Sperre wurde ersetzt: die Quer-Nullzeile ist die einzige zusätzliche, nachweislich strengere interne Formulierung, die durch die offizielle Schwelle ersetzt wurde. Die 0,054-m-Endpunktgrenze ist ein explizites Projekt-Hartziel und bleibt unverändert; nach dem infeasible Cut-LP wurde gestoppt. Es wurde kein globales MIP und kein langes IIS ausgeführt.

## 5. Float32-Proben, Treffer und Vergleich

[S] Der Legacy-Vorlauf (vor harter R3- und Stationskorrektur) hatte 586 pruefe_regeln-Treffer, R8 42 und R9 344; D1 R3 war 12/1/20, G5 68/1, G6 0, R5-Loch 25/8, R9w 287. Er ist nur ein Diagnosevergleich. Die korrigierte vorläufige Probe 1 ist ein Float32-Diagnosekandidat aus der offiziellen Ersatzfassung vor der vollständigen Vier-Endpunkt-Abdeckung; sie ist keine Abschlussprobe des finalen Modells.

| Zielwert Probe 1 | Soll | Ist | Status |
|---|---:|---:|---|
| R5-Spitze D1 | 0 | 0 | erfüllt |
| G6 D1 | ≤3 | 6 | verfehlt |
| R8b D1 | ≤1 | 1 | erfüllt |
| G3 D1 | ≤1 | 0 | erfüllt |
| R9w gesamt | ≤280 | 285 | verfehlt |
| G5 gesamt / D1 | ≤69 / ≤2 | 74 / 7 | verfehlt |
| R5-Loch gesamt / D1 | ≤22 / ≤5 | 29 / 12 | verfehlt |
| D1-R4-Schlucht | 0 | 0 | erfüllt |
| R3 D1 längs/quer/Wölbung | ≤6/7/7 | 0/0/0 | erfüllt |
| neue R8-Hitrecords vs p3d17-Replay | 0 | 3 | verfehlt |
| R8/R9 D2 | 0/0 | 0/0 | erfüllt |
| pruefe_regeln D2 neue Treffer | 0 | 0 | erfüllt |
| G1-/D2-Höhenhash | unverändert | unverändert | erfüllt |

[S] Probe 1 hatte pruefe_regeln 571 Treffer, R8 48 (Stufe 9, Gitter 10, Quer 6, R8a 23), R9 342 (R8b 23, Sägezahn 34, R9w 285). D1/G1/D2: pruefe_regeln 34/13/8, R8 9/0/0, R9 26/13/0. D2-Hitrecords waren bitgleich; außerhalb des aktiven D1-Fensters war die Probe bitgleich zur p3d17-Referenz.

[A] Versionsvergleich der Baseline: der Auftrag nennt für Stand 9d3f8fc pruefe_regeln 596, R8 48 (9/10/5/24), R9 334 (25/34/275). Die versionierten p3d17-Replay-Dateien, die der Prüferlauf selbst verwendet, enthalten dagegen pruefe_regeln 600, R8 46 (9/10/4/23) und R9 344 (23/34/287). Beide Baselines sind getrennt aufgeführt; gegen den älteren R9w-Wert 275 steigt Probe 1 um 10, gegen die Replay-Datei fällt R9w um 2. Die geforderte R9w-Grenze 280 wird unabhängig davon verfehlt.

### pruefe_regeln je Regel: versionierter p3d17-Replay → Probe 1

| Regel | vorher gesamt | Probe gesamt | Δ | D1 vorher→Probe | G1 vorher→Probe | D2 vorher→Probe |
|---|---:|---:|---:|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 4 | 4 | +0 | 2→2 | 2→2 | 0→0 |
| G2_spitze_oben | 3 | 3 | +0 | 0→0 | 0→0 | 0→0 |
| G2_spitze_oben_fein | 8 | 8 | +0 | 0→0 | 0→0 | 0→0 |
| G3_spitze_unten | 4 | 3 | -1 | 1→0 | 0→0 | 0→0 |
| G3_spitze_unten_fein | 2 | 2 | +0 | 0→0 | 0→0 | 0→0 |
| G5_beule_klippe | 69 | 74 | +5 | 2→7 | 0→0 | 0→0 |
| G6_facette | 219 | 222 | +3 | 3→6 | 3→3 | 0→0 |
| G7_wand_glatte_flaeche | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_feld | 25 | 25 | +0 | 1→1 | 0→0 | 0→0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G7b_wandkontur_rauheit | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| R1_blind | 24 | 24 | +0 | 2→2 | 1→1 | 0→0 |
| R1_wand | 0 | 2 | +2 | 0→2 | 0→0 | 0→0 |
| R2_getrennt | 15 | 15 | +0 | 1→1 | 0→0 | 1→1 |
| R3_laengs_m | 35 | 29 | -6 | 6→0 | 1→1 | 0→0 |
| R3_quer_pct | 29 | 12 | -17 | 17→0 | 0→0 | 0→0 |
| R3_woelb_m | 31 | 12 | -19 | 19→0 | 0→0 | 0→0 |
| R4_rand | 1 | 1 | +0 | 1→1 | 0→0 | 0→0 |
| R5_loch | 25 | 29 | +4 | 8→12 | 0→0 | 0→0 |
| R6_wasser_schnee | 4 | 4 | +0 | 0→0 | 3→3 | 0→0 |
| T1_fleckrand | 94 | 94 | +0 | 0→0 | 3→3 | 7→7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 | 0→0 | 0→0 | 0→0 |

### R8 je Regel: versionierter p3d17-Replay → Probe 1

| Regel | vorher gesamt | Probe gesamt | Δ | D1 vorher→Probe | G1 vorher→Probe | D2 vorher→Probe |
|---|---:|---:|---:|---:|---:|---:|
| R8_gitter | 10 | 10 | +0 | 2→2 | 0→0 | 0→0 |
| R8_quer | 4 | 6 | +2 | 0→2 | 0→0 | 0→0 |
| R8_stufe | 9 | 9 | +0 | 2→2 | 0→0 | 0→0 |
| R8a_wegende | 23 | 23 | +0 | 3→3 | 0→0 | 0→0 |

### R9 je Regel: versionierter p3d17-Replay → Probe 1

| Regel | vorher gesamt | Probe gesamt | Δ | D1 vorher→Probe | G1 vorher→Probe | D2 vorher→Probe |
|---|---:|---:|---:|---:|---:|---:|
| R8b_delle | 23 | 23 | +0 | 1→1 | 0→0 | 0→0 |
| R9_saegezahn | 34 | 34 | +0 | 1→1 | 1→1 | 0→0 |
| R9w_wellen | 287 | 285 | -2 | 27→24 | 12→12 | 0→0 |

[S] Vergleich des vorläufigen Diagnosekandidaten mit den vorgegebenen Referenzen: p3d35 R0 hatte pruefe_regeln 607, R8 44, R9 344, R5-Loch 25/8, R9w 287 und D1 R3 13/21/20. p3d31 Runde 3 hatte G5 71/4, R5-Loch 24/7, G6 D1 2, R5-Spitze 0, R8b D1 1, R3 D1 6/7/7, R9w 283 und Kreuzung Stufe/Gitter 0,073/0,019 m. Probe 1 verbessert R3 und Kreuzungsstufe, ist aber bei G5 74/7, R5-Loch 29/12, G6 6, R9w 285 und den Rampenenden schlechter bzw. über den Zielwerten.

## 6. Mesh

[F] Kein Mesh gebaut: der abschließende Vier-Endpunkt-Lauf war bereits in Runde 1 infeasible; auch der vorläufige Diagnosekandidat verfehlte harte Ziele. Daher wurden gen_relief.py und baue_html.py nicht ausgeführt; es gibt keine Mesh-Deltas, Mesh-pytest-, xvfb-Lochscan-, t42u-, Klippen-, LOD1- oder Bildnachweise. LOD1 <1,3 Mio. Dreiecke und t42u Summe 0 sind für einen Mesh-Stand nicht neu gemessen; das Arbeitsrelief, Zellquellwerte, Overlay und G1/D2 wurden nicht verändert.

## 7. Prüfer-Diff, Hashes und Speicher

[S] Selbstberechnete SHA-256:

| Datei / Prüffeld | SHA-256 |
|---|---|
| relief3d/neu/zellen_relief.csv | 99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa |
| relief3d/neu/vektor.json | aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e |
| relief3d/neu/felder.json | e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435 |
| G1-Probehöhe | 38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb |
| D2-Probehöhe | 749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6 |
| Quelle relief V3 gzip | b1e347e048d1f26d79b812b795645bf348ef83e831209669cf5cbd2f7717b4a6 |
| Transferbasis p3d21 | 07c140cffa97df408f2c688ee910b4085e429e986b047f15b62551727ea69287 |

[S] G1/D2 hashes stimmen mit den vorgegebenen Werten überein; D2 hat keine neuen pruefe_regeln-Hitrecords und null R8/R9-Treffer. Der Prüfer-Diff gegen 89c61ce enthält im Bestand ausschließlich die erlaubten geerbten Dateien r8_kreuzung.py, r8a_policy.py und test_r8a_policy_p3d26.py; p3d36 änderte keinen Prüfer, Test, relief_o18n.py, Overlay oder ../referenz/*.

[S] codex_jobs/tools/p3d36/results/ belegt insgesamt rund 428 KiB und bleibt deutlich unter 30 MB; es liegen keine LP/MPS-Dateien darin. Vor den Solves waren rund 33 GB frei. Die eigenen Probedateien und Solver-Exporte unter /tmp/p3d36 wurden nach Übernahme kompakter JSON-Belege entfernt. Die fünf bekannten roten Bestandstests wurden nicht ausgeführt oder verändert.

## 8. Schluss in drei Sätzen

[F] Der absolute rampe_11-Höhenpin bei 20,7 m war strenger als R3/R8/R8a und wurde im Modell geöffnet; die strengere p3d30-Nullquerzeile wurde nach Filterbeleg durch die offizielle 3%-Entsprechung ersetzt. [S] Der abschließende LP-Lauf mit Stufenzeilen an allen vier Rampenenden ist in Runde 1 infeasible, mit 0,004526635 m tatsächlicher Überschreitung im rampe_11-Startband; der ältere Float32-Diagnosekandidat verfehlte ebenfalls Zielwerte. [F] Es wurde kein Mesh gebaut, und das p3d36-Ziel ist nicht erreicht.
