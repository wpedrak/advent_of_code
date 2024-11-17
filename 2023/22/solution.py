from typing import Self

class Point:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'
    
    def __repr__(self) -> str:
        return str(self)

class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def move_down(self) -> None:
        self.start.z -= 1
        self.end.z -= 1

    def move_up(self) -> None:
        self.start.z += 1
        self.end.z += 1

    def is_dug_up(self) -> bool:
        return self.start.z <= 0 or self.end.z <= 0
    
    def intersections(self, lines: list[Self]) -> list[Self]:
        return [l for l in lines if self.intersects(l)]

    def intersects(self, line: Self) -> bool:
        return all(intervals_intersect(i1, i2) for i1, i2 in [
            ((self.start.x, self.end.x), (line.start.x, line.end.x)),
            ((self.start.y, self.end.y), (line.start.y, line.end.y)),
            ((self.start.z, self.end.z), (line.start.z, line.end.z)),
        ])
    
    def above(self, lines: list[Self]) -> list[Self]:
        self.move_up()
        result = [l for l in self.intersections(lines) if l is not self]
        self.move_down()
        return result
    
    def below(self, lines: list[Self]) -> list[Self]:
        self.move_down()
        result = [l for l in self.intersections(lines) if l is not self]
        self.move_up()
        return result
    
    def move_down_to(self, target: int) -> None:
        min_z = min(self.start.z, self.end.z)
        diff = min_z - target
        if diff < 0:
            raise Exception(':<')
        
        self.start.z -= diff
        self.end.z -= diff
    
    def is_supported(self, lines: list[Self]) -> bool:
        self.move_down()
        have_support = bool(self.intersections(lines))
        self.move_up()

        return have_support

    def __str__(self) -> str:
        return f'{self.start}~{self.end}'
    
    def __repr__(self) -> str:
        return str(self)

def intervals_intersect(interval1: tuple[int, int], interval2: tuple[int, int]) -> bool:
    a, b = min(interval1, interval2)
    c, d = max(interval1, interval2)

    return b >= c

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def load_lines() -> list[Line]:
    return [parse_line(l) for l in read_lines()]

def parse_line(input_line: str) -> Line:
    start_str, end_str = input_line.split('~')
    start = Point(*[int(x) for x in start_str.split(',')])
    end = Point(*[int(x) for x in end_str.split(',')])
    return Line(start, end)

def stabilize(lines: list[Line]) -> None:
    lines = sorted(lines, key=lambda x: x.start.z)
    for idx, line in enumerate(lines):
        print(idx)
        min_line_z = min(line.start.z, line.end.z)
        previous_lines = lines[:idx]
        target_heights = sorted({z+1 for l in previous_lines for z in (l.start.z, l.end.z) if z < min_line_z}, reverse=True) + [1]
        for target in target_heights:
            line.move_down_to(target)
            if line.is_supported(previous_lines):
                break

def run() -> None:
    lines = load_lines()
    stabilize(lines)
    
    print('stabilized')

    result = 0
    for idx, line in enumerate(lines):
        print(idx)
        result += all(len(line_above.below(lines)) > 1 for line_above in line.above(lines))

    print(result)
    
run()
