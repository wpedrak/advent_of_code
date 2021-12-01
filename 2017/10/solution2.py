from functools import reduce

def get_dense_hash(sparse_hash):
    BLOCK_SIZE = 16
    dense_hash = []
    for block_begin in range(0, BLOCK_SIZE * BLOCK_SIZE, BLOCK_SIZE):
        dense_byte = reduce(
            lambda x,y: x ^ y,
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

    lengths = [ord(c) for c in string_input] + [17,31,73,47,23]
    
    for _ in range(ROUNDS):
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

    dense_hash = get_dense_hash(circle)
    return ''.join([hex(x)[2:] for x in dense_hash])
    

result = knot_hash('227,169,3,166,246,201,0,47,1,255,2,254,96,3,97,144')
print(result)
