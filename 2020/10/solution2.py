def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_adapters():
    return [int(number) for number in get_lines()]


adapters = [0] + get_adapters()
my_device = max(adapters) + 3
adapters += [my_device]
sorted_adapters = sorted(adapters)

# no 2 jolt diffs

series_of_one_jolt = []
series = 0

for adapter, next_adapter in zip(sorted_adapters, sorted_adapters[1:]):
    jolt_diff = next_adapter - adapter
    if jolt_diff == 3:
        if series:
            series_of_one_jolt.append(series)
        series = 0
        continue

    series += 1

# seres are from 1 to 4
# print(series_of_one_jolt)

combinations = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
}

possible_combinations = 1

for series in series_of_one_jolt:
    possible_combinations *= combinations[series]

print(possible_combinations)
