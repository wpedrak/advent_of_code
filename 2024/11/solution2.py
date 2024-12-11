import functools

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

@functools.cache
def count(stone: int, remaining_blinks: int) -> int:
    if not remaining_blinks:
        return 1
    
    if stone == 0:
        return count(1, remaining_blinks-1)
    
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        num1 = int(stone_str[:len(stone_str)//2])
        num2 = int(stone_str[len(stone_str)//2:])
        return count(num1, remaining_blinks-1) + count(num2, remaining_blinks-1)

    return count(stone * 2024, remaining_blinks-1)


def run() -> None:
    stones = [int(x) for x in read_lines()[0].split()]

    result = sum(count(s, 75) for s in stones)
    print(result)

run()
