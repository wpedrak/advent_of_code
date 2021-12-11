def get_lines(filename='input.txt'):
    return [line.rstrip() for line in open(filename, 'r')]

def get_displays():
    return [get_display(l) for l in get_lines()]

def get_display(line: str) -> tuple[list[str], list[str]]:
    all_numbers, message = line.split(' | ')
    return all_numbers.split(), message.split()

unique_digit_count = 0

for _, message in get_displays():
    for digit in message:
        if len(digit) not in [2, 3, 4, 7]:
            continue
        unique_digit_count += 1

print(unique_digit_count)
