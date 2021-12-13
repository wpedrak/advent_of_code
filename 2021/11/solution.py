Board = list[list[int]]

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_board() -> Board:
    lines = get_lines()
    width = len(lines[0])
    board = []
    no_energy = -12321
    board.append([no_energy] * (width+2))
    for line in lines:
        board.append([no_energy] + [int(n) for n in line] + [no_energy])
    board.append([no_energy] * (width+2))
    return  board

def tick(board: Board) -> int:
    width = len(board)-2
    height = len(board)-2
    to_increase = [(x, y) for x in range(1, width+1) for y in range(1, height+1)]

    flashes = 0
    while to_increase:
        point = to_increase.pop()
        x, y = point
        board[y][x] += 1
        if board[y][x] == 10:
            flashes += 1
            to_increase += get_neighbours(point)

    clear_high_power(board)
    return flashes

def clear_high_power(board: Board):
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value < 10:
                continue
            board[y][x] = 0

def get_neighbours(point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    return [
        (x+dx, y+dy)
        for dy in range(-1, 2)
        for dx in range(-1, 2)
        if (dx, dy) != (0, 0)
    ]

def print_board(board: Board) -> None:
    for row in board[1:-1]:
        print(''.join(str(x) for x in row[1:-1]))

board = get_board()
flashes = 0
for i in range(100):
    # print(i)
    # print_board(board)
    tick_flashes = tick(board)
    flashes += tick_flashes

print(flashes)
