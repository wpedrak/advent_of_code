def get_groups():
    file = open("input.txt", "r").read()[:-1]
    return file.split('\n\n')


def get_lines_from_group(group):
    return group.split('\n')


def get_groups_lines():
    return [get_lines_from_group(group) for group in get_groups()]


sum_count = 0

for group_lines in get_groups_lines():
    group_letters = set()
    for line in group_lines:
        group_letters |= set(line)

    sum_count += len(group_letters)

print(sum_count)
