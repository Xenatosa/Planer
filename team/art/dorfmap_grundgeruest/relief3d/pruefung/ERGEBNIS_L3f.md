# ERGEBNIS L3f – Rest E3-Westufer (≈188|100 / 190|106 entlang des Ufers) – Basis art/dorfmap-L3e @ 1778473

Kosten: 0 € · Codex: nein · Laufzeit: 16:54–17:17

Basis 1778473 (baut auf #32 auf). Branch art/dorfmap-L3f (vor dem ersten Push angelegt; spaeter Rebase auf den Merge ohne Force-Push bzw. neuer Branch).
Viewer fuer alle Nahbilder: `pruefung/alle_kacheln` (P12b) auf 1778473. Kameras `l3f_nahbilder/kameras.json` (QA-Punkt notiz_E3_westufer 186|110 Abstand 20,
dazu 188|100, 188|118, 190|106 u. a.; oben = Norden).

## Kurz
**Gescheitert (4 Versuche) – keine Datenaenderung geliefert.** Die Zacke steckt **nicht in der VC**, sondern in der Geometrie der schmalen Bachrinne auf dem
Maskenraster. Ohne den Flusslauf (Maske) zu aendern oder das Bachbett so anzuheben, dass das Wasser optisch verschwindet, geht sie nicht weg.
Keine Ausnahme eingetragen (Auftrag: nach zweimaligem Scheitern nur Messwert und Nahbild melden; Fabians Vorgabe vom 16.11.: nur unsichtbare Reste auf die
Ausnahmeliste). **Entscheidung bei Grundgeruest.**

## Ursache (gemessen, `pruefung/l3f/l3f_ursache.json`)
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

## Optionen fuer Grundgeruest
1. Bachmaske E3 geglaettet zulassen (Weg A wie L3e, Maske waechst nur, ≈33 Vertices; Wasser/Flusslauf aendern sich dann am Rand).
2. Bach im Viewer anders darstellen (Rinne nicht auf Maskenvertices schattieren, z. B. Normalen im Bachband glaetten) – Viewer-Sache.
3. Lassen (Befund ist leicht, QA P4d: „Westufer leicht gezackt – nur Notiz“).

## Gate (vorher 1778473 = nachher, keine Datenaenderung)
regeln **368**, R8 31, R9 325, W1 0, W1 alle 56 0, Lochscan 0 (Vorher-Werte = L3e-Nachher-Messung derselben Daten, `pruefung/l3e/gate/*_nachher.json`).

## Abstaende / Wasser
Geaenderte Vertices: **0** (GB/WV/VC/FW bitgleich zu 1778473) → 0 auf Wegen, Kreuzungen, Rampenkernen, WEGA, D2 (D2-GB 749d3c4b unveraendert);
Sperrzonen D1 nicht beruehrt; Wasser und Flusslauf unveraendert.

## bau_endstand.sh
Echter **Schritt 14** (relief_l3f.py → html_payload_p3.py → waende_einsetzen.py; `L3F=0` schaltet ab, L3F folgt standardmaessig L3E, L3E=0 mit L3F=1 bricht ab).
Da keine Stelle aktiv ist, schreibt relief_l3f.py nichts (Log: „keine aktive Stelle, nichts geschrieben“), keine Nebenausgaben.
Volllauf `sh bau_endstand.sh /tmp/l3f_bau` auf Commit e3ccd8e: **ENDBAU BITGLEICH (519 s)**, 29/29 Ausgaben gleich, keine Warnung.

## Rueckweg
`relief_l3f.py --aus` → „L3f nicht aktiv“ (nichts zu tun); `L3F=0` laesst Schritt 14 weg. Stand = 1778473.

## SHA (unveraendert gegenueber 1778473)
| Datei | sha256 |
|---|---|
| relief_daten.json.gz | a023ec2b82a8f83be020d1a9ec601b30fa9a90b14630f608f220081617ece29f |
| neu/relief_neu.json.gz | 399fc725844b5d380e7e941e3fc22ee4e0bdaf002a7f08f4a1e9cf683efd7f7c |
| index.html = neu/index.html | 97ce8f3ca795428a7f9352b8af52b611f567a69caef0e5de78272463d513a493 |
| relief_l3f.py | 8cad019a9574cf767c35d4814895c323b47f3a49504dd3a41afabdb2d452d662 |

## Nahbilder (`pruefung/l3f_nahbilder/`)
Je Kamera `<name>_akt_{farbe,clay,ohnew}_{vorher,versuch_a..d}.jpg`; Diagnose `_diag_vc_gauss3`, `_diag_gb_gauss2`, `_diag_maske_waechst` (QA-Kameras).
Blaetter `blatt_versuche_farbe_clay.jpg`, `blatt_diagnose_vc_gb_maske.jpg`, Datenplot `vc_und_schummer_vorher_vs_versuch_b.png`. Selbst angesehen; Bewertung wie oben.
