import re


def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def is_nice(string):
    return have_double_doublet(string) and have_aba(string)


def have_double_doublet(string):
    regexp = r'(\w\w)\w*\1'
    return len(re.findall(regexp, string)) > 0


def have_aba(string):
    regexp = r'(\w)\w\1'
    return len(re.findall(regexp, string)) > 0


nice_count = 0
for string in get_lines():
    nice_count += is_nice(string)

print(nice_count)
