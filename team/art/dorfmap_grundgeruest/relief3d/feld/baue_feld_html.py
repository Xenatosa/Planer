#!/usr/bin/env python3
"""t82u: je Rasterfeld (A1..H7, raster_def.py t1744u) eine eigenstaendige 3D-HTML (dorfmap_3d_feld_XX.html).
Geometrie: unveraenderter Viewer-Code (main.js) + unveraenderte relief_daten; Rasterdaten ausserhalb Feld+Rand+Sicherheitsabstand
werden auf 0 gesetzt (nur Dateigroesse), danach entfernt der Feldmodus alle Dreiecke/Instanzen ausserhalb Feld+Rand.
Aufruf: python3 feld/baue_feld_html.py [OUT_DIR] [FELD ...]   (Default OUT=/workspace/dorfmap_felder_3d, alle 56)
Liest nur; aendert keine Kartendateien."""
import base64,gzip,json,os,re,subprocess,sys,hashlib
import numpy as np
HIER=os.path.dirname(os.path.abspath(__file__));R3D=os.path.dirname(HIER)
NM=os.environ.get('NODE_DIR','/tmp/w3');RAND=7.0;SICHER=15
sys.path.insert(0,os.environ.get('RASTER_DIR',os.path.join(R3D,'..','pruefung','raster_t1744u')))
import raster_def as RD
OUT=sys.argv[1] if len(sys.argv)>1 else '/workspace/dorfmap_felder_3d';WAHL=set(sys.argv[2:])
os.makedirs(OUT,exist_ok=True)
def git(*a):
    try:return subprocess.run(['git','-C',R3D,*a],capture_output=True,text=True).stdout.strip()
    except Exception:return '?'
COMMIT=os.environ.get('FELD_COMMIT') or git('rev-parse','--short','HEAD')
# --- main_feld.js: Kopie von main.js mit dokumentierten Ersetzungen (jede muss genau 1x greifen) ---
src=open(os.path.join(R3D,'main.js')).read()
def ers(s,alt,neu,n=1):
    k=s.count(alt);assert k==n,(alt[:60],k);return s.replace(alt,neu)
src=ers(src,'DA=await gz(window.ALT_GZ)','DA=null')
a=src.index('{const E=f32(DA.E)');b=src.index('objekte(DA,HA,ALT,menschPos);}')+len('objekte(DA,HA,ALT,menschPos);}')
src=src[:a]+'HA=(x,z)=>0;'+src[b:]
src=ers(src,'SP={alt:spaltenLesen(DA),','SP={alt:null,')
src=ers(src,"if(/[?&]clay=1/.test(location.search)){const CL","window.__clayZ={m,fwMesh,ovMesh};if(/[?&]clay=1/.test(location.search)){const CL")
src=ers(src,"await stufe('Erstes Bild zeichnen …');","await feldModus({THREE,sc,NEU,cam,oc,HN,DN,ebSicht});await stufe('Erstes Bild zeichnen …');")
src=src.replace('location.search','window.__QS')
assert 'window.TEX' not in src,'TEX wird noch benutzt'
src="import {feldModus} from './feld/feld_modus.js';\n"+src
open(os.path.join(R3D,'_main_feld_tmp.js'),'w').write(src)
subprocess.run(f'{NM}/node_modules/.bin/esbuild _main_feld_tmp.js --bundle --minify --format=iife --outfile=/tmp/w3/bundle_feld.js',shell=True,check=True,cwd=R3D,env={**os.environ,'NODE_PATH':NM+'/node_modules'})
os.remove(os.path.join(R3D,'_main_feld_tmp.js'))
JS=open('/tmp/w3/bundle_feld.js').read()
b64=lambda by:base64.b64encode(by).decode()
# TEX (ALT-Bodentextur t36u) wird nur von der ALT-Welt benutzt, die hier entfaellt -> nicht eingebettet
RTEX=b64(open(os.path.join(R3D,'detail_textur.png'),'rb').read());WTEX=b64(open(os.path.join(R3D,'wand_textur.png'),'rb').read())
D0=json.load(gzip.open(os.path.join(R3D,'relief_daten.json.gz')))
NX,NY,RS=D0['nx'],D0['ny'],D0['rs'];GX,GY=NX*RS+1,NY*RS+1;FS=D0['FW']['fs'];FX=NX*FS+1
def ausschnitt(f):
    x0,x1,z0,z1=f['cx0'],f['cx1']+1,f['cy0'],f['cy1']+1;M=RAND+SICHER
    ca,cb,za,zb=max(0,int(x0-M)),min(NX,int(np.ceil(x1+M))),max(0,int(z0-M)),min(NY,int(np.ceil(z1+M)))
    D=json.loads(json.dumps(D0))
    if os.environ.get('FELD_VOLL'):return D,dict(name=f['feld'],x0=x0,x1=x1,z0=z0,z1=z1,rand=RAND,maske=None)  # Pruefmodus: ungekuerzte Daten
    def gitter(k,dt,ch):
        a=np.frombuffer(base64.b64decode(D[k]),dt).reshape(GY,GX,ch).copy();m=np.zeros(a.shape[:2],bool);m[za*RS:zb*RS+1,ca*RS:cb*RS+1]=True;a[~m]=0;D[k]=b64(a.tobytes())
    for k in ['G','GB']:gitter(k,np.float32,1)
    gitter('VC',np.uint8,3)  # WV+WEGA bleiben ungekuerzt: Wasser- und Wegebau wirken ueber den Ausschnitt hinaus (Pruefung H7/A1)
    zm=np.zeros((NY,NX),bool);zm[za:zb,ca:cb]=True;zf=zm.ravel()
    for c,v in D['spalten'].items():
        dt={'uint8':np.uint8,'uint16':np.uint16}.get(v['t'],np.uint32);a=np.frombuffer(base64.b64decode(v['i']),dt).copy();a[~zf]=a[zf][0] if zf.any() else 0;v['i']=b64(a.tobytes())
    W=D['FW'];band=np.frombuffer(base64.b64decode(W['band']),np.uint32);band=band[zf[band]];W['band']=b64(band.astype(np.uint32).tobytes())
    vid=np.frombuffer(base64.b64decode(W['vid']),np.uint32);fx,fy=vid%FX,vid//FX
    k=(fx>=ca*FS)&(fx<=cb*FS)&(fy>=za*FS)&(fy<=zb*FS)
    W['vid']=b64(vid[k].tobytes());W['h']=b64(np.frombuffer(base64.b64decode(W['h']),np.float32)[k].tobytes())
    for q,ch in [('c',3),('t',3),('s',1)]:W[q]=b64(np.frombuffer(base64.b64decode(W[q]),np.uint8).reshape(-1,ch)[k].tobytes())
    return D,dict(name=f['feld'],x0=x0,x1=x1,z0=z0,z1=z1,rand=RAND,maske=[ca,za,cb,zb])
CSS='''body{margin:0;overflow:hidden;font:15px sans-serif;background:#cfdbe6;touch-action:none}
#lade{position:absolute;inset:0;display:grid;place-items:center;font-size:20px;background:#dfe8ef;z-index:50;text-align:center;white-space:pre-wrap}
#lab{position:absolute;left:10px;top:6px;font:bold 64px sans-serif;color:#ffe000;text-shadow:0 0 6px #000,0 0 2px #000;pointer-events:none;z-index:5}
#ban{position:absolute;left:0;right:0;bottom:0;background:#000a;color:#fff;font:12px sans-serif;padding:4px 8px;pointer-events:none;z-index:5}
#knoepfe{position:absolute;right:8px;top:8px;display:flex;flex-direction:column;gap:8px;z-index:6}
#knoepfe button{min-width:84px;min-height:48px;font:bold 16px sans-serif;border:0;border-radius:10px;background:#fffe;box-shadow:0 1px 4px #0006}
#versteckt,#info,#modus{display:none}'''
def html(D,F):
    gzd=gzip.compress(json.dumps(D,separators=(',',':')).encode(),9,mtime=0)
    ban=f"Feld {F['name']} · x {F['x0']}–{F['x1']} m, z {F['z0']}–{F['z1']} m (+{RAND:g} m Rand, abgedunkelt) · Commit {COMMIT} · Relief t67u Runde O18 · Handy-LOD (lod=1)"
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Epodarien Dorf 3D – Feld {F['name']}</title><style>{CSS}</style></head><body>
<div id="lade">Lade Feld {F['name']} …</div><div id="lab">{F['name']}</div><div id="ban">{ban}</div>
<div id="knoepfe"><button id="bclay">Clay</button><button id="bum">Umriss</button><button id="bweg">Wege</button><button id="bstart">Start</button></div>
<div id="versteckt"><span id="modus"></span><button id="bneu"></button><button id="balt"></button><button id="reset"></button><button id="voben"></button><button id="vunten"></button><button id="vwand"></button><button id="gehen"></button>
<input type=checkbox data-l=gelaende checked><input type=checkbox data-l=baeume checked><input type=checkbox data-l=felsen checked><input type=checkbox data-l=gebaeude checked><input type=checkbox data-l=wasser checked><input type=checkbox data-l=wege checked>
<input id=az type=range min=0 max=360 value=315><input id=el type=range min=5 max=90 value=45><input id=st type=range min=0 max=150 value=90></div><div id="info"></div>
<script>window.FELD={json.dumps(F)};window.__QS=(location.search||'?')+'&lod=1';window.NEU_GZ="{b64(gzd)}";window.RTEX="data:image/png;base64,{RTEX}";window.WANDTEX="data:image/png;base64,{WTEX}";</script>
<script>{JS}</script>
<script>(function w(){{var U=window.__feldUI;if(!U)return setTimeout(w,200);var q=function(i){{return document.getElementById(i)}};
q('bclay').onclick=function(){{U.setClay(!U.clay())}};q('bum').onclick=function(){{this.style.opacity=U.umriss()?1:0.5}};q('bstart').onclick=U.start;
if(!U.hatWege)q('bweg').style.display='none';q('bweg').onclick=function(){{this.style.opacity=U.wege()?1:0.5}};if(/[?&]clay=1/.test(location.search))U.setClay(true);}})();</script></body></html>'''
idx=[]
for f in RD.felder():
    if WAHL and f['feld'] not in WAHL:continue
    D,F=ausschnitt(f);h=html(D,F);p=os.path.join(OUT,f"dorfmap_3d_feld_{f['feld']}.html");open(p,'w').write(h)
    idx.append(dict(feld=f['feld'],datei=os.path.basename(p),mb=round(len(h.encode())/1e6,2),sha256=hashlib.sha256(h.encode()).hexdigest()[:16]));print(idx[-1],flush=True)
json.dump(dict(commit=COMMIT,rand_m=RAND,felder=idx),open(os.path.join(OUT,'_bau_'+('alle' if not WAHL else '_'.join(sorted(WAHL)))+'.json'),'w'),indent=1)
