def get_lines(filename='input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_dimensions():
    return [parse_dimensions(line) for line in get_lines()]


def parse_dimensions(line):
    return [int(d) for d in line.split('x')]


def needed_ribbon(l, w, h):
    a, b, _ = sorted([l, w, h])
    return l*w*h + 2*(a+b)


ribbon = 0
for dimensions in get_dimensions():
    ribbon += needed_ribbon(*dimensions)

print(ribbon)
