from numpy import source

INF = 2**31

def get_lines(filename='input2.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_board() -> list[list[str]]:
    return [list(l) for l in get_lines()]

def get_min_cost(board: list[list[str]]) -> int:
    if is_solved(board):
        return 0
    movable_positions = get_movable_positions(board)
    costs = []

    for source in movable_positions:
        for dest in get_moves(board, source):
            swap(board, source, dest)
            move_cost = get_move_cost(board, source, dest)
            costs.append(get_min_cost(board) + move_cost)
            swap(board, source, dest)

    return min(costs, default=INF)

def is_solved(board: list[list[int]]) -> bool:
    bottom_fields = [
        ('A', 3),
        ('B', 5),
        ('C', 7),
        ('D', 9),
    ]
    y = 5
    for desired_letter, x in bottom_fields:
        for dy in range(4):
            if board[y+dy][x] != desired_letter:
                return False

    return True

def get_movable_positions(board: list[list[str]]) -> list[tuple[int, int]]:
    height = len(board)
    width = len(board[0])
    return [
        (x, y)
        for x in range(1, width-2)
        for y in range(1, height-2)
        if is_movable_position(board, x, y)
    ]

def is_movable_position(board, x, y):
    field = board[y][x]
    if field not in 'ABCD':
        return False
    
    deltas = [
        (1, 0),
        (-1, 0),
        (0, -1),
    ]
    return any(board[y+dy][x+dx] == '.' for dx, dy in deltas)

def get_moves(board: list[list[int]], src: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = src
    letter = board[y][x]
    board[y][x] = '.'
    possible_dest = get_possible_moves(board, src)
    board[y][x] = letter

def get_possible_moves(board: list[list[int]], point: tuple[int, int]) -> set[tuple[int, int]]:
    visited = set()
    to_visit 
    # TODO

def get_move_cost(board: list[list[int]], src: tuple[int, int], dest: tuple[int, int]) -> int:
    sx, sy = src
    dx, dy = dest
    letter = board[sy][sx]
    unit_price = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }[letter]

    path_length = (sy - 1) + abs(sx - dx) + (dy - 1)
    return path_length * unit_price


def swap(board: list[list[str]], src: tuple[int, int], dest: tuple[int, int]) -> None:
    sx, sy = src
    dx, dy = dest
    board[sy][sx], board[dy][dx] = board[dy][dx], board[sy][sx]


board = get_board()
cost = get_min_cost(board)
print(cost)
