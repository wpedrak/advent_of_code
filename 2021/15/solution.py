import heapq

Grid = list[list[int]]

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_grid() -> Grid:
    return [list(map(int, l)) for l in get_lines()]

def find_lowest_risk(grid: Grid):
    source = (0, 0)
    width = len(grid[0])
    height = len(grid)
    destination = (width-1, height-1)

    risk = {
        (x, y): float('inf')
        for x in range(0, width)
        for y in range(0, height)
    }
    risk[source] = 0

    visited = set()
    queue = [(0, source)]
    while queue:
        _, point = heapq.heappop(queue)
        if point in visited:
            continue
        for neighbour in get_neighbours(width, height, point):
            x, y = neighbour
            if risk[neighbour] > risk[point] + grid[y][x]:
                risk[neighbour] = risk[point] + grid[y][x]
                heapq.heappush(queue, (risk[neighbour], neighbour))

    return risk[destination]


def get_neighbours(width: int, height: int, point: tuple[int, int]):
    x, y = point
    potential_points = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1),
    ]

    return [
        (x, y) for x, y in potential_points
        if 0 <= x < width and 0 <= y < height 
    ]

grid = get_grid()
result = find_lowest_risk(grid)
print(result)
