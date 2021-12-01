from functools import reduce


def get_dense_hash(sparse_hash):
    BLOCK_SIZE = 16
    dense_hash = []
    for block_begin in range(0, BLOCK_SIZE * BLOCK_SIZE, BLOCK_SIZE):
        dense_byte = reduce(
            lambda x, y: x ^ y,
            sparse_hash[block_begin:block_begin+BLOCK_SIZE]
        )
        dense_hash.append(dense_byte)

    return dense_hash


def knot_hash(string_input):
    SIZE = 256
    circle = list(range(SIZE))
    current_position = 0
    skip_size = 0
    ROUNDS = 64

    lengths = [ord(c) for c in string_input] + [17, 31, 73, 47, 23]

    for _ in range(ROUNDS):
        for length in lengths:
            left_idx = current_position
            right_idx = (left_idx + length) % SIZE
            if left_idx <= right_idx:
                circle[left_idx:right_idx] = reversed(
                    circle[left_idx:right_idx])
            else:
                tmp_circle = circle * 3
                tmp_circle[left_idx:right_idx +
                           SIZE] = reversed(tmp_circle[left_idx:right_idx+SIZE])
                tmp_circle[left_idx+SIZE:right_idx+2 *
                           SIZE] = reversed(tmp_circle[left_idx+SIZE:right_idx+2*SIZE])
                circle = tmp_circle[SIZE:2*SIZE]

            current_position = (current_position + length + skip_size) % SIZE
            skip_size += 1

    dense_hash = get_dense_hash(circle)
    return ''.join([f'{x:02x}' for x in dense_hash])


def get_memory(prefix):
    size = 128
    memory = ['0' * (size + 2)]
    for row_number in range(size):
        value_to_hash = prefix + '-' + str(row_number)
        hash_value = knot_hash(value_to_hash)
        row = get_row_value(hash_value)
        memory.append(f'0{row}0')
    memory.append('0' * (size + 2))

    return memory

def get_row_value(hash_value):
    row = []
    for letter in hash_value:
        value = int(letter, 16)
        row.append(f'{value:04b}')

    return ''.join(row)


def get_group_containing(memory, start):
    to_visit = [start]
    visited = set()

    while to_visit:
        current = to_visit.pop()

        if current in visited:
            continue

        visited.add(current)
        to_visit += [p for p in neighbours(memory, current)
                     if p not in visited]

    return visited


def neighbours(memory, point):
    x, y = point
    potential_points = [
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1),
    ]

    return list(filter(
        lambda p: memory[p[1]][p[0]] == '1',
        potential_points
    ))


def all_memory_points(memory):
    points = []
    for y, row in enumerate(memory):
        for x, item in enumerate(row):
            if item == '0':
                continue
            points.append((x, y))

    return points


def solve(memory):
    points = all_memory_points(memory)
    rest_of_points = set(points)
    count = 0

    while rest_of_points:
        count += 1
        any_item = list(rest_of_points)[0]
        items_in_group = get_group_containing(memory, any_item)
        rest_of_points -= items_in_group

    return count


prefix = 'jzgqcdpd'
memory = get_memory(prefix)
result = solve(memory)
print(result)
