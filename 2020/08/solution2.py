def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_line(line):
    operation, value = line.split()
    return operation, int(value)


def get_instructions():
    return [parse_line(line) for line in get_lines()]


def change_acc(ip, acc, value):
    acc += value
    ip += 1
    return acc, ip


def jmp(ip, acc, value):
    ip += value
    return acc, ip


def nop(ip, acc, value):
    ip += 1
    return acc, ip


def run(instructions, operations):
    instruction_pointer = 0
    acc = 0
    visited_instruction_pointers = {0}

    while 0 <= instruction_pointer < len(instructions):
        operation_name, value = instructions[instruction_pointer]
        operation = operations[operation_name]
        acc, instruction_pointer = operation(instruction_pointer, acc, value)

        if instruction_pointer in visited_instruction_pointers:
            return -1

        visited_instruction_pointers.add(instruction_pointer)

    if instruction_pointer != len(instructions):
        return -1

    return acc


def flip_jmp_nop(operation):
    return {
        'jmp': 'nop',
        'nop': 'jmp',
    }[operation]


operations = {
    'acc': change_acc,
    'jmp': jmp,
    'nop': nop,
}

instructions = get_instructions()

for idx, (operation, value) in enumerate(instructions):
    if operation not in ['jmp', 'nop']:
        continue

    flipped_operation = flip_jmp_nop(operation)
    instructions[idx] = (flipped_operation, value)
    acc_result = run(instructions, operations)
    instructions[idx] = (operation, value)

    if acc_result != -1:
        print(acc_result)
        break
