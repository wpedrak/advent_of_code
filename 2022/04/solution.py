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

result = 0
for a, b, c, d in parse_lines(read_lines()):
    first_contains_second = a <= c and d <= b
    second_contains_first = c <= a and b <= d
    result += first_contains_second or second_contains_first

print(result)
