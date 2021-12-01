from collections import defaultdict

INFECTED = '#'
HEALTHY = '.'
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def get_grid():
    grid = defaultdict(lambda: HEALTHY)
    lines = get_lines()
    offset = (len(lines) // 2)
    size = len(lines)

    for y, row in enumerate(lines):
        for x, item in enumerate(row):
            grid[(x - offset, (size - 1) - y - offset)] = item

    return grid


def perform_bursts(grid, virus_position, number_of_bursts):
    infections = 0
    virus_direction = UP

    for _ in range(number_of_bursts):
        state = grid[virus_position]
        virus_direction = turn(virus_direction, state)
        changed_to_infected = flip_position(grid, virus_position)
        infections += changed_to_infected
        virus_position = move(virus_position, virus_direction)

        # print_grid(grid)
        # print('')


    return infections


def turn(direction, state):
    directions_order = [UP, RIGHT, DOWN, LEFT]
    clockwise_indicator = 1 if state == INFECTED else -1
    current_idx = directions_order.index(direction)
    after_turn_idx = (
        current_idx + clockwise_indicator
    ) % len(directions_order)

    after_turn = directions_order[after_turn_idx]

    return after_turn


def flip_position(grid, position):
    item = grid[position]
    to_insert = INFECTED if item == HEALTHY else HEALTHY
    grid[position] = to_insert

    return to_insert == INFECTED


def move(position, direction):
    delta = {
        UP: (0, 1),
        DOWN: (0, -1),
        LEFT: (-1, 0),
        RIGHT: (1, 0)
    }

    x, y = position
    dx, dy = delta[direction]

    return (x + dx, y + dy)

def print_grid(grid):
    min_x = min(grid, key=lambda p: p[0])[0]
    min_y = min(grid, key=lambda p: p[1])[1]

    max_x = max(grid, key=lambda p: p[0])[0]
    max_y = max(grid, key=lambda p: p[1])[1]

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            print(grid[(x,y)], end='')
        print('')

grid = get_grid()
virus_position = (0, 0)
number_of_bursts = 10000
result = perform_bursts(grid, virus_position, number_of_bursts)

print(result)
