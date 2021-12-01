def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_parsed_lines():
    return [parse_line(line) for line in get_lines()]


def parse_line(line):
    splitted = line.split()
    policy = splitted[0].split('-')
    first_idx = int(policy[0])
    second_idx = int(policy[1])
    letter = splitted[1][:-1]
    password = splitted[2]

    return first_idx, second_idx, letter, password


number_of_correct_passwords = 0

for first_idx, second_idx, letter, password in get_parsed_lines():
    number_of_matches = (password[first_idx - 1] == letter) + (password[second_idx - 1] == letter)
    number_of_correct_passwords += number_of_matches == 1

print(number_of_correct_passwords)
