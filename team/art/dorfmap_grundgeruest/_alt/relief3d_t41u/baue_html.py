# baut index.html: three.js-Bundle + NEU-Daten + ALT-Daten (t39u, _alt) + Texturen. Aufruf: python3 gen_relief.py && python3 baue_html.py
import base64,subprocess,os
NM=os.environ.get('NODE_DIR','/tmp/w3');A='../_alt/modell3d_t36u/'
subprocess.run(f'{NM}/node_modules/.bin/esbuild main.js --bundle --minify --format=iife --outfile=/tmp/w3/bundle_r.js',shell=True,check=True,env={**os.environ,'NODE_PATH':NM+'/node_modules'})
b=lambda p:base64.b64encode(open(p,'rb').read()).decode()
js=open('/tmp/w3/bundle_r.js').read()
html=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Epodarien Dorf – 3D-Relief t41u (Platzhalter)</title><style>body{{margin:0;overflow:hidden;font:13px sans-serif}}
#p{{position:absolute;left:8px;top:8px;background:#fffd;padding:8px;border-radius:6px;max-width:260px}}#info{{position:absolute;right:8px;top:8px;background:#fffd;padding:8px;border-radius:6px;white-space:pre;max-height:90vh;overflow:auto;font:11px monospace}}
#lade{{position:absolute;inset:0;display:grid;place-items:center;font-size:20px}}label{{display:block}}button{{margin:2px}}#modus{{font-weight:bold;color:#a00}}</style></head><body>
<div id="lade">Lade Welt …</div>
<div id="p"><b>3D-Relief (PLATZHALTER)</b><br><span id="modus"></span><br><button id="bneu">NEU</button><button id="balt">ALT</button><br>
1 Einheit = 1 m. Rot = Mensch 1,8 m.<br>
<button id="reset">Reset</button><button id="voben">Oben</button><button id="vunten">Unten</button><button id="vwand">Am Nordwand-Fuß</button><button id="gehen">Gehen an/aus</button><br>
Maus: links drehen, rechts verschieben, Rad zoomen. Gehen: Ziehen = umsehen, WASD, Shift = schnell. Klick = Info.<hr>
<label><input type=checkbox data-l=gelaende checked> Gelände</label><label><input type=checkbox data-l=baeume checked> Bäume</label>
<label><input type=checkbox data-l=felsen checked> Felsen/Findlinge</label><label><input type=checkbox data-l=gebaeude checked> Gebäude (E40)</label>
<label><input type=checkbox data-l=wasser checked> Wasser</label><label><input type=checkbox data-l=wege checked> Overlay Wege/Brücken</label><hr>
Licht Richtung <input id=az type=range min=0 max=360 value=315><br>Licht Höhe <input id=el type=range min=5 max=90 value=45><br>Licht Stärke <input id=st type=range min=0 max=150 value=80></div>
<div id="info">Klick auf die Welt …</div>
<script>window.NEU_GZ="{b('relief_daten.json.gz')}";window.ALT_GZ="{b(A+'welt3d/welt_daten.json.gz')}";window.TEX="data:image/jpeg;base64,{b(A+'textur_c20_8px.jpg')}";window.WANDTEX="data:image/png;base64,{b('wand_textur.png')}";</script><script>{js}</script></body></html>'''
open('index.html','w').write(html);print(len(html)/1e6,'MB')
