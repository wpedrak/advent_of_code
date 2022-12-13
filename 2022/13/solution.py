def run() -> None:
    lines = read_lines()
    idx_sum = 0
    idx = 1
    for packet_1_str, packet_2_str in zip(lines[0::3], lines[1::3]):
        packet_1 = eval(packet_1_str)
        packet_2 = eval(packet_2_str)
        if cmp(packet_1, packet_2) < 0:
            idx_sum += idx
        idx += 1

    print(idx_sum)

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
