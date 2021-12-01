OCCUPIED = '#'
EMPTY = 'L'
FLOOR = '.'


def get_lines(file_name="input.txt"):
    file = open(file_name, "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_area():
    return [list(line) for line in get_lines()]


def find_first(sitting_area, middle_x, middle_y, dx, dy):
    height = len(sitting_area)
    width = len(sitting_area[0])

    x = middle_x + dx
    y = middle_y + dy

    while 0 <= x < width and 0 <= y < height and sitting_area[y][x] == FLOOR:
        x += dx
        y += dy

    if 0 <= x < width and 0 <= y < height:
        return x, y

    return None


def get_neighbour(sitting_area, middle_x, middle_y):
    deltas = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]

    neighbours = []

    for dx, dy in deltas:
        target = find_first(sitting_area, middle_x, middle_y, dx, dy)
        if not target:
            continue

        neighbours.append(target)

    return neighbours


def count_occupied_neighbours(sitting_area, middle_x, middle_y):
    neighbours = get_neighbour(sitting_area, middle_x, middle_y)

    return sum([sitting_area[y][x] == OCCUPIED for x, y in neighbours])


def get_next(sitting_area):
    next_area = [row[:] for row in sitting_area]

    for y, row in enumerate(sitting_area):
        for x, cell in enumerate(row):
            if cell == FLOOR:
                continue

            # print(x, y)
            occupied_neighbours_count = count_occupied_neighbours(sitting_area, x, y)

            if cell == EMPTY and occupied_neighbours_count == 0:
                next_area[y][x] = OCCUPIED

            if cell == OCCUPIED and occupied_neighbours_count >= 5:
                next_area[y][x] = EMPTY

    return next_area


def count_seats(sitting_area):
    return sum(map(
        lambda row: sum(map(
            lambda cell: cell == OCCUPIED,
            row
        )),
        sitting_area
    ))


def print_area(sitting_area):
    print('\n'.join([''.join(row) for row in sitting_area]) + '\n')


if __name__ == '__main__':
    sitting_area = get_area()
    previous_sitting_area = None
    counter = 0

    while sitting_area != previous_sitting_area:
        previous_sitting_area = sitting_area
        sitting_area = get_next(sitting_area)
        counter += 1
        print(counter)

    result = count_seats(sitting_area)
    print(result)
