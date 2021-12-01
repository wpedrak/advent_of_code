from collections import defaultdict
import itertools


def get_lines(filename='13/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_edges():
    edges = defaultdict(lambda: defaultdict(lambda: 0))
    edges['Me']
    
    for line in get_lines():
        splited = line.split()
        source = splited[0]
        destination = splited[-1][:-1]
        direction = 1 if splited[2] == 'gain' else -1
        happiness = int(splited[3])

        edges[source][destination] += direction * happiness
        edges[destination][source] += direction * happiness

    return edges


def longest_circle(edges):
    max_path_length = -float('inf')
    for circle in itertools.permutations(edges):
        dist = find_distance(edges, circle)
        max_path_length = max(max_path_length, dist)

    return max_path_length


def find_distance(distances, path):
    dist = 0

    for idx, source in enumerate(path):
        destination = path[(idx+1) % len(path)]

        dist += distances[source][destination]

    return dist


edges = get_edges()
max_dist = longest_circle(edges)

print(max_dist)
