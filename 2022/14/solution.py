from numpy import sign

AIR = '.'
ROCK = '#'
SAND = 'o'

def run() -> None:
    rock_paths = [parse(line) for line in read_lines()]
    max_x = max(point[0] for path in rock_paths for point in path)
    max_y = max(point[1] for path in rock_paths for point in path)

    grid = [[AIR] * (max_x+1) for _ in range(max_y+1)]
    for path in rock_paths:
        for source, target in zip(path[:-1], path[1:]):
            mark_rock(grid, source, target)

    sand_count = 0
    while put_sand(grid, max_y):
        sand_count += 1

    print(sand_count)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse(line: str) -> list[tuple[int, int]]:
    points = []
    for part in line.split(' -> '):
        x, y = part.split(',')
        points.append((int(x), int(y)))

    return points

def mark_rock(grid: list[list[str]], source: tuple[int, int], target: tuple[int, int]) -> None:
    sx, sy = source
    tx, ty = target
    dx = sign(tx - sx)
    dy = sign(ty - sy)

    x, y = source
    while (x, y) != target:
        grid[y][x] = ROCK
        x += dx
        y += dy

    grid[y][x] = ROCK

# True iff succeded successfully added sand, False otherwise
def put_sand(grid: list[list[str]], bottom_line: int) -> bool:
    x, y = 500, 0

    while y < bottom_line:
        # print(x, y)
        if grid[y+1][x] == AIR:
            y += 1
            continue
        if grid[y+1][x-1] == AIR:
            x -= 1
            y += 1
            continue
        if grid[y+1][x+1] == AIR:
            x += 1
            y += 1
            continue

        grid[y][x] = SAND
        return True

    return False
    
def print_grid(grid: list[list[str]]) -> None:
    for row in grid:
        print(''.join(row)[-50:])

run()
