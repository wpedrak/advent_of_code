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
        'se': (1, -1),
        'sw': (-1, -1),
        'ne': (1, 1),
        'nw': (-1, 1),
        'e': (2, 0),
        'w': (-2, 0),
    }

    x, y = 0, 0

    for directions in direction_line:
        dx, dy = delta[directions]
        x += dx
        y += dy

    return x, y


def get_changeable(black_tiles):
    return list(black_tiles) + [coordinate for black_tile in black_tiles for coordinate in get_neighbours(black_tile)]


def get_black_neighbours_count(black_tiles, coordinates):
    neighbours_set = set(get_neighbours(coordinates))

    return len(black_tiles & neighbours_set)


def get_neighbours(coordinate):
    delta = [
        (1, -1),
        (-1, -1),
        (1, 1),
        (-1, 1),
        (2, 0),
        (-2, 0),
    ]

    x, y = coordinate

    return [(x + dx, y + dy) for dx, dy in delta]


def tick(old_black_tiles):
    new_black_tiles = set()
    changeable_coordinates = get_changeable(old_black_tiles)

    for coordinates in changeable_coordinates:
        black_neighbours_count = get_black_neighbours_count(old_black_tiles, coordinates)

        if coordinates in old_black_tiles and black_neighbours_count in [1, 2]:
            new_black_tiles.add(coordinates)
            continue

        if coordinates not in old_black_tiles and black_neighbours_count == 2:
            new_black_tiles.add(coordinates)

    return new_black_tiles


def print_grid(black_tiles):
    max_x = max(black_tiles, key=lambda c: c[0])[0]
    min_x = min(black_tiles, key=lambda c: c[0])[0]
    max_y = max(black_tiles, key=lambda c: c[1])[1]
    min_y = min(black_tiles, key=lambda c: c[1])[1]

    print(min_x, min_y)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (abs(x) + abs(y)) % 2:
                print(' ', end='')
                continue
            if (x, y) in black_tiles:
                print('X', end='')
                continue
            print('.', end='')
        print()


if __name__ == '__main__':
    target_tiles = [follow_directions(directions) for directions in get_directions()]
    counter = Counter(target_tiles)

    black_tiles = set()
    for coordinates, count in counter.items():
        if count % 2:
            black_tiles.add(coordinates)

    for _ in range(100):
        black_tiles = tick(black_tiles)

    print(len(black_tiles))
