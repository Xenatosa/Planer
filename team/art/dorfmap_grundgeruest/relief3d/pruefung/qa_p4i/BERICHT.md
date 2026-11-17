# QA P4i – Nachsicht L3k / L3l / P13 / L3m (Stand 80489c5)

Kosten: 0 € extern · Codex: nein · nur Grok-Laufzeit QA-Subagent (Start 00:57 MEZ)
Prüfer und Schwellen unverändert. Viewer: neuer Viewer (`alle_kacheln.html` aus `baue_alle_kacheln.py`, FrontSide), `nosh=1`, Farbe + Ton (clay). `?silh=0` nur als Beleg. Kamera-Skript `rendere_kacheln.js` (wie P4h, ergänzt um `SILH0=1`).
Maßstab Fabian: „Wenn man es nicht sieht ist es mir egal. Aber hier geht es prinzipiell um Optik ist alles.“ Sichtbar in Farbe = Befund, nur in Farbe unsichtbar = Ausnahme.

## Ergebnis
**56 sauber / 0 leicht / 0 stark** (Maßstab Spielerdistanz 30 m, el 35°).
**Vorbehalt H2/H3 (Abschnitt 6):** Ein Kamera-Mindestabstand ist **nicht festgelegt**. Bei Nahzoom unter ~20 m sind der G3-Sägesaum (H2) und die Wegränder (H3) in Farbe sichtbar. Ohne erzwungenen Mindestabstand ≥ 25 m wären G3 und die Wegkacheln „leicht“.

## 1. Gate (selbst gelaufen, 80489c5)
| Prüfung | Ist |
|---|---|
| regeln | **359** (0 Ausnahmen) |
| R8 | **31** (21 Kreuzungen) |
| R9 | **321** |
| W1 / W1 alle 56 | **0 / 0** |
| Loch offen_innen | **0** |

Die Treffer liegen an denselben Orten wie in P4h. Nur 4 Werte sind leicht gesunken: G7b_wandkontur_feld B3 63|107 0,359→0,349, B4 63|150 0,369→0,361, C3 105|107 0,349→0,346, G7b_rauheit 0,604→0,603. Im Gebiet von L3k/L3l liegt nur der bekannte Treffer G6_facette 87,5|129,8 (6), unverändert. „GATE ROT“ (Exit 1) kam wie erwartet als Exportsperre. `w1_alle56_letzter_lauf.json` habe ich per git checkout zurückgesetzt.

## 2. Nahbilder (Koordinate mittig, 8/15/30 m, Farbe | Ton) – `bilder_80489c5/nah/`
| Ort | Urteil | Bild |
|---|---|---|
| B3 63\|107,5 | sauber | nah/B3_{8,15,30} |
| B4 63\|150,5 | sauber | nah/B4_* |
| C3 105\|107,5 | sauber | nah/C3_* |
| C4 Gratkerbe 84\|129 (L3k) | **behoben**: Kerbe weg, glatte Gratlinie in Farbe und Ton | vn/C4_kerbe_{8,15,30} (oben 42f05de, unten jetzt) |
| C4 Südflanke 82,5\|135 (L3l) | **behoben**: Sägezahn weg (vorher im Ton deutlich, in Farbe schwach) | vn/C4_suedflanke_{8,15,30} |
| C5 105\|193,5 | sauber | nah/C5_* |
| G3 273\|107,5 | sauber | nah/G3_* |
| H2 315\|64,5 / H3 315\|107,5 / H4 315\|150,5 | sauber | nah/H2_*, H3_*, H4_* |
| D3 147\|107,5 | sauber | nah/D3_* |
| E3 Ufer 188\|97,5 · 189\|104 · 189\|110 (+ quer az 90) | in Farbe sauber, Stufe nur im Ton schwach → Abschnitt 5 | nah/E3_ufer_* |

Hinweis C4: Am Ende des Nordgrats ≈87|126, über dem Fadenkreuz von vn/C4_notch_875_1298_15 bzw. _8, liegt eine kleine dunkle Facette. Sie ist **gegenüber 42f05de unverändert** (vorher/jetzt gleich), außerhalb der L3k-Änderung und entspricht dem bekannten G6-Treffer 87,5|129,8 (6). In Farbe wirkt sie wie ein Felsgrat-Ende und nicht wie ein Defekt. Deshalb ist sie kein neuer Befund; ich nenne sie nur der Vollständigkeit halber.

## 3. Alle 56 Übersichten + Pixeldiff gegen P4h (42f05de)
- Alle 56 U-Bilder habe ich einzeln angesehen (`uebersicht/U_reihe1..7.jpg`). Löcher, durchsichtige Klippen, Wasser von unten oder fehlende Flächen habe ich nicht gefunden.
- Pixeldiff U+Q1–Q4, Farbe und Ton: **alle 56 Kacheln haben Abweichungen**, weil die P13-Vorderseiten-Darstellung überall Silhouetten berührt. Mittlere Abweichung je Datei ≤ 0,57. Die größten Werte: B3 0,57, E3 0,56, C3 0,33, B4 0,22, C4 0,14, F3 0,13, E2 0,12.
- **Beleg mit `?silh=0`:** Die 56 Übersichten mit silh=0 auf denselben Daten sind z. B. bei G3 und H4 bitgleich zu P4h (Δ 0,0). Der Unterschied neu ↔ silh=0 ist also allein FrontSide. Komponentenanalyse neu ↔ silh=0 (Δ > 60, ≥ 12 px): 442 Flecken. **Alle sind im neuen Bild heller** (mittlere Helligkeitsänderung +63 … +123): Entfernt wurden dunkle Rückseiten-Punktlinien. Die 12 größten habe ich vorher/jetzt angesehen (`silh/top12_komponenten_silh0_vs_neu.jpg`): überall verschwinden gepunktete Linien, nirgends fehlt eine Fläche.
- Die dunkle Linie am Kraterrand C4 ist identisch zu P4h und silh=0 (`uebersicht/C4_U_p4h_silh0_neu.jpg`), also nicht neu.

## 4. A14 (Nähte x=84, z=43)
- Die Messwerte an den drei A14-Punkten sind unverändert: B4|C4 84|150 **0,08 m / 29,2°**, D1|D2 147|43 **0,10 / 24,0°**, 160|43 **0,05 / 15,0°**.
- Neu geprüft habe ich die Naht x=84 im Bereich von L3k/L3l (z 129–140). Die Nahtprüfung des Builds meldet 97 Paare mit max. 0,0 m, die Naht ist also geschlossen. Messung dort: zacke 0,46–1,18 m / Hang 68–78°. Das ist der Grat bzw. die Steilkante selbst und keine Nahtstufe; vor L3k waren es 0,51–0,60 m / 71–73°.
- Bild nah/naht_x84_z133 (20 m): keine Nahtlinie in Farbe und Ton. Bilder nah/naht_B4C4_x84, nah/naht_D1D2_z43_a/b: unverändert unsichtbar.
- **A14 stimmt weiter** (Ort, Messwert, Sichtbarkeit). Empfehlung: in AUSNAHMEN_FINAL nur ergänzen „x=84 bei z 129–140 durch L3k/L3l geändert, Naht dort geschlossen, Nahbild qa_p4i nah/naht_x84_z133“.

## 5. E3-Uferstufe (z 86–112)
Messung im GB-Höhenfeld (0,5-m-Raster, `stufe_e3_messung.txt`):
- Das Profil quer zum Kanal hat am Wasserrand (Spiegel −1,30 m) einen **Knick**, keine senkrechte Stufe. Oberhalb fällt das Ufer mit ≈ 0,18 m je 0,5 m (≈ 19°), an der Wasserlinie steiler.
- Größter Höhensprung je Zelle: **0,31 m auf 0,5 m = 31,9°** bei 187,5→188|97,5 (Wert aus L3m). **Median beider Ufer 0,28 m / 29,2°.** **Maximum 0,43 m / 40,4° bei 187|110 (West)**, Ost 0,39 m / 37,9° bei 191,5|111,5.
- messung.py r = 3 m: 188|97,5 **0,18 m / 29,6°**, 189|104 0,16 / 29,8°, 189|110 0,19 / 31,4°, 187|110 0,19 / 31,3°.
- Bildmessung, Senke in der Helligkeit quer zum Ufer (8 m, ±12 px): **Farbe ≤ 2,3 Graustufen** (bei 189|104 läuft die Helligkeit monoton 166→110, keine Linie), **Ton ≤ 3,3**. Im Ton zeichnet sich eine weiche Schattierungskante ab.
- Bilder: nah/E3_ufer_189_104_8 (Fadenkreuz am Ufer), vn/E3_stufe_189_104_8_ausschnitt.jpg (×2, Farbe | Ton), quer: nah/E3_ufer_188_97_quer15, E3_ufer_187_110_quer8.
- **Urteil: in Farbe aus 8, 15 und 30 m unsichtbar, nur im Ton schwach → Ausnahme.** Den Vorschlag für den Eintrag lege ich in `VORSCHLAG_AUSNAHME_E3.md` ab; AUSNAHMEN_FINAL.md habe ich dafür nicht geändert.

## 6. Nachtrag Grundgerüst: H2 / H3 (Kritiker P9) – eingetragen in AUSNAHMEN_FINAL.md als A18 / A19
**Kamera-Mindestabstand: nicht festgelegt.**
- `ANFORDERUNGEN_3D_WELTKARTE.md` Z.39 „Zoom-Grenzen … festlegen [A, offen]“, Z.73 offene Frage.
- `relief3d/neu/viewer.js` Z.101 `controls.minDistance = 2`; `pruefung/alle_kacheln/viewer_alle.js` Z.107 `minDistance = 2`; `relief3d/main.js` Z.44 `oc.minDistance=3`; `index.html` (Bundle) `minDistance=2`. `maxDistance` ist nirgends gesetzt.
- `team/gdd`: kein Treffer zu Zoom. `team/entscheidungen.md` Z.14 sagt nur „scroll-/zoombar“.

**H2 – G3-Gratsaum.** Nahbilder h2h3/H2_G3_grat_300_90_d{10,15,22,30}, h2h3/H2_G3_grat_290_98_az90_d*:
- 300|90: Fadenkreuz auf der Gratsilhouette. Bei 10 und 15 m ist die Silhouette links vom Fadenkreuz in Farbe deutlich gezackt. Bei 22 m ist sie noch leicht unruhig, bei 30 m glatt.
- 290|98 (Kamera im Osten, az 90, Blick nach Westen; der Kritiker schrieb „Blick nach Osten“, seine Kamera hat aber auch az 90): heller Saum am Grat nur bei 15–22 m, bei 30 m unauffällig.
- Messung r = 3 m: 300|90 **zacke 0,69 m / Hang max 73,5°**, 290|98 **0,49 m / 71,0°**. Zum Vergleich der glatte Grat 280|112: 0,74 / 57,7°. Die Zacke liegt auf einer Steilkante.

**H3 – Wegrand.** Nahbilder mit dem Fadenkreuz auf der Wegkante, h2h3/H3_wegrand_E3_193_119_d* und H3_wegrand_D3_1545_97_d*:
- Die Kritiker-Punkte 189|119 und 157,5|96,8 liegen neben dem Weg, deshalb habe ich die Kante aus der WEGA-Maske bestimmt: E3 Westkante 193|119, D3 Ostkante 154,5|97.
- Bei 10 m ist der Rand in Farbe gezackt (Sägeband), und das Raster im Belag ist zu sehen. Bei 15 m ist der Rand ausgefranst, bei 22–30 m weich wie ein Erdweg.
- Messung WEGA: Raster 0,5 m. Der Übergang 10→245 ist 1,75–2,0 m breit je Seite. Die Randlinie (50 %) weicht von einer glatten Kurve um **max. 0,24 m (E3) / 0,27 m (D3)** ab, Std. 0,12 / 0,15 m. Das Gelände ist flach (zacke 0,13 / 0,0 m).

**Bei beiden gilt:** sichtbar nur bei Nahzoom unter ~20 m; Empfehlung Mindestkameraabstand ≥ 25 m. **Nach Fabians Regel (sichtbare Fehler müssen weg) gilt die Ausnahme nur, wenn der Spiel-Mindestabstand ≥ 25 m wirklich erzwungen wird. Heute ist er nicht festgelegt (Viewer minDistance 2–3). Die Entscheidung liegt bei Grundgerüst/New Bot.**

## 7. Nachtrag Grundgerüst: Himmelpixel G3 U / H4 U
- Bild: `silh/himmel_G3_H4_silh0_vs_neu.jpg`. Links `?silh=0`, Mitte neu, ×4; rechts die Lage im Gesamtbild.
- **Ursache: Vorderseiten-Darstellung (P13), kein Kamera-Clipping.** Die Stellen liegen mitten in der Bildfläche an der fernen Gratsilhouette am Kartenrand (G3 U bei ≈ 650|16 px, H4 U bei ≈ 289–307|25–37 px), nicht an der Nahebene.
- Mit silh=0 sitzt dort eine dunkle gepunktete Rückseitenlinie über dem Himmel. Mit FrontSide entfällt sie, und die Silhouette endet sauber vor dem Himmel. Die betroffenen Pixel sind im neuen Bild um ≈ 30 Graustufen heller (z. B. (131,133,124) → (162,164,155)).
- Daten und Viewer sonst gleich: silh=0 ist dort bitgleich zu P4h.
- **Urteil: kein Loch, keine fehlende Fläche, aus Spielerdistanz in Farbe nicht als Fehler sichtbar. Es ist eine Verbesserung.**

## 8. Endurteil alle 56 (Pixeldiff gegen P4h: max. mittlere Abweichung je Datei / Pixel > 25 über U+Q1–Q4 Farbe+Ton; silh-Flecken = Komponenten neu↔silh=0)
| Kachel | Endurteil | Δ max / px>25 | silh-Flecken | Bemerkung |
|---|---|---|---|---|
| A1 | sauber | 0.005 / 106 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| B1 | sauber | 0.004 / 188 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| C1 | sauber | 0.003 / 172 | 1 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| D1 | sauber | 0.005 / 333 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| E1 | sauber | 0.01 / 469 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| F1 | sauber | 0.007 / 296 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| G1 | sauber | 0.005 / 185 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| H1 | sauber | 0.003 / 65 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| A2 | sauber | 0.017 / 1657 | 1 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| B2 | sauber | 0.023 / 2370 | 13 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| C2 | sauber | 0.011 / 825 | 2 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| D2 | sauber | 0.016 / 330 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| E2 | sauber | 0.12 / 934 | 2 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| F2 | sauber | 0.009 / 650 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| G2 | sauber | 0.007 / 140 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| H2 | sauber | 0.052 / 2840 | 19 | Nahbilder sauber |
| A3 | sauber | 0.021 / 1830 | 10 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| B3 | sauber | 0.57 / 8087 | 32 | L3k-Umfeld (Kachelecke 84|129) + Silhouetten; Nahbilder 8/15/30 m sauber |
| C3 | sauber | 0.329 / 8245 | 24 | L3k-Umfeld + Silhouetten; Nahbilder sauber |
| D3 | sauber | 0.048 / 1041 | 4 | Nahbilder sauber; Ufer-Saum (P13b) weg |
| E3 | sauber | 0.56 / 2369 | 7 | L3m Ufer z 86–112 hell, kein Saum in Farbe; Uferstufe nur im Ton schwach → Vorschlag Ausnahme (VORSCHLAG_AUSNAHME_E3.md) |
| F3 | sauber | 0.129 / 875 | 2 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| G3 | sauber | 0.032 / 3094 | 20 | Nahbilder sauber aus 30 m; H2-Sägesaum 300|90 nur ≤15–22 m → Ausnahme A18 (bedingt) |
| H3 | sauber | 0.024 / 3115 | 12 | Nahbilder sauber |
| A4 | sauber | 0.019 / 1963 | 19 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| B4 | sauber | 0.216 / 10498 | 55 | L3l-Umfeld + Silhouetten; Nahbilder sauber |
| C4 | sauber | 0.141 / 6030 | 18 | L3k Kerbe 84|129 weg, L3l Sägezahn Südflanke 82,5|135 weg (vn/C4_*). Grat-Ende ≈87|126 (dunkle Facette) unverändert gegenüber 42f05de, wirkt als Felsgrat |
| D4 | sauber | 0.054 / 1102 | 5 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| E4 | sauber | 0.056 / 894 | 1 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| F4 | sauber | 0.049 / 822 | 5 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| G4 | sauber | 0.021 / 1780 | 17 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| H4 | sauber | 0.027 / 2170 | 10 | Nahbilder sauber; Himmelpixel U = entfernte Rückseitenpunkte, kein Loch |
| A5 | sauber | 0.012 / 1037 | 8 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| B5 | sauber | 0.04 / 4196 | 32 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| C5 | sauber | 0.066 / 4622 | 17 | Nahbilder sauber; Kraterrand unverändert |
| D5 | sauber | 0.025 / 1486 | 4 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| E5 | sauber | 0.024 / 1825 | 7 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| F5 | sauber | 0.005 / 296 | 1 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| G5 | sauber | 0.008 / 305 | 3 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| H5 | sauber | 0.029 / 2334 | 23 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| A6 | sauber | 0.017 / 1884 | 10 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| B6 | sauber | 0.007 / 672 | 4 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| C6 | sauber | 0.006 / 514 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| D6 | sauber | 0.014 / 842 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| E6 | sauber | 0.015 / 1043 | 2 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| F6 | sauber | 0.017 / 1410 | 10 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| G6 | sauber | 0.012 / 944 | 5 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| H6 | sauber | 0.018 / 1120 | 9 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| A7 | sauber | 0.025 / 2677 | 9 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| B7 | sauber | 0.011 / 1025 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| C7 | sauber | 0.01 / 1197 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| D7 | sauber | 0.017 / 1911 | 4 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| E7 | sauber | 0.015 / 1471 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| F7 | sauber | 0.021 / 2415 | 13 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| G7 | sauber | 0.014 / 1897 | 2 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |
| H7 | sauber | 0.005 / 694 | 0 | Übersicht angesehen, nichts Neues; Änderungen nur entfernte dunkle Rückseitenpunkte an Silhouetten |

## Dateien
`punkte_p4i.json`, `punkte_zusatz.json`, `punkte_notch.json`, `punkte_h2h3.json`, `punkte_h3rand.json`, `punkte_a14.json`, `messung_p4i.json`, `messung_h2h3.json`, `stufe_e3_messung.txt`, `pixdiff.json`, `silh_komp.json`, `VORSCHLAG_AUSNAHME_E3.md`, `bilder_80489c5/` (nah, vn, h2h3, silh, uebersicht). Die Skripte sind Kopien aus qa_p4h; `rendere_kacheln.js` hat zusätzlich `SILH0=1`.

Eigene Gegenprüfung: Alle Koordinaten stammen aus zentrierten Nahbildern oder aus dem Höhenfeld bzw. der WEGA-Maske, nicht aus der Übersicht geschätzt. Die H3-Punkte des Kritikers lagen neben dem Weg; ich habe sie korrigiert (s. 6). Die C4-Facette ≈87|126 habe ich vorher/jetzt verglichen.
