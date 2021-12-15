def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_points() -> list[tuple[int, int]]:
    return [parse_point(l) for l in get_lines()]

def parse_point(line: str) -> tuple[int, int]:
    x, y = line.split(',')
    return int(x), int(y)

points = get_points()
sheet = set(points)
fold = 655
for point in sheet.copy():
    x, y = point
    if x < fold:
        continue
    sheet.remove(point)
    sheet.add((fold-(x-fold), y))

print(len(sheet))
