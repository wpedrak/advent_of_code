def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_marker(word):
    marker = [0] * 26

    for letter in word:
        marker[ord(letter) - ord('a')] += 1

    return tuple(marker)

def is_valid(passphrase):
    lst = [get_marker(word) for word in  passphrase.split()]
    return len(lst) == len(set(lst))

valid_count = 0

for line in get_lines():
    valid_count += is_valid(line)

print(valid_count)
