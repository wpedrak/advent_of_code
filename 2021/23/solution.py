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

def one_step(rooms: tuple[str], corridor: str, cost: int):
    pass

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
        to_visit += one_step(rooms, corridor, cost)
        
    return min_cost


board = get_board()
rooms = get_rooms(board)
print(rooms)
cost = min_cost(board)
print(cost)
