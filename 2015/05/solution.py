from collections import Counter, defaultdict


def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def is_nice(string):
    have_three_vowels = count_vowels(string) >= 3
    have_doublet = check_if_have_doublet(string)
    have_bad_substring = check_if_have_bad_substring(string)

    return have_three_vowels and have_doublet and not have_bad_substring


def count_vowels(string):
    vowels = 'aeiou'
    occurences_count = defaultdict(lambda: 0, Counter(string))
    count = 0
    for vowel in vowels:
        count += occurences_count[vowel]

    return count


def check_if_have_doublet(string):
    return any(map(
        lambda t: t[0] == t[1],
        zip(string, '-' + string)
    ))


def check_if_have_bad_substring(string):
    bad_strings = ['ab', 'cd', 'pq', 'xy']

    return any(map(
        lambda bs: bs in string,
        bad_strings
    ))


nice_count = 0
for string in get_lines():
    nice_count += is_nice(string)

print(nice_count)
