def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [x.rstrip() for x in file]


def max_bit(numbers, idx):
    ones = sum(n[idx] == '1' for n in numbers)
    return '1' if ones >= len(numbers)/2 else '0'


def min_bit(numbers, idx):
    return str(1 - int(max_bit(numbers, idx)))


def bit_filter(numbers, f):
    numbers = numbers[:]
    number_size = len(numbers[0])
    for idx in range(number_size):
        bit = f(numbers, idx)
        numbers = [n for n in numbers if n[idx] == bit]
        if len(numbers) == 1:
            return numbers[0]

    raise Exception('Not filtered to 1')


lines = get_lines()
oxygen = bit_filter(lines, max_bit)
co2 = bit_filter(lines, min_bit)
print(oxygen, co2)
result = int(oxygen, base=2) * int(co2, base=2)
print(result)
