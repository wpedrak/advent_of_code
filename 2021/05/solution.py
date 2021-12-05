def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [x.rstrip() for x in file]

def get_ends():
    ends = []
    for line in get_lines():
        start, end = line.split(' -> ')
        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))
        min_point = min(start, end)
        max_point = max(start, end)
        ends.append((min_point, max_point))

    return ends

ends = [e for e in get_ends() if e[0][0] == e[1][0] or e[0][1] == e[1][1]]

size = 1000
board = [[0]*size for _ in range(size)]

for start, end in ends:

    for y in range(start[1], end[1]+1):
        for x in range(start[0], end[0]+1):
            board[y][x] += 1

result = sum(map(
    lambda row: sum(map(lambda x: x > 1, row)),
    board
    ))
print(result)
