# Ganze-Karte-Ansicht fuer Sichtpruefung (der Relief-Neu-Viewer index.html zeigt nur D1/G1/D2): wie baue_html.py Legacy-Pfad,
# aber Bundle/Ausgabe in eigene Pfade. Aufruf aus relief3d/: RD=relief.json.gz OUT=/pfad.html python3 pruefung/p3_nahbilder/werkzeug/baue_legacy_p3.py
import base64,subprocess,os,tempfile
NM=os.environ.get('NODE_DIR','/workspace/.p3_node');A='../_alt/modell3d_t36u/'
t=tempfile.mkdtemp(prefix='p3_bundle_');bj=t+'/b.js'
subprocess.run(f'{NM}/node_modules/.bin/esbuild main.js --bundle --minify --format=iife --outfile={bj}',shell=True,check=True,env={**os.environ,'NODE_PATH':NM+'/node_modules'})
s=open('baue_html.py').read();i=s.index("html=f'''");j=s.index("'''",i+9)+3
b=lambda p:base64.b64encode(open(os.environ['RD'] if p=='relief_daten.json.gz' else p,'rb').read()).decode()
js=open(bj).read();RELIEF_NEU=False
html=eval(s[i+5:j])
open(os.environ['OUT'],'w').write(html);print(len(html)/1e6,'MB')
