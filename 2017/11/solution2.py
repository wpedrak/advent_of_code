from collections import Counter, defaultdict

def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_directions():
    return get_lines()[0].split(',')

def distance(direction_counter):
    directions = ['n', 'ne', 'se', 's', 'sw', 'nw']
    size = len(directions)
    changed = 1

    while changed:
        changed = 0
        for idx in range(size):
            left = directions[idx]
            middle = directions[(idx+1) % size]
            right = directions[(idx+2) % size]
            oposite_middle = directions[(idx+4) % size]

            simplified_on_oposite_directions = min(direction_counter[middle], direction_counter[oposite_middle])
            changed += simplified_on_oposite_directions
            direction_counter[middle] -= simplified_on_oposite_directions
            direction_counter[oposite_middle] -= simplified_on_oposite_directions

            simplified_on_diagonal = min(direction_counter[left], direction_counter[right])
            changed += simplified_on_diagonal
            direction_counter[left] -= simplified_on_diagonal
            direction_counter[middle] += simplified_on_diagonal
            direction_counter[right] -= simplified_on_diagonal

    return sum(direction_counter.values())

def solve(steps):
    furthest = 0
    directions_counter = defaultdict(lambda: 0)

    for direction in steps:
        directions_counter[direction] += 1
        dist = distance(directions_counter)
        furthest = max(furthest, dist)

    return furthest
    

directions = get_directions()
result = solve(directions)
print(result)
