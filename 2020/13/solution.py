def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_timestamp():
    return int(get_lines()[0])


def get_busses():
    all_busses = get_lines()[1].split(',')
    return [int(bus) for bus in all_busses if bus != 'x']


timestamp = get_timestamp()

time_and_bus = [((bus - timestamp) % bus, bus) for bus in get_busses()]
min_time = min(time_and_bus)
print(min_time[0] * min_time[1])
