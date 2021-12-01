from collections import defaultdict

LAST_PLAYED_SOUND = 'last played sound'
NOT_PLAYED = 'Not played'
RECOVERED = 'recovered'


def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def parse_program(lines):
    return [parse_line(line) for line in lines]


def parse_line(line):
    splited = line.split()
    return splited[0], splited[1:]


def retrieve(env, arg):
    if arg.isalpha():
        return env[arg]

    return int(arg)


def snd(ip, env, arg1_raw):
    arg1 = retrieve(env, arg1_raw)
    env[LAST_PLAYED_SOUND] = arg1
    return ip + 1


def set_val(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] = arg2
    return ip + 1


def add(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] += arg2
    return ip + 1


def mul(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] *= arg2
    return ip + 1


def mod(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] %= arg2
    return ip + 1


def rcv(ip, env, arg1_raw):
    arg1 = retrieve(env, arg1_raw)
    if arg1:
        env[RECOVERED] += 1

    return ip + 1


def jgz(ip, env, arg1_raw, arg2_raw):
    arg1 = retrieve(env, arg1_raw)
    arg2 = retrieve(env, arg2_raw)

    if arg1 > 0:
        return ip + arg2

    return ip + 1


def run(instructions, program, env):
    instruction_pointer = 0

    env[LAST_PLAYED_SOUND] = NOT_PLAYED

    while 0 <= instruction_pointer < len(program):
        instruction_name, args = program[instruction_pointer]
        instruction = instructions[instruction_name]

        instruction_pointer = instruction(instruction_pointer, env, *args)

        if env[RECOVERED]:
            return env[LAST_PLAYED_SOUND]

    raise Exception('Failed to recover sound')


instructions = {
    'snd': snd,
    'set': set_val,
    'add': add,
    'mul': mul,
    'mod': mod,
    'rcv': rcv,
    'jgz': jgz
}

env = defaultdict(lambda: 0)
program = parse_program(get_lines())

result = run(instructions, program, env)

print(result)
