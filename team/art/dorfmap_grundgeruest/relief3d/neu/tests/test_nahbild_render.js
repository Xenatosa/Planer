'use strict';
const assert = require('assert');
const { spawnSync } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '../..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'test-neu-render-'));
const data = path.join(tmp, 'source.json.gz');
const output = path.join(tmp, 'output');
const code = String.raw`
import gzip,json,sys
from pathlib import Path
from unittest.mock import patch
from neu.tests.helpers import make_data
from neu.nahbild import render, RENDER, ANALYZER

tmp=Path(sys.argv[1]); data=tmp/'source.json.gz'; output=tmp/'output'; html=tmp/'index.html'
make_data(data); html.write_text('<html></html>')
calls=[]
def fake_run(cmd, **kwargs):
    calls.append((cmd, kwargs))
    if cmd[1] == str(ANALYZER): Path(cmd[3]).write_text('{"images":[]}', encoding='utf-8')
with patch('neu.nahbild.subprocess.run', side_effect=fake_run):
    import os
    os.environ['NAHBILD_XVFB']='0'
    result=render(html,data,output,('D1','G1','D2'),Path('/tmp/w3/node_modules'))
cameras=json.loads((output/'kameras.json').read_text())
assert result['bilder']==36 and len(cameras)==18
assert len(calls)==3 and calls[-1][0][1]==str(ANALYZER)
assert calls[0][0][5]=='?clay=1&manual=1&nosh=1' and calls[1][0][5]=='?manual=1&nosh=1'
print(json.dumps({'test':'nahbild-render','render_calls':len(calls),'kameras':len(cameras)}))
`;
const r = spawnSync('python3', ['-c', code, tmp], { cwd: root, encoding: 'utf8' });
assert.strictEqual(r.status, 0, r.stdout + r.stderr);
process.stdout.write(r.stdout);
