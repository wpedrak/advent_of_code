import re
from collections import deque

Button = tuple[int, ...]
Lights = tuple[bool, ...]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_input():
    result: list[tuple[Lights, list[Button]]] = []
    for line in read_lines():
        lights = tuple(c == '#' for c in re.findall(r'\[([.#]+)\]', line)[0])
        buttons = [tuple(int(b) for b in buttons.split(',')) for buttons in re.findall(r'\(([0-9,]+)\)', line)]
        result.append((lights, buttons))

    return result

def count_edits(target: Lights, buttons: list[Button]):
    steps = 0
    to_visit = deque([(False,) * len(target), 'UP'])
    visited: set[Lights] = set()

    while len(to_visit) > 1:
        state = to_visit.popleft()
        if isinstance(state, str):
            steps += 1
            to_visit.append('UP')
            continue

        if state in visited:
            continue
        visited.add(state)

        if state == target:
            return steps
        
        to_visit += [n for b in buttons if (n := next_state(state, b)) not in visited]

    raise Exception(':<')

def next_state(lights: Lights, button: Button) -> Lights:
    lights_list = list(lights)
    for b in button:
        lights_list[b] = not lights_list[b]
    return tuple(lights_list)


def run() -> None:
    result = 0
    for target, buttons in read_input():
        result += count_edits(target, buttons)

    print(result)

run()
