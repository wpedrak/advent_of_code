import re
from collections import namedtuple

class Interval:
    def __init__(self, left: int, right: int) -> None:
        self.left = left
        self.right = right

    def __len__(self) -> bool:
        return max(0, self.right - self.left - 1)

    def __and__(self, other) -> "Interval":
        return Interval(max(self.left, other.left), min(self.right, other.right))

    def __add__(self, delta: int) -> "Interval":
        if not isinstance(delta, int):
            raise f'Interval class supports addition of int values only, got: {delta}'
        
        return Interval(self.left + delta, self.right + delta)

    def __sub__(self, other) -> list["Interval"]:
        if other.left < self.left or other.right > self.right:
            raise f'One can only subtract interval that is fully contained in the another interval.'

        left_interval = Interval(min(self.left, other.left), max(self.left, other.left) - 1)
        right_interval = Interval(min(self.right, other.right) + 1, max(self.right, other.right))
        intervals = [left_interval, right_interval]
        return [i for i in intervals if i]
    
    def __repr__(self) -> str:
        return f'<{self.left}, {self.right}>'

class Map:
    def __init__(self, mappings: list[tuple[Interval, int]]) -> None:
        self.mappings = mappings

    def __translate_interval(self, interval: Interval) -> list[Interval]:
        intervals = [interval]
        translated_intervals = []

        for mapping_interval, delta in self.mappings:
            next_intervals = []
            for interval in intervals:
                common_part = interval & mapping_interval
                if not common_part:
                    next_intervals.append(interval)
                    continue
                
                translated_intervals.append(common_part + delta)
                next_intervals += interval - common_part

            intervals = next_intervals

        return translated_intervals + intervals


    def translate(self, intervals: list[Interval]) -> list[Interval]:
        return [
            translated_interval
            for interval in intervals
            for translated_interval in self.__translate_interval(interval)
        ]


def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]


def load_maps(lines: list[str]) -> list[Map]:
    lines = lines[2:]
    maps = []
    current_mappings = []
    for line in lines:
        if 'map' in line:  # header
            continue
        if not line:  # blank line
            maps.append(Map(current_mappings))
            current_mappings = []
            continue

        dest_start, src_start, rng = map(int, line.split())
        mapping = (Interval(src_start, src_start + rng - 1), dest_start - src_start)
        current_mappings.append(mapping)

    maps.append(Map(current_mappings))
    return maps


lines = get_lines()
seeds_input = [int(n) for n in re.findall('\d+', lines[0])]
seed_intervals = [Interval(left, left + delta - 1)
                  for left, delta in zip(seeds_input[::2], seeds_input[1::2])]
maps = load_maps(lines)

min_seed = 1 << 100  # inf
for interval in seed_intervals:
    curr_intervals = [interval]
    for m in maps:
        curr_intervals = m.translate(curr_intervals)
    
    curr_min = min(i.left for i in curr_intervals)
    min_seed = min(min_seed, curr_min)

print(min_seed)
