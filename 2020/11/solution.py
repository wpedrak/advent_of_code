OCCUPIED = '#'
EMPTY = 'L'
FLOOR = '.'


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_area():
    return [list(line) for line in get_lines()]


def get_neighbour(sitting_area, middle_x, middle_y):
    height = len(sitting_area)
    width = len(sitting_area[0])
    potential_neighbours = [(middle_x + dx, middle_y + dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]
    return list(filter(
        lambda n: 0 <= n[0] < width and 0 <= n[1] < height,
        potential_neighbours
    ))


def count_occupied_neighbours(sitting_area, middle_x, middle_y):
    neighbours = get_neighbour(sitting_area, middle_x, middle_y)

    return sum([sitting_area[y][x] == OCCUPIED for x, y in neighbours])


def get_next(sitting_area):
    next_area = [row[:] for row in sitting_area]

    for y, row in enumerate(sitting_area):
        for x, cell in enumerate(row):
            if cell == FLOOR:
                continue

            occupied_neighbours_count = count_occupied_neighbours(sitting_area, x, y)

            if cell == EMPTY and occupied_neighbours_count == 0:
                next_area[y][x] = OCCUPIED

            if cell == OCCUPIED and occupied_neighbours_count >= 4:
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

    while sitting_area != previous_sitting_area:
        previous_sitting_area = sitting_area
        sitting_area = get_next(sitting_area)

    result = count_seats(sitting_area)
    print(result)
