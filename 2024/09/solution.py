def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def move_files(disk: list[int]) -> None:
    left, right = 0, len(disk)-1

    while left < right:
        if disk[left] != -1:
            left += 1
            continue
        if disk[right] == -1:
            right -= 1
            continue
        disk[left], disk[right] = disk[right], disk[left]

def run() -> None:
    disk = [idx//2 if idx % 2 == 0 else -1 for idx, x in enumerate(read_lines()[0]) for _ in range(int(x))]
    move_files(disk)
    checksum = sum(idx * file_id for idx, file_id in enumerate(disk) if file_id != -1)
    print(checksum)

run()
