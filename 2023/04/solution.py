import re
from collections import Counter

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

score = 0
for line in get_lines():
    count = Counter(re.findall(r'\d+', line)[1:])
    common = sum(v == 2 for v in count.values()) 
    score += 2**(common-1) if common else 0

print(score)
