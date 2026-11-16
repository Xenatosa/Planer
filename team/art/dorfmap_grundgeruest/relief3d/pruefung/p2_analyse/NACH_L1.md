# P2 nach L1 – Befehlsliste (Wege & Deko)

Voraussetzung: L1 ist fertig und von Dorfmap-Grundgerüst freigegeben. Kein Force-Push: neuer Branch statt Rebase des gepushten `wege/dorfmap-p2`.

```sh
# 0) Variablen
REPO=/workspace/handygame-plan; BASIS=origin/art/dorfmap-L1   # oder origin/art/dorfmap-fertig, falls L1 dort schon gemergt ist
WT=/workspace/wt_wege_p2_l1; NEU=wege/dorfmap-p2-l1
git -C $REPO fetch origin art/dorfmap-L1 art/dorfmap-fertig wege/dorfmap-p2

# 1) neuer Branch auf der L1-Basis, P2-Commits übernehmen (nur gen_relief.py, p2_verbinder.json, p2_d2_referenz.npz, pruefung/p2_analyse/)
git -C $REPO worktree add -b $NEU $WT $BASIS
cd $WT && git cherry-pick $(git rev-list --reverse $(git merge-base origin/wege/dorfmap-p2 origin/art/dorfmap-fertig)..origin/wege/dorfmap-p2)
#    Konflikt in gen_relief.py: L1-Änderungen behalten, P2-Blöcke (Suche "P2") wieder einsetzen.
cd team/art/dorfmap_grundgeruest/relief3d

# 2) D2-Referenz prüfen (muss 749d3c4b sein, sonst STOP und an Dorfmap-Grundgerüst melden)
python3 - <<'PY'
import json,gzip,base64,hashlib,numpy as np
D=json.load(gzip.open('relief_daten.json.gz'));G=np.frombuffer(base64.b64decode(D['GB']),np.float32).reshape(607,673)
print('D2 Basis',hashlib.sha256(np.ascontiguousarray(G[86:173,252:337]).astype('<f4').tobytes()).hexdigest())
r=np.load('p2_d2_referenz.npz');print('D2 Referenz',hashlib.sha256(r['GB'].astype('<f4').tobytes()).hexdigest())
PY

# 3) Gate VORHER auf der Basis (eigene Lochscan-Datei, nicht /tmp/gate_loch.json)
L=/tmp/p2_gate_loch.json; rm -f $L
NODE_PATH=/tmp/w3/node_modules HTML=index.html OUT=$L RAND=0.6 node pruefung/loch_o18g.js
mkdir -p /tmp/p2_vorher   # Dateinamen wie im Gate, damit trefferkarte.py --vorher sie findet
LOCHSCAN=$L python3 pruefung/pruefe_regeln.py relief_daten.json.gz /tmp/p2_vorher/regeln_letzter_lauf.json
python3 pruefung/r8_kreuzung.py relief_daten.json.gz /tmp/p2_vorher/r8_letzter_lauf.json
python3 pruefung/r9_form.py relief_daten.json.gz /tmp/p2_vorher/r9_letzter_lauf.json
cp relief_daten.json.gz /tmp/p2_vorher/relief_daten.json.gz   # für die Kantenprüfung D1|D2 in Schritt 6

# 4) neu erzeugen (ca. 80 s) und Viewer bauen. Build-Weg von index.html wie in ERGEBNIS_L1.md (Legacy vs. RELIEF_NEU=1) übernehmen.
python3 gen_relief.py > /tmp/p2_gen.log 2>&1 && grep -E "p2_d2_lock|p2_verbinder|serpentinen|rampe9_o16" /tmp/p2_gen.log
#    baue_html.py erst NACH der L1-Meldung und nur mit eigenem Bundle-Pfad (Standard /tmp/w3/bundle_r.js gehört L1):
mkdir -p /tmp/p2_w3 && BUNDLE_OUT=/tmp/p2_w3/bundle_r.js python3 baue_html.py   # liest weiter Module aus /tmp/w3/node_modules, schreibt dort nichts

# 5) Gate NACHHER (offizieller Ablauf)
rm -f /tmp/gate_loch.json; NODE_PATH=/tmp/w3/node_modules HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js && sh pruefung/export_gate.sh
#    Trefferkarte vorher/nachher (pruefung/trefferkarte/ aus art/dorfmap-fertig, ggf. vorher mergen/cherry-picken):
python3 pruefung/trefferkarte/trefferkarte.py --vorher /tmp/p2_vorher
#    Abnahme: R1_blind <= 1 und R2 <= 2 (nur X084/G2, beide Ausnahmeliste), R6 = 4 (L2), keine andere Familie höher als VORHER (je Regel UND je Kachel vergleichen).
#    Wird eine Familie schlechter: Stelle im Nahbild prüfen; zweimal gescheitert -> einfachere Geometrie oder Ausnahme, Rückmeldung an Dorfmap-Grundgerüst.

# 6) D2-Hash nachher (muss 749d3c4b... sein, Farben b67dc719...) – Befehl aus Schritt 2 ohne Referenzzeile; gen-Log: grep p2_d2_lock
#    Kante D1|D2: keine NEUEN G2/G3/G6-Treffer in Zeile z 40-46 (D1/D2-Kante) gegenüber /tmp/p2_vorher/regeln_letzter_lauf.json,
#    sonst Stelle mit Messwert + Nahbild in die Ausnahmeliste. Knickänderung an der Kante gegen Basis messen (Trockenlauf: max 1,16 mm):
python3 - <<'PY'
import json,gzip,base64,numpy as np
f=lambda p:np.frombuffer(base64.b64decode(json.load(gzip.open(p))['GB']),np.float32).reshape(607,673).astype(float)
B=f('/tmp/p2_vorher/relief_daten.json.gz');W=f('relief_daten.json.gz');z0,x0,x1=86,252,336
k=lambda G:(G[z0-1,x0:x1+1]-G[z0,x0:x1+1])-((G[z0,x0:x1+1]-G[z0+1,x0:x1+1])+(G[z0-2,x0:x1+1]-G[z0-1,x0:x1+1]))/2
print('Knick-Aenderung D1|D2 max mm',round(float(np.abs(k(W)-k(B)).max()*1000),2))
a=json.load(open('/tmp/p2_vorher/regeln_letzter_lauf.json'))['treffer'];b=json.load(open('pruefung/regeln_letzter_lauf.json'))['treffer']
s=lambda T:{(t['regel'],t['x'],t['z']) for t in T if t['regel'][:2] in('G2','G3','G6') and 40<=t['z']<=46 and 120<=t['x']<=174}
print('neue G2/G3/G6 an der Kante:',sorted(s(b)-s(a)))
PY

# 7) Commit, Push, PR (nicht mergen)
git add -A . && git commit -m "P2 Wegnetz: Rampen raus, Verbinder D2/F4/E3, Gate vorher/nachher" && git push -u origin $NEU
gh pr create --repo Xenatosa/Planer --base art/dorfmap-fertig --head $NEU --title "P2 Wegnetz: Rampen raus, Verbinder D2/F4/E3" --body-file pruefung/p2_analyse/PR_TEXT.md
#    PR_TEXT.md vorher schreiben: Fundstellen (p2_analyse.json), Gate vorher/nachher alle Familien je Kachel, D2-Hash, Ausnahmeliste (TROCKENLAUF_P2.md).
```
