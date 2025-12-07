Point = tuple[int, int]


def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]


def move(manifold: list[list[str]], beam: Point) -> list[Point]:
    x, y = beam
    if x < 0 or x >= len(manifold[0]) or y >= len(manifold):
        return []

    match manifold[y][x]:
        case '|':
            return []
        case 'S' | '.':
            manifold[y][x] = '|'
            return [(x, y+1)]
        case '^':
            return [(x-1, y), (x+1, y)]
        case _:
            raise Exception(':<')

def run() -> None:
    manifold = [list(line) for line in read_lines()]
    beams = [(manifold[0].index('S'), 0)]

    splits = 0
    while beams:
        beam = beams.pop()
        new_beams = move(manifold, beam)
        splits += len(new_beams) == 2
        beams += new_beams

    print(splits)

run()
