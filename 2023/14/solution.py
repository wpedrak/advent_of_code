from collections import Counter

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def roll_north(board: list[list[str]], x: int, y: int) -> None:
    while y > 0 and board[y-1][x] == '.':
        board[y][x] = '.'
        board[y-1][x] = 'O'
        y -= 1

def tilt_north(board: list[list[str]]) -> None:
    height = len(board)
    width = len(board[0])
    for y in range(height):
        for x in range(height):
            if board[y][x] != 'O':
                continue
            roll_north(board, x, y)

def total_load(board: list[list[str]]):
    result = 0
    for south_dist, row in enumerate(reversed(board)):
        result += (south_dist+1) * Counter(row)['O']
    
    return result

board = [list(l) for l in get_lines()]
tilt_north(board)
result = total_load(board)
print(result)
