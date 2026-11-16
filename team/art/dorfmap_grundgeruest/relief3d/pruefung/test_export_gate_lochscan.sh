#!/bin/sh
# P11b: Test der Lochscan-Pfaduebergabe in export_gate.sh.
#  1) LOCHSCAN=<Kontrolldatei mit offen_innen=7>: pruefe_regeln.py muss genau diese Datei lesen
#     (Treffer G1_loch_offen mit wert 7 im Lauf, Gate ROT).
#  2) GATE_LOCH_JSON=<Kontrolldatei>: dasselbe ueber die neue Variable.
#  3) ohne Variable: eigener mktemp-Lochscan, G1_loch_offen 0, kein export_gate.*-Ordner bleibt liegen.
#  Immer: /tmp/gate_loch.json bleibt unberuehrt (sha256 + mtime vorher = nachher, oder fehlt vorher und nachher).
# Die vom Gate geschriebenen pruefung/*_letzter_lauf.json werden gesichert und am Ende zurueckgelegt.
set -u
cd "$(dirname "$0")/.." || exit 2
T=$(mktemp -d "${TMPDIR:-/tmp}/test_export_gate.XXXXXX") || exit 2
L="regeln r8 r9 w1 w1_alle56"
for f in $L; do cp "pruefung/${f}_letzter_lauf.json" "$T/$f.bak"; done
trap 'for f in $L; do cp "$T/$f.bak" "pruefung/${f}_letzter_lauf.json"; done; rm -rf "$T"' EXIT
trap 'exit 2' HUP INT TERM
stempel() { if [ -e /tmp/gate_loch.json ]; then echo "$(sha256sum /tmp/gate_loch.json | cut -c1-64) $(stat -c %Y.%y /tmp/gate_loch.json)"; else echo fehlt; fi; }
VOR=$(stempel); FEHLER=0
printf '{"meshes":1,"dreiecke":1,"offen_innen":7,"bb":[0,0,1,1],"punkte":[]}' > "$T/kontrolle.json"
g1() { python3 -c "import json;d=json.load(open('pruefung/regeln_letzter_lauf.json'));w=[t['wert'] for t in d['treffer'] if t['regel']=='G1_loch_offen'];print(w[0] if w else 0,d['summe'])"; }
pruefe() { # name erwartet_g1 erwartet_exit
  r=$(g1); set -- "$1" "$2" "$3" "$r"
  [ "${4%% *}" = "$2" ] && [ "$EXIT" = "$3" ] && echo "OK   $1: G1_loch_offen=${4%% *} summe=${4#* } exit=$EXIT" || { echo "FEHL $1: G1_loch_offen=${4%% *} exit=$EXIT (erwartet $2/$3)"; FEHLER=1; }
}
LOCHSCAN="$T/kontrolle.json" sh pruefung/export_gate.sh > "$T/1.log" 2>&1; EXIT=$?; pruefe "LOCHSCAN gesetzt" 7 1
env -u LOCHSCAN GATE_LOCH_JSON="$T/kontrolle.json" sh pruefung/export_gate.sh > "$T/2.log" 2>&1; EXIT=$?; pruefe "GATE_LOCH_JSON gesetzt" 7 1
ls -d "${TMPDIR:-/tmp}"/export_gate.* > "$T/vorher_tmp.txt" 2>/dev/null
env -u LOCHSCAN -u GATE_LOCH_JSON sh pruefung/export_gate.sh > "$T/3.log" 2>&1; EXIT=$?; pruefe "ohne Variable (mktemp)" 0 1
ls -d "${TMPDIR:-/tmp}"/export_gate.* > "$T/nachher_tmp.txt" 2>/dev/null
cmp -s "$T/vorher_tmp.txt" "$T/nachher_tmp.txt" && echo "OK   mktemp-Ordner aufgeraeumt" || { echo "FEHL mktemp-Ordner liegt noch"; FEHLER=1; }
NACH=$(stempel)
[ "$VOR" = "$NACH" ] && echo "OK   /tmp/gate_loch.json unberuehrt ($VOR)" || { echo "FEHL /tmp/gate_loch.json veraendert: $VOR -> $NACH"; FEHLER=1; }
grep -v "^ *#" pruefung/export_gate.sh | grep -q "/tmp/gate_loch" && { echo "FEHL fester Pfad /tmp/gate_loch.json noch in export_gate.sh"; FEHLER=1; } || echo "OK   kein fester Pfad /tmp/gate_loch.json in export_gate.sh"
[ $FEHLER = 0 ] && echo "TEST GRUEN" || { echo "TEST ROT"; exit 1; }
