import re
from collections import defaultdict, deque

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

    max_preassure = release_max_preassure(set(non_zero_valves), dist, flows, 'AA')
    print(max_preassure)


def release_max_preassure(non_zero_valves: set[str], distance: dict[tuple[str, str], int], flows: dict[str, int], start: str) -> int:
    to_visit = [(start, start, set(), 26, 26, 0)]
    max_preassure = 0
    best_pressure = defaultdict(int)
    it = 0
    while to_visit:
        it += 1
        if not it % 100000:
            print(max_preassure, f'{it//1000000}M')
            print(len(best_pressure))

        me, elephant, visited, my_time, elephant_time, pressure = to_visit.pop()
        not_visited = non_zero_valves - visited

        my_reachable_neighbours = [nv for nv in not_visited if distance[(me, nv)] < my_time]
        for neighbour in my_reachable_neighbours:
            dist = distance[(me, neighbour)]
            new_pressure = pressure + (my_time - dist) * flows[neighbour]
            state = (neighbour, elephant, frozenset(visited | {neighbour}), my_time - dist, elephant_time)
            if new_pressure <= best_pressure[state]:
                continue
            best_pressure[state] = new_pressure
            max_preassure = max(max_preassure, new_pressure)
            to_visit.append((neighbour, elephant, visited | {neighbour}, my_time - dist, elephant_time, new_pressure))

        elephant_reachable_neighbours = [nv for nv in not_visited if distance[(elephant, nv)] < elephant_time]
        for neighbour in elephant_reachable_neighbours:
            dist = distance[(elephant, neighbour)]
            new_pressure = pressure + (elephant_time - dist) * flows[neighbour]
            state = (me, neighbour, frozenset(visited | {neighbour}), my_time, elephant_time - dist)
            if new_pressure <= best_pressure[state]:
                continue
            best_pressure[state] = new_pressure
            max_preassure = max(max_preassure, new_pressure)
            to_visit.append((me, neighbour, visited | {neighbour}, my_time, elephant_time - dist, new_pressure))

    return max_preassure

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
