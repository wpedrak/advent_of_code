import re


def get_lines(filename='19/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_molecule():
    return get_lines()[-1]


def get_replacements():
    return [parse_replecement(line) for line in get_lines()[:-2]]


def parse_replecement(line):
    return line.split(' => ')


def create(molecule, replecements):
    results = set()
    for source, target in replecements:
        for idx in find_all_indices(molecule, source):
            to_idx = idx
            from_idx = idx + len(source)
            results.add(molecule[:to_idx] + target + molecule[from_idx:])

    return results


def find_all_indices(string, substring):
    return [s.start() for s in re.finditer(substring, string)]


replecements = get_replacements()
molecule = get_molecule()
one_step_results = create(molecule, replecements)
print(len(one_step_results))
