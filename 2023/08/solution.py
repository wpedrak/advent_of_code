import re

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def build_node_map(lines: list[str])-> dict:
    node_map = {}
    for line in lines[2:]:
        node, left, right = re.findall(r'\w+', line)
        node_map[node] = {'L': left, 'R': right}
    return node_map

lines = get_lines()
node_map = build_node_map(lines)

directions = lines[0]
node = 'AAA'
steps = 0
while node != 'ZZZ':
    direction = directions[steps % len(directions)]
    steps += 1
    node = node_map[node][direction]

print(steps)
