# Ergebnis p3d18

**Zwischenstand nach R3-Kalibrierung; Machbarkeit noch offen.**
Stand: 10.11.2026 · Branch `art/dorfmap-p3d18` · Basis `c3659e7` · Kosten **0 EUR**.

## Kalibrierung gegen p3d17

Die unveränderte p3d17-Variante 22 wurde mit dem offiziellen Relief-Neu-Transfer nachgebildet und in ein temporäres Prüfeingabefeld überführt. Der rekonstruierte D1-Höhenraster ist bytegleich zum p3d17-Bericht: SHA-256 `26b849f6384993d5029b58dc08f6c657406785e26939f7c172a0d8fafe1ace29`. Danach wurde der unveränderte `pruefung/pruefe_regeln.py` ausgeführt.

| R3 D1-Zähler | p3d17-interne Ersatzindikatoren | offizieller Prüfer: Bericht | offizieller Prüfer: Wiederholung |
|---|---:|---:|---:|
| längs | 6 | 6 | 6 |
| quer | 5 | 17 | 17 |
| Wölbung | 4 | 19 | 19 |

Die Abweichung ist damit reproduziert und für das Modell behoben: Die bisherigen Quer- und Wölbungsindikatoren werteten das Zielraster aus, bevor der vollständige p3d17-Transfer einschließlich äußerer Überblendung angewendet wurde. Der Längsindikator nutzte zusätzlich `0,075 m` statt der offiziellen `0,08 m`. Das neue Modell bildet den feststehenden Transfer als affine Abbildung von Zielraster zu ausgegebenem Raster ab. Die R3-Abtastung folgt dem Prüfer mit `0,25` Karteneinheiten, 16 Werten je Abschnitt, gaußgefiltertem Längsrest (`sigma=8`), seitlichen Abständen `±1,5`, Querschwelle `3,5 %`, Wölbungsschwelle `0,08 m` und Querkappe `20 %`. Der Prüfer selbst wurde nicht geändert.

Reproduktion: `python3 codex_jobs/tools/p3d18_r3/calibrate_p3d17.py`. Der Lauf speichert seine temporären Prüfdaten unter `/tmp/gate_loch_p3d18_kalibrierung.json.gz` und `/tmp/regeln_p3d18_kalibrierung.json`. Die Kalibrierung bestätigt den Ausgangszustand; sie ist noch keine Machbarkeitsaussage für die neuen gemeinsamen Limits.

## Noch offen

- Gemeinsame Machbarkeit mit Kreuzungsstufe `≤0,116 m`, R8-Gitter `≤0,020 m`, R8-Quer `≤3 %`, R3 `≤6/≤7/≤7`, Querkappe `≤20 %` und Achsstützen `±0,02 m`.
- Falls unmachbar: minimale erreichbare R3-Quer- und Wölbungszähler bei Stufe `≤0,116 m` und R3-Längs `≤6`, außerdem minimale Stufe und bindende Stationen bei Quer/Wölbung `≤7`.
- Gegebenenfalls danach erst Mesh-Bau, gemeinsame Gate-Prüfungen und Bildprüfung.

Keine Wegführung, Prüfschwelle, Zellquelle, D2-Datei oder Ebenenkernradius wurde geändert. Es wurde noch kein p3d18-Mesh gebaut.
