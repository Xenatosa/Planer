#!/usr/bin/env python3
"""Abnahme v1.7.3: CSVs, Faktoren, Snapshot, Validate und ein Sim-Seed."""
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIM = ROOT / 'sim' / 'sim_f2p.py'
ERRORS = []

def fail(message):
    ERRORS.append(message)

# Alle CSV-Zeilen müssen spaltenrein sein.
for path in sorted(ROOT.rglob('*.csv')):
    try:
        with path.open(newline='', encoding='utf-8') as handle:
            rows = list(csv.reader(handle))
        if not rows:
            fail(f'Leere CSV: {path.relative_to(ROOT)}')
            continue
        widths = {len(row) for row in rows}
        if len(widths) != 1:
            fail(f'Spaltenzahl inkonsistent: {path.relative_to(ROOT)}')
    except (OSError, UnicodeError, csv.Error) as exc:
        fail(f'CSV nicht lesbar: {path.relative_to(ROOT)} ({exc})')

# Entfernte Alt-IDs dürfen in der Ausrüstung nicht vorkommen.
forbidden = ('slot_' + 'charm', 'cur_forge_' + 'mark', 'cost_forge_' + 'mark')
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix == '.pyc':
        continue
    if ROOT / 'sim' / 'data' in path.parents:
        continue  # GDD-Snapshots können historische IDs außerhalb des Ausrüstungsschemas enthalten.
    try:
        content = path.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        continue
    for token in forbidden:
        if token in content:
            fail(f'Entfernte Alt-ID in {path.relative_to(ROOT)}')

# GDD-Snapshot muss vollständig und unverändert zum Manifest sein.
data_dir = ROOT / 'sim' / 'data'
manifest = data_dir / 'MANIFEST.sha256'
if not manifest.is_file():
    fail('GDD-Snapshot-Manifest fehlt: sim/data/MANIFEST.sha256')
else:
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        try:
            expected, name = line.split('  ', 1)
        except ValueError:
            fail(f'Ungültige Manifestzeile: {line}')
            continue
        path = data_dir / name
        if not path.is_file():
            fail(f'GDD-Snapshot-Datei fehlt: sim/data/{name}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            fail(f'GDD-Snapshot-Hash stimmt nicht: sim/data/{name}')

# Die v1.7.3-Validate muss alle Budget-/Ratio-Prüfungen bestehen.
validation = subprocess.run([sys.executable, str(ROOT / 'validate_v1_7.py')], capture_output=True, text=True)
print(validation.stdout, end='')
if validation.stderr:
    print(validation.stderr, file=sys.stderr, end='')
if validation.returncode != 0:
    fail(f'Validate Exit-Code {validation.returncode}')

# Zufall wirkt nur auf Beschwörungen; der Standardlauf mit Seed 1 genügt.
result = subprocess.run([sys.executable, str(SIM)], capture_output=True, text=True)
ascent_day = None
if result.returncode != 0:
    fail(f'Sim Standard-Seed Exit-Code {result.returncode}: {result.stderr.strip()}')
else:
    match = re.search(r'Aufstieg \(Übergang aktiv\) Tag (\d+)', result.stdout)
    if not match:
        fail('Sim Standard-Seed: kein E2-Aufstieg binnen 21 Tagen')
    else:
        ascent_day = int(match.group(1))
        if ascent_day > 10:
            fail(f'Sim Standard-Seed: Aufstieg Tag {ascent_day} > 10')
        print(f'Aufstieg Standard-Seed 1: Tag {ascent_day}')

if ascent_day is not None:
    report = [
        'Ausrüstung v1.7.3 – F2P-Simulationsprotokoll',
        'Sim: team/ausruestung/sim/sim_f2p.py; Standardlauf, 21 Tage; Seed 1.',
        'E2-Aufstieg (Übergang aktiv):',
        f'Seed 1: Tag {ascent_day}',
        'Abnahme: Seed 1 steigt spätestens an Tag 10 auf.' if ascent_day <= 10 else 'Abnahme: Ziel nicht erreicht.',
    ]
    (ROOT / 'sim' / 'sim_seed_default.txt').write_text('\n'.join(report) + '\n', encoding='utf-8')
if ERRORS:
    print('\n'.join('FEHLER: ' + message for message in ERRORS), file=sys.stderr)
    sys.exit(1)
print('OK: CSVs spaltenrein, Snapshot-Hashes gültig, Alt-IDs fehlen, Validate Exit 0, Standard-Seed steigt bis Tag 10 auf')
