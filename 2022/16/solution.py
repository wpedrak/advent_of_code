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

    new_graph = {v: non_zero_valves for v in interesting_valves}

    max_preassure = release_max_preassure(new_graph, dist, flows, 'AA')
    print(max_preassure)


def release_max_preassure(graph: dict[str, list[str]], distance: dict[tuple[str, str], int], flows: dict[str, int], start: str) -> int:
    to_visit = [(start, set(), 30, 0)]
    max_preassure = 0
    while to_visit:
        vertex, visited, time, pressure = to_visit.pop()
        for neighbour in (n for n in graph[vertex] if n not in visited):
            dist = distance[(vertex, neighbour)]
            if time <= dist:
                continue
            new_pressure = pressure + (time - dist) * flows[neighbour]
            max_preassure = max(max_preassure, new_pressure)
            to_visit.append((neighbour, visited | {neighbour}, time - dist, new_pressure))

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
