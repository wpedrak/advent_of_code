def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def get_firewall():
    firewall = {}
    for line in get_lines():
        depth, scan_range = line.split(': ')
        firewall[int(depth)] = int(scan_range)

    return firewall

def caught(firewall, delay):
    for depth, scan_range in firewall.items():
        if (depth + delay) % ((scan_range - 1) * 2) == 0:
            return True

    return False

def solve(firewall):
    delay = 0
    while caught(firewall, delay):
        delay += 1

    return delay

firewall = get_firewall()
result = solve(firewall)

print(result)
