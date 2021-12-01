import re


def get_lines(filename='08/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


result = 0

for string in get_lines():
    result += len(re.escape(string)) + 2
    result -= len(string)

print(result)
