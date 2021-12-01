def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def parse_line(line):
    variable, value_str = line.split(' = ')

    if variable == 'mask':
        and_mask = int(value_str.replace('1', '0').replace('X', '1'), base=2)
        mask_value = int(value_str.replace('X', '0'), base=2)
        return 'mask', and_mask, mask_value

    if variable[:3] == 'mem':
        memory_idx = int(variable[4:-1])
        return 'mem', memory_idx, int(value_str)

    raise Exception('wrong input')


def get_commands():
    return [parse_line(line) for line in get_lines()]


and_mask = None
mask_value = None
memory = {}

for command in get_commands():
    command_name = command[0]

    if command_name == 'mask':
        and_mask = command[1]
        mask_value = command[2]
        continue

    if command_name == 'mem':
        memory_idx = command[1]
        raw_value = command[2]
        masked_value = (raw_value & and_mask) + mask_value
        memory[memory_idx] = masked_value
        continue

    raise Exception('command undefined')

sum_of_values = sum(memory.values())
print(sum_of_values)
