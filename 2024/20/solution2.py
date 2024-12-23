Point = tuple[int, int]
Board = list[str]
Cheat = tuple[Point, Point, int]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def find_start(board: Board) -> Point:
    for y, row in enumerate(board):
        try:
            return row.index('S'), y
        except:
            pass
    
    raise Exception(':<')

def find_neighbours(board: Board, point: Point) -> list[Point]:
    x, y = point
    return [(a, b) for a, b in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if board[b][a] != '#']

def find_path(board: Board, start: Point) -> list[Point]:
    to_visit = [start]
    visited = set()
    path = []

    while to_visit:
        current = to_visit.pop()
        visited.add(current)
        path.append(current)

        neighbours = [n for n in find_neighbours(board, current) if n not in visited]
        assert len(neighbours) < 2

        to_visit += neighbours

    return path

def cheat_ends(board: Board, point: Point) -> list[Point]:
    x, y = point
    height, width = len(board), len(board[0])

    return [(x+dx, y+dy)
            for dx in range(-20, 21) 
            for dy in range(-20, 21)
            if abs(dx)+abs(dy) <= 20
            if 0 <= x+dx < width
            if 0 <= y+dy < height
            if board[y+dy][x+dx] != '#']

def manhattan(p1: Point, p2: Point):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_cheats(board: Board, path: list[Point]):
    position = {p: idx for idx, p in enumerate(path)}
    cheats: list[Cheat] = []
    for start in path:
        for end in cheat_ends(board, start):
            profit = position[end] - position[start] - manhattan(start, end)
            if profit <= 0:
                continue
            cheats.append((start, end, profit))

    return cheats

def run() -> None:
    board = read_lines()
    start = find_start(board)
    path = find_path(board, start)
    cheats = find_cheats(board, path)

    result = sum(dist >= 100 for _, _, dist in cheats)
    print(result)

run()
