import heapq

Point = tuple[int, int]
Priority = tuple[int, int, int]

SPLITTER = -1

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]


def move(manifold: list[list[int]], beam: Point, worlds: int) -> list[tuple[Point, int]]:
    x, y = beam
    if x==8 and y==11:
        pass
    if x < 0 or x >= len(manifold[0]) or y >= len(manifold):
        return []

    value = manifold[y][x]

    if value == SPLITTER:
        new_beams: list[tuple[Point, int]] = []
        if not manifold[y][x-1]:
            new_beams.append(((x-1, y), 0))
        manifold[y][x-1] += worlds

        if not manifold[y][x+1]:
            new_beams.append(((x+1, y), 0))
        manifold[y][x+1] += worlds

        return new_beams

    manifold[y][x] += worlds
    return [((x, y+1), manifold[y][x])]


def priority(manifold: list[list[int]], point: Point) -> Priority:
    x, y = point
    if x < 0 or x >= len(manifold[0]) or y >= len(manifold):
        return -1, -1, -1

    return y, manifold[y][x] != SPLITTER, x

def run() -> None:
    manifold_str = [list(line) for line in read_lines()]
    start_beam = (manifold_str[0].index('S'), 0)
    manifold = [[SPLITTER if v == '^' else 0 for v in row] for row in manifold_str]
    beams: list[tuple[Priority, Point, int]] = [(priority(manifold, start_beam), start_beam, 1)]
    visited: set[Point] = set()

    while beams:
        _, beam, worlds = heapq.heappop(beams)
        new_beams = move(manifold, beam, worlds)
        for new_beam, new_worlds in new_beams:
            if new_beam in visited:
                continue
            heapq.heappush(beams, (priority(manifold, new_beam), new_beam, new_worlds))
            visited.add(new_beam)

    result = sum(manifold[-1])
    print(result)

run()
