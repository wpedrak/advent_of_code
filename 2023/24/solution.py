import itertools
from typing import Self

class Hailstone:
    def __init__(self, x: int, y: int, z: int, vx: int, vy: int, vz: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def intersection_point(self, other: Self):
        assert self.vx
        if self.is_parallel_to(other):
            # this might be wrong!
            return None 
        
        t2 = (self.vy * (other.x - self.x) + self.vx * (self.y - other.y)) / (self.vx * other.vy - other.vx * self.vy)
        t1 = (other.vx * t2 + other.x - self.x) / self.vx

        if t1 < 0 or t2 < 0:
            return None
        
        return (self.vx * t1 + self.x, self.vy * t1 + self.y)

    def is_parallel_to(self, other: Self):
        return self.vx * other.vy == other.vx * self.vy

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_hilestones():
    return [parse_hilestone(l) for l in read_lines()]

def parse_hilestone(line: str):
    position_str, velocity_str = line.split(' @ ')
    position = [int(x) for x in position_str.split(', ')]
    velocity = [int(x) for x in velocity_str.split(', ')]
    return Hailstone(*(position+velocity))

def run() -> None:
    MIN = 200000000000000
    MAX = 400000000000000
    hilestones = read_hilestones()
    
    result = 0
    for h1, h2 in itertools.combinations(hilestones, 2):
        intersection_point = h1.intersection_point(h2)
        if not intersection_point:
            continue

        x, y = intersection_point
        result += MIN <= x <= MAX and MIN <= y <= MAX

    print(result)
    
run()
