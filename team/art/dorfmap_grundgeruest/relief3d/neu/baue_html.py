"""Build the opt-in Three.js viewer that consumes the new tiled terrain mesh."""
from __future__ import annotations

import base64
import os
from pathlib import Path
import subprocess

from .vektor import OUT, ROOT


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def run() -> None:
    data_path = OUT / "relief_neu.json.gz"
    if not data_path.exists():
        raise FileNotFoundError("neu/relief_neu.json.gz fehlt; zuerst RELIEF_NEU=1 python3 gen_relief.py ausfuehren")

    alt = ROOT.parent / "_alt" / "modell3d_t36u"
    world = alt / "welt3d" / "welt_daten.json.gz"
    texture = alt / "textur_c20_8px.jpg"
    detail_texture = ROOT / "detail_textur.png"
    wall_texture = ROOT / "wand_textur.png"
    node_dir = Path(os.environ.get("NODE_DIR", "/tmp/w3"))
    bundle = Path("/tmp/bundle_main_pgelaende.js")
    env = {**os.environ, "NODE_PATH": str(node_dir / "node_modules")}
    subprocess.run(
        [
            str(node_dir / "node_modules" / ".bin" / "esbuild"),
            "main.js", "--bundle", "--minify", "--format=iife", f"--outfile={bundle}",
        ],
        cwd=ROOT,
        env=env,
        check=True,
    )

    doc = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Epodarien Dorf – Relief-Neu Geländemesh</title><style>body{{margin:0;overflow:hidden;font:13px sans-serif}}
#p{{position:absolute;left:8px;top:8px;background:#fffd;padding:8px;border-radius:6px;max-width:260px}}#info{{position:absolute;right:8px;top:8px;background:#fffd;padding:8px;border-radius:6px;white-space:pre;max-height:90vh;overflow:auto;font:11px monospace}}
#lade{{position:absolute;inset:0;display:grid;place-items:center;font-size:20px}}label{{display:block}}button{{margin:2px}}#modus{{font-weight:bold;color:#087a36}}</style></head><body>
<div id="lade">Lade Welt …</div>
<div id="p"><b>3D-Relief – neue Geländeprofile</b><br><span id="modus"></span><br><button id="bneu">NEU</button><button id="balt">ALT</button><br>
1 Einheit = 1 m. Rot = Mensch 1,8 m.<br>
<button id="reset">Reset</button><button id="voben">Oben</button><button id="vunten">Unten</button><button id="vwand">Am Nordwand-Fuß</button><button id="gehen">Gehen an/aus</button><br>
Maus: links drehen, rechts verschieben, Rad zoomen. Gehen: Ziehen = umsehen, WASD, Shift = schnell. Klick = Info.<hr>
<label><input type=checkbox data-l=gelaende checked> Gelände</label><label><input type=checkbox data-l=baeume checked> Bäume</label>
<label><input type=checkbox data-l=felsen checked> Felsen/Findlinge</label><label><input type=checkbox data-l=gebaeude checked> Gebäude (E40)</label>
<label><input type=checkbox data-l=wasser checked> Wasser</label><label><input type=checkbox data-l=wege checked> Overlay Wege/Brücken</label><hr>
Licht Richtung <input id=az type=range min=0 max=360 value=315><br>Licht Höhe <input id=el type=range min=5 max=90 value=45><br>Licht Stärke <input id=st type=range min=0 max=150 value=90></div>
<div id="info">Klick auf die Welt …</div>
<script>window.NEU_GZ="{_b64(data_path)}";window.ALT_GZ="{_b64(world)}";window.TEX="data:image/jpeg;base64,{_b64(texture)}";window.RTEX="data:image/png;base64,{_b64(detail_texture)}";window.WANDTEX="data:image/png;base64,{_b64(wall_texture)}";</script><script>{bundle.read_text(encoding="utf-8")}</script></body></html>'''
    # The embedded Three.js bundle contains source lines with trailing spaces.
    # Normalize the generated document so repeated builds stay clean under
    # whitespace checks without changing rendered JavaScript or shaders.
    doc = "\n".join(line.rstrip() for line in doc.splitlines()) + "\n"
    output = OUT / "index.html"
    output.write_text(doc, encoding="utf-8")
    print(f"{output} ({len(doc)} Zeichen; neu_mesh_tiles eingebettet)")
