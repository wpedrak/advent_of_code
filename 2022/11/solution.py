from collections import deque

class Monkey:
    def __init__(self, items: list[int], operation, divisor: int, target_true: int, target_false: int):
        self.items = deque(items)
        self.operation = operation
        self.divisor = divisor
        self.target_true = target_true
        self.target_false = target_false
        self.inspections = 0

    def inspect(self) -> tuple[int, int]:
        self.inspections += 1
        item = self.items.popleft()
        new_item = self.operation(item) // 3
        target = self.target_true if new_item % self.divisor == 0 else self.target_false
        return new_item, target

    def receive(self, item) -> None:
        self.items.append(item)

    def inspections_number(self) -> int:
        return self.inspections

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_monkeys(lines: list[str]) -> list[Monkey]:
    return [parse_monkey(lines[i:i+6]) for i in range(0, len(lines) + 1, 7)]

def parse_monkey(lines: list[str]) -> Monkey:
    number = int(lines[0][-2])
    items = [int(n) for n in lines[1].lstrip('  Starting items: ').split(', ')]
    operation = [
        lambda x: x*5,
        lambda x: x+5,
        lambda x: x*19,
        lambda x: x+7,
        lambda x: x+2,
        lambda x: x+1,
        lambda x: x*x,
        lambda x: x+4,
    ][number]
    divisor = int(lines[3].split(' ')[-1])
    target_true = int(lines[4].split(' ')[-1])
    target_false = int(lines[5].split(' ')[-1])

    return Monkey(items, operation, divisor, target_true, target_false)

monkeys = parse_monkeys(read_lines())
for _ in range(20):
    for monkey in monkeys:
        for _ in range(len(monkey.items)):
            item, target = monkey.inspect()
            monkeys[target].receive(item)

sorted_monkeys = list(sorted(monkeys, key=lambda x: x.inspections_number(), reverse=True))
print(sorted_monkeys[0].inspections_number(), sorted_monkeys[1].inspections_number())
print(sorted_monkeys[0].inspections_number() * sorted_monkeys[1].inspections_number())
