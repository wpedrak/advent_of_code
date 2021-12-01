FACTOR_A = 16807
FACTOR_B = 48271
LIMIT = 2147483647
LAST_16_BITS = 0b1111111111111111
ITERATIONS = 40000000

def next_number(previous, factor):
    return (previous * factor) % LIMIT

judge_count = 0

a_value = 591
b_value = 393

for time in range(ITERATIONS):
    if time % 1000000 == 0:
        print(time)
        print(judge_count)

    a_value = next_number(a_value, FACTOR_A)
    b_value = next_number(b_value, FACTOR_B)

    bit16_a = a_value & LAST_16_BITS
    bit16_b = b_value & LAST_16_BITS

    judge_count += bit16_a == bit16_b

print(judge_count)
