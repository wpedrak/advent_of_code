from collections import defaultdict

ACTIVE = '#'
INACTIVE = '.'


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_grid():
    grid = defaultdict(lambda: INACTIVE)
    for y, row in enumerate(get_lines()):
        for x, value in enumerate(row):
            grid[(x, y, 0, 0)] = value

    return grid


def count_active(grid):
    return sum(map(
        lambda x: x == ACTIVE,
        grid.values()
    ))


def get_neighbours(coordinates):
    x, y, z, w = coordinates
    deltas = [(dx, dy, dz, dw) for dx in range(-1, 2) for dy in range(-1, 2) for dz in range(-1, 2) for dw in range(-1, 2) if (dx, dy, dz, dw) != (0, 0, 0, 0)]

    return list(map(
        lambda d: (x + d[0], y + d[1], z + d[2], w + d[3]),
        deltas
    ))


def get_all_changeable(grid):
    all_changeable = set()

    for coordinates, value in grid.items():
        if value == INACTIVE:
            continue

        all_changeable.add(coordinates)
        all_changeable |= set(get_neighbours(coordinates))

    return all_changeable


def count_active_neighbours(grid, coordinates):
    neighbours = get_neighbours(coordinates)
    return sum(map(
        lambda n: grid[n] == ACTIVE,
        neighbours
    ))


def tick(grid):
    new_grid = defaultdict(lambda: INACTIVE)

    all_neighbours = get_all_changeable(grid)
    for coordinates in all_neighbours:
        active_neighbours = count_active_neighbours(grid, coordinates)

        if grid[coordinates] == ACTIVE and active_neighbours in [2, 3]:
            new_grid[coordinates] = ACTIVE
            continue

        if grid[coordinates] == INACTIVE and active_neighbours == 3:
            new_grid[coordinates] = ACTIVE

    return new_grid


grid = get_grid()

for _ in range(6):
    grid = tick(grid)

result = count_active(grid)
print(result)
