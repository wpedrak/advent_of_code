def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def split_into_two_parts(lines: list[str]):
    empty_idx = lines.index('')
    return lines[:empty_idx], lines[empty_idx+1:]

def parse_stacks(lines: list[str]) -> list[list[str]]:
    # drop numbers
    lines = lines[:-1]
    stacks = [[] for _ in range(10)]
    for line in lines:
        for idx, letter in enumerate(line[1::4]):
            if letter == ' ':
                continue
            stacks[idx+1].append(letter)

    return [list(reversed(s)) for s in stacks]

def parse_commands(lines: list[str]) -> list[tuple[int, int, int]]:
    return [parse_command(l) for l in lines]

def parse_command(line: str) -> tuple[int, int, int]:
    parts = line.split(' ')
    return int(parts[1]), int(parts[3]), int(parts[5])

stacks_lines, commands_lines = split_into_two_parts(read_lines())
stacks = parse_stacks(stacks_lines)
commands = parse_commands(commands_lines)

for count, source, target in commands:
    for _ in range(count):
        stacks[target].append(stacks[source].pop())

result = ''.join(s[-1] for s in stacks if s)
print(result)
