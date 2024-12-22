def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_program():
    return [int(x) for x in read_lines()[-1].lstrip('Program: ').split(',')]

def execute_pure(a: int) -> str:
    '''rewritten int-code without any reorganisations'''
    b = 0
    c = 0
    out = []
    while a:
        b = a & 7  # bst 4
        b ^= 1  # bxl 1
        c = a >> b  # cdv 5
        b ^= 5  # bxl 5
        a >>= 3  # adv 3
        b ^= c  # bxc 4
        out.append(b & 7)  # out 5
        #jnz 0

    return ','.join(map(str, out))

def single_output(a: int) -> str:
    # take last 3 bits
    b = a & 7
    # flip last bit
    b ^= 1
    c = a >> b
    # revert last bit and flip first one
    b ^= 5
    b ^= c
    return b & 7
    

def viable_inputs(targets: list[int]) -> int:
    possible_numbers = [0]

    for target in targets:
        possible_numbers = [pn*8+byte for pn in possible_numbers for byte in range(8) if single_output(pn*8+byte) == target]
        
    return min(possible_numbers)
    

def visualise() -> None:
    program = read_program()
    name = ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv']

    for opcode, operand in zip(program[::2], program[1::2]):
        print(name[opcode], operand)

def run() -> None:
    program = read_program()
    result = viable_inputs(list(reversed(program)))
    print(result)

run()
# visualise()
