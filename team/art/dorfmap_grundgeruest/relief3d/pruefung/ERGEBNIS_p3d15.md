# Ergebnis p3d15

**Stand:** 09.11.2026 · **Branch:** art/dorfmap-p3d15 · **Basis:** origin/art/dorfmap-p3d14 @ 5e61682

**Ergebnis: Ziel nicht erreicht.** Die Achsprofile halten im finalen Neu-Mesh ±0,02 m und die Kreuzungsebene bleibt innerhalb 0,0191 m bei 3 % Neigung. Eine unabhängige Minimierung über ein feineres Raster ergibt mit diesen Stützen trotzdem mindestens 0,156708 m Sprung statt höchstens 0,116 m. Die gebaute Oberfläche hat 0,844 m. Die p3d6/p3d8/p3d14-Delta-Gates steigen; D1-R3 und der Wegendpunkt verfehlen ihre Ziele. Diese Fassung ist kein Nachweis einer lieferbaren Zielerreichung.

## Änderung

- In neu/mesh.py kamen Kreuzungsvarianten 18 und 19 dazu. Variante 18 verwendet ein gemeinsames Thin-Plate-Feld mit harten Achs- und Ebenenstützen; sie verfehlte bei 32 von 359 D1-Achsproben ±0,02 m, maximal um 0,08066 m.
- Variante 19 ist Standard über RELIEF_KREUZUNG_VAR=19. Sie ergänzt eine gemeinsame Thin-Plate-Fläche durch ein sparse LP auf dem auszugebenden Raster: 359 Achsproben innerhalb ±0,015 m, 45 Meshstützen im Ebenenkern innerhalb ±0,019 m und 980 exklusive Rampenbandstützen mit dokumentiertem weichem Slack. Die Rampe bleibt über RELIEF_WEGEND_VAR=1.
- Die monotone MILP-Bedingung erzwingt bei quellseitig fallenden Rampenstationen ein nicht steigendes Soll. Wegführung, neu/vektor.json, Zellquellwerte und Overlay wurden nicht geändert. Prüfer, Tests und Schwellenwerte blieben unverändert.
- Ein Endpunktversuch mit Wegendvariante 2 wurde verworfen: Er verschlechterte die D1-Endstufe von rund 0,22 m auf rund 0,24 m und änderte den G1-Hash. Die Standardvariante blieb 1.
- Die Mess- und MILP-Werkzeuge sowie Rastermessungen liegen unter ../../../../../codex_jobs/tools/p3d15_milp/.

## Schritt 1: Transferursache vor p3d15

Die p3d14-Produktionsfläche (Variante 17, vor dem neuen Transfer) wurde auf 0,25 Map-Einheiten abgetastet: 441 Punkte im Fenster 149–154 | 29–34. 0,25 Map-Einheiten entsprechen bei CELL_M=1,2 einem Abstand von 0,30 m.

| Punkt | Profilziel (m) | Profilabdeckung | Ebenenziel (m) | Ebenengewicht | Hintergrundterm (m) | Bandterm (m) | Ebenenterm (m) | Meshhöhe (m) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 152,25|31,75 | 3,269000 | 0,999920 | 3,947141 | 0,059260 | 0,000401 | 3,063812 | 0,234436 | 3,298649 |
| 152,25|32,00 | 3,082242 | 0,999840 | 3,938529 | 0 | 0,000803 | 3,081751 | 0 | 3,082554 |

Zwischen den beiden Punkten beträgt die Meshänderung −0,216095 m. Die Komponentenänderungen sind Hintergrund +0,000401 m, Band +0,017940 m und Ebene −0,234436 m. Der ausblendende Ebenenanteil erzeugt damit fast den gesamten Sprung; das Bandprofil selbst ändert sich nur um rund 0,018 m. Die Komponenten rekonstruieren die Meshhöhe mit höchstens 8,9e−16 m Abweichung. Zahlen und Raster: [Transfer JSON](../../../../../codex_jobs/tools/p3d15_milp/transfer_raster_p3d15.json), [0,25-Raster CSV](../../../../../codex_jobs/tools/p3d15_milp/transfer_raster_p3d15.csv).

## Schritt 2: MILP und monotone Rampe

Das p3d14-Soll von rampe_11 stieg bei fallender Quelle zwischen s=46,2 und 46,5 m von 3,079459 auf 3,157020 m, also um 0,077561 m. Die ergänzte Monotoniebedingung beseitigt den Anstieg. Für g=0,45 ist das neue Soll dort 2,942390 → 2,863169 m; für g=0,60 ist es 3,397901 → 3,247901 m. Die unterschiedlichen absoluten Höhen folgen den jeweiligen optimierten Profilen.

| Stand / g | MILP-Status | Ebene Hc (m) | Ebenengefälle | R3-Abschnitte gesamt / D1 | Engstes Paar / maximaler Paargrad | A/B rampe_11 s=45,6→48,9 m | Quellen-L1-Verschiebung |
|---|---|---:|---:|---:|---|---|---:|
| p3d14 / 0,60 | optimal | 4,061716 | 3,0 % | 5 / 3 | s=47,4→47,7: Δh=0,138085 m, d=0,230141 m, g=0,60 | Δh=1,023513 m bei d=2,538903 m | — |
| p3d14 / 0,45 | optimal | 4,061716 | 3,0 % | 5 / 3 | rampe_2 s=26,4 zu rampe_11 s=46,2: Δh=1,982237 m, d=4,404971 m, g=0,45 | Δh=1,015088 m bei d=2,538903 m | — |
| p3d15 / 0,60 | optimal, 380 Monotoniezeilen | 4,091716 | 3,0 % | 5 / 3 | rampe_11 s=47,4→47,7: Δh=0,138085 m, d=0,230141 m, g=0,60 | Δh=1,333531 m bei d=2,538903 m, g=0,5252 | 176,911152 m |
| p3d15 / 0,45 | optimal, 380 Monotoniezeilen | 4,068565 | 3,0 % | 6 / 4 | rampe_2 s=26,1 zu rampe_11 s=45,9: Δh=2,012286 m, d=4,471747 m, g=0,45 | Δh=0,730895 m bei d=2,538903 m, g=0,2879 | 206,618149 m |

A/B hat einen Bogen von 3,30 m, eine Sehne von 2,538903 m und ein Verhältnis Bogen/Sehne von 1,299774. Bei g=0,45 bleibt das Paar innerhalb der Grenze; bei g=0,60 ebenfalls. Das endgültige Neu-Mesh verwendet g=0,45. Vollständige Paarlisten und Profile stehen in den JSON-Dateien und der Profiltabelle.

## Schritt 3: Transfer und lokale Machbarkeitsgrenze

Im finalen D1-Profil liegt der maximale Achsfehler bei rampe_2 bei 0,015912 m und bei rampe_11 bei 0,015001 m; keine der 359 D1-Stationen überschreitet 0,02 m. Im Ebenenkern beträgt der maximale Mesh-Ebenenfehler 0,019000 m bei 3,0 % Gefälle.

Für die Kreuzung wurde anschließend ein LP auf einem unabhängigen 0,25-Map-Einheiten-Raster gerechnet. Dieses Raster hat mehr Freiheitsgrade als das ausgelieferte 0,5-Map-Einheiten-Mesh. Es minimiert den größten Nachbarsprung über die 1.114 R8-Prüferpaare und hält die 68 Achsstützen sowie 177 Ebenenkernstützen jeweils auf ±0,02 m. Es verwendet das g=0,45-Profil mit vier MILP-R3-Abschnitten in D1.

| Minimierungsbefund | Wert |
|---|---:|
| Minimal erreichbarer größter Nachbarsprung | 0,156707928 m |
| Abstand der Punkte | 0,30 m |
| daraus folgende lokale Neigung | 52,236 % |
| R8-Ziel bei gleichem Abstand | 0,116 m = 38,667 % |
| Überschreitung des Zielsprungs | 0,040708 m |
| Engstes Paar | (154,00|25,00), h=5,063937 m → (154,25|25,00), h=5,220645 m |
| nächste rampe_11-Stützen | s=37,2 m, Abstand 0,3285 m → s=36,9 m, Abstand 0,0295 m |

Die Optimierung ist optimal; das ist eine Machbarkeitsuntergrenze bei den genannten Achs- und Ebenenstützen, kein gemessener Meshwert. Selbst dieses feinere, freier verformbare Raster liegt über 0,116 m. Die volle 2D-R3-Bedingung ist kein LP-Ziel; das verwendete g=0,45-Profil hat aber vier D1-MILP-Abschnitte und liegt damit innerhalb der geforderten sechs. Unter den verlangten lokalen Stützen ist bereits die Stufengrenze allein nicht erfüllbar. Deshalb wurden nach diesem Nachweis keine weiteren Transfervarianten gebaut.

Sensitivität, nicht als Produkt gebaut: Wird der Ebenenkernradius von 2,25 auf 2,00 m verkleinert, sinkt die LP-Untergrenze auf 0,113468 m. Eine Achstoleranz von 0,12 m ergibt 0,113532 m; eine Ebenentoleranz von 0,15 m ergibt 0,113083 m. Diese Varianten lockern die Vorgaben und belegen keine vollständige R3-Erfüllung. Eine Wegverschiebung wurde nicht modelliert und die Wegführung nicht geändert.

## Schritt 4: D1-R8-Treffer im finalen Neu-Mesh

Die Tabelle nennt die Feinpunkte des jeweiligen Prüfertreffers. Höhen sind Meshhöhen. Residuum meint die Abweichung vom lokalen Rampenprofil, nicht die absolute Höhe. Wo der Prüfer eine Ausgleichsebene fitten lässt, gibt es kein einzelnes Höhenpaar für den Prozentwert.

| Regel / Ort | Prüferwert | Feinpunkte, Höhen oder Residuen | beteiligte Stationen | Transferterm |
|---|---:|---|---|---|
| R8_stufe, Kreuzung 152,5|28,5 | 0,844060 m | (154,50|28,25) 4,089830 m → (154,50|28,50) 4,933890 m | rampe_2 s=33,9→33,9 m; rampe_11 s=40,2→40,5 m | Variante 19: gemeinsames Thin-Plate-Feld plus Raster-LP. Die Bandstütze bei 154,50|28,50 hat Ziel 3,954575 m, Mesh 4,933890 m und maximalen weichen Slack 0,959315 m. |
| R8_gitter, Kreuzung 152,5|28,5 | 0,873 m | (153,50|28,50) 4,053720 m, Residuum −0,020804 m → (154,50|28,50) 4,933890 m, Residuum +0,856242 m | rampe_2 s=32,7→33,9 m; rampe_11 s=41,1→40,5 m | Derselbe gemeinsame Raster-LP-Kompromiss; die Bandstütze am zweiten Punkt ist der Slack-Maximalpunkt. |
| R8_quer, Kreuzung 152,5|28,5 | 3,433 % | kein einzelnes Höhenpaar; Fitgradient (−0,003976, −0,034095) je Map-Einheit | nahe Arme rampe_2 s≈31,5 m und rampe_11 s≈41,4–41,7 m | Neigung des durch Variante 19 übertragenen gemeinsamen Feldes. |
| R8_gitter, rampe_11 Anfang 148,5|2,5 | 0,276468 m | (149,50|3,00) 13,040636 m / Residuum +0,146721 m → (149,50|4,00) 12,706048 m / Residuum −0,129747 m | s=0,0→0,9 m | Gemeinsames Feld im Startband; dort wirkt zusätzlich der lokale Endauslauf mit RELIEF_WEGEND_VAR=1. |
| R8_gitter, rampe_11 Ende 156,5|37,5 | 0,246987 m | (157,00|36,00) 0,732458 m / Residuum +0,107697 m → (157,00|37,00) 0,418676 m / Residuum −0,139290 m | s=56,4→57,0 m | Bandtransfer hinter dem Ende; dieser Prüfstreifen liegt außerhalb des wirksamen Endauslaufstützbereichs von Variante 1. |
| R8a_wegende, rampe_2 Anfang | 0,117908 m | (126,50|34,00) 12,504212 m → (126,75|34,00) 12,386304 m | s=0,0 m | Lokaler Startauslauf Variante 1 plus gemeinsamer Profiltransfer. |
| R8a_wegende, rampe_11 Anfang | 0,176239 m | (150,00|3,00) 13,028206 m → (150,00|3,25) 12,851967 m | s=0,0 m | Lokaler Startauslauf Variante 1 plus gemeinsamer Profiltransfer. |
| R8a_wegende, rampe_11 Ende | 0,198631 m | (157,50|35,75) 0,855988 m → (157,75|35,75) 0,657357 m | s=56,7→57,0 m | Bandtransfer am Meshrand hinter dem Endpunkt, nicht durch die Variante-1-Endstützen abgedeckt. |

Damit ist das Kreuzungsziel 0,116 m deutlich verfehlt; das Gitterziel 0,02 m wird mit 0,873 m verfehlt. Die Kreuzung hat weiterhin einen R8_quer-Treffer. In D1 gibt es insgesamt acht R8/R8a-Treffer; gefordert waren null. G1 und D2 haben keine R8/R8a-Treffer. Der vollständige Diagnose-Datensatz steht in [r8_detail.json](bilder_p3d15/r8_detail.json).

Am Endpunkt 156,5|37,5 liegt der Endauslauf-Treffer bei 0,198631 m und damit schlechter als p3d11 mit 0,054 m und ohne R8a.

## Regel- und Kachelzahlen

Die historischen Standardprüfer werden weiterhin direkt auf relief_daten.json.gz ausgeführt. Der gelieferte Neu-Mesh-Adapter ersetzt für die Produktmessung nur D1/G1 und lässt D2 unverändert. Deshalb sind beide Messreihen getrennt aufgeführt.

Der direkt angegebene Ausgangswert 596 für pruefe_regeln ließ sich wie bereits in p3d8/p3d14 auf dem bereitgestellten Reliefstand nicht reproduzieren: Der direkte p3d15-Lauf ergibt 570; p3d14s legacy_standard ergibt ebenfalls 570. Die direkten R8/R9-Werte reproduzieren dagegen die angegebenen Ausgangswerte und bleiben gegenüber p3d14 unverändert.

| direkter Prüfer auf relief_daten.json.gz | Ausgangswert laut Aufgabe | p3d15 direkt | Vergleich zu p3d14 direkt |
|---|---:|---:|---:|
| pruefe_regeln gesamt | 596 | 570 | unverändert zu p3d14 |
| R8 gesamt | 48 | 48 | unverändert |
| R8_stufe / R8_gitter / R8_quer / R8a_wegende | 9 / 10 / 5 / 24 | 9 / 10 / 5 / 24 | unverändert |
| R9 gesamt | 334 | 334 | unverändert |
| R8b_delle / R9_saegezahn / R9w_wellen | 25 / 34 / 275 | 25 / 34 / 275 | unverändert |

Die folgende Tabelle vergleicht die vollständigen Neu-Mesh-Adapterregeln aus p3d14/nachher mit p3d15. Diese Paarung ist der detaillierte Vorher/Nachher-Zähler für die p3d15-Meshänderung.

| Regel | p3d14 | p3d15 | Δ |
|---|---:|---:|---:|
| R1_blind | 24 | 24 | 0 |
| R2_getrennt | 15 | 15 | 0 |
| R3_laengs_m | 40 | 43 | +3 |
| R3_quer_pct | 21 | 35 | +14 |
| R3_woelb_m | 19 | 26 | +7 |
| R5_loch | 17 | 17 | 0 |
| R6_wasser_schnee | 4 | 4 | 0 |
| G2_spitze_oben | 3 | 3 | 0 |
| G2_spitze_oben_fein | 8 | 8 | 0 |
| G3_spitze_unten | 3 | 3 | 0 |
| G3_spitze_unten_fein | 2 | 2 | 0 |
| G5_beule_klippe | 67 | 70 | +3 |
| G6_facette | 217 | 219 | +2 |
| G7_wand_glatte_flaeche | 1 | 1 | 0 |
| G8_fluss_nicht_bis_rand | 1 | 1 | 0 |
| G11_baum_an_wand | 2 | 2 | 0 |
| G7b_wandkontur_rauheit | 1 | 1 | 0 |
| G7b_wandkontur_kantenschaerfe | 1 | 1 | 0 |
| G7b_wandkontur_feld | 25 | 25 | 0 |
| T1_fleckrand | 94 | 94 | 0 |
| T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 | 0 |
| T3_streifen_ringe_bildpruefung_offen | 1 | 1 | 0 |
| T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 | 0 |
| T5_textur_vs_clay_bildpruefung_offen | 1 | 1 | 0 |
| **Summe pruefe_regeln, Adapter** | **569** | **598** | **+29** |

R3_quer_pct steigt um 14 und R3_woelb_m um 7, also mehr als die erlaubten +5. Das Hauptproblem liegt in D1; andere Regelzähler bleiben überwiegend gleich.

| Adapterregel | p3d14 | p3d15 | Δ |
|---|---:|---:|---:|
| R8_stufe | 8 | 8 | 0 |
| R8_gitter | 8 | 11 | +3 |
| R8_quer | 5 | 5 | 0 |
| R8a_wegende | 21 | 23 | +2 |
| **R8 gesamt** | **42** | **47** | **+5** |
| R8b_delle | 22 | 22 | 0 |
| R9_saegezahn | 34 | 34 | 0 |
| R9w_wellen | 284 | 287 | +3 |
| **R9 gesamt** | **340** | **343** | **+3** |

### Adapterzahlen je Kachel

| Prüfer / Kachel | p3d14 | p3d15 | Δ |
|---|---:|---:|---:|
| pruefe_regeln D1 | 34 | 63 | +29 |
| pruefe_regeln G1 | 11 | 11 | 0 |
| pruefe_regeln D2 | 8 | 8 | 0 |
| R8 D1 | 3 | 8 | +5 |
| R8 G1 | 0 | 0 | 0 |
| R8 D2 | 0 | 0 | 0 |
| R9 D1 | 24 | 28 | +4 |
| R9 G1 | 13 | 13 | 0 |
| R9 D2 | 0 | 0 | 0 |

D1-Regeln p3d15: R1=2, R2=1, R3 längs=14, quer=23, Wölbung=14, G5=3, G6=3, G11=2, G7b-Feld=1. D1-p3d14 hatte dafür 2, 1, 11, 9, 7, 0, 1, 2, 1. Die Zunahmen sind damit G5 +3, G6 +2, R3 längs +3, R3 quer +14 und R3 Wölbung +7.

G1-Regeln p3d15: R1=1, R3 längs=1, R6=3, G6=3, T1=3; unverändert zu p3d14. D2: R2=1 und T1=7; insgesamt 8 wie p3d14. Kein D2-Regel-Treffer kam neu hinzu. D2 hat in R8 und R9 weiterhin null Treffer.

D1 R9: R8b=0, ein Sägezahn-Treffer mit Zählerwert 41 und R9w=27. Gegenüber p3d8 ist R9w von 21 auf 27 gestiegen; der Sägezahnwert sank gegenüber p3d8 von 47 auf 41. G6 D1 stieg von 0 auf 3 und G11 D1 von 0 auf 2; diese Nebenregeln sind schlechter als p3d8. R8b blieb bei null.

## Deltas, Bilder und Prüfungen

| Vergleich | alle Delta-Anstiege | Gate-Anstiege | Bildproxy-Anstiege | Ergebnis |
|---|---:|---:|---:|---|
| VAR0 → p3d15 | 37 | 14 | 23 | nicht null |
| p3d6 → p3d15 | 29 | 12 | 17 | nicht null |
| p3d8 → p3d15 | 25 | 11 | 14 | nicht null |
| p3d14 → p3d15 | 22 | 9 | 13 | nicht null |

Die verlangte Null bei allen drei Deltas wird verfehlt. Details: [p3d6](bilder_p3d15/delta_p3d6_p3d15.md), [p3d8](bilder_p3d15/delta_p3d8_p3d15.md), [p3d14](bilder_p3d15/delta_p3d14_p3d15.md), [VAR0](bilder_p3d15/delta_VAR0_p3d15.md). Positive Gate-Änderungen für D1 sind jeweils im Delta-JSON nach Regel und Kachel aufgeführt.

Die geforderten Vorher-Aufnahmen aus p3d8 und p3d14 wurden angesehen. Danach wurden alle sechs p3d15-Bilder gerendert und angesehen: [D1-Kreuzung](bilder_p3d15/nachher/clay/D1_kreuzung.png), [Kreuzung im Streiflicht](bilder_p3d15/nachher/streiflicht/D1_kreuzung_streiflicht_rampe11.png), [D1-Wandfuß 140|35](bilder_p3d15/nachher/clay/D1_wandfuss_140_35.png), [D1-Wegende](bilder_p3d15/nachher/clay/D1_wegende.png), [G1-Wandfuß](bilder_p3d15/nachher/clay/G1_wandfuss.png), [D2-Draufsicht](bilder_p3d15/nachher/clay/D2_draufsicht.png). Der Clay-Facettenzähler der D1-Kreuzung sinkt von p3d14s 365 auf 279 und erfüllt damit ≤317. Im Streiflicht bleibt am Wandfuß/rampe_11 eine sichtbare Falte bzw. Kerbe; die geforderte weich wirkende Fläche ist nicht erreicht. Wandfußthemen außerhalb dieser Kreuzung wurden nicht bearbeitet.

| Bildproxy | p3d14 | p3d15 | Δ |
|---|---:|---:|---:|
| D1-Kreuzung Clay-Facetten | 365 | 279 | −86 |
| D2-Draufsicht Facetten | 13 | 13 | 0 |
| D2-Draufsicht Normalensprünge | 2.275 | 2.275 | 0 |
| D2-Draufsicht Sprunginseln | 9 | 9 | 0 |

Die sechs Zwischenrender, die vor dem finalen Raster-LP entstanden, wurden per git mv unter bilder_p3d15/_alt/initial_root_render/ aufbewahrt. Der Bildproxy kann trotz unverändertem D2-Mesh Unterschiede durch Viewer-/Rasterung abbilden; die unveränderte Meshhöhe wird durch den Meshhash und changed_vertices=0 belegt. D2-Bildwerte bleiben gegenüber p3d14 gleich.

| weitere Anforderung | p3d15 | Ziel | Status |
|---|---:|---:|---|
| D1-R3 längs | 14 Treffer, max. 0,403 m bei 153,7|26,1 | ≤6 | verfehlt |
| D1-R3 quer | 23 Treffer, max. 26,4 % bei 151,8|29,6 | ≤7 und kein Wert >20 % | verfehlt |
| D1-R3 Wölbung | 14 Treffer, max. 0,383 m bei 146,4|29,2 | ≤7 | verfehlt |
| D1-Kreuzungsstufe | 0,844 m | ≤0,116 m | verfehlt |
| D1-Kreuzungsgitter | 0,873 m | ≤0,020 m | verfehlt |
| Endpunkt 156,5|37,5 | 0,199 m R8a | p3d11: 0,054 m, kein R8a | verfehlt |
| G6 D1 / G11 D1 / R8b D1 / R9w D1 / Sägezahnwert D1, p3d8 → p3d15 | 0→3 / 0→2 / 0→0 / 21→27 / 47→41 | nicht schlechter als p3d8 | G6, G11 und R9w schlechter; R8b gleich; Sägezahnwert besser |
| D1-Kreuzung Clay-Facetten | 279 | ≤317 | erfüllt |
| D1-Höhenversatz zur Quelle | 3,023922 m | ≤4,0 m | erfüllt |
| Neu-LOD1 | 134.316 Dreiecke | <1.300.000 | erfüllt |
| t42u | 0 Abweichungen | 0 | erfüllt |
| Lochscan, Legacy und Neu mit xvfb | beide Exit 0; Neu: 9 Meshes, 88.728 Dreiecke, offen_innen=0, Punkte=0 | kein offenes Innenloch | erfüllt |

## Unveränderte Eingaben und Hashes

| Artefakt | p3d15-Wert | Prüfung |
|---|---|---|
| D1-Mesh | 0448b249a4d68547f34300bf5546f808ff7883877679cfda7a6c5afe66e5c102 | neu und nicht in den ausgeschlossenen Hashes |
| G1-Mesh | 38afeb304c9aefec48cbfdc8a90fe11c7fa08e3080147730deb9be5d666a4bfb | unverändert |
| D2-Mesh | 749d3c4b637cf513c35d42c144e9a645ac96b5107f33f017d439d6286cb480f6 | unverändert; changed_vertices=0 |
| neu/vektor.json | aac6afff89ecba5298377080b6442da03515721ccda68acff287fdc5b8652d1e | unverändert |
| neu/zellen_relief.csv | 99d30e55310453725aa1c9613900b5203f430f75f19745244fe3ebd650fc93fa | Quell-Diff 0 |
| neu/felder.npz | 64db8aac398fe627ee92935b662a0106d983337f57dd1b0412a7c3f5561fa41a | unverändert |
| Klippe 140|35 | 7,8840365 m | Kontrollwert |

Die Profilmessung liegt in [profil_tabelle.csv](bilder_p3d15/profil_tabelle.csv) und [profil_messung.json](bilder_p3d15/profil_messung.json). Kamera- und Sichtindikatoren sind in [kameras.json](bilder_p3d15/kameras.json) und [nahbild_werte.json](bilder_p3d15/nachher/nahbild_werte.json) archiviert.

## Testresultat

pytest neu/tests: **25 bestanden, 6 fehlgeschlagen** in 351,66 s. Das Ziel ≥26 bestanden / höchstens 5 fehlgeschlagen ist verfehlt.

- test_kreuzung_d1_g1_mesh_stufe: 0,844 m > 0,20 m.
- test_wegende_allgemein_mesh_ohne_blindenden: 23 Wegenden statt 0.
- test_saegezahn_d1_mesh_count: 41 Elemente statt 0.
- test_verwaschene_wand_d1_kantenschaerfe: 2,24 < 3,00.
- test_wegende_f1_c1_meshmessung: F1 0,17 > 0,10 m und keine C1-Endpunktmessung.
- test_schattenartefakt_renderbild: 0,307 > 0,25.

test_gelaende_mesh lief mit 4/4 bestandenen Prüfungen; der finale Meshmanifestwert für den maximalen D1-Quellenversatz ist 3,023922 m und liegt unter 4,0 m. Es wurden keine Tests oder Schwellen geändert.

## Annahmen, Grenzen und offene Punkte

- Map-Koordinaten werden für physische Abstände mit CELL_M=1,2 skaliert; der Gate-Nachbarsprung von 0,25 Map-Einheiten entspricht 0,30 m.
- Die LP-Untergrenze gilt für die ausgewiesenen Achs- und Ebenenstützen im lokalen R8-Prüffenster und das g=0,45-Profil. Das ist ein gezielter lokaler Unmöglichkeitsnachweis für die Stufengrenze, kein vollständiger Beweis zu allen Eigenschaften eines beliebigen künftigen Geländes.
- Ein kleinerer Ebenenkernradius von 2,00 m oder deutlich weichere Achs-/Ebenentoleranzen können die isolierte LP-Untergrenze unter 0,116 m bringen. Sie erfüllen die vorgegebenen Kern-/Toleranzbedingungen nicht; außerdem wurden R3-Zähler für solche gelockerten Varianten nicht nachgewiesen.
- Eine Verschiebung der Wegeführung könnte die Geometrie ändern, wurde aber wegen des Verbots einer vektor.json-Änderung nicht untersucht.
- Der direkte pruefe_regeln-Wert 596 aus dem vorgegebenen Stand ist auf dem aktuellen Reliefstand nicht reproduzierbar; p3d8 und p3d14 dokumentieren dieselbe Abweichung. Die direkte R8/R9-Basiswerte stimmen überein. Detaillierte Regelvergleiche in diesem Bericht verwenden deshalb p3d14s gespeicherten Neu-Mesh-Adapterstand als Vorher-Zustand und weisen die alte 596-Angabe getrennt aus.

**Build:** im relief3d-Verzeichnis mit RELIEF_NEU=1, RELIEF_KREUZUNG_VAR=19 und RELIEF_WEGEND_VAR=1: gen_relief.py, danach baue_html.py. Die Standardvariante der Kreuzung ist 19.

**Laufzeitnachweis:** /workspace/codex_jobs/log_p3d15.txt — gpt-6-luna, reasoning effort xhigh.
