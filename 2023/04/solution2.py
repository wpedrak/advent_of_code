import re
from collections import Counter

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

lines = get_lines()
cards_count = [0] + [1] * len(lines)
for line in lines:
    numbers = re.findall(r'\d+', line)
    card_id = int(numbers[0])
    common = sum(v == 2 for v in Counter(numbers[1:]).values()) 
    for delta in range(1, common+1):
        cards_count[card_id + delta] += cards_count[card_id]

print(sum(cards_count))
