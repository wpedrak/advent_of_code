import random, re
from typing import Callable
from collections import defaultdict

FoldFun = Callable[[int, int], int]

class Operation:
    def __init__(self, op: str, arg1: str, arg2: str | int) -> None:
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self) -> str:
        if self.op == 'inp':
            return f'{self.arg1} = input()'
        if self.op == 'eql':
            return f'{self.arg1} = {self.arg1} == {self.arg2}'
        op = {
            'add': '+=',
            'mul': '*=',
            'div': '//=',
            'mod': '%=',
        }[self.op]
        return f'{self.arg1} {op} {self.arg2}'

    def __repr__(self) -> str:
        return str(self)

def run_alu(program: list[Operation], inp: list[int], debug=False) -> dict[str, int]:
    inp = inp[::-1]
    state = {x: 0 for x in 'wxyz'}
    def val(x: int | str) -> int:
        return state[x] if x in state else x
    
    for idx, operation in enumerate(program):
        if operation.op == 'inp':
            state[operation.arg1] = inp.pop()
        elif operation.op == 'add':
            state[operation.arg1] += val(operation.arg2)
        elif operation.op == 'mul':
            state[operation.arg1] *= val(operation.arg2)
        elif operation.op == 'div':
            state[operation.arg1] //= val(operation.arg2)
            state[operation.arg1] += state[operation.arg1] < 0
        elif operation.op == 'mod':
            state[operation.arg1] %= val(operation.arg2)
        elif operation.op == 'eql':
            state[operation.arg1] = state[operation.arg1] == val(operation.arg2)

        if debug:
            print(f'{idx+1: <3}   {str(operation): <11} {state}')

    return state

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def safe_to_int(s: str) -> int | str:
    if s in 'wxyz':
        return s
    return int(s)

def parse_operation(line: str) -> Operation:
    split = line.split()
    if len(split) == 2:
        return Operation(split[0], split[1], None)
    op, arg1, arg2 = split
    return Operation(op, safe_to_int(arg1), safe_to_int(arg2))

def parse_alu_program(lines: list[str]) -> list[Operation]:
    return [parse_operation(l) for l in lines]

def find_fold_fun_args(input_str: str) -> list[tuple[int, int, int]]:
    program_section = r'''inp w
mul x 0
add x z
mod x 26
div z (\d+)
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (\d+)
mul y x
add z y'''
    return [tuple(int(g) for g in match.groups()) for match in re.finditer(program_section, input_str)]

def parse_fold_program(input_str: str) -> list[FoldFun]:
    return [genereate_digit_fun(*args) for args in find_fold_fun_args(input_str)]

def digits_to_int(digits: list[int]) -> int:
    res = 0
    for digit in digits:
        res *= 10
        res += digit
    return res

def int_to_digits(number: int) -> list[int]:
    digits = []
    while number:
        digits.append(number % 10)
        number //= 10
    return digits[::-1]

def genereate_digit_fun(arg1: int, arg2: int, arg3: int) -> FoldFun:
    def digit_fun(digit: int, z: int) -> int:
        reminder = z % 26
        z //= arg1
        
        if (reminder + arg2) == digit:    
            return z

        z *= 26
        z += digit + arg3        
        return z

    return digit_fun

def run_fold(program: list[FoldFun], digits: list[int]) -> int:
    z = 0
    for f, digit in zip(program, digits):
        z = f(digit, z)
    return z

raw_program = open('input.txt', 'r', encoding='utf-8').read()
alu_program = parse_alu_program(get_lines())
fold_program = parse_fold_program(raw_program)

if True:
    random.seed(314)
    for _ in range(1000):
        model_number = random.randint(10_000_000_000_000, 99_999_999_999_999)
        alu_result = run_alu(alu_program, int_to_digits(model_number))['z']
        fold_result = run_fold(fold_program, int_to_digits(model_number))
        if alu_result != fold_result:
            print(f'for model number {model_number}: {alu_result} != {fold_result}')
            exit(1)
    print('tests passed')

z_reduction = [arg[0] for arg in find_fold_fun_args(raw_program)]
z_limit = z_reduction[::-1]
cumulative = 1
for idx in range(len(z_limit)):
    cumulative *= z_limit[idx]
    z_limit[idx] = cumulative
z_limit = z_limit[::-1]

zs = {0: [0]}
for num, (f, limit) in enumerate(zip(fold_program, z_limit)):
    new_zs = defaultdict(list)
    for z in zs:
        for digit in range(1, 10):
            new_z = f(digit, z)
            if new_z >= limit:
                continue
            new_zs[new_z] += [prev_digits * 10 + digit for prev_digits in zs[z]]
    zs = new_zs
    print(num, len(zs))

print(max(zs[0]))
