import re


class ChristmasNumber:
    def __init__(self, number: int):
        self.number = number

    def __add__(self, other):
        return ChristmasNumber(self.number * other.number)

    def __mul__(self, other):
        return ChristmasNumber(self.number + other.number)


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_christmas_expressions():
    return [parse_christmas_expression(line) for line in get_lines()]


def parse_christmas_expression(line: str):
    expression = line.replace('*', '?').replace('+', '*').replace('?', '+')
    return re.sub(r'(\d+)', 'ChristmasNumber(\\1)', expression)


result = 0

for expression in get_christmas_expressions():
    result += eval(expression).number

print(result)
