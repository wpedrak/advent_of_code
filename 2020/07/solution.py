from collections import defaultdict


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_edges_from_line(line: str):
    words = line.split()

    outer_color = words[0] + ' ' + words[1]
    contain_part = words[4:]

    if ' '.join(contain_part) == 'no other bags.':
        return []

    edges = []

    for inner_color_part_idx in range(0, len(contain_part), 4):
        inner_color = contain_part[inner_color_part_idx + 1] + ' ' + contain_part[inner_color_part_idx + 2]
        edges.append((inner_color, outer_color))

    return edges


def get_edges():
    tuple_edges = []
    for line in get_lines():
        tuple_edges += get_edges_from_line(line)

    edges = defaultdict(lambda: [])

    for from_vertex, to_vertex in tuple_edges:
        edges[from_vertex].append(to_vertex)

    return edges


def find_all_reachable(edges, start_point):
    visited = set()
    to_visit = [start_point]

    while to_visit:
        current = to_visit.pop()

        if current in visited:
            continue

        visited.add(current)

        for neighbour in edges[current]:
            if neighbour in visited:
                continue

            to_visit.append(neighbour)

    return len(visited)


edges = get_edges()
my_bag_color = 'shiny gold'
reachable_colors_count = find_all_reachable(edges, my_bag_color)
print(reachable_colors_count - 1)
