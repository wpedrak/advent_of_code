from collections import Counter, deque

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
WALL = '#'

pnt = tuple[int, int]

def run() -> None:
    lines = read_lines()
    blizzard = []
    walls = set()

    for y, row in enumerate(lines):
        for x, item in enumerate(row):
            if item in ['>', '<', '^', 'v']:
                blizzard.append(((x, y), item))
            if item == WALL:
                walls.add((x, y))
    width = len(lines[0])
    height = len(lines)

    steps = walk(walls, blizzard, (1, 0), (width-2, height-1))
    print(steps)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(file_name, 'r', encoding='utf-8')]

def print_blizzard(blizzard: list[tuple[pnt, str]]) -> None:
    blizzard_dict = dict(blizzard)
    max_x = max(e[0] for e in blizzard_dict)
    max_y = max(e[1] for e in blizzard_dict)

    for y in range(1, max_y+1):
        for x in range(1, max_x+1):
            field = blizzard_dict.get((x, y), '.')
            print(field, end='')
        print('')
    print('')


def walk(walls: set[pnt], blizzard: list[tuple[pnt, str]], start: pnt, end: pnt) -> int:
    next_level = deque([start])
    time = 0
    obstacles = {p for p, _ in blizzard} | walls
    visited = None

    while True:
        time += 1
        to_visit = next_level
        next_level = deque()
        visited = set()
    
        blizzard = progress_blizzard(blizzard, walls)
        obstacles = {p for p, _ in blizzard} | walls
        print(time)

        while to_visit:
            item = to_visit.popleft()
            if item == end:
                return time - 1

            item_neighbours = neighbours(item, obstacles)
            next_level += [n for n in item_neighbours if n not in visited]
            visited |= set(item_neighbours)

def progress_blizzard(blizzard: list[tuple[pnt, str]], walls: set[pnt]) -> list[tuple[pnt, str]]:
    right_wall_x = max(w[0] for w in walls)
    bot_wall_y = max(w[1] for w in walls)
    return [(move_shard(point, direction, right_wall_x, bot_wall_y), direction) for point, direction in blizzard]

def move_shard(point: pnt, direction: str, right_wall_x: int, bot_wall_y: int) -> pnt:
    x, y = point
    x, y = {
        UP: (x, y-1),
        DOWN: (x, y+1),
        LEFT: (x-1, y),
        RIGHT: (x+1, y),
    }[direction]

    if direction == UP and y == 0:
        return (x, bot_wall_y-1)
    if direction == DOWN and y == bot_wall_y:
        return (x, 1)
    if direction == LEFT and x == 0:
        return (right_wall_x-1, y)
    if direction == RIGHT and x == right_wall_x:
        return (1, y)

    return x, y

def neighbours(point: pnt, obstacles: set[pnt]) -> list[pnt]:
    if point == (1, 0):
        return [p for p in [(1, 0), (1, 1)] if p not in obstacles]

    x, y = point
    return [p for p in [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x, y)] if p not in obstacles]

run()
