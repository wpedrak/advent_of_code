Tile = tuple[int, int]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_tiles():
    tiles: list[Tile] = []
    for line in read_lines():
        x, y = map(int, line.split(','))
        tiles.append((x, y))

    return tiles

def run() -> None:
    tiles = read_tiles()
    result = max((abs(t1[0]-t2[0])+1) * (abs(t1[1]-t2[1])+1) for t1 in tiles for t2 in tiles)
    print(result)

run()
