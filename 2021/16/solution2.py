import functools

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_message() -> str:
    return get_lines()[0]

def to_bits(hex: str) -> str:
    return ''.join(f'{int(c, base=16):04b}' for c in hex)

def eval_bits(message: str) -> tuple[int, int]:
    type_id = int(message[3:6], base=2)
    
    if type_id == 4:
        value, length = read_literal(message[6:])
        return value, 6 + length

    length_type_id = int(message[6])
    offset = 11 if length_type_id else 15
    nesting_size = int(message[7:7+offset], base=2)
    nested_message = message[7+offset:]
    read_bytes = 7+offset
    nested_values = []

    while nesting_size > 0:
        nested_value, nested_bytes = eval_bits(nested_message)
        nested_values.append(nested_value)
        read_bytes += nested_bytes
        nesting_size -= 1 if length_type_id else nested_bytes
        nested_message = nested_message[nested_bytes:]

    value = value_by_type(type_id, nested_values)
    return value, read_bytes

def read_literal(message: str) -> tuple[int, int]:
    still_read = True
    offset = 0
    bin_values = []
    while still_read:
        still_read = message[offset] == '1'
        bin_values.append(message[offset+1:offset+5])
        offset += 5
    return int(''.join(bin_values), base=2), offset
            
def value_by_type(type_id, args):
    func = {
        0: sum,
        1: lambda seq: functools.reduce(lambda x,y: x*y, seq),
        2: min,
        3: max,
        5: lambda x: 1 if x[0]>x[1] else 0,
        6: lambda x: 1 if x[0]<x[1] else 0,
        7: lambda x: 1 if x[0]==x[1] else 0,
    }[type_id]

    return func(args)

hex_message = get_message()
message = to_bits(hex_message)
result, _ = eval_bits(message)
print(result)
