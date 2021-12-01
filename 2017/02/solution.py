def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [ line.strip() for line in f.readlines()]

checksum = 0

for line in get_lines():
    numbers = [int(x) for x in line.split()]
    diff = max(numbers) - min(numbers)
    checksum += diff

print(checksum)