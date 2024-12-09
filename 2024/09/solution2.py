import itertools

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def move_files(disk: list[int], disk_map: list[int]) -> None:
    positions = list(zip(disk_map, itertools.accumulate(disk_map, initial=0)))
    files = positions[::2]
    empty = positions[1::2]
    
    for file_size, file_position in reversed(files):
        empty_idx = find_empty_space(empty, file_size)
        if empty_idx == -1:
            continue
        empty_size, empty_position = empty[empty_idx]
        if empty_position > file_position:
            continue

        move(disk, file_position, empty_position, file_size)
        empty[empty_idx] = (empty_size-file_size, empty_position+file_size)

def find_empty_space(empty_map: list[tuple[int, int]], size: int) -> int:
    for idx, (empty_size, _) in enumerate(empty_map):
        if empty_size < size:
            continue
        return idx
    
    return -1

def move(disk: list[int], source: int, target: int, size: int) -> None:
    for i in range(size):
        disk[target+i] = disk[source+i]
        disk[source+i] = -1

def run() -> None:
    disk_map = [int(x) for x in read_lines()[0]]
    disk = [idx//2 if idx % 2 == 0 else -1 for idx, x in enumerate(disk_map) for _ in range(x)]
    move_files(disk, disk_map)
    checksum = sum(idx * file_id for idx, file_id in enumerate(disk) if file_id != -1)
    print(checksum)

run()
