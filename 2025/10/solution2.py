import re
from collections import Counter, defaultdict
from itertools import combinations, product

Button = tuple[int, ...]
Counters = tuple[int, ...]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_input(filename: str = 'input.txt'):
    result: list[tuple[Counters, list[Button]]] = []
    for line in read_lines(filename=filename):
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
                # TODO: if calling with non-reducable data, we might result with negative counters
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

def is_reducable_to_zero(buttons: list[Button]):
   fake_target = tuple(range(max(b for button in buttons for b in button) + 1))
   _, _, remaining_buttons = reduce_sigle_counter_coverage(fake_target, buttons)
   return len(remaining_buttons) == 0

def find_min_independent_buttons(buttons: list[Button]):
    buttons_len = len(buttons)
    for size in range(buttons_len):
        for idx_to_delete in combinations(range(buttons_len), size):
            new_buttons = [b for idx, b in enumerate(buttons) if idx not in idx_to_delete]
            if not is_reducable_to_zero(new_buttons):
                continue
            return idx_to_delete

    raise Exception(':<')

def brute(target: Counters, buttons: list[Button], independent_indices: tuple[int, ...]):
    max_clicks = [max_count(target, buttons[ii]) for ii in independent_indices]
    max_clicks_ranges = [range(mc+1) for mc in max_clicks]
    min_clicks = 999_999

    difficulty = 1
    for mc in max_clicks:
        difficulty *= mc
    print(difficulty, max_clicks)
    for independent_clicks in product(*max_clicks_ranges):
        new_target = target
        for clicks, idx in zip(independent_clicks, independent_indices):
            new_target = click(new_target, clicks, buttons[idx])

        clicks, new_target, _ = reduce_sigle_counter_coverage(new_target, [b for idx, b in enumerate(buttons) if idx not in independent_indices])

        if min(new_target) < 0 or max(new_target) > 0:
            continue

        min_clicks = min(min_clicks, clicks + sum(independent_clicks))

    assert min_clicks != 999_999
    return min_clicks

def click(target: Counters, clicks_number: int, button: Button) -> Counters:
    editable_target = list(target)
    for b in button:
        editable_target[b] -= clicks_number
    return tuple(editable_target)

def max_count(target: Counters, button: Button):
    return min(target[b] for b in button)

def solve(target: Counters, buttons: list[Button]) -> int:
    indepedent_indices = find_min_independent_buttons(buttons)
    return brute(target, buttons, indepedent_indices)

def run() -> None:
    result = 0
    button_len: defaultdict[int, int]   = defaultdict(int)

    for idx, (target, buttons) in enumerate(read_input()):
        print(f'{idx:03}/196')
        indepedent_indices = find_min_independent_buttons(buttons)
        button_len[len(indepedent_indices)] += 1

        if len(indepedent_indices) <= 3:
            result += solve(target, buttons)

    print('')

    for k, v in sorted(list(button_len.items())):
        print(k, v)

    print(result)

def test():
    test_cases = read_input(filename='example.txt')
    assert solve(*test_cases[0]) == 10
    assert solve(*test_cases[1]) == 12
    assert solve(*test_cases[2]) == 11

test()
run()
