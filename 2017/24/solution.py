def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def parse_components():
    lines = get_lines()
    return [parse_component(line) for line in lines]


def parse_component(line):
    return tuple(int(port) for port in line.split('/'))


def bridge_strength(port, components):
    all_having_port = filter(
        lambda c: c[0] == port or c[1] == port,
        components
    )

    results = []

    for component in all_having_port:
        other_port = get_other_port(component, port)
        without_current = components - set([component])
        without_component = bridge_strength(other_port, without_current)
        results.append(without_component + port + other_port)

    if not results:
        return 0

    return max(results)


def get_other_port(component, port):
    port1, port2 = component

    return port2 if port == port1 else port1


def solve(components):
    components = set(components)
    start_port = 0

    streangth = bridge_strength(start_port, components)

    return streangth


components = parse_components()
result = solve(components)

print(result)
