from time import time

class Point():
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return (f'({self.x}, {self.y}, {self.z})')

    __repr__ = __str__

class Cuboid():
    def __init__(self, min_point: Point, max_point: Point, on: bool) -> None:
        self.min_point = min_point
        self.max_point = max_point
        self.on = on

    def intersects(self, cuboid) -> bool:
        if cuboid.max_point.x < self.min_point.x or cuboid.min_point.x > self.max_point.x:
            return False

        if cuboid.max_point.y < self.min_point.y or cuboid.min_point.y > self.max_point.y:
            return False

        if cuboid.max_point.z < self.min_point.z or cuboid.min_point.z > self.max_point.z:
            return False

        return True

    def volume(self) -> int:
        dx = self.max_point.x - self.min_point.x + 1
        dy = self.max_point.y - self.min_point.y + 1
        dz = self.max_point.z - self.min_point.z + 1

        return dx * dy * dz

    def xs(self) -> tuple[int, int]:
        return self.min_point.x, self.max_point.x

    def ys(self) -> tuple[int, int]:
        return self.min_point.y, self.max_point.y

    def zs(self) -> tuple[int, int]:
        return self.min_point.z, self.max_point.z

    def __contains__(self, point: Point):
        return (
            self.min_point.x <= point.x <= self.max_point.x and
            self.min_point.y <= point.y <= self.max_point.y and
            self.min_point.z <= point.z <= self.max_point.z
        )

    def __str__(self) -> str:
        return (f'<{self.on}, {self.min_point}, {self.max_point}>')

    __repr__ = __str__


def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_cuboids() -> list[Cuboid]:
    return [parse_cuboid(l) for l in get_lines()]

def parse_cuboid(line: str) -> Cuboid:
    state, coordinates = line.split(' ')
    xs, ys, zs = [get_range(c) for c in coordinates.split(',')]
    point_from = Point(xs[0], ys[0], zs[0])
    point_to = Point(xs[1], ys[1], zs[1])

    return Cuboid(point_from, point_to, state == 'on')

def get_range(range_str: str) -> tuple[int, int]:
    from_str, to_str = range_str[2:].split('..')
    return int(from_str), int(to_str)

def pop_all_intersecting(cuboid: Cuboid, cuboids: list[Cuboid]) -> list[Cuboid]:
    intersecting_cuboids = [(idx, c) for idx, c in enumerate(cuboids) if cuboid.intersects(c)]
    for idx, _ in reversed(intersecting_cuboids):
        del cuboids[idx]

    return [c for _, c in intersecting_cuboids]

def do_intersections(cuboid: Cuboid, not_intersecting_cuboids: list[Cuboid]) -> list[Cuboid]:
    cuboids = [cuboid]

    while cuboids:
        cuboid = cuboids.pop()
        intersecting_cuboid = pop_first_intersecting(cuboid, not_intersecting_cuboids)
        
        if not intersecting_cuboid and not cuboid.on:
            continue

        if not intersecting_cuboid:
            not_intersecting_cuboids.append(cuboid)
            continue

        exploded_cuboids = explode(intersecting_cuboid, cuboid)
        cuboids += exploded_cuboids

    return not_intersecting_cuboids

def pop_first_intersecting(cuboid: Cuboid, cuboids: list[Cuboid]) -> Cuboid or None:
    for cuboid2 in cuboids:
        if cuboid.intersects(cuboid2):
            idx = cuboids.index(cuboid2)
            del cuboids[idx]
            return cuboid2

    return None

def explode(c1: Cuboid, c2: Cuboid) -> list[Cuboid]:
    x_ranges = ranges(c1.xs(), c2.xs())
    y_ranges = ranges(c1.ys(), c2.ys())
    z_ranges = ranges(c1.zs(), c2.zs())

    explosion = []
    for x1, x2 in x_ranges:
        for y1, y2 in y_ranges:
            for z1, z2 in z_ranges:
                p1 = Point(x1, y1, z1)
                p2 = Point(x2, y2, z2)

                if p1 in c2:
                    explosion.append(Cuboid(p1, p2, c2.on))
                    continue

                if p1 in c1:
                    explosion.append(Cuboid(p1, p2, c1.on))
                    continue                

    return explosion

def ranges(r1: tuple[int, int], r2: tuple[int, int]) -> list[tuple[int, int]]:
    a, b, c, d = sorted([r1[0], r1[1], r2[0], r2[1]])
    almost_ranges = [
        (a, b-1),
        (b, c),
        (c+1, d),
    ]

    return [r for r in almost_ranges if r[0] <= r[1]]


cuboids = get_cuboids()
not_intersecting_cuboids = []

next_update_time = time() + 1
exec_time = 0

for idx, cuboid in enumerate(cuboids):
    print(idx)
    intersecting_cuboids = pop_all_intersecting(cuboid, not_intersecting_cuboids)
    not_intersecting_cuboids += do_intersections(cuboid, intersecting_cuboids)

print(sum(c.volume() for c in not_intersecting_cuboids))
