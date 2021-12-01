from collections import Counter


def get_lines(filename='19/input_simplified.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_molecule():
    return get_lines()[-1]


def get_changes_length(medicine):
    # observation: after renaming elements we spot that ~every reaction creates 2 new elements
    count = Counter(molecule)
    ones = count['1']
    deuces = count['2']
    threes = count['3']

    return len(medicine) - ones - deuces - 2 * threes - len('e')


molecule = get_molecule()
result = get_changes_length(molecule)
print(result)
