import re
from fractions import Fraction

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
        machines.append((ax, ay, bx, by, px + 10000000000000, py + 10000000000000))

    return machines

def win(machine: Machine)  -> int:
    ax, ay, bx, by, px, py = machine
    # A and B are the same (possibly scaled)
    if ax*by == bx*ay:
        if ax != bx:
            return -1    
        raise Exception(':<')
    
    b = Fraction(ax*py - px*ay, ax*by - bx*ay)
    a = Fraction(px - b*bx, ax)

    if a < 0 or b < 0:
        return -1
    
    if not a.is_integer() or not b.is_integer():
        return -1
    
    return 3 * a.as_integer_ratio()[0] + b.as_integer_ratio()[0]

def run() -> None:
    machines = read_machines()
    result = sum(tokens for m in machines if (tokens := win(m)) != -1)
    print(result)

run()
