DIAGNOSTIC_STEPS = 12481997
LEFT = -1
RIGHT = 1

def instructions(state, value):
    return {
        'A': [
            [1, RIGHT, 'B'],
            [0, LEFT, 'C']
        ],
        'B': [
            [1, LEFT, 'A'],
            [1, RIGHT, 'D']
        ],
        'C': [
            [0, LEFT, 'B'],
            [0, LEFT, 'E']
        ],
        'D': [
            [1, RIGHT, 'A'],
            [0, RIGHT, 'B']
        ],
        'E': [
            [1, LEFT, 'F'],
            [1, LEFT, 'C']
        ],
        'F': [
            [1, RIGHT, 'D'],
            [1, RIGHT, 'A']
        ]
    }[state][value]

tape = [0] * (DIAGNOSTIC_STEPS * 2)
position = DIAGNOSTIC_STEPS
state = 'A'

for time in range(DIAGNOSTIC_STEPS):
    if time % 100000 == 0:
        print(time)
    value = tape[position]
    to_write, direction, next_state = instructions(state, value)
    tape[position] = to_write
    position += direction
    state = next_state

result = sum(tape)

print(result)