import re
import itertools

Point = tuple[int, int]
Shape = str
Line = tuple[Point, Point, Shape]

SHAPE_Z: Shape = "Z"
SHAPE_U: Shape = "U"

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def get_instructions() -> list[tuple[str, int]]:
    instructions = []
    for line in get_lines():
        hex_dist, number_direction = re.findall(r'\(#([0-9a-f]{5})([0-9a-f])\)', line)[0]
        instructions.append(('RDLU'[int(number_direction)], int(hex_dist, base=16)))

    return instructions

def calculate_points() -> list[Point]:
    currect_point = (0, 0)
    points: set[tuple[int, int]] = [currect_point]
    for direction, steps in get_instructions():
        dx, dy = {
            'U': (0, steps),
            'D': (0, -steps),
            'L': (-steps, 0),
            'R': (steps, 0),
        }[direction]
        x, y = currect_point
        currect_point = (x+dx, y+dy)
        points.append(currect_point)
    
    return points

def find_lines(points: list[Point]) -> tuple[list[Line], list[Line]]:
    horizontal = []
    vertical = []
    directions = [direction for direction, _ in get_instructions()]
    directions_left_shift = [directions[-1]] + directions[:-1]
    directions_right_shift = directions[1:] + [directions[0]]

    for (point1, point2), dir_left, dir_right in zip(itertools.pairwise(points), directions_left_shift, directions_right_shift):
        point_from = min(point1, point2)
        point_to = max(point1, point2)
        shape = SHAPE_Z if dir_left == dir_right else SHAPE_U
        line = (point_from, point_to, shape)
        if point1[0] == point2[0]:
            vertical.append(line)
            continue
        if point1[1] == point2[1]:
            horizontal.append(line)
            continue

        raise Exception(':<')
    
    return vertical, horizontal

def count_in_loop_length(vertical_lines: list[Line], y_from: int, y_to: int) -> int:
    intersecting_xs = sorted([start[0] for start, end, _ in vertical_lines if start[1] <= y_from and end[1] >= y_to])
    assert len(intersecting_xs) % 2 == 0
    result = 0
    for x1, x2 in zip(intersecting_xs[::2], intersecting_xs[1::2]):
        result += x2 - x1 + 1
    return result

def count_in_loop_length_with_horizontal(vertical_lines: list[Line], horizontal_lines: list[Line], y: int):
    horizontal_lines_on_y = [hl for hl in horizontal_lines if hl[0][1] == y]
    horizontal_lines_xs = {x for start, end, _ in horizontal_lines_on_y for x in (start[0], end[0])}
    intersecting_xs = [x for start, end, _ in vertical_lines if start[1] <= y and end[1] >= y if (x := start[0]) not in horizontal_lines_xs]
    items_on_y = sorted(horizontal_lines_on_y + intersecting_xs, key=lambda x: x if isinstance(x, int) else x[0][0])
    assert len(items_on_y) > 0

    result, inside, prev_x = process_item(items_on_y[0], False, 0)

    for item in items_on_y[1:]:
        item_result, inside, prev_x = process_item(item, inside, prev_x)
        result += item_result

    return result

def process_item(item: int | Line, is_inside: bool, prev_x: int):
    if isinstance(item, int):
        x = item
        return x - prev_x + 1 if is_inside else 0, not is_inside, x

    p_from, p_to, shape = item
    x_from, x_to = p_from[0], p_to[0]
    
    dist = 0
    if shape == SHAPE_Z and is_inside:
        dist = x_to - prev_x + 1
    if shape == SHAPE_Z and not is_inside:
        dist = x_to - x_from
    if shape == SHAPE_U and is_inside:
        dist = x_to - prev_x
    if shape == SHAPE_U and not is_inside:
        dist = x_to - x_from + 1
    
    if shape == SHAPE_Z:
        is_inside = not is_inside

    return dist, is_inside, x_to

def run() -> None:
    points = calculate_points()
    vertical_lines, horizontal_lines = find_lines(points)
    ys = sorted({y for x, y in points})
    result = 0

    for y1, y2 in itertools.pairwise(ys + [ys[-1] + 1]):
        # loop iteration covers interval [y1, y2)

        # covers [y1, y1]
        result += count_in_loop_length_with_horizontal(vertical_lines, horizontal_lines, y1)
        
        # covers (y1, y2)
        height = y2 - y1 - 1
        result += height * count_in_loop_length(vertical_lines, y1+1, y2-1)

    print(result)

run()
