from collections import Counter

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def run() -> None:
    left, right = zip(*[(int(l.split()[0]), int(l.split()[1])) for l in read_lines()])
    cnt = Counter(right)
    result = sum(num * cnt[num] for num in left)
    print(result)

run()
