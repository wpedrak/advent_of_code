from collections import deque
from itertools import combinations


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_parsed_lines():
    return [int(number) for number in get_lines()]


def is_sum_of_two(preamble, number):
    for x, y in combinations(preamble, 2):
        if x + y == number:
            return True

    return False


def get_breaking_number(xmas):
    preamble_length = 25
    preamble = deque(xmas[:preamble_length])

    for number in xmas[preamble_length:]:
        if is_sum_of_two(preamble, number):
            preamble.append(number)
            preamble.popleft()
            continue

        return number


xmas = get_parsed_lines()
breaking_number = get_breaking_number(xmas)
print(breaking_number)
