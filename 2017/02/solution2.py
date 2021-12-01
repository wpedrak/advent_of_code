import itertools


def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


checksum = 0

for line in get_lines():
    numbers = [int(x) for x in line.split()]
    for n1, n2 in itertools.combinations(numbers, 2):
        if n1 % n2 == 0:
            checksum += n1 // n2
        if n2 % n1 == 0:
            checksum += n2 // n1

print(checksum)
