class Board():
    def __init__(self, program: list[bool], initial_board: list[list[bool]]) -> None:
        self.program = program
        self.board = initial_board
        self.infinity = False

    def tick(self) -> None:
        self.expand_board()

        initial_board = [row[:] for row in self.board]
        for y, row in enumerate(self.board):
            for x, _ in enumerate(row):
                row[x] = self.calculate_value(initial_board, x, y)

        self.infinity = self.calculate_value(None, -10, -10)

    def expand_board(self) -> None:
        for idx, row in enumerate(self.board):
            self.board[idx] = [self.infinity] + row + [self.infinity]

        width = len(self.board[0])
        self.board = [[self.infinity] * width] + self.board + [[self.infinity] * width]

    def calculate_value(self, board:list[list[bool]], x: int, y: int) -> bool:
        coordinates = [
            (x+dx, y+dy)
            for dy in range(-1, 2)
            for dx in range(-1, 2)
        ]

        board_values = [self.board_value(board, x, y) for x, y in coordinates]
        bin_idx = ''.join('1' if v else '0' for v in board_values)
        idx = int(bin_idx, base=2)
            
        return self.program[idx]

    def board_value(self, board:list[list[bool]], x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return self.infinity
        
        height = len(board)
        width = len(self.board[0])
        if x >= width or y >= height:
            return self.infinity

        return board[y][x]

    def count_on(self) -> int:
        return sum(sum(row) for row in self.board)

    def print(self) -> None:
        for row in self.board:
            print(''.join('#' if x else '.' for x in row))


def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_program() -> list[bool]:
    return [c == '#' for c in get_lines()[0]]

def get_board() -> list[list[bool]]:
    return [
        [c == '#' for c in l]
        for l in get_lines()[2:]
    ]


program = get_program()
initial_board = get_board()

board = Board(program, initial_board)
for _ in range(50):
    board.tick()

print(board.count_on())
