import re

RIGHT = 'right'
LEFT = 'left'
DOWN = 'down'
UP = 'up'

def run() -> None:
    lines = read_lines()
    board = lines[:-2]
    row_len = max(len(row) for row in board)
    board = [' ' * row_len] + board + [' ' * row_len]
    board = [' ' + row + ' ' * (row_len - len(row)) + ' ' for row in board]

    x, y = board[1].index('.'), 1
    facing = RIGHT

    for command in parse_commands(lines[-1]):
        if command in ['L', 'R']:
            facing = turn(facing, command)
            continue

        x, y = move(board, x, y, facing, command)

    print(y * 1000 + x * 4 + facing_cost(facing))

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(file_name, 'r', encoding='utf-8')]

def parse_commands(line: str) -> list[int|str]:
    numbers = [int(x) for x in  re.findall(r'\d+', line)]
    turns = re.findall(r'L|R', line)
    longer = numbers if len(numbers) > len(turns) else turns
    shorter = numbers if len(numbers) <= len(turns) else turns

    return [longer[i//2] if not i % 2 else shorter[i//2] for i in range(len(numbers) + len(turns))]

def turn(facing: str, t: str) -> str:
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

def move(board: list[str], x: int, y: int, facing: str, distance: int) -> tuple[int, int]:
    dx, dy = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0),
    }[facing]

    while distance and board[y][x] != '#':
        distance -= 1
        x += dx
        y += dy
        while board[y][x] == ' ':
            x = (x+dx) % len(board[y])
            y = (y+dy) % len(board)

    if board[y][x] == '#':
        x, y = x-dx, y-dy

    if board[y][x] == ' ':
        dx, dy = {
            UP: (0, 1),
            DOWN: (0, -1),
            LEFT: (1, 0),
            RIGHT: (-1, 0),
        }[facing]
        while board[y][x] == ' ':
            x = (x+dx) % len(board[0])
            y = (y+dy) % len(board)

    return x, y

def facing_cost(facing: str) -> int:
    return [RIGHT, DOWN, LEFT, UP].index(facing)

run()
