def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_parts():
    parts = []

    part = []
    for line in read_lines():
        if not line:
            parts.append(part)
            part = []
            continue
        part.append(line) 

    return parts + [part]

def signature(part: list[str]) -> list[int]:
    return [int(p.replace('#', '1').replace('.', '0'), base=2) for p in part]

def is_key(part: list[str]) -> bool:
    return part[0] == '#####'

def fits(key: list[int], lock: list[int]) -> bool:
    assert len(key) == len(lock)

    return sum(k & l for k, l in zip(key, lock)) == 0

def run() -> None:
    keys = []
    locks = []

    for part in read_parts():
        sig = signature(part)
        if is_key(part):
            keys.append(sig)
            continue
        locks.append(sig)

    result = sum(fits(key, lock) for key in keys for lock in locks)
    print(result)

run()
