elves = []
elf = 0
for line in open('input.txt', 'r', encoding='utf-8'):
    line = line.rstrip()
    if not line:
        elves.append(elf)
        elf = 0
        continue

    elf += int(line)

elves.append(elf)
print(max(elves))
