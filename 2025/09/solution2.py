import itertools

Tile = tuple[int, int]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]


def read_tiles():
    tiles: list[Tile] = []
    for line in read_lines():
        x, y = map(int, line.split(','))
        tiles.append((x, y))

    return tiles


def valid_rectangle(tiles: list[Tile], x1: int, y1: int, x2: int, y2: int) -> bool:
    x_min, x_max = min([x1, x2]), max([x1, x2])
    y_min, y_max = min([y1, y2]), max([y1, y2])

    for line_start, line_end in itertools.pairwise(tiles + [tiles[0]]):
        x_ls, y_ls = line_start
        x_le, y_le = line_end
        if x_ls <= x_min and x_le <= x_min:
            continue
        if x_max <= x_ls and x_max <= x_le:
            continue
        if y_ls <= y_min and y_le <= y_min:
            continue
        if y_max <= y_ls and y_max <= y_le:
            continue

        return False
    
    return True


def run() -> None:
    tiles = read_tiles()

    current_max = 0
    for idx1, (x1, y1) in enumerate(tiles):
        for idx2 in range(idx1+1, len(tiles)):
            x2, y2 = tiles[idx2]
            field = (abs(x1-x2)+1) * (abs(y1-y2)+1)
            if field <= current_max:
                continue

            if not valid_rectangle(tiles, x1, y1, x2, y2):
                continue

            current_max = field

    print(current_max)


run()
