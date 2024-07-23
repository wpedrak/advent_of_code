from collections import deque

LEFT = 'L'
RIGHT = 'R'
UP = 'U'
DOWN = 'D'

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def min_path(board: list[list[int]]) -> int:
    height = len(board)
    width = len(board[0])
    to_visit: deque[tuple[int, int, str, int, int]] = deque([(0, 0, RIGHT, 0, 0)])
    lowest_heat: dict[tuple[int, int, str, int], int] = {(0, 0, RIGHT, 0): 0}
    target = (width-1, height-1)
    best_heat = (width + height) * 9

    while to_visit:
        x, y, direction, direction_steps, heat = to_visit.popleft()
        state = (x, y, direction, direction_steps)

        if lowest_heat[state] < heat:
            continue

        if (x, y) == target:
            best_heat = min(best_heat, heat)

        for neighbour in get_neighbours(board, state):
            x, y, direction, direction_steps = neighbour
            neighbour_heat = heat + board[y][x]
            if neighbour_heat > best_heat:
                continue
            if neighbour in lowest_heat and lowest_heat[neighbour] <= neighbour_heat:
                continue

            lowest_heat[neighbour] = neighbour_heat
            to_visit.append((x, y, direction, direction_steps, neighbour_heat))

    return best_heat

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
