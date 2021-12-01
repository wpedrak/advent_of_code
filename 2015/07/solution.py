CONST = 'CONST'
NOT = 'NOT'
AND = 'AND'
OR = 'OR'
LSHIFT = 'LSHIFT'
RSHIFT = 'RSHIFT'


def get_lines(filename='07/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_gates():
    return [parse_gate(line) for line in get_lines()]


def parse_gate(line):
    description, output = line.split(' -> ')
    description_by_word = description.split()
    if len(description_by_word) == 1:
        return CONST, output, [cast_if_int(description_by_word[0])]

    snd_arg = cast_if_int(description_by_word[-1])

    if len(description_by_word) == 2:
        return NOT, output, [snd_arg]

    fst_arg = cast_if_int(description_by_word[0])
    operation = description_by_word[1]

    return operation, output, [fst_arg, snd_arg]


def cast_if_int(string):
    if string.isnumeric():
        return int(string)
    return string


def solve():
    sources = {output: (operation_name, args) for operation_name, output, args in get_gates()}
    env = {}
    evaluate(sources, env, 'a')
    return env['a']


def evaluate(descriptions, env, value):
    if type(value) == int:
        return value

    if value in env:
        return env[value]

    operation_name, args = descriptions[value]
    args_values = [evaluate(descriptions, env, arg) for arg in args]
    operation = get_operation_by_name(operation_name)
    env[value] = operation(*args_values)

    return env[value]


def get_operation_by_name(name):
    return {
        CONST: int,
        NOT: lambda x: ~x % 2**16,
        AND: lambda x, y: x & y,
        OR: lambda x, y: x | y,
        LSHIFT: lambda x, y: (x << y) % 2**16,
        RSHIFT: lambda x, y: x >> y
    }[name]


result = solve()
print(result)
