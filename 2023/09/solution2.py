import re

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def extrapolate(seq: list[int]) -> int:
    seq = seq[:]
    first_numbers = [seq[0]]
    while any(x != 0 for x in seq):
        seq = [b-a for a, b in zip(seq, seq[1:])]
        first_numbers.append(seq[0])

    result = 0
    for number in reversed(first_numbers):
        result = number - result

    return result

result = 0
for line in get_lines():
    sequence = [int(n) for n in re.findall(r'-?\d+', line)]
    result += extrapolate(sequence)

print(result)