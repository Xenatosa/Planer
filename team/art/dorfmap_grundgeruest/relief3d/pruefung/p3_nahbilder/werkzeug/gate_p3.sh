#!/bin/sh
# P3-Gate = pruefung/export_gate.sh, aber eigene Lochscan-Datei (export_gate.sh nutzt fest /tmp/gate_loch.json) und eigenes NODE_PATH.
# Nutzung (aus relief3d/): sh pruefung/p3_nahbilder/werkzeug/gate_p3.sh
cd "$(dirname "$0")/../../.." || exit 2
NP=${NODE_PATH:-/workspace/.p3_node/node_modules};L=${LOCHSCAN:-/workspace/.p3_tmp/gate_loch_p3.json}
rm -f "$L"
NODE_PATH=$NP HTML=${HTML:-index.html} OUT=$L RAND=0.6 node pruefung/loch_o18g.js || echo LOCHSCAN_FEHLER
ROT=0
LOCHSCAN=$L python3 pruefung/pruefe_regeln.py relief_daten.json.gz pruefung/regeln_letzter_lauf.json || ROT=1
python3 pruefung/r8_kreuzung.py relief_daten.json.gz pruefung/r8_letzter_lauf.json || ROT=1
python3 pruefung/r9_form.py relief_daten.json.gz pruefung/r9_letzter_lauf.json || ROT=1
[ $ROT = 0 ] || { echo "GATE ROT"; exit 1; }
echo "GATE GRUEN"
