
def read_lines(file_name: str = 'input.txt'):
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def priority(letter):
    if 'a' <= letter <= 'z':
        return ord(letter) - ord('a') + 1

    return  ord(letter) - ord('A') + 27

result = 0

for line in read_lines():
    split_point = len(line) // 2
    half1 = set(line[:split_point])
    half2 = set(line[split_point:])
    same_letter = list(half1 & half2)[0]
    result += priority(same_letter)

print(result)
