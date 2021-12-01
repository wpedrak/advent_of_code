from itertools import combinations


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


numbers = [int(x) for x in get_lines()]

for x, y in combinations(numbers, 2):
    if x + y == 2020:
        print(x * y)
