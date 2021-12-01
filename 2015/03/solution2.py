NORTH = '^'
SOUTH = 'v'
WEST = '<'
EAST = '>'

SANTA = 'santa'
ROBOT = 'robot'


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


def flip(turn):
    return {
        SANTA: ROBOT,
        ROBOT: SANTA
    }[turn]


instructions = get_line()
start_position = (0, 0)
visited = set([start_position])
santa_position = start_position
robot_position = start_position

turn = SANTA

for direction in instructions:
    if turn == SANTA:
        santa_position = move(santa_position, direction)
    elif turn == ROBOT:
        robot_position = move(robot_position, direction)
    else:
        raise Exception(f'Unexpected turn: {turn}')

    visited.add(santa_position)
    visited.add(robot_position)
    turn = flip(turn)

print(len(visited))
