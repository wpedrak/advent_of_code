lines = [int(line.strip()) for line in open('input.txt', 'r')]

count = 0
for x, y in zip(lines, lines[1:]):
    count += y > x

print(count)
