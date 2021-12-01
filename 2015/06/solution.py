def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_instructions():
    return [parse_instruction(line) for line in get_lines()]


def parse_instruction(line):
    splited = line.split()
    name = ' '.join(splited[:-3])
    from_point = parse_point(splited[-3])
    to_point = parse_point(splited[-1])

    return name, from_point, to_point


def parse_point(string):
    x, y = string.split(',')
    return int(x), int(y)


def create_empty_grid(size):
    return [[False] * size for _ in range(size)]


def execute(grid, instructions):

    for instruction in instructions:
        name, from_point, to_point = instruction
        operation = get_operation_by_name(name)
        operation(grid, from_point, to_point)


def get_operation_by_name(name):
    return {
        'turn on': do_on_square(lambda p: True),
        'turn off': do_on_square(lambda p: False),
        'toggle': do_on_square(lambda p: not p)
    }[name]


def do_on_square(operation):
    def aux(grid, from_point, to_point):
        from_x, from_y = from_point
        to_x, to_y = to_point

        for y in range(from_y, to_y + 1):
            for x in range(from_x, to_x + 1):
                grid[y][x] = operation(grid[y][x])

    return aux


def count_on(grid):
    return sum(map(
        lambda r: sum(r),
        grid
    ))


instructions = get_instructions()
grid = create_empty_grid(1000)
execute(grid, instructions)
result = count_on(grid)

print(result)
