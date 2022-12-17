import re
from collections import deque

def run() -> None:
    graph, flows = build_graph(read_lines())
    non_zero_valves = [v for v, flow in flows.items() if flow]
    interesting_valves = ['AA'] + non_zero_valves
    dist = {}
    for valve_1 in interesting_valves:
        for valve_2 in interesting_valves:
            if valve_1 == valve_2:
                continue
            # +1 for opening the valve
            dst = distance_in_graph(graph, valve_1, valve_2) + 1
            dist[(valve_1, valve_2)] = dst
            dist[(valve_2, valve_1)] = dst

    print('Finding paths')
    paths = all_paths(set(non_zero_valves), dist, 'AA', 26)
    print('Sorting paths')
    sorted_paths = list(sorted(paths, key=lambda x: pressure(dist, flows, x), reverse=True))

    set_and_pressure = [(set(p) - {'AA'}, pressure(dist, flows, p)) for p in sorted_paths]
    local_max = 0
    set_and_pressure_chunk = set_and_pressure[:1000]
    print(f'Searching for result in {len(set_and_pressure_chunk)} most valuable paths. If the result is too low, please increase the limit.')
    for idx_1, (set_1, preassure_1) in enumerate(set_and_pressure_chunk):
        for idx_2 in range(idx_1+1, len(set_and_pressure_chunk)):
            set_2, preassure_2 = set_and_pressure_chunk[idx_2]

            if not (set_1 & set_2):
                local_max = max(local_max, preassure_1 + preassure_2)

    print(local_max)


def pressure(distance: dict[tuple[str, str], int], flows: dict[str, int], path: list[str]) -> int:
    time = 26
    res = 0
    for a, b in zip(path[:-1], path[1:]):
        time -= distance[(a, b)]
        res += time * flows[b]

    return res

def all_paths(vertices: set[str], distance: dict[tuple[str, str], int], start: str, time: int) -> list[list[str]]:
    reachable = {v for v in vertices if distance[(start, v)]<= time}
    if not reachable:
        return [[start]]
    res = [[start]]
    for vertex in reachable:
        for prev in all_paths(reachable-{vertex}, distance, vertex, time - distance[(start, vertex)]):
            res.append([start] + prev)

    return res

def distance_in_graph(graph: dict[str, list[str]], start: str, end: str) -> None:
    to_visit = deque([start, 'LEVEL_UP'])
    visited = set()
    dist = 0
    while to_visit:
        vertex = to_visit.popleft()
        if vertex == 'LEVEL_UP':
            dist += 1
            to_visit.append('LEVEL_UP')
            continue

        if vertex == end:
            return dist

        new_vertices = [n for n in graph[vertex] if n not in visited]
        to_visit += new_vertices
        visited |= set(new_vertices)


def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def build_graph(lines: list[str]) -> tuple[dict[str, list[str]], dict[str, int]]:
    graph = {}
    flows = {}

    for line in lines:
        letters = re.findall(r'[A-Z]{2}', line)
        source = letters[0]
        graph[source] = letters[1:]
        flows[source] = int(re.findall(r'\d+', line)[0])

    return graph, flows

run()
