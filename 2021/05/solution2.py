def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [x.rstrip() for x in file]

def get_ends():
    ends = []
    for line in get_lines():
        start, end = line.split(' -> ')
        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))
        ends.append((start, end))

    return ends

def get_delta(start, end):
    if start == end:
        return 0

    return 1 if start < end else -1


ends = get_ends()

size = 1000
board = [[0]*size for _ in range(size)]

for (start_x, start_y), (end_x, end_y) in ends:
    dx = get_delta(start_x, end_x)
    dy = get_delta(start_y, end_y)
    t = 0
    x, y = start_x, start_y
    while (x + t*dx, y + t*dy) != (end_x, end_y):
        board[y][x] += 1
        x += dx
        y += dy
    board[y][x] += 1

result = sum(map(
    lambda row: sum(map(lambda x: x > 1, row)),
    board
    ))
print(result)
