lines = [x.strip() for x in open('input.txt', 'r')]
moves = [line.split() for line in lines]

x, y = 0, 0

for cmd, arg in moves:
    if cmd == 'forward':
        x += int(arg)
        continue
    if cmd == 'down':
        y += int(arg)
        continue
    if cmd == 'up':
        y -= int(arg)

print(x, y, x*y)
