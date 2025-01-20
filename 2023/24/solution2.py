import numpy as np
from collections.abc import Callable
from typing import Self

class Hailstone:
    def __init__(self, x: int, y: int, z: int, vx: int, vy: int, vz: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def intersects(self, other: Self) -> bool:
        # self.vx * t + self.x = other.vx * t + other.x
        t = (other.x - self.x) / (self.vx - other.vx)
        return abs(self.vy * t + self.y - other.vy * t - other.y) < 0.01 and abs(self.vz * t + self.z - other.vz * t - other.z) < 0.01

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

    print('Calculating valid velocities...', end='', flush=True)

    min_vx = min(h.vx for h in hailstones)
    max_vx = max(h.vx for h in hailstones)
    min_vy = min(h.vy for h in hailstones)
    max_vy = max(h.vy for h in hailstones)
    min_vz = min(h.vz for h in hailstones)
    max_vz = max(h.vz for h in hailstones)

    valid_vx = find_valid_v(hailstones, min_vx, max_vx, lambda h: h.x, lambda h: h.vx)
    valid_vy = find_valid_v(hailstones, min_vy, max_vy, lambda h: h.y, lambda h: h.vy)
    valid_vz = find_valid_v(hailstones, min_vz, max_vz, lambda h: h.z, lambda h: h.vz)

    print('done!', flush=True)
    print('Testing valid velocities...', end='', flush=True)

    h1, h2 = hailstones[:2]
    stones = []
    for vx in valid_vx:
        for vy in valid_vy:
            for vz in valid_vz:
                # variables are x, y, z, t1, t2
                eq = np.array([
                    [-1, 0, 0, h1.vx - vx, 0],  # vx1 * t1 + x1 = vx * t1 + x
                    [0, -1, 0, h1.vy - vy, 0],  # vy1 * t1 + y1 = vy * t1 + y
                    [0, 0, -1, h1.vz - vz, 0],  # vz1 * t1 + z1 = vz * t1 + z
                    [-1, 0, 0, 0, h2.vx - vx],  # vx2 * t2 + x1 = vx * t2 + x
                    [0, -1, 0, 0, h2.vy - vy],  # vy2 * t2 + y1 = vy * t2 + y
                ])
                const = np.array([
                    -h1.x,  # vx1 * t1 + x1 = vx * t1 + x
                    -h1.y,  # vy1 * t1 + y1 = vy * t1 + y
                    -h1.z,  # vz1 * t1 + z1 = vz * t1 + z
                    -h2.x,  # vx2 * t2 + x1 = vx * t2 + x
                    -h2.y,  # vy2 * t2 + y1 = vy * t2 + y
                ])
                x, y, z, t1, t2 = np.linalg.solve(eq, const)
                if t1 < 0 or t2 < 0:
                    continue
                if h2.vz * t2 + h2.z - vz * t2 - z > 0.01:
                    continue
                if abs(x - int(x)) > 0.01 or abs(y - int(y)) > 0.01 or abs(z - int(z)) > 0.01:
                    continue
                
                stone = Hailstone(int(x), int(y), int(z), vx, vy, vz)
                if any(not stone.intersects(h) for h in hailstones):
                    continue

                stones.append(stone)

    print('done!', flush=True)
    assert len(stones) == 1
    s = stones[0]
    print(s.x + s.y + s.z)

run()
