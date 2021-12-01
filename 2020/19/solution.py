def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_rules():
    lines = get_lines()
    split_idx = lines.index('')
    return dict(parse_rule(line) for line in lines[:split_idx])


def parse_rule(line):
    colon_idx = line.index(':')
    rule_id = int(line[:colon_idx])
    rule_body = line[colon_idx + 2:]
    if '"' in rule_body:
        quote_idx = rule_body.index('"')
        return rule_id, rule_body[quote_idx + 1]

    alternative_strings = rule_body.split(' | ')
    alternatives = [[int(number) for number in alternative_string.split()] for alternative_string in alternative_strings]

    return rule_id, alternatives


def get_messages():
    lines = get_lines()
    split_idx = lines.index('')
    return lines[split_idx + 1:]


def get_all_correct_strings(rules):
    entry_mapping = {}
    for idx, rule in rules.items():
        if isinstance(rule, str):
            entry_mapping[idx] = {rule}

    return get_all_correct_strings_for_rule(rules, 0, entry_mapping)


def get_all_correct_strings_for_rule(rules, rule_idx, memory):
    if rule_idx in memory:
        return memory[rule_idx]

    rule = rules[rule_idx]
    rule_passing_strings = set()

    for alternative in rule:
        alternative_passing_strings = {''}
        correct_strings_for_values = [get_all_correct_strings_for_rule(rules, value, memory) for value in alternative]

        for correct_string_set in correct_strings_for_values:
            alternative_passing_strings = {old + new for old in alternative_passing_strings for new in correct_string_set}

        rule_passing_strings |= alternative_passing_strings

    memory[rule_idx] = rule_passing_strings
    return rule_passing_strings


rules = get_rules()
all_correct_messages = get_all_correct_strings(rules)

result = sum(map(
    lambda m: m in all_correct_messages,
    get_messages()
))

print(result)
