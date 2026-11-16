#!/bin/sh
# Nachbildung von pruefung/export_gate.sh mit eigenen Pfaden: sh gate.sh <html> <ausgabeordner>
set -u
cd "$(dirname "$0")/../.." || exit 2
H=$1; O=$2; mkdir -p "$O"
export NODE_PATH=/tmp/w3/node_modules O17REF=${O17REF:-/tmp/p10c/o17.json.gz}
HTML=$H OUT=$O/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js > $O/loch.log 2>&1
LOCHSCAN=$O/gate_loch.json python3 pruefung/pruefe_regeln.py relief_daten.json.gz $O/regeln_letzter_lauf.json > $O/regeln.log 2>&1; echo "regeln exit $?"
python3 pruefung/r8_kreuzung.py relief_daten.json.gz $O/r8_letzter_lauf.json > $O/r8.log 2>&1; echo "r8 exit $?"
python3 pruefung/r9_form.py relief_daten.json.gz $O/r9_letzter_lauf.json > $O/r9.log 2>&1; echo "r9 exit $?"
python3 pruefung/w1_wand.py "$H" $O/w1_letzter_lauf.json > $O/w1.log 2>&1; echo "w1 exit $?"
