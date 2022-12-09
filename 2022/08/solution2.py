def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def scenic_score(heights: list[list[int]], x: int, y: int) -> int:
    if x == 0 or x == len(heights[0])-1 or y == 0 or y == len(heights)-1:
        # One of scores == 0
        return 0

    move_deltas = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]
    score = 1
    for move_delta in move_deltas:
        score *= viewing_range(heights, x, y, move_delta)
    
    return score

def viewing_range(heights: list[list[int]], x: int, y: int, delta: tuple[int, int]) -> int:
    dx, dy = delta
    tree_height = heights[y][x]
    x += dx
    y += dy
    curr_range = 1

    while 0 <= x < len(heights[0]) and 0 <= y < len(heights) and heights[y][x] < tree_height:
        curr_range += 1
        x += dx
        y += dy

    if x == -1 or x == len(heights[0]) or y == -1 or y == len(heights):
        # outside of the edge
        curr_range -= 1

    return curr_range


heights = [list(map(int, l)) for l in read_lines()]
max_scenic_score = 0

for y, row in enumerate(heights):
    for x, height in enumerate(row):
        max_scenic_score = max(max_scenic_score, scenic_score(heights, x, y))

print(max_scenic_score)
