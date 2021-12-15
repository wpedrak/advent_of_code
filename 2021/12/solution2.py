from collections import defaultdict

class RejectSet:
    def __init__(self, reject_term: str | None) -> None:
        self.reject_term = reject_term
        self.rejected = reject_term == None
        self.set = set()

    def rejection_inserted(self) -> bool:
        if self.reject_term is None:
            return True
        return self.reject_term in self.set
    
    def __contains__(self, item: str) -> bool:
        return item in self.set

    def add(self, item: str):
        if item == self.reject_term and not self.rejected:
            self.rejected = True
            return
        self.set.add(item)

    def copy(self):
        new = RejectSet(self.reject_term)
        new.rejected = self.rejected
        new.set = self.set.copy()
        return new

def get_lines(filename='2021/12/input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_edges() -> list[tuple[str, str]]:
    return [parse_edge(l) for l in get_lines()]

def parse_edge(line: str) -> tuple[str, str]:
    return line.split('-')

def get_graph() -> dict[str, list[str]]:
    graph = defaultdict(lambda: [])
    for vertex_from, vertex_to in get_edges():
        graph[vertex_from].append(vertex_to)
        graph[vertex_to].append(vertex_from)
    
    return graph

def count_paths(graph: dict[str, list[str]], cave: str, visited: RejectSet) -> int:
    if cave == 'end':
        return int(visited.rejection_inserted())

    new_visited = visited.copy()
    if cave.islower():
        new_visited.add(cave)
    
    paths = 0
    not_visited_neighbours = [n for n in graph[cave] if n not in visited]
    for neighbour in not_visited_neighbours:
        paths += count_paths(graph, neighbour, new_visited)

    return paths

lower_caves = {v_to for _, v_to in get_edges() if v_to.islower()} - {'end', 'start'}
graph = get_graph()
result = count_paths(graph, 'start', RejectSet(None))
for lower_cave in lower_caves:
    partial_result = count_paths(graph, 'start', RejectSet(lower_cave))
    result += partial_result

print(result)
