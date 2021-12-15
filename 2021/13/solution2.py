def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_points() -> list[tuple[int, int]]:
    return [parse_point(l) for l in get_lines()]

def parse_point(line: str) -> tuple[int, int]:
    x, y = line.split(',')
    return int(x), int(y)

def fold(sheet: set[tuple[int, int]], fold_line: tuple[str, int]) -> None:
    direction, value = fold_line
    for point in sheet.copy():
        x, y = point
        if direction == 'x' and x < value:
            continue
        if direction == 'y' and y < value:
            continue
        sheet.remove(point)
        if direction == 'y':
            sheet.add((x, value-(y-value)))
        if direction == 'x':
            sheet.add((value-(x-value), y))

def print_sheet(sheet: set[tuple[int, int]]) -> None:
    for y in range(6):
        for x in range(40):
            mark = '#' if (x, y) in sheet else ' '
            print(mark, end='')
        print('')

points = get_points()
sheet = set(points)
fold_lines = [
    ('x', 655),
    ('y', 447),
    ('x', 327),
    ('y', 223),
    ('x', 163),
    ('y', 111),
    ('x', 81),
    ('y', 55),
    ('x', 40),
    ('y', 27),
    ('y', 13),
    ('y', 6),
]
for fold_line in fold_lines:
    fold(sheet, fold_line)

print_sheet(sheet)
