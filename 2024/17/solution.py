IP = 0
REG_A = 1
REG_B = 2
REG_C = 3

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_registers():
    return [int(row.split()[-1]) for row in read_lines()[:3]]

def read_program():
    return [int(x) for x in read_lines()[-1].lstrip('Program: ').split(',')]

def combo(state: list[int], v: int) -> int:
    if v <= 3:
        return v
    return state[v-3]

def adv(state: list[int], v: int) -> None:
    state[REG_A] = state[REG_A] // (2**combo(state, v))
    state[IP] += 2

def bxl(state: list[int], v: int) -> None:
    state[REG_B] = state[REG_B] ^ v
    state[IP] += 2

def bst(state: list[int], v: int) -> None:
    state[REG_B] = combo(state, v) % 8
    state[IP] += 2

def jnz(state: list[int], v: int) -> None:
    if not state[REG_A]:
        state[IP] += 2
        return
    state[IP] = v

def bxc(state: list[int], v: int) -> None:
    state[REG_B] = state[REG_B] ^ state[REG_C]
    state[IP] += 2

def out(state: list[int], v: int) -> int:
    state[IP] += 2
    return combo(state, v) % 8

def bdv(state: list[int], v: int) -> None:
    state[REG_B] = state[REG_A] // (2**combo(state, v))
    state[IP] += 2

def cdv(state: list[int], v: int) -> None:
    state[REG_C] = state[REG_A] // (2**combo(state, v))
    state[IP] += 2

def run() -> None:
    a, b, c = read_registers()
    program = read_program()
    operations = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    state = [0, a, b, c]
    output = []


    while state[IP] < len(program):
        opcode, operand = program[state[IP]: state[IP]+2]
        op = operations[opcode]
        res = op(state, operand)
        if res is not None:
            output.append(res)

    print(','.join(map(str, output)))

run()
