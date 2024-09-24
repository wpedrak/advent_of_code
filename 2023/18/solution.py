def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def get_instructions() -> list[tuple[int, int]]:
    return [(x[0], int(x[1])) for line in get_lines() if (x := line.split()) is not None]

def calculate_points() -> set[tuple[int, int]]:
    currect_point = (0, 0)
    points: set[tuple[int, int]] = {currect_point}
    for direction, steps in get_instructions():
        dx, dy = {
            'U': (0, 1),
            'D': (0, -1),
            'L': (-1, 0),
            'R': (1, 0),
        }[direction]
        for _ in range(steps):
            x, y = currect_point
            currect_point = (x+dx, y+dy)
            points.add(currect_point)
    
    return points

def count_outside(points: set[tuple[int, int]], min_x: int, max_x: int, min_y: int, max_y: int) -> int:
    start = (min_x, min_y)
    visited = set()
    to_visit = [start]

    while to_visit:
        point = to_visit.pop()

        for neighbour in find_neighbours(points, point, min_x, max_x, min_y, max_y):
            if neighbour in visited:
                continue
            
            to_visit.append(neighbour)
            visited.add(neighbour)

    return len(visited)

def find_neighbours(points: set[tuple[int, int]], point: tuple[int, int], min_x: int, max_x: int, min_y: int, max_y: int) -> list[tuple[int, int]]:
    x, y = point
    proposal = [(x+dx, y+dy) for dx in range(-1, 2) for dy in range(-1, 2) if abs(dx+dy) == 1]

    return [
        (x, y) for (x, y) in proposal
        if min_x <= x <= max_x
        if min_y <= y <= max_y
        if (x, y) not in points
        ]

points = calculate_points()
min_x = min(p[0] for p in points)
min_y = min(p[1] for p in points)
max_x = max(p[0] for p in points)
max_y = max(p[1] for p in points)

volume = (max_x - min_x + 3) * (max_y - min_y + 3) - count_outside(points, min_x-1, max_x+1, min_y-1, max_y+1)
print(volume)
