def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def get_hash(string: str) -> int:
    current_value = 0
    for char in string:
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value

steps = get_lines()[0].split(',')
result = sum(get_hash(s) for s in steps)
print(result)
