def run() -> None:
    monkeys = dict(parse_monkey(l) for l in read_lines())
    left_monkey, _, right_monkey = monkeys['root']
    left, left_ok = number(monkeys, left_monkey)
    right, _ = number(monkeys, right_monkey)

    result = left if left_ok else right
    root = left_monkey if not left_ok else right_monkey

    print(find_human_value(monkeys, root, result))

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_monkey(line: str) -> tuple[int, list|int]:
    monkey_id = line.split(':')[0]
    operands = line.split()[1:]

    if len(operands) == 1:
        return monkey_id, int(operands[0])

    return monkey_id, operands

def number(monkeys: dict[str, int|list], monkey: str) -> tuple[int, bool]:
    if monkey == 'humn':
        return 0, False
    operands = monkeys[monkey]
    if isinstance(operands, int):
        return operands, True

    left_monkey, operation, right_monkey = operands
    fn = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x//y,
    }[operation]

    left, left_ok = number(monkeys, left_monkey)
    right, right_ok = number(monkeys, right_monkey)

    if not left_ok or not right_ok:
        return 0, False

    return fn(left, right), True

def find_human_value(monkeys: dict[str, int|list], monkey: str, monkey_result: int) -> int:
    if monkey == 'humn':
        return monkey_result

    left_monkey, operation, right_monkey = monkeys[monkey]
    left_result, left_ok = number(monkeys, left_monkey)
    right_result, right_ok = number(monkeys, right_monkey)

    lower_monkey = ''

    if left_ok:
        fn = {
            '+': lambda x, y: x-y,
            '-': lambda x, y: y-x,
            '*': lambda x, y: x//y,
            '/': lambda x, y: y//x,
        }[operation]
        lower_result = fn(monkey_result, left_result)
        return find_human_value(monkeys, right_monkey, lower_result)

    if right_ok:
        fn = {
            '+': lambda x, y: x-y,
            '-': lambda x, y: x+y,
            '*': lambda x, y: x//y,
            '/': lambda x, y: x*y,
        }[operation]
        lower_result = fn(monkey_result, right_result)
        return find_human_value(monkeys, left_monkey, lower_result)

    raise Exception('Exactly one should be ok')

run()
