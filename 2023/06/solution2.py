import math
import re

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

lines = get_lines()
time = int(re.search('\d+', lines[0].replace(' ', ''))[0])
distance = int(re.search('\d+', lines[1].replace(' ', ''))[0])

# a*x^2 + b*x + c
a, b, c = -1, time, -distance
delta = b * b - 4 * a * c
solution_1 = (-b + math.sqrt(delta)) / 2*a
solution_2 = (-b - math.sqrt(delta)) / 2*a
min_valid = math.ceil(min(solution_1, solution_2) + 1e-10)
max_valid = math.floor(max(solution_1, solution_2) - 1e-10)

print(max_valid - min_valid + 1)
