from collections import deque

Point = tuple[int, int]

HEIGHT = 70
WIDTH = 70

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def neighbours(point: Point):
    x, y = point
    potential = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [(x, y) for x, y in potential if 0 <= x <= WIDTH if 0 <= y <= HEIGHT]


def escape_path_len(walls: set[Point]):
    to_visit = deque([(0,0), 'UP'])
    dist = 0
    visited = set()

    while len(to_visit) > 1:
        current = to_visit.popleft()
        if isinstance(current, str):
            dist += 1
            to_visit.append('UP')
            continue

        if current in visited:
            continue
        visited.add(current)

        if current == (WIDTH, HEIGHT):
            return dist

        to_visit += [n for n in neighbours(current) if n not in visited if n not in walls]

def find_blocking(walls: list[Point]) -> Point:
    l = 0
    r = len(walls) - 1

    while r - l > 1:
        print(l, r)
        mid = (l + r) // 2
        if escape_path_len(set(walls[:mid+1])):
            l = mid + 1
        else:
            r = mid        

    return walls[l]

def run() -> None:
    walls = [(int(spl[0]), int(spl[1])) for l in read_lines() if (spl := l.split(','))]
    x, y = find_blocking(walls)
    print(f'{x},{y}')

run()
