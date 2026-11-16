# ERGEBNIS L3f – Rest E3-Westufer (≈188|100 / 190|106) + Nachtrag F7/G7-Lichtspitzen – Basis art/dorfmap-fertig @ 8c1fc80

Kosten: 0 € · Codex: nein · Laufzeit: 16:54–17:46

Branch **art/dorfmap-L3f2** = rebased auf art/dorfmap-fertig @ 8c1fc80 (nach L3e #32, P12c #33, P2d #34). art/dorfmap-L3f (b58334a) war schon gepusht und
bleibt unangetastet (kein Force-Push). Kein Konflikt in Binaerdaten: L3f liefert keine Datenaenderung; einziger Konflikt bau_endstand.sh (P2d = Schritt 14,
L3f jetzt Schritt 15). E3-Nahbilder: Viewer `pruefung/alle_kacheln` (P12b) auf 1778473 (Daten in E3 seither unveraendert ausser P2d-Bruecke Ostende). Kameras `l3f_nahbilder/kameras.json` (QA-Punkt notiz_E3_westufer 186|110 Abstand 20,
dazu 188|100, 188|118, 190|106 u. a.; oben = Norden).

## Kurz
**Gescheitert (4 Versuche) – keine Datenaenderung geliefert.** Die Zacke steckt **nicht in der VC**, sondern in der Geometrie der schmalen Bachrinne auf dem
Maskenraster. Ohne den Flusslauf (Maske) zu aendern oder das Bachbett so anzuheben, dass das Wasser optisch verschwindet, geht sie nicht weg.
Keine Ausnahme eingetragen (Auftrag: nach zweimaligem Scheitern nur Messwert und Nahbild melden; Fabians Vorgabe vom 16.11.: nur unsichtbare Reste auf die
Ausnahmeliste). **Entscheidung bei Grundgeruest.**

## E3 – Ursache (gemessen, `pruefung/l3f/l3f_ursache.json`)
- **VC ist dort glatt** (seit L3d): die Gradientenlinien der Farbe laufen als glatte Kurven, keine Zellstufen (`l3f_nahbilder/vc_und_schummer_vorher_vs_versuch_b.png`, Spalten 1–2).
- **Test VC Gauss 3** (ganze Box stark weichgezeichnet): Zickzacklinie bleibt unveraendert (`*_diag_vc_gauss3.jpg`, `blatt_diagnose_vc_gb_maske.jpg` Spalte 2).
- **Test GB Gauss 2**: Linie weg, aber das Bett wird dabei angehoben und der Bach ist fast unsichtbar (`*_diag_gb_gauss2.jpg`, Spalte 3).
- Also: Schattierung der Bachrinne. Der Bach ist 1–8 Wasservertices breit (Median 4), das Bett liegt ≈0,35 m unter dem Spiegel genau auf den Maskenvertices,
  das Ufer-Land daneben ≈0,05–0,1 m ueber dem Spiegel (Sprung ≈0,4 m auf einen Vertex). Rinnenachse und Boeschungsknick folgen dem 0,5-Zellen-Raster der Maske
  (Achse weicht bis 0,41 Zellen von ihrer geglaetteten Linie ab, Mittel 0,11). Die Facetten dieses Knicks geben auf dem dunklen Bett-VC die dunkle Zacke
  (Schummerung, Spalte 3 im PNG: helle Treppe genau auf der Maskenkante). Es gibt keine VC-Schwelle oder Zellklassen-Mischmaske, an der man ansetzen koennte.

## Versuche (Nahbilder `blatt_versuche_farbe_clay.jpg`: Spalten vorher | a | b | c | d, je Farbe und Clay)
| Versuch | Verfahren | Ergebnis | Gate |
|---|---|---|---|
| a | GB im Uferband (|Abstand| ≤ 6 V.) weich zum Gauss-GB gemischt (Abstandsfeld, Box-Fade, fester Abstand zu Wegen), Bett bis Spiegel−5 mm anhebbar | Zacke weg, **aber Bach optisch weg** (Bett flach, Wasser fast durchsichtig) | 367 |
| b | wie a, Bett nie angehoben | Zacke unveraendert | 372 (4 neue G6 in E3) |
| c | L3e-Profil (Art ufer) ohne Maskenwachstum | Bach schmaler und heller, Zacke staerker | 373 |
| d | wie a, Bett hoechstens bis 0,35 m unter Spiegel | Wasser bleibt, Zacke nur minimal weicher | 372 (5 neue G6, 1 weg) |
Alle Versuche sind in `pruefung/l3f/l3f_stellen.json` mit `"aktiv": false` und Ergebnis dokumentiert, `relief_l3f.py` enthaelt die Verfahren (Code-Stand d).
**Diagnose ausserhalb des Auftrags** (nicht geliefert, verletzt „Flusslauf unveraendert“): L3e-Art „ufer“ mit Maskenwachstum (33 neue Wasservertices) macht
die Linie deutlich ruhiger (`*_diag_maske_waechst.jpg`, Spalte 4) – das waere der Weg, wenn Grundgeruest eine glatte Bachmaske erlaubt.

## Optionen fuer Grundgeruest (E3)
1. Bachmaske E3 geglaettet zulassen (Weg A wie L3e, Maske waechst nur, ≈33 Vertices; Wasser/Flusslauf aendern sich dann am Rand).
2. Bach im Viewer anders darstellen (Rinne nicht auf Maskenvertices schattieren, z. B. Normalen im Bachband glaetten) – Viewer-Sache.
3. Lassen (Befund ist leicht, QA P4d: „Westufer leicht gezackt – nur Notiz“).


## Nachtrag F7/G7 – Lichtspitzen (≈246|279) – gescheitert (2 Versuche), keine Ausnahme
Kamera wie Dev UI P12c `F7G7sued_distanz` (246|276, Azimut 180, Abstand 60, Neigung 45), Viewer = P12c (normaler Viewer seit cffe940).
- **Ort:** Die 4–5 hellen Spitzen sitzen am **kameranahen Ufer = Nordufer ≈240–252|265–271**, nicht am Suedufer 246|279 (Kamera schaut von Norden;
  Differenzbild Versuch 1 zeigt die Aenderung am fernen Suedufer, die Spitzen bleiben).
- **Messwert** (`pruefung/l3f/fg7_messung.json`): sichtbar in Farbe, Clay, ohne Schatten, ohne Waende, ohne Wege – **nicht** ohne Wasser → Wasseroberflaeche,
  nicht Gelaende/Landecken. Spiegelhoehen WV am Nordufer: Randring der Wasser-Vertices im Mittel **−18,69 m gegen −18,26 m innen (0,43 m tiefer)**,
  treppenfoermig auf dem Maskenraster (z. B. Zeile z 270: −18,82 | −18,38 nebeneinander). Die geglaettete Oberflaeche (WR, Klemme WV−0,6…+0,3) knickt dort
  in Zacken → helle Spitzen. Das liegt in WV auf **altem Wasser**, das laut Auftrag unveraendert bleibt.
- **Versuch 1** (`FG7_sued`, Art ufer wie L3e + Treppenecken fuellen, 88 neue Wasser-Vertices, kein Wasser entfernt, Komponenten 9→9): Spitzen unveraendert.
- **Versuch 2** (`FG7_nord`, dasselbe am Nordufer 236–256|261–272,5, 58 neue Wasser-Vertices): Uferlinie wandert, **Spitzen bleiben ortsfest** im Wasser,
  dazu neue dunkle Kruemel an der Kante → schlechter. Beide in `l3f_stellen.json` mit `"aktiv": false` + Ergebnis; Code (Art „ufer“, `ecken_fuellen`) bleibt inaktiv.
- Nahbild: `pruefung/l3f_nahbilder/fg7/blatt_fg7_lichtspitzen.jpg` (vorher | Versuch 1 | Versuch 2 | vorher Clay | ohne Wasser), Einzelbilder `fg7/FG_*.png`.
- **Optionen fuer Grundgeruest:** (1) WV-Randring am Nordufer 240–256|262–272 auf den Innenspiegel anheben (Wasserdaten, braucht Freigabe);
  (2) Viewer: WR-Glaettung am Rand ohne Treppe (Dev UI); (3) lassen.

## Gate (Endstand art/dorfmap-L3f2 auf 8c1fc80, keine Datenaenderung)
regeln **368**, R8 **31**, R9 **325**, W1 **0**, W1 alle 56 0, Lochscan **0** (offen_innen 0). Treffer identisch zu 8c1fc80
(`regeln_letzter_lauf.json` byte-gleich zur P2d-Datei auf dem Kopf; Laufergebnisse in `pruefung/l3f/gate/`).

## Abstaende / Wasser
Geaenderte Vertices: **0** (GB/WV/VC/FW bitgleich zu 8c1fc80, beide Stellen-Gruppen inaktiv) → 0 auf Wegen, Kreuzungen, Rampenkernen, WEGA, D2 (D2-GB 749d3c4b unveraendert);
Sperrzonen D1 nicht beruehrt; Wasser und Flusslauf unveraendert.

## bau_endstand.sh
Echter **Schritt 15** nach P2d-Schritt 14 (relief_l3f.py → html_payload_p3.py → waende_einsetzen.py; `L3F=0` schaltet ab, L3F folgt standardmaessig P2D,
P2D=0 mit L3F=1 bricht ab). Da keine Stelle aktiv ist, schreibt relief_l3f.py nichts (Log 15_l3f: „keine aktive Stelle, nichts geschrieben“), keine Nebenausgaben.
Volllauf `sh bau_endstand.sh /tmp/l3f_bau3` auf dem rebasten Stand (c6dd64f): **ENDBAU BITGLEICH (515 s)**, 31/31 Ausgaben gleich.

## Rueckweg
`relief_l3f.py --aus` (mit `l3f_rueck.npz`, bei den Versuchen benutzt und jeweils auf den Basis-sha zurueckgekehrt); jetzt nichts zu tun. `L3F=0` laesst Schritt 15 weg. Stand = 8c1fc80.

## SHA (unveraendert gegenueber 8c1fc80)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | 98a6c8c4582b8c206550fc7b26b8af95c6940ca7b9cade43ab8a45a94df8a1eb |
| neu/relief_neu.json.gz | 275ee752dbee3099774b78fd568ab7eaf6f15891d4238d99a1173ffb7e8f9135 |
| index.html = neu/index.html | 9b36295720313dc06f9cdd7eac4dc3d19567fc9b601069551e1d5262f545872c |
| relief_l3f.py | ded432b0be24aec1afe912f371963d46f88cda5275f4f17090b4c89e26d7d364 |
| bau_endstand.sh | 2e9a114dea71b66ac14eb74603099beddf78f0013c6fe2a72f951e0b8783f272 |

## Nahbilder (`pruefung/l3f_nahbilder/`)
Je Kamera `<name>_akt_{farbe,clay,ohnew}_{vorher,versuch_a..d}.jpg`; Diagnose `_diag_vc_gauss3`, `_diag_gb_gauss2`, `_diag_maske_waechst` (QA-Kameras).
Blaetter `blatt_versuche_farbe_clay.jpg`, `blatt_diagnose_vc_gb_maske.jpg`, Datenplot `vc_und_schummer_vorher_vs_versuch_b.png`. Selbst angesehen; Bewertung wie oben.
Nachtrag: `fg7/` (siehe oben). Endstand 8c1fc80+L3f: `blatt_endstand_8c1fc80.jpg` + `endstand/END_*_{farbe,clay}.png` (F7/G7 Distanz, E3 Distanz, E3 West nah) –
angesehen: unveraendert zum Kopf, E3-Zacke und F7/G7-Spitzen weiter sichtbar (ehrlich: L3f bringt keine sichtbare Verbesserung).
