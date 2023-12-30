import re
from typing import Callable
from collections import defaultdict

FoldFun = Callable[[int, int], int]

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

raw_program = open('input.txt', 'r', encoding='utf-8').read()
fold_program = parse_fold_program(raw_program)

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

print(min(zs[0]))
