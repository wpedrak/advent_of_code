from bisect import bisect_right

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def all_dir_sizes(tree: dir) -> list[int]:
    _, result = all_dir_sizes_aux(tree)
    return result

def all_dir_sizes_aux(node) -> tuple[int, list[int]]:
    # leaf
    if isinstance(node, int):
        return node, []

    # node
    node_size = 0
    node_dir_sizes = []
    for child in node.values():
        child_size, child_dir_sizes = all_dir_sizes_aux(child)
        node_size += child_size
        node_dir_sizes += child_dir_sizes

    return node_size, node_dir_sizes + [node_size]


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

dirs_sizes = list(sorted(all_dir_sizes(tree['/'])))
root_size = dirs_sizes[-1]
free_space = 70000000 - root_size
missing_space = 30000000 - free_space

print(dirs_sizes[bisect_right(dirs_sizes, missing_space)])
