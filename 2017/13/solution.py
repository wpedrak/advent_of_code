def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_firewall():
    firewall = {}
    for line in get_lines():
        depth, scan_range = line.split(': ')
        firewall[int(depth)] = int(scan_range)

    return firewall

firewall = get_firewall()
trip_severity = 0

for depth, scan_range in firewall.items():
    if depth % ((scan_range - 1) * 2) == 0:
        trip_severity += depth * scan_range

print(trip_severity)
