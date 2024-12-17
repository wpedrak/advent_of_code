import re
import time

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

def move_all(robots: list[Robot], time: int):
    return {move(r, time) for r in robots}

def draw(points: set[tuple[int, int]]) -> None:
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print('#' if (x, y) in points else ' ', end='')
        print('')

def max_vertical_line(points: set[tuple[int, int]]):
    line_length = 0
    max_line_length = 0
    prev = (-1, -1)
    for x, y in sorted(points, key=lambda p: (p[1], p[0])):
        if prev == (x-1, y):
            line_length += 1
            max_line_length = max(max_line_length, line_length)
        else:
            line_length = 1

        prev = (x, y)

    return max_line_length

def run() -> None:
    robots = read_robots()
    t = 0
    while True:
        points = move_all(robots, t)
        print(t)
        if max_vertical_line(points) > 10:
            draw(points)
            break
        t += 1

run()
