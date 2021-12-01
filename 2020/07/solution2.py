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
        inner_count = int(contain_part[inner_color_part_idx])
        inner_color = contain_part[inner_color_part_idx + 1] + ' ' + contain_part[inner_color_part_idx + 2]
        edges.append((outer_color, inner_color, inner_count))

    return edges


def get_edges():
    tuple_edges = []
    for line in get_lines():
        tuple_edges += get_edges_from_line(line)

    edges = defaultdict(lambda: [])

    for from_vertex, to_vertex, count in tuple_edges:
        edges[from_vertex].append((to_vertex, count))

    return edges


def count_bags(edges, start_point):
    count = 1
    for inner_bag, inner_bag_count in edges[start_point]:
        count += inner_bag_count * count_bags(edges, inner_bag)

    return count


edges = get_edges()
my_bag_color = 'shiny gold'
bags_count = count_bags(edges, my_bag_color)
print(bags_count - 1)
