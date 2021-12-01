from collections import Counter


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_parsed_lines():
    return [parse_line(line) for line in get_lines()]


def parse_line(line):
    splitted = line.split()
    policy = splitted[0].split('-')
    from_policy = int(policy[0])
    to_policy = int(policy[1])
    letter = splitted[1][:-1]
    password = splitted[2]

    return from_policy, to_policy, letter, password


number_of_correct_passwords = 0

for from_policy, to_policy, letter, password in get_parsed_lines():
    counter = Counter(password)
    number_of_correct_passwords += from_policy <= counter[letter] <= to_policy

print(number_of_correct_passwords)
