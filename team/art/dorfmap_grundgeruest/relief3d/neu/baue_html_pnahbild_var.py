"""Self-contained HTML builder for the opt-in RELIEF_NEU artifact."""
from __future__ import annotations

import base64
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("RELIEF_NEU_DIR", Path(__file__).parent / "build"))
NODE_DIR = Path(os.environ.get("NODE_DIR", "/tmp/w3"))
ALT = ROOT.parent / "_alt" / "modell3d_t36u"


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build() -> Path:
    candidate = OUT / "relief_daten_neu.json.gz"
    if not candidate.exists():
        raise FileNotFoundError(f"Kandidaten-Daten fehlen: {candidate}; zuerst RELIEF_NEU=1 python3 gen_relief.py ausfuehren")
    bundle = Path("/tmp/bundle_r_pnahbild_neu.js")
    env = {**os.environ, "NODE_PATH": str(NODE_DIR / "node_modules")}
    subprocess.run(
        [str(NODE_DIR / "node_modules" / ".bin" / "esbuild"), "main.js", "--bundle", "--minify", "--format=iife", f"--outfile={bundle}"],
        cwd=ROOT, env=env, check=True,
    )
    js = bundle.read_text(encoding="utf-8")
    html = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Epodarien Dorf – Relief NEU Prototyp pnahbild</title><style>body{{margin:0;overflow:hidden;font:13px sans-serif}}
#p{{position:absolute;left:8px;top:8px;background:#fffd;padding:8px;border-radius:6px;max-width:260px}}#info{{position:absolute;right:8px;top:8px;background:#fffd;padding:8px;border-radius:6px;white-space:pre;max-height:90vh;overflow:auto;font:11px monospace}}
#lade{{position:absolute;inset:0;display:grid;place-items:center;font-size:20px}}label{{display:block}}button{{margin:2px}}#modus{{font-weight:bold;color:#a00}}</style></head><body>
<div id="lade">Lade Welt …</div>
<div id="p"><b>3D-Relief (Prototyp pnahbild)</b><br><span id="modus"></span><br><button id="bneu">NEU</button><button id="balt">ALT</button><br>
1 Einheit = 1 m. Rot = Mensch 1,8 m.<br>
<button id="reset">Reset</button><button id="voben">Oben</button><button id="vunten">Unten</button><button id="vwand">Am Nordwand-Fuß</button><button id="gehen">Gehen an/aus</button><br>
Maus: links drehen, rechts verschieben, Rad zoomen. Gehen: Ziehen = umsehen, WASD, Shift = schnell. Klick = Info.<hr>
<label><input type=checkbox data-l=gelaende checked> Gelände</label><label><input type=checkbox data-l=baeume checked> Bäume</label>
<label><input type=checkbox data-l=felsen checked> Felsen/Findlinge</label><label><input type=checkbox data-l=gebaeude checked> Gebäude (E40)</label>
<label><input type=checkbox data-l=wasser checked> Wasser</label><label><input type=checkbox data-l=wege checked> Overlay Wege/Brücken</label><hr>
Licht Richtung <input id=az type=range min=0 max=360 value=315><br>Licht Höhe <input id=el type=range min=5 max=90 value=45><br>Licht Stärke <input id=st type=range min=0 max=150 value=90></div>
<div id="info">Klick auf die Welt …</div>
<script>window.NEU_GZ="{b64(candidate)}";window.ALT_GZ="{b64(ALT / 'welt3d' / 'welt_daten.json.gz')}";window.TEX="data:image/jpeg;base64,{b64(ALT / 'textur_c20_8px.jpg')}";window.RTEX="data:image/png;base64,{b64(ROOT / 'detail_textur.png')}";window.WANDTEX="data:image/png;base64,{b64(ROOT / 'wand_textur.png')}";</script><script>{js}</script></body></html>'''
    path = OUT / "index_neu.html"
    path.write_text(html, encoding="utf-8")
    return path


if __name__ == "__main__":
    print(f"{build()} ({(OUT / 'index_neu.html').stat().st_size / 1e6:.2f} MB)")
