def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_directions():
    return [get_direction(line) for line in get_lines()]


def get_direction(line):
    return line[0], int(line[1:])


def rotate90clockwise(x, y):
    return y, -x


delta_map = {
    'N': (0, 1),
    'S': (0, -1),
    'W': (-1, 0),
    'E': (1, 0),
}

current_x = 0
current_y = 0
waypoint_x = 10
waypoint_y = 1

for command, value in get_directions():
    if command in delta_map:
        dx, dy = delta_map[command]
        waypoint_x += dx * value
        waypoint_y += dy * value
        continue

    if command == 'F':
        current_x += waypoint_x * value
        current_y += waypoint_y * value
        continue

    if command in 'LR':
        rotation = (value if command == 'R' else -value) % 360
        for _ in range(rotation // 90):
            waypoint_x, waypoint_y = rotate90clockwise(waypoint_x, waypoint_y)
        continue

    raise Exception(f'Unknown command: {command}, {value}')

print(current_x, current_y)
print(abs(current_x) + abs(current_y))
