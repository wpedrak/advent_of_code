def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_lines(lines: list[str]) -> list[tuple[int, int, int, int]]:
    return [parse_line(l) for l in lines]

def parse_line(line: str) -> tuple[int, int, int, int]:
    first, second = line.split(',')
    first_from = int(first.split('-')[0])
    first_to = int(first.split('-')[1])
    second_from = int(second.split('-')[0])
    second_to = int(second.split('-')[1])

    return first_from, first_to, second_from, second_to

lines = read_lines()
result = len(lines)
for a, b, c, d in parse_lines(lines):
    dont_overlap = b < c or a > d
    result -= dont_overlap

print(result)
