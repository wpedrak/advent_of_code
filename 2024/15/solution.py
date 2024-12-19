Board = list[list[str]]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_board() -> Board:
    lines = read_lines()
    return [list(l) for l in lines[:lines.index('')]]

def read_directions():
    lines = read_lines()
    return ''.join(lines[lines.index('')+1:])

def find_robot(board: Board) -> tuple[int, int]:
    for y, row in enumerate(board):
        for x, item in enumerate(row):
            if item != '@':
                continue
            return x, y
        
    raise Exception(':<')

def move(board: Board, robot: tuple[int, int], direction: str):
    x, y = robot
    assert board[y][x] == '.'
    dx, dy = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}[direction]

    first_step = (x+dx, y+dy)
    x, y = first_step

    while board[y][x] == 'O':
        x, y = x+dx, y+dy

    if board[y][x] == '#':
        return robot

    board[y][x], board[first_step[1]][first_step[0]] = 'O', '.'

    return first_step

def run() -> None:
    board = read_board()
    directions = read_directions()
    robot = find_robot(board)
    board[robot[1]][robot[0]] = '.'

    for direction in directions:
        robot = move(board, robot, direction)

    result = sum(x + 100*y for y, row in enumerate(board) for x, item in enumerate(row) if item == 'O')
    print(result)

run()
