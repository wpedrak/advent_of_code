import itertools, re

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def calculate_signature(springs: list[str]) -> str:
    block_size = 0
    blocks = []
    for spring in springs:
        if spring == '#':
            block_size += 1
            continue
        if block_size:
            blocks.append(block_size)
            block_size = 0

    if block_size:
        blocks.append(block_size)

    return ','.join(map(str, blocks))

def count_arrangements(line: str) -> int:
    unknown_part, signature = line.split()
    unknown_indexes = [match.start() for match in re.finditer(r'\?', unknown_part)]
    num_hashes_total = sum(int(match) for match in re.findall(r'\d+', signature))
    num_hashes_known = len(re.findall(r'#', unknown_part))
    num_missing_hashes = num_hashes_total - num_hashes_known
    springs = list(unknown_part)

    arrangements = 0
    for hash_indexes in itertools.combinations(unknown_indexes, num_missing_hashes):
        for unknown_idx in unknown_indexes:
            springs[unknown_idx] = '.'
        for hash_index in hash_indexes:
            springs[hash_index] = '#'

        arrangements += calculate_signature(springs) == signature

    return arrangements

result = sum(count_arrangements(l) for l in get_lines())
print(result)