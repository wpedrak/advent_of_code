REQUIRED_FIELDS = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
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


def has_all_fields(passport):
    for field in REQUIRED_FIELDS:
        if field not in passport:
            return False

    return True


def is_valid(passport):
    if not passport['byr'].isnumeric():
        return False

    byr = int(passport['byr'])
    if byr < 1920 or byr > 2002:
        return False

    if not passport['iyr'].isnumeric():
        return False

    iyr = int(passport['iyr'])
    if iyr < 2010 or iyr > 2020:
        return False

    eyr = int(passport['eyr'])
    if eyr < 2020 or eyr > 2030:
        return False

    hgh_unit = passport['hgt'][-2:]
    if not passport['hgt'][:-2].isnumeric():
        return False

    hgh_value = int(passport['hgt'][:-2])
    if hgh_unit == 'cm':
        if hgh_value < 150 or hgh_value > 193:
            return False
    elif hgh_unit == 'in':
        if hgh_value < 59 or hgh_value > 76:
            return False
    else:
        return False

    hcl = passport['hcl']
    if hcl[0] != '#' or len(hcl) != 7:
        return False

    hcl_color = hcl[1:]
    for letter in hcl_color:
        if letter not in '0123456789abcdef':
            return False

    ecl = passport['ecl']
    if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False

    pid = passport['pid']
    if len(pid) != 9 or not pid.isnumeric():
        return False

    return True


valid_passports_number = 0

for passport in get_passports():
    if not has_all_fields(passport):
        continue

    valid_passports_number += is_valid(passport)

print(valid_passports_number)
