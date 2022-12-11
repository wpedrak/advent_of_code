def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def sum_small(tree: dir) -> int:
    _, result = size_sum_small(tree)
    return result

def size_sum_small(node) -> int:
    # leaf
    if isinstance(node, int):
        return node, 0

    # node
    node_size = 0
    small_sum = 0
    for child in node.values():
        child_size, child_small_sum = size_sum_small(child)
        node_size += child_size
        small_sum += child_small_sum

    if node_size <= 100000:
        small_sum += node_size

    return node_size, small_sum


tree = {'/': {}}
dir_stack = [tree]

for line in read_lines():
    # $ ls
    if line == '$ ls':
        continue

    parts = line.split(' ')

    # $ cd aaaaa
    if parts[0] == '$' and parts[1] == 'cd':
        destionation = parts[2]
        if destionation == '..':
            dir_stack.pop()
            continue
        dir_stack.append(dir_stack[-1][destionation])
        continue

    name = parts[1]

    # dir aaaaa
    if parts[0] == 'dir':
        dir_stack[-1][name] = {}
        continue

    # 1234 aaaaa
    dir_stack[-1][name] = int(parts[0])

print(sum_small(tree))
