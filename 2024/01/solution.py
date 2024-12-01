def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def run() -> None:
    left, right = zip(*[(int(l.split()[0]), int(l.split()[1])) for l in read_lines()])
    result = sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))
    print(result)

run()
