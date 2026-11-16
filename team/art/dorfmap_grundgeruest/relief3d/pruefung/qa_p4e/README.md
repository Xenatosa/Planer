# QA P4e – Dorfmap Relief, Stand art/dorfmap-fertig @ bfe8dce

Dateien: `TABELLE.md` (56 Kacheln), `LISTE_SICHTBAR.md`, `LISTE_AUSNAHMEN.md`, `messung_p4e.json`, `punkte_p4e.json`, `punkte_schatten.json`, Bilder in `bilder_bfe8dce/` (vn = vorher 2771f70 / jetzt bfe8dce, schatten = Stichprobe mit Schatten, kacheln = 56 Komposite). Skripte aus qa_p4d unverändert übernommen.

## Gate (aus relief3d/)

    export NODE_PATH=/tmp/w3/node_modules
    HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js
    GATE_LOCH_JSON=/tmp/gate_loch.json sh pruefung/export_gate.sh

Ist = Soll: pruefe_regeln 367 (G6 212, G5 34, G7b_feld 29, R3_laengs 21, R1 17, G2_fein 9, R3_quer 8, R3_woelb 8, R2 8, …), Ausnahmen 0; r8 31 (21 Kreuzungen); r9 321 (R8b 18, R9 34, R9w 269); W1 0 (index) / 0 (alle 56); Lochscan offen_innen 0. „GATE ROT“ (Exit 1) ist die erwartete Exportsperre. `pruefung/w1_alle56_letzter_lauf.json` wurde vom Gate geändert und wieder zurückgesetzt.

## Bilder

    python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out /tmp/p4e     # 56 Kacheln, Naht max 0, wand_dreiecke 0
    HTML=/tmp/p4e/alle_kacheln.html DIR=/tmp/p4e/roh node pruefung/qa_p4e/rendere_kacheln.js
    python3 pruefung/qa_p4e/komposit.py /tmp/p4e/roh /tmp/p4e/komp
    PUNKTE=pruefung/qa_p4e/punkte_p4e.json HTML=/tmp/p4e/alle_kacheln.html DIR=/tmp/p4e/detail/farbe node pruefung/qa_p4e/rendere_kacheln.js   # + CLAY=1 → detail/clay
    (vorher genauso mit HTML=/tmp/p4d/alle_kacheln.html, DIR=/tmp/p4e/vorher/detail/…)
    WURZEL=/tmp/p4e STAND=bfe8dce python3 pruefung/qa_p4e/paar.py pruefung/qa_p4e/punkte_p4e.json
    WURZEL=/tmp/p4e/vorher STAND=2771f70 python3 pruefung/qa_p4e/paar.py pruefung/qa_p4e/punkte_p4e.json
    python3 pruefung/qa_p4e/vergleich.py /tmp/p4e/vorher/paar /tmp/p4e/paar /tmp/p4e/vn <namen…>
    SH=1 PUNKTE=pruefung/qa_p4e/punkte_schatten.json … node pruefung/qa_p4e/rendere_kacheln.js
    python3 pruefung/qa_p4e/messung.py pruefung/qa_p4e/punkte_p4e.json > pruefung/qa_p4e/messung_p4e.json

Der Kachelvergleich P4d → P4e lief pixelweise über die Komposite (mittlere Grauwert-Abweichung je Kachel). Die geänderten Kacheln habe ich einzeln angesehen.

Außerdem korrigiert dieser Branch qa_p4d (G7-Eintrag, siehe qa_p4d/TABELLE.md unten). PR #30 war bereits gemergt.
