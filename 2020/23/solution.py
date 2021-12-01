def take_three(cups, current_cup):
    current_cup_idx = cups.index(current_cup)
    right_slice = cups[current_cup_idx + 1:current_cup_idx + 4]
    right_slice_length = len(right_slice)
    left_slice = cups[:3 - right_slice_length]
    whole_slice = right_slice + left_slice

    return whole_slice, [cup for cup in cups if cup not in whole_slice]


def get_destination_cup(taken_cups, current_cup, max_cup):
    destination_cup = (current_cup - 1)
    destination_cup = (destination_cup - 1) % max_cup + 1
    while destination_cup in taken_cups:
        destination_cup -= 1
        destination_cup = (destination_cup - 1) % max_cup + 1

    return destination_cup


def insert_cups(rest_of_cups, taken_cups, destination_cup):
    destination_cup_idx = rest_of_cups.index(destination_cup)
    return rest_of_cups[:destination_cup_idx + 1] + taken_cups + rest_of_cups[destination_cup_idx + 1:]


def get_next(cups, current_cup):
    current_cup_idx = cups.index(current_cup)
    next_idx = (current_cup_idx + 1) % len(cups)
    return cups[next_idx]


if __name__ == '__main__':
    cups = [1, 5, 6, 7, 9, 4, 8, 2, 3]
    max_cup = max(cups)
    current_cup = cups[0]

    for _ in range(100):
        taken_cups, rest_of_cups = take_three(cups, current_cup)
        destination_cup = get_destination_cup(taken_cups, current_cup, max_cup)
        cups = insert_cups(rest_of_cups, taken_cups, destination_cup)
        current_cup = get_next(cups, current_cup)

    one_idx = cups.index(1)
    result = ''

    for shift in range(1, len(cups)):
        next_digit = cups[(one_idx + shift) % len(cups)]
        result += str(next_digit)

    print(result)
