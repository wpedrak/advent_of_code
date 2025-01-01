import itertools
from collections import defaultdict

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_network() -> dict[str, set[str]]:
    network = defaultdict(set)

    for pair in read_lines():
        v1, v2 = pair.split('-')
        network[v1].add(v2)
        network[v2].add(v1)

    return network

def find_clique(graph: dict[str, set[str]], clique_size: int) -> list[str] | None:
    edges = {(v1, v2) for v1, neighbours in graph.items() for v2 in neighbours}

    for node, neighbours in graph.items():
        for potential_clique in itertools.combinations(neighbours, clique_size - 1):
            if all((v1, v2) in edges for v1, v2 in itertools.combinations(potential_clique, 2)):
                return sorted(potential_clique + (node,))

def max_clique(graph: dict[str, set[str]]) -> list[str]:
    k = 3
    clique = []
    while True and k < 20:
        new_clique = find_clique(graph, k)
        if not new_clique:
            return clique
        clique = new_clique
        k += 1

def run() -> None:
    network = read_network()
    clique = max_clique(network)
    print(','.join(clique))

run()
