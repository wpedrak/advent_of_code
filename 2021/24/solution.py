from collections import namedtuple

Operation = namedtuple('Operation', ['op', 'arg1', 'arg2'])

class Alu:
    def __init__(self) -> None:
        self.input: list[int] = []

    def set_input(self, input: list[int]) -> None:
        self.input = input[::-1]

    def __read_from_input(self) -> int:
        return self.input.pop()

    def run(self, program: list[Operation]) -> tuple[int, int, int, int]:
        state = {x: 0 for x in 'wxyz'}
        def val(x: int | str) -> int:
            return state[x] if x in state else x

        for operation in program:
            if operation.op == 'inp':
                state[operation.arg1] = self.__read_from_input()
            if operation.op == 'add':
                state[operation.arg1] += val(operation.arg2)
            if operation.op == 'mul':
                state[operation.arg1] *= val(operation.arg2)
            if operation.op == 'div':
                state[operation.arg1] //= val(operation.arg2)
                state[operation.arg1] += state[operation.arg1] < 0
            if operation.op == 'mod':
                state[operation.arg1] %= val(operation.arg2)
            if operation.op == 'eql':
                state[operation.arg1] = state[operation.arg1] == val(operation.arg2)

        return tuple(state[x] for x in 'wxyz')


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

def parse_program(lines: list[str]) -> list[Operation]:
    return [parse_operation(l) for l in lines]

program = parse_program(get_lines())
alu = Alu()
# alu.set_input([13])
# state = alu.run(program)
# print(state)
