from collections import Counter


def get_line(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()][0]


text = get_line()
count = Counter(text)

print(count['('] - count[')'])
