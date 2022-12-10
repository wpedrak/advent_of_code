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
print('#', end='')
original_commands = [parse_command(l) for l in read_lines()]
commands = add_noops(original_commands)
for command, number in commands:
    if command == 'addx':
        x_register += number

    if x_register <= (cycle % 40) + 1 <= x_register + 2:
        print('#', end='')
    else:
        print('.', end='')

    cycle += 1
    if cycle % 40 == 0:
        print('')
