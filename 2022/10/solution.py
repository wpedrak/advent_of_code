def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_command(line: str) -> tuple[str, int | None]:
    parts = line.split(' ')
    number = int(parts[1]) if len(parts) > 1 else None
    return parts[0], number

def add_noops(commands: list[tuple[str, int | None]]) -> list[tuple[str, int | None]]:
    new_commands = []
    for command in commands:
        if command[0] == 'addx':
            new_commands.append(('noop', None))
        new_commands.append(command)

    return new_commands

cycle = 1
x_register = 1
power = 0
original_commands = [parse_command(l) for l in read_lines()]
commands = add_noops(original_commands)
for command, number in commands:
    if cycle % 40 == 20:
        power += cycle * x_register
    if command == 'addx':
        x_register += number
    cycle += 1

print(power)
