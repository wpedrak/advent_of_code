def get_lines(filename='08/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


result = 0

for string in get_lines():
    result += len(string)
    result -= len(string.encode('utf-8').decode('unicode_escape')) - 2

print(result)
