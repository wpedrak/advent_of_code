import re

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

def is_neutral(engine: list[str], point: tuple[int, int]) -> bool:
    x, y = point
    val = engine[y][x]
    return val == '.' or val.isdecimal()

engine = build_engine()
result = 0
for y, line in enumerate(engine):
    for match in re.finditer(r'\d+', line):
        if all(is_neutral(engine, n) for n in neighbours(match.span(), y)):
            continue
        result += int(match[0])

print(result)
