def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_wires() -> dict[str, bool]:
    lines = read_lines()
    splitter = lines.index('')
    return {l[0]: l[1] == '1' for line in lines[:splitter] if (l := line.split(': '))}

def read_gates():
    lines = read_lines()
    splitter = lines.index('')
    operand = {
        'AND': lambda a, b: a & b,
        'OR': lambda a, b: a | b,
        'XOR': lambda a, b: a ^ b,
    }
    return {l[4]: (operand[l[1]], l[0], l[2]) for line in lines[splitter+1:] if (l := line.split())}

def wire_value(wires: dict, wire: str) -> bool:
    value = wires[wire]
    if isinstance(value, bool):
        return value
    
    op, input1, input2 = value
    return op(wire_value(wires, input1), wire_value(wires, input2))

def run() -> None:
    wires = read_wires() | read_gates()
    z_wires = sorted([w for w in wires if w.startswith('z')], reverse=True)
    binary = ''.join('1' if wire_value(wires, w) else '0' for w in z_wires)
    result = int(binary, base=2)
    print(result)

run()
