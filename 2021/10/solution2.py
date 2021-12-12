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
        if want != got:
            return None
        
    pairs = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }
    return ''.join(pairs[b] for b in reversed(stack))

def completion_score(completion: str) -> int:
    point_table = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    score = 0
    for char in completion:
        score *= 5
        score += point_table[char]
    return score

scores = []
for line in get_lines():
    completion = pair(line)
    if not completion:
        continue
    scores.append(completion_score(completion))

print(list(sorted(scores))[len(scores)//2])
