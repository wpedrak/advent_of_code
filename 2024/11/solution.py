def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def transform(stone: int)-> list[int]:
    if stone == 0:
        return [1]
    
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        return [int(stone_str[:len(stone_str)//2]), int(stone_str[len(stone_str)//2:])]

    return [stone * 2024]

def blink(stones: list[int]) -> list[int]:
    return [s for stone in stones for s in transform(stone)]

def run() -> None:
    stones = [int(x) for x in read_lines()[0].split()]

    for i in range(25):
        stones = blink(stones)

    print(len(stones))

run()
