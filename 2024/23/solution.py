import itertools
from collections import defaultdict

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_network() -> dict[str, list[str]]:
    network = defaultdict(set)

    for pair in read_lines():
        v1, v2 = pair.split('-')
        network[v1].add(v2)
        network[v2].add(v1)

    return network

def find_k3s(network: dict[str, list[str]]) -> tuple[str, str, str]:
    k3s = set()

    for v1, neighbours in network.items():
        for v2, v3 in itertools.product(neighbours, repeat=2):
            if v2 not in network[v3]:
                continue
            k3s.add(tuple(sorted((v1, v2, v3))))

    return k3s

def run() -> None:
    network = read_network()
    k3s = find_k3s(network)
    result = sum(a.startswith('t') or b.startswith('t') or c.startswith('t') for a, b, c in k3s)
    print(result)

run()
