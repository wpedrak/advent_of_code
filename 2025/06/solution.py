def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_worksheet() -> list[list[str]]:
    lines = read_lines()

    separators_set = set(range(len(lines[0])))
    for line in lines:
        separators_set &= {y for y, item in enumerate(line) if item == ' '}

    separators: list[int] = sorted(separators_set) + [len(lines[0])]
    worksheet: list[list[str]] = []
    for line in lines:
        row: list[str] = []
        idx_start = 0
        for idx_end in separators:
            row.append(line[idx_start : idx_end])
            idx_start = idx_end + 1

        worksheet.append(row)
    
    return worksheet

def mul(numbers: list[int]) -> int:
    result = 1
    for n in numbers:
        result *= n

    return result

def run() -> None:
    worksheet = read_worksheet()
    total_sum = 0

    for x in range(len(worksheet[0])):
        numbers: list[int] = []
        for y in range(len(worksheet)-1):
            numbers.append(int(worksheet[y][x]))

        last_y = len(worksheet) - 1
        if '+' in worksheet[last_y][x]:
            total_sum += sum(numbers)
        elif '*' in worksheet[last_y][x]:
            total_sum += mul(numbers)
        else:
            raise Exception(':<')

    print(total_sum)    

run()
