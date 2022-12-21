def run() -> None:
    monkeys = dict(parse_monkey(l) for l in read_lines())
    print(number(monkeys, 'root'))


def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_monkey(line: str) -> tuple[int, list|int]:
    monkey_id = line.split(':')[0]
    operands = line.split()[1:]

    if len(operands) == 1:
        return monkey_id, int(operands[0])

    return monkey_id, operands

def number(monkeys: dict[str, int|list], monkey: str) -> int:
    operands = monkeys[monkey]
    if isinstance(operands, int):
        return operands

    left_monkey, operation, right_monkey = operands
    fn = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x//y,
    }[operation]

    return fn(number(monkeys, left_monkey), number(monkeys, right_monkey))

run()
