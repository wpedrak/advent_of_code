from collections import deque


def play_game(deck1, deck2):
    visited_states = set()

    while deck1 and deck2:
        immutable_decks = (tuple(deck1), tuple(deck2))
        if immutable_decks in visited_states:
            return 1, deck1, deck2

        visited_states.add(immutable_decks)

        top1 = deck1.popleft()
        top2 = deck2.popleft()

        round_winner = get_round_winner(deck1, deck2, top1, top2)

        if round_winner == 1:
            deck1 += [top1, top2]
        else:
            deck2 += [top2, top1]

    game_winner = 1 if deck1 else 2

    return game_winner, deck1, deck2


def get_round_winner(deck1, deck2, top1, top2):
    if len(deck1) < top1 or len(deck2) < top2:
        return 1 if top1 > top2 else 2

    sliced_deck1 = deque(list(deck1)[:top1])
    sliced_deck2 = deque(list(deck2)[:top2])

    winner, _, _ = play_game(sliced_deck1, sliced_deck2)
    return winner


deck1 = deque([21, 50, 9, 45, 16, 47, 27, 38, 29, 48, 10, 42, 32, 31, 41, 11, 8, 33, 25, 30, 12, 40, 7, 23, 46])
deck2 = deque([22, 20, 44, 2, 26, 17, 34, 37, 43, 5, 15, 18, 36, 19, 24, 35, 3, 13, 14, 1, 6, 39, 49, 4, 28])

winner, deck1_after_game, deck2_after_game = play_game(deck1, deck2)

deck = deck1_after_game if winner == 1 else deck2_after_game

score = 0
for idx, card in enumerate(reversed(deck)):
    score += (idx + 1) * card

print(score)
