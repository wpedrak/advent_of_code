def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_adapters():
    return [int(number) for number in get_lines()]


adapters = [0] + get_adapters()
sorted_adapters = sorted(adapters)

one_jolt_diff = 0
three_jolt_diff = 1

for adapter, next_adapter in zip(sorted_adapters, sorted_adapters[1:]):
    jolt_diff = next_adapter - adapter
    one_jolt_diff += jolt_diff == 1
    three_jolt_diff += jolt_diff == 3

print(one_jolt_diff * three_jolt_diff)
