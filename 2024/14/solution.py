import re
from collections import defaultdict

Robot = tuple[int, int, int, int]
WIDTH, HEIGHT = 101, 103

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_robots():
    return [parse_robot(l) for l in read_lines()]

def parse_robot(line: str) -> Robot:
    return tuple(int(x) for x in re.findall(r'-?\d+', line))

def move(robot: Robot, time: int) -> tuple[int, int]:
    x, y, dx, dy = robot
    return (x + dx * time) % WIDTH, (y + dy * time) % HEIGHT

def run() -> None:
    robots = read_robots()
    quadrants = defaultdict(int)

    for robot in robots:
        x, y = move(robot, 100)
        key = (x < WIDTH // 2, y < HEIGHT // 2, x == WIDTH // 2 or y == HEIGHT // 2)
        quadrants[key] += 1

    result = 1
    for k, v in quadrants.items():
        # on the middle
        if k[2]:
            continue
        result *= v

    print(result)

run()
