def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def move(floor: list[list[str]]) -> None:
    to_move_right = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if floor[y][x] == '>'
        if floor[y][(x+1) % width] == '.'
    ]
    for x, y in to_move_right:
        floor[y][x] = '.'
        floor[y][(x+1) % width] = '>'

    to_move_left = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if floor[y][x] == 'v'
        if floor[(y+1) % height][x] == '.'
    ]
    for x, y in to_move_left:
        floor[y][x] = '.'
        floor[(y+1) % height][x] = 'v'

def hashable(floor: list[list[str]]) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(row) for row in floor)

def print_floor(floor: list[list[str]]) -> None:
    print('\n'.join(''.join(row) for row in floor))
    print('')

floor = [list(l) for l in get_lines()]
height = len(floor)
width = len(floor[0])

visited = set()
steps = 0
while hashable(floor) not in visited:
    visited.add(hashable(floor))
    move(floor)
    steps += 1

print(steps)
