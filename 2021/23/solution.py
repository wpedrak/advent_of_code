ROOM_LENGTH = 2

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def get_board() -> list[list[str]]:
    return [list(l) for l in get_lines()]

def get_rooms(board: list[list[str]]) -> tuple[str]:
    rooms = [[], [], [], []]
    for room in range(4):
        for delta in range(2):
            rooms[room].append(board[2+delta][3+2*room])
    return tuple(''.join(room) for room in rooms)

def unit_cost(symbol: str) -> int:
    return {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[symbol]

def corridor_dist(src: int, dst: int):
    regular_dist = dst - src + 1
    rooms_in_between = sum(src <= x < dst for x in range(1, 5))
    return regular_dist + rooms_in_between

def one_step(corridor: str, room_number: int, symbol: str) -> list[tuple[str, int]]:
    left, right = room_number+1, room_number+2
    available_corridor_spots = []
    for idx in range(left, -1, -1):
        if corridor[idx] != '.':
            break
        available_corridor_spots.append((idx, corridor_dist(idx, left)))

    for idx in range(right, len(corridor)):
        if corridor[idx] != '.':
            break
        available_corridor_spots.append((idx, corridor_dist(right, idx)))

    return [(corridor[:idx] + symbol + corridor[idx+1:], dist) for idx, dist in available_corridor_spots]

def short_circuit(rooms: tuple[str], corridor: str, cost: int):
    pass

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

def min_cost(rooms: tuple[str]):
    to_visit = [(rooms, '.' * 7, 0)]
    visited = set()
    min_cost = 9876543210123456789

    while to_visit:
        rooms, corridor, cost = to_visit.pop()
        if rooms == ('AA', 'BB', 'CC', 'DD'):
            min_cost = min(min_cost, cost)
            continue

        if rooms in visited:
            continue

        visited.add(rooms)
        to_visit += one_step_and_cleanup(rooms, corridor, cost)
        
    return min_cost


board = get_board()
rooms = get_rooms(board)
cost = min_cost(rooms)
print(cost)
