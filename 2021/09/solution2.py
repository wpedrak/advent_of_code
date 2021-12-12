import heapq

def get_lines(filename='input.txt'):
    return [line.rstrip() for line in open(filename, 'r')]

def get_board() -> list[list[int]]:
    return [list(map(int, l)) for l in get_lines()]

def get_basins(board: list[list[int]]):
    visited = set()
    basins = []
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value == 9:
                continue
            point = (x, y)
            if point in visited:
                continue
            basin = get_basin(board, point)
            visited |= basin
            basins.append(basin)

    return basins

def get_basin(board: list[list[int]], point: tuple[int, int]) -> set[tuple[int, int]]:
    width = len(board[0])
    height = len(board)
    basin = set()
    to_visit = [point]

    while to_visit:
        point = to_visit.pop()
        x, y = point
        if point in basin:
            continue
        if x < 0 or x >= width:
            continue
        if y < 0 or y >= height:
            continue
        if board[y][x] == 9:
            continue

        basin.add(point)
        to_visit += get_neighbours(point)

    return basin

def get_neighbours(point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    return [
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1),
    ]

board = get_board()
basins = get_basins(board)
lb1, lb2, lb3 = heapq.nlargest(3, basins, len)
print(len(lb1)*len(lb2)*len(lb3))
