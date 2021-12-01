from math import sqrt


def find_house(gifts_number):
    number = 786240  # result from previous part
    while get_gifts_sum(number) < gifts_number:
        if number % 1000 == 0:
            print(f'{number}/{gifts_number // 10}')
        number += 1

    return number


def get_gifts_sum(number):
    gifts_sum = 0

    for potential_divider in range(1, int(sqrt(number))):
        div = number // potential_divider
        if number % div == 0 and div * 50 >= number:
            gifts_sum += 11 * div

    return gifts_sum


gifts_to_gather = 34000000
house_nr = find_house(gifts_to_gather)
print(house_nr)
