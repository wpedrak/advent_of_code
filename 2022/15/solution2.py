import re

pnt = tuple[int, int]

def run() -> None:
    signals = parse_signals(read_lines())
    y = find_y(signals)
    print('y =', y)
    transposed_signals = [((s[1], s[0]), (b[1], b[0])) for s, b in signals]
    x = find_y(transposed_signals)
    print('x =', x)
    print(x*4000000 + y)

def find_y(signals: list[tuple[pnt, pnt]]) -> None:
    for y in range(4000001):
        if not y % 100000:
            print(f'{y//100000}/{40}')
        if can_put_beacon_in_row(signals, y):
            return y

    raise Exception('Not found')

def can_put_beacon_in_row(signals: list[tuple[pnt, pnt]], y: int) -> bool:
    intervals = []
    for signal in signals:
        x1, x2 = square_line_intersect(signal[0], manhatan(signal[0], signal[1]), y)
        if (x1, x2) != (None, None):
            intervals.append((max(x1, 0), min(x2, 4000000)))

    no_becon_places = 0

    # counted_ptr points to the place after the last concidered x
    counted_ptr = 0
    for x1, x2 in sorted(intervals):
        counted_ptr = max(counted_ptr, x1)
        if counted_ptr > x2:
            continue
        no_becon_places += x2 - counted_ptr + 1
        counted_ptr = x2 + 1

    return no_becon_places < 4000001

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_signals(lines: list[str]) -> list[tuple[pnt, pnt]]:
    return [parse_signal(l) for l in lines]

def parse_signal(line: str) -> tuple[pnt, pnt]:
    str_coordinates = re.findall(r'-?\d+', line)
    sx, sy, bx, by = map(int, str_coordinates)
    return ((sx, sy), (bx, by))

def manhatan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def square_line_intersect(middle: pnt, radius: int, y: int) -> tuple[int, int]:
    dist_to_y = abs(middle[1] - y)
    if radius < dist_to_y:
        return None, None

    remaining_range = radius - dist_to_y
    return (middle[0] - remaining_range, middle[0] + remaining_range)

run()
