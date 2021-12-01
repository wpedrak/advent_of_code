IP = '_IP'


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


def set_val(env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] = arg2
    env[IP] += 1


def sub(env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] -= arg2
    env[IP] += 1


def mul(env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] *= arg2
    env[IP] += 1


def jnz(env, arg1_raw, arg2_raw):
    arg1 = retrieve(env, arg1_raw)
    arg2 = retrieve(env, arg2_raw)

    if arg1 != 0:
        env[IP] += arg2
        return

    env[IP] += 1


def print_env(env):
    for k, v in sorted(env.items()):
        print(f'{k}: {v}, ', end='')
    print('')


def run(instructions, program):
    env = {x: 0 for x in 'bcdefgh'}
    env[IP] = 0
    env['a'] = 1

    while 0 <= env[IP] < len(program):
        print_env(env)

        instruction_pointer = env[IP]
        instruction_name, args = program[instruction_pointer]
        instruction = instructions[instruction_name]
        instruction(env, *args)


    return env['h']


instructions = {
    'set': set_val,
    'sub': sub,
    'mul': mul,
    'jnz': jnz
}

program = parse_program(get_lines())

result = run(instructions, program)

print(result)
