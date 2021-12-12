def get_lines(filename='input.txt'):
    return [line.rstrip() for line in open(filename, 'r')]

def pair(line: str) -> str | None:
    stack = []
    for char in line:
        if char in '([{<':
            stack.append(char)
            continue
        want = {
            ')': '(',
            ']': '[',
            '}': '{',
            '>': '<',
        }[char]
        if not stack:
            return None
        got = stack.pop()
        if want == got:
            continue
        return char
        
    return None

score = 0
for line in get_lines():
    wrong_char = pair(line)
    if not wrong_char:
        continue
    score += {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }[wrong_char]

print(score)
