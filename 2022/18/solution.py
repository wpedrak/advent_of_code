def run() -> None:
    points = set()
    external_walls = 0
    for line in read_lines():
        point = parse_point(line)
        external_walls += 6
        external_walls -= 2 * len([n for n in neighbours(point) if n in points])
        points.add(point)

    print(external_walls)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_point(line: str) -> tuple[int, int, int]:
    return tuple(int(p) for p in line.split(','))

def neighbours(point: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    x, y, z = point
    return [
        (x+dx, y+dy, z+dz)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
        if abs(dx) + abs(dy) + abs(dz) == 1
    ]

run()
