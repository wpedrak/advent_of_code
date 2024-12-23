import re

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def run() -> None:
    towels = read_lines()[0]
    pattern = re.compile(f'({towels.replace(', ', '|')})*')

    result = 0
    for design in read_lines()[2:]:
        result += re.fullmatch(pattern, design) is not None

    print(result)

run()
