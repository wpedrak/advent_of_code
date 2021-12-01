from collections import Counter, defaultdict

def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_directions():
    return get_lines()[0].split(',')

def distance(steps):
    counter = Counter(steps)
    counts = defaultdict(lambda: 0, counter)
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

            simplified_on_oposite_directions = min(counts[middle], counts[oposite_middle])
            changed += simplified_on_oposite_directions
            counts[middle] -= simplified_on_oposite_directions
            counts[oposite_middle] -= simplified_on_oposite_directions

            simplified_on_diagonal = min(counts[left], counts[right])
            changed += simplified_on_diagonal
            counts[left] -= simplified_on_diagonal
            counts[middle] += simplified_on_diagonal
            counts[right] -= simplified_on_diagonal

    return sum(counts.values())

directions = get_directions()
result = distance(directions)
print(result)
