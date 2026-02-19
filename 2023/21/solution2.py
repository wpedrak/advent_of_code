from collections import deque

Point = tuple[int, int]
Plots = list[str]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_plots(filename: str = 'input.txt') -> list[str]:
    return wrapped(read_lines(filename=filename))

def wrapped(plots: list[str]) -> list[str]:
    wrapped_plots: list[str] = []
    for row in plots:
        wrapped_plots.append('#' + row + '#')
    width = len(wrapped_plots[0])
    return ['#' * width] + wrapped_plots + ['#' * width] 

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
    visited_even: set[Point] = set()
    visited_odd: set[Point] = set()
    visited = visited_even
    
    while to_visit:
        position = to_visit.popleft()

        if isinstance(position, str):
            if not to_visit:
                break

            to_visit.append('UP')
            cnt.append(len(visited))
            dist += 1
            visited = visited_even if is_even(dist) else visited_odd
            continue

        if position in visited:
            continue

        visited.add(position)
        x, y = position
        to_visit += {(x+dx, y+dy) for dx, dy in deltas if plots[y+dy][x+dx] != '#'}

    return cnt

def count_cross(plots: Plots, total_steps: int):
    map_size = len(plots) - 2

    top_mid: Point = (len(plots)//2, 1)
    mid_left: Point = (1, len(plots)//2)
    mid_right: Point = (len(plots)-2, len(plots)//2)
    bottom_mid: Point = (len(plots)//2, len(plots)-2)
    start_points: list[Point] = [top_mid, mid_left, mid_right, bottom_mid]

    result = 0
    for start_point in start_points:
        cnt = achievable_count(plots, start_point)
        result += count_path(map_size, cnt, total_steps - map_size//2 - 1)
    return result

def count_diagonals(plots: Plots, total_steps: int):
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
        for steps_till_start in range(map_size + 2, total_steps + 1, map_size):
            result += count_path(map_size, cnt, total_steps - steps_till_start)

    return result

def count_path(map_size: int, cnt: list[int], remaining_steps: int) -> int:
    options_count = 0

    max_cnt = len(cnt) - 1
    full_map_cnt_even, full_map_steps_even = (cnt[-1], max_cnt) if is_even(max_cnt) else (cnt[-2], max_cnt-1)
    full_map_cnt_odd, full_map_steps_odd = (cnt[-1], max_cnt) if is_odd(max_cnt) else (cnt[-2], max_cnt-1)

    first_map_is_even = is_even(remaining_steps)

    # go till you can reach every point in the map
    # 1. go straight
    full_maps = remaining_steps // map_size
    remaining_steps -= full_maps * map_size
    # 2. it might be that we weren't able to reach every point in the last map, so go back 1 map
    pre_last_map_is_even = is_even(first_map_is_even + full_maps - 1)
    pre_last_map_full_steps = full_map_steps_even if pre_last_map_is_even else full_map_steps_odd
    if remaining_steps + map_size < pre_last_map_full_steps:
        options_count += cnt[remaining_steps]  # count very last map before going back
        full_maps -= 1
        remaining_steps += map_size

    # count the whole path
    options_count += full_maps//2 * full_map_cnt_even
    options_count += full_maps//2 * full_map_cnt_odd
    first_map_cnt = full_map_cnt_even if first_map_is_even else full_map_cnt_odd
    options_count += first_map_cnt if is_odd(full_maps) else 0
    # count the last map (possibly last AFTER taking step back)
    options_count += cnt[remaining_steps]

    return options_count

def is_even(n: int) -> bool:
    return n % 2 == 0

def is_odd(n: int) -> bool:
    return n % 2 == 1


def count_options(plots: list[str], total_steps: int):
    start_position = find_starting_plot(plots)

    # plots shape is odd-sized square
    assert len(plots) == len(plots[0]) and len(plots) % 2
    # start point is in the middle
    assert start_position == (len(plots) // 2, len(plots) // 2)
    # there is a cross of '.' that has 'S' in the middle
    assert '#' not in {row[start_position[0]] for row in plots[1:-1]}
    assert '#' not in set(plots[start_position[1]][1:-1])

    cnt = achievable_count(plots, start_position)
    full_map_cnt_even = cnt[-1] if is_even(len(cnt)-1) else cnt[-2]
    full_map_cnt_odd = cnt[-1] if is_odd(len(cnt)-1) else cnt[-2]

    result = full_map_cnt_even if is_even(total_steps) else full_map_cnt_odd
    result += count_cross(plots, total_steps)
    result += count_diagonals(plots, total_steps)

    return result

def count_options_naive(plots: list[str], total_steps: int):
    plots = [row[1:-1] for row in plots[1:-1]]
    scale_factor = (total_steps  // len(plots)) + 1
    big_plots = [row * scale_factor for _ in range(scale_factor) for row in plots]
    return achievable_count(wrapped(big_plots), (len(big_plots) // 2, len(big_plots) // 2))[total_steps]

def run() -> None:
    plots = read_plots()
    result = count_options(plots, 26501365)
    print(result)
    # so far failed with the following results
    assert 638110317012349 < result < 1278103017916873


def test_unit():
    plots1 = [
        '#######',
        '#.....#',
        '#.#.#.#',
        '#.....#',
        '#.#.#.#',
        '#.....#',
        '#######',
    ]
    corner_cnt = [1, 2, 3, 6, 6, 10, 8, 12, 9]
    edge_cnt = [1, 3, 4, 8, 7, 12, 9]
    assert achievable_count(plots1, (1,1)) == corner_cnt
    assert achievable_count(plots1, (5,1)) == corner_cnt
    assert achievable_count(plots1, (1,5)) == corner_cnt
    assert achievable_count(plots1, (5,5)) == corner_cnt
    assert achievable_count(plots1, (3,3)) == [1, 4, 5, 12, 9]
    assert achievable_count(plots1, (3,1)) == edge_cnt
    assert achievable_count(plots1, (1,3)) == edge_cnt
    assert achievable_count(plots1, (5,3)) == edge_cnt
    assert achievable_count(plots1, (3,5)) == edge_cnt

    assert count_path(5, corner_cnt, 3) == 6
    assert count_path(5, corner_cnt, 5) == 10 + 1
    assert count_path(5, corner_cnt, 6) == 8 + 2

def test_hard():
    plots = read_plots()
    for steps in range(100):
        print(steps, end=' ')
        smart = count_options(plots, steps)
        naive = count_options_naive(plots, steps)
        print(naive, end='')
        if smart != naive:
            print('', smart, end='')
        print('')


def experiment():
    plots = read_plots(filename="example.txt")

    corner = (1, 1)
    mid_top = (len(plots)//2, 1)

    cnt1 = achievable_count(plots, corner)
    cnt2 = achievable_count(plots, mid_top)
    
    print(len(cnt1), cnt1[::2])
    print(len(cnt1), cnt1[1::2])
    print(len(cnt2), cnt2[::2])
    print(len(cnt2), cnt2[1::2])
    print(sum(sum(x in '.S' for x in row) for row in plots))



# Example:
# In exactly 6 steps, he can still reach 16 garden plots.
# In exactly 10 steps, he can reach any of 50 garden plots.
# In exactly 50 steps, he can reach 1594 garden plots.
# In exactly 100 steps, he can reach 6536 garden plots.
# In exactly 500 steps, he can reach 167004 garden plots.
# In exactly 1000 steps, he can reach 668697 garden plots.
# In exactly 5000 steps, he can reach 16733044 garden plots.

# run()
# experiment()
test_hard()