SPIN = 's'
EXCHANGE = 'x'
PARTNER = 'p'


def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def get_moves():
    lines = get_lines()
    return lines[0].split(',')


def parse_moves(moves):
    return [parse_move(m) for m in moves]


def parse_move(move):
    move_type = move[0]
    without_type = move[1:]
    if move_type == SPIN:
        return move_type, int(without_type), -1

    splited = without_type.split('/')
    arg1 = splited[0]
    arg2 = splited[1]

    if move_type == PARTNER:
        return move_type, arg1, arg2

    if move_type == EXCHANGE:
        return move_type, int(arg1), int(arg2)

    raise Exception(f'Wrong type:"{move_type}"')


def perform_move(programs, move):
    move_type = move[0]

    if move_type == SPIN:
        return spin(programs, move[1])

    if move_type == EXCHANGE:
        return exchange(programs, move[1], move[2])

    if move_type == PARTNER:
        return partner(programs, move[1], move[2])


def spin(programs, spin_size):
    if spin_size > 16:
        raise Exception('Nope')
    return programs[-spin_size:] + programs[:-spin_size]


def exchange(programs, pos1, pos2):
    programs_copy = programs[:]
    programs_copy[pos1] = programs[pos2]
    programs_copy[pos2] = programs[pos1]

    return programs_copy


def partner(programs, name1, name2):
    pos1 = programs.index(name1)
    pos2 = programs.index(name2)

    return exchange(programs, pos1, pos2)


moves = parse_moves(get_moves())
programs = list('abcdefghijklmnop')

for move in moves:
    programs = perform_move(programs, move)

print(''.join(programs))
