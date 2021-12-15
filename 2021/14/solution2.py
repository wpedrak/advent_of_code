from collections import Counter
import itertools
import functools

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_template() -> str:
    return get_lines()[0]

def get_rules() -> dict[str, str]:
    return dict(parse_rule(l) for l in get_lines()[2:])

def parse_rule(line: str) -> tuple[str, str]:
    return line.split(' -> ')

@functools.cache
def get_count(pair: str, iterations: int) -> dict[str, int]:
    first, last = pair
    if iterations == 0:
        cnt = empty_cnt()
        cnt[first] += 1
        cnt[last] += 1
        return cnt

    middle = RULES[pair]
    left_cnt = get_count(first+middle, iterations-1)
    right_cnt = get_count(middle+last, iterations-1)
    cnt = add_cnts(left_cnt, right_cnt)
    cnt[middle] -= 1
    return cnt

def empty_cnt() -> dict[str, int]:
    return {x: 0 for x in ALL_LETTERS}

def add_cnts(cnt1: dict[str, int], cnt2: dict[str, int]) -> dict[str, int]:
    cnt = cnt1.copy()
    for l in ALL_LETTERS:
        cnt[l] += cnt2[l]
    
    return cnt

ALL_LETTERS = ['S', 'C', 'B', 'F', 'H', 'O', 'K', 'P', 'N', 'V']
RULES = get_rules()
polimer = get_template()
cnt = empty_cnt()
for a, b in itertools.pairwise(polimer):
    pair = a+b
    pair_count = get_count(pair, 40)
    cnt = add_cnts(cnt, pair_count)

for letter in polimer[1:-1]:
    cnt[letter] -= 1

all_cnts = [x for x in (sorted(cnt.values())) if x > 0]
print(all_cnts[-1] - all_cnts[0])
