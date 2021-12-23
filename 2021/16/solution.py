def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_message() -> str:
    return get_lines()[0]

def to_bits(hex: str) -> str:
    return ''.join(f'{int(c, base=16):04b}' for c in hex)

def sum_versions(message: str) -> int:
    pass

hex_message = get_message()
message = to_bits(hex_message)
result = sum_versions(message)
print(result)
