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

    def is_parallel(self, other: Self) -> bool:
        x, ox = self.x, other.x
        return (self.vx*ox, self.vy*ox, self.vz*ox) == (other.vx*x, other.vy*x, other.vz*x)

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
    hilestones = read_hilestones()
    
    rights_skip = 0
    lefts_skip = 0
    both_skip = 0
    xs = sorted((h.x, h.vx) for h in hilestones)
    for idx, (pos, _) in enumerate(xs):
        left_min_speed = min((vx for _, vx in xs[:idx] if vx > 0), default=9999)
        right_max_speed = max((vx for _, vx in xs[idx+1:] if vx > 0), default=-9999)
        rights_skip += left_min_speed < right_max_speed

        speed_to_reach = min((vx for _, vx in xs[:idx] if vx < 0), default=9999)
        speed_limit = max((vx for _, vx in xs[idx+1:] if vx < 0), default=-9999)
        lefts_skip += speed_to_reach < speed_limit

        both_skip += (left_min_speed < right_max_speed) and (speed_to_reach < speed_limit)

        if not ((left_min_speed < right_max_speed) and (speed_to_reach < speed_limit)):
            print(pos, left_min_speed, right_max_speed, speed_limit, speed_to_reach)

    print(rights_skip, lefts_skip, both_skip)

run()
