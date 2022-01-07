def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_cuboids() -> list[tuple[int, int, int, int, int, int, bool]]:
    return [parse_cuboid(l) for l in get_lines()]

def parse_cuboid(line: str) -> tuple[int, int, int, int, int, int, bool]:
    state, coordinates = line.split(' ')
    xs, ys, zs = [get_range(c) for c in coordinates.split(',')]

    return state == 'on', xs[0], xs[1], ys[0], ys[1], zs[0], zs[1]

def get_range(range_str: str) -> tuple[int, int]:
    from_str, to_str = range_str[2:].split('..')
    return int(from_str), int(to_str)


reactor = [[[False] * 101 for _ in range(101)] for _ in range(101)]

for on, x1, x2, y1, y2, z1, z2 in get_cuboids():
    if x1 < -50 or y1 < -50 or z1 < -50:
        continue
    if x2 > 50 or y2 > 50 or z2 > 50:
        continue
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                reactor[z][y][x] = on

print(sum(sum(sum(r1d) for r1d in r2d) for r2d in reactor))
