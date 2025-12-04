from collections import Counter

def max_joltage(pack: str) -> int:
    cnt = Counter(pack)
    max_digit = max(cnt)
    if cnt[max_digit] > 1:
        return int(max_digit*2)
    
    max_digit_positon = pack.index(max_digit)
    if max_digit_positon == len(pack) - 1:
        del cnt[max_digit]
        return int(max(cnt) + max_digit)
    
    return int(max_digit + max(pack[max_digit_positon+1:]))

result = 0
for pack in open('input.txt', 'r'):
    result += max_joltage(pack.strip())

print(result)
    