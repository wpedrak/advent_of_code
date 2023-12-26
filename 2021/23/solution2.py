from collections import defaultdict

ROOM_LENGTH = 4
board_state = tuple[tuple[str,...], str, int]

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def get_board() -> list[list[str]]:
    board = [list(l) for l in get_lines()]
    board.insert(3, list('  #D#C#B#A#'))
    board.insert(4, list('  #D#B#A#C#'))
    return board

def get_rooms(board: list[list[str]]) -> tuple[str]:
    rooms = [[], [], [], []]
    for room in range(4):
        for delta in range(ROOM_LENGTH):
            rooms[room].append(board[2+delta][3+2*room])
    return tuple(''.join(room) for room in rooms)

def unit_cost(symbol: str) -> int:
    return {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[symbol]

def corridor_dist(src: int, dst: int) -> int:
    left = min(src, dst)
    right = max(src, dst)
    regular_dist = right - left
    rooms_in_between = sum(left <= x < right for x in range(1, 5))
    return regular_dist + rooms_in_between

def one_step(corridor: str, room_number: int, symbol: str) -> list[tuple[str, int]]:
    left, right = room_number+1, room_number+2
    available_corridor_spots = []
    for idx in range(left, -1, -1):
        if corridor[idx] != '.':
            break
        available_corridor_spots.append((idx, corridor_dist(idx, left) + 1))

    for idx in range(right, len(corridor)):
        if corridor[idx] != '.':
            break
        available_corridor_spots.append((idx, corridor_dist(right, idx) + 1))

    return [(corridor[:idx] + symbol + corridor[idx+1:], dist) for idx, dist in available_corridor_spots]    

def can_enter_room(symbol: str, room: str, room_idx: int) -> bool:
    room_symbol = 'ABCD'[room_idx]
    return symbol == room_symbol and all(c == room_symbol for c in room)

def is_room_entry(corridor_idx: int, right: bool):
    if right:
        return 1 <= corridor_idx <= 4
    return 2 <= corridor_idx <= 5

def short_circuit_one_direction(state: board_state, right=True) -> board_state:
    rooms, corridor, cost = state
    last_symbol = '.'
    symbol_idx = 0

    corridor_with_index = list(enumerate(corridor))
    if not right:
        corridor_with_index= reversed(corridor_with_index)

    for idx, symbol in corridor_with_index:
        if symbol != '.':
            last_symbol = symbol
            symbol_idx = idx
        if not is_room_entry(idx, right):
            continue
        room_idx = idx - 1 if right else idx - 2
        room = rooms[room_idx]
        if not can_enter_room(last_symbol, room, room_idx):
            continue
        corridor = corridor[:symbol_idx] + '.' + corridor[symbol_idx+1:]
        
        room = rooms[room_idx] + last_symbol
        rooms = rooms[:room_idx] + (room,) + rooms[room_idx+1:]

        corridor_distance = corridor_dist(idx, symbol_idx) + 1
        room_distance = ROOM_LENGTH - len(room) + 1
        cost += (corridor_distance + room_distance) * unit_cost(last_symbol)

        last_symbol = '.'

    return rooms, corridor, cost

def short_circuit(state: board_state) -> board_state:
    state_changed = True
    while state_changed:
        corridor_before = state[1]
        state = short_circuit_one_direction(state, right=True)
        state = short_circuit_one_direction(state, right=False)
        corridor_after = state[1]
        state_changed = corridor_before != corridor_after

    return state

def one_step_and_cleanup(rooms: tuple[str], corridor: str, cost: int):
    one_step_states = []
    for idx, room in enumerate(rooms):
        if not room:
            continue
        symbol = room[0]
        new_rooms = rooms[:idx] + (room[1:],) + rooms[idx+1:]
        dist_til_corridor = ROOM_LENGTH - len(room) + 1
        one_step_states += [(new_rooms, new_corridor, cost + (dist_til_corridor + corridor_dist) * unit_cost(symbol)) for new_corridor, corridor_dist in one_step(corridor, idx, symbol)]

    return [short_circuit(s) for s in one_step_states]

def print_history(prev: dict[board_state, board_state], state: board_state) -> None:
    while state in prev:
        print(state)
        state = prev[state]
    print(state)
    print('')

def min_cost(rooms: tuple[str]):
    to_visit = [(rooms, '.' * 7, 0)]
    visited = defaultdict(lambda: 9876543210123456789)
    min_cost = 9876543210123456789
    prev = {}
    while to_visit:
        rooms, corridor, cost = to_visit.pop()
        if rooms == tuple(x * ROOM_LENGTH for x in 'ABCD'):
            if cost >= min_cost:
                continue
            min_cost =cost
            print_history(prev, (rooms, corridor, cost))
            
            continue

        if visited[(rooms, corridor)] <= cost:
            continue

        visited[(rooms, corridor)] = cost
        next_steps = one_step_and_cleanup(rooms, corridor, cost)
        for step in next_steps:
            prev[step] = (rooms, corridor, cost)
        to_visit += next_steps
        
    return min_cost

if True:
    test1 = short_circuit_one_direction((('', '', '', ''), 'DB.....', 0), right=True)
    assert test1[2] == 70
    assert 'B' not in test1[1]
    assert test1[0][1] == 'B'

    test2 = short_circuit_one_direction((('', '', '', ''), 'DB.....', 0), right=False)
    assert test2[1] == 'DB.....'

    test3 = short_circuit((('', '', '', ''), 'DB.....', 0))
    assert test3[1] == '.......'

    test4 = short_circuit((('', '', '', ''), '.....CA', 0))
    assert test4[1] == '.......'

    test5 = one_step('..B....', 2, 'C')
    assert ('..BC...', 1) in test5

    print('tests passed')

board = get_board()
rooms = get_rooms(board)
cost = min_cost(rooms)
print(cost)
