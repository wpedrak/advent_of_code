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

    result = 0
    for start_point in [(len(plots)//2, 1), (1, len(plots)//2), (len(plots)-2, len(plots)//2), (len(plots)//2, len(plots)-2)]:
        cnt = achievable_count(plots, start_point)
        full_map_cnt_even, full_map_steps_even = max((cnt, dist) for dist, cnt in enumerate(cnt) if not dist % 2)
        full_map_cnt_odd, full_map_steps_odd = max((cnt, dist) for dist, cnt in enumerate(cnt) if dist % 2)

        # max cnts should be at the end of cnt list
        assert {full_map_cnt_even, full_map_cnt_odd} == set(cnt[-2:])

        print(full_map_cnt_even, full_map_steps_even)
        print(full_map_cnt_odd, full_map_steps_odd)

        steps = STEPS
        # go til you leave first map
        steps -= map_size//2 + 1

        # go till you can reach every point in the map
        # 1. go straight
        full_maps = steps // map_size
        steps -= full_maps * map_size
        # 2. it might be that we weren't able to reach every point in the last map, so go back 1 map
        first_map_parity = (STEPS - map_size//2 - 1) % 2
        assert first_map_parity == 0
        pre_last_map_parity = (first_map_parity + full_maps - 1) % 2
        pre_last_map_full_steps = full_map_steps_even if pre_last_map_parity == 0 else full_map_steps_odd
        if steps + map_size < pre_last_map_full_steps:
            full_maps -= 1
            steps += map_size

        result += full_maps//2 * full_map_cnt_even
        result += full_maps//2 * full_map_cnt_odd
        first_map_cnt = full_map_cnt_even if first_map_parity == 0 else full_map_cnt_odd
        result += first_map_cnt if full_maps % 2 == 1 else 0
        result += cnt[steps]

    return result

def count_diagonals(plots: Plots):
    map_size = len(plots) - 2

    result = 0
    for start_point in [(1, 1), (len(plots)-2, 1), (1, len(plots)-2), (len(plots)-2, len(plots)-2)]:
        cnt = achievable_count(plots, start_point)
        full_map_cnt, full_map_steps = max((cnt, dist) for dist, cnt in enumerate(cnt) if dist % 2 == (STEPS - map_size - 1) % 2)

        print(full_map_cnt, full_map_steps)

        for steps_till_start in range(map_size + 1, STEPS, map_size):
            steps = STEPS - steps_till_start
     
            full_maps = steps // map_size
            steps -= full_maps * map_size
            result += cnt[steps]
            while steps + map_size < full_map_steps and full_maps > 0:
                steps += map_size
                full_maps -= 1
                result += cnt[steps]

            result += full_maps * full_map_cnt

    return result

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
    # so far the result is too low
    assert result > 638110317012349
    # TODO: account for changing parity when counting full maps

run()
