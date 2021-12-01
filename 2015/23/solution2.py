IP = '_IP'


def get_lines(filename='23/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_program():
    return [parse_instruction(line) for line in get_lines()]


def parse_instruction(line):
    splited = line.split()
    splited[1] = splited[1].rstrip(',')

    name = splited[0]
    args = splited[1:]

    if name in ['jmp', 'jie', 'jio']:
        args[-1] = int(args[-1])

    return name, args


def get_fresh_env():
    return {
        'a': 0,
        'b': 0,
        IP: 0,
    }


def half(env, reg):
    env[reg] //= 2


def triple(env, reg):
    env[reg] *= 3


def increment(env, reg):
    env[reg] += 1


def jump(env, offset):
    env[IP] += offset


def jump_if_even(env, reg, offset):
    if env[reg] % 2 == 0:
        env[IP] += offset
        return

    env[IP] += 1


def jump_if_one(env, reg, offset):
    if env[reg] == 1:
        env[IP] += offset
        return

    env[IP] += 1


def run(instructions, program, env):
    while 0 <= env[IP] < len(program):
        instruction_pointer = env[IP]
        name, args = program[instruction_pointer]
        instruction = instructions[name]
        instruction(env, *args)
        if name not in ['jmp', 'jie', 'jio']:
            env[IP] += 1


instructions = {
    'hlf': half,
    'tpl': triple,
    'inc': increment,
    'jmp': jump,
    'jie': jump_if_even,
    'jio': jump_if_one,
}

env = get_fresh_env()
env['a'] = 1
program = get_program()
run(instructions, program, env)
print(env['b'])
