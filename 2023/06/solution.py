import math
import re

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

lines = get_lines()
times = [int(n) for n in re.findall('\d+', lines[0])]
distances = [int(n) for n in re.findall('\d+', lines[1])]

result = 1
for time, distance in zip(times, distances):
    # a*x^2 + b*x + c
    a, b, c = -1, time, -distance
    delta = b * b - 4 * a * c
    solution_1 = (-b + math.sqrt(delta)) / 2*a
    solution_2 = (-b - math.sqrt(delta)) / 2*a
    min_valid = math.ceil(min(solution_1, solution_2) + 1e-10)
    max_valid = math.floor(max(solution_1, solution_2) - 1e-10)
    result *= (max_valid - min_valid + 1)

print(result)
