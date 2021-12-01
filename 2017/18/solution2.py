from collections import defaultdict, deque

PROGRAM_ID = 'program id'
IP = 'instruction pointer'
IN_QUEUE = 'in queue'
OUT_QUEUE = 'out queue'
SEND_COUNTER = 'send counter'
IS_LOCKED = 'is locked'

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


def set_val(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] = arg2
    env[IP] += 1


def add(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] += arg2
    env[IP] += 1


def mul(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] *= arg2
    env[IP] += 1


def mod(ip, env, arg1, arg2_raw):
    arg2 = retrieve(env, arg2_raw)
    env[arg1] %= arg2
    env[IP] += 1


def jgz(ip, env, arg1_raw, arg2_raw):
    arg1 = retrieve(env, arg1_raw)
    arg2 = retrieve(env, arg2_raw)

    if arg1 > 0:
        env[IP] += arg2
        return

    env[IP] += 1


def snd(ip, env, arg1_raw):
    arg1 = retrieve(env, arg1_raw)
    env[OUT_QUEUE].append(arg1)
    env[SEND_COUNTER] += 1
    env[IP] += 1


def rcv(ip, env, arg1):
    if not env[IN_QUEUE]:
        env[IS_LOCKED] = True
        return

    env[IS_LOCKED] = False
    value = env[IN_QUEUE].popleft()
    env[arg1] = value
    env[IP] += 1



def in_range(size, envs):
    return all(map(
        lambda e: 0 <= e[IP] < size,
        envs
    ))

def deadlocked(envs):
    return all(map(
        lambda e: e[IS_LOCKED],
        envs
    ))

def run(instructions, program):
    queue_0_to_1 = deque()
    queue_1_to_0 = deque()

    env0 = defaultdict(lambda: 0)
    env0['p'] = 0
    env0[PROGRAM_ID] = env0['p']
    env0[IN_QUEUE] = queue_1_to_0
    env0[OUT_QUEUE] = queue_0_to_1

    env1 = defaultdict(lambda: 0)
    env1['p'] = 1
    env1[PROGRAM_ID] = env1['p']
    env1[IN_QUEUE] = queue_0_to_1
    env1[OUT_QUEUE] = queue_1_to_0

    while in_range(len(program), [env0, env1]) and not deadlocked([env0, env1]):
        instruction_pointer0 = env0[IP]
        instruction_name0, args0 = program[instruction_pointer0]
        instruction0 = instructions[instruction_name0]
        instruction0(instruction_pointer0, env0, *args0)

        instruction_pointer1 = env1[IP]
        instruction_name1, args1 = program[instruction_pointer1]
        instruction1 = instructions[instruction_name1]
        instruction1(instruction_pointer1, env1, *args1)

    return env1[SEND_COUNTER]


instructions = {
    'snd': snd,
    'set': set_val,
    'add': add,
    'mul': mul,
    'mod': mod,
    'rcv': rcv,
    'jgz': jgz
}

program = parse_program(get_lines())

result = run(instructions, program)

print(result)
