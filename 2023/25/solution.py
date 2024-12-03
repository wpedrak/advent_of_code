from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_graph() -> dict[str, list[str]]:
    graph = defaultdict(list)

    for line in read_lines():
        src, dsts_str = line.split(': ')
        for dst in dsts_str.split():
            graph[src].append(dst)
            graph[dst].append(src)

    return graph

def count_nodes(graph: dict[str, list[str]], start: str):
    visited = set()
    to_visit = [start]

    while to_visit:
        node = to_visit.pop()
        visited.add(node)

        to_visit += [v for v in graph[node] if v not in visited]

    return len(visited)

def run() -> None:
    graph = read_graph()

    # see graph.png for values in this list
    for v1, v2 in [('sxx', 'zvk'), ('pzr', 'sss'), ('njx', 'pbx')]:
        graph[v1].remove(v2)
        graph[v2].remove(v1)

    result = count_nodes(graph, 'sxx') * count_nodes(graph, 'zvk')
    print(result)

def visualise() -> None:
    graph = read_graph()

    G = nx.Graph()
    G.add_nodes_from(graph)
    for v, neighbours in graph.items():
        G.add_edges_from((v, n) for n in neighbours)

    plt.figure(figsize=(30, 15), dpi=200)
    nx.draw(G, with_labels=True)
    plt.savefig("graph.png")

run()
# visualise()
