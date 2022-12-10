from numpy import sign

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse_command(line: str) -> tuple[str, int]:
    parts = line.split(' ')
    return parts[0], int(parts[1])

def move_tail(hx: int, hy: int, tx: int, ty: int) -> tuple[int, int]:
    x_diff = abs(hx - tx)
    y_diff = abs(hy - ty)
    # tail is adjecent to the head
    if x_diff**2 + y_diff**2 <= 2:
        return tx, ty

    return tx + sign(hx - tx), ty + sign(hy - ty)


hx, hy = 0, 0
tx, ty = 0, 0
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
        hx += dx
        hy += dy
        tx, ty = move_tail(hx, hy, tx, ty)
        visited.add((tx, ty))

print(len(visited))
