def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def parse_points():
    lines = get_lines()
    return [parse_point(line) for line in lines]


def parse_point(line):
    parts = line.split(', ')
    position_part = parts[0][3:-1]
    velocity_part = parts[1][3:-1]
    acceleration_part = parts[2][3:-1]
    position = parse_tiplet(position_part)
    velocity = parse_tiplet(velocity_part)
    acceleration = parse_tiplet(acceleration_part)

    return position, velocity, acceleration


def parse_tiplet(triplet):
    return [int(x) for x in triplet.split(',')]


def dist_to_zero(coordinates):
    return sum([abs(coordinate) for coordinate in coordinates])


def get_closest(points):
    acceleration_power = []
    for idx, point in enumerate(points):
        _, _, acceleration = point
        acceleration_dist = dist_to_zero(acceleration)
        acceleration_power.append((acceleration_dist, idx))

    return min(acceleration_power)[1]


points = parse_points()
closest = get_closest(points)

print(closest)
