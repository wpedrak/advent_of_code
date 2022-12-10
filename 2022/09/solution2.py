from numpy import sign

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_command(line: str) -> tuple[str, int]:
    parts = line.split(' ')
    return parts[0], int(parts[1])

def move_knot(head_knot: tuple[int, int], tail_knot: tuple[int, int]) -> tuple[int, int]:
    hx, hy = head_knot
    tx, ty = tail_knot
    x_diff = abs(hx - tx)
    y_diff = abs(hy - ty)
    # tail is adjecent to the head
    if x_diff**2 + y_diff**2 <= 2:
        return tx, ty

    return tx + sign(hx - tx), ty + sign(hy - ty)

# head = knots[0] and tail = knots[9]
knots = [(0, 0)] * 10
visited = {(0, 0)}

for line in read_lines():
    direction, steps = parse_command(line)
    dx, dy = {
        'U': (0, 1),
        'D': (0, -1),
        'R': (1, 0),
        'L': (-1, 0),
    }[direction]
    
    for _ in range(steps):
        knots[0] = (knots[0][0] + dx, knots[0][1] + dy)
        for idx in range(1, 10):
            knots[idx] = move_knot(knots[idx-1], knots[idx])
        visited.add(knots[9])

print(len(visited))
