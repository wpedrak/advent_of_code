DASH = [(x, 0) for x in range(4)]
PLUS = [(1, 2), (0, 1), (1, 1), (2, 1), (1, 0)]
L_SHAPE = [(2, 2), (2, 1), (0, 0), (1, 0), (2, 0)]
PIPE = [(0, y) for y in range(4)]
SQUARE = [(0, 1), (1, 1), (0, 0), (1, 0)]
SHAPES = [DASH, PLUS, L_SHAPE, PIPE, SQUARE]

AIR = '.'
STONE = '#'

def run() -> None:
    moves = read_lines()[0]
    chamber = [[AIR] * 7 for _ in range(2022*5)]
    insertion_point = (2, 3)
    move_nr = 0

    for shape_nr in range(2022):
        shape = SHAPES[shape_nr % 5]
        while can_insert(chamber, shape, insertion_point):
            insertion_point = move_to_side(chamber, shape, insertion_point, moves[move_nr % len(moves)])
            move_nr += 1
            insertion_point = (insertion_point[0], insertion_point[1]-1)

        insertion_point = (insertion_point[0], insertion_point[1]+1)
        insert(chamber, shape, insertion_point)
        insertion_point = (2, first_free_row(chamber, insertion_point[1]) + 3)

    print(insertion_point[1] - 3)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def can_insert(chamber: list[list[str]], shape: list[tuple[int, int]], insertion_point: tuple[int, int]):
    dx, dy = insertion_point
    width = len(chamber[0])
    for x, y in shape:
        if x+dx < 0 or x+dx >= width:
            return False
        if y+dy < 0:
            return False
        if chamber[y+dy][x+dx] == STONE:
            return False

    return True

def move_to_side(chamber: list[list[str]], shape: list[tuple[int, int]], insertion_point: tuple[int, int], move: str) -> tuple[int, int]:
    dx = {
        '<': -1,
        '>': 1,
    }[move]
    x, y = insertion_point

    if can_insert(chamber, shape, (x+dx, y)):
        return (x+dx, y)

    return (x, y)

def insert(chamber: list[list[str]], shape: list[tuple[int, int]], insertion_point: tuple[int, int]) -> None:
    x, y = insertion_point
    for dx, dy in shape:
        chamber[y+dy][x+dx] = STONE

def first_free_row(chamber: list[list[str]], hint: int) -> int:
    y = hint
    width = len(chamber[0])
    while any(chamber[y][x] == STONE for x in range(width)):
        y += 1

    return y

run()
