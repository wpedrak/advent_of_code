from collections import defaultdict

Graph = dict[str, list[str]]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_graph():
    graph: Graph = {}
    for line in read_lines():
        chunks = line.split()
        graph[chunks[0][:-1]] = chunks[1:]

    graph['out'] = []
    return graph

def count_paths(graph: Graph, start: str, end: str):
    ants = {start: 1}
    paths = 0

    for _ in range(len(graph)):
        new_ants: dict[str, int] = defaultdict(int)
        for key, value in ants.items():
            for neighbour in graph[key]:
                new_ants[neighbour] += value

        ants = new_ants
        paths += ants[end]

    return paths

def run() -> None:
    graph = read_graph()
    order_one = count_paths(graph, 'svr', 'fft') * count_paths(graph, 'fft', 'dac') * count_paths(graph, 'dac', 'out')
    order_two = count_paths(graph, 'svr', 'dac') * count_paths(graph, 'dac', 'fft') * count_paths(graph, 'fft', 'out')

    print(order_one + order_two)

run()
