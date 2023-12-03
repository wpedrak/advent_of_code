import re
from collections import defaultdict

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def build_engine() -> list[str]:
    lines = get_lines()
    width = len(lines[0]) + 2
    engine = ['.' * width]
    
    for line in lines:
        engine.append('.' + line + '.')

    return engine + ['.' * width]

def neighbours(x_span: tuple[int, int], y: int) -> list[tuple[int, int]]:
    start, end = x_span
    return [(start-1, y), (end, y)] + [
        (x, y+dy)
        for x in range(start-1, end+1)
        for dy in [-1, 1]
    ]

engine = build_engine()
stars_numbers = defaultdict(list)
for y, line in enumerate(engine):
    for match in re.finditer(r'\d+', line):
        number = int(match[0])
        number_stars = [n for n in neighbours(match.span(), y) if engine[n[1]][n[0]] == '*']
        for star in number_stars:
            stars_numbers[star].append(number)

result = sum(n[0] * n[1] for n in stars_numbers.values() if len(n) == 2)
print(result)
