import functools

Puzzle = tuple[str, tuple[int]]

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_puzzles():
    return [parse_puzzle(l) for l in get_lines()]

def parse_puzzle(line: str) -> Puzzle:
    unknown_part, signature_str = line.split()
    signature = tuple(int(d) for d in signature_str.split(','))
    
    return ((unknown_part + '?') * 5)[:-1], signature * 5

def count_arrangements(puzzle: Puzzle):
    unknown, signature = puzzle
    unknown = unknown + '.'
    @functools.cache
    def aux(unknown_idx: int, signature_idx: int, block_size: int):
        if unknown_idx == len(unknown):
            return signature_idx == len(signature)
        if signature_idx == len(signature):
            return '#' not in unknown[unknown_idx:]

        item = unknown[unknown_idx]
        if item == '#':
            return aux(unknown_idx+1, signature_idx, block_size+1)
        if item == '.':
            if not block_size:
                return aux(unknown_idx+1, signature_idx, 0)
            return aux(unknown_idx+1, signature_idx+1, 0) if signature[signature_idx] == block_size else 0
        
        # sum of '#' and '.' conditions form above
        if not block_size:
            return aux(unknown_idx+1, signature_idx, block_size+1) + aux(unknown_idx+1, signature_idx, 0)
        return aux(unknown_idx+1, signature_idx, block_size+1) + (aux(unknown_idx+1, signature_idx+1, 0) if signature[signature_idx] == block_size else 0)
        
    return aux(0, 0, 0)

def run() -> None:
    puzzles = read_puzzles()
    result = sum(count_arrangements(p) for p in puzzles)
    print(result)

run()
