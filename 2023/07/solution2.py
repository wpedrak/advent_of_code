from collections import Counter

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def type_key(hand: str) -> list[int]:
    counter = Counter(hand)
    jockers = counter['J'] if 'J' in counter else 0
    del counter['J']
    sorted_hand = list(sorted(counter.values(), reverse=True))
    if not sorted_hand:
        return [5]
    sorted_hand[0] += jockers
    return sorted_hand

def high_card_key(hand: str) -> int:
    key = 0
    for idx, card in enumerate(hand):
        shift = 10**(10-2*idx)
        key += shift * 'JX23456789TQKA'.index(card)
    return key

def hand_key(hand: str) -> tuple[list[int], int]:
    return (type_key(hand), high_card_key(hand))


result = 0
hands_with_bids = [(l.split()[0], int(l.split()[1])) for l in get_lines()]
for idx, (hand, bid) in enumerate(sorted(hands_with_bids, key=lambda x: hand_key(x[0]))):
    result += (idx+1) * bid

print(result)
