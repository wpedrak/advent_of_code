result = 0

for id_range in open('input.txt', 'r').read().strip().split(','):
    start, end = map(int, id_range.split('-'))
    start_str = str(start)
    prefix  = start_str[:len(start_str)//2] if not len(start_str) % 2 else '1' + '0' * (len(start_str) // 2)
    if int(prefix * 2) < start:
        prefix = str(int(prefix) + 1)
    while int(prefix * 2) <= end:
        result += int(prefix * 2)
        prefix = str(int(prefix) + 1)

print(result)
