def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_message() -> str:
    return get_lines()[0]

def to_bits(hex: str) -> str:
    return ''.join(f'{int(c, base=16):04b}' for c in hex)

def sum_versions(message: str) -> tuple[int, int]:
    version_sum = 0
    version = int(message[:3], base=2)
    version_sum += version
    type_id = int(message[3:6], base=2)
    
    if type_id == 4:
        _, length = read_literal(message[6:])
        return version_sum, 6 + length

    length_type_id = int(message[6])
    offset = 11 if length_type_id else 15
    nesting_size = int(message[7:7+offset], base=2)
    nested_message = message[7+offset:]
    read_bytes = 7+offset

    while nesting_size > 0:
        nested_sum, nested_bytes = sum_versions(nested_message)
        version_sum += nested_sum
        read_bytes += nested_bytes
        nesting_size -= 1 if length_type_id else nested_bytes
        nested_message = nested_message[nested_bytes:]

    return version_sum, read_bytes

def read_literal(message: str) -> tuple[int, int]:
    still_read = True
    offset = 0
    while still_read:
        still_read = message[offset] == '1'
        offset += 5
    return -1, offset
            

hex_message = get_message()
message = to_bits(hex_message)
result, _ = sum_versions(message)
print(result)
