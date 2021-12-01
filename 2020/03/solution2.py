def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def count_trees(tree_map, step_right, step_down):
    height = len(tree_map)
    width = len(tree_map[0])
    number_of_trees = 0
    x = 0

    for y in range(0, height, step_down):
        row = tree_map[y]
        number_of_trees += row[x % width] == '#'
        x += step_right

    return number_of_trees


tree_map = get_lines()
tree_product = 1

for step_right, step_down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    tree_product *= count_trees(tree_map, step_right, step_down)

print(tree_product)
