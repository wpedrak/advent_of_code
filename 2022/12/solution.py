from collections import deque

def run() -> None:
    grid = make_grid(read_lines())
    sx, sy = find_position(grid, 'S')
    ex, ey = find_position(grid, 'E')
    grid[sy][sx] = 'a'
    grid[ey][ex] = 'z'

    print(shortest_path_length(grid, (sx, sy), (ex, ey)))

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def make_grid(lines: list[str]) -> list[list[str]]:
    width = len(lines[0])
    grid = []
    # ord('|') == ord('z') + 2
    grid.append(['|'] * (width + 2))
    for line in lines:
        grid.append(list('|' + line + '|'))
    grid.append(['|'] * (width + 2))
    return grid

def find_position(grid: list[list[str]], val: str) -> tuple[int, int]:
    for y, row in enumerate(grid):
        if val not in row:
            continue
        return row.index(val), y

    raise Exception(f'"{val}" not found')

def shortest_path_length(grid: list[list[str]], start: tuple[int, int], end: tuple[int, int]) -> int:
    visited = {start}
    length = 0
    to_visit = deque([start, 'UP'])

    while to_visit:
        point = to_visit.popleft()
        if point == 'UP':
            length += 1
            to_visit.append('UP')
            continue

        if point == end:
            return length

        neighbours = find_neighbours(grid, point)
        to_visit += [n for n in neighbours if n not in visited]
        visited |= set(neighbours)

    raise Exception('Path not found')

def find_neighbours(grid: list[list[str]], point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    return [
            (x+dx, y+dy)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
            if ord(grid[y][x]) + 1 >= ord(grid[y+dy][x+dx])
        ]

run()
