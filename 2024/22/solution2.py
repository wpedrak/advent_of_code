import itertools

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def calculate_prices(secret: int) -> list[int]:
    secrets = [secret % 10]
    for _ in range(2000):
        secret = ((secret*64) ^ secret) % 16777216
        secret = ((secret//32) ^ secret) % 16777216
        secret = ((secret*2048) ^ secret) % 16777216
        secrets.append(secret % 10)
    return secrets

def calculate_changes(prices: list[int]) -> list[int]:
    return [b-a for a, b in itertools.pairwise(prices)]

def calculate_first_change_patterns(changes: list[int]) -> dict[tuple, int]:
    patterns = {}

    for idx, pattern in enumerate(zip(changes, changes[1:], changes[2:], changes[3:]), start=4):
        if pattern in patterns:
            continue
        patterns[pattern] = idx

    return patterns

def monkey_price(first_change_patterns: dict[tuple, int], prices: list[int], pattern: tuple) -> int:
    if pattern not in first_change_patterns:
        return 0
    
    return prices[first_change_patterns[pattern]]


def run() -> None:
    init_secrets = [int(l) for l in read_lines()]
    print('prices...', end='', flush=True)
    prices = [calculate_prices(s) for s in init_secrets]
    print('done')
    print('changes...', end='', flush=True)
    changes = [calculate_changes(p) for p in prices]
    print('done')
    print('patterns...', end='', flush=True)
    first_change_patterns = [calculate_first_change_patterns(c) for c in changes]
    print('done')

    best_price = 0
    best_pattern = None

    for i, pattern in enumerate(itertools.product(range(-9, 10), repeat=4)):
        if not i % 100:
            print(i, '/', 19*19*19*19)
        price = sum(monkey_price(f, p, pattern) for f, p in zip(first_change_patterns, prices))
        if price > best_price:
            best_price = price
            best_pattern = pattern

    print(best_pattern)
    print(best_price)

run()
