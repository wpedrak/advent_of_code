PIXEL_ON = '#'


class Rule:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def match(self, arr):
        return arr == self.source


def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def parse_rules():
    lines = get_lines()
    return [parse_rule(line) for line in lines]


def parse_rule(line):
    splited = line.split(' => ')
    return Rule(*splited)


def count_set_pixels(art):
    row_sums = [sum(map(
        lambda p: p == PIXEL_ON,
        row
    )) for row in art]
    return sum(row_sums)


def transform_n_times(rules, art_arg, iterations):
    art = [row[:] for row in art_arg]
    for time in range(iterations):
        print(time)
        art = transform(rules, art)

    return art


def transform(rules, art):
    size = len(art)
    split_size = 2 if size % 2 == 0 else 3
    new_size = size + (size // split_size)
    new_art = [[] for _ in range(new_size)]
    y_offset = 0

    for y in range(0, size, split_size):
        for x in range(0, size, split_size):
            art_slice = get_slice(art, x, y, split_size)
            enchancmented_slice = match(rules, art_slice)
            insert_slice(new_art, enchancmented_slice, y + y_offset)

        y_offset += 1

    return new_art


def get_slice(art, begin_x, begin_y, split_size):
    art_slice = []

    for y in range(begin_y, begin_y + split_size):
        slice_row = art[y][begin_x:begin_x + split_size]
        art_slice.append(slice_row)

    return art_slice


def insert_slice(new_art, enchancmented_slice, y):
    for idx, row in enumerate(enchancmented_slice):
        new_art[y+idx] += row


def match(rules, art_slice):
    options = flip_and_rotate(art_slice)

    matches = set()

    for option in options:
        option_str = arr_to_str(option)
        for rule in rules:
            if not rule.match(option_str):
                continue

            matches.add(rule.target)

    if len(matches) != 1:
        raise Exception('Found wrong number of matches')

    return str_to_arr(list(matches)[0])

def flip_and_rotate(array):
    flipped = flip(array)

    return spins(array) + spins(flipped)

def flip(array):
    return [list(reversed(row)) for row in array]

def spins(array):
    all_spins = []
    to_spin = array
    for _ in range(4):
        to_spin = spin90(to_spin)
        all_spins.append(to_spin)

    return all_spins

def spin90(array):
    size = len(array)
    spinned = [[None] * size for _ in range(size)]

    for y in range(size):
        for x in range(size):
            spinned[y][x] = array[x][size-y-1]

    return spinned



def arr_to_str(array):
    return '/'.join([''.join(row) for row in array])


def str_to_arr(string):
    return [list(row) for row in string.split('/')]


art = [
    ['.', '#', '.'],
    ['.', '.', '#'],
    ['#', '#', '#']
]
rules = parse_rules()

transformed_art = transform_n_times(rules, art, 18)
result = count_set_pixels(transformed_art)

print(result)
