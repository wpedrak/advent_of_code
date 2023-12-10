UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

SHAPE_DIRECTION = {
    '|': [UP, DOWN],
    '-': [LEFT, RIGHT],
    'L': [UP, RIGHT],
    'J': [UP, LEFT],
    '7': [DOWN, LEFT],
    'F': [DOWN, RIGHT],
    '.': [],
}

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def build_board(lines: list[str]) -> list[str]:
    width = len(lines[0]) + 2
    return ['.' * width] + [f'.{line}.' for line in lines] + ['.' * width]

def find_start(board: list[str]) -> tuple[int, int]:
    for y, line in enumerate(board):
        if 'S' not in line:
            continue
        return (line.index('S'), y)
    
    raise Exception('Start not found')

def points(direction: str, board: list[str], point: tuple[int, int]):
    x, y = point
    symbol = board[y][x]
    return direction in SHAPE_DIRECTION[symbol]

def guess_shape(board: list[str], point):
    x, y = point
    up = [UP] if points(DOWN, board, (x, y-1)) else []
    down = [DOWN] if points(UP, board, (x, y+1)) else []
    left = [LEFT] if points(RIGHT, board, (x-1, y)) else []
    right = [RIGHT] if points(LEFT, board, (x+1, y)) else []
    directions = up + down + left + right

    for shape in SHAPE_DIRECTION:
        if SHAPE_DIRECTION[shape] == directions:
            return shape
        
    raise Exception(f'Failed to find shape for directions: {directions}')

def find_neighbours(board: list[str], point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    shape = board[y][x]
    directions = SHAPE_DIRECTION[shape]
    up = [(x, y-1)] if UP in directions else []
    down = [(x, y+1)] if DOWN in directions else []
    left = [(x-1, y)] if LEFT in directions else []
    right = [(x+1, y)] if RIGHT in directions else []
    return up + down + left + right

lines = get_lines()
board = build_board(lines)
start = find_start(board)
sx, sy = start
board[sy] = board[sy].replace('S', guess_shape(board, start))
previous = start
current = find_neighbours(board, start)[0]
loop_size = 1

while current != start:
    loop_size += 1
    previous, current = current, (set(find_neighbours(board, current)) - {previous}).pop()

print(loop_size // 2)
