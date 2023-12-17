import numpy as np
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

def rotate(board: list[list[str]]) -> list[list[str]]:
    board_array = np.array(board, str)
    return np.rot90(board_array, axes=(1,0)).tolist()

def spin(board: list[list[str]]) -> list[list[str]]:
    for _ in range(4):
        tilt_north(board)
        board = rotate(board)

    return board

def total_load(board: list[list[str]]):
    result = 0
    for south_dist, row in enumerate(reversed(board)):
        result += (south_dist+1) * Counter(row)['O']
    
    return result

def hashable(board: list[list[int]]) -> tuple[str,...]:
    return tuple(''.join(row) for row in board)

board = [list(l) for l in get_lines()]

visited_set = set()
visited_list = []

while hashable(board) not in visited_set:
    hb = hashable(board)
    visited_set.add(hb)
    visited_list.append(hb)
    board = spin(board)

repeated_idx = visited_list.index(hashable(board))
cycle_size = len(visited_list) - repeated_idx

spins = 1_000_000_000
spins_in_cycle = spins - repeated_idx
ala = spins_in_cycle % cycle_size
final_board = visited_list[repeated_idx + (spins_in_cycle % cycle_size)]

result = total_load(final_board)
print(result)
