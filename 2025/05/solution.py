Range = tuple[int, int]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_input() -> tuple[list[Range], list[int]]:
    lines = read_lines()
    split_index = lines.index('')

    ranges: list[Range] = []
    for line in lines[:split_index]:
        x, y = line.split('-')
        ranges.append((int(x), int(y)))

    ids = [int(l) for l in lines[split_index + 1:]]

    return ranges, ids

def run() -> None:
    ranges, ids = read_input()
    fresh = 0
    for item_id in ids:
        fresh += any(r[0] <= item_id <= r[1] for r in ranges)

    print(fresh)

run()
