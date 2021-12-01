import itertools
from math import ceil


def find_best_equipment(weapons, armors, rings, boss):
    current_best_gold = float('inf')
    for items in items_combinations(weapons, armors, rings):
        attack = 0
        armor = 0
        gold_spent = 0

        for gold, atk, arm in items:
            attack += atk
            armor += arm
            gold_spent += gold

        if gold_spent >= current_best_gold:
            continue

        if can_win(attack, armor, boss):
            current_best_gold = gold_spent

    return current_best_gold


def items_combinations(weapons, armors, rings):
    combinations = []
    for w in weapons:
        for a in armors:
            for r1, r2 in itertools.combinations(rings, 2):
                combinations.append((w, a, r1, r2))

    return combinations


def can_win(attack, armor, boss):
    hp = 100
    boss_hp, boss_attack, boss_armor = boss

    effective_attack = max(1, attack - boss_armor)
    effective_boss_attack = max(1, boss_attack - armor)

    turns_to_kill_boss = ceil(boss_hp / effective_attack)
    turns_to_die = ceil(hp / effective_boss_attack)

    return turns_to_kill_boss <= turns_to_die


weapons = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]
armors = [
    (0, 0, 0),
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]
rings = [
    (0, 0, 0),
    (0, 0, 0),
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]

boss = (100, 8, 2)

gold_spent = find_best_equipment(weapons, armors, rings, boss)
print(gold_spent)
