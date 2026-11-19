"""Minimaler glTF-2.0-Binaer-Leser/-Schreiber (nur was QA braucht, keine Abhaengigkeit ausser numpy).
Liest je Mesh-Primitive: POSITION, NORMAL, TEXCOORD_0/1/2, Indizes, Namen und extras."""
import json, struct
import numpy as np

_CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
_NK = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def lies_glb(pfad):
    raw = open(pfad, 'rb').read()
    magic, ver, laenge = struct.unpack_from('<4sII', raw, 0)
    if magic != b'glTF' or ver != 2:
        raise ValueError(f'{pfad}: kein glTF-2-GLB')
    off, js, binb = 12, None, b''
    while off < laenge:
        cl, ct = struct.unpack_from('<I4s', raw, off); off += 8
        chunk = raw[off:off + cl]; off += cl
        if ct == b'JSON': js = json.loads(chunk.decode('utf-8'))
        elif ct == b'BIN\x00': binb = chunk

    def acc(i):
        a = js['accessors'][i]; bv = js['bufferViews'][a['bufferView']]
        dt = _CT[a['componentType']]; n = _NK[a['type']]
        start = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        stride = bv.get('byteStride', 0); cnt = a['count']; isz = np.dtype(dt).itemsize * n
        if stride and stride != isz:
            buf = np.frombuffer(binb, np.uint8, count=stride * (cnt - 1) + isz, offset=start)
            arr = np.lib.stride_tricks.as_strided(buf, (cnt, isz), (stride, 1)).copy().view(dt)
        else:
            arr = np.frombuffer(binb, dt, count=cnt * n, offset=start).copy()
        return arr.reshape(cnt, n) if n > 1 else arr

    # Knoten -> Mesh (Name des Knotens, Transform nur Translation/keine; QA verlangt Weltkoordinaten)
    knotname = {}
    for nd in js.get('nodes', []):
        if 'mesh' in nd:
            if any(k in nd for k in ('matrix', 'rotation', 'scale')) or nd.get('translation', [0, 0, 0]) != [0, 0, 0]:
                raise ValueError(f'{pfad}: Knoten {nd.get("name")} hat Transform – QA erwartet Weltkoordinaten')
            knotname[nd['mesh']] = nd.get('name', '')
    prims = []
    for mi, m in enumerate(js.get('meshes', [])):
        for pi, p in enumerate(m['primitives']):
            if p.get('mode', 4) != 4:
                continue
            at = p['attributes']
            d = {'mesh': m.get('name', ''), 'knoten': knotname.get(mi, ''), 'extras': {**m.get('extras', {}), **p.get('extras', {})},
                 'pos': acc(at['POSITION']).astype(np.float64)}
            for k, key in (('normal', 'NORMAL'), ('uv0', 'TEXCOORD_0'), ('uv1', 'TEXCOORD_1'), ('uv2', 'TEXCOORD_2'), ('flaeche', '_FLAECHE')):
                if key in at: d[k] = acc(at[key]).astype(np.float64)
            d['idx'] = (acc(p['indices']).astype(np.int64).reshape(-1, 3) if 'indices' in p
                        else np.arange(len(d['pos'])).reshape(-1, 3))
            # bitgenaue Positionen (float32) fuer Q1-Nahtvergleich
            d['pos32'] = acc(at['POSITION'])
            prims.append(d)
    return js, prims


def schreibe_glb(pfad, meshes):
    """meshes: Liste {name, extras, prims:[{pos, idx, uv0?, uv1?, uv2?, normal?, extras}]} -> GLB (Weltkoordinaten)."""
    js = {'asset': {'version': '2.0', 'generator': 'dv2qa-dummy'}, 'scene': 0, 'scenes': [{'nodes': []}],
          'nodes': [], 'meshes': [], 'accessors': [], 'bufferViews': [], 'buffers': [{}]}
    blob = bytearray()

    def add(arr, typ, target=None, minmax=False):
        arr = np.ascontiguousarray(arr)
        while len(blob) % 4: blob.append(0)
        bv = {'buffer': 0, 'byteOffset': len(blob), 'byteLength': arr.nbytes}
        if target: bv['target'] = target
        blob.extend(arr.tobytes()); js['bufferViews'].append(bv)
        ct = {np.dtype(np.float32): 5126, np.dtype(np.uint32): 5125}[arr.dtype]
        a = {'bufferView': len(js['bufferViews']) - 1, 'componentType': ct, 'count': int(arr.shape[0]), 'type': typ}
        if minmax: a['min'] = arr.min(0).tolist(); a['max'] = arr.max(0).tolist()
        js['accessors'].append(a); return len(js['accessors']) - 1

    for m in meshes:
        pr = []
        for p in m['prims']:
            at = {'POSITION': add(np.asarray(p['pos'], np.float32), 'VEC3', 34962, True)}
            for k, key in (('normal', 'NORMAL'), ('uv0', 'TEXCOORD_0'), ('uv1', 'TEXCOORD_1'), ('uv2', 'TEXCOORD_2'), ('flaeche', '_FLAECHE')):
                if k in p and p[k] is not None:
                    typ = 'VEC3' if k == 'normal' else 'SCALAR' if k == 'flaeche' else 'VEC2'
                    at[key] = add(np.asarray(p[k], np.float32), typ, 34962)
            e = {'attributes': at, 'indices': add(np.asarray(p['idx'], np.uint32).reshape(-1), 'SCALAR', 34963), 'mode': 4}
            if p.get('extras'): e['extras'] = p['extras']
            pr.append(e)
        mm = {'name': m['name'], 'primitives': pr}
        if m.get('extras'): mm['extras'] = m['extras']
        js['meshes'].append(mm); js['nodes'].append({'name': m['name'], 'mesh': len(js['meshes']) - 1})
        js['scenes'][0]['nodes'].append(len(js['nodes']) - 1)
    while len(blob) % 4: blob.append(0)
    js['buffers'][0]['byteLength'] = len(blob)
    jb = json.dumps(js, separators=(',', ':')).encode()
    jb += b' ' * ((4 - len(jb) % 4) % 4)
    total = 12 + 8 + len(jb) + 8 + len(blob)
    with open(pfad, 'wb') as f:
        f.write(struct.pack('<4sII', b'glTF', 2, total)); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
        f.write(struct.pack('<I4s', len(blob), b'BIN\x00')); f.write(blob)
