REQUIRED_FIELDS = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid',
]


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_passports():
    passports = []
    current_passport = {}

    for line in get_lines():
        if not line:
            passports.append(current_passport)
            current_passport = {}
            continue

        key_value_list = dict([key_value_string.split(':') for key_value_string in line.split()])
        current_passport.update(key_value_list)

    if current_passport:
        passports.append(current_passport)

    return passports


def is_valid_passport(passport):
    for field in REQUIRED_FIELDS:
        if field not in passport:
            return False

    return True


valid_passports_number = 0

for passport in get_passports():
    valid_passports_number += is_valid_passport(passport)

print(valid_passports_number)
