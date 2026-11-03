#!/bin/sh
# Pflicht-Gate vor jedem Export/ZIP (REGELN_VERPFLICHTEND.md). Bricht ab, solange pruefe_regeln.py Treffer meldet.
# Nutzung: sh pruefung/export_gate.sh && <export/zip-Befehl>
cd "$(dirname "$0")/.." || exit 2
[ -f /tmp/gate_loch.json ] || HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js >/dev/null 2>&1
LOCHSCAN=/tmp/gate_loch.json python3 pruefung/pruefe_regeln.py relief_daten.json.gz pruefung/regeln_letzter_lauf.json || { echo "GATE ROT: kein Export/ZIP"; exit 1; }
echo "GATE GRUEN"
