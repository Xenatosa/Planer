cd /workspace/wt_wege_p2b_v2/team/art/dorfmap_grundgeruest/relief3d
sh /tmp/p2b2_pipe.sh && sh /tmp/p2b2_gate.sh >/dev/null 2>&1
sed "s#V='/tmp/p2b2_vorher'#V='/tmp/p2c_vorher'#" /tmp/p2b2_zaehl.py > /tmp/p2c_zaehl.py; python3 /tmp/p2c_zaehl.py .
python3 - <<'P'
import json
for f in ('regeln','r8','r9'):
  a=json.load(open(f'/tmp/p2c_vorher/{f}_letzter_lauf.json'));b=json.load(open(f'pruefung/{f}_letzter_lauf.json'))
  key=lambda t:(t['regel'],json.dumps({k:v for k,v in t.items() if k not in ('wert','regel')},sort_keys=True))
  A={key(t) for t in a['treffer']};B={key(t) for t in b['treffer']}
  for t in b['treffer']:
    if key(t) not in A: print(f,'NEU',t)
  for t in a['treffer']:
    if key(t) not in B: print(f,'WEG',t)
P
python3 pruefung/p2_analyse/p2_d2hash.py; cat /tmp/p2b2_gate_loch.json; echo; python3 -c "
import json
for f in ('pruefung/w1_letzter_lauf.json','pruefung/w1_alle56_letzter_lauf.json'): print(f,json.load(open(f))['summe'])"
echo LAUF_FERTIG
