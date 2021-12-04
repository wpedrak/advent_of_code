def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [x.rstrip() for x in file]

def get_numbers():
    return [int(x) for x in get_lines()[0].split(',')]

def get_boards():
    board_lines = get_lines()[2:]

    boards = []
    board = []
    for line in board_lines:
        if not line:
            boards += [board]
            board = []
            continue
        board += [[[int(x), False] for x in line.split()]]

    return boards

def mark(boards, number):
    for board in boards:
        for row in board:
            for field in row:
                item = field[0]
                if item != number:
                    continue
                field[1] = True


def get_winner(boards):
    for board in boards:
        if is_board_winning(board):
            return board


def is_board_winning(board):
    if have_winning_row(board):
        return True
    transpose(board)
    if have_winning_row(board):
        return True
    transpose(board)


def have_winning_row(board):
    for row in board:
        if all(x[1] for x in row):
            return True

    return False


def transpose(matrix):
    size = len(matrix)
    for y in range(size):
        for x in range(y+1, size):
            matrix[y][x], matrix[x][y] = matrix[x][y], matrix[y][x]


def calculate_score(board, number):
    unmarked_sum = sum(x for row in board for x, marked in row if not marked)
    return unmarked_sum * number


numbers = get_numbers()
boards = get_boards()

for number in numbers:
    mark(boards, number)
    winner = get_winner(boards)
    if winner:
        result = calculate_score(winner, number)
        print(result)
        break
