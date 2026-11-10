# Ergebnis p3d18

**Zwischenstand: Variante 23 verfehlt die offizielle R3-Prüfung; die korrigierte Variante-24-Modellformulierung hat eine zulässige Lösung bewiesen. Stufenoptimierung und Endprüfung laufen.**
Stand: 10.11.2026 · Branch `art/dorfmap-p3d18` · Basis `c3659e7` · Kosten **0 EUR**.

## Kalibrierung gegen p3d17

Die unveränderte p3d17-Variante 22 wurde mit dem offiziellen Relief-Neu-Transfer nachgebildet und in ein temporäres Prüfeingabefeld überführt. Der rekonstruierte D1-Höhenraster ist bytegleich zum p3d17-Bericht: SHA-256 `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`. Danach wurde der unveränderte `pruefung/pruefe_regeln.py` ausgeführt.

| R3 D1-Zähler | p3d17-interne Ersatzindikatoren | offizieller Prüfer: Bericht | offizieller Prüfer: Wiederholung |
|---|---:|---:|---:|
| längs | 6 | 6 | 6 |
| quer | 5 | 17 | 17 |
| Wölbung | 4 | 19 | 19 |

Die Abweichung ist damit reproduziert und für das Modell behoben: Die bisherigen Quer- und Wölbungsindikatoren werteten das Zielraster aus, bevor der vollständige p3d17-Transfer einschließlich äußerer Überblendung angewendet wurde. Der Längsindikator nutzte zusätzlich `0,075 m` statt der offiziellen `0,08 m`. Das neue Modell bildet den feststehenden Transfer als affine Abbildung von Zielraster zu ausgegebenem Raster ab. Die R3-Abtastung folgt dem Prüfer mit `0,25` Karteneinheiten, 16 Werten je Abschnitt, gaußgefiltertem Längsrest (`sigma=8`), seitlichen Abständen `±1,5`, Querschwelle `3,5 %`, Wölbungsschwelle `0,08 m` und Querkappe `20 %`. Der Prüfer selbst wurde nicht geändert.

Reproduktion: `python3 codex_jobs/tools/p3d18_r3/calibrate_p3d17.py`. Der Lauf speichert seine temporären Prüfdaten unter `/tmp/gate_loch_p3d18_kalibrierung.json.gz` und `/tmp/regeln_p3d18_kalibrierung.json`.

## Korrigierte Machbarkeit Variante 24

Die Variante-23-Meshprüfung offenbarte einen Transferfehler; ihr vorheriger Modellpunkt ist daher kein Machbarkeitsbeleg. Nach Korrektur des affinen Intercepts und der Achsbedingungen wurde dieselbe Rechnung mit unveränderter Wegführung, `r=2,00 m`, Achsstützen `±0,02 m`, den offiziellen R3-Operatoren und Limits längs/quer/Wölbung `6/7/7`, Querkappe `20 %`, R8-Gitter `0,020 m`, R8-Quer `3 %` und Stufe `0,116 m` neu gelöst.

HiGHS fand einen zulässigen ganzzahligen Punkt und bewies das Optimum der verwendeten Machbarkeitszielfunktion (Summe der R3-Indikatoren plus `0,001 × Stufe`). Das beantwortet die geforderte Machbarkeitsfrage mit **ja**; die separaten Mindeststufenrechnung läuft anschließend.

| Modellmessung am zulässigen Punkt | Ergebnis | Schranke |
|---|---:|---:|
| Kreuzungsstufe | `0,115153279 m` | `≤0,116 m` |
| R8-Gitter | `0,020000000000037 m` | `≤0,020 m` (numerisch am Rand) |
| R8-Quer | `2,999422 %` | `≤3 %` |
| R3 längs / quer / Wölbung | `4 / 0 / 4` Abschnitte | `≤6 / ≤7 / ≤7` |
| R3 maximales Quergefälle | `≤20 %` im Modell | `≤20 %` |
| Achsstützen | 359 Stützpunkte, mit `±0,02 m` begrenzt | `±0,02 m` |
| Ebenenkern | `r=2,00 m`; Ebenenneigung `2,216100 %` | Radius unverändert; `≤3 %` |
| Modell | 7.858 Variablen, 10.136 Nebenbedingungen; MIP-Lücke `0` | HiGHS Status optimal |

Das ist ein Modellbeleg, noch kein Mesh-Gate-Beleg. Der R8-Gitterwert liegt numerisch praktisch auf der Grenze und wird am ausgegebenen Mesh durch den unveränderten offiziellen Prüfer kontrolliert. Der vollständige Solverbericht liegt unter [`bilder_p3d18/variante24_machbarkeit.json`](bilder_p3d18/variante24_machbarkeit.json).

## Stufenoptimierung und Variante-23-Diagnose

Nach dem Machbarkeitsnachweis lief dieselbe Ganzzahlrechnung mit der Kreuzungsstufe als Zielfunktion und einem vollständigen zulässigen MIP-Start. HiGHS erreichte nach 3.600 Sekunden keinen Optimalitätsbeweis, fand aber einen besseren zulässigen Punkt. Dieser Stand ist für den direkten Transfer mit Variante 23 vorgesehen.

| Messung am verwendeten Baupunkt | Ergebnis | Schranke | Status |
|---|---:|---:|---|
| Kreuzungsstufe am tatsächlichen R8-Zentrum | `0,097046496 m` | `≤0,116 m` | erfüllt |
| R8-Gitter | `0,020000000000011 m` | `≤0,020 m` | numerisch an Grenze; Mesh-Prüfer maßgeblich |
| R8-Quer | `2,993470 %` | `≤3 %` | erfüllt |
| R3 längs / quer / Wölbung | Modell: `6 / 7 / 6` Abschnitte | `≤6 / ≤7 / ≤7` | Modellzählung später durch Mesh-Prüfung widerlegt |
| R3 maximales Quergefälle | Modell: `≤20 %` | `≤20 %` | Modellzählung später durch Mesh-Prüfung widerlegt |
| Achsstützen | 359, je `±0,02 m` | `±0,02 m` | erfüllt |
| Ebenenkern | `r=2,00 m`, Neigung `2,308368 %` | unveränderter Radius, `≤3 %` | erfüllt |

Der Incumbent ist `0,097046486 m`; die duale Untergrenze beträgt `0,076068872 m`, die MIP-Lücke `21,616 %`. Das ist nur der beste Punkt der fehlerhaften Transferformulierung, kein bestätigtes Mesh-Ergebnis und kein bewiesenes globales Minimum. Die frühere Modell-Machbarkeitslösung bei `0,115266302 m` zählt ebenfalls nicht als unabhängiger offizieller R3-Beleg.

Variante 23 wurde mit dem unveränderten Neu-Mesh-Adapter geprüft. Am Zielkreuz `152.5|28.5` misst R8 Stufe `0,097 m`, Gitter `0,020 m` und keinen R8-Quer-Treffer. Die Abweichungen an Achsstützen und R3-Zählern belegen jedoch einen Transferfehler:

| Variante-23-Meshmessung D1 | Ergebnis | Vorgabe | Bewertung |
|---|---:|---:|---|
| Offizielles R3 längs / quer / Wölbung | `7 / 20 / 21` Abschnitte | `≤6 / ≤7 / ≤7` | verfehlt |
| Größter offizieller R3-Querwert | `41,3 %` (`rampe_11`, `148.5|2.5`) | `≤20 %` | verfehlt |
| Achsstützen nach endgültigem Meshtransfer | `12 / 359` über 2 cm; maximal `0,064167 m` | alle `±0,02 m` | verfehlt |
| Internes Transferdiagnostikfeld vor nachgelagertem Tile-Fade | 2 Punkte über 2 cm; maximal `0,622627 m` | alle `±0,02 m` | verfehlt |
| D1-R8-Gesamttreffer (Stufe/Gitter/Quer/Wegende) | `2 / 3 / 1 / 1` | Zielkreuz `0` | Zielkreuz selbst erfüllt; weitere Punkte außerhalb davon offen |

Die Ursache ist im Modell lokalisiert: Der affine Transferabschnitt behandelte den festen Transferintercept irrtümlich wie einen Hintergrundwert und multiplizierte ihn nochmals mit `1−Deckung`; die Achsbedingung bezog sich außerdem auf das Zielraster statt auf die ausgegebene, überblendete Meshfläche. Dadurch sagte das Modell R3 `6/7/6` voraus, während derselbe offizielle Prüfer am gebauten Mesh `7/20/21` zählt. Variante 24 korrigiert diese Abbildung und bindet die ausgegebene Meshhöhe an den Achsstützen. Prüfer, Schwellen, Route und Ebenenkernradius bleiben unverändert.

Die vollständigen Variante-23-Treffer und Achsabweichungen liegen unter [`bilder_p3d18/variante23_diagnose/`](bilder_p3d18/variante23_diagnose/). Der vorläufige `pruefe_regeln`-Lauf diente nur der R3-Diagnose und lief ohne Lochscan; seine Gesamtsumme ist deshalb kein Gate-Gesamtergebnis.

Der Variante-23-Build hielt D2 bytegleich (`749d3c4b…`), G1 bytegleich (`38afeb30…`), Zellquellspalten (`zellen_quell_diff=0`) und Vektorhash (`aac6afff…`) ein. LOD1 hat `134.316` Dreiecke. Die maximale D1-Höhenänderung lag genau an der Grenze `4,0 m`. D1-Hash: `c7a10535…`.

## Noch offen

- Mindeststufe bei denselben harten Grenzen; der zulässige Machbarkeitspunkt dient als MIP-Start.
- Variante-24-Mesh und vollständige offizielle Gate-Läufe, Regression, Adapter/Xvfb/LOD- und Bildprüfung.

Keine Wegführung, Prüfschwelle, Zellquelle, D2-Datei oder Ebenenkernradius wurde geändert. Es wurde noch kein p3d18-Mesh gebaut.
