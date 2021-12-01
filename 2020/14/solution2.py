def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_all_fillings(value_str):
    x_number = sum(map(
        lambda x: x == 'X',
        value_str
    ))
    x_positions = [idx for idx, digit in enumerate(value_str) if digit == 'X']
    x_powers = [35 - idx for idx in x_positions]

    fillings = []

    for number_to_embed in range(2 ** x_number):
        binary_repr = f"{number_to_embed:036b}"[-x_number:]
        number = 0
        for digit, x_power in zip(binary_repr, x_powers):
            number += int(digit) * (2 ** x_power)

        fillings.append(number)

    return fillings


def parse_line(line):
    variable, value_str = line.split(' = ')

    if variable == 'mask':
        or_mask = int(value_str.replace('X', '0'), base=2)
        and_mask = int(value_str.replace('0', '1').replace('X', '0'), base=2)
        mask_values = get_all_fillings(value_str)
        return 'mask', or_mask, and_mask, mask_values

    if variable[:3] == 'mem':
        memory_idx = int(variable[4:-1])
        return 'mem', memory_idx, int(value_str)

    raise Exception('wrong input')


def get_commands():
    return [parse_line(line) for line in get_lines()]


if __name__ == '__main__':
    and_mask = None
    or_mask = None
    mask_values = None
    memory = {}

    for command in get_commands():
        command_name = command[0]

        if command_name == 'mask':
            or_mask = command[1]
            and_mask = command[2]
            mask_values = command[3]
            continue

        if command_name == 'mem':
            raw_memory_idx = command[1]
            value = command[2]
            for mask_value in mask_values:
                masked_memory_idx = ((raw_memory_idx | or_mask) & and_mask) + mask_value
                memory[masked_memory_idx] = value

            continue

        raise Exception('command undefined')

    sum_of_values = sum(memory.values())
    print(sum_of_values)
