def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def next_secret(secret: int, iterations: int=1) -> int:
    for _ in range(iterations):
        secret = ((secret*64) ^ secret) % 16777216
        secret = ((secret//32) ^ secret) % 16777216
        secret = ((secret*2048) ^ secret) % 16777216

    return secret

def run() -> None:
    secrets = [int(l) for l in read_lines()]
    result = sum(next_secret(s, iterations=2000) for s in secrets)
    print(result)

run()
