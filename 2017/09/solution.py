IN_GROUP = 'IN_GROUP'
IN_GARBAGE = 'IN_GARBAGE'

def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_stream():
    lines = get_lines()
    return lines[0]

def total_score(stream):
    level = 1
    score = 0
    state = IN_GROUP
    skip_next = False

    for char in stream:
        if skip_next:
            skip_next = False
            continue

        if state == IN_GARBAGE:
            if char == '!':
                skip_next = True
                continue
            if char == '>':
                state = IN_GROUP
                continue

        if state == IN_GROUP:
            if char == '{':
                score += level
                level += 1
                continue
            if char == '}':
                level -= 1
                continue
            if char == '<':
                state = IN_GARBAGE
                continue

    return score

stream = get_stream()
result = total_score(stream)
print(result)
