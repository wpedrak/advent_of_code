import re
from collections import Counter

Button = tuple[int, ...]
Counters = tuple[int, ...]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_input():
    result: list[tuple[Counters, list[Button]]] = []
    for line in read_lines():
        counters = tuple(int(x) for x in re.findall(r'\{([0-9,]+)\}', line)[0].split(','))
        buttons = [tuple(int(b) for b in buttons.split(',')) for buttons in re.findall(r'\(([0-9,]+)\)', line)]
        result.append((counters, buttons))

    return result

def reduce_sigle_counter_coverage(target: Counters, buttons: list[Button]) -> tuple[int, Counters, list[Button]]:
    cnt = Counter(b for button in buttons for b in button)
    buttons = buttons[:]
    target_list = list(target)
    clicks = 0
    while min(cnt.values(), default=0) == 1:
        for key, value in cnt.items():
            if value > 1:
                continue
            idx, button = find_button(buttons, key)
            del buttons[idx]
            button_clicks = target_list[key]
            clicks += button_clicks
            for b in button:
                target_list[b] -= button_clicks
            break

        cnt = Counter(b for button in buttons for b in button)


    return clicks, tuple(target_list), buttons

def find_button(buttons: list[Button], key: int) -> tuple[int, Button]:
    for idx, button in enumerate(buttons):
        if key not in button:
            continue
        return idx, button
    
    raise Exception(':<')

def max_count(target: Counters, button: Button):
    return min(target[b] for b in button)

def is_easy(target: Counters, buttons: list[Button]):
    options = 1
    for button in buttons:
        options *= max_count(target, button)
    return options <= 10**6

def count_clicks_brute_force(target: Counters, buttons: list[Button]):
    

def count_clicks(target: Counters, buttons: list[Button]):
    return 0

def run() -> None:
    result = 0
    easy, hard = 0, 0
    missing = 0

    for target, buttons in read_input():
        clicks, target, buttons = reduce_sigle_counter_coverage(target, buttons)
        result += clicks
        if not buttons:
            continue
        
        if min(len(b) for b in buttons) == max(len(b) for b in buttons):
            result += sum(target) // len(buttons[0])
            continue

        easy += is_easy(target, buttons)
        hard += not is_easy(target, buttons)

        # result += count_clicks(target, buttons)
        missing += 1

    print(f'missing: {missing}')
    print(result, easy, hard)

run()
