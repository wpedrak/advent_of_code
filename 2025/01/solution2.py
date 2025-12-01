old_dial = 50
result = 0
for line in open('input.txt', 'r'):
    direction = 1 if line[0] == 'R' else -1
    move = int(line[1:])
    if move >= 100:
        result += move // 100
        move %= 100

    new_dial = old_dial + direction * move
    result += move != 0 and new_dial in [0, 100]
    result += old_dial != 0 and new_dial != 100 and new_dial != new_dial % 100
    old_dial = new_dial % 100

print(result)
assert result > 5702
