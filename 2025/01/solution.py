dial = 50
result = 0
for line in open('input.txt', 'r'):
    direction = 1 if line[0] == 'R' else -1
    dial += direction * int(line[1:])
    result += dial % 100 == 0

print(result)
