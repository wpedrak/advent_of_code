from collections import defaultdict

def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [x.rstrip() for x in file]

lines = get_lines()
bits_counter = defaultdict(int)
for line in lines:
    for idx, bit in enumerate(line):
        bits_counter[(idx, bit)] += 1

gamma_rate = ''
epsilon_rate = ''
numbers_length = len(lines[0])
for idx in range(numbers_length):
    if bits_counter[(idx, '0')] > len(lines) / 2:
        gamma_rate += '0'
        epsilon_rate += '1'
        continue

    gamma_rate += '1'
    epsilon_rate += '0'

result = int(gamma_rate, base=2) * int(epsilon_rate, base=2)
print(result)
