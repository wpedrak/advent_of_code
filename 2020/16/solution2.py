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


def get_my_ticket():
    rules_section = open("input.txt", "r").read().split('\n\n')[1]
    return parse_ticket(rules_section.split('\n')[1])


def is_ticket_valid(rules, ticket):
    for field in ticket:
        if not is_field_valid(rules, field):
            return False

    return True


def is_field_valid(rules, field):
    return len(get_rules_matching_field(rules, field)) > 0


def get_rules_matching_field(rules, field):
    matched_rules = []

    for name, range1_from, range1_to, range2_from, range2_to in rules:
        if range1_from <= field <= range1_to:
            matched_rules.append(name)

        if range2_from <= field <= range2_to:
            matched_rules.append(name)

    return matched_rules


def get_columns_sets(tickets):
    number_of_columns = len(tickets[0])
    column_sets = []

    for column_idx in range(number_of_columns):
        column_set = set()
        for ticket in tickets:
            column_set.add(ticket[column_idx])

        column_sets.append(column_set)

    return column_sets


def get_rules_matching_set(rules, column_set):
    matching_rules = set(name for name, _, _, _, _ in rules)

    for field in column_set:
        rules_matching_field = get_rules_matching_field(rules, field)
        matching_rules &= set(rules_matching_field)

    return matching_rules


rules = get_rules()
my_ticket = get_my_ticket()
tickets = [ticket for ticket in get_nearby_tickets() if is_ticket_valid(rules, ticket)]
column_sets = get_columns_sets(tickets)

mapping = {}
unmatched_rules = rules[:]

while len(mapping) < len(rules):
    for idx, column_set in enumerate(column_sets):
        if idx in mapping:
            continue

        matching_rule_names = get_rules_matching_set(unmatched_rules, column_set)
        if len(matching_rule_names) == 1:
            matched_rule_name = list(matching_rule_names)[0]
            mapping[idx] = matched_rule_name
            unmatched_rules = list(filter(
                lambda r: r[0] != matched_rule_name,
                unmatched_rules
            ))

result = 1

for idx, field in enumerate(my_ticket):
    if mapping[idx].startswith('departure'):
        result *= field

print(result)
