def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_board():
    lines = read_lines()
    width = len(lines[0]) + 2
    board = ['?' * width]
    for line in lines:
        board.append('?' + line + '?')
    board.append('?' * width)
    return board

def neighbours(board: list[str], point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    value = board[y][x]
    potential = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
    return [(x, y) for x, y in potential if board[y][x] == value]

def find_region(board: list[str], start: tuple[int, int]):
    to_visit = [start]
    visited = set()
    while to_visit:
        current = to_visit.pop()
        visited.add(current)
        to_visit += [n for n in neighbours(board, current) if n not in visited]

    return visited

def find_regions(board: list[str]):
    height, width = len(board), len(board[0])
    to_visit = {(x, y) for x in range(1, width-1) for y in range(1, height-1)}
    regions = []

    while to_visit:
        current = to_visit.pop()
        region = find_region(board, current)
        to_visit -= region
        regions.append(region)

    return regions

def perimeter(board: list[str], region: set[tuple[int, int]]):
    return sum(4-len(neighbours(board, p)) for p in region)

def run() -> None:
    board = read_board()
    regions = find_regions(board)
    result = sum(len(r)*perimeter(board, r) for r in regions)
    print(result)

run()
