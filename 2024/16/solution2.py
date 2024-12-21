import heapq
from collections import defaultdict

NORTH = '^'
SOUTH = 'v'
WEST = '<'
EAST = '>'

Board = list[list[str]]
Point = tuple[int, int]
DirectedPoint = tuple[Point, str]

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

def find_neighbours(board: Board, directed_point: DirectedPoint) -> list[DirectedPoint]:
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

def backtrack_tiles(prev: dict[DirectedPoint, list[DirectedPoint]], end: DirectedPoint) -> set[Point]:
    visited = set()
    current_points = [end]

    while current_points:
        visited |= {p for p, _ in current_points}
        current_points = [p for point in current_points for p in prev[point]]

    return visited

def shortest_paths(board: Board, start: Point) -> tuple[dict[DirectedPoint, int], dict[DirectedPoint, list[DirectedPoint]]]:
    dist = defaultdict(lambda: 999999999999999)
    prev = defaultdict(list)
    dist[(start, EAST)] = 0
    visited = set()
    heap = [(0, (start, EAST))]

    while heap:
        _, directed_point = heapq.heappop(heap)
        if directed_point in visited:
            continue
        
        visited.add(directed_point)

        for neighbour, edge in find_neighbours(board, directed_point):
            new_dist = dist[directed_point] + edge
            if dist[neighbour] < new_dist:
                continue

            if dist[neighbour] == new_dist:
                prev[neighbour].append(directed_point)
                continue

            dist[neighbour] = new_dist
            prev[neighbour] = [directed_point]
            heapq.heappush(heap, (dist[neighbour], neighbour))

    return dist, prev

def run() -> None:
    board = read_board()
    start = find(board, 'S')
    end = find(board, 'E')

    dist, prev = shortest_paths(board, start)
    min_dist = min(dist[(end, d)] for d in [NORTH, SOUTH, WEST, EAST])
    directed_ends = [(end, d) for d in [NORTH, SOUTH, WEST, EAST] if dist[(end, d)] == min_dist]
    tiles = set()
    for directed_end in directed_ends:
        tiles |= backtrack_tiles(prev, directed_end)

    print(len(tiles))

run()
