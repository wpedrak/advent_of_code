IN_GROUP = 'IN_GROUP'
IN_GARBAGE = 'IN_GARBAGE'

def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_stream():
    lines = get_lines()
    return lines[0]

def count_garbage_chars(stream):
    state = IN_GROUP
    skip_next = False
    garbage_chars = 0

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

            garbage_chars += 1

        if state == IN_GROUP:
            if char == '<':
                state = IN_GARBAGE
                continue

    return garbage_chars

stream = get_stream()
result = count_garbage_chars(stream)
print(result)
