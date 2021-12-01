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


max_id_seat = max(get_lines(), key=get_id)
print(get_id(max_id_seat))
