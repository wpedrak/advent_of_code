NORTH = '^'
SOUTH = 'v'
WEST = '<'
EAST = '>'


def get_line(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()][0]


def move(position, direction):
    x, y = position
    dx, dy = delta(direction)

    return x+dx, y+dy


def delta(direction):
    return {
        NORTH: (0, 1),
        SOUTH: (0, -1),
        WEST: (-1, 0),
        EAST: (1, 0)
    }[direction]


instructions = get_line()
start_position = (0, 0)
visited = set([start_position])
position = start_position

for direction in instructions:
    position = move(position, direction)
    visited.add(position)

print(len(visited))
