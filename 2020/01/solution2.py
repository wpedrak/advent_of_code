from itertools import combinations


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


numbers = [int(x) for x in get_lines()]

for x, y, z in combinations(numbers, 3):
    if x + y + z == 2020:
        print(x * y * z)
