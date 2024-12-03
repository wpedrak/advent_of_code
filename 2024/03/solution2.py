import re

PATTERN = r'''(?x)
    mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)
    |do\(\)
    |don't\(\)
'''

def run() -> None:
    memory = open('input.txt', 'r', encoding='utf-8').read()
    do = True
    result = 0
    for match in re.finditer(PATTERN, memory):
        if match[0] == 'do()':
            do = True
            continue
        if match[0] == "don't()":
            do = False
            continue

        if do:
            result += int(match[1]) * int(match[2])

    print(result)

run()
