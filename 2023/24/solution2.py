import matplotlib.pyplot as plt
import numpy as np
import math

class Hailstone:
    def __init__(self, x: int, y: int, z: int, vx: int, vy: int, vz: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def move(self, t: int):
        vector_len = math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)
        vx, vy, vz = self.vx / vector_len, self.vy / vector_len, self.vz / vector_len
        return vx * t + self.x, vy * t + self.y, vz * t + self.z

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_hailstones():
    return [parse_hailstone(l) for l in read_lines()]

def parse_hailstone(line: str):
    position_str, velocity_str = line.split(' @ ')
    position = [int(x) for x in position_str.split(', ')]
    velocity = [int(x) for x in velocity_str.split(', ')]
    return Hailstone(*(position+velocity))

def run() -> None:
    hailstones = read_hailstones()
    
    rights_skip = 0
    lefts_skip = 0
    both_skip = 0
    xs = sorted((h.x, h.vx) for h in hailstones)
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

def visualise() -> None:
    hailstones = read_hailstones()
    tick = 100000000000000
    
    ax = plt.figure().add_subplot(projection='3d')
    for hailstone in hailstones[:30]:
        x1, y1, z1 = hailstone.move(0)
        x2, y2, z2 = hailstone.move(tick)
        
        ax.plot([x1, x2], [y1, y2], [z1, z2])
        ax.quiver(x1, y1, z1, x2-x1, y2-y1, z2-z1)

    plt.savefig("lines.png")


# run()
visualise()
