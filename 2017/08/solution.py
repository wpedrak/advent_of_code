from collections import defaultdict


def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def parse_instructions(lines):
    return [parse_instruction(line) for line in lines]


class Instruction:
    def __init__(self, register, operation, value, condition):
        self.register = register
        operation_multiplier = 1 if operation == 'inc' else -1
        self.value = int(value) * operation_multiplier
        self.condition = condition

    def execute(self, env):
        if not self.condition.holds(env):
            return

        env[self.register] += self.value


class Condition:
    def __init__(self, register, operation, value):
        self.register = register
        self.operation = operation
        self.value = int(value)

    def holds(self, env):
        reg_value = env[self.register]

        if self.operation == '>':
            return reg_value > self.value
        if self.operation == '<':
             return reg_value < self.value
        if self.operation == '>=':
             return reg_value >= self.value
        if self.operation == '<=':
             return reg_value <= self.value
        if self.operation == '==':
             return reg_value == self.value
        if self.operation == '!=':
             return reg_value != self.value

        raise Exception('wrong operation')

def parse_instruction(line):
    splited = line.split()
    condition = Condition(*splited[4:])
    instruction_args = splited[:3] + [condition]
    return Instruction(*instruction_args)


instructions = parse_instructions(get_lines())

environment = defaultdict(lambda: 0)

for instruction in instructions:
    instruction.execute(environment)

result = max(environment.values())
print(result)
