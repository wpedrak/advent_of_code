UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_board() -> list[list[str]]:
    lines = read_lines()
    width =  len(lines[0]) + 2
    board = ['.' * width]
    for line in lines:
        board.append('.' + line + '.')
    board.append('.' * width)

    return [list(row) for row in board]

def find_guard(board: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(board):
        if '^' not in row:
            continue
        return row.index('^'), y

def move(board: list[list[str]], position: tuple[int, int], direction: str):
    x, y = position
    dx, dy = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0),
    }[direction]

    next_x, next_y = x+dx, y+dy
    if board[next_y][next_x] != '#':
        return (next_x, next_y), direction
    
    new_direction = {
        UP: RIGHT,
        RIGHT: DOWN,
        DOWN: LEFT,
        LEFT: UP,
    }[direction]

    return position, new_direction

def walk(board: list[list[str]], position: tuple[int, int]) -> tuple[bool, set[tuple[int, int]]]:
    height, width = len(board), len(board[0])
    direction = UP

    visited = set()
    while (position, direction) not in visited and position[0] not in [0, width-1] and position[1] not in [0, height-1]:
        visited.add((position, direction))
        position, direction = move(board, position, direction)

    return (position, direction) in visited, {pos for pos, _ in visited}

def run() -> None:
    board = read_board()
    height, width = len(board), len(board[0])
    start_position = find_guard(board)

    _, walk_set = walk(board, start_position)
    walk_set.remove(start_position)

    result = 0
    for idx, (x, y) in enumerate(walk_set):
        print(idx, len(walk_set))
        board[y][x] = '#'
        is_loop, _ = walk(board, start_position)
        result += is_loop
        board[y][x] = '.'

    print(result)

run()
