import re
from collections import defaultdict, deque

rsc = tuple[int, int, int, int]

def add_tup(a: rsc, b: rsc) -> rsc:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2], a[3]+b[3])

def sub_tup(a: rsc, b: rsc) -> rsc:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2], a[3]-b[3])

def geodes(a: rsc) -> int:
    return a[3]

def is_neg_tup(a: rsc) -> bool:
    return a[0] < 0 or a[1] < 0 or a[2] < 0 or a[3] < 0

def resource_by_idx(idx: int) -> rsc:
    resource_list = [0, 0, 0, 0]
    resource_list[idx] = 1
    return tuple(resource_list)

class Factory:
    def __init__(self, ore_cost: int, clay_cost: int, obsidian_cost_ore: int, obsidian_cost_clay: int, geode_cost_ore: int, geode_cost_obsidian: int) -> None:
        self.cost = [
            (ore_cost, 0, 0, 0),
            (clay_cost, 0, 0, 0),
            (obsidian_cost_ore, obsidian_cost_clay, 0, 0),
            (geode_cost_ore, 0, geode_cost_obsidian, 0),
        ]

    def can_buy(self, resources: rsc, robot_index: int) -> bool:
        return not is_neg_tup(sub_tup(resources, self.cost[robot_index]))

    def posible_targets(self, robots: rsc) -> list[int]:
        if robots[2]:
            return [0, 1, 2, 3] # will also return correct value if changed to [2, 3]
        if robots[1]:
            return [0, 1, 2] #  will also return correct value if changed to [1, 2]
        return [0, 1]

def run() -> None:
    result = 0
    for line in read_lines(file_name='2022/19/input.txt'):
    # for line in read_lines():
        blueprint_id, factory = parse(line)
        geodes_count = test(factory)
        result += blueprint_id * geodes_count
        print(blueprint_id, geodes_count)

    print(result)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse(line: str) -> tuple[int, Factory]:
    values = [int(v) for v in  re.findall(r'\d+', line)]
    return values[0], Factory(*values[1:])

def test(factory: Factory) -> int:
    to_visit = deque([((1, 0, 0, 0), None, (0, 0, 0, 0), target_robot, 24) for target_robot in [0, 1]])
    visited = defaultdict(lambda: -1)
    max_geodes = 0

    while to_visit:
        item = to_visit.popleft()
        robots, robot_in_factory, resources, target_robot, time = item

        if time > 0 and robot_in_factory is not None:
            resources = add_tup(resources, robots)
            time -= 1
            robots = add_tup(robots, resource_by_idx(robot_in_factory))

        while time > 0 and not factory.can_buy(resources, target_robot):
            resources = add_tup(resources, robots)
            time -= 1

        # run out of time, check geodes
        if time <= 0:
            max_geodes = max(max_geodes, geodes(resources))
            continue

        # pay resources, build robot
        resources = sub_tup(resources, factory.cost[target_robot])
        robot_in_factory = target_robot

        for next_target_robot in factory.posible_targets(robots):
            new_item = (robots, robot_in_factory, resources, next_target_robot, time)
            visit_key = (robots, robot_in_factory, resources, next_target_robot)
            if visited[visit_key] >= time:
                continue

            visited[visit_key] = time
            to_visit.append(new_item)

    return max_geodes

run()
# If running too long, one can apply changes to posible_targets function.
# This is not guaranteed to give correct result, tho.
