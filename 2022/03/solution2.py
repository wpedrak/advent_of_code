
def read_lines(file_name: str = 'input.txt'):
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def priority(letter):
    if 'a' <= letter <= 'z':
        return ord(letter) - ord('a') + 1

    return  ord(letter) - ord('A') + 27

result = 0
lines = read_lines()
for bag1, bag2, bag3 in zip(lines[::3], lines[1::3], lines[2::3]):
    bag1, bag2, bag3 = set(bag1), set(bag2), set(bag3)
    same_letter = list(bag1 & bag2 & bag3)[0]
    result += priority(same_letter)

print(result)
