from collections import Counter


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_directions():
    return [parse_line(line) for line in get_lines()]


def parse_line(line):
    directions = []
    while line:
        begin = line[:2]
        if begin in ['se', 'sw', 'ne', 'nw']:
            directions.append(begin)
            line = line[2:]
            continue

        begin = line[0]
        if begin in ['e', 'w']:
            directions.append(begin)
            line = line[1:]
            continue

        raise Exception('parsing error')

    return directions


def follow_directions(direction_line):
    delta = {
        'se': (1, -3),
        'sw': (-1, -3),
        'ne': (1, 3),
        'nw': (-1, 3),
        'e': (2, 0),
        'w': (-2, 0),
    }

    x, y = 0, 0

    for directions in direction_line:
        dx, dy = delta[directions]
        x += dx
        y += dy

    return x, y


target_tiles = [follow_directions(directions) for directions in get_directions()]
counter = Counter(target_tiles)

black_tiles_number = 0

for count in counter.values():
    black_tiles_number += count % 2

print(black_tiles_number)
