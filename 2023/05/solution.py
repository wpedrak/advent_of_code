import re
from collections import namedtuple

Rule = namedtuple('Rule', ['dest_start', 'src_start', 'range'])

class Map:
    def __init__(self, rules: list[Rule]) -> None:
        self.rules = rules

    def __getitem__(self, key: int) -> int:
        for r in self.rules:
            if r.src_start <= key < r.src_start + r.range:
                return key - r.src_start + r.dest_start
        return key

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def load_maps(lines: list[str]) -> list[Map]:
    lines = lines[2:]
    maps = []
    current_rules = []
    for line in lines:
        if 'map' in line: # header
            continue
        if not line: # blank line
            maps.append(Map(current_rules))
            current_rules = []
            continue

        dest_start, src_start, rng = map(int, line.split())
        r = Rule(dest_start, src_start, rng)
        current_rules.append(r)

    maps.append(Map(current_rules))
    return maps

lines = get_lines()
seeds = [int(n) for n in  re.findall('\d+', lines[0])]
maps = load_maps(lines)

location = 1 << 100 # inf
for seed in seeds:
    curr_location = seed
    for m in maps:
        curr_location = m[curr_location]
    location = min(location, curr_location)

print(location)
