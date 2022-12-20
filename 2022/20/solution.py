def run() -> None:
    # idx is for distinguishing equal numbers
    original_numbers = [(int(l), idx) for idx, l in enumerate(read_lines())]
    numbers = original_numbers[:]

    for number in original_numbers:
        idx = numbers.index(number)
        del numbers[idx]
        insert_position = (idx+number[0]) % len(numbers)
        numbers.insert(insert_position, number)

    zero_idx = find_zero(numbers)
    a = numbers[(zero_idx + 1000) % len(numbers)][0]
    b = numbers[(zero_idx + 2000) % len(numbers)][0]
    c = numbers[(zero_idx + 3000) % len(numbers)][0]

    print(f'{a}+{b}+{c}={a+b+c}')

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def find_zero(numbers: list[tuple[int, int]]) -> int:
    for idx, n in enumerate(numbers):
        if n[0] == 0:
            return idx

    raise Exception('No zero')

run()
