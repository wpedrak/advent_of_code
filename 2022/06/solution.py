def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def find_start(signal: str) -> int:
    for idx in range(len(signal)-4):
        if len(set(signal[idx:idx+4])) == 4:
            return idx + 4

    raise Exception('start not found')

line = read_lines()[0]
print(find_start(line))
