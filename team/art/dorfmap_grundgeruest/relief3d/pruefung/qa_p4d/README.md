# QA P4d – Dorfmap Relief, Stand art/dorfmap-fertig @ 2771f70

Dateien: `TABELLE.md` (56 Kacheln), `LISTE_SICHTBAR.md`, `LISTE_AUSNAHMEN.md`, `messung_p4d.json`, Bilder in `bilder_2771f70/` (vn = vorher P4c 8cd6d37 / jetzt, nah = neue Funde, schatten = Stichprobe mit Schatten, kacheln = 56 Komposite).

## Gate (aus relief3d/)

    export NODE_PATH=/tmp/w3/node_modules
    HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js
    GATE_LOCH_JSON=/tmp/gate_loch.json sh pruefung/export_gate.sh

Ist = Soll: pruefe_regeln 372 (G6 217, G5 34, G7b_feld 29, R3_laengs 21, R1 17, G2_fein 9, R3_quer 8, R3_woelb 8, R2 8, …), Ausnahmen 0; r8 31 (21 Kreuzungen); r9 325; W1 0 (index) / 0 (alle 56); Lochscan offen_innen 0. Ausgabe „GATE ROT“ (Exit 1) = Exportsperre wegen Gesamttreffern > 0, erwartet. `pruefung/w1_alle56_letzter_lauf.json` wird vom Gate geändert und wurde zurückgesetzt.

## Bilder

index.html enthält nur D1, D2, G1 → Vollansicht:

    python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p4d      # 56 Kacheln, Naht max 0, wand_dreiecke 0
    NODE_PATH=… HTML=/tmp/p4d/alle_kacheln.html DIR=/tmp/p4d/roh node pruefung/qa_p4d/rendere_kacheln.js
    python3 pruefung/qa_p4d/komposit.py /tmp/p4d/roh /tmp/p4d/komp
    PUNKTE=pruefung/qa_p4d/punkte_p4d.json HTML=/tmp/p4d/alle_kacheln.html DIR=/tmp/p4d/detail/farbe node pruefung/qa_p4d/rendere_kacheln.js
    CLAY=1 PUNKTE=… DIR=/tmp/p4d/detail/clay node pruefung/qa_p4d/rendere_kacheln.js
    WURZEL=/tmp/p4d STAND=2771f70 python3 pruefung/qa_p4d/paar.py pruefung/qa_p4d/punkte_p4d.json
    python3 pruefung/qa_p4d/vergleich.py /tmp/p4d/vorher/paar /tmp/p4d/paar /tmp/p4d/vn <namen…>
    SH=1 PUNKTE=pruefung/qa_p4d/punkte_schatten.json … node pruefung/qa_p4d/rendere_kacheln.js   # Schatten-Stichprobe
    python3 pruefung/qa_p4d/messung.py pruefung/qa_p4d/punkte_p4d.json > pruefung/qa_p4d/messung_p4d.json

Vorher-Bilder mit dem P4c-Viewer (8cd6d37) aus denselben Punkten. Neue Funde: `punkte_neu_funde.json`.
Änderung an rendere_kacheln.js gegenüber P4c: `SH=1` rendert mit Schatten (ohne nosh=1).
