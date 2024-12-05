from functools import cmp_to_key
from collections import defaultdict

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_rules() -> list[tuple[int, int]]:
    lines = read_lines()    
    return [tuple(map(int, l.split('|'))) for l in lines[:lines.index('')]]

def read_updates() -> list[list[int]]:
    lines = read_lines()    
    return [list(map(int, l.split(','))) for l in lines[lines.index('')+1:]]

def is_valid(rules: list[tuple[int, int]], update: list[int]) -> bool:
    update_dict = {value: idx for idx, value in enumerate(update)}
    return all(update_dict[before] < update_dict[after] 
               for before, after in rules 
               if before in update_dict 
               if after in update_dict)

def fix(rules: list[tuple[int, int]], update: list[int]):
    rules_dict = defaultdict(set)
    for k, v in rules:
        rules_dict[k].add(v)

    def cmp(p1: int, p2: int):
        if p1 in rules_dict[p2]:
            return 1
        if p2 in rules_dict[p1]:
            return -1
        return 0

    return sorted(update, key=cmp_to_key(cmp))

def run() -> None:
    rules = read_rules()
    updates = read_updates()

    result = sum(fix(rules, u)[len(u)//2] for u in updates if not is_valid(rules, u))

    print(result)

run()
