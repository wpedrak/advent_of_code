from collections import defaultdict
import itertools


def get_lines(filename='09/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_edges():
    edges = defaultdict(lambda: {})

    for line in get_lines():
        splited = line.split()
        source = splited[0]
        destination = splited[2]
        distance = int(splited[-1])
        edges[source][destination] = distance
        edges[destination][source] = distance

    return edges


def longest_path(edges):
    max_path_length = 0
    for path in itertools.permutations(edges):
        dist = find_distance(edges, path)
        max_path_length = max(max_path_length, dist)

    return max_path_length


def find_distance(distances, path):
    dist = 0

    for idx in range(len(path) - 1):
        source = path[idx]
        destination = path[idx+1]

        dist += distances[source][destination]

    return dist


edges = get_edges()
min_dist = longest_path(edges)

print(min_dist)
