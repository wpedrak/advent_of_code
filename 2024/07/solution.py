def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_equations() -> list[tuple[int, list[int]]]:
    return [parse_equation(l) for l in read_lines()]

def parse_equation(line: str) -> tuple[int, list[int]]:
    result, parts = line.split(': ')

    return int(result), [int(p) for p in parts.split()]

def can_be_true(result: int, parts: list[int]):
    def aux(acc: int, parts_idx: int):
        if parts_idx == len(parts):
            return acc == result
        
        part = parts[parts_idx]
        return aux(acc + part, parts_idx+1) or aux(acc*part, parts_idx+1)

    return aux(parts[0], 1)

def run() -> None:
    equations = read_equations()

    result = sum(res for res, parts in equations if can_be_true(res, parts))
    print(result)

run()
