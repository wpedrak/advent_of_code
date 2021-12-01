FACTOR_A = 16807
FACTOR_B = 48271
LIMIT = 2147483647
LAST_16_BITS = 0b1111111111111111
ITERATIONS = 5000000

def next_number_with_condition(previous, factor, divisibility_condition):
    number = next_number(previous, factor)
    while number % divisibility_condition != 0:
        number = next_number(number, factor)
    
    return number

def next_number(previous, factor):
    return (previous * factor) % LIMIT


def judge_compare(a_value, b_value):
    bit16_a = a_value & LAST_16_BITS
    bit16_b = b_value & LAST_16_BITS

    return bit16_a == bit16_b

judge_count = 0

a_value = 591
b_value = 393

for time in range(ITERATIONS):
    if time % 100000 == 0:
        print(time // 100000, '/50')
        print(judge_count)

    a_value = next_number_with_condition(a_value, FACTOR_A, 4)
    b_value = next_number_with_condition(b_value, FACTOR_B, 8)

    judge_count += judge_compare(a_value, b_value)

print(judge_count)
