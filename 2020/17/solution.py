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
            grid[(x, y, 0)] = value

    return grid


def count_active(grid):
    return sum(map(
        lambda x: x == ACTIVE,
        grid.values()
    ))


def get_neighbours(coordinates):
    x, y, z = coordinates
    deltas = [(dx, dy, dz) for dx in range(-1, 2) for dy in range(-1, 2) for dz in range(-1, 2) if (dx, dy, dz) != (0, 0, 0)]

    return list(map(
        lambda d: (x + d[0], y + d[1], z + d[2]),
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


def print_grid_for_z(grid, z):
    min_x = min(grid.keys(), key=lambda c: c[0])[0]
    max_x = max(grid.keys(), key=lambda c: c[0])[0]
    min_y = min(grid.keys(), key=lambda c: c[1])[1]
    max_y = max(grid.keys(), key=lambda c: c[1])[1]

    print(f"top-left at ({min_x}, {min_y})")
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(grid[(x, y, z)], end='')
        print()
    print()


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
