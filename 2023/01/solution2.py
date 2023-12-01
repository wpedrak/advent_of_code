import re

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def find_calibration_number(string: str) -> int:
    # a?=(b|c) looks for "a" followed by "b" or "b" and reports "a".
    # I enclose it in the parenthesis to form group and keep the match after ?=
    # The only purpose of using ?= is to not consume the pattern and allow for overlapping matches
    digits = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', string)
    return to_int(digits[0]) * 10 + to_int(digits[-1])

def to_int(s: str) -> int:
    numbers = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    if s in numbers:
        s = numbers[s]
    return int(s)

result = sum(find_calibration_number(l) for l in get_lines())
print(result)
