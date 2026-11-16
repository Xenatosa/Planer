# ERGEBNIS L3c – Wasser-Folgebefunde aus QA P4c (G7, C7, H7, E3)

Branch `art/dorfmap-L3c`, Basis `d5b17e2` (L3b-Kopf, PR #20 – **baut auf #20 auf, erst nach #20 mergen**). Kein Codex, 0 €.
Umsetzung im schaltbaren Nachschritt `relief_l3.py` (Stellen `L3c_*` in `pruefung/l3_stellen.json`). `--aus` und erneutes Einschalten sind bytegleich. Im aus-Zustand sind GB, WV und FW.h vor und nach L3c identisch.

## Ursache der „hellen Platten“ (geprüft, nicht geraten)
- **C7 und G7-Ost:** Es sind **eingeschlossene Landinseln** in der Wassermaske (WV ≤ -900 mitten im Fluss): 39 + 3 Vertices bei C7 (≈93\|280, 99\|280.5) und 5 Vertices bei G7 (≈271.5\|259.5). Der Wasserspiegel endet dort in 0,5-m-Rasterkanten, darunter liegt helles Ufergelände. Das ist keine Textur- und keine Wasserfarbe. Behebung an der Ursache: Inseln werden Wasser (WV aus der Nachbarschaft), das Bett darunter liegt 0,6 m unter dem Spiegel. Die Außenkontur bleibt gleich (Beleg unten).
- **G7 Leitern und helle Linien:** Es sind **1-Zeilen-Rillen und Stufen im Wasserspiegel WV**, mit gleichen Rillen im Bett. Der Viewer zeichnet an WV-Sprüngen über 0,9 m Schaum (helle Linie, `viewer_alle.js` fo-Term). Behebung: Rillen in WV und Bett schließen, dann glätten (wie Stelle 10 in L3b). Schaum-Vertices in G7: 83 → 1.
- **H7 Blöcke:** Ufergelände am Klippenfuß lag bis 0,37 m **unter** dem Spiegel (61 Randvertices). Der Wasserrand fiel dort auf das Gelände ab, das ergab helle Stufenblöcke. Behebung: Landufer knapp über den Spiegel heben und glätten.

## Ergebnis je Stelle (Nahbild entscheidet, selbst angesehen)

| Stelle | Maßnahme | Ergebnis | Nahbild-Paar |
|---|---|---|---|
| G7 (≈255–265\|265–276) + Ost (x 266–298) | `L3c_G7`, `L3c_G7b`: Rillen schließen, WV und Bett glätten, Insel füllen, Landufer +0,08 m | **weg**: keine Leitern, keine hellen Linien, Platte weg, Wasser durchgehend | `l3c_nahbilder/paare/G7_vorher_nachher.jpg` |
| C7 (≈88–100\|276–284) | `L3c_C7`: 2 Inseln gefüllt, Bett 0,6 m unter Spiegel, glätten | **weg**: helle Treppenplatten verschwunden | `paare/C7_vorher_nachher.jpg` |
| H7 (≈315–335\|268–280) | `L3c_H7`: Landufer heben, glätten | **teilweise**: helle Blöcke am Klippenfuß weg, Rand ruhiger. Treppenrand der Südost-Bucht bleibt → Ausnahme | `paare/H7_vorher_nachher.jpg` |
| E3 (≈186–193\|88–128) | 1 Versuch ohne Wirkung | **Ausnahme**: Bach liegt 0–5 m an bzw. unter Gasse G013 | `paare/E3_vorher_nachher.jpg` |

Paarblätter: Ton vorher \| Ton nachher \| Farbe vorher \| Farbe nachher. Die QA-Blickpunkte (N06/N07/N08/N10) sind enthalten. Einzelbilder in `l3c_nahbilder/einzel/`. Die QA-Vorlage liegt in `l3c_nahbilder/qa_p4c_vorlage.jpg`.

## Neu in relief_l3.py
- `"inseln_fuellen": true`: Ganz von Wasser umschlossene Landinseln, die vollständig im Kern der Stelle liegen (Gewicht > 0,99, ≤ 400 Vertices), werden Wasser. Zusammen mit `"bett_tiefe_m"` liegt das Bett dort unter dem Spiegel. Abbruch, falls Wasser entfernt würde oder sich die Maske außerhalb eingeschlossener Inseln ändert.
- `"land_ufer_heben_m"` / `"land_ufer_band_m"`: Landvertices am Maskenrand, die unter dem Spiegel liegen, werden knapp darüber gehoben.
- Für die alten L3/L3b-Stellen ändert sich nichts.

## Gate vorher/nachher (d5b17e2 → L3c), Details `L3c_gate_vorher_nachher.json`

| Prüfer | vorher | nachher |
|---|---:|---:|
| pruefe_regeln (export_gate) | 374 | 375 |
| pruefe_regeln mit eigenem Lochscan `/tmp/gate_loch_L3c.json` | 374 | 375 (identisch) |
| r8 | 33 | 33 |
| r9 | 325 | 325 |
| W1 / W1 alle56 | 0 / 0 | 0 / 0 |

Geändert: G5_beule_klippe 35→34, G6_facette 213→215 (2 neue, beide unsichtbar, `AUSNAHMEN_L3c.md`). Alle anderen gleich, insbesondere **R6_wasser_schnee 4→4, G8_fluss_nicht_bis_rand 1→1, R5_loch 4→4**.

## Wasser-Belege (`l3c_sha_belege.json`)
- Wasser entfernt: 0 Vertices. Neu Wasser: 47 Vertices, ausschließlich die 3 eingeschlossenen Inseln.
- Außenkontur bzw. Flussverlauf: SHA256 der Maske ohne Inseln (fill_holes) vorher = nachher `defa6d61…98c4`. Die Rohmaske ändert sich gewollt nur durch die gefüllten Inseln (`c897e44c…` → `2e8006ba…`).
- WV auf altem Wasser: 4092 Vertices geändert, max 0,895 m (Rillen und Stufen in G7/H7 geschlossen).
- Wasserfälle: keine in den Stellen. R6 und G8 unverändert, G8 bleibt der eine bekannte Treffer.

## SHA- und Schutzbelege
- D2: GB-Slab = Kachel-height_sha256 = `749d3c4b…80f6` (bitgleich).
- Unverändert: G, WEGA, wege, rampenwege, bruecken, vektor.json, felder.json, alle Prüfer.
- Wege: Kreuzungsflächen 17644 Vertices und vektor.json-Wege 19272 Vertices, je max 0,0 m. Keine Änderung innerhalb 5 m einer Rampe oder innerhalb Rand+5 m eines Weges.
- `alles.sh /tmp/l3c/p10`: siehe Abschnitt unten.

## Pipeline
`relief_l3.py` → `gen_textur.py vc` → `waende_einsetzen.py` → `html_payload_p3.py` → Gate → `alles.sh`.
