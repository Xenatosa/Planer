#!/usr/bin/env python3
"""Abnahme v1.7.2: CSVs, Faktoren, Validate und Sim-Seeds 1–20."""
import csv
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
    try:
        content = path.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        continue
    for token in forbidden:
        if token in content:
            fail(f'Entfernte Alt-ID in {path.relative_to(ROOT)}')

# Die v1.7.2-Validate muss alle Budget-/Ratio-Prüfungen bestehen.
validation = subprocess.run([sys.executable, str(ROOT / 'validate_v1_7.py')], capture_output=True, text=True)
print(validation.stdout, end='')
if validation.stderr:
    print(validation.stderr, file=sys.stderr, end='')
if validation.returncode != 0:
    fail(f'Validate Exit-Code {validation.returncode}')

# Seeds 1–20; beim ersten fehlenden oder verspäteten Aufstieg scheitert die Abnahme.
ascents = []
for seed in range(1, 21):
    result = subprocess.run([sys.executable, str(SIM), str(seed), '21'], capture_output=True, text=True)
    if result.returncode != 0:
        fail(f'Sim Seed {seed} Exit-Code {result.returncode}: {result.stderr.strip()}')
        continue
    match = re.search(r'Aufstieg \(Übergang aktiv\) Tag (\d+)', result.stdout)
    if not match:
        fail(f'Sim Seed {seed}: kein E2-Aufstieg binnen 21 Tagen')
        continue
    day = int(match.group(1))
    ascents.append((seed, day))
    if day > 10:
        fail(f'Sim Seed {seed}: Aufstieg Tag {day} > 10')

if ascents:
    days = [day for _, day in ascents]
    print(f"Aufstieg Seeds 1–20: min Tag {min(days)}, max Tag {max(days)} ({len(ascents)}/20)")
    print('Einzeltage: ' + ', '.join(f'{seed}:{day}' for seed, day in ascents))
    report = [
        'Ausrüstung v1.7.2 – F2P-Simulationsprotokoll',
        'Sim: team/ausruestung/sim/sim_f2p.py; 21 Tage je Lauf; Seeds 1–20.',
        'E2-Aufstieg (Übergang aktiv) je Seed:',
        *[f'Seed {seed}: Tag {day}' for seed, day in ascents],
        f'Minimum: Tag {min(days)}; Maximum: Tag {max(days)}.',
        'Abnahme: alle 20 Seeds steigen spätestens an Tag 10 auf.' if len(ascents) == 20 and max(days) <= 10 else 'Abnahme: Ziel nicht in allen Seeds erreicht.',
    ]
    (ROOT / 'sim' / 'sim_seeds_1_20.txt').write_text('\n'.join(report) + '\n', encoding='utf-8')
if ERRORS:
    print('\n'.join('FEHLER: ' + message for message in ERRORS), file=sys.stderr)
    sys.exit(1)
print('OK: CSVs spaltenrein, Alt-IDs fehlen, Validate Exit 0, Seeds 1–20 steigen bis Tag 10 auf')
