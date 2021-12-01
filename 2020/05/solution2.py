def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_id(seat: str):
    seat = seat.replace('F', '0')
    seat = seat.replace('B', '1')
    seat = seat.replace('L', '0')
    seat = seat.replace('R', '1')

    return int(seat, base=2)


taken_ids = set(map(get_id, get_lines()))
all_free_ids = set(range(min(taken_ids), max(taken_ids) + 1))
my_id = next(iter(all_free_ids - taken_ids))
print(my_id)
