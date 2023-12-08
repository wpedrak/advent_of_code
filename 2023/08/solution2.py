import re, math

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def build_node_map(lines: list[str])-> dict:
    node_map = {}
    for line in lines[2:]:
        node, left, right = re.findall(r'\w+', line)
        node_map[node] = {'L': left, 'R': right}
    return node_map

def travel(node_map: dict, directions: str, start_node: str) -> int:
    node = start_node
    steps = 0
    while not node.endswith('Z'):
        direction = directions[steps % len(directions)]
        steps += 1
        node = node_map[node][direction]

    return steps

lines = get_lines()
node_map = build_node_map(lines)
steps = [travel(node_map, lines[0], n) for n in node_map if n.endswith('A')]
print(math.lcm(*steps))
