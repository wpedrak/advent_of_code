from functools import reduce
import heapq

class Grid:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid

    def width(self) -> int:
        return len(self.grid[0]) * 5

    def height(self) -> int:
        return len(self.grid) * 5 

    def __getitem__(self, point: tuple[int, int]) -> int:
        x, y = point
        total_x, mod_x = divmod(x, len(self.grid[0]))
        total_y, mod_y = divmod(y, len(self.grid))
        original_value = self.grid[mod_y][mod_x]
        increase = total_x + total_y
        value = original_value + increase
        if value <= 9:
            return value
        return value - 9

def get_lines(filename='2021/15/input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_base_grid() -> Grid:
    return [list(map(int, l)) for l in get_lines()]

def get_grid() -> Grid:
    return Grid(get_base_grid())

def find_lowest_risk(grid: Grid):
    source = (0, 0)
    width = grid.width()
    height = grid.height()
    destination = (width-1, height-1)

    risk = {
        (x, y): float('inf')
        for x in range(0, width)
        for y in range(0, height)
    }
    prev = {}
    risk[source] = 0

    visited = set()
    queue = [(0, source)]
    while queue:
        _, point = heapq.heappop(queue)
        if point in visited:
            continue
        visited.add(point)
        for neighbour in get_neighbours(width, height, point):
            new_risk = risk[point] + grid[neighbour]
            if risk[neighbour] > new_risk:
                risk[neighbour] = new_risk
                heapq.heappush(queue, (new_risk, neighbour))
                prev[neighbour] = point

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
