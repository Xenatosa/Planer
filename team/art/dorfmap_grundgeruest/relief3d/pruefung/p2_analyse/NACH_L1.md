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
LOCHSCAN=$L python3 pruefung/pruefe_regeln.py relief_daten.json.gz /tmp/p2_vorher_regeln.json
python3 pruefung/r8_kreuzung.py relief_daten.json.gz /tmp/p2_vorher_r8.json
python3 pruefung/r9_form.py relief_daten.json.gz /tmp/p2_vorher_r9.json
git checkout -- pruefung/   # falls die Prüfer dort etwas überschrieben haben

# 4) neu erzeugen (ca. 80 s) und Viewer bauen. Build-Weg von index.html wie in ERGEBNIS_L1.md (Legacy vs. RELIEF_NEU=1) übernehmen.
python3 gen_relief.py > /tmp/p2_gen.log 2>&1 && grep -E "p2_d2_lock|p2_verbinder|serpentinen|rampe9_o16" /tmp/p2_gen.log
python3 baue_html.py      # schreibt /tmp/w3/bundle_r.js (geteilt!) + index.html

# 5) Gate NACHHER (offizieller Ablauf)
rm -f /tmp/gate_loch.json; NODE_PATH=/tmp/w3/node_modules HTML=index.html OUT=/tmp/gate_loch.json RAND=0.6 node pruefung/loch_o18g.js && sh pruefung/export_gate.sh
#    Abnahme: R1_blind <= 1 und R2 <= 2 (nur X084/G2, beide Ausnahmeliste), R6 = 4 (L2), keine andere Familie höher als VORHER (je Regel UND je Kachel vergleichen).
#    Wird eine Familie schlechter: Stelle im Nahbild prüfen; zweimal gescheitert -> einfachere Geometrie oder Ausnahme, Rückmeldung an Dorfmap-Grundgerüst.

# 6) D2-Hash nachher (muss 749d3c4b... sein) – Befehl aus Schritt 2 ohne Referenzzeile

# 7) Commit, Push, PR (nicht mergen)
git add -A . && git commit -m "P2 Wegnetz: Rampen raus, Verbinder D2/F4/E3, Gate vorher/nachher" && git push -u origin $NEU
gh pr create --repo Xenatosa/Planer --base art/dorfmap-fertig --head $NEU --title "P2 Wegnetz: Rampen raus, Verbinder D2/F4/E3" --body-file pruefung/p2_analyse/PR_TEXT.md
#    PR_TEXT.md vorher schreiben: Fundstellen (p2_analyse.json), Gate vorher/nachher alle Familien je Kachel, D2-Hash, Ausnahmeliste (TROCKENLAUF_P2.md).
```
