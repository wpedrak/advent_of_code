import re
import functools
from collections import deque

rsc = tuple[int, int, int, int]
bns = tuple[bool, bool, bool, bool]

def add_tup(a: tuple, b: tuple) -> tuple:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2], a[3]+b[3])

def sub_tup(a: tuple, b: tuple) -> tuple:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2], a[3]-b[3])

def geodes(a: tuple) -> int:
    return a[3]

def is_neg_tup(a: tuple) -> bool:
    return a[0] < 0 or a[1] < 0 or a[2] < 0 or a[3] < 0

class Factory:
    def __init__(self, ore_cost: int, clay_cost: int, obsidian_cost_ore: int, obsidian_cost_clay: int, geode_cost_ore: int, geode_cost_obsidian: int) -> None:
        self.cost = [
            (ore_cost, 0, 0, 0),
            (clay_cost, 0, 0, 0),
            (obsidian_cost_ore, obsidian_cost_clay, 0, 0),
            (geode_cost_ore, 0, geode_cost_obsidian, 0),
        ]

    @functools.cache
    def possible_production(self, resources: rsc, bans: bns) -> list[tuple[rsc, rsc, bns]]:
        spendable_resources = list(resources)
        spendable_resources[3] = 0
        spendable_resources = tuple(spendable_resources)
        result = []
        for robots, prices in self.__possible_production_aux(spendable_resources, 0):
            # don't allow banned robots
            if any(b and r for b, r in zip(bans, robots)):
                continue

            # something was bought
            new_bans = [False] * 4
            if robots == (0, 0, 0, 0):
                # nothing was bought
                new_bans = list(bans)

            money_left = sub_tup(resources, prices)
            for idx in range(4):
                if robots[idx]:
                    continue
                # ban if had resources to buy the robot
                new_bans[idx] |= not is_neg_tup(sub_tup(money_left, self.cost[idx]))

            if all(new_bans):
                continue

            result.append((robots, money_left, tuple(new_bans)))

        return result


    @functools.cache
    def __possible_production_aux(self, resources: rsc, idx: int) -> list[tuple[rsc, rsc]]:
        if idx >= 4:
            return [((0, 0, 0, 0), (0, 0, 0, 0))]

        no_buy_options = self.__possible_production_aux(resources, idx+1)
        robot_cost = self.cost[idx]
        post_buy_resources = sub_tup(resources, robot_cost)
        if is_neg_tup(post_buy_resources):
            return no_buy_options

        one_robot_list = [0, 0, 0, 0]
        one_robot_list[idx] = 1
        one_robot = tuple(one_robot_list)
        post_buy_options = [(add_tup(one_robot, option), add_tup(robot_cost, cost)) for option, cost in self.__possible_production_aux(post_buy_resources, idx)]

        return no_buy_options + post_buy_options

def run() -> None:
    result = 0
    for line in read_lines():
        blueprint_id, factory = parse(line)
        geodes_count = test(factory)
        result += blueprint_id * geodes_count
        print(blueprint_id, geodes_count)

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def parse(line: str) -> tuple[int, Factory]:
    values = [int(v) for v in  re.findall(r'\d+', line)]
    return values[0], Factory(*values[1:])

def test(factory: Factory) -> int:
    to_visit = deque([((1, 0, 0, 0), (0,) * 4, (False,) * 4), 'TICK'])
    visited = set()
    it = 0
    max_geodes = 0
    # prev = {}
    time = 24

    while to_visit:
        item = to_visit.popleft()

        if item == 'TICK':
            time -= 1
            if time == 0:
                return max_geodes
            print(max_geodes, it, len(visited), len(to_visit), time)
            to_visit.append('TICK')
            continue

        robots, resources, bans = item

        it += 1
        if not it % 10000:
            print(max_geodes, it, len(visited), len(to_visit), time)

        for new_robots, resources_left, new_bans in factory.possible_production(resources, bans):
            resources_after_minute = add_tup(resources_left, robots)
            robots_after_minute = add_tup(robots, new_robots)

            # limit = 5
            # if robots_after_minute[0] > limit or robots_after_minute[1] > limit or robots_after_minute[2] > limit:
            #     continue

            new_item = (robots_after_minute, resources_after_minute, new_bans)
            if new_item in visited:
                continue

            visited.add(new_item)

            if time > 1:
                to_visit.append(new_item)
            # prev[new_item] = item

            if max_geodes < geodes(resources_after_minute):
                max_geodes = geodes(resources_after_minute)
                print(max_geodes, it, len(visited), time)
                print(new_item)
                # tmp = new_item
                # tmp2 = []
                # while tmp in prev:
                #     tmp2.append(tmp)
                #     tmp = prev[tmp]
                # tmp2.append(tmp)
                # for tmp3 in reversed(tmp2):
                #     print(tmp3)


    return max_geodes

run()
