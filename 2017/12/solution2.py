from collections import defaultdict

def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_pipes():
    pipes = {}
    for line in get_lines():
        splited = line.split(' <-> ')
        from_id = splited[0]
        to_ids = splited[1].split(', ')
        pipes[from_id] = to_ids

    return pipes

def get_group_containing(pipes, start):
    to_visit = [start]
    visited = set()
    count = 0

    while to_visit:
        current = to_visit.pop()

        if current in visited:
            continue
        
        visited.add(current)

        count += 1
        to_visit += [p for p in pipes[current] if p not in visited]

    return visited

def solve(pipes):
    rest_of_points = set(pipes)
    count = 0

    while rest_of_points:
        count += 1
        any_item = list(rest_of_points)[0]
        items_in_group = get_group_containing(pipes, any_item)
        rest_of_points -= items_in_group

    return count

pipes = get_pipes()
result = solve(pipes)

print(result)
