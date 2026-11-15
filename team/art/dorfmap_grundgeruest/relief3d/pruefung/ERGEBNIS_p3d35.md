# Ergebnis p3d35

Stand 15.11.2026 · Worktree `/workspace/wt_dorfmap_p3d35` · Branch `art/dorfmap-p3d35` · Startbasis `origin/art/dorfmap-p3d34` @ `cc3693e` · Kosten 0 EUR.

Laufzeitnachweis: `/workspace/codex_jobs/log_p3d35.txt` (`gpt-6-luna`, reasoning effort `xhigh`). Marker: `[S]` gemessen · `[R]` Modell-/Diagnosebefund · `[A]` Annahme oder Grenze · `[F]` Entscheidung.

`[R]` Neue p3d35-Werkzeuge: `diagnose_lp_p3d35.py`, `run_lp_p3d35.py`, `diagnose_lp_iis_p3d35.py`, `probe_direct_transfer_p3d35.py`, `derive_event_cuts_p3d35.py` und `run_checker_loop_p3d35.py`, alle unter `codex_jobs/tools/p3d35/`. `neu/mesh.py` und dessen Standardvariante blieben unverändert.

## 1. Kreuzungsanker und Plattform

`[R]` `P3D35_POLICY=official` ist Standard; `P3D35_POLICY=p3d34` erhält den alten p3d34-Modellzustand zur Reproduktion. Die LP-Variable für die gemeinsame Plattformhöhe wurde freigegeben; die feste Höhenzeile am Anker `[152.5|28.5]` ist entfernt. Ebenenkernradius 2,0 m, Kreuzungslage und Auslaufgradient 1,5 % bleiben gleich. Als unveränderte Projekt-Hartziele modelliert p3d35 Stufe ≤0,116 m, Gitter ≤0,020 m, Quergefälle ≤3 %, Einzelquergefälle ≤20 % und Endpunktstufe ≤0,054 m.

`[R]` Prüfer-Diff gegen `89c61ce` (geerbter Stand; p3d35 selbst änderte keinen Prüfer): `M pruefung/r8_kreuzung.py`, `A pruefung/r8a_policy.py`, `A pruefung/test_r8a_policy_p3d26.py`. `pruefe_regeln.py`, `r9_form.py` und `relief_o18n.py` sind unverändert. Die literal implementierten Schwellen in `r8_kreuzung.py` sind Stufe 0,20 m, Gitter 0,15 m und Quergefälle 3 %; die oben genannten 0,116/0,020/0,054 m sind die engeren, im Auftrag festgehaltenen Projekt-Hartziele und wurden nicht gelockert. `pruefe_regeln.py` prüft R3 in 0,25-m-Abständen und 16-Sample-Sektionen: längs ≤0,08 m, quer ≤3,5 %, Wölbung ≤0,08 m. `r8a_policy.py` hält 0,10 m allgemein und 0,18 m ausschließlich für `rampe_2_anfang` am Punkt `[126.51|31.62]` (Koordinatentoleranz 1e-5); p3d35 änderte diese Definitionen nicht.

`[S]` Runde 0 wählte am Anker `[152.5|28.5]` die Höhe **3.952680478 m** gegenüber **4.054505123 m** aus p3d31 V3 Runde 3, also **-0.101824645 m**. Am ungerundeten R8-Prüfzentrum `[152.6292918621|28.3535909942]` änderte sich die Plattformhöhe von **4.057357106 m** auf **3.955532461 m**. Die offizielle Float32-R8-Kreuzungsgruppe zeigt Stufe **0.063 m**, Gitter **0.020 m** und Quergefälle **1.800 %**; der offizielle Quer-Prüfer meldet keinen Treffer. Der LP-Einzelquer-Grenzwert bleibt 20 %.

## 2. Rampenprofile und Übergänge

`[R]` rampe_2-Profilpunkte 0–50 m einschließlich Station 0 und 0,3 m sind Variablen; die Probe enthält 167 variable Werte von 0,0 bis 49,8 m. rampe_11 70–90 m enthält 34 variable Werte von 70,2 bis 90,0 m. Alle übrigen Profilwerte sind an p3d31 V3 fixiert. Die Profile außerhalb ihrer geöffneten Fenster sind für beide Rampen bitgleich zum p3d31-V3-Profil.

`[A]` Für rampe_11 werden die Stationsnamen des p3d34-IIS mit Faktor 2,4 abgebildet, weil dessen Zeile rampe_11 Station 83,4 m so benennt; die p3d33-rampe_2-Stationen folgen Faktor 1,2. Das ist eine durch die alten IIS-Namen motivierte Zuordnung, keine unabhängig vermessene Weglänge.

`[S]` Die inneren Übergänge erfüllen C0 und haben links/rechts gleiche Steigung. rampe_2 am Übergang 49,8 m: Steigung −0,208387980 m/m auf beiden Seiten, Differenz < 5·10⁻¹⁵ m/m, zweite Differenz 0; offizieller R3-Wölbwert 0,014924859 m. rampe_11 bei 70,2 m: −0,099868404 m/m auf beiden Seiten, Differenz < 3·10⁻¹⁵ m/m, zweite Differenz 0; berechneter R3-Wölbwert 0,080000120 m. rampe_11 bei 90,0 m: −0,142006709 m/m auf beiden Seiten, Differenz < 4·10⁻¹⁵ m/m, zweite Differenz 0; R3-Wölbwert 0,079999934 m.

`[A]` Das Roh-LP-JSON speichert die rampe_11-Übergänge in seinem separaten `p3d35_profile_transitions`-Feld fälschlich als 35,1/45,0 m; das widerspricht seinen exportierten `station_m`-Werten 70,2/90,0 m. Die Probe berechnet die Übergangsangaben aus den exportierten Stationsarrays; die Tabellen und Werte oben verwenden diese nachgerechneten Stationen. Die Metadaten-Erzeugung im Modellcode wurde für künftige Läufe auf dieselbe Stationsarray-Quelle umgestellt; das archivierte Solver-JSON wurde nicht umgeschrieben.

### rampe_2, Station 0–55 m

| Station (m) | Höhe alt (m) | Höhe neu (m) | Steigung (m/m) | 2. Differenz (m/m²) |
| --- | --- | --- | --- | --- |
| 0.0 | 12.469810 | 12.469810 | -0.072180 | -0.000472 |
| 0.3 | 12.448156 | 12.448155 | -0.072322 | -0.009542 |
| 0.6 | 12.426416 | 12.426416 | -0.077906 | -0.018480 |
| 0.9 | 12.401412 | 12.401412 | -0.083410 | -0.018679 |
| 1.2 | 12.376370 | 12.376370 | -0.089113 | -0.018907 |
| 1.5 | 12.347944 | 12.347944 | -0.094754 | -0.018875 |
| 1.8 | 12.319518 | 12.319518 | -0.100438 | -0.018978 |
| 2.1 | 12.287682 | 12.287682 | -0.106141 | 0.078930 |
| 2.4 | 12.255834 | 12.255834 | -0.053080 | 0.176901 |
| 2.7 | 12.255834 | 12.255834 | -0.000000 | 0.056039 |
| 3.0 | 12.255834 | 12.255834 | -0.019457 | -0.074231 |
| 3.3 | 12.244160 | 12.244160 | -0.044538 | -0.094346 |
| 3.6 | 12.229111 | 12.229111 | -0.076064 | -0.097583 |
| 3.9 | 12.198521 | 12.198521 | -0.103088 | -0.056488 |
| 4.2 | 12.167258 | 12.167258 | -0.109957 | -0.021012 |
| 4.5 | 12.132547 | 12.132547 | -0.115695 | -0.020691 |
| 4.8 | 12.097841 | 12.097841 | -0.122372 | -0.022592 |
| 5.1 | 12.059124 | 12.059124 | -0.129250 | -0.023331 |
| 5.4 | 12.020291 | 12.020291 | -0.136371 | -0.023903 |
| 5.7 | 11.977301 | 11.977301 | -0.143592 | -0.024758 |
| 6.0 | 11.934136 | 11.934136 | -0.151225 | -0.024861 |
| 6.3 | 11.886566 | 11.886566 | -0.158509 | -0.024035 |
| 6.6 | 11.839030 | 11.839030 | -0.165646 | -0.025471 |
| 6.9 | 11.787178 | 11.787178 | -0.173791 | -0.026309 |
| 7.2 | 11.734756 | 11.734756 | -0.181432 | -0.025800 |
| 7.5 | 11.678319 | 11.678319 | -0.189271 | -0.024197 |
| 7.8 | 11.621193 | 11.621193 | -0.195950 | -0.025943 |
| 8.1 | 11.560750 | 11.560750 | -0.204837 | -0.030229 |
| 8.4 | 11.498291 | 11.498291 | -0.214087 | -0.025982 |
| 8.7 | 11.432297 | 11.432297 | -0.220426 | -0.022795 |
| 9.0 | 11.366035 | 11.366035 | -0.227764 | -0.025977 |
| 9.3 | 11.295639 | 11.295639 | -0.236012 | -0.026708 |
| 9.6 | 11.224427 | 11.224427 | -0.243789 | -0.025962 |
| 9.9 | 11.149366 | 11.149366 | -0.251590 | -0.025918 |
| 10.2 | 11.073474 | 11.073474 | -0.259339 | -0.025953 |
| 10.5 | 10.991237 | 10.993762 | -0.267161 | -0.025009 |
| 10.8 | 10.907963 | 10.913177 | -0.274345 | -0.025955 |
| 11.1 | 10.820650 | 10.829155 | -0.282735 | -0.027532 |
| 11.4 | 10.732512 | 10.743536 | -0.290864 | -0.025971 |
| 11.7 | 10.639165 | 10.654637 | -0.298317 | -0.025194 |
| 12.0 | 10.543779 | 10.564546 | -0.305981 | -0.026002 |
| 12.3 | 10.442234 | 10.471048 | -0.313918 | -0.026099 |
| 12.6 | 10.339087 | 10.376195 | -0.321640 | -0.026039 |
| 12.9 | 10.242306 | 10.278064 | -0.329542 | -0.028340 |
| 13.2 | 10.146814 | 10.178470 | -0.338644 | -0.026050 |
| 13.5 | 10.041532 | 10.074878 | -0.345171 | -0.020740 |
| 13.8 | 9.933838 | 9.971367 | -0.351088 | -0.025972 |
| 14.1 | 9.822822 | 9.864226 | -0.360755 | -0.030182 |
| 14.4 | 9.710628 | 9.754914 | -0.369197 | -0.025681 |
| 14.7 | 9.595002 | 9.642707 | -0.376163 | -0.023841 |
| 15.0 | 9.478292 | 9.529216 | -0.383501 | -0.025015 |
| 15.3 | 9.357597 | 9.412607 | -0.391173 | -0.023804 |
| 15.6 | 9.235619 | 9.294513 | -0.397784 | -0.023626 |
| 15.9 | 9.105719 | 9.173937 | -0.405348 | -0.025054 |
| 16.2 | 8.973414 | 9.051304 | -0.412816 | -0.021509 |
| 16.5 | 8.839964 | 8.926247 | -0.418254 | -0.017319 |
| 16.8 | 8.706290 | 8.800351 | -0.423208 | -0.066391 |
| 17.1 | 8.571890 | 8.672322 | -0.458088 | -0.119165 |
| 17.4 | 8.437761 | 8.525498 | -0.494707 | -0.069853 |
| 17.7 | 8.297050 | 8.375498 | -0.500000 | -0.008822 |
| 18.0 | 8.153484 | 8.225498 | -0.500000 | -0.000000 |
| 18.3 | 8.005455 | 8.075498 | -0.500000 | -0.000000 |
| 18.6 | 7.855455 | 7.925498 | -0.500000 | 0.000000 |
| 18.9 | 7.707975 | 7.775498 | -0.500000 | 0.000000 |
| 19.2 | 7.560441 | 7.625498 | -0.500000 | 0.001715 |
| 19.5 | 7.419894 | 7.475498 | -0.498971 | 0.028716 |
| 19.8 | 7.281330 | 7.326116 | -0.482770 | 0.062440 |
| 20.1 | 7.151310 | 7.185836 | -0.461507 | 0.058811 |
| 20.4 | 7.024110 | 7.049211 | -0.447483 | 0.044365 |
| 20.7 | 6.899746 | 6.917346 | -0.434888 | 0.035658 |
| 21.0 | 6.778757 | 6.788278 | -0.426089 | 0.023635 |
| 21.3 | 6.659922 | 6.661693 | -0.420707 | 0.019389 |
| 21.6 | 6.540496 | 6.535854 | -0.414456 | 0.020644 |
| 21.9 | 6.421535 | 6.413020 | -0.408321 | 0.013372 |
| 22.2 | 6.301968 | 6.290862 | -0.406432 | 0.003362 |
| 22.5 | 6.182906 | 6.169160 | -0.406304 | 0.003618 |
| 22.8 | 6.063112 | 6.047079 | -0.404262 | 0.010767 |
| 23.1 | 5.945836 | 5.926603 | -0.399844 | 0.020312 |
| 23.4 | 5.831002 | 5.807173 | -0.392074 | 0.034730 |
| 23.7 | 5.726366 | 5.691359 | -0.379006 | 0.015457 |
| 24.0 | 5.633417 | 5.579770 | -0.382800 | -0.034625 |
| 24.3 | 5.541686 | 5.461678 | -0.399781 | -0.035283 |
| 24.6 | 5.445037 | 5.339901 | -0.403970 | -0.002235 |
| 24.9 | 5.347548 | 5.219296 | -0.401122 | 0.013110 |
| 25.2 | 5.247491 | 5.099228 | -0.396104 | 0.028286 |
| 25.5 | 5.149916 | 4.981634 | -0.384151 | -0.051561 |
| 25.8 | 5.059055 | 4.868738 | -0.427040 | -0.174547 |
| 26.1 | 4.947978 | 4.725410 | -0.488879 | -0.024854 |
| 26.4 | 4.813953 | 4.575410 | -0.441952 | 0.355049 |
| 26.7 | 4.716424 | 4.460239 | -0.275849 | 0.435678 |
| 27.0 | 4.658087 | 4.409901 | -0.180546 | 0.131729 |
| 27.3 | 4.588834 | 4.351911 | -0.196812 | -0.032708 |
| 27.6 | 4.516572 | 4.291813 | -0.200170 | -0.004357 |
| 27.9 | 4.444276 | 4.231809 | -0.199426 | 0.001806 |
| 28.2 | 4.371976 | 4.172158 | -0.199087 | -0.000262 |
| 28.5 | 4.294335 | 4.112357 | -0.199584 | 0.021472 |
| 28.8 | 4.223831 | 4.052408 | -0.186203 | 0.139576 |
| 29.1 | 4.159449 | 4.000635 | -0.115838 | 0.219723 |
| 29.4 | 4.111556 | 3.982905 | -0.054369 | 0.151698 |
| 29.7 | 4.076493 | 3.968014 | -0.024819 | 0.090616 |
| 30.0 | 4.076493 | 3.968014 | 0.000000 | 0.041365 |
| 30.3 | 4.076493 | 3.968014 | 0.000000 | 0.000000 |
| 30.6 | 4.076493 | 3.968014 | 0.000000 | 0.000000 |
| 30.9 | 4.076493 | 3.968014 | 0.000000 | 0.000000 |
| 31.2 | 4.076493 | 3.968014 | 0.000000 | 0.000000 |
| 31.5 | 4.071804 | 3.968014 | 0.000000 | 0.000000 |
| 31.8 | 4.071804 | 3.968014 | 0.000000 | 0.029594 |
| 32.1 | 4.071661 | 3.968014 | 0.017756 | 0.033072 |
| 32.4 | 4.069486 | 3.978667 | 0.019843 | -0.026116 |
| 32.7 | 4.065246 | 3.979919 | 0.002087 | -0.033072 |
| 33.0 | 4.065243 | 3.979919 | 0.000000 | -0.003478 |
| 33.3 | 4.063035 | 3.979919 | 0.000000 | 0.000000 |
| 33.6 | 4.045427 | 3.979919 | 0.000000 | 0.000000 |
| 33.9 | 4.026791 | 3.979919 | 0.000000 | 0.000000 |
| 34.2 | 4.016937 | 3.979919 | 0.000000 | -0.074477 |
| 34.5 | 4.016937 | 3.979919 | -0.044686 | -0.205584 |
| 34.8 | 3.998436 | 3.953108 | -0.123351 | -0.175185 |
| 35.1 | 3.972291 | 3.905909 | -0.149797 | -0.028590 |
| 35.4 | 3.963651 | 3.863229 | -0.140504 | 0.028242 |
| 35.7 | 3.961552 | 3.821606 | -0.132852 | 0.025020 |
| 36.0 | 3.961552 | 3.783518 | -0.125492 | -0.135895 |
| 36.3 | 3.961552 | 3.746311 | -0.214389 | -0.381116 |
| 36.6 | 3.936517 | 3.654885 | -0.354162 | -0.139513 |
| 36.9 | 3.933205 | 3.533814 | -0.298096 | 0.348397 |
| 37.2 | 3.933205 | 3.476027 | -0.145124 | 0.338407 |
| 37.5 | 3.933205 | 3.446740 | -0.095052 | 0.089835 |
| 37.8 | 3.933205 | 3.418995 | -0.091223 | 0.083450 |
| 38.1 | 3.933205 | 3.392006 | -0.044982 | 0.152038 |
| 38.4 | 3.928109 | 3.392006 | 0.000000 | 0.074971 |
| 38.7 | 3.918000 | 3.392006 | 0.000000 | -0.065525 |
| 39.0 | 3.884541 | 3.392006 | -0.039315 | -0.134887 |
| 39.3 | 3.845652 | 3.368417 | -0.080932 | -0.082856 |
| 39.6 | 3.812169 | 3.343447 | -0.089029 | 0.041454 |
| 39.9 | 3.789403 | 3.315000 | -0.056060 | 0.117593 |
| 40.2 | 3.774670 | 3.309811 | -0.018473 | 0.077059 |
| 40.5 | 3.763668 | 3.303916 | -0.009825 | 0.025623 |
| 40.8 | 3.746477 | 3.303916 | -0.003099 | -0.003881 |
| 41.1 | 3.724547 | 3.302057 | -0.012153 | -0.027416 |
| 41.4 | 3.696350 | 3.296624 | -0.019548 | -0.057392 |
| 41.7 | 3.664757 | 3.290328 | -0.046589 | -0.087657 |
| 42.0 | 3.628655 | 3.268671 | -0.072143 | -0.049245 |
| 42.3 | 3.590352 | 3.247042 | -0.076136 | -0.014324 |
| 42.6 | 3.549642 | 3.222989 | -0.080737 | -0.025168 |
| 42.9 | 3.507030 | 3.198599 | -0.091236 | -0.023478 |
| 43.2 | 3.461655 | 3.168247 | -0.094824 | -0.001964 |
| 43.5 | 3.414695 | 3.141705 | -0.092415 | -0.019239 |
| 43.8 | 3.365068 | 3.112798 | -0.106368 | -0.049063 |
| 44.1 | 3.313495 | 3.077884 | -0.121853 | -0.039531 |
| 44.4 | 3.258865 | 3.039687 | -0.130086 | -0.025492 |
| 44.7 | 3.202180 | 2.999833 | -0.137148 | -0.020479 |
| 45.0 | 3.138729 | 2.957398 | -0.142374 | -0.020472 |
| 45.3 | 3.070417 | 2.914409 | -0.149432 | -0.023753 |
| 45.6 | 3.000029 | 2.867739 | -0.156625 | -0.023928 |
| 45.9 | 2.928065 | 2.820433 | -0.163788 | -0.023088 |
| 46.2 | 2.856129 | 2.769466 | -0.170478 | 0.026824 |
| 46.5 | 2.783953 | 2.718147 | -0.147694 | 0.131983 |
| 46.8 | 2.713181 | 2.680850 | -0.091288 | 0.031786 |
| 47.1 | 2.647029 | 2.663374 | -0.128622 | -0.298228 |
| 47.4 | 2.575444 | 2.603677 | -0.270225 | -0.317836 |
| 47.7 | 2.501948 | 2.501239 | -0.319324 | -0.005368 |
| 48.0 | 2.428499 | 2.412083 | -0.273446 | 0.118272 |
| 48.3 | 2.355263 | 2.337171 | -0.248360 | 0.046970 |
| 48.6 | 2.282194 | 2.263066 | -0.245263 | 0.008079 |
| 48.9 | 2.209220 | 2.190013 | -0.243513 | 0.001661 |
| 49.2 | 2.136293 | 2.116959 | -0.244267 | 0.028015 |
| 49.5 | 2.062919 | 2.043453 | -0.226704 | 0.059798 |
| 49.8 | 1.990185 | 1.980936 | -0.208388 | 0.005978 |
| 50.1 | 1.918420 | 1.918420 | -0.223117 | -0.048014 |
| 50.4 | 1.847066 | 1.847066 | -0.237196 | -0.020830 |
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

### rampe_11, Station 65–95 m

| Station (m) | Höhe alt (m) | Höhe neu (m) | Steigung (m/m) | 2. Differenz (m/m²) |
| --- | --- | --- | --- | --- |
| 65.4 | 5.399203 | 5.399203 | -0.131607 | -0.008501 |
| 66.0 | 5.318817 | 5.318817 | -0.139001 | -0.014681 |
| 66.6 | 5.232402 | 5.232402 | -0.149224 | -0.013984 |
| 67.2 | 5.139748 | 5.139748 | -0.155782 | -0.004589 |
| 67.8 | 5.045464 | 5.045464 | -0.154731 | -0.024364 |
| 68.4 | 4.954071 | 4.954071 | -0.185019 | -0.065939 |
| 69.0 | 4.823442 | 4.823442 | -0.233858 | 0.008404 |
| 69.6 | 4.673442 | 4.673442 | -0.174934 | 0.111658 |
| 70.2 | 4.523442 | 4.613521 | -0.099868 | 0.088211 |
| 70.8 | 4.404452 | 4.553600 | -0.069081 | 0.035785 |
| 71.4 | 4.274776 | 4.530623 | -0.056926 | -0.005085 |
| 72.0 | 4.191081 | 4.485288 | -0.075183 | -0.014178 |
| 72.6 | 4.137136 | 4.440404 | -0.073939 | 0.002793 |
| 73.2 | 4.113860 | 4.396561 | -0.071831 | 0.003942 |
| 73.8 | 4.100060 | 4.354206 | -0.069209 | 0.014958 |
| 74.4 | 4.100060 | 4.313510 | -0.053882 | 0.019114 |
| 75.0 | 4.100060 | 4.289548 | -0.046272 | -0.013263 |
| 75.6 | 4.100060 | 4.257984 | -0.069797 | -0.048964 |
| 76.2 | 4.100060 | 4.205791 | -0.105028 | -0.052176 |
| 76.8 | 4.100060 | 4.131950 | -0.132409 | -0.011273 |
| 77.4 | 4.100060 | 4.046901 | -0.118556 | 0.070606 |
| 78.0 | 4.100060 | 3.989682 | -0.047682 | 0.098797 |
| 78.6 | 4.100060 | 3.989682 | 0.000000 | 0.039735 |
| 79.2 | 4.100060 | 3.989682 | 0.000000 | 0.000000 |
| 79.8 | 4.100060 | 3.989682 | 0.000000 | -0.000817 |
| 80.4 | 4.092111 | 3.989682 | -0.000980 | -0.003710 |
| 81.0 | 4.083911 | 3.988507 | -0.004452 | -0.004970 |
| 81.6 | 4.080261 | 3.984340 | -0.006944 | -0.002077 |
| 82.2 | 4.075349 | 3.980174 | -0.006944 | -0.000000 |
| 82.8 | 4.072651 | 3.976007 | -0.006944 | 0.000006 |
| 83.4 | 4.075321 | 3.971841 | -0.006937 | 0.000019 |
| 84.0 | 4.067432 | 3.967683 | -0.006921 | 0.000021 |
| 84.6 | 4.054987 | 3.963536 | -0.006912 | 0.000004 |
| 85.2 | 4.050919 | 3.959389 | -0.006916 | -0.000017 |
| 85.8 | 4.050919 | 3.955237 | -0.006932 | -0.000023 |
| 86.4 | 4.049386 | 3.951070 | -0.006944 | -0.006377 |
| 87.0 | 4.045132 | 3.946904 | -0.014585 | -0.033811 |
| 87.6 | 4.031384 | 3.933568 | -0.047517 | -0.063969 |
| 88.2 | 3.957879 | 3.889883 | -0.091348 | -0.065458 |
| 88.8 | 3.858984 | 3.823951 | -0.126067 | -0.042315 |
| 89.4 | 3.760090 | 3.738603 | -0.142126 | -0.013284 |
| 90.0 | 3.661332 | 3.653399 | -0.142007 | -0.002722 |
| 90.6 | 3.568195 | 3.568195 | -0.145393 | -0.010200 |
| 91.2 | 3.478928 | 3.478928 | -0.154247 | -0.021944 |
| 91.8 | 3.383099 | 3.383099 | -0.171725 | -0.040083 |
| 92.4 | 3.272857 | 3.272857 | -0.202347 | -0.053128 |
| 93.0 | 3.140282 | 3.140282 | -0.235479 | -0.038333 |
| 93.6 | 2.990282 | 2.990282 | -0.248347 | 0.028221 |
| 94.2 | 2.842267 | 2.842267 | -0.201614 | 0.069814 |
| 94.8 | 2.748346 | 2.748346 | -0.164570 | 0.058827 |

## 3. Machbarkeit und IIS

`[S]` Der harte LP der Runde 0 ist optimal und kontinuierlich: 20.411 Variablen, 76.223 Zeilen, 0 Integer-Variablen, Zielfunktionswert **0.062933867 m**. Die verwendete Konstruktion ist der p3d33/p3d34-LP mit offiziellen R3/R8/R8a-Grenzen, D1-Lokalität, Plattformkern und lokalen Event-Schnitten; R9w-Höhen werden nicht gleichheitsfixiert. Die Klippenform-Zeilen sind außerhalb der ausgeschlossenen Straßen-/Kreuzungs-/Auslaufstencils hart. Die JSON-Laufmetadaten enthalten 34 Zeilenfamilien-Namen einschließlich Event-, Stütz- und Regelzeilen; das belegt keine 1:1-Abbildung auf die angeforderten 22 übergeordneten Familien.

`[R]` Der Priority-Flood-Lauf nutzte 1-mm-Epsilon und fand keine neue Untergrenze; 20 tiefe Spill-Zellen blieben in geschützten Weg-/Klippen-/Randmasken. Die Konstruktionsmetadaten verzeichnen 6.938 verworfene Straßenrichtungs-Kandidaten, aber zugleich `modeled_drainage_candidate_count=0` und eine Sink-Policy ohne Nachfolger-/Erreichbarkeitsbedingungen. Damit ist „kein Querabfluss über den Weg“ im LP nicht durch aktive Flusszeilen erzwungen; diese geforderte Eigenschaft ist hier nicht nachgewiesen.

`[S]` Nach 64 aus Runde 0 abgeleiteten lokalen Schnitten (54 R3-Abschnitt, 3 R5-Loch, 7 R9w) ist das harte LP Runde 1 infeasible: 20.411 Variablen, 76.246 Zeilen, 0 Integer-Variablen. Es gibt deshalb keine Float32-Probe für Runde 1.

`[R]` Angefordert wurde HiGHS 1.15.1, `iis_strategy=6`. Die IIS-Reduktion lief drei Stunden CPU-gebunden und schrieb weder IIS-JSON noch `.iis.lp`; sie wurde nach diesem Diagnosebudget beendet. Das ist **kein gelesener IIS**. Der All-Familien-Filter (Status optimal, aber elastisch) ist kein Ersatz dafür: positive Slacks waren `variable_bounds_extra_m=0,590540708 m` an rampe_11 Station 20,7 m, Karte `[152.2981|14.9911]` (interne Begrenzung 7,923292889 m; Filterlösung 8,513833597 m), sowie `r3_long_residual_m=0,009098929 m`. Die rampe_11-Stelle liegt außerhalb des freigegebenen Fensters 70–90 m; ohne IIS und mit der festen Außenbereichsvorgabe wurde sie nicht geöffnet.

| Iteration | IIS-Zeilen | Sperre / Modellierung | Offizielle Definition und Urteil | Ersatz / Ergebnis |
|---|---:|---|---|---|
| p3d34-Basis, vor p3d35 | 9 Zeilen / 10 Spalten; keine rampe_2-Zeile. | rampe_11 St. 83,4 m Profiluntergrenze 4,075321254 m, Achsstütze ±0,02 m und festgehaltener Kreuzungsanker ≤4,054505123 m; Ebenenkern-Stützzeilen. Der Abstand von ca. 0,000816 m war Teil des IIS. Ein separater All-Familien-Filter fand außerdem rampe_2 St. 0,3 m mit `variable_bounds_extra_m=0,001655529 m`. | Die p3d33-Fixierung der gemeinsamen Kreuzungshöhe war strenger als das Projekt-Hartziel. Die p3d34-Rampen-Pins wurden innerhalb der ausdrücklich genannten Fenster durch Variablen mit den R3/R8/R8a-Zeilen ersetzt. | In p3d35 R00 löste der offizielle Hart-LP; ausgewählte Ankerhöhe −0,101824645 m. |
| p3d35-R01 nach 64 Event-Schnitten | IIS versucht, aber keine IIS-Zeilenliste/kein Artefakt nach 3 h. | Hartes LP infeasible. Elastischer All-Familien-Filter zeigt `variable_bounds` an rampe_11 St. 20,7 m plus R3-Längsresiduum; R3-Zeile und Pinursache sind nicht per IIS zugeordnet. | **Ungeklärt**, kein Beleg, dass diese Außenfenster-Pin strenger als die offizielle Regel ist. Die Stelle liegt außerhalb des geöffneten rampe_11-Fensters. | Keine weitere Sperre gelockert, keine zweite Iteration, keine Schwelle/Prüfung geändert. Stopp. |

`[S]` JSON-Belege liegen unter `codex_jobs/tools/p3d35/results/`: Runde-0-LP, Konstruktion, Machbarkeitsmetadaten und Probe; die unveränderten Checker-Ausgaben `p3d35_r00_pruefe_regeln.json`, `p3d35_r00_r8_kreuzung.json`, `p3d35_r00_r9_form.json`, `p3d35_r00_loch_gate.json`; abgeleitete Event-/Priority-Flood-Schnitte und Übergangs-Metadaten-Audit; Runde-1-LP, Konstruktion, All-Familien-Filter, Event-Schnitte und Checker-Loop-Zusammenfassung; sowie `p3d35_r01_official_hard_iis_check_construction.json` und `p3d35_r01_iis_timeout.json`. Es gibt kein abgeschlossenes p3d35-IIS-JSON/`.iis.lp`. Der erste elastische Diagnoseversuch ist unverändert und ausdrücklich als kein IIS in `results/_alt/` erhalten.

## 4. Float32-Probe, Regeln und Kacheln

`[S]` Runde 0 ist die einzige abgeschlossene LP-Kandidatenrunde; der Float32-Probe-Lauf wurde zweimal auf genau demselben gespeicherten Relief ausgeführt, beim zweiten Lauf wurde die R8a-Hartzielauswertung präzisiert. Runde 1 hatte keinen primal zulässigen Punkt und wurde nicht probiert. Die R8-/R9-Zahlen werden getrennt von `pruefe_regeln.py` gezählt. Vergleich für die +5-Grenze ist der p3d17-Replay (600 Regel-Treffer, R8 46, R9 344); der ältere Ausgang 9d3f8fc bleibt zusätzlich dokumentiert: `pruefe_regeln.py` 596, R8 48 (Stufe 9, Gitter 10, Quer 5, R8a 24), R9 334 (R8b 25, Sägezahn 34, R9w 275).

| Regel | p3d17 vorher | p3d35 R00 nachher | Δ | D1 vorher → nachher | G1 vorher → nachher | D2 vorher → nachher |
| --- | --- | --- | --- | --- | --- | --- |
| R1_blind | 24 | 24 | 0 | 2 → 2 | 1 → 1 | 0 → 0 |
| R2_getrennt | 15 | 15 | 0 | 1 → 1 | 0 → 0 | 1 → 1 |
| R3_laengs_m | 35 | 42 | 7 | 6 → 13 | 1 → 1 | 0 → 0 |
| R3_woelb_m | 31 | 32 | 1 | 19 → 20 | 0 → 0 | 0 → 0 |
| R3_quer_pct | 29 | 33 | 4 | 17 → 21 | 0 → 0 | 0 → 0 |
| R4_rand | 1 | 0 | -1 | 1 → 0 | 0 → 0 | 0 → 0 |
| R5_loch | 25 | 25 | 0 | 8 → 8 | 0 → 0 | 0 → 0 |
| R6_wasser_schnee | 4 | 4 | 0 | 0 → 0 | 3 → 3 | 0 → 0 |
| G2_spitze_oben | 3 | 3 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G3_spitze_unten | 4 | 3 | -1 | 1 → 0 | 0 → 0 | 0 → 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G5_beule_klippe | 69 | 68 | -1 | 2 → 1 | 0 → 0 | 0 → 0 |
| G6_facette | 219 | 217 | -2 | 3 → 1 | 3 → 3 | 0 → 0 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G11_objekt_schwebt_sinkt | 4 | 4 | 0 | 2 → 2 | 2 → 2 | 0 → 0 |
| T1_fleckrand | 94 | 94 | 0 | 0 → 0 | 3 → 3 | 7 → 7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| G7b_wandkontur_feld | 25 | 25 | 0 | 1 → 1 | 0 → 0 | 0 → 0 |
| R8_stufe | 9 | 9 | 0 | 2 → 2 | 0 → 0 | 0 → 0 |
| R8_gitter | 10 | 9 | -1 | 2 → 1 | 0 → 0 | 0 → 0 |
| R8_quer | 4 | 4 | 0 | 0 → 0 | 0 → 0 | 0 → 0 |
| R8a_wegende | 23 | 22 | -1 | 3 → 2 | 0 → 0 | 0 → 0 |
| R8b_delle | 23 | 23 | 0 | 1 → 1 | 0 → 0 | 0 → 0 |
| R9_saegezahn | 34 | 34 | 0 | 1 → 1 | 1 → 1 | 0 → 0 |
| R9w_wellen | 287 | 287 | 0 | 27 → 27 | 12 → 12 | 0 → 0 |

`[S]` p3d35 Runde 0 hatte `pruefe_regeln.py` **607** Treffer, R8 **44** (Stufe 9, Gitter 9, Quer 4, R8a 22) und R9 **344** (R8b 23, Sägezahn 34, R9w 287). Gegenüber dem p3d17-Replay steigt R3 längs um 7 (über +5); R5-Löcher bleiben 25 gesamt und 8 in D1; R9w bleibt 287. Damit verfehlt Runde 0 die unveränderten harten Ziele R3 D1 6/7/7, R5-Loch 22/5, R9w 280 sowie +5 je Regel.

`[S]` D1/G1/D2: D1 hat R3 längs/quer/wölb 13/21/20, R5-Loch 8, G5 1, G6 1, R8b 1, R8a 2, R9w 27, R4-Schlucht 0 und R5-Spitze 0. G1-Treffer bleiben gegenüber p3d17 unverändert (R1 1, R3 längs 1, R6 3, G6 3, G11 2, T1 3; R9 Sägezahn 1/R9w 12). D2 bleibt exakt unverändert (R2 1, T1 7); D2-Regel-Hitrecords entsprechen p3d17 und R8/R9 D2 sind 0.

`[S]` Alle 138 Trefferorte der drei unveränderten Prüfer, gefiltert auf D1/G1/D2 (die unveränderten G1/D2-Treffer sind mit enthalten; Gesamtzahlen stehen in der Tabelle je Regel):

| Kachel | Prüfer | Regel | Ort x|z | Wert | Weg/Art und Zusatz |
| --- | --- | --- | --- | ---: | --- |
| D1 | R8 | R8_gitter | 148.5|2.5 | 0.35 | rampe_11_anfang |
| D1 | R8 | R8_stufe | 126.5|31.6 | 0.21 | rampe_2_anfang |
| D1 | R8 | R8_stufe | 148.5|2.5 | 0.67 | rampe_11_anfang |
| D1 | R8 | R8a_wegende | 148.5|2.5 | 0.1 | rampe_11_anfang; limit=0.1 |
| D1 | R8 | R8a_wegende | 156.5|37.5 | 0.1 | rampe_11_ende; limit=0.1 |
| D1 | R9 | R8b_delle | 146.0|9.5 | 0.49 | Wegabstand=0.7 |
| D1 | R9 | R9_saegezahn | 148.5|5.0 | 115 |  |
| D1 | R9 | R9w_wellen | 128.5|30.0 | 0.21 |  |
| D1 | R9 | R9w_wellen | 132.5|29.5 | 0.18 |  |
| D1 | R9 | R9w_wellen | 134.3|32.6 | 0.88 |  |
| D1 | R9 | R9w_wellen | 135.8|40.1 | 0.53 |  |
| D1 | R9 | R9w_wellen | 136.8|20.9 | 0.55 |  |
| D1 | R9 | R9w_wellen | 139.5|27.9 | 0.42 |  |
| D1 | R9 | R9w_wellen | 141.2|0.2 | 0.17 |  |
| D1 | R9 | R9w_wellen | 142.8|13.3 | 0.27 |  |
| D1 | R9 | R9w_wellen | 143.5|0.5 | 0.24 |  |
| D1 | R9 | R9w_wellen | 145.2|30.6 | 0.35 |  |
| D1 | R9 | R9w_wellen | 147.8|36.2 | 0.16 |  |
| D1 | R9 | R9w_wellen | 149.2|7.8 | 0.19 |  |
| D1 | R9 | R9w_wellen | 149.3|27.2 | 0.43 |  |
| D1 | R9 | R9w_wellen | 152.5|5.6 | 0.28 |  |
| D1 | R9 | R9w_wellen | 152.9|2.2 | 0.13 |  |
| D1 | R9 | R9w_wellen | 153.5|0.2 | 0.27 |  |
| D1 | R9 | R9w_wellen | 154.6|39.3 | 0.15 |  |
| D1 | R9 | R9w_wellen | 155.0|35.0 | 0.4 |  |
| D1 | R9 | R9w_wellen | 155.0|40.8 | 0.15 |  |
| D1 | R9 | R9w_wellen | 156.7|27.3 | 0.25 |  |
| D1 | R9 | R9w_wellen | 159.5|35.8 | 0.22 |  |
| D1 | R9 | R9w_wellen | 159.9|9.5 | 0.4 |  |
| D1 | R9 | R9w_wellen | 162.6|29.5 | 0.42 |  |
| D1 | R9 | R9w_wellen | 163.5|31.0 | 0.22 |  |
| D1 | R9 | R9w_wellen | 164.0|24.2 | 0.21 |  |
| D1 | R9 | R9w_wellen | 164.4|22.3 | 0.57 |  |
| D1 | R9 | R9w_wellen | 167.8|13.8 | 0.23 |  |
| D1 | pruefe_regeln | G11_objekt_schwebt_sinkt | 136.2|39.8 | 0.74 | baeume |
| D1 | pruefe_regeln | G11_objekt_schwebt_sinkt | 138.2|37.8 | 1.7 | baeume |
| D1 | pruefe_regeln | G5_beule_klippe | 149.5|34.5 | 1.27 |  |
| D1 | pruefe_regeln | G6_facette | 157.7|29.1 | 8 |  |
| D1 | pruefe_regeln | G7b_wandkontur_feld | 147.0|21.0 | 0.649 |  |
| D1 | pruefe_regeln | R1_blind | 126.5|31.6 | 0 | rampe_2; anfang |
| D1 | pruefe_regeln | R1_blind | 156.5|37.5 | 0 | rampe_11; ende |
| D1 | pruefe_regeln | R2_getrennt | 150.9|23.6 | 116 |  |
| D1 | pruefe_regeln | R3_laengs_m | 134.5|30.7 | 0.082 | rampe_2 |
| D1 | pruefe_regeln | R3_laengs_m | 138.4|30.4 | 0.084 | rampe_2 |
| D1 | pruefe_regeln | R3_laengs_m | 146.4|29.5 | 0.25 | rampe_2 |
| D1 | pruefe_regeln | R3_laengs_m | 146.6|6.0 | 0.104 | rampe_11 |
| D1 | pruefe_regeln | R3_laengs_m | 148.5|2.5 | 0.1 | rampe_11 |
| D1 | pruefe_regeln | R3_laengs_m | 150.3|28.7 | 0.216 | rampe_2 |
| D1 | pruefe_regeln | R3_laengs_m | 151.8|29.6 | 0.252 | rampe_11 |
| D1 | pruefe_regeln | R3_laengs_m | 153.7|26.1 | 0.17 | rampe_11 |
| D1 | pruefe_regeln | R3_laengs_m | 153.7|35.4 | 0.153 | rampe_11 |
| D1 | pruefe_regeln | R3_laengs_m | 154.2|28.1 | 0.149 | rampe_2 |
| D1 | pruefe_regeln | R3_laengs_m | 155.6|22.6 | 0.182 | rampe_11 |
| D1 | pruefe_regeln | R3_laengs_m | 157.5|19.1 | 0.107 | rampe_11 |
| D1 | pruefe_regeln | R3_laengs_m | 162.1|26.9 | 0.123 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 130.5|31.1 | 3.5 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 134.5|30.7 | 4.6 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 138.4|30.4 | 9.3 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 142.4|30.2 | 15.3 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 144.8|9.5 | 14.5 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 146.4|29.5 | 17.7 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 146.6|6.0 | 10.2 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 148.1|11.9 | 3.7 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 148.5|2.5 | 5.8 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 150.3|28.7 | 16.2 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 150.4|33.1 | 4.5 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 151.3|14.3 | 3.5 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 151.8|29.6 | 20.0 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 153.7|26.1 | 11.2 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 154.2|28.1 | 20.0 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 154.5|16.6 | 7.5 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 155.6|22.6 | 20.0 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 157.5|19.1 | 4.2 | rampe_11 |
| D1 | pruefe_regeln | R3_quer_pct | 158.2|27.3 | 19.8 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 162.1|26.9 | 10.4 | rampe_2 |
| D1 | pruefe_regeln | R3_quer_pct | 166.1|26.7 | 3.6 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 126.5|31.6 | 0.08 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 130.5|31.1 | 0.082 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 134.5|30.7 | 0.122 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 138.4|30.4 | 0.199 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 142.4|30.2 | 0.246 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 144.8|9.5 | 0.202 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 146.4|29.5 | 0.177 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 146.6|6.0 | 0.628 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 148.1|11.9 | 0.086 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 148.5|2.5 | 0.733 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 150.3|28.7 | 0.105 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 150.4|33.1 | 1.027 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 151.3|14.3 | 0.083 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 151.8|29.6 | 0.509 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 154.2|28.1 | 0.346 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 154.5|16.6 | 0.133 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 155.6|22.6 | 0.295 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 157.5|19.1 | 0.266 | rampe_11 |
| D1 | pruefe_regeln | R3_woelb_m | 158.2|27.3 | 0.356 | rampe_2 |
| D1 | pruefe_regeln | R3_woelb_m | 162.1|26.9 | 0.231 | rampe_2 |
| D1 | pruefe_regeln | R5_loch | 143.5|10.0 | 2.15 |  |
| D1 | pruefe_regeln | R5_loch | 143.5|8.0 | 1.7 |  |
| D1 | pruefe_regeln | R5_loch | 144.0|7.0 | 1.35 |  |
| D1 | pruefe_regeln | R5_loch | 154.0|14.0 | 1.14 |  |
| D1 | pruefe_regeln | R5_loch | 155.0|15.5 | 1.41 |  |
| D1 | pruefe_regeln | R5_loch | 157.5|16.5 | 2.86 |  |
| D1 | pruefe_regeln | R5_loch | 157.5|20.0 | 1.45 |  |
| D1 | pruefe_regeln | R5_loch | 159.0|18.5 | 2.17 |  |
| G1 | R9 | R9_saegezahn | 257.0|20.5 | 37 |  |
| G1 | R9 | R9w_wellen | 256.8|35.8 | 0.42 |  |
| G1 | R9 | R9w_wellen | 263.0|34.0 | 0.45 |  |
| G1 | R9 | R9w_wellen | 264.7|21.5 | 0.63 |  |
| G1 | R9 | R9w_wellen | 271.4|10.1 | 0.29 |  |
| G1 | R9 | R9w_wellen | 272.2|14.0 | 0.12 |  |
| G1 | R9 | R9w_wellen | 274.1|19.4 | 0.27 |  |
| G1 | R9 | R9w_wellen | 275.1|5.9 | 0.26 |  |
| G1 | R9 | R9w_wellen | 276.0|29.9 | 0.67 |  |
| G1 | R9 | R9w_wellen | 281.9|34.9 | 0.42 |  |
| G1 | R9 | R9w_wellen | 285.4|25.8 | 0.18 |  |
| G1 | R9 | R9w_wellen | 289.0|29.8 | 0.4 |  |
| G1 | R9 | R9w_wellen | 292.3|29.9 | 0.33 |  |
| G1 | pruefe_regeln | G11_objekt_schwebt_sinkt | 253.8|20.2 | 0.99 | baeume |
| G1 | pruefe_regeln | G11_objekt_schwebt_sinkt | 256.9|19.9 | 0.96 | baeume |
| G1 | pruefe_regeln | G6_facette | 271.7|11.1 | 8 |  |
| G1 | pruefe_regeln | G6_facette | 277.5|16.8 | 6 |  |
| G1 | pruefe_regeln | G6_facette | 279.3|32.1 | 20 |  |
| G1 | pruefe_regeln | R1_blind | 273.4|21.2 | 0 | rampe_1; anfang |
| G1 | pruefe_regeln | R3_laengs_m | 273.4|21.2 | 0.093 | rampe_1 |
| G1 | pruefe_regeln | R6_wasser_schnee | 272.5|9.8 | 22 |  |
| G1 | pruefe_regeln | R6_wasser_schnee | 273.1|7.3 | 7 |  |
| G1 | pruefe_regeln | R6_wasser_schnee | 275.0|6.1 | 6 |  |
| G1 | pruefe_regeln | T1_fleckrand | 260.4|41.6 | 19 |  |
| G1 | pruefe_regeln | T1_fleckrand | 285.0|42.9 | 11 |  |
| G1 | pruefe_regeln | T1_fleckrand | 288.1|42.1 | 10 |  |
| D2 | pruefe_regeln | R2_getrennt | 166.9|81.5 | 1227 |  |
| D2 | pruefe_regeln | T1_fleckrand | 155.2|59.1 | 8 |  |
| D2 | pruefe_regeln | T1_fleckrand | 155.6|50.2 | 23 |  |
| D2 | pruefe_regeln | T1_fleckrand | 156.4|47.7 | 11 |  |
| D2 | pruefe_regeln | T1_fleckrand | 158.5|74.7 | 11 |  |
| D2 | pruefe_regeln | T1_fleckrand | 161.1|56.9 | 26 |  |
| D2 | pruefe_regeln | T1_fleckrand | 161.4|60.8 | 22 |  |
| D2 | pruefe_regeln | T1_fleckrand | 162.2|74.5 | 14 |  |

`[S]` Alle 17 Checks der Runde-0-Probe:

| Harter Check | Ergebnis |
| --- | --- |
| D1_R4_schlucht_eq_0 | erfüllt |
| D2_no_new_pruefe_regeln_hits | erfüllt |
| G3_D1_le_1 | erfüllt |
| G5_D1_le_2 | erfüllt |
| G5_total_le_69 | erfüllt |
| G6_D1_le_3 | erfüllt |
| R3_D1_le_6_7_7 | VERFEHLT |
| R5_loch_D1_le_5 | VERFEHLT |
| R5_loch_total_le_22 | VERFEHLT |
| R5_spitze_D1_eq_0 | erfüllt |
| R8_D2_zero | erfüllt |
| R8a_D1_no_unpermitted_hits | VERFEHLT |
| R8b_D1_le_1 | erfüllt |
| R9_D2_zero | erfüllt |
| R9w_total_le_280 | VERFEHLT |
| per_rule_increase_vs_p3d17_le_5 | VERFEHLT |
| rampe_2_start_R8a_exception_not_exceeded | erfüllt |


`[S]` Die offizielle R8a-Probe meldet zusätzlich zwei nicht ausgenommene D1-Treffer gegen 0,10 m: `rampe_11_anfang` bei `[148.5|2.5]` und `rampe_11_ende` bei `[156.5|37.5]` (beide in der Ausgabe auf 0,1 m gerundet). Die erlaubte rampe_2-Startausnahme wurde nicht ausgelöst; diese R8a-Treffer sind ein eigener Zielverstoß.


`[S]` Vergleich p3d31 Runde 3: G5 68/1 statt 71/4 (gesamt/D1); R5-Loch 25/8 statt 24/7; G6 D1 1 statt 2; R5-Spitze D1 0 statt 0; R8b D1 1 statt 1; R3 D1 13/21/20 statt 6/7/7; R9w 287 statt 283; Kreuzungsstufe/Gitter 0,063/0,020 m statt 0,073/0,019 m. Der Vergleich ist eine Messung, kein Zielwechsel.

## 5. Lokalität und Hashes

`[S]` Die 1.415 Float32-Rasterpunkte außerhalb D1 sind bitgleich zur p3d17-Referenz: SHA-256 beider Ausschnitte `996c1ce6f4c1b48f5a6e7cd74a270a87b541e1fc75f0b56884cf423a2e02daf7`. G1-Höhenhash `38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb`; D2-Höhenhash `749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6`.

`[S]` Geschützte Eingaben: `zellen_relief.csv` `99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa`; `vektor.json` `aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e`; `felder.json` `e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435`. Die vorgegebenen Hashes bleiben erhalten. Prüfer, Tests, Overlay, Referenzdaten, Zellquellwerte, G1 und D2 wurden durch p3d35 nicht geändert.

## 6. Mesh-Gate und Grenzen

`[F]` Kein Mesh gebaut: die Runde-0-Zielwerte sind verfehlt und Runde 1 infeasible. Daher wurden `python3 gen_relief.py`, `python3 baue_html.py`, kompletter Mesh-Gate-Lauf, `delta.py`, pytest, t42u, Klippenmessung, LOD1 und Bilder nicht ausgeführt. Es gibt keine Messung für LOD1 <1,3 Mio. Dreiecke oder t42u-Summe; der neue Mesh-t42u-Wert kann folglich nicht als 0 bestätigt werden. Der letzte gebaute Stand bleibt p3d18 @ `ee46fe5`. Die fünf bekannten roten Bestandstests (R8a gesamt, R9-Sägezahn D1, D1-Wandkante, F1/C1-Wegende, Schattenbild) wurden nicht verändert und nicht ausgeführt. Bildpflicht entfiel mangels Mesh.

`[A]` Offene Punkte: genaue Zeilen-/Spalten-IIS für Runde 1 (HiGHS Strategy 6 nach drei Stunden ohne Artefakt); Ursache des R3-Längsresiduums; ob eine Regelkonforme Reparatur innerhalb der freigegebenen Fenster möglich ist. Keine offizielle Schwelle wurde geändert; keine Mesh-Aussage wird aus der Float32-Probe abgeleitet.

## Schluss in drei Sätzen

`[F]` Die offizielle Plattform- und Profilfreigabe machte das p3d35-LP in Runde 0 lösbar, senkte die Kreuzungsankerhöhe um 0,101825 m und hielt G1, D2 sowie den Außenbereich bitgleich. Die Float32-Probe verfehlte R3, R5-Loch, R8a, R9w und die +5-Grenze; Runde 1 war nach 64 lokalen Schnitten infeasible, die dreistündige IIS-Reduktion blieb ohne Artefakt, und der Querabfluss über den Weg ist nicht erzwungen. Deshalb wurde kein Mesh gebaut und p3d35 erreicht das Ziel nicht.
