LEFT = 'L'
RIGHT = 'R'
UP = 'U'
DOWN = 'D'

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def find_best_start(board: list[str]) -> int:
    height = len(board)
    width = len(board[0])

    energy = []
    for x in range(width):
        energy.append(count_energized(board, (x, 0, DOWN)))
        energy.append(count_energized(board, (x, height-1, UP)))

    for y in range(height):
        energy.append(count_energized(board, (0, y, RIGHT)))
        energy.append(count_energized(board, (width-1, y, LEFT)))

    return max(energy)

def count_energized(board: list[str], start_point) -> int:
    to_visit = [start_point]
    visited = {start_point}

    while to_visit:
        x, y, direction = to_visit.pop()
        
        for point in next_step(board, x, y, direction):
            if point in visited:
                continue
            visited.add(point)
            to_visit.append(point)

    visited_points = {(x, y) for (x, y, _) in visited}

    return len(visited_points)

def next_step(board: list[str], x: int, y: int, direction: str) -> list[tuple[int, int, str]]:
    width = len(board[0])
    height = len(board)
    board_item = board[y][x]

    new_directions = change_direction(direction, board_item)

    points = []
    for new_direction in new_directions:
        dx, dy = delta_by(new_direction)
        points.append((x+dx, y+dy, new_direction))

    return [p for p in points if 0 <= p[0] < width and 0 <= p[1] < height]

def change_direction(direction: str, item: str) -> list[str]:
    if item == '.':
        return [direction]
    
    if item == '-' and direction in [LEFT, RIGHT]:
        return [direction]

    if item == '|' and direction in [UP, DOWN]:
        return [direction]
    
    if item in ['-', '|']:
        return [change_direction(direction, '/'), change_direction(direction, '\\')]

    if item == '/':
        return {
            RIGHT: UP,
            LEFT: DOWN,
            UP: RIGHT,
            DOWN: LEFT,
        }[direction]
    
    if item == '\\':
        return {
            RIGHT: DOWN,
            LEFT: UP,
            UP: LEFT,
            DOWN: RIGHT,
        }[direction]

    raise Exception(f'Failed to change_direction({direction}, {item})')

def delta_by(direction: str) -> tuple[int, int]:
    return {
        LEFT: (-1, 0),
        RIGHT: (1, 0),
        UP: (0, -1),
        DOWN: (0, 1),
    }[direction]

board = get_lines()
result = find_best_start(board)

print(result)
