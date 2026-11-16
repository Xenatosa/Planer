# ERGEBNIS L3d – E3-Westufer, G7-Nordufer (Basis art/dorfmap-fertig @ 2771f70)

Kosten: 0 € · Codex: nein · Laufzeit: 15:14–15:45

Basis: zunaechst 9742a92, nach Steuerung (P12b #29 gemergt) lokal auf **2771f70** neu angelegt (Branch war nicht gepusht, kein Force-Push).
2771f70 aendert gegenueber 9742a92 nur viewer_alle.js + P12b-Berichte; Reliefdaten identisch (relief_daten sha 76a1e583…), der L3d-Basis-Hash passt unveraendert.
Alle Gate-Werte und Nahbilder unten sind auf 2771f70 mit dem normalen (jetzt weichen) Viewer gemessen.

## Gate je Regel (vorher 2771f70 / nachher L3d)
| Regel | vorher | nachher |
|---|---|---|
| regeln gesamt | 372 | **369** |
| G6_facette | 217 | **214** (3 E3-Treffer weg: 187.5/92.6, 187.8/108.0, 186.8/120.5; kein neuer) |
| alle uebrigen Regeln (G2, G2f, G3f, G5, G7, G7b, G8, R1–R6, T1–T5) | gleich | gleich (G8 1/1, R6 4/4) |
| R8 | 31 | 31 |
| R9 | 325 | 325 |
| W1 / W1 alle 56 | 0 / 0 | 0 / 0 |
| Lochscan (offen_innen) | 0 | 0 |
Dateien: `pruefung/l3d/gate/regeln_vorher.json`, `regeln_nachher.json`. Keine neuen Treffer, keine Ausnahmen fuer Treffer noetig.

## Stellen
**E3-Westufer (x 184–195, z 86–130) – umgesetzt, Wirkung maessig.**
Die Zickzacklinie sitzt nicht nur in der VC, sondern vor allem in der Bachrinne: deren Wand folgte dem Maskenraster (Stufe bis 0,7 m) und erzeugt die dunkle Zickzackschattierung (im Ton-Render ohne Farbe sichtbar).
`relief_l3d.py` (Art „farbe“, `rinne: true`):
1. VC: Farbe quer zum Ufer ueber ein geglaettetes Abstandsfeld zur Wassermaske als Profil + geglaetteter Rest neu gesetzt (1508 Vertices, max. 22 Stufen), weich ausgeblendet an der Box (fade 3 m). Nur in der Box, wie l3c_vc_lokal (kein gen_textur-Lauf, FW.c: 0 Punkte betroffen).
2. GB: Rinne quer geglaettet (Landflaeche harmonisch ueber den Bach + Rinnenprofil ueber geglaettetem Abstand + geglaetteter Rest), Bett nie angehoben, Land nie unter naechsten Spiegel+0,05 m; danach 3 Runden Nachglaetten (σ 1 Vertex) mit erneutem Klemmen. 945 Vertices, max. 0,275 m.
   (Ohne Nachglaetten kamen 2 neue Treffer G3/G6 dazu → verworfen; mit Nachglaetten 3 G6 weniger.)
Ehrliche Bewertung: Die Uferlinie wirkt im Farb- und Ton-Bild ruhiger, die harten Zacken der dunklen Rinnenkante sind weicher; ganz weg ist die Unruhe nicht (Rinnenverlauf selbst bleibt leicht wellig). Keine Treppe, keine gerade Kante neu. Kontrollen E2 (194|63) und E4 (176|133) unveraendert.
Bilder: `l3d_nahbilder/paar_E3_west_gross.jpg`, `uebersicht_E3.jpg`, `uebersicht_E3_querschnitte.jpg`, Einzelbilder `E3_*`, `t1…t4_E3_*` je farbe/ohnew(ohne Wasser)/clay, vorher/nachher.

**G7-Nordufer westlich x≈265 – Ausnahme (zweimal gescheitert), siehe AUSNAHMEN_L3d.md.**
Im gemergten P12b-Viewer ist die Treppe zu kleinen Zacken weichgezeichnet, aber sichtbar. Beide Maskenwachstums-Versuche (0,25 m / 0,5 m ueber Spiegel; 29 / 75 neue Wasservertices) verschoben die Zacken nur. Stelle `aktiv: false`; Wassermaske bleibt bitgleich.
Bilder: `l3d_nahbilder/paar_G7_nord_gross.jpg`, `uebersicht_G7.jpg`, `G7_nord*`.

## Wassermasken-Beleg (`pruefung/l3d/l3d_abstaende.json`)
WV bitgleich, Maske bitgleich, fill_holes-Vergleich gleich, Komponenten 9 → 9, keine neuen Inseln/Luecken; Bett ueber Spiegel 525 → 523 Vertices (nicht angehoben). Flusslauf unveraendert. Lochscan 0.

## Abstaende / feste Flaechen (korrekter Massstab, zellweite_m 1,2)
Geaenderte Vertices gesamt 1556 (GB 945, VC 1508, WV 0), Box x 181,5–194,5, z 83,5–132,5.
| Flaeche | geaenderte Vertices darauf | kleinster Abstand |
|---|---|---|
| Weg (vektor.json) | 0 | 0,5 Zellen (0,6 m) |
| Kreuzung | 0 | 1,5 Zellen (1,8 m) |
| Rampenkern | 0 | 46,8 Zellen |
| WEGA/wege/Bruecken | 0 | 0,5 Zellen (0,6 m) |
| D2 | 0 | 15,5 Zellen |
D2 GB sha256 749d3c4b… vorher = nachher. Sperrzonen D1 (X084/rampe_2, Mulde 159|22,9): nicht beruehrt (≥ 65 Zellen entfernt). Skript `pruefung/l3d/l3d_abstaende.py`.

## bau_endstand.sh
Neuer Schritt 12 (nach L3c2-Schritt 11, der schon drin war): `relief_l3d.py`, `html_payload_p3.py`, `waende_einsetzen.py`; Nebenausgaben `pruefung/l3d/l3d_rueck.npz` + `l3d_bericht.json` werden mitverglichen. `L3D=0` laesst Schritt 12 weg.
Kompletter Lauf `sh bau_endstand.sh /tmp/l3d_endbau` auf Commit 0ec72f7 (Code/Daten = Lieferstand; spaetere Commits nur Berichte/Bilder): **27/27 gleich, ENDBAU BITGLEICH (399 s)**, Schritt l3d 11 s.

## Rueckweg
`python3 relief_l3d.py --aus` → relief_daten/relief_neu sha = 2771f70 (76a1e583… / 233b8373…), danach html_payload_p3.py + waende_einsetzen.py fuer index.html. Wieder anwenden → bitgleich (1b06f413… / 0b4111ac… / index 18bcc670…, rueck 23ecbb80…, bericht dc1db84b…).

## SHA Lieferstand
relief_daten.json.gz 1b06f413f38a042011e8b368b61effb87d909dea829da1a155f00a1ad531027e
neu/relief_neu.json.gz 0b4111ac996ae18121593d37cb1c50f3b063920abceb230bc654f413645e5cc5
index.html = neu/index.html 18bcc6700805689b86fe097d6908b23814e09a8f39ae9a3b877997d0c20497c7

Pruefer und Schwellen unveraendert. Nichts nach main.
