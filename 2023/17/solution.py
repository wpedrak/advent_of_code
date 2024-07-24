import heapq
from collections import defaultdict

LEFT = 'L'
RIGHT = 'R'
UP = 'U'
DOWN = 'D'

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def min_path(board: list[list[int]]) -> int:
    height = len(board)
    width = len(board[0])
    to_visit: list[tuple[int, tuple[int, int, str, int]]] =  [(0, (0, 0, RIGHT, 0))]
    lowest_heat = defaultdict(lambda: float("inf"))
    lowest_heat[(0, 0, RIGHT, 0)] = 0

    while to_visit:
        heat, state = heapq.heappop(to_visit)

        if heat > lowest_heat[state]:
            continue

        for neighbour in get_neighbours(board, state):
            x, y, _, _ = neighbour
            neighbour_heat = heat + board[y][x]
            if lowest_heat[neighbour] <= neighbour_heat:
                continue

            lowest_heat[neighbour] = neighbour_heat
            heapq.heappush(to_visit, (neighbour_heat, neighbour))

    return min(v for k, v in lowest_heat.items() if k[:2] == (width-1, height-1))

def get_neighbours(board: list[list[int]], state: tuple[int, int, str, int]) -> list[tuple[int, int, str, int]]:
    height = len(board)
    width = len(board[0])

    x, y, direction, direction_steps = state
    oposite_direction = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,
    }[direction]

    proposal: list[tuple[int, int, str, int]] = [
        (x+1, y, RIGHT, direction_steps + 1 if direction == RIGHT else 1),
        (x-1, y, LEFT, direction_steps + 1 if direction == LEFT else 1),
        (x, y+1, DOWN, direction_steps + 1 if direction == DOWN else 1),
        (x, y-1, UP, direction_steps + 1 if direction == UP else 1),
    ]

    return [p for p in proposal
            if 0 <= p[0] < width
            if 0 <= p[1] < height
            if p[2] != oposite_direction
            if p[3] <= 3]


board = [[int(cell) for cell in row] for row in get_lines()]
result = min_path(board)
print(result)
