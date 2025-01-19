import matplotlib.pyplot as plt
import numpy as np
import math
from collections.abc import Callable

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

def find_valid_v(hailstones: list[Hailstone], min_v: int, max_v: int, position: Callable[[Hailstone], int], velocity: Callable[[Hailstone], int]):
    valid = []
    for v in range(min_v, max_v + 1):
        lower_velocity = [h for h in hailstones if velocity(h) < v]
        equal_velocity = [h for h in hailstones if velocity(h) == v]
        higher_velocity = [h for h in hailstones if velocity(h) > v]

        if len({position(h) for h in equal_velocity}) > 1:
            continue

        max_position = min((position(h) for h in lower_velocity), default=int(1e100))
        min_position = max((position(h) for h in higher_velocity), default=int(-1e100))

        if min_position > max_position:
            continue

        valid.append(v)

    return valid

def run() -> None:
    hailstones = read_hailstones()
    min_vx = min(h.vx for h in hailstones)
    max_vx = max(h.vx for h in hailstones)
    min_vy = min(h.vy for h in hailstones)
    max_vy = max(h.vy for h in hailstones)
    min_vz = min(h.vz for h in hailstones)
    max_vz = max(h.vz for h in hailstones)

    valid_vx = find_valid_v(hailstones, min_vx, max_vx, lambda h: h.x, lambda h: h.vx)
    valid_vy = find_valid_v(hailstones, min_vy, max_vy, lambda h: h.y, lambda h: h.vy)
    valid_vz = find_valid_v(hailstones, min_vz, max_vz, lambda h: h.z, lambda h: h.vz)

    print(len(valid_vx))
    print(len(valid_vy))
    print(len(valid_vz))
    print(len(valid_vx) * len(valid_vy) * len(valid_vz))

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


run()
# visualise()
