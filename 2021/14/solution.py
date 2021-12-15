from collections import Counter
import itertools

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_template() -> str:
    return get_lines()[0]

def get_rules() -> dict[str, str]:
    return dict(parse_rule(l) for l in get_lines()[2:])

def parse_rule(line: str) -> tuple[str, str]:
    return line.split(' -> ')

def insert(rules: dict[str, str], polimer: str) -> str:
    result = []
    for a, b in itertools.pairwise(polimer):
        result.append(a)
        result.append(rules[a+b])

    return ''.join(result) + polimer[-1]

polimer = get_template()
rules = get_rules()

for _ in range(10):
    polimer = insert(rules, polimer)

cnt = Counter(polimer)
_, max_cnt = cnt.most_common()[0]
_, min_cnt = cnt.most_common()[-1]

print(max_cnt - min_cnt)
