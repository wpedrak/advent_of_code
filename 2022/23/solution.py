from collections import Counter

ELF = '#'

NORTH = 'N'
SOUTH = 'S'
WEST = 'W'
EAST = 'E'

def run() -> None:
    elves = set()
    for y, row in enumerate(read_lines()):
        for x, field in enumerate(row):
            if field == ELF:
                elves.add((x, y))

    order = [NORTH, SOUTH, WEST, EAST]
    for _ in range(10):
        elves = move(elves, order)
        order = order[1:] + order[:1]

    min_x = min(e[0] for e in elves)
    max_x = max(e[0] for e in elves)
    x_range = max_x - min_x + 1

    min_y = min(e[1] for e in elves)
    max_y = max(e[1] for e in elves)
    y_range = max_y - min_y + 1

    print(x_range * y_range - len(elves))


def print_elves(elves: set[tuple[int, int]]) -> None:
    min_x = min(e[0] for e in elves)
    max_x = max(e[0] for e in elves)
    min_y = min(e[1] for e in elves)
    max_y = max(e[1] for e in elves)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            field = '#' if (x, y) in elves else '.'
            print(field, end='')
        print('')
    print('')

def move(elves: set[tuple[int, int]], order: list[str]) -> set[tuple[int, int]]:
    ordered_elves = list(elves)
    targets = [proposition(elves, order, elf) for elf in ordered_elves]
    cnt = Counter(targets)
    new_elves = set()

    for elf, target in zip(ordered_elves, targets):
        if cnt[target] > 1:
            new_elves.add(elf)
            continue
        new_elves.add(target)

    return new_elves

def proposition(elves: set[tuple[int, int]], order: list[str], elf: tuple[int, int]) -> tuple[int, int]:
    if is_alone(elves, elf):
        return elf

    for direction in order:
        neighbours = find_neighbours(elf, direction)
        if all(n not in elves for n in neighbours):
            return neighbours[1]

    return elf

def is_alone(elves: set[tuple[int, int]], elf: tuple[int, int]) -> bool:
    x, y = elf
    return sum((x+dx, y+dy) in elves for dx in range(-1, 2) for dy in range(-1, 2)) == 1

def find_neighbours(elf: tuple[int, int], direction: str) -> list[tuple[int, int]]:
    x, y = elf
    return {
        NORTH: [(x-1, y-1), (x, y-1), (x+1, y-1)],
        SOUTH: [(x-1, y+1), (x, y+1), (x+1, y+1)],
        WEST: [(x-1, y-1), (x-1, y), (x-1, y+1)],
        EAST: [(x+1, y-1), (x+1, y), (x+1, y+1)],
    }[direction]

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(file_name, 'r', encoding='utf-8')]

run()
