from int_computer import Computer, Queue
from point import Point
from collections import defaultdict as dd, deque


class Droid:

    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    UNKNOWN = ' '
    WALL = '#'
    EMPTY = '.'
    DROID = 'D'
    OXYGEN = 'X'

    FOUND_WALL = 0
    MOVED = 1
    FOUND_OXYGEN = 2

    def __init__(self, tape):
        self.in_queue = Queue(name="in")
        self.out_queue = Queue(name="out")

        self.computer = Computer(inq=self.in_queue, outq=self.out_queue)
        self.computer.load(tape)

        self.board = dd(lambda: Droid.UNKNOWN)
        self.board[Point(0, 0)] = Droid.EMPTY
        self.position = Point(0, 0)
        self.oxygen = None

    @staticmethod
    def get_neighbour(p, direction):
        if direction == Droid.NORTH:
            return Point(p.x, p.y + 1)
        elif direction == Droid.SOUTH:
            return Point(p.x, p.y - 1)
        elif direction == Droid.WEST:
            return Point(p.x - 1, p.y)
        elif direction == Droid.EAST:
            return Point(p.x + 1, p.y)

        raise Exception('wrong direction')

    def move(self, direction):
        self.in_queue.put_message(direction)
        self.computer.run()
        res = self.out_queue.get_message()

        target_field = Droid.get_neighbour(self.position, direction)

        if res == Droid.FOUND_WALL:
            self.board[target_field] = Droid.WALL
        elif res == Droid.MOVED:
            self.board[target_field] = Droid.EMPTY
            self.position = target_field
        elif res == Droid.FOUND_OXYGEN:
            self.board[target_field] = Droid.OXYGEN
            self.position = target_field
            self.oxygen = target_field

        return res

    def display(self, display_droid=False):
        min_x = min(self.board, key=lambda x: x.x).x
        min_y = min(self.board, key=lambda x: x.y).y

        min_p = Point(min_x, min_y)

        def sub_mins(p):
            return p - min_p

        shifted_board = dd(lambda: Droid.UNKNOWN)

        for p, obj in self.board.items():
            shifted_board[sub_mins(p)] = obj

        if display_droid:
            shifted_board[sub_mins(self.position)] = Droid.DROID
            shifted_board[sub_mins(Point(0, 0))] = 'O'

        max_x = max(shifted_board, key=lambda x: x.x).x
        max_y = max(shifted_board, key=lambda x: x.y).y

        rows = []

        for y in range(max_y + 1):
            row = []
            for x in range(max_x + 1):
                row.append(str(shifted_board[Point(x, y)]))
            rows = [row] + rows

        image = "\n".join(map(lambda x: "".join(x), rows))

        print(image)

    def be_curious(self):
        oposite = {
            Droid.NORTH: Droid.SOUTH,
            Droid.SOUTH: Droid.NORTH,
            Droid.WEST: Droid.EAST,
            Droid.EAST: Droid.WEST,
        }

        for mv in [Droid.EAST, Droid.NORTH, Droid.WEST, Droid.SOUTH]:
            res = self.move(mv)
            if res != Droid.FOUND_WALL:
                self.move(oposite[mv])

    def right_move(self, mv):
        order = [Droid.EAST, Droid.NORTH, Droid.WEST, Droid.SOUTH]
        direction = (order.index(mv) - 1) % 4

        for _ in range(4):
            res = self.move(order[direction])
            if res != Droid.FOUND_WALL:
                return order[direction]
            direction = (direction + 1) % 4

        raise Exception('walls around')

    def keep_right(self, number_of_moves):
        last_move = Droid.NORTH
        for _ in range(number_of_moves):
            last_move = self.right_move(last_move)
            self.be_curious()


def get_neighbours(p, board):
    potential = [
        Point(p.x, p.y + 1),
        Point(p.x, p.y - 1),
        Point(p.x - 1, p.y),
        Point(p.x + 1, p.y)
    ]

    return list(filter(lambda x: board[x] != Droid.WALL, potential))


def solve(tape):
    droid = Droid(tape)
    droid.keep_right(1500)  # will check whole map

    print('Map prepared')

    board_map = droid.board

    target = droid.oxygen
    visited = set()
    to_visit = deque([Point(0, 0), 'LVL_UP'])
    dist = 0

    while to_visit:

        current = to_visit.popleft()
        if current == 'LVL_UP':
            dist += 1
            to_visit.append('LVL_UP')
            continue

        if current == target:
            return dist

        visited.add(current)

        to_visit += deque([n for n in get_neighbours(current, board_map) if n not in visited])


tape = "3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,102,1,1034,1039,101,0,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1001,1034,0,1039,102,1,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,102,1,1035,1040,1002,1038,1,1043,101,0,1037,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,37,1032,1006,1032,165,1008,1040,39,1032,1006,1032,165,1102,2,1,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,0,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,74,1044,1106,0,224,1102,0,1,1044,1106,0,224,1006,1044,247,1002,1039,1,1034,102,1,1040,1035,1002,1041,1,1036,102,1,1043,1038,1001,1042,0,1037,4,1044,1106,0,0,4,35,96,8,87,44,67,40,80,25,91,53,86,23,96,7,76,76,10,30,90,46,47,40,93,75,3,17,1,19,89,7,92,47,95,3,92,39,72,69,6,18,86,94,19,82,98,9,7,91,42,86,29,83,65,43,91,71,92,16,96,82,5,81,6,92,93,76,71,17,91,91,73,64,33,27,89,4,99,81,80,6,57,87,9,42,99,97,13,42,81,82,72,68,35,93,2,99,6,6,94,2,39,39,86,43,97,77,86,21,56,75,61,91,82,56,94,32,47,90,33,72,93,13,87,12,42,68,99,71,34,97,79,87,99,79,25,42,95,97,51,93,80,33,71,68,89,50,49,78,77,24,93,70,13,11,56,29,18,77,77,94,60,80,75,84,42,87,90,58,84,27,78,3,80,70,85,79,4,36,94,65,79,93,94,13,97,75,49,92,15,84,5,85,35,67,96,87,64,32,83,97,20,89,64,18,93,32,46,91,57,53,75,56,7,56,92,99,36,22,93,19,25,29,48,86,94,68,18,95,79,87,97,55,75,44,65,82,99,31,94,42,53,81,72,85,70,93,47,40,77,60,85,87,11,60,98,25,90,88,93,93,85,64,43,88,96,36,83,14,98,40,48,11,18,80,97,49,23,2,91,85,50,88,94,41,75,99,84,15,45,9,81,83,96,51,56,58,76,72,50,94,59,76,87,10,25,88,73,99,20,95,46,93,88,2,50,89,86,26,18,85,72,85,75,66,83,25,97,96,25,94,14,34,94,89,57,88,78,17,92,59,40,29,84,87,55,61,81,9,82,93,17,33,81,81,58,43,91,68,86,80,61,83,23,46,78,60,14,94,79,28,91,57,79,83,48,92,5,49,97,81,56,53,84,42,58,93,20,71,29,29,89,88,34,31,87,92,78,62,78,72,93,3,54,97,82,38,32,89,86,88,38,19,84,51,99,60,90,95,14,78,11,82,89,12,87,98,70,79,33,76,44,97,79,33,19,34,83,58,4,89,21,88,78,46,78,76,66,61,92,91,38,86,27,61,86,46,52,97,44,80,89,53,55,47,83,34,44,97,37,41,92,28,70,95,82,91,76,8,99,2,80,1,66,96,71,94,1,44,89,29,13,99,35,80,89,31,91,19,77,46,85,77,93,61,31,62,14,92,82,73,94,86,20,31,94,72,73,44,61,91,79,40,88,69,85,6,83,96,49,12,77,39,83,91,24,70,13,81,57,39,88,38,23,80,43,92,67,46,87,25,80,93,82,68,98,93,63,85,29,18,78,94,27,89,85,20,63,89,93,96,99,50,71,97,15,28,53,78,85,78,82,64,67,14,94,47,96,65,58,81,20,91,36,82,55,11,85,87,59,84,6,67,87,69,88,81,68,38,84,52,33,79,97,69,89,89,34,96,18,78,67,87,36,93,57,77,77,21,47,99,27,26,79,7,88,37,90,33,25,96,66,83,24,30,82,84,16,82,85,15,55,92,20,80,92,38,20,34,87,67,11,84,28,42,93,26,54,89,85,78,82,60,14,9,76,85,10,80,80,50,85,29,86,20,61,81,80,51,32,88,91,92,34,56,79,58,76,41,47,89,24,40,90,85,88,30,48,91,42,2,91,95,98,60,79,40,86,61,79,81,23,91,91,12,21,78,54,75,61,11,79,89,73,84,13,95,81,6,52,92,37,76,65,82,84,87,40,94,70,78,71,83,46,94,2,79,57,80,35,99,21,83,81,93,64,81,78,99,57,87,49,87,41,92,83,82,58,92,0,0,21,21,1,10,1,0,0,0,0,0,0"


print(solve(tape))
