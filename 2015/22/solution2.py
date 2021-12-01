from collections import deque


def find_min_mana_spent(player, boss, spells):
    effects = {
        'shield': 0,
        'poison': 0,
        'recharge': 0,
    }

    begin_state = to_state(player, boss, effects, 0, True)

    to_visit = deque([begin_state])
    visited = set()
    min_mana_spent = float('inf')

    prev = {}

    while to_visit:
        current = to_visit.popleft()

        for neighbour in make_turn(spells, current):
            if neighbour in visited:
                continue

            neighbour_mana_spent = neighbour[-2]

            prev[neighbour] = current

            if neighbour_mana_spent < min_mana_spent and player_won(neighbour):
                min_mana_spent = neighbour_mana_spent
                win_state = neighbour
                continue

            if player_won(neighbour):
                continue

            visited.add(neighbour)
            to_visit.append(neighbour)

    # state = win_state
    # path = [state]
    # while state in prev:
    #     state = prev[state]
    #     path.append(state)

    # path = list(reversed(path))

    # print(path[0])

    # for idx in range(len(path) - 1):
    #     state = path[idx]
    #     state_after = path[idx + 1]
    #     mana_diff = state_after[-2] - state[-2]
    #     print({
    #         53: 'magic missile',
    #         73: 'drain',
    #         113: 'shield',
    #         173: 'poison',
    #         229: 'recharge',
    #         0: ''
    #     }[mana_diff])
    #     print(state_after)

    return min_mana_spent


def make_turn(spells, state):
    player_turn = state[-1]
    if not player_turn:
        return make_boss_turn(state)

    states_after_round = []

    for cost, spell in spells:
        player, boss, effects, mana_spent, _ = to_repr(state)
        player['hp'] -= 1
        if cost > player['mp'] or player['hp'] <= 0:
            continue

        player['mp'] -= cost
        trigger_effects(player, boss, effects)
        spell(player, boss, effects)
        new_state = to_state(player, boss, effects, mana_spent + cost, False)
        states_after_round.append(new_state)

    return states_after_round


def make_boss_turn(state):
    player, boss, effects, mana_spent, _ = to_repr(state)
    trigger_effects(player, boss, effects)
    effective_attack = boss['damage'] - player['arm']
    player['hp'] -= effective_attack

    return [to_state(player, boss, effects, mana_spent, True)]


def trigger_effects(player, boss, effects):
    for name, duration in effects.items():
        if name not in ['shield', 'poison', 'recharge']:
            raise Exception(f'Unknown effect: {name}')

        if name == 'shield':
            if duration == 0:
                player['arm'] = 0
            else:
                player['arm'] = 7

        if duration == 0:
            continue

        if name == 'poison':
            boss['hp'] -= 3

        if name == 'recharge':
            player['mp'] += 101

        effects[name] -= 1


def player_won(state):
    player, boss, _, _, _ = to_repr(state)

    return boss['hp'] <= 0


def to_state(player, boss, effects, mana_spent, player_turn):
    return (
        player['hp'],
        player['mp'],
        player['arm'],
        boss['hp'],
        boss['damage'],
        effects['shield'],
        effects['poison'],
        effects['recharge'],
        mana_spent,
        player_turn
    )


def to_repr(state):
    player = {
        'hp': state[0],
        'mp': state[1],
        'arm': state[2]
    }
    boss = {
        'hp': state[3],
        'damage': state[4],
    }
    effects = {
        'shield': state[5],
        'poison': state[6],
        'recharge': state[7],
    }

    return player, boss, effects, state[8], state[9]


def magic_missle(player, boss, effects):
    boss['hp'] -= 4


def drain(player, boss, effects):
    boss['hp'] -= 2
    player['hp'] += 2


def shield(player, boss, effects):
    if effects['shield'] > 0:
        return

    effects['shield'] = 6


def poison(player, boss, effects):
    if effects['poison'] > 0:
        return

    effects['poison'] = 6


def recharge(player, boss, effects):
    if effects['recharge'] > 0:
        return

    effects['recharge'] = 5


player = {
    'hp': 50,
    'mp': 500,
    'arm': 0,
}

boss = {
    'hp': 71,
    'damage': 10,
}

spells = [
    (53, magic_missle),
    (73, drain),
    (113, shield),
    (173, poison),
    (229, recharge)
]

min_mana = find_min_mana_spent(player, boss, spells)
print(min_mana)
