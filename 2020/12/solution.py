def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_directions():
    return [get_direction(line) for line in get_lines()]


def get_direction(line):
    return line[0], int(line[1:])


delta_map = {
    'N': (0, 1),
    'S': (0, -1),
    'W': (-1, 0),
    'E': (1, 0),
}

rotation_to_direction_map = {
    0: 'E',
    90: 'S',
    180: 'W',
    270: 'N',
}

current_x = 0
current_y = 0
current_rotation = 0

for command, value in get_directions():
    if command in delta_map:
        dx, dy = delta_map[command]
        current_x += dx * value
        current_y += dy * value
        continue

    if command == 'F':
        current_direction = rotation_to_direction_map[current_rotation]
        dx, dy = delta_map[current_direction]
        current_x += dx * value
        current_y += dy * value
        continue

    if command in 'LR':
        rotation = value if command == 'R' else -value
        current_rotation += rotation
        current_rotation %= 360
        continue

    raise Exception(f'Unknown command: {command}, {value}')

print(current_x,  current_y)
print(abs(current_x) + abs(current_y))
