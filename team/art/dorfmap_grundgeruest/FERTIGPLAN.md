# FERTIGPLAN Dorfmap (Endstand 16.11.2026, 23:01 Uhr MEZ)

Branch `art/dorfmap-fertig` (Kopf **a1775fc** = QA P4h, Kartendaten **42f05de** = L3j). Basis des Branches: eb2cd86 (p3d36). Marker: [S] gemessen, [A] Annahme, [R] gerechnet, [F] Fabian.

## Lieferregel [F] (t2029u)

> „Wenn man es nicht sieht ist es mir egal. Aber hier geht es prinzipiell um Optik ist alles.“

1. Maßstab ist die Optik. Was mit bloßem Auge nicht sichtbar ist, kommt mit Messwert und Nahbild in die Ausnahmeliste und blockiert die Lieferung nicht.
2. Sichtbare Stellen kommen nie auf die Ausnahmeliste; sie bleiben Befund und müssen weg.
3. Priorität hat, was im Nahbild auffällt. P4 (QA) ist der Hauptfilter.
4. Die Abnahme ist die Sichtprüfung aller 56 Kacheln, nicht die Trefferzahl allein.
5. Schwellen und Prüfer bleiben unverändert. Eine Ausnahme ersetzt keinen Prüfer, sie dokumentiert nur einen unsichtbaren Rest.

## Endstand Sichtprüfung [S]

QA P4h ([PR #43](https://github.com/Xenatosa/Planer/pull/43), Commit a1775fc, gegen 42f05de): **56 sauber / 0 leicht / 0 stark.** Ablage: `relief3d/pruefung/qa_p4h/`.

Gate (Prüfer und Schwellen unverändert):

| Größe | Ist |
|---|---|
| Regeln (pruefe_regeln) | **359** (Ausnahmen 0, Trefferliste identisch zu P4g) |
| R8 | **31** |
| R9 | **321** |
| W1 (Index) | **0** |
| W1 alle 56 | **0** |
| Loch (offen_innen) | **0** |

E3 190\|97 (letzter offener Befund aus P4g): Schulter und Breitensprung sind weg, der Trichter läuft glatt in den Kanal. Messung 0,18 m / 29,6°, kein Gate-Treffer. Die 17 Ausnahmen bleiben unsichtbar.

Das QA-Urteil 56/0/0 ersetzt nicht die Endabnahme nach t2029u. Die Sichtprüfung der 56 Kacheln geht über New Bot an Fabian.

## Merge-Kette 16.11.2026 [S]

Alle PRs #28–#43 auf `art/dorfmap-fertig`, jeweils mit Aufseher-Prozess-JA, ohne Direkt-Push nach `main` oder in den Integrationsbranch. Zeiten in MEZ. Merge-Commit laut `gh pr list`; erster Eltern-Kopf ist a1775fc (`git log --first-parent`).

| PR | Merge (MEZ) | Commit | Titel |
|---|---|---|---|
| [#28](https://github.com/Xenatosa/Planer/pull/28) | 15:13 | 9742a92 | P12-v3: Normalen über Kachelnähte gemeinsam (ersetzt #24) |
| [#29](https://github.com/Xenatosa/Planer/pull/29) | 15:28 | 2771f70 | P12b-v4: Wasserrand im 56-Kachel-Viewer weich statt geklemmt |
| [#30](https://github.com/Xenatosa/Planer/pull/30) | 15:46 | d631cf8 | QA P4d: Dorfmap 2771f70 – 56 Kacheln, Restfehler, Ausnahmeliste (ersetzt #18) |
| [#31](https://github.com/Xenatosa/Planer/pull/31) | 16:05 | b3698e0 | L3d: QA-P4d-Platten + H7-Rand, E3-Westufer, G7-Nord Ausnahme, bau_endstand Schritt 12 |
| [#32](https://github.com/Xenatosa/Planer/pull/32) | 16:54 | 1778473 | L3e: F7-Nordufer-Zähnchen, G7-Nordufer (Weg A), G7-Plättchen |
| [#33](https://github.com/Xenatosa/Planer/pull/33) | 17:18 | cffe940 | P12c: Wasserrand-Abstandsfeld |
| [#34](https://github.com/Xenatosa/Planer/pull/34) | 17:27 | 8c1fc80 | P2d: rampe_5-Band D4/D5 + Brückenanschlüsse E2/E3 |
| [#35](https://github.com/Xenatosa/Planer/pull/35) | 18:24 | bfe8dce | L3f+L3g: F7/G7-Lichtspitzen und E3-West-Rinne, bau Schritt 15 |
| [#36](https://github.com/Xenatosa/Planer/pull/36) | 18:45 | 41d3953 | QA P4e: 56 Kacheln (52/4/0), Restfehler, Ausnahmen, Korrektur P4d-G7 |
| [#37](https://github.com/Xenatosa/Planer/pull/37) | 19:29 | f942124 | P2e: rampe_5 Milchband D4/D5 nur VC angeglichen |
| [#38](https://github.com/Xenatosa/Planer/pull/38) | 20:51 | a6b00ba | L3h: E3-Bach kräftiger, E4-Bach Uferrand glatt (Schritt 17) |
| [#39](https://github.com/Xenatosa/Planer/pull/39) | 21:19 | 30ffe43 | QA P4f: finale Sichtprüfung 56 Kacheln @ a6b00ba (54 sauber / 2 leicht) |
| [#40](https://github.com/Xenatosa/Planer/pull/40) | 21:57 | 0a0b83a | L3i: E3-Nord durchgehender Kanal, G1-Krater Wasser→Schnee (Schritt 18) |
| [#41](https://github.com/Xenatosa/Planer/pull/41) | 22:11 | 15763a7 | QA P4g: Nachsicht L3i @ 0a0b83a (55 sauber / 1 leicht E3) |
| [#42](https://github.com/Xenatosa/Planer/pull/42) | 22:45 | 42f05de | L3j: E3-Kanalanfang als Trichter (Schritt 19) |
| [#43](https://github.com/Xenatosa/Planer/pull/43) | 23:03 | a1775fc | QA P4h: Mini-Nachsicht E3-Kanalanfang @42f05de – 56 sauber / 0 / 0 |

Hinweis: #41 ist im ersten Eltern-Log über den Merge-Commit 7a87d1a in `art/dorfmap-L3j` eingegangen, der Kopf nach #42 ist 42f05de. Inhaltlich keine Überschneidung mit den Kartendaten.

## Ausnahmeliste [S]

Konsolidiert in [`AUSNAHMEN_FINAL.md`](AUSNAHMEN_FINAL.md): **17 Einträge (A1–A17)**, jeweils mit Messwert und Nahbild, übernommen aus `relief3d/pruefung/qa_p4h/LISTE_AUSNAHMEN.md` (Stand 42f05de). Alle mit bloßem Auge unsichtbar. Sichtbare Stellen stehen nicht in dieser Liste.

## Kosten [S]

Nachtrag zur Kostenzeile in QA P4h: Die Laufzeit dort stand nur mit Beginn „ab 22:45“. Ende nachgetragen: **22:45–23:01 MEZ** (Commit-Zeit von `qa/dorfmap-p4h` a1775fc: 2026-11-16 23:01:33 +0100). Kosten 0 €, kein Codex. Das hat den Merge von #43 nicht blockiert.

## Offen

- Kritiker-Sicht **P8** (unabhängiger Blick auf die 56 Kacheln).
- **Endabnahme durch Fabian** nach t2029u: Sichtprüfung der 56 Kacheln, über New Bot.

## Arbeitspakete (Stand)

| Nr | Inhalt | Stand |
|---|---|---|
| P1 / L3 | Höhen und sichtbare Formfehler (L3b–L3j statt des ursprünglichen L1/L2-Plans) | erledigt bis L3j (#42) |
| P2 | Wegnetz (P2b–P2e) | erledigt (#34, #37) |
| P3 | Texturen T1–T5 | erledigt (früherer PR #8) |
| P4 | QA-Sichtfilter, alle 56 Kacheln | erledigt in P4h (#43), 56/0/0 |
| P5 | unabhängige Gate-Nachzählung | unverändert vorgesehen, nicht Teil dieses Endstands |
| P6 | Trefferkarte 8×7 | erledigt (PR #4) |
| P7 | Gate-Beschleunigung | niedrige Priorität, volles Gate bleibt maßgebend |
| P8 | Kritiker-Sichtprüfung | **offen** |
| P9 | Endabnahme an Fabian | **offen** (QA-Urteil liegt vor, Freigabe durch Fabian ausstehend) |

## Ausgangsstand am Morgen (Kontext) [S]

Am 16.11. 07:15 Uhr MEZ, vor der Tagesarbeit: pruefe_regeln 570, r8 48, r9 334. Gate-Befehl im Ordner `team/art/dorfmap_grundgeruest/relief3d`:

`NODE_PATH=/tmp/w3/node_modules HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js && sh pruefung/export_gate.sh`

D2-Höhen bleiben bitgleich gesperrt (SHA-256 749d3c4b… seit p3d25). Die Kacheltabelle mit den Morgen-Treffern ist durch P4h und die Gate-Zahlen oben ersetzt.

## Arbeitsregel für andere Bots

- Eigener Branch von `art/dorfmap-fertig`, Lieferung als PR auf `art/dorfmap-fertig`. Nichts nach `main`, kein Direkt-Push in den Integrationsbranch.
- Gate-Zahlen (pruefe_regeln, r8, r9, W1, Loch; vorher/nachher) liegen jeder Kartendaten-PR bei.
- Keine neuen Treffer in fremden Familien. D2-Höhen bitgleich, Schwellen und Prüfer unverändert.
- Nichts löschen, alte Dateien per `git mv` nach `_alt/`. Keine Secrets. Keine Binärdaten in Doku-PRs.
