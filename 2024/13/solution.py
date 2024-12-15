import re

Machine = tuple[int, int, int, int, int, int]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_machines() -> list[Machine]:
    lines = read_lines()
    machines = []
    for start in range(0, len(lines), 4):
        ax, ay = map(int, re.findall(r'\d+', lines[start]))
        bx, by = map(int, re.findall(r'\d+', lines[start+1]))
        px, py = map(int, re.findall(r'\d+', lines[start+2]))
        machines.append((ax, ay, bx, by, px, py))

    return machines

def win(machine: Machine):
    ax, ay, bx, by, px, py = machine
    win_tokens = []
    for a in range(101):
        remaining_x = px - ax * a
        remaining_y = py - ay * a

        if remaining_x % bx:
            continue
        b = remaining_x // bx

        if by * b != remaining_y:
            continue

        win_tokens.append(3*a + b)

    return min(win_tokens, default=-1)

def run() -> None:
    machines = read_machines()
    result = sum(tokens for m in machines if (tokens := win(m)) != -1)
    print(result)

run()
