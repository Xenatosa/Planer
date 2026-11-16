set -e
cd /workspace/wt_wege_p2b_v2/team/art/dorfmap_grundgeruest/relief3d
git checkout d5b17e2 -- relief_daten.json.gz neu/relief_neu.json.gz index.html neu/index.html
python3 relief_p2b.py > /tmp/p2b_apply.log
python3 pruefung/p2_analyse/p2b/p2b_bruecken.py
python3 gen_textur.py vc | tail -1
python3 pruefung/p2_analyse/p2b/p2b_vc_lokal.py /tmp/p2b2_vorher/relief_daten.json.gz /tmp/p2b2_vorher/relief_neu.json.gz
python3 pruefung/p2_analyse/p2b/p2b_r5_textur.py
python3 pruefung/p3_nahbilder/werkzeug/html_payload_p3.py > /dev/null
python3 pruefung/p10c/waende_einsetzen.py > /dev/null
