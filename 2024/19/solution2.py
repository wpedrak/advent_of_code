import functools

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def count_organisations(towels: list[str], design: str) -> int:
    @functools.cache
    def aux(design: str) -> int:
        if not design:
            return 1
        return sum(aux(design.removeprefix(t)) for t in towels if design.startswith(t))

    return aux(design)

def run() -> None:
    towels = read_lines()[0].split(', ')

    result = 0
    for design in read_lines()[2:]:
        result += count_organisations(towels, design)

    print(result)

run()
