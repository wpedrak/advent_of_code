from collections import deque

deck1 = deque([21, 50, 9, 45, 16, 47, 27, 38, 29, 48, 10, 42, 32, 31, 41, 11, 8, 33, 25, 30, 12, 40, 7, 23, 46])
deck2 = deque([22, 20, 44, 2, 26, 17, 34, 37, 43, 5, 15, 18, 36, 19, 24, 35, 3, 13, 14, 1, 6, 39, 49, 4, 28])

while deck1 and deck2:
    top1 = deck1.popleft()
    top2 = deck2.popleft()

    if top1 > top2:
        deck1 += [top1, top2]
    else:
        deck2 += [top2, top1]

deck = deck1 if deck1 else deck2

score = 0
for idx, card in enumerate(reversed(deck)):
    score += (idx + 1) * card

print(score)
