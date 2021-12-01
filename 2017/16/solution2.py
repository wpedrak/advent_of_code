SPIN = 's'
EXCHANGE = 'x'
PARTNER = 'p'
BILION = 1000000000

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

def dance(moves, programs):
    for move in moves:
        programs = perform_move(programs, move)
    return programs

moves = parse_moves(get_moves())
programs = list('abcdefghijklmnop')

visited = set([''.join(programs)])
visited_seq = [''.join(programs)]

for time in range(BILION % 36): # 36 is loop size
    programs = dance(moves, programs)
    programs_str = ''.join(programs)
    if programs_str in visited:
        idx = visited_seq.index(programs_str)
        print(idx)
        print(time)
        break
    visited.add(programs_str)
    visited_seq.append(programs_str)

print(''.join(programs))
