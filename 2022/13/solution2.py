from functools import cmp_to_key

def run() -> None:
    lines = read_lines()
    packets = [eval(line) for line in lines[0::3] + lines[1::3]] + [[[2]], [[6]]]
    sorted_packets = list(sorted(packets, key=cmp_to_key(cmp)))
    first_divider_idx = sorted_packets.index([[2]]) + 1
    second_divider_idx = sorted_packets.index([[6]]) + 1

    print(f'{first_divider_idx} * {second_divider_idx} = {first_divider_idx * second_divider_idx}')

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

# cmp < 0 when left is smaller, cmp > 0 when left is bigger, 0 whe left == right
def cmp(left: int | list, right: int | list) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if isinstance(left, int):
        left = [left]

    if isinstance(right, int):
        right = [right]

    return cmp_list(left, right)

def cmp_list(left: list, right: list) -> int:
    for left_item, right_item in zip(left, right):
        items_cmp = cmp(left_item, right_item)
        if items_cmp:
            return items_cmp

    return len(left) - len(right)

run()
