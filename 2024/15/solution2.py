Board = list[list[str]]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_board() -> Board:
    lines = read_lines()
    board = []

    replace = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}

    for line in lines[:lines.index('')]:
        board.append([x for item in line for x in replace[item]])

    return board

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

def move_horizontally(board: Board, robot: tuple[int, int], dx: int):
    rx, ry = robot
    row = board[ry]

    x = rx + dx

    while row[x] in '[]':
        x += dx

    if row[x] == '#':
        return robot

    while x != rx:
        row[x] = row[x-dx]
        x -= dx

    return rx + dx, ry

def move_vertically(board: Board, robot: tuple[int, int], dy: int):
    current_level = [robot]
    potential_movers = {robot}
    box_shift = {'[': 1, ']': -1}

    while current_level:
        next_level = [(x, y+dy) for x, y in current_level if board[y+dy][x] != '.']
        if any(board[y][x] == '#' for x, y in next_level):
            return robot
        next_level += [(x + box_shift[board[y][x]], y) for x, y in next_level]
        potential_movers |= set(next_level)
        current_level = next_level

    for x, y in sorted(potential_movers, key=lambda p: p[1] * (-dy)):
        board[y+dy][x] = board[y][x]
        board[y][x] = '.'

    return robot[0], robot[1] + dy

def move(board: Board, robot: tuple[int, int], direction: str):
    x, y = robot
    assert board[y][x] == '.'

    if direction in '<>':
        return move_horizontally(board, robot, -1 if direction == '<' else 1)
    
    return move_vertically(board, robot, -1 if direction == '^' else 1)

def print_board(board: Board, robot: tuple[int, int]) -> None:
    x, y = robot
    board[y][x] = '@'
    print('\n'.join(''.join(row) for row in board))
    print('')
    board[y][x] = '.'

def run() -> None:
    board = read_board()
    directions = read_directions()
    robot = find_robot(board)
    board[robot[1]][robot[0]] = '.'

    for direction in directions:
        robot = move(board, robot, direction)

    result = sum(x + 100*y for y, row in enumerate(board) for x, item in enumerate(row) if item == '[')
    print(result)

run()
