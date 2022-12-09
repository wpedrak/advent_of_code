def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def max_for_invisibility(heights: list[list[int]], x: int, y: int) -> int:
    move_deltas = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]
    return min(max_in_line(heights, x, y, move_delta) for move_delta in move_deltas)

def max_in_line(heights: list[list[int]], x: int, y: int, delta: tuple[int, int]) -> int:
    dx, dy = delta
    x += dx
    y += dy
    curr_max = -1
    while 0 <= x < len(heights[0]) and 0 <= y < len(heights):
        curr_max = max(curr_max, heights[y][x])
        x += dx
        y += dy

    return curr_max


heights = [list(map(int, l)) for l in read_lines()]
hidden_spots = 0

for y, row in enumerate(heights):
    for x, height in enumerate(row):
        hidden_spots += max_for_invisibility(heights, x, y) < height

print(hidden_spots)
