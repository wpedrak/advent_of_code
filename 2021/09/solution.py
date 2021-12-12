def get_lines(filename='input.txt'):
    return [line.rstrip() for line in open(filename, 'r')]

def get_board():
    lines = get_lines()
    width = len(lines[0])
    board = []
    board.append([9] * (width+2))
    for line in lines:
        board.append([9] + [int(n) for n in line] + [9])
    board.append([9] * (width+2))
    return  board

board = get_board()
width = len(board[0])
height = len(board)
risk_level = 0
for y in range(1, height-1):
    for x in range(1, width-1):
        mid = board[y][x]
        top = board[y-1][x]
        bot = board[y+1][x]
        left = board[y][x-1]
        right = board[y][x+1]
        if mid < top and mid < bot and mid < left and mid < right:
            risk_level += mid + 1

print(risk_level)
