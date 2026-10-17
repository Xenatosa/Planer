#!/usr/bin/env python3
"""Prüft Budget, Referenzfaktoren und E2-Startartefakte für Ausrüstung v1.7.3."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEIGHTS = {'stat_atk_pct': 0.5, 'stat_hp_pct': 0.25, 'stat_def_pct': 0.25}
SHORT = {'stat_atk_pct': 'atk', 'stat_hp_pct': 'hp', 'stat_def_pct': 'def'}
errors = []

def read_csv(name):
    with (ROOT / name).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))

def need(condition, message):
    if not condition:
        errors.append(message)

config_rows = read_csv('game_config_ausruestung.csv')
need(all(len(row) == 3 for row in config_rows), 'Config hat nicht genau 3 Spalten je Zeile')
config = {row['key']: row['value'] for row in config_rows}
rarities = {row['gear_rarity_id']: row for row in read_csv('gear_rarities.csv')}
slots = read_csv('gear_slots.csv')
slot_map = {row['slot_id']: row for row in slots}
equipment = read_csv('equipment.csv')
sets = {row['set_id']: row for row in read_csv('gear_sets.csv')}
artifacts = read_csv('artifacts.csv')
need(len({row['equipment_id'] for row in equipment}) == len(equipment), 'Doppelte Ausrüstungs-ID')
need(len({row['artifact_id'] for row in artifacts}) == len(artifacts), 'Doppelte Artefakt-ID')
need(len([row for row in slots if row['slot_group'] != 'artifact']) == 8, 'Erwartet 8 Gear-Slots')
need(len([row for row in slots if row['slot_group'] == 'artifact']) == 2, 'Erwartet 2 Artefaktslots')
need(abs(sum(float(row['stat_budget_share_pct']) for row in slots) - 100) < 1e-9, 'Slot-Shares summieren sich nicht auf 100 %')
need(config.get('gear_main_budget_master_mult') == '1.38', 'Budget-Multiplikator Meister ist nicht 1,38')
need(config.get('gear_rarity_mult_master') == '1.38', 'Raritäts-Multiplikator Meister ist nicht 1,38')
need(rarities.get('gr_master', {}).get('stat_mult_pct') == '138', 'Raritäts-CSV Meister ist nicht 138')
need(rarities.get('gr_fine', {}).get('stat_mult_pct') == '120', 'Raritäts-CSV Geschliffen ist nicht 120')
need(config.get('e2_center_max_level') == '15', 'E2-Feuerobergrenze ist nicht 15')
need(config.get('gear_main_budget_max_level_e1') == '9', 'E1-Referenzstufe ist nicht 9')
need(config.get('gear_main_budget_max_level_e2') == '14', 'E2-Referenzstufe ist nicht 14')
need(config.get('gear_tier_ratio_max') == '1.15', 'Ratio-Deckel pro Teil ist nicht 1,15')
need(config.get('gear_class_affinity_locks') == '0', 'Klassenaffinität ist als Lock gesetzt')
need(config.get('gear_budget_excludes') == 'crit;ult_cd', 'Budgetausschlüsse stimmen nicht')
need(config.get('gear_start_artifact_1') == 'art_e1_firestone', 'E1-Startartefakt ist nicht konfiguriert')
need(config.get('gear_start_artifact_2') == 'art_e2_atk_focus', 'E2-Startartefakt ist nicht konfiguriert')

# Jede Klassen-/Slot-Zeile folgt der veröffentlichten Budgetformel.
by_class = {}
for row in equipment:
    by_class.setdefault(row['class_affinity'], []).append(row)
slot_share = {key: float(row['stat_budget_share_pct']) / 100 for key, row in slot_map.items()}
set_factor = {}
for set_id, row in sets.items():
    factor = 0.0
    for pieces in (2, 4, 6):
        for suffix in ('', '_2'):
            stat = row.get(f'bonus_{pieces}_stat{suffix}', '')
            if stat in WEIGHTS:
                factor += float(row[f'bonus_{pieces}_value{suffix}']) * WEIGHTS[stat]
    set_factor[set_id] = factor
expected_factor_e1 = float(config['ref_gear_factor_max_e1']) - 1
master_mult = float(config['gear_main_budget_master_mult'])
level_mult_e1 = 1 + float(config['gear_stat_per_level_pct']) / 100 * (int(config['gear_main_budget_max_level_e1']) - 1)
for class_id, rows in by_class.items():
    set_id = next(row['set_id'] for row in rows if row['set_id'])
    gear_share = expected_factor_e1 * 0.8
    class_scale = (gear_share - set_factor[set_id] / 100) / gear_share
    for row in rows:
        weight = WEIGHTS.get(row['main_stat_id'])
        need(weight is not None, f"Statgewicht fehlt: {row['equipment_id']}")
        expected = (expected_factor_e1 * 100 * slot_share[row['slot_id']] * class_scale / weight) / (master_mult * level_mult_e1)
        actual = float(row['main_stat_base_pct'])
        need(abs(actual - expected) <= 0.00000051, f"Hauptwert weicht von Budgetformel ab: {row['equipment_id']} ({actual} ≠ {expected})")

# E2-Artefakte haben die gesetzten Werte und den bereits eingerechneten Signaturbonus.
expected_artifacts = {
    'stat_atk_pct': (1.2095, 2.4190),
    'stat_hp_pct': (2.4190, 4.8381),
    'stat_def_pct': (2.4190, 4.8381),
}
e2_artifacts = [row for row in artifacts if row['epoch_id'] == 'epoch_2']
for stat, (l1, maximum) in expected_artifacts.items():
    matches = [row for row in e2_artifacts if row['effect_stat_id'] == stat]
    need(bool(matches), f'E2-Artefakt für {stat} fehlt')
    if matches:
        row = matches[0]
        need(abs(float(row['effect_value_l1']) - l1) < 0.000051, f"E2-Startwert falsch: {row['artifact_id']}")
        need(abs(float(row['effect_value_max']) - maximum) < 0.000051, f"E2-Maximalwert falsch: {row['artifact_id']}")
        need(row['signature_bonus_rel_pct'] == '5', f"Signaturbonus falsch: {row['artifact_id']}")
        contribution = float(row['effect_value_max']) * 1.05 * WEIGHTS[stat]
        need(contribution <= 1.270001, f"Artefakt überzieht den 10-%-Anteil: {row['artifact_id']}")

artifact_max_pp = max(float(row['effect_value_max']) * 1.05 * WEIGHTS[row['effect_stat_id']] for row in artifacts if row['effect_stat_id'] in WEIGHTS)
def full_factor(class_id, rarity_id, level, artifact_count):
    total_pct = 0.0
    active_sets = {}
    for slot in slots:
        if slot['slot_group'] == 'artifact':
            continue
        row = next(item for item in equipment if item['class_affinity'] == class_id and item['slot_id'] == slot['slot_id'] and item['gear_rarity_id'] == rarity_id)
        total_pct += float(row['main_stat_base_pct']) * float(rarities[rarity_id]['stat_mult_pct']) / 100 * (1 + float(config['gear_stat_per_level_pct']) / 100 * (level - 1)) * WEIGHTS[row['main_stat_id']]
        if row['set_id']:
            active_sets[row['set_id']] = active_sets.get(row['set_id'], 0) + 1
    for set_id, count in active_sets.items():
        row = sets[set_id]
        for pieces in (2, 4, 6):
            if count < pieces:
                continue
            for suffix in ('', '_2'):
                stat = row.get(f'bonus_{pieces}_stat{suffix}', '')
                if stat in WEIGHTS:
                    total_pct += float(row[f'bonus_{pieces}_value{suffix}']) * WEIGHTS[stat]
    total_pct += artifact_count * artifact_max_pp
    return 1 + total_pct / 100

classes = sorted(by_class)
e1_factors = [full_factor(class_id, 'gr_master', 9, 1) for class_id in classes]
e2_factors = [full_factor(class_id, 'gr_master', 14, 2) for class_id in classes]
need(max(e1_factors) <= float(config['ref_gear_factor_max_e1']) + 1e-9, 'E1-Gesamtfaktor über dem Deckel')
need(max(e2_factors) <= float(config['ref_gear_factor_max_e2']) + 1e-9, 'E2-Gesamtfaktor über dem Deckel')

ratio_limit = float(config['gear_tier_ratio_max'])
rarity_mult = {key: float(row['stat_mult_pct']) / 100 for key, row in rarities.items()}
piece_rows = {}
for row in equipment:
    if row['gear_rarity_id'] in ('gr_master', 'gr_fine'):
        piece_rows.setdefault((row['class_affinity'], row['slot_id']), {})[row['gear_rarity_id']] = row
piece_ratios = []
for (class_id, slot_id), tiers in piece_rows.items():
    master = tiers.get('gr_master')
    fine = tiers.get('gr_fine')
    need(master is not None and fine is not None, f'Meister/Geschliffen-Teil fehlt: {class_id}/{slot_id}')
    if master is None or fine is None:
        continue
    need(master['main_stat_id'] == fine['main_stat_id'], f'Hauptwert unterscheidet sich nach Rarität: {class_id}/{slot_id}')
    for level in (1, int(config['gear_main_budget_max_level_e1']), int(config['gear_main_budget_max_level_e2'])):
        level_mult = 1 + float(config['gear_stat_per_level_pct']) / 100 * (level - 1)
        master_value = float(master['main_stat_base_pct']) * rarity_mult['gr_master'] * level_mult
        fine_value = float(fine['main_stat_base_pct']) * rarity_mult['gr_fine'] * level_mult
        ratio = master_value / fine_value
        piece_ratios.append(ratio)
        need(ratio <= ratio_limit + 1e-9, f'Meister/Geschliffen-Hauptwert pro Teil über 1,15: {class_id}/{slot_id}, Stufe {level} ({ratio:.6f})')

print(f"E1 Gesamtfaktor max: {max(e1_factors):.6f} / {float(config['ref_gear_factor_max_e1']):.3f}")
print(f"E2 Gesamtfaktor max: {max(e2_factors):.6f} / {float(config['ref_gear_factor_max_e2']):.2f}")
print(f"Meister/Geschliffen-Hauptwert pro Teil max: {max(piece_ratios):.6f} / {ratio_limit:.2f}")
if errors:
    print('\n'.join('FEHLER: ' + message for message in errors))
    sys.exit(1)
print('OK: Budget-, Ratio-, Artefakt- und Konfigurationsregeln erfüllt')
