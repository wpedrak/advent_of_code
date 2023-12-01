import re

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def find_calibration_number(string: str) -> int:
    digits = re.findall(r'\d', string)
    return int(digits[0]) *10 + int(digits[-1])

result = sum(find_calibration_number(l) for l in get_lines())
print(result)
