import heapq
from collections import defaultdict

NORTH = '^'
SOUTH = 'v'
WEST = '<'
EAST = '>'

Board = list[list[str]]
Point = tuple[int, int]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_board() -> Board:
    return [list(l) for l in read_lines()]

def find(board: Board, value: str) -> Point:
    for y, row in enumerate(board):
        for x, item in enumerate(row):
            if item != value:
                continue
            return x, y
        
    raise Exception(':<')

def find_neighbours(board: Board, directed_point: tuple[Point, str]):
    point, direction = directed_point
    rotation = {
        NORTH: [WEST, EAST],
        SOUTH: [WEST, EAST],
        WEST: [NORTH, SOUTH],
        EAST: [NORTH, SOUTH],
    }
    neighbours = [((point, d), 1000) for d in rotation[direction]]
    x, y = point
    dx, dy = {
        NORTH: (0, -1),
        SOUTH: (0, 1),
        WEST: (-1, 0),
        EAST: (1, 0),
    }[direction]
    if board[y+dy][x+dx] != '#':
        neighbours.append((((x+dx, y+dy), direction), 1))

    return neighbours


def shortest_path(board: Board, start: Point, end: Point):
    dist = defaultdict(lambda: 999999999999999)
    dist[(start, EAST)] = 0
    visited = set()
    heap = [(0, (start, EAST))]

    while heap:
        _, directed_point = heapq.heappop(heap)
        if directed_point in visited:
            continue
        
        visited.add(directed_point)

        for neighbour, edge in find_neighbours(board, directed_point):
            if dist[neighbour] <= dist[directed_point] + edge:
                continue

            dist[neighbour] = dist[directed_point] + edge
            heapq.heappush(heap, (dist[neighbour], neighbour))

    return min(dist[(end, d)] for d in [NORTH, SOUTH, WEST, EAST])

def run() -> None:
    board = read_board()
    start = find(board, 'S')
    end = find(board, 'E')

    result = shortest_path(board, start, end)
    print(result)

run()
