import itertools

def get_lines(filename='2021/08/input.txt'):
    return [line.rstrip() for line in open(filename, 'r')]

def get_displays():
    return [get_display(l) for l in get_lines()]

def get_display(line: str) -> tuple[list[str], list[str]]:
    all_numbers, message = line.split(' | ')
    return all_numbers.split(), message.split()

def decode(numbers: list[str], message: list[str]) -> int:
    mapping = guess_mapping(numbers)
    translated_message = translate(mapping, message)
    return int(''.join(str(display(x)) for x in translated_message))

def guess_mapping(numbers: list[str]) -> dict[str, str]:
    letters = 'abcdefg'
    for perm in itertools.permutations(letters):
        mapping = dict(zip(perm, letters))
        if not fits(mapping, numbers):
            continue
        return mapping

    raise Exception('failed to guess mapping')

def fits(mapping: dict[str, str], numbers: list[str]) -> bool:
    new_numbers = translate(mapping, numbers)
    return set(display(n) for n in new_numbers) == set(range(9+1))

def translate(mapping: dict[str, str], numbers: list[str]) -> list[str]:
    return [
        ''.join(mapping[letter] for letter in number) 
        for number in numbers
    ]

def display(number: str) -> int:
    to_int = {
        'abcefg': 0,
        'cf': 1,
        'acdeg': 2,
        'acdfg': 3,
        'bcdf': 4,
        'abdfg': 5,
        'abdefg': 6,
        'acf': 7,
        'abcdefg': 8,
        'abcdfg': 9,
    }
    sorted_number = ''.join(sorted(number))
    if sorted_number not in to_int:
        return -1
    return to_int[sorted_number]

result = 0
for idx, (numbers, message) in enumerate(get_displays()):
    if idx % 10 == 0:
        print(idx)
    result += decode(numbers, message)

print(result)
