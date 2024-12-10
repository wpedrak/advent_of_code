Point = tuple[int, int]

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_map() -> list[list[int]]:
    return [[int(x) for x in line] for line in read_lines()]

def find_trailheads(top_map: list[list[int]]) -> list[Point]:
    trailheads = []
    
    for y, row in enumerate(top_map):
        for x, item in enumerate(row):
            if item != 0:
                continue
            trailheads.append((x, y))

    return trailheads

def find_neighbours(top_map: list[list[int]], point: Point) -> list[Point]:
    x, y = point
    height, width = len(top_map), len(top_map[0])
    value = top_map[y][x]
    potential = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
    return [(x, y) 
            for x, y in potential 
            if 0 <= x < width
            if 0 <= y < height
            if top_map[y][x] == value+1
            ]

def score(top_map: list[list[int]], start: Point) -> int:
    rating = 0
    to_visit = [start]

    while to_visit:
        x, y = to_visit.pop()
        if top_map[y][x] == 9:
            rating += 1

        to_visit += [n for n in find_neighbours(top_map, (x, y))]

    return rating

def run() -> None:
    top_map = read_map()
    trailheads = find_trailheads(top_map)

    result = sum(score(top_map, t) for t in trailheads)
    print(result)

run()
