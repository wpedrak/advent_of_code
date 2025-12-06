Range = tuple[int, int]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_input() -> list[Range]:
    lines = read_lines()
    split_index = lines.index('')

    ranges: list[Range] = []
    for line in lines[:split_index]:
        x, y = line.split('-')
        ranges.append((int(x), int(y)))

    return ranges

def run() -> None:
    ranges= read_input()
    points = sorted([x for r in ranges for x in [(r[0], 'LEFT'), (r[1], 'RIGHT')]])
    starts: list[int] = []
    
    result = 0
    for value, side in points:
        if side == 'LEFT':
            starts.append(value)
            continue

        start = starts.pop()
        if starts:
            continue

        result += value - start + 1

    print(result)

run()
