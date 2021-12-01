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


def get_summing_range(xmas, breaking_number):
    current_sum = xmas[0]
    from_idx = 0
    to_idx = 0

    while current_sum != breaking_number:
        if current_sum < breaking_number:
            to_idx += 1
            current_sum += xmas[to_idx]
            continue

        if current_sum > breaking_number:
            current_sum -= xmas[from_idx]
            from_idx += 1

    return from_idx, to_idx


xmas = get_parsed_lines()
breaking_number = get_breaking_number(xmas)
from_idx, to_idx = get_summing_range(xmas, breaking_number)
summing_slice = xmas[from_idx:to_idx]
result = min(summing_slice) + max(summing_slice)
print(result)
