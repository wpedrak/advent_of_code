def max_joltage(pack: str, batteries_to_turn: int) -> str:
    if batteries_to_turn == 1:
        return max(pack)
    max_digit = max(pack[:-batteries_to_turn+1])
    max_digit_positon = pack.index(max_digit)
    return max_digit + max_joltage(pack[max_digit_positon+1:], batteries_to_turn-1)

result = 0
for pack in open('input.txt', 'r'):
    result += int(max_joltage(pack.strip(), 12))

print(result)
    