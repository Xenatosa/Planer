#!/bin/sh
cd /workspace/wt_wege_p2b_v2/team/art/dorfmap_grundgeruest/relief3d || exit 2
L=/tmp/p2b2_gate_loch.json; rm -f $L
NODE_PATH=/workspace/.p3_node/node_modules HTML=index.html OUT=$L RAND=0.6 node pruefung/loch_o18g.js >/tmp/p2b_loch.log 2>&1 || echo LOCHSCAN_FEHLER
LOCHSCAN=$L python3 pruefung/pruefe_regeln.py relief_daten.json.gz pruefung/regeln_letzter_lauf.json >/tmp/p2b_r.log 2>&1
python3 pruefung/r8_kreuzung.py relief_daten.json.gz pruefung/r8_letzter_lauf.json >/tmp/p2b_r8.log 2>&1
python3 pruefung/r9_form.py relief_daten.json.gz pruefung/r9_letzter_lauf.json >/tmp/p2b_r9.log 2>&1
tail -2 /tmp/p2b_loch.log; echo fertig
cd /workspace/wt_wege_p2b_v2/team/art/dorfmap_grundgeruest/relief3d
python3 pruefung/w1_wand.py index.html pruefung/w1_letzter_lauf.json >/tmp/p2b_w1.log 2>&1
W1T=$(mktemp -d /tmp/p2b2_w1alle.XXXXXX) && python3 pruefung/alle_kacheln/baue_alle_kacheln.py --out "$W1T" --ohne-html >/dev/null 2>&1 && python3 pruefung/w1_wand.py "$W1T/alle_kacheln.json.gz" pruefung/w1_alle56_letzter_lauf.json >/tmp/p2b_w1a.log 2>&1; rm -rf "$W1T"; echo w1fertig
