def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_dimensions():
    return [parse_dimensions(line) for line in get_lines()]


def parse_dimensions(line):
    return [int(d) for d in line.split('x')]


def needed_paper(l, w, h):
    squares = [l*w, w*h, h*l]
    smallest = min(squares)
    return 2 * sum(squares) + smallest


paper = 0
for dimmensions in get_dimensions():
    paper += needed_paper(*dimmensions)

print(paper)
