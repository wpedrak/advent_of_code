Graph = dict[str, list[str]]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_graph():
    graph: Graph = {}
    for line in read_lines():
        chunks = line.split()
        graph[chunks[0][:-1]] = chunks[1:]
    return graph

def run() -> None:
    graph = read_graph()
    to_visit = ['you']
    result = 0

    while to_visit:
        item = to_visit.pop()
        if item == 'out':
            result += 1
            continue
        to_visit += graph[item]

    print(result)

run()
