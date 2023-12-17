import numpy as np

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def separate_patterns(lines: list[str]) -> list[list[str]]:
    patterns = []
    pattern = []
    for line in lines:
        if not line:
            patterns.append(pattern)
            pattern = []
            continue
        pattern.append(line)
    return patterns + [pattern]

def transpose(pattern: list[str]) -> list[str]:
    pattern_array = np.array([list(row) for row in pattern])
    return [''.join(row) for row in pattern_array.T.tolist()]

def find_horizontal_reflection(pattern: list[str]) -> int | None:
    return find_vertical_reflection(transpose(pattern))

def find_vertical_reflection(pattern: list[str]) -> int | None:
    height = len(pattern)
    for idx in range(1, height):
        reflection_size = min(idx, height - idx)
        upper = pattern[idx-reflection_size:idx]
        lower = pattern[idx:idx+reflection_size]
        if upper == lower[::-1]:
            return idx        
    
    return 0

result = 0
for pattern in separate_patterns(get_lines()):
    result += 100 * find_vertical_reflection(pattern) + find_horizontal_reflection(pattern)

print(result)
