# Ergebnis p3d31

Stand 14.11.2026 · Worktree /workspace/wt_dorfmap_p3d31 · Branch art/dorfmap-p3d31 · Basis origin/art/dorfmap-p3d30 @ 1c2c4e3 · Kosten 0 EUR.

Marker: [S] gemessen · [R] Diagnose/Modellbefund · [A] Annahme oder Grenze · [F] Entscheidung.

## Entscheidung

[F] Keine der vier V1-Float32-Proben hielt alle harten Ziele. Die beste Probe war Runde 3 mit Score 11; Runde 4 verschlechterte sich auf Score 18. Gemäß Abbruchregel wurde kein Mesh gebaut, und die konstruktive V2-LP/Priority-Flood-Variante blieb offen.

## 0. Ursache der p3d30-Infeasibility

[S] Verwendet wurde highspy 1.15.1 aus /tmp/p3d18_highspy. Das originale p3d30-Hartmodell war mit 95.347 Variablen und 173.134 Zeilen infeasible (HiGHS-Status 8); der Standardaufruf getIis() lieferte für das MIP keine IIS-Zeilen. Da HiGHS die IIS-Suche als LP-Funktion beschreibt, wurde die Integrität relaxiert und iis_strategy=6 (Elasticity-Filter plus Reduktion) gesetzt; das ergab ein IIS mit 7 Zeilen und 6 Spalten. Siehe [HiGHS-IIS-Dokumentation](https://github.com/ERGO-Code/HiGHS/blob/master/docs/src/guide/advanced.md) und codex_jobs/tools/p3d31/results/p3d31_step0_lp_iis.json.

[S] Alle 7 IIS-Zeilen gehören zur Abflussgruppe: eine p3d30_drainage_successor_choice- und sechs p3d30_drainage_selected_edge_height-Zeilen am Knoten 150,5|1,0. Die sechs möglichen Nachfolger sind 150,5|0,5; 151|0,5; 151|1,0; 150|1,5; 150,5|1,5; 151|1,5. Die Referenzhöhen-Differenzen Nachbar minus Knoten reichen von 0,005548 bis 0,172322 m; alle sechs Kanten haben eps=0, Transferdeckung ist 0, und der Punkt liegt im Kern außerhalb des Rings.

[R] Das konkrete IIS weist auf eine feste lokale Senke im p3d17-Relief: die interne Pflicht, von jeder aktiven Zelle einen tieferen Nachfolger zu wählen, kollidiert dort mit den fixierten Familien-/Lokalitätsbedingungen. Es war weder eine über viele Kanten summierte 1-mm-Epsilonstufe noch die Ringgrenze. Der separate p3d30-All-open-Relaxationslauf benötigte maximal 0,017688 m Schlupf an 150,0|0,5 → 149,5|1,0; über 121 Kanten summierte er 0,125 m, ist aber nicht die Ursache des IIS. Zusätzliche Lockerung fixer Wegzellen, des Rings oder der Randauslässe war nach diesem IIS nicht erforderlich.

## 1. Modelländerungen gegenüber p3d30

[R] Neue Werkzeuge und Belege liegen unter codex_jobs/tools/p3d31/. V1 (Standard P3D31_VARIANT=1) entfernt Nachfolgerwahl, Flussbilanz und gerichtete Abflusskanten vollständig: im ersten Modell gab es 0 Drainage-Kandidaten, 0 Nachfolger-Binärvariablen und 0 Flussvariablen. Die bestehenden p3d29/p3d30-Lokalität, 22 Familien, Weghöhen, R4-Ereignisschnitte, Klippenform, R8-Grenzen und R3-Grenzen blieben Teil des Modells.

[R] Senken werden in V1 nicht durch eine künstliche Erreichbarkeitspflicht begrenzt. Stattdessen übersetzt die Checker-in-the-loop-Schleife nur tatsächlich vom Float32-Transfer und offiziellen Prüfern gemeldete G5-, R5-Loch-, G6-, R8b-, R5-Spitzen- und R9w-Ereignisse in frische Komponentenschnitte. Die fest gesetzten Budgets bleiben G5 gesamt ≤69 und D1 ≤2, R5_loch gesamt ≤22 und D1 ≤5, G6 D1 ≤3, R8b D1 ≤1; für R9w gilt gesamt ≤280. Es wurden keine Schwellen oder Checker geändert; R9w erhielt weder Höhen-Pins noch Gleichheitsfixierungen.

[S] Die D1-Rekonstruktion aus jeder final übertragenen Float32-Probe stimmte in allen vier Runden bei den gezählten Ereignisfamilien exakt mit dem offiziellen Checker überein: G5, R5_loch, G6, R8b und R9w, jeweils 0 Abweichung bei den D1-Komponentenzahlen; R9w stimmte zudem global überein. V1 enthält keine eigenen vollständigen offiziellen Komponentenindikatoren: die Modellrestriktionen sind Lazy-Cuts aus den geprüften Komponenten. Die Belegdateien sind die jeweiligen *_derived_summary.json und *_official_probe.json.

[A] V2 wurde nicht ausgeführt. Der kopierte p3d30-Soft-Abfluss-Code bildet nicht die angeforderte lokale LP-Konstruktion mit festem Kreuzungs-/Ramp2-Quergefälle und anschließendem Priority-Flood ab; er wurde nach Abschluss der vier erlaubten Float32-Runden gesperrt, damit er nicht fälschlich als V2 verwendet wird. Es gibt deshalb keinen V2-Machbarkeits- oder Prüfbeleg.

## 2. Machbarkeit und Solves

[S] Der V1-Hartstart ohne Ereignisschnitte war Optimal und primal zulässig: 19.975 Variablen, 75.451 Zeilen, Drainage-Modus off, 1 Thread. Auch die vier Checker-Runden lösten jeweils Optimal mit bewiesenem Optimum; die Modelle blieben MIPs aufgrund der bestehenden R3-/Familien-Binärvariablen, obwohl alle Drainage-Variablen entfernt waren.

| Runde | Status | Variablen | Zeilen | Schnitte davor | Zeitlimit je Solve |
|---:|---|---:|---:|---:|---:|
| Start | Optimal | 19.975 | 75.451 | 0 | 600 s |
| 1 | Optimal | 19975 | 75451 | 0 | 600 s |
| 2 | Optimal | 19978 | 75475 | 9 | 600 s |
| 3 | Optimal | 19995 | 75505 | 18 | 600 s |
| 4 | Optimal | 20007 | 75525 | 25 | 600 s |

[S] Jeder Solve lief seriell mit einem Thread. Kein Soft-Fallback wurde verwendet. Der LP-IIS-Gruppenfilter aus Schritt 0 war für p3d30 maßgeblich; p3d31-V1 war machbar, daher gab es dort keinen Infeasibility-Filter.

## 3. Float32-Prüferrunden

[S] Pro Runde wurde der unveränderte Float32-Direkttransfer ausgeführt und damit der offizielle Regelsatz einschließlich R8 und R9 geprüft. Regel-Gesamtsummen zeigen D1/G1/D2 in Klammern; R8 und R9 zeigen Gesamt und dieselbe Kachelfolge. Der Score addiert getrennte Gate-Abweichungen. Für R9w gilt der allgemeine p3d17-+5-Grenzwert 292 und zusätzlich das strengere harte Maximum 280; in diesen Runden wurde nur das harte Maximum verletzt.

| Runde | pruefe_regeln gesamt (D1/G1/D2) | G5 gesamt/D1 | R5_loch gesamt/D1 | G6 D1 | R8 gesamt (D1/G1/D2) | R9 gesamt (D1/G1/D2) | R9w gesamt | Score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 574 (37/13/8) | 67/0 | 25/8 | 2 | 42 (3/0/0) | 343 (28/13/0) | 286 | 12.0 |
| 2 | 578 (41/13/8) | 72/5 | 24/7 | 2 | 42 (3/0/0) | 341 (26/13/0) | 284 | 14.0 |
| 3 | 576 (39/13/8) | 71/4 | 24/7 | 2 | 42 (3/0/0) | 340 (25/13/0) | 283 | 11.0 |
| 4 | 576 (39/13/8) | 73/6 | 25/8 | 0 | 42 (3/0/0) | 340 (25/13/0) | 284 | 18.0 |

Belege: [R1](../../../../../codex_jobs/tools/p3d31/results/p3d31_V3_round01_official_probe.json) · [R2](../../../../../codex_jobs/tools/p3d31/results/p3d31_V3_round02_official_probe.json) · [R3](../../../../../codex_jobs/tools/p3d31/results/p3d31_V3_round03_official_probe.json) · [R4](../../../../../codex_jobs/tools/p3d31/results/p3d31_V3_round04_official_probe.json).

[S] Runde 3 war die beste gültige Modellprobe, aber kein zielgültiger Punkt: G5 71 gesamt / 4 D1 überschritt 69 / 2; R5_loch 24 / 7 überschritt 22 / 5; R9w 283 überschritt 280. Alle übrigen bewerteten harten Bedingungen bestanden. Runde 4 fiel auf G5 73 / 6, R5_loch 25 / 8 und R9w 284 zurück; der Checkerloop hielt nach dem vierten Lauf an.

### Modell- und Prüferabgleich

| Runde | G5 D1 rekonstruiert / geprüft | R5_loch D1 rekonstruiert / geprüft | G6 D1 rekonstruiert / geprüft | R8b D1 rekonstruiert / geprüft | R9w D1 rekonstruiert / geprüft; global |
|---:|---:|---:|---:|---:|---:|
| 1 | 0 / 0 (0) | 8 / 8 (0) | 2 / 2 (0) | 1 / 1 (0) | 26 / 26 (0); 286 / 286 (0) |
| 2 | 5 / 5 (0) | 7 / 7 (0) | 2 / 2 (0) | 1 / 1 (0) | 24 / 24 (0); 284 / 284 (0) |
| 3 | 4 / 4 (0) | 7 / 7 (0) | 2 / 2 (0) | 1 / 1 (0) | 23 / 23 (0); 283 / 283 (0) |
| 4 | 6 / 6 (0) | 8 / 8 (0) | 0 / 0 (0) | 0 / 0 (0) | 24 / 24 (0); 284 / 284 (0) |

### Regelzahlen: p3d17-Replay → beste p3d31-Probe (Runde 3)

[S] Grundlage für die +5-Schranke ist das p3d17-Replay im aktuellen Schema (600 Regeln insgesamt einschließlich G11). Der vom Auftrag genannte ältere Stand 9d3f8fc ist separat: 596 Regeln, R8 48 (Stufe 9, Gitter 10, Quer 5, Wegende 24), R9 334 (R8b 25, Sägezahn 34, R9w 275).

| pruefe_regeln | vorher | nachher | Δ | vorher D1 | vorher G1 | vorher D2 | nachher D1 | nachher G1 | nachher D2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| G11_objekt_schwebt_sinkt | 4 | 4 | +0 | 2 | 2 | 0 | 2 | 2 | 0 |
| G2_spitze_oben | 3 | 3 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| G2_spitze_oben_fein | 8 | 8 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| G3_spitze_unten | 4 | 3 | -1 | 1 | 0 | 0 | 0 | 0 | 0 |
| G3_spitze_unten_fein | 2 | 2 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| G5_beule_klippe | 69 | 71 | +2 | 2 | 0 | 0 | 4 | 0 | 0 |
| G6_facette | 219 | 218 | -1 | 3 | 3 | 0 | 2 | 3 | 0 |
| G7_wand_glatte_flaeche | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| G7b_wandkontur_feld | 25 | 25 | +0 | 1 | 0 | 0 | 1 | 0 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R1_blind | 24 | 24 | +0 | 2 | 1 | 0 | 2 | 1 | 0 |
| R2_getrennt | 15 | 15 | +0 | 1 | 0 | 1 | 1 | 0 | 1 |
| R3_laengs_m | 35 | 35 | +0 | 6 | 1 | 0 | 6 | 1 | 0 |
| R3_quer_pct | 29 | 19 | -10 | 17 | 0 | 0 | 7 | 0 | 0 |
| R3_woelb_m | 31 | 19 | -12 | 19 | 0 | 0 | 7 | 0 | 0 |
| R4_rand | 1 | 0 | -1 | 1 | 0 | 0 | 0 | 0 | 0 |
| R5_loch | 25 | 24 | -1 | 8 | 0 | 0 | 7 | 0 | 0 |
| R6_wasser_schnee | 4 | 4 | +0 | 0 | 3 | 0 | 0 | 3 | 0 |
| T1_fleckrand | 94 | 94 | +0 | 0 | 3 | 7 | 0 | 3 | 7 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |

| R8 | vorher | nachher | Δ | vorher D1 | vorher G1 | vorher D2 | nachher D1 | nachher G1 | nachher D2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R8_gitter | 10 | 9 | -1 | 2 | 0 | 0 | 1 | 0 | 0 |
| R8_quer | 4 | 4 | +0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R8_stufe | 9 | 9 | +0 | 2 | 0 | 0 | 2 | 0 | 0 |
| R8a_wegende | 23 | 20 | -3 | 3 | 0 | 0 | 0 | 0 | 0 |

| R9 | vorher | nachher | Δ | vorher D1 | vorher G1 | vorher D2 | nachher D1 | nachher G1 | nachher D2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R8b_delle | 23 | 23 | +0 | 1 | 0 | 0 | 1 | 0 | 0 |
| R9_saegezahn | 34 | 34 | +0 | 1 | 1 | 0 | 1 | 1 | 0 |
| R9w_wellen | 287 | 283 | -4 | 27 | 12 | 0 | 23 | 12 | 0 |

[S] Summen: pruefe_regeln 600 (D1/G1/D2 63/13/8) → 576 (39/13/8); R8 46 (7/0/0) → 42 (3/0/0); R9 344 (29/13/0) → 340 (25/13/0). In Runde 3 lag keine Regel über p3d17 +5; die drei oben genannten strengeren harten Budgets blieben trotzdem verletzt.

### Verbleibende Treffer in der besten Probe (Runde 3)

[S] G5 D1 (4): 154,5|30,5; 154,0|31,0; 149,5|34,5; 159,0|35,0.

[S] R5_loch D1 (7; jeweiliger Prüfpunkt und Tiefe): 143,5|8,0 (1,17 m); 143,5|10,0 (1,75 m); 154,0|14,0 (1,15 m); 155,0|15,5 (1,41 m); 157,5|16,5 (2,86 m); 159,0|18,5 (2,17 m); 157,5|20,0 (1,45 m).

[S] R9w D1 (23 Prüfmaxima; global sind es 283): 141,2|0,2; 143,5|0,5; 153,5|0,2; 152,8|2,2; 159,9|9,5; 152,6|5,5; 140,9|11,1; 167,8|13,8; 137,0|20,8; 164,4|22,4; 164,5|24,1; 149,3|27,0; 158,9|26,5; 139,8|28,1; 165,6|28,9; 156,6|29,2; 128,5|30,0; 135,7|32,4; 163,8|31,0; 155,4|35,2; 135,7|40,1; 154,6|39,3; 155,0|40,8.

[S] Andere harte D1-Ziele in Runde 3: R5_spitze 0, G6 2, R8b 1, G3 0, R4-Schlucht 0, R3 6/7/7. Die Kreuzung am offiziellen Punkt 152,6|28,4 hatte Stufe 0,073 m und Gitter 0,019 m; Querung bestand den offiziellen Prüfer, Wegende-Stufe und R8a hatten in D1 keinen Treffer, und der einzelne Querslope-Überhang war 0.

## 4. Grenzen, geschützte Dateien und Prüfstatus

[S] Laufzeitnachweis in /workspace/codex_jobs/log_p3d31.txt: gpt-6-luna, reasoning effort xhigh. Selbstberechnete SHA-256-Präfixe und Float32-Ausgabehashes: zellen_relief.csv 99d30e55 (voll: 99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa); vektor.json aac6afff (voll: aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e); felder.json e4e2ec8f (voll: e4e2ec8f5f4b7b7bb825f8fdda6c0400b5525e9c8c31153f7d9b10d4185e3435); G1 38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb; D2 749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6. G1/D2-Probehashes blieben in allen vier Runden konstant; D2 hatte gegenüber dem p3d17-Replay keine neuen pruefe_regeln-Treffer und null R8/R9-Treffer.

[S] Diff der Prüfer-/Testquellcode-Dateien gegen 89c61ce: r8_kreuzung.py enthält die bereits freigegebene Änderung; r8a_policy.py und test_r8a_policy_p3d26.py sind die historischen Hinzufügungen. pruefe_regeln.py, r9_form.py und relief_o18n.py haben keinen Diff; p3d31 änderte keine Prüfer-/Testquelldatei. p3d31 hat keine Prüfer, Schwellen, Ausnahmeregeln, Tests, relief_o18n.py, Zellquellen, Overlay, Referenzen, G1 oder D2 geändert.

[F] Der Meshbau (gen_relief.py, baue_html.py), die Mesh-Gates, LOD1, t42u, Klippenmessung und Bildprüfung wurden nicht ausgeführt, weil Runde 3/4 die harten Ziele verfehlten. Die fünf bekannten roten Bestandstests blieben unangetastet und wurden nicht ausgeführt. Es gibt daher keine p3d31-Mesh-Zahlen oder Bilder zu behaupten.

## 5. Selbstprüfung der Anforderungen 0–8

- [x] 0: p3d30-Ursache mit MIP-IIS-Aufruf, LP-IIS-Version, Strategie, Gruppen und Ort dokumentiert.
- [x] 1: V1 nutzt unveränderte harte Familien-/Lokalitätsbedingungen und entfernt die interne Abflusspflicht.
- [x] 2: V1-Machbarkeit, Variablen/Zeilen und alle vier Solve-Status dokumentiert; V2 nicht gerechnet.
- [!] 3: V1 wurde mit offiziellen komponentenbasierten Lazy-Cuts geprüft; konstruktive V2-LP/Priority-Flood-Implementierung und Probe fehlen.
- [x] 4: V1 zuerst hart gerechnet; keine Soft-Lockerung; vier Runden als Obergrenze eingehalten.
- [x] 5: vier serielle offizielle Float32-Prüferrunden mit frischen Schnitten; D1-Rekonstruktionen stimmen bei G5/R5/G6/R8b/R9w mit Prüferzählern überein.
- [x] 6: harte Ziele wurden nicht gelockert; Nichterfüllung mit Orten dokumentiert.
- [x] 7: kein Meshbau, weil keine Probe alle Ziele hielt; Mesh-Gates/Bilder folgerichtig nicht behauptet.
- [x] 8: nach vier Runden gestoppt und Resttreffer dokumentiert.

## 6. Schluss in drei Sätzen

Die LP-IIS-Analyse zeigte, dass p3d30 an einer lokalen p3d17-Senke wegen der internen Pflicht zur Abfluss-Erreichbarkeit infeasible war. V1 entfernte diese Pflicht, fand aber in vier offiziellen Float32-Runden keinen Punkt, der G5, R5_loch und R9w zugleich innerhalb der harten Budgets hielt; die beste Probe verfehlte diese Grenzwerte um 2, 2 und 3 Treffer. Daher wurde kein Mesh gebaut, und die konstruktive V2-LP/Priority-Flood-Variante bleibt der offene nächste Schritt.
