import re
import functools
from collections import defaultdict, deque

class Resources:
    def __init__(self, ore: int, clay: int, obsidian: int, geodes: int) -> None:
        self.tup = (ore, clay, obsidian, geodes)

    def __add__(self, r):
        return Resources(*(t1 + t2 for t1, t2 in zip(self.tup, r.tup)))

    def __sub__(self, r):
        return self + Resources(*(-t for t in r.tup))

    def is_negative(self) -> bool:
        return any((t < 0 for t in self.tup))

    def __repr__(self) -> str:
        return str(self.tup)

    def __hash__(self):
        return hash(self.tup)

    def __eq__(self, r) -> bool:
        return self.tup == r.tup

    def geodes(self) -> int:
        return self.tup[3]

class Factory:
    def __init__(self, ore_cost: int, clay_cost: int, obsidian_cost_ore: int, obsidian_cost_clay: int, geode_cost_ore: int, geode_cost_obsidian: int) -> None:
        self.ore_robot_cost = Resources(ore_cost, 0, 0, 0)
        self.clay_robot_cost = Resources(clay_cost, 0, 0, 0)
        self.obsidian_robot_cost = Resources(obsidian_cost_ore, obsidian_cost_clay, 0, 0)
        self.geode_robot_cost = Resources(geode_cost_ore, 0, geode_cost_obsidian, 0)
        print(self.ore_robot_cost)
        print(self.clay_robot_cost)
        print(self.obsidian_robot_cost)
        print(self.geode_robot_cost)

    def cost_by_idx(self, idx: int):
        return [self.ore_robot_cost, self.clay_robot_cost, self.obsidian_robot_cost, self.geode_robot_cost][idx]

    @functools.cache
    def possible_production(self, resources: Resources) -> list[tuple[Resources, Resources]]:
        return self.__possible_production_aux(resources, 0)


    def __possible_production_aux(self, resources: Resources, idx: int) -> list[tuple[Resources, Resources]]:
        if idx >= 4:
            return [(Resources(0, 0, 0, 0), Resources(0, 0, 0, 0))]

        no_buy_options = self.__possible_production_aux(resources, idx+1)
        robot_cost = self.cost_by_idx(idx)
        post_buy_resources = resources - robot_cost
        if post_buy_resources.is_negative():
            return no_buy_options

        one_robot_list = [0, 0, 0, 0]
        one_robot_list[idx] = 1
        one_robot = Resources(*one_robot_list)
        post_buy_options = [(one_robot + option, robot_cost + cost) for option, cost in self.__possible_production_aux(post_buy_resources, idx)]

        return no_buy_options + post_buy_options


def run() -> None:
    result = 0
    for line in read_lines():
        blueprint_id, factory = parse(line)
        geodes = test(factory)
        result += blueprint_id * geodes
        print(blueprint_id, geodes)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse(line: str) -> tuple[int, Resources]:
    values = [int(v) for v in  re.findall(r'\d+', line)]
    return values[0], Factory(*values[1:])

def test(factory: Factory) -> int:
    to_visit = deque([(Resources(1, 0, 0, 0), Resources(0, 0, 0, 0), 24)])
    visited = defaultdict(lambda: 25)
    it = 0
    max_geodes = 0

    while to_visit:
        item = to_visit.popleft()
        robots, resources, time = item
        if visited[(robots, resources)] < time:
            continue

        it += 1
        max_geodes = max(max_geodes, resources.geodes())
        if not it % 10000:
            print(max_geodes, it, len(visited), time)
        if time == 0:
            continue

        for new_robots, cost in factory.possible_production(resources):
            resources_after_minute = resources - cost + robots
            robots_after_minute = robots + new_robots
            
            new_item = (robots_after_minute, resources_after_minute, time - 1)
            if visited[(robots_after_minute, resources_after_minute)] <= time - 1:
                continue

            visited[(robots_after_minute, resources_after_minute)] = time - 1
            to_visit.append(new_item)


    return max_geodes

run()
