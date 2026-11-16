# ERGEBNIS L3c2 – L3c neu aufgebaut auf art/dorfmap-fertig @a6a4831 (nach P2b/P2c, PR #21)

Kosten: 0 € · Codex: nein · Laufzeit: 13:30–13:44

Branch `art/dorfmap-L3c2`, Basis `a6a4831`. **Ersetzt #22.** Generierte Daten (relief_daten, relief_neu, index.html, Gate-Dateien) wurden auf a6a4831 neu erzeugt; aus L3c (#22) stammen nur Code, Stellen, Test und Berichte.

## 1. Reihenfolge und Aufbau (P2b wird nicht überschrieben)
Die Erzeugungskette auf `art/dorfmap-fertig` lautet: `relief_l3.py` (L3/L3b) → `relief_p2b.py` (P2b/P2c, prüft `basis_gb_sha256` = GB nach L3) → `p2b_bruecken.py` → `gen_textur.py vc` + `p2b_vc_lokal.py` → `p2b_r5_textur.py` → `html_payload_p3.py` → `waende_einsetzen.py`.

Würde L3c die L3/L3b-Stellen mit dem neuen Maßstab neu rechnen, passte der Basis-Hash von P2b nicht mehr, und P2b liefe nicht. Deshalb:
- **L3/L3b eingefroren:** `relief_l3.py` ohne Option rechnet L3/L3b weiter mit dem alten Maßstab (`massstab_l3_l3b_eingefroren: 1.0` in `l3_stellen.json`). Belegt: Neu gerechnet aus dem Ursprung (c6a3db0) ergibt das GB `32e93914…`, genau die P2b-Basis, also bitgleich. Mit richtigem Maßstab käme `4531adaf…` heraus; P2b bräche dann ab.
- **L3c als eigener Nachschritt NACH P2b/P2c:**
  - Aufruf `relief_l3.py --stufe-c` mit Basis-Hash = GB von a6a4831 (`91c831fd…`).
  - Eigener Rückweg `pruefung/l3c_rueck.npz` (`--stufe-c --aus`).
  - Nur die Stellen `L3c_*`, mit dem richtigen Maßstab.
- **Rücksetzen der alten Wegtreffer:** Stufe c setzt jeden Vertex auf den Originalwert zurück, den L3/L3b auf einer echten Kernfläche geändert hat (Weg, Kreuzung, Rampenkern ≤ 1,8, WEGA/wege, Brücke, richtiger Maßstab) und den P2b nicht angefasst hat. Das waren genau **7 Vertices**: 13 G4 (277,5–278,5|140,5–141,5, max 0,284 m) und 18 H2 (329,5|67,0 und 330,5|67,5). Im Nahbild ist nichts sichtbar (`l3c2_nahbilder/wegtreffer_zurueckgesetzt/`).
- **Farbe nur lokal:** `gen_textur.py vc` rechnet VC/FW.c überall neu und würde P2b-Farbarbeit (rampe_5) überschreiben. Neu ist `pruefung/l3c_vc_lokal.py`: Es setzt VC/FW.c außerhalb von 8 Zellen um die L3c-Änderungen auf a6a4831 zurück (gleiches Muster wie `p2b_vc_lokal.py`) und hat einen Rückweg (`--aus`). Ergebnis: VC ist gegenüber a6a4831 bytegleich.
- **Kette L3c2:** a6a4831 → `relief_l3.py --stufe-c` → `gen_textur.py vc` → `pruefung/l3c_vc_lokal.py <vorher> <vorher_neu>` → `html_payload_p3.py` → `waende_einsetzen.py` → Gate → `alles.sh`.

## 2. Maßstab-Fix `relief_l3.schutz()` und Test
- `schutz(..., zellweite=None)`: Standard ist der richtige Maßstab aus `vektor.json karte.zellweite_m` (1,2). `zellweite=1.0` gibt es nur für den eingefrorenen L3/L3b-Lauf.
- Neu: `feste_flaechen()` (Kernflächen im richtigen Maßstab) für das Rücksetzen.
- Test `pruefung/test_l3_schutz.py` auf a6a4831/L3c2: **bestanden (exit 0)**.
  - Median-Abstand der Quellzellen zur Mittellinie: 0,0 Zellen (Meter als Zellen wären 49,53).
  - Quellzellen von Wegen und Kreuzungen: 4120 von 4120 im Schutz; allein über vektor.json 100 %.
  - WEGA: 100 %.
  - Der alte Code fiel in L3c durch (43,6 %).

## 3. Stelle 23 (G6) – Entscheidung
- Das Nahbild auf a6a4831 (`l3c2_nahbilder/paare/G6_vorher_nachher.jpg`, Blicke G6_23, G6_23_oben, G6_p2b 283|222) zeigt die Rippen aus L3 nicht mehr; P2b hat die Sägezahn-Böschung von rampe_4 behoben.
- **L3c2 ändert in G6 nichts:** 0 Vertices in x 260–290 / z 220–250, vorher = nachher.
- **Stelle 23 bleibt trotzdem in `l3_stellen.json` (unverändert).** Begründung: Sie ist Teil des eingefrorenen L3-Ergebnisses, auf das P2b per Hash aufsetzt (P2b-Stelle 23 arbeitet auf dem L3-23-Stand weiter). Nimmt man 23 heraus, wird die P2b-Basis ungültig: `relief_p2b.py` bricht ab, oder die P2b-Arbeit in G6 ginge verloren. Eine zusätzliche L3c-Änderung braucht 23 nicht. P2b hat dort Vorrang.
- Im Ton-Nahbild sieht man eine leichte Kerbe an der Krone und eine fein gezahnte Unterkante; beides ist vorher wie nachher gleich. Das gehört zu P2b/rampe_4 und wird nicht angefasst.

## 4. Ergebnis je Stelle (Nahbild, selbst angesehen; Paare in `l3c2_nahbilder/paare/`)

| Stelle | Maßnahme | Ergebnis | Paar |
|---|---|---|---|
| G7 + Ost | `L3c_G7`, `L3c_G7b` (Rillen schließen, WV/Bett glätten, Insel 5 V füllen, Landufer +0,08 m) | **weg**: keine Leitern, keine Linien, keine Platte, Wasser durchgehend | `G7_vorher_nachher.jpg` |
| C7 | `L3c_C7` (2 Inseln, 42 V, gefüllt) | **weg** | `C7_vorher_nachher.jpg` |
| H7 | `L3c_H7` (Landufer heben) | **teilweise**: Blöcke weg, Treppenrand der SO-Bucht bleibt → Ausnahme | `H7_vorher_nachher.jpg` |
| E2-Westufer (20) | – | **Ausnahme** (Renderer-Rasterkante des Wassermeshes, siehe AUSNAHMEN_L3c) | `E2_vorher_nachher.jpg` |
| E3 | – | **Ausnahme** (gleiche Ursache) | `E3_vorher_nachher.jpg` |
| 23 G6 | keine (P2b-Vorrang) | unverändert, vorher = nachher | `G6_vorher_nachher.jpg` |

## 5. Gate je Regel (vorher a6a4831 / nachher L3c2), `L3c2_gate_vorher_nachher.json`

| Prüfer | vorher | nachher |
|---|---:|---:|
| pruefe_regeln (export_gate) | 371 | 372 |
| pruefe_regeln mit eigenem Lochscan `/tmp/gate_loch_L3c2.json` | 371 | 372 |
| r8 | 31 | 31 |
| r9 | 325 | 325 |
| W1 / W1 alle56 | 0 / 0 | 0 / 0 |
| Lochscan Hauptviewer (offene Innenkanten) | 0 | 0 |

| Datei | Regel | vorher | nachher |
|---|---|---:|---:|
| regeln | G2_spitze_oben | 2 | 2 |
| regeln | G2_spitze_oben_fein | 9 | 9 |
| regeln | G3_spitze_unten_fein | 2 | 2 |
| regeln | G5_beule_klippe | 35 | 34 | **geändert**
| regeln | G6_facette | 215 | 217 | **geändert**
| regeln | G7_wand_glatte_flaeche | 1 | 1 |
| regeln | G7b_wandkontur_feld | 29 | 29 |
| regeln | G7b_wandkontur_kantenschaerfe | 1 | 1 |
| regeln | G7b_wandkontur_rauheit | 1 | 1 |
| regeln | G8_fluss_nicht_bis_rand | 1 | 1 |
| regeln | R1_blind | 17 | 17 |
| regeln | R2_getrennt | 8 | 8 |
| regeln | R3_laengs_m | 21 | 21 |
| regeln | R3_quer_pct | 8 | 8 |
| regeln | R3_woelb_m | 8 | 8 |
| regeln | R5_loch | 4 | 4 |
| regeln | R6_wasser_schnee | 4 | 4 |
| regeln | T1_fleckrand | 1 | 1 |
| regeln | T2_textur_abgeschnitten_bildpruefung_offen | 1 | 1 |
| regeln | T3_streifen_ringe_bildpruefung_offen | 1 | 1 |
| regeln | T4_graue_flussstreifen_bildpruefung_offen | 1 | 1 |
| regeln | T5_textur_vs_clay_bildpruefung_offen | 1 | 1 |
| r8 | R8_gitter | 6 | 6 |
| r8 | R8_quer | 3 | 3 |
| r8 | R8_stufe | 6 | 6 |
| r8 | R8a_wegende | 16 | 16 |
| r9 | R8b_delle | 22 | 22 |
| r9 | R9_saegezahn | 34 | 34 |
| r9 | R9w_wellen | 269 | 269 |

- Neu sind 2 Treffer, beide im Nahbild unsichtbar (`AUSNAHMEN_L3c.md`, `l3c2_nahbilder/neue_treffer/`): G6_facette G7 264,0|268,8 (18) und G6_facette H7 319,1|275,4 (9).
- Entfallen ist G5_beule_klippe H7 331,8|278,0.
- **R6_wasser_schnee 4→4, G8_fluss_nicht_bis_rand 1→1, R5_loch 4→4.**

## 6. Abstand je Stelle (alle L3-, L3b- und L3c-Stellen)
Vergleich gegen den Ursprung c6a3db0, ohne die von P2b/P2c geänderten Vertices (`p2b_rueck.npz`; das ist P2b-Verantwortung). Einheit Zellen (1 Zelle = 1,2 m), Vertexraster 0,5, richtiger Maßstab. Die Daten stehen in `l3c2_abstaende_je_stelle.json`.

| Stelle | Kachel | Vertices | max Δ m | Vektorweg | Kreuzung | Rampenkern | WEGA/wege | Wasser | auf Weg/Kreuz/Rampe/WEGA | auf Wasser |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | C3 | 2077 | 2.405 | 36.0 | 39.15 | 44.32 | 38.01 | 19.45 | 0 | 0 |
| 02 | C3 | 1215 | 1.51 | 34.79 | 33.2 | 33.35 | 33.68 | 40.07 | 0 | 0 |
| 03 | D1 | 576 | 1.797 | 12.51 | 11.67 | 0.5 | 12.02 | 47.43 | 0 | 0 |
| 04 | C3 | 492 | 1.32 | 34.64 | 33.09 | 24.14 | 33.32 | 51.97 | 0 | 0 |
| 05 | D4 | 891 | 2.405 | 15.0 | 17.5 | 1.41 | 17.5 | 22.98 | 0 | 0 |
| 06 | C4 | 741 | 1.605 | 39.2 | 40.48 | 1.8 | 41.15 | 28.15 | 0 | 0 |
| 06b | C4 | 501 | 1.704 | 31.95 | 33.72 | 1.8 | 34.15 | 27.95 | 0 | 0 |
| 07 | D6 | 904 | 2.537 | 47.71 | 48.13 | 2.0 | 46.04 | 10.77 | 0 | 0 |
| 08 | B4 | 696 | 1.29 | 76.13 | 78.54 | 44.32 | 78.6 | 38.5 | 0 | 0 |
| 09 | C5 | 874 | 1.135 | 56.02 | 56.7 | 1.8 | 57.4 | 34.71 | 0 | 0 |
| 10 | E7 | 104 | 0.045 | 65.76 | 66.71 | 29.44 | 67.06 | 0.5 | 0 | 0 |
| 11 | C4 | 1150 | 1.099 | 67.8 | 69.1 | 17.89 | 69.77 | 48.63 | 0 | 0 |
| 12 | D6 | 421 | 1.178 | 67.53 | 68.31 | 0.5 | 66.19 | 15.7 | 0 | 0 |
| 13 | G4 | 662 | 2.004 | 0.5 | 1.0 | 1.8 | 1.58 | 77.43 | 0 | 0 |
| 14 | E1 | 552 | 3.223 | 7.63 | 9.18 | 1.8 | 8.08 | 19.14 | 0 | 0 |
| 15 | C6 | 697 | 1.014 | 93.43 | 94.04 | 9.18 | 93.13 | 33.74 | 0 | 0 |
| 16 | H6 | 879 | 1.922 | 32.6 | 31.95 | 4.12 | 32.5 | 32.5 | 0 | 0 |
| 17 | H3 | 488 | 0.709 | 14.33 | 16.32 | 44.82 | 14.21 | 83.44 | 0 | 0 |
| 18 | H2 | 1229 | 1.241 | 0.5 | 5.7 | 55.86 | 1.58 | 65.12 | 0 | 0 |
| 19 | G3 | 1069 | 1.028 | 3.54 | 3.16 | 8.85 | 3.0 | 85.65 | 0 | 0 |
| 20 | E2 | 126 | 0.058 | 8.14 | 9.5 | 25.61 | 7.5 | 2.06 | 0 | 0 |
| 21 | F6 | 208 | 1.271 | 15.21 | 17.61 | 21.32 | 17.1 | 1.58 | 0 | 0 |
| 21b | F6 | 973 | 1.865 | 26.4 | 29.33 | 7.16 | 28.18 | 1.58 | 0 | 0 |
| 22 | F1 | 393 | 0.164 | 25.81 | 28.64 | 17.22 | 26.52 | 0.5 | 0 | 0 |
| 23 | G6 | 227 | 0.417 | 22.68 | 20.43 | 0.5 | 21.02 | 6.8 | 0 | 0 |
| L3b_10 | E7/F7 | 3869 | 0.75 | 66.5 | 66.5 | 15.4 | 65.02 | Wasserstelle | 0 | 2267 |
| L3b_22 | F1 | 1534 | 0.669 | 24.17 | 26.86 | 7.91 | 25.12 | Wasserstelle | 0 | 361 |
| L3b_24 | C4/D4 | 840 | 1.402 | 28.86 | 30.91 | 1.8 | 31.18 | 28.43 | 0 | 0 |
| L3c_G7 | G7 | 1390 | 0.66 | 57.21 | 57.0 | 5.83 | 55.51 | Wasserstelle | 0 | 685 |
| L3c_C7 | C7 | 1511 | 0.818 | 125.9 | 126.57 | 43.8 | 124.45 | Wasserstelle | 0 | 808 |
| L3c_H7 | H7 | 2031 | 0.968 | 76.04 | 74.5 | 43.41 | 75.03 | Wasserstelle | 0 | 1044 |
| L3c_G7b | G7/H7 | 2802 | 1.057 | 55.11 | 53.24 | 10.4 | 53.6 | Wasserstelle | 0 | 1517 |

- **Summen nach L3c2:** Geänderte Vertices auf vektor.json-Weg / Kreuzung / Rampenkern / WEGA-wege: **0 / 0 / 0 / 0**. Nicht-Wasserstellen auf Wasser: 0. Änderungen ohne Stelle: 0.
- Vorher (a6a4831) waren es 7 / 0 / 0 / 0 (13: 5, 18: 2).
- Die kleinsten Abstände sind 0,5 Zellen (Nachbarvertex), nicht auf der Fläche: 13 und 18 am Wegrand, 03, 12 und 23 am Rampenkern.

## 7. Wasser- und SHA-Belege (`l3c2_sha_belege.json`)
- **Wasser:** 0 Vertices entfernt. Neu sind 47 Vertices, nur die 3 eingeschlossenen Inseln; außerhalb von fill_holes(alt): 0.
- **Flussverlauf:** SHA256(packbits(fill_holes(WV > −900))) vorher = nachher `defa6d61…98c4`. Rohmaske `c897e44c…` → `2e8006ba…` (nur die Inseln).
- **WV auf altem Wasser:** 4092 Vertices geändert, max 0,895 m.
- **GB:** 7799 Vertices geändert, max 1,057 m (davon 7 Rücksetzungen).
- Felder geändert: FW (nur h), GB, WV, baeume, steine (Höhen folgen). **VC unverändert.**
- **D2 bitgleich** `749d3c4b…80f6`. D1 und D2: GB, WV und VC je 0 Vertices geändert → **Sperrzone D1 (X084/rampe_2, Mulde 159|22,9) unberührt.**
- Endstand: relief_daten.json.gz `76a1e5830e8834c9…`, neu/relief_neu.json.gz `233b8373060c1744…`, index.html = neu/index.html `995a2764008befdb…`.
- `--aus`-Roundtrip: `relief_l3.py --stufe-c --aus` + `l3c_vc_lokal.py --aus` + payload + waende ergibt **bytegleich a6a4831** (relief_daten `c4489748…`, relief_neu `941d0e21…`, index.html `d4703a48…`). Erneutes Einschalten ist bytegleich zum ersten Lauf, einschließlich der Rückweg-Dateien.
- `alles.sh /tmp/l3c2/p10`: EXIT 0. D1/G1/D2 sind identisch mit index.html, Wände identisch, Naht max 0,0 m. Lochscan über 56 Kacheln: 0 (Positivkontrolle C3 = 3).

## 8. Hinweis für bau_endstand.sh
Nachschritt 11 (neu, nach den P2b-Schritten 7–10): `python3 relief_l3.py --stufe-c`, dann `gen_textur.py vc` und `pruefung/l3c_vc_lokal.py <vorher> <vorher_neu>`, dann `html_payload_p3.py` und `waende_einsetzen.py`. Hier nur dokumentiert; `bau_endstand.sh` selbst ist nicht geändert (wie bei P2b/P2c).
