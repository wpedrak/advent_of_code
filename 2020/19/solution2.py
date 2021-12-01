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


def get_all_correct_strings(rules, rule_idx):
    entry_mapping = {}
    for idx, rule in rules.items():
        if isinstance(rule, str):
            entry_mapping[idx] = {rule}

    return get_all_correct_strings_for_rule(rules, rule_idx, entry_mapping)


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


def research(rules, messages):
    # each of 31, 42 yields set of 8-char long strings
    valid_strings_for_31 = get_all_correct_strings(rules, 31)
    valid_strings_for_42 = get_all_correct_strings(rules, 42)

    print({len(m) for m in valid_strings_for_31})
    print({len(m) for m in valid_strings_for_42})

    # max length of message is 88
    max_length_message = max(messages, key=lambda m: len(m))
    print(len(max_length_message))

    # original setup (will loop forever)
    # rules[8] = [[42], [42, 8]]
    # rules[11] = [[42, 31], [42, 11, 31]]
    # get_all_correct_strings(rules, 0)

    # finite set based on research (python process was killed)
    # rules[8] = [[42] * i for i in range(1, 12)]
    # rules[11] = [[42] * i + [31] * i for i in range(1, 6)]
    # get_all_correct_strings(rules, 0)

    # reminder: "0: 8 11" (python process was killed)
    # rules[0] = [[42] * i + [31] * (11 - i) for i in range(6, 11)]
    # get_all_correct_strings(rules, 0)

    # however above can be used explicitly


def is_message_valid(valid_strings_for_31, valid_strings_for_42, message):
    chunk_messages_length = 8
    if len(message) % chunk_messages_length != 0:
        return False

    chunked_message = [message[idx:idx + chunk_messages_length] for idx in range(0, len(message), chunk_messages_length)]
    number_of_chunks = len(chunked_message)

    for split_idx in range(number_of_chunks // 2 + 1, number_of_chunks):
        if is_split_valid(valid_strings_for_31, valid_strings_for_42, chunked_message[:split_idx], chunked_message[split_idx:]):
            return True

    return False


def is_split_valid(valid_strings_for_31, valid_strings_for_42, first_part, second_part):
    assert len(first_part) > len(second_part)
    for chunk in first_part:
        if chunk not in valid_strings_for_42:
            return False

    for chunk in second_part:
        if chunk not in valid_strings_for_31:
            return False

    return True


rules = get_rules()
messages = get_messages()

# research(rules, messages)

valid_strings_for_31 = get_all_correct_strings(rules, 31)
valid_strings_for_42 = get_all_correct_strings(rules, 42)

result = sum(map(
    lambda m: is_message_valid(valid_strings_for_31, valid_strings_for_42, m),
    messages
))

print(result)
