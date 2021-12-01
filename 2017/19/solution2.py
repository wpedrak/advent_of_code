UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
EMPTY = ' '
TURN = '+'


def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line for line in f.readlines()]


def count_steps(packet_map, start_position, direction):
    x, y = start_position

    steps = 0

    while packet_map[y][x] != EMPTY:
        item = packet_map[y][x]

        if is_turn(item):
            direction = take_turn(packet_map, x, y, direction)

        x, y = move(x, y, direction)
        steps += 1

    return steps


def is_turn(item):
    return item == TURN


def take_turn(packet_map, x, y, direction):
    if is_vertical(direction):
        if packet_map[y][x-1] == '-':
            return LEFT
        if packet_map[y][x+1] == '-':
            return RIGHT

        raise Exception('No left/right')

    if packet_map[y-1][x] == '|':
        return UP
    if packet_map[y+1][x] == '|':
        return DOWN

    raise Exception('No up/down')


def is_vertical(direction):
    return direction in [UP, DOWN]


def move(x, y, direction):
    delta_dict = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0)
    }
    dx, dy = delta_dict[direction]

    return x + dx, y + dy


packet_map = get_lines()
start_position = (1, 0)
result = count_steps(packet_map, start_position, DOWN)

print(result)
