def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_busses_with_offset():
    all_busses = get_lines()[1].split(',')
    return [(offset, int(bus)) for offset, bus in enumerate(all_busses) if bus != 'x']


def bezout_coefficients(number1, number2):
    old_r, r = number1, number2
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_s, old_t


def solve_congruences(congruences):
    modulo_product = 1
    for _, modulo in congruences:
        modulo_product *= modulo

    result = 0

    for y, modulo in congruences:
        _, g = bezout_coefficients(modulo, modulo_product // modulo)

        result += y * g * (modulo_product // modulo)

    return result % modulo_product


congruences = [(bus - offset, bus) for offset, bus in get_busses_with_offset()]
result = solve_congruences(congruences)
print(result)
