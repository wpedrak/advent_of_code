ON = '#'
OFF = '.'


def get_lines(filename='18/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_empty_grid(size):
    return [[OFF] * size for _ in range(size)]


def get_grid():
    raw_grid = get_lines()
    size = len(raw_grid) + 2
    grid = get_empty_grid(size)

    for y, row in enumerate(raw_grid):
        for x, item in enumerate(row):
            grid[y+1][x+1] = item

    return grid


def make_steps(grid, steps):
    for _ in range(steps):
        grid = step(grid)

    return grid


def step(grid):
    size = len(grid) - 2
    next_grid = get_empty_grid(size + 2)

    for y in range(1, size + 1):
        for x in range(1, size + 1):
            state = grid[y][x]
            on_neighbours = count_on_neighbours(grid, x, y)

            if on_neighbours == 3:
                next_grid[y][x] = ON
                continue

            if on_neighbours == 2 and state == ON:
                next_grid[y][x] = ON
                continue

    return next_grid


def count_on_neighbours(grid, x, y):
    neighbours = [(x+dx, y+dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]

    return sum(map(
        lambda p: grid[p[1]][p[0]] == ON,
        neighbours
    ))


def count_on(grid):
    return sum(map(
        lambda row: sum(map(
            lambda x: x == ON,
            row
        )),
        grid
    ))


grid = get_grid()
new_grid = make_steps(grid, 100)
result = count_on(new_grid)
print(result)
