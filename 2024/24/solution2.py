Wires = dict[str, bool | tuple[str, str, str]]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_wires() -> Wires:
    lines = read_lines()
    splitter = lines.index('')
    return {l[0]: l[1] == '1' for line in lines[:splitter] if (l := line.split(': '))}

def read_gates() -> Wires:
    lines = read_lines()
    splitter = lines.index('')
    return {l[4]: (l[1], l[0], l[2]) for line in lines[splitter+1:] if (l := line.split())}

def dependencies(wires: Wires, wire: str):
    if wire.startswith(('carry', 'and', 'xor')):
        return wire
    value = wires[wire]
    if isinstance(value, bool):
        return wire
    
    op_name, input1, input2 = value
    return f'{op_name}({dependencies(wires, input1)}, {dependencies(wires, input2)})'

def rename_wire(wires: Wires, source: str, target: str) -> None:
    if source == target:
        return
    
    for wire, value in wires.copy().items():
        if isinstance(value , bool):
            continue
        op, in1, in2 = value
        t1 = target if in1 == source else in1
        t2 = target if in2 == source else in2
        wires[wire] = (op, t1, t2)

    wires[target] = wires[source]
    del wires[source]

def is_carry(wires: Wires, wire: str, bit: int):
    value = wires[wire]
    if isinstance(value, bool):
        return False

    carry_prev = f'carry{bit-1:02}'
    and_prev = f'and{bit-1:02}'
    xor_prev = f'xor{bit-1:02}'
    
    op, in1, in2 = value
    if op != 'OR' or and_prev not in {in1, in2}:
        return False
    
    non_and_wire = in1 if in2 == and_prev else in2
    non_and_value = wires[non_and_wire]
    if isinstance(non_and_value, bool):
        return False
    
    op, in1, in2 = non_and_value
    return op == 'AND' and {in1, in2} == {carry_prev, xor_prev}

def name_wires(wires: Wires) -> tuple[Wires, dict[str, str]]:
    wires = wires.copy()
    mapping = {}
    
    # rename to "xorXX" and "andXX"
    for wire, value in wires.copy().items():
        if isinstance(value, bool) or wire.startswith('z'):
            continue
        op, in1, in2 = value
        if {in1[0], in2[0]} != {'x', 'y'} or in1[1:] != in2[1:]:
            continue
            
        new_name = op.lower() + in1[1:]
        rename_wire(wires, wire, new_name)
        mapping[new_name] = wire
        
    # rename to carryXX
    max_bit = int(max(w for w in wires if w.startswith('z'))[1:])
    rename_wire(wires, 'and00', 'carry01')
    mapping['carry01'] = mapping['and00']
    for bit in range(2, max_bit+1):
        for wire, value in wires.copy().items():
            if isinstance(value, bool) or wire.startswith('z'):
                continue
            op, in1, in2 = value
            if not is_carry(wires, wire, bit):
                continue
            name = f'carry{bit:02}'
            rename_wire(wires, wire, name)
            mapping[name] = wire

    return wires, mapping

def rename_wires(wires: Wires, mapping: dict[str, str]) -> tuple[Wires, dict[str, str]]:
    wires = wires.copy()
    for k, v in mapping.items():
        rename_wire(wires, k, v)

    return name_wires(wires)

def swap(wires: Wires, wire1: str, wire2: str) -> None:
    wires[wire1], wires[wire2] = wires[wire2], wires[wire1]

def find_wire(wires: Wires, operation: str, inputs: tuple[str, str]):
    for wire, value in wires.items():
        if isinstance(value, bool):
            continue
        op, in1, in2 = value
        if op != operation or {in1, in2} != set(inputs):
            continue

        return wire
    
    raise Exception(':<')

def run() -> None:
    wires = read_wires() | read_gates()
    swap_pairs = [('z08', 'thm'), ('wss', 'wrm'), ('z22', 'hwq'), ('z29', 'gbs')]
    
    for w1, w2 in swap_pairs:
        swap(wires, w1, w2)

    wires, name_mapping = name_wires(wires)
    max_bit = int(max(w for w in wires if w.startswith('z'))[1:])

    # swap1 = find_wire(wires, 'XOR', ('xor08', 'carry08'))
    # swap3 = find_wire(wires, 'XOR', ('xor22', 'carry22'))
    # swap4 = find_wire(wires, 'XOR', ('xor29', 'carry29'))

    for bit in range(max_bit-1, 0, -1):
        z = f'z{bit:02}'
        op, in1, in2 = wires[z]
        if op == 'XOR' and {in1, in2} == {f'carry{bit:02}', f'xor{bit:02}'}:
            continue
        # print(z, '=', wires[z])
        print(z, '=', dependencies(wires, z))

    print(','.join(sorted(w for pair in swap_pairs for w in pair)))

run()
