def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [x.rstrip() for x in file]


def get_moves():
    return [get_move(line) for line in get_lines()]


def get_move(line: str):
    cmd, arg = line.split()
    return cmd, int(arg)


moves = get_moves()
shifts = {
    'forward': (1, 0),
    'up': (0, -1),
    'down': (0, 1),
}
x, y = 0, 0

for cmd, arg in moves:
    dx, dy = shifts[cmd]
    x += dx * arg
    y += dy * arg

print(x, y, x*y)
