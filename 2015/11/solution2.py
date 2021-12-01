import re


def generate_password(old_password):
    password = increment_password(old_password)
    while not is_valid(password):
        password = increment_password(password)

    return password


def increment_password(password):
    password_as_number = 0
    for letter in password:
        password_as_number += ord(letter) - ord('a')
        password_as_number *= 26

    password_as_number //= 26
    new_password_as_number = password_as_number + 1

    new_password = []

    while new_password_as_number:
        new_password.append(chr(new_password_as_number % 26 + ord('a')))
        new_password_as_number //= 26

    return ''.join(reversed(new_password))


def is_valid(password):
    return have_3_up(password) and not is_confusing(password) and have_pairs(password)


def have_3_up(password):
    triplets = [chr(x) + chr(x+1) + chr(x+2) for x in range(ord('a'), ord('z') - 2 + 1)]
    for triplet in triplets:
        if triplet in password:
            return True

    return False


def is_confusing(password):
    return 'i' in password or 'o' in password or 'l' in password


def have_pairs(password):
    pattern_for_pair = r'(\w)\1'

    findings = re.findall(pattern_for_pair, password)

    return len(findings) >= 2


password = 'vzbxxyzz'
new_password = generate_password(password)
print(new_password)
