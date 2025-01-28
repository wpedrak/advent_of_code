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

def achievable_count(plots: Plots, start: Point):
    reached = {start}
    deltas = [(1,0), (-1,0), (0,1), (0, -1)]
    dist = 0
    cnt = {}
    to_visit = deque([start, 'UP'])
    visited_odd = set()
    visited_even = set()
    visited_current = visited_even

    while to_visit:
        position = to_visit.popleft()

        if isinstance(position, str):
            cnt[dist] = len(visited_current)
            dist += 1
            visited_current = visited_odd if dist % 2 else visited_even

            if to_visit:
                to_visit.append('UP')
            continue

        if position in visited_odd or position in visited_even:
            continue

        visited_current.add(position)
        x, y = position
        to_visit += {(x+dx, y+dy) for dx, dy in deltas if plots[y+dy][x+dx] != '#'}

    return cnt

def count_cross(plots: Plots):
    return 0

def count_diagonals(plots: Plots):
    return 0

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

    
    result = max(cnt for dist, cnt in achievable_count(plots, start_position).items() if dist % 2 == STEPS % 2)
    result += count_cross(plots)
    result += count_diagonals(plots)

    print(result)

run()
