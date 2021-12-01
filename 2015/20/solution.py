from math import sqrt


def find_house(gifts_number):
    dividers_sum = gifts_number // 10
    number = 1
    while get_dividers_sum(number) < dividers_sum:
        if number % 1000 == 0:
            print(f'{number}/{dividers_sum}')
        number += 1

    return number


def get_dividers_sum(number):
    dividers_sum = 0
    for potential_divider in range(1, int(sqrt(number)) + 1):
        if number % potential_divider == 0:
            dividers_sum += potential_divider
            dividers_sum += number // potential_divider

    return dividers_sum


gifts_to_gather = 34000000
house_nr = find_house(gifts_to_gather)
print(house_nr)
