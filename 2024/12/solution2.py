UP = 'U'
RIGHT = 'R'
DOWN = 'D'
LEFT = 'L'

Point = tuple[int, int]

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

def find_neighbours(board: list[str], point: Point) -> list[Point]:
    x, y = point
    value = board[y][x]
    potential = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
    return [(x, y) for (x, y) in potential if board[y][x] == value]

def find_outer_with_direction(board: list[str], point: Point) -> list[tuple[Point, str]]:
    x, y = point
    value = board[y][x]
    potential = [((x, y+1), DOWN), ((x, y-1), UP), ((x+1, y), RIGHT), ((x-1, y), LEFT)]
    return [((x, y), direction) for (x, y), direction in potential if board[y][x] != value]


def find_region(board: list[str], start: Point):
    to_visit = [start]
    visited = set()
    while to_visit:
        current = to_visit.pop()
        visited.add(current)
        to_visit += [n for n in find_neighbours(board, current) if n not in visited]

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

def scan_wall(point: Point, direction: str) -> tuple[Point, Point]:
    x, y = point
    dx1, dy1 = {
        UP: (0, -1),
        DOWN: (0, 1),
        LEFT: (-1, 0),
        RIGHT: (1, 0),
        }[direction]
    dx2, dy2 = {
        UP: (1, -1),
        DOWN: (-1, 1),
        LEFT: (-1, -1),
        RIGHT: (1, 1),
    }[direction]

    return ((x+dx1, y+dy1), (x+dx2, y+dy2))

def right(direction: str) -> str:
    return {
        UP: RIGHT,
        RIGHT: DOWN,
        DOWN: LEFT,
        LEFT: UP,
    }[direction]

def left(direction: str) -> str:
    return right(right(right(direction)))

def sides_starting_at(region: set[Point], start_point: Point, start_direction: str) -> tuple[int, set[Point]]:
    outer = start_point
    direction = start_direction
    visited = set()
    sides_count = 0

    while outer != start_point or direction != start_direction or sides_count == 0:
        visited.add(outer)
        front_point, right_point = scan_wall(outer, direction)
        if front_point not in region and right_point not in region:
            outer = right_point
            direction = right(direction)
            sides_count += 1
        elif front_point not in region:
            outer = front_point
        else:
            direction = left(direction)
            sides_count += 1

    return sides_count, visited

def sides(board: list[str], region: set[Point]):
    neighbours = [(o, right(direction)) for point in region for o, direction in find_outer_with_direction(board, point)]

    sides_count = 0
    while neighbours:
        point, direction = neighbours.pop()
        partial_sides_count, visited = sides_starting_at(region, point, direction)
        sides_count += partial_sides_count
        neighbours = [(p, direction) for p, direction in neighbours if p not in visited]

    return sides_count

def run() -> None:
    board = read_board()
    regions = find_regions(board)
    result = sum(len(r)*sides(board, r) for r in regions)
    print(result)

run()
