import re

RIGHT = 'right'
LEFT = 'left'
DOWN = 'down'
UP = 'up'

PRINT = 0

def mark(board, x, y, facing):
    global PRINT
    if PRINT:
        board[y][x] = {
            UP: '^', DOWN: 'V', LEFT: '<', RIGHT: '>'
        }[facing]
        PRINT -= 1

def run() -> None:
    lines = read_lines(file_name='input.txt')
    board = lines[:-2]
    row_len = max(len(row) for row in board)
    board = [' ' * row_len] + board + [' ' * row_len]
    board = [' ' + row + ' ' * (row_len - len(row)) + ' ' for row in board]

    x, y = board[1].index('.'), 1
    board = [list(row) for row in board]
    facing = RIGHT

    for command in parse_commands(lines[-1]):
        if command in ['L', 'R']:
            facing = turn(command, facing)
            mark(board, x, y, facing)
            continue

        x, y, facing = move(board, x, y, facing, command)

    print(f'({x}, {y}, {facing}) ->', y * 1000 + x * 4 + facing_cost(facing))
    for row in board:
        print(''.join(row))

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(file_name, 'r', encoding='utf-8')]

def parse_commands(line: str) -> list[int|str]:
    numbers = [int(x) for x in  re.findall(r'\d+', line)]
    turns = re.findall(r'L|R', line)
    longer = numbers if len(numbers) > len(turns) else turns
    shorter = numbers if len(numbers) <= len(turns) else turns

    return [longer[i//2] if not i % 2 else shorter[i//2] for i in range(len(numbers) + len(turns))]

def turn(t: str, facing: str) -> str:
    return {
        'L': {
            UP: LEFT,
            LEFT: DOWN,
            DOWN: RIGHT,
            RIGHT: UP,
        },
        'R': {
            UP: RIGHT,
            RIGHT: DOWN,
            DOWN: LEFT,
            LEFT: UP,
        },
    }[t][facing]

def move(board: list[str], x: int, y: int, facing: str, distance: int) -> tuple[int, int, str]:
    deltas = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0),
    }
    dx, dy = deltas[facing]
    next_x, next_y = x+dx, y+dy
    next_facing = facing
    if board[next_y][next_x] == ' ':
        print(f'wrap ({next_x}, {next_y}, {next_facing}) -> ', end='')
        next_x, next_y, next_facing = wrap(next_x, next_y, next_facing)
        print(f'({next_x}, {next_y}, {next_facing})')
        dx, dy = deltas[next_facing]

    while distance and board[next_y][next_x] != '#':
        distance -= 1
        x = next_x
        y = next_y
        facing = next_facing
        mark(board, x, y, facing)
        next_x += dx
        next_y += dy
        # next step will require wrapping
        if board[next_y][next_x] == ' ':
            print(f'wrap ({next_x}, {next_y}, {next_facing}) -> ', end='')
            next_x, next_y, next_facing = wrap(next_x, next_y, next_facing)
            print(f'({next_x}, {next_y}, {next_facing})')
            dx, dy = deltas[next_facing]

    return x, y, facing

def wrap(x: int, y: int, facing: str) -> tuple[int, int, str]:
    if facing == UP:
        if 0 < x <= 50 and y == 100:
            x, y = shift(RIGHT, x, y)
            return rotate_right(x, y, facing)
        if 50 < x <= 100 and y == 0:
            x, y = shift(DOWN, x, y, times=4)
            x, y = shift(LEFT, x, y)
            return rotate_right(x, y, facing)
        if 100 < x <= 150 and y == 0:
            x, y = shift(DOWN, x, y, times=4)
            x, y = shift(LEFT, x, y, times=2)
            return x, y, facing

    if facing == RIGHT:
        if x == 151 and 0 < y <= 50:
            x, y = shift(DOWN, x, y, times=2)
            x, y = shift(LEFT, x, y, times=2)
            return rotate_back(x, y, facing)
        if x == 101 and 50 < y <= 100:
            x, y = shift(UP, x, y)
            return rotate_left(x, y, facing)
        if x == 101 and 100 < y <= 150:
            x, y = shift(UP, x, y, times=2)
            return rotate_back(x, y, facing)
        if x == 51 and 150 < y <= 200:
            x, y = shift(UP, x, y)
            return rotate_left(x, y, facing)

    if facing == DOWN:
        if 0 < x <= 50 and y == 201:
            x, y = shift(UP, x, y, times=4)
            x, y = shift(RIGHT, x, y, times=2)
            return x, y, facing
        if 50 < x <= 100 and y == 151:
            x, y = shift(LEFT, x, y)
            return rotate_right(x, y, facing)
        if 100 < x <= 150 and y == 51:
            x, y = shift(LEFT, x, y)
            return rotate_right(x, y, facing)

    if facing == LEFT:
        if x == 50 and 0 < y <= 50:
            x, y = shift(DOWN, x, y, times=2)
            return rotate_back(x, y, facing)
        if x == 50 and 50 < y <= 100:
            x, y = shift(DOWN, x, y)
            return rotate_left(x, y, facing)
        if x == 0 and 100 < y <= 150:
            x, y = shift(UP, x, y, times=2)
            x, y = shift(RIGHT, x, y, times=2)
            return rotate_back(x, y, facing)
        if x == 0 and 150 < y <= 200:
            x, y = shift(UP, x, y, times=3)
            x, y = shift(RIGHT, x, y, times=2)
            return rotate_right(x, y, facing)

    raise Exception(f'Failed to wrap ({x}, {y})')

def rotate_right(*args) -> tuple[int, int, str]:
    if len(args) == 1:
        args = args[0]
    original_x, original_y, facing = args
    # move left top point of the square to (0, 0)
    x = (original_x-1) % 50
    x_offset = original_x - x
    y = (original_y-1) % 50
    y_offset = original_y - y

    # move middle of the square to (0,0)
    x -= 24.5
    y -= 24.5

    # rotate right
    x, y = -y, x

    # move left top point of the square to (0, 0)
    x = int(x + 24.5)
    y = int(y + 24.5)

    return x_offset + x, y_offset + y, turn('R', facing)

def rotate_back(*args) -> tuple[int, int, str]:
    args = rotate_right(args)
    return rotate_right(args)

def rotate_left(*args) -> tuple[int, int, str]:
    args = rotate_right(args)
    args = rotate_right(args)
    return rotate_right(args)
    
def shift(direction: str, x: int, y: int, times=1) -> tuple[int, int]:
    dx, dy = {
        UP: (0, -50),
        DOWN: (0, 50),
        LEFT: (-50, 0),
        RIGHT: (50, 0),
    }[direction]

    return x + dx*times, y + dy*times

def facing_cost(facing: str) -> int:
    return [RIGHT, DOWN, LEFT, UP].index(facing)

run()

# 108239 too low
# 178196 too high
