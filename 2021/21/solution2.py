import itertools
import functools

WIN_SCORE = 21

@functools.cache
def win_cnt(pos1: int, pos2: int, score1: int, score2: int, player: int) -> tuple[int, int]:
    if score1 >= WIN_SCORE:
        return (1, 0)
    if score2 >= WIN_SCORE:
        return (0, 1)

    results = [0, 0]
    for roll1, roll2, roll3 in itertools.product(range(1, 4), repeat=3):
        positions = [pos1, pos2]
        scores = [score1, score2]
        move = roll1 + roll2 + roll3
    
        positions[player] = (positions[player] + move - 1) % 10 + 1
        scores[player] += positions[player]
        result = win_cnt(positions[0], positions[1], scores[0], scores[1], 1-player)
        results[0] += result[0]
        results[1] += result[1]

    return tuple(results)

print(max(win_cnt(10, 7, 0, 0, 0)))
