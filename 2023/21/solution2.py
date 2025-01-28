from collections import deque

Point = tuple[int, int]
Plots = list[str]

STEPS = 26501365

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_plots() -> list[str]:
    lines = read_lines()
    plots = []
    for line in lines:
        plots.append('#' + line + '#')
    width = len(plots[0])
    return ['#' * width] + plots + ['#' * width] 

def find_starting_plot(plots: list[str]) -> Point:
    for y, row in enumerate(plots):
        try:
            x = row.index('S')
        except:
            continue
        return x, y
    
    raise Exception(':<')

def manhattan(p1: Point, p2: Point):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def achievable_count(plots: Plots, start: Point):
    reached = {start}
    deltas = [(1,0), (-1,0), (0,1), (0, -1)]
    dist = 0
    cnt = {}
    to_visit = deque([start, 'UP'])
    visited = set()

    while to_visit:
        position = to_visit.popleft()

        if isinstance(position, str):
            cnt[dist] = sum(manhattan(start, v) % 2 == dist % 2 for v in visited)
            dist += 1
            if to_visit:
                to_visit.append('UP')
            continue

        if position in visited:
            continue

        visited.add(position)
        x, y = position
        to_visit += {(x+dx, y+dy) for dx, dy in deltas if plots[y+dy][x+dx] != '#'}

    return cnt


def run() -> None:
    plots = read_plots()
    start_position = find_starting_plot(plots)

    # plots shape is odd-sized square
    assert len(plots) == len(plots[0]) and len(plots) % 2
    # start point is in the middle
    assert start_position == (len(plots) // 2, len(plots) // 2)
    # there is a cross of '.' that has 'S' in the middle
    assert '#' not in {row[start_position[0]] for row in plots[1:-1]}
    assert '#' not in set(plots[start_position[1]][1:-1])

    tmp = achievable_count(plots, start_position)
    print(tmp[64])

run()
