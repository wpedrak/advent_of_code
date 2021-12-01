from collections import defaultdict


class Point:
    def __init__(self, x, y, z, dx, dy, dz, ax, ay, az):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.ax = ax
        self.ay = ay
        self.az = az
        self.destroyed = False

    def tick(self):
        self.dx += self.ax
        self.dy += self.ay
        self.dz += self.az
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    def get_position(self):
        return (self.x, self.y, self.z)

    def is_destroyed(self):
        return self.destroyed

    def destroy(self):
        self.destroyed = True


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
    all_params = position + velocity + acceleration

    return Point(*all_params)


def parse_tiplet(triplet):
    return [int(x) for x in triplet.split(',')]


def dist_to_zero(coordinates):
    return sum([abs(coordinate) for coordinate in coordinates])


def emulate(points):
    points_count = len(points)
    while True:
        positions = defaultdict(lambda: [])
        for point in points:
            point.tick()
            positions[point.get_position()].append(point)

        for grouped_points in positions.values():
            if len(grouped_points) <= 1:
                continue
            for point in grouped_points:
                point.destroy()

        points_count_after_tick = sum(map(
            lambda p: not p.is_destroyed(),
            points
        ))

        if points_count > points_count_after_tick:
            points_count = points_count_after_tick
            print(points_count)

points = parse_points()
emulate(points)
