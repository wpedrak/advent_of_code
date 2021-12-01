lengths = [227, 169, 3, 166, 246, 201, 0, 47, 1, 255, 2, 254, 96, 3, 97, 144]

SIZE = 256
circle = list(range(SIZE))
current_position = 0
skip_size = 0

for length in lengths:
    left_idx = current_position
    right_idx = (left_idx + length) % SIZE
    if left_idx <= right_idx:
        circle[left_idx:right_idx] = reversed(circle[left_idx:right_idx])
    else:
        tmp_circle = circle * 3
        tmp_circle[left_idx:right_idx + SIZE] = reversed(tmp_circle[left_idx:right_idx+SIZE])
        tmp_circle[left_idx+SIZE:right_idx+2 * SIZE] = reversed(tmp_circle[left_idx+SIZE:right_idx+2*SIZE])
        circle = tmp_circle[SIZE:2*SIZE]

    current_position = (current_position + length + skip_size) % SIZE
    skip_size += 1

print(circle[0] * circle[1])
