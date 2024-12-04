import numpy as np

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def is_x_mas(puzzle: list[str], x: int, y: int):
    return puzzle[y][x] == 'A' and {puzzle[y+1][x+1], puzzle[y-1][x-1]} == {puzzle[y+1][x-1], puzzle[y-1][x+1]} == {'M', 'S'}


def run() -> None:
    puzzle = read_lines()
    height, width = len(puzzle), len(puzzle[0])

    result = sum(is_x_mas(puzzle, x, y) for y in range(1, height-1) for x in range(1, width-1))
    print(result)
            
run()
