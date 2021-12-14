from collections import defaultdict

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_edges() -> list[list[tuple[str, str]]]:
    return [parse_edge(l) for l in get_lines()]

def parse_edge(line: str) -> tuple[str, str]:
    return line.split('-')


def get_graph() -> dict[str, list[str]]:
    graph = defaultdict(lambda: [])
    for vertex_from, vertex_to in get_edges():
        graph[vertex_from].append(vertex_to)
        graph[vertex_to].append(vertex_from)
    
    return graph

def count_paths(graph: dict[str, list[str]], cave: str, visited: set[str]) -> int:
    if cave == 'end':
        return 1
    if cave.islower():
        visited.add(cave)
    paths = 0
    not_visited_neighbours = [n for n in graph[cave] if n not in visited]
    for neighbour in not_visited_neighbours:
        paths += count_paths(graph, neighbour, visited)

    if cave.islower():
        visited.remove(cave)

    return paths


graph = get_graph()
result = count_paths(graph, 'start', set())
print(result)
