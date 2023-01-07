def run() -> None:
    current_sum = [0]
    for number_str in read_lines():
        number_list = to_list(number_str)
        current_sum = add(current_sum, number_list)

    print(to_str(current_sum))

def to_list(number: str) -> list[int]:
    return [{'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}[char] for char in number]

def to_str(number: list[int]) -> str:
    return ''.join({-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}[digit] for digit in number)

def add(number_1: list[int], number_2: list[int]) -> list[int]:
    max_len = max(len(number_1), len(number_2))
    number_1_pad = [0] * (max_len - len(number_1)) + number_1
    number_2_pad = [0] * (max_len - len(number_2)) + number_2
    res = [n1 + n2 for n1, n2 in zip(number_1_pad, number_2_pad)]

    carry = 0
    for idx in range(len(res)-1, -1, -1):
        digit = res[idx] + carry
        carry = 0
        if digit < -2:
            digit += 5
            carry = -1
        if digit > 2:
            digit -= 5
            carry = 1

        res[idx] = digit

    if carry == 0:
        return res

    return [carry] + res


def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(file_name, 'r', encoding='utf-8')]

run()
