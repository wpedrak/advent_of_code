def get_nearby_tickets_lines():
    nearby_tickets_section = open("input.txt", "r").read().split('\n\n')[2]
    return nearby_tickets_section.split('\n')[1:]


def get_nearby_tickets():
    return [parse_ticket(line) for line in get_nearby_tickets_lines()]


def parse_ticket(line):
    return [int(value) for value in line.split(',')]


def get_rules_lines():
    rules_section = open("input.txt", "r").read().split('\n\n')[0]
    return rules_section.split('\n')


def get_rules():
    return [parse_rule(line) for line in get_rules_lines()]


def parse_rule(line):
    name, ranges = line.split(': ')
    range1, range2 = ranges.split(' or ')
    range1_from, range1_to = [int(x) for x in range1.split('-')]
    range2_from, range2_to = [int(x) for x in range2.split('-')]

    return name, range1_from, range1_to, range2_from, range2_to


def is_field_valid(rules, field):
    for _, range1_from, range1_to, range2_from, range2_to in rules:
        if range1_from <= field <= range1_to:
            return True

        if range2_from <= field <= range2_to:
            return True

    return False


error_rate = 0

rules = get_rules()
tickets = get_nearby_tickets()

for ticket in tickets:
    for field in ticket:
        if not is_field_valid(rules, field):
            error_rate += field

print(error_rate)
