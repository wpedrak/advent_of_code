def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def is_valid(passphrase):
    lst = passphrase.split()
    return len(lst) == len(set(lst))

valid_count = 0

for line in get_lines():
    valid_count += is_valid(line)

print(valid_count)
