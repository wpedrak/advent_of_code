from collections import deque

Point = tuple[int, int]
Plots = list[str]

STEPS = 26501365

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_plots() -> list[str]:
    lines = read_lines()
    plots: list[str] = []
    for line in lines:
        plots.append('#' + line + '#')
    width = len(plots[0])
    return ['#' * width] + plots + ['#' * width] 

def find_starting_plot(plots: Plots) -> Point:
    for y, row in enumerate(plots):
        try:
            x = row.index('S')
        except:
            continue
        return x, y
    
    raise Exception(':<')

def achievable_count(plots: Plots, start: Point) -> list[int]:
    deltas = [(1,0), (-1,0), (0,1), (0, -1)]
    dist = 0
    cnt: list[int] = []
    to_visit = deque([start, 'UP'])
    visited: set[Point] = set()
    
    while to_visit:
        position = to_visit.popleft()

        if isinstance(position, str):
            cnt.append(len(visited))
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

def count_cross(plots: Plots):
    map_size = len(plots) - 2

    top_mid: Point = (len(plots)//2, 1)
    mid_left: Point = (1, len(plots)//2)
    mid_right: Point = (len(plots)-2, len(plots)//2)
    bottom_mid: Point = (len(plots)//2, len(plots)-2)
    start_points: list[Point] = [top_mid, mid_left, mid_right, bottom_mid]

    result = 0
    for start_point in start_points:
        cnt = achievable_count(plots, start_point)
        result += count_path(map_size, cnt, STEPS - map_size//2 - 1)
    return result

def count_diagonals(plots: Plots):
    map_size = len(plots) - 2

    top_left: Point = (1, 1)
    top_right: Point = (len(plots)-2, 1)
    bottom_left: Point = (1, len(plots)-2)
    bottom_right: Point = (len(plots)-2, len(plots)-2)
    start_points: list[Point] = [top_left, top_right, bottom_left, bottom_right]

    result: int = 0
    for start_point in start_points:
        cnt = achievable_count(plots, start_point)

        # we will count quater: row by row starting from the closest to the start
        for steps_till_start in range(map_size + 2, STEPS + 1, map_size):
            result += count_path(map_size, cnt, STEPS - steps_till_start)

    return result

def count_path(map_size: int, cnt: list[int], remaining_steps: int) -> int:
    options_count = 0

    max_cnt = len(cnt) - 1
    full_map_cnt_even, full_map_steps_even = (cnt[-1], max_cnt) if is_even(max_cnt) else (cnt[-2], max_cnt-1)
    full_map_cnt_odd, full_map_steps_odd = (cnt[-1], max_cnt) if is_odd(max_cnt) else (cnt[-2], max_cnt-1)

    first_map_parity = (STEPS - remaining_steps) % 2

    # go till you can reach every point in the map
    # 1. go straight
    full_maps = remaining_steps // map_size
    remaining_steps -= full_maps * map_size
    # 2. it might be that we weren't able to reach every point in the last map, so go back 1 map
    pre_last_map_parity = (first_map_parity + full_maps - 1) % 2
    pre_last_map_full_steps = full_map_steps_even if is_even(pre_last_map_parity) else full_map_steps_odd
    if remaining_steps + map_size < pre_last_map_full_steps:
        options_count += cnt[remaining_steps]  # count very last map before going back
        full_maps -= 1
        remaining_steps += map_size

    # count the whole path
    options_count += full_maps//2 * full_map_cnt_even
    options_count += full_maps//2 * full_map_cnt_odd
    first_map_cnt = full_map_cnt_even if is_even(first_map_parity) else full_map_cnt_odd
    options_count += first_map_cnt if is_odd(full_maps) else 0
    # count the last map (possibly last AFTER taking step back)
    options_count += cnt[remaining_steps]

    return options_count

def is_even(n: int) -> bool:
    return n % 2 == 0

def is_odd(n: int) -> bool:
    return n % 2 == 1

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


    corner = (1, 1)
    mid_top = (len(plots)//2, 1)

    cnt1 = achievable_count(plots, corner)
    cnt2 = achievable_count(plots, mid_top)
    
    print(len(cnt1), cnt1[-5:])
    print(len(cnt2), cnt2[-5:])


    result = max(cnt for dist, cnt in enumerate(achievable_count(plots, start_position)) if dist % 2 == STEPS % 2)
    result += count_cross(plots)
    result += count_diagonals(plots)

    print(result)
    # so far failed with the following results
    assert 638110317012349 < result < 1278103017916873

# Example:
# In exactly 6 steps, he can still reach 16 garden plots.
# In exactly 10 steps, he can reach any of 50 garden plots.
# In exactly 50 steps, he can reach 1594 garden plots.
# In exactly 100 steps, he can reach 6536 garden plots.
# In exactly 500 steps, he can reach 167004 garden plots.
# In exactly 1000 steps, he can reach 668697 garden plots.
# In exactly 5000 steps, he can reach 16733044 garden plots.

run()
