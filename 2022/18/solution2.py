def run() -> None:
    points = [parse_point(l) for l in read_lines()]
    max_dim = max((max(p[coord] for p in points) for coord in range(3)))

    grid = [[[False] * (max_dim+1) for _ in range(max_dim+1)] for _ in range(max_dim+1)]
    for x, y, z in points:
        grid[z][y][x] = True

    surface = set()
    for a in range(max_dim+1):
        for b in range(max_dim+1):
            surface.add((0, a, b))
            surface.add((a, 0, b))
            surface.add((a, b, 0))
            surface.add((max_dim, a, b))
            surface.add((a, max_dim, b))
            surface.add((a, b, max_dim))

    external_air = set()
    for surface_point in surface:
        if surface_point in external_air:
            continue
        external_air |= find_air(grid, surface_point)

    external_sides = 0
    for point in points:
        x, y, z = point
        # have side connected to external air
        external_sides += sum(n in external_air for n in find_neighbours(grid, point))
        # have side connected to end of range (thus external air)
        external_sides += sum([x == 0, y == 0, z == 0, x == max_dim, y == max_dim, z == max_dim])

    print(external_sides)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_point(line: str) -> tuple[int, int, int]:
    return tuple(int(p) for p in line.split(','))

def find_air(grid: list[list[list[bool]]], start: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    x, y, z = start
    if grid[z][y][x]:
        return set()

    to_visit = [start]
    visited = {start}

    while to_visit:
        point = to_visit.pop()

        not_visited_neighbours = [
            n for n in find_neighbours(grid, point)
            if n not in visited
            # exclude non-air neighbours
            if not grid[n[2]][n[1]][n[0]]
        ]
        to_visit += not_visited_neighbours
        visited |= set(not_visited_neighbours)

    return visited

def find_neighbours(grid: list[list[list[bool]]], point: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    x, y, z = point
    z_size = len(grid)
    y_size = len(grid[0])
    x_size = len(grid[0][0])
    return [
        (x+dx, y+dy, z+dz)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
        if abs(dx) + abs(dy) + abs(dz) == 1
        if 0 <= x+dx < x_size
        if 0 <= y+dy < y_size
        if 0 <= z+dz < z_size
    ]

run()
