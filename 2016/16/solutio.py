def get_lines(filename='16/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_aunts():
    return [parse_aunt(line) for line in get_lines()]


def parse_aunt(line):
    splited = line.split()
    number = int(splited[1][:-1])
    data_str = ''.join(splited[2:])
    data = data_str.split(',')

    informations = {}

    for info in data:
        name, quantity = info.split(':')
        informations[name] = int(quantity)

    return number, informations


def find_aunt(aunts, tape):
    for number, aunt_info in aunts:
        if not fits(aunt_info, tape):
            continue
        return number

    raise Exception('Aunt not found')


def fits(aunt_info, tape):
    for name, quantity in aunt_info.items():
        if tape[name] != quantity:
            return False

    return True


tape = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

aunts = get_aunts()
result = find_aunt(aunts, tape)

print(result)
