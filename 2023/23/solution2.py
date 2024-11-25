import heapq
from collections import defaultdict

Position = tuple[int, int]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def reduce_board(board: list[str]):
    graph: dict[Position, dict[Position, int]] = {}
    
    to_visit = [(1, 1)]
    visited = set()

    while to_visit:
        current = to_visit.pop()
        visited.add(current)
        graph_neighbours = dict(x for n in get_neighbours(board, current) if (x := walk_the_path(board, current, n)) is not None)

        graph[current] = graph_neighbours
        to_visit += (n for n in graph_neighbours if n not in visited)

    return graph

def walk_the_path(board: list[str], start: Position, first_step: Position):
    height, width = len(board), len(board[0])
    visited = {start}
    current_step = first_step

    while True:
        visited.add(current_step)
        
        if is_crossing(board, current_step) or current_step == (width-2, height-2):
            return current_step, len(visited)-1
        
        neighbours = [n for n in get_neighbours(board, current_step) if n not in visited]
        if not neighbours:
            # it's ok to find a dead end
            return None
        
        current_step = neighbours[0]

def is_crossing(board: list[str], position: Position):
    x, y = position
    return sum(board[y+dy][x+dx] != '#' for dx in range(-1, 2) for dy in range(-1, 2) if abs(dx) + abs(dy) == 1) > 2

def get_neighbours(board: list[str], position: Position) -> list[Position]:
    x, y = position
    neighbours = []
    if board[y][x+1] != '#':
        neighbours.append((x+1, y))
    if board[y][x-1] != '#':
        neighbours.append((x-1, y))
    if board[y+1][x] != '#':
        neighbours.append((x, y+1))
    if board[y-1][x] != '#':
        neighbours.append((x, y-1))
    return neighbours

def longest_path(graph: dict[Position, dict[Position, int]], start: Position, end: Position):
    def aux(graph: dict[Position, dict[Position, int]], current: Position, end: Position, visited: set[Position]) -> int:
        if current == end:
            return 0
        return max([aux(graph, n, end, visited | {current}) + d for n, d in graph[current].items() if n not in visited], default=-999999999)

    return aux(graph, start, end, set())

def run() -> None:
    board = read_lines()
    height, width = len(board), len(board[0])
    board[0] = board[0].replace('.', '#')
    board[height-1] = board[height-1].replace('.', '#')

    graph = reduce_board(board)
    result = longest_path(graph, (1, 1), (width-2, height-2)) + 2
    print(result)

run()
