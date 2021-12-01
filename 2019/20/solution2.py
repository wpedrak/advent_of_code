from collections import deque, defaultdict as dd
from point import Point


class Maze():

    WALL = '#'
    EMPTY = '.'
    UNKNOWN = ' '

    def __init__(self, inp):
        rows = inp.split("\n")
        self.board = dd(lambda: Maze.UNKNOWN)
        self.teleports = dd(lambda: [])

        self.height = len(rows)
        self.width = len(rows[0])

        for y in range(len(rows)):
            for x in range(len(rows[0])):
                value = rows[y][x]
                point = Point(x, y)
                self.board[point] = value

        # print(self.board)

        for p, item in dict(self.board).items():
            if item.isalpha():
                # print(p)
                name, refer_to = self.parse_teleport(p)
                if name:
                    self.teleports[name].append(refer_to)

        # print('zium')
        self.zium = {}

        for name, fields in self.teleports.items():
            # print(name, fields)
            fields = list(set(fields))
            # print(name, fields)
            if len(fields) == 1:
                continue
            elif len(fields) == 2:
                self.zium[fields[0]] = fields[1]
                self.zium[fields[1]] = fields[0]
                continue

            raise Exception('Wrong length of teleports.')

    def parse_teleport(self, point):
        neighbours = self.get_neighbours(point)
        snd_letter_point = list(filter(
            lambda x: self.board[x].isalpha(),
            neighbours
        ))[0]

        potential_tlp_from = list(filter(
            lambda x: self.board[x] == Maze.EMPTY,
            neighbours
        ))

        # name is left to right and up to down
        name = None
        if point < snd_letter_point:
            name = self.board[point] + self.board[snd_letter_point]
        else:
            name = self.board[snd_letter_point] + self.board[point]

        if potential_tlp_from:
            return name, potential_tlp_from[0]

        tlp_from = list(filter(
            lambda x: self.board[x] == Maze.EMPTY,
            self.get_neighbours(snd_letter_point)
        ))

        # print(point)
        # print(potential_name)
        # print(snd_letter_point)
        # print(self.get_neighbours(snd_letter_point))
        # print(tlp_from)

        return name, tlp_from[0]

    def get_neighbours(self, p):
        potential = [
            Point(p.x, p.y + 1),
            Point(p.x, p.y - 1),
            Point(p.x - 1, p.y),
            Point(p.x + 1, p.y)
        ]

        return list(filter(lambda x: self.board[x] != Maze.WALL, potential))

    def is_outer_tlp(self, p):
        return p.x == 2 or p.x == self.width - 3 or p.y == 2 or p.y == self.height - 3

    def get_all_neighbours(self, point, level):
        steps = self.get_neighbours(point)
        steps = list(filter(lambda x: self.board[x] == Maze.EMPTY, steps))
        steps = list(map(lambda x: (x, level), steps))
        if point in self.zium:
            level_modifier = -1 if self.is_outer_tlp(point) else 1
            if level + level_modifier >= 0:
                steps.append((self.zium[point], level + level_modifier))
        return steps

    def find_path(self):
        visited = set()
        print(self.teleports['AA'][0])
        to_visit = deque([(self.teleports['AA'][0], 0), 'LVL_UP'])
        dist = 0

        target = (self.teleports['ZZ'][0], 0)

        while len(to_visit) > 1:
            current = to_visit.popleft()
            # print(current)
            # print(dist)
            visited.add(current)

            if current == 'LVL_UP':
                dist += 1
                to_visit.append('LVL_UP')
                continue

            if current == target:
                return dist

            to_visit += deque([n for n in self.get_all_neighbours(current[0], current[1]) if n not in visited])

        raise Exception('Failed to reach (ZZ, 0)')


def solve(inp):
    maze = Maze(inp)
    print('path finding')
    return maze.find_path()


maze = '''                                 A       N         N         I     K   F W                                       
                                 P       N         A         J     D   A L                                       
  ###############################.#######.#########.#########.#####.###.#.#####################################  
  #.#.#.#.#...#.....#...#.........#.....#.....#.....#.......#.....#.....#...#.#...#...#.#.............#.......#  
  #.#.#.#.###.#####.###.#########.#.###.#.#######.###.#.#####.#.###.###.#.#.#.#.#.#.###.#.#############.#######  
  #...............#.#...#...........#...#...#.....#...#.#.....#.#.#.#...#.#.....#...#.#.......#...#.#...#...#.#  
  #####.###.#####.#.###.###.###.#####.###.#####.#.#.#.###.#.###.#.###.#####.###.###.#.#.###.###.###.###.###.#.#  
  #.....#.#.#.#.....#.#.#.#...#.....#...#.....#.#.#.#...#.#.#...#.......#...#.#...#.#...#.......#.#.....#.#.#.#  
  #######.###.#####.#.#.#.#.#.#########.#.#######.#.###.#.#####.#.#########.#.#.#####.###.#.#.#.#.#.#####.#.#.#  
  #.#...............#.#.....#.#.....#...#.....#.......#.#...#...#.....#...#.#...#...#...#.#.#.#.........#.....#  
  #.#.###.#.###.###.#.#.#.#######.#.#.#####.###########.#####.#.#.#.#####.###.#.#.###.#######.###########.#####  
  #.#.#...#.#...#.#.....#.#.......#...#.....#...#.....#.#.....#.#.#.#.......#.#...........#.....#.#.#.#.#.....#  
  #.###########.#.#.#.###.#######.#######.#####.#.###.#.###.###.#.#########.###.#####.#.#.###.#.#.#.#.#.#.#####  
  #.#.....#...#.#...#...#.#.#...#...#.......#.......#...#...#...#.....#.............#.#.#.#...#.#.....#.#...#.#  
  #.#.###.###.#.#.###.###.#.###.#.#######.#########.###########.#.#.###.###.###.#####.###############.#.#.###.#  
  #.....#.#.#...#.#...#.....#.#.....#.#.#.....#.#...#.......#...#.#...#.#...#...#.#.#.....#...#.#...#...#.....#  
  ###.#####.###.#####.#######.#.#.###.#.###.###.#.#.###.#.#####.###.#######.###.#.#.#######.###.###.#.#####.###  
  #.........#...#.......#.......#.#.#...#.......#.#...#.#.....#.#.....#.....#.........#.#.#...#...#.......#...#  
  ###.#####.###.#.#.###.#.###.#.#.#.#.#########.#.#######.###.#.#.#######.#####.###.###.#.#.###.###.#####.#.#.#  
  #...#.#.#.#.#.#.#.#...#.#.#.#.#.......#.#.....#.#.#...#.#.#.#.#.#.#.#.....#.#.#.#.#.........#...#.#.#.#...#.#  
  ###.#.#.###.#######.#####.#.###.###.###.###.#.#.#.#.###.#.#.#.#.#.#.###.###.###.#####.#######.#####.#.###.###  
  #.....#...#...#.#.#.#.....#.#.....#.#.#.....#.#.....#.....#...#.....#...#.....#...#...#.....#.#...#.#.#.....#  
  ###.###.###.#.#.#.#######.#####.#####.###.#.###.#.#.#####.#####.#######.###.###.###.#.###.###.###.#.#.###.#.#  
  #.......#.#.#.....#.#.#.#...#.#...#.#.....#.#.#.#.#.#.#.#.#...#...#.#...............#.#.#...#.#.#.#.......#.#  
  ###.#####.###.###.#.#.#.#.###.#.###.###.#####.#.###.#.#.#.#.#.#.###.#.#.#####.#.#.#.###.#.###.#.#.#.#.#.#####  
  #.#...#.....#.#.#.................#.#...#.........#.#.#.#...#.#.....#.#.#...#.#.#.#.........#.#...#.#.#...#.#  
  #.#.###.###.###.###.#.#.#.#####.###.###.#######.#####.#.#.###.#####.#.#.#.#.#.#.#.#.#.#####.#.#.#.#####.#.#.#  
  #.#.....#...#.....#.#.#.#.#...........#...#.......#.......#.....#...#.#.#.#...#.#.#.#.#...#.#.#.#.#.#...#...#  
  #.#.#######.#####.###.###.#########.#####.#####.###########.#####.#.#####.#############.#####.###.#.###.#####  
  #.........#.#...#...#...#.#        J     T     S           F     N W     A        #...#.#.#...#.#.#.....#.#.#  
  ###.#####.#####.#.#########        R     R     E           A     N P     P        #.###.#.###.#.#.###.#.#.#.#  
  #...#.#.#...#.#...#...#...#                                                       #.#...#.......#...#.#.....#  
  ###.#.#.#####.###.###.#.###                                                       #.###.#####.#####.###.#####  
  #...#.#.#.#...#...#.#...#..HV                                                     #.#.#.#...#...#...#.#...#.#  
  #.#.#.#.#.###.###.#.###.#.#                                                       #.#.#.###.#.#####.#.#.###.#  
  #.#.......#.....#.....#...#                                                       #.#...#.#.........#.....#.#  
  #.###.#######.#.#.#.#.#.#.#                                                       #.#.#.#.#.#######.#.#.###.#  
  #.#...#.#...#.#.#.#.#.#.#.#                                                     QJ..#.#.#.#.......#...#...#..KV
  #.#.###.#.###.###.#.###.###                                                       #.#.#.#.#.###.#########.#.#  
FZ..#...............#.......#                                                       #...#.#.....#.#.....#...#..ZZ
  #####.#.#.#####.###.#.#####                                                       #.###.#.#########.###.###.#  
JR..#.#.#.#...#.#...#.#.#....HR                                                     #.#.#...#.....#.#.#.......#  
  #.#.#########.#########.###                                                       ###.#####.#####.#.#########  
  #...#.#.#.#.....#.#.......#                                                     IJ....#...#.............#.#.#  
  #.#.#.#.#.###.#.#.###.#####                                                       ###.#.#####.###.#.#.###.#.#  
  #.#...........#.......#.#.#                                                       #.....#.....#...#.#...#....SE
  #########.###.#########.#.#                                                       ###.###.###.#######.###.###  
  #.......#...#.#.#...#.....#                                                       #.#.....#.....#.....#.....#  
  #.#.###########.#.#.#.#.###                                                       #.###.#.###########.#####.#  
  #.#...#.#...#.#.#.#...#...#                                                       #.#.#.#.#.....#...........#  
  #.#.###.#.###.#.#.#####.###                                                       #.#.#####.###############.#  
AB..#.......#.........#.....#                                                       #.............#.........#.#  
  #####.###.###.#.#####.#####                                                       #.#.###.###.#######.#.#.###  
  #...#.#.......#...#........KV                                                   KD..#.#.#.#.......#.#.#.#...#  
  #.#########.###.###.#.#.###                                                       #.###.#####.###.#.###.#.###  
QJ........#.#...#.#...#.#.#.#                                                       #.#.....#...#.#.....#.#...#  
  #.#.#.#.#.#.#########.###.#                                                       #.###.#######.###.#.#.#.#.#  
  #.#.#.#.#.#.#.#...#...#.#.#                                                       #.#.....#.#...#.#.#...#.#..YO
  #####.#.#.###.#.#######.#.#                                                       #####.###.###.#.###########  
  #.....#...#.#...#.#........RF                                                   KR..........#................AX
  #########.#.###.#.###.#####                                                       #.#.###.###.#.#.###.###.#.#  
  #.#...#...................#                                                       #.#.#.....#.#.#...#.#...#.#  
  #.###.#####.#.#.#.#.#######                                                       #.#####.###.#########.#####  
  #.........#.#.#.#.#.#.....#                                                       #.#.#.......#.#...#.#.#...#  
  ###.#.#########.#####.###.#                                                       ###.#.#######.#.###.###.###  
KR....#.#.......#.#.#.#.#...#                                                       #.....#.....#.............#  
  #####.#.###.#####.#.#.#.###                                                       ###.#####.#.###.###.#.#.#.#  
  #.....#.#.....#.#...#.#....HM                                                     #.#...#.#.#.....#.#.#.#.#..XY
  #.#####.#.#####.#.#.#.#####                                                       #.#####.#.#.#.###.#.###.###  
  #.......#.........#.....#.#                                                     AI..#.#.#...#.#.#.#.#.#.#...#  
  #################.###.#.#.#                                                       #.#.#.###.#.###.#.###.#.###  
  #...........#...#.#...#.#.#                                                       #.........#.#...#.#.....#.#  
  #.###.#.###.#.#.#.#.#####.#                                                       #.###.#########.#.#######.#  
  #.#.#.#...#...#.#.#.....#..ZW                                                     #.#...#.....#...#.....#....WP
  #.#######.#.#############.#                                                       #######.#.#.#.#.#.#.#.#.###  
AA......#...#.......#.....#.#                                                     XY....#...#.#...#...#.#.#...#  
  ###.#######.###.#.###.###.#                                                       ###.#.#####.#####.###.#.#.#  
HV......#.#...#.#.#.........#                                                       #.#...#.........#.#.#.#.#.#  
  #######.#####.###.#.###.###                                                       #.#.#######.###.###.#.###.#  
RF..#.#...#.#.#.#.#.#.#.#.#..KH                                                     #.....#.......#...#.......#  
  #.#.###.#.#.#.#.#####.###.#                                                       #.#######.#.###.#####.#####  
  #.#.....#.....#...#.....#.#                                                       #.#.#.....#.#.....#.......#  
  #.#.#.###.###.#.#.#.###.#.#                                                       #.#.#.#.#.#.###.#####.#.###  
  #...#.....#.#...#...#.....#                                                       #.#.#.#.#.#.#.......#.#...#  
  #####.#.#.#.#.#####.###.#.#      A   W         N       F       Y     U       A    ###.#####.#.###.#####.#.#.#  
  #.....#.#...#...#.....#.#.#      B   L         A       Z       O     E       X    #.#.#...#.#.#.#.#...#.#.#.#  
  ###.#.###.#######.#.#####.#######.###.#########.#######.#######.#####.#######.#####.#.#.###.###.#.###.#.#.###  
  #...#.#.....#.....#.....#.......#...#.#.......#.#.#.....#...#.#.....#...#.....#...........#...#.......#.#...#  
  #.###.###.#.###.#.###.###.#.#####.###.#.###.###.#.###.###.#.#.###.###.#.#.#####.###.#.#.#######.#####.#######  
  #.#.....#.#.#...#.#.....#.#.#.....#.....#...#...#.#.....#.#.#.......#.#.#.........#.#.#.#.#.......#.#.#.....#  
  #####.#####.#####.###.#.#########.#######.#.#.###.#####.#.#.#.#########.###.###.#.#.#####.###.#####.#.###.###  
  #.........#.#.....#...#.#.#.........#.....#.#.......#.....#.#.......#...#...#...#.#.......#.#.#.............#  
  #####.###.#######.#####.#.###.#####.#.#############.#######.#######.###.#.#####.#.###.###.#.#####.###.#####.#  
  #.......#.#...#.....#.......#.#.#.#.#.....#.#.......#.....#...#.#.....#.#.#...#.#.#.....#.....#...#.......#.#  
  #.###.#####.#.###.#.#.#.#######.#.#.###.###.#.#####.###.#.#.###.###.###.#.#.#########.#####.#.###.#.###.#.#.#  
  #.#.........#.#.#.#.#.#.#.....#.....#.......#.....#.#...#...#...#.#...#.#...........#.#.#.#.#...#.#.#.#.#.#.#  
  #.#.#.#.#.###.#.#############.###.#.#.#######.#####.#.###.###.###.#.###.#.#.#.#####.#.#.#.#.#########.#.#####  
  #.#.#.#.#...#.#.#.....#...#.#...#.#.#...#.........#.#.#.......#.....#...#.#.#.#.....#...#.#.......#.#.....#.#  
  #.#.#.#.#.#####.###.#####.#.#.#.###.#.#.#.#######.#.#.###.#.#####.###.###.###############.#.#######.#####.#.#  
  #.#.#.#.#.....#.........#.#.#.#.#...#.#.#.#.....#.#.#.#...#.#.......#.#...#.#.......#...#.#...#...#.........#  
  ###.#.#.###.###.#.#.###.#.#.###.#.###.#####.#.###.###.#############.#.###.#.#####.###.###.#.#####.#.#####.#.#  
  #...#.#.#.....#.#.#.#...............#.#...#.#.......#.........#.....#.#.#.......#.....#.#.........#.#.....#.#  
  #######################.#.#########.#.###.#####.###.#.###########.#.#.#.###.#####.#####.###.#########.#.###.#  
  #.#.......#.............#.#.#.......#.......#.#.#.#.#...#...#.....#.#...#.....#.#.#...#.#.#...#.....#.#...#.#  
  #.#####.#.###.#############.#.###.#####.#####.###.#.#.###.#####.#######.#.#####.#.###.#.#.#######.#####.#.#.#  
  #.......#.......#.........#.#.#.....#.......#.......#.#.#.#.#.#.......#.#.....#...#.#...#.#.....#.#.#...#.#.#  
  #.###.###.#.#.###########.#.#######.#.#####.#######.#.#.#.#.#.#####.#.#.###.#.###.#.#.#.#.#.#.#.#.#.###.#####  
  #...#.#...#.#.#.....#...#.....#...#.#.#.#...#...#...#.........#.....#.#.#...#...#.....#.....#.#.....#.#.....#  
  ###.###.###.#####.#####.#.###.#.###.#.#.#######.###.#.#.###.#.#####.###.#.#######.#####.#######.#####.#####.#  
  #...#...#...#...........#.#.........#.......#.....#.#.#.#...#.#.#.....#.#...#.#.#.#.#...#.....#.#.......#.#.#  
  #.#.###.###.#####.#####.#####.#########.###.###.###.#####.#####.###.###.###.#.#.#.#.#####.#.###.#.#.#.#.#.###  
  #.#.#...#.......#...#.............#.......#.#.......#.........#.....#.....#...............#...#...#.#.#.....#  
  #################################.###.#########.#######.#########.###.#######.###############################  
                                   H   U         H       A         Z   K       T                                 
                                   M   E         R       I         W   H       R                                 '''

res = solve(maze)

print(res)