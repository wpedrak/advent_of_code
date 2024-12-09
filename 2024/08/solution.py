import itertools

class Antenna:
    def __init__(self, type: str, x: int, y: int) -> None:
        self.type = type
        self.x = x
        self.y = y

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_antennas() -> list[Antenna]:
    return [Antenna(item, x, y) 
        for y, row in enumerate(read_lines())
        for x, item in enumerate(row)
        if item != '.']

def get_dimmensions() -> tuple[int, int]:
    lines = read_lines()
    return len(lines[0]), len(lines)

def run() -> None:
    antennas = read_antennas()
    width, height = get_dimmensions()
    
    antinodes = set()
    for a1, a2 in itertools.combinations(antennas, 2):
        if a1.type != a2.type:
            continue
        antinodes.add((a1.x*2 - a2.x, a1.y*2 - a2.y))
        antinodes.add((a2.x*2 - a1.x, a2.y*2 - a1.y))

    print(sum(0 <= a[0] < width and 0 <= a[1] < height for a in antinodes))

run()
