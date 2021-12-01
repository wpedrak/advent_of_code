from collections import Counter
from math import sqrt

PIXEL_ON = '#'
PIXELS_PER_MONSTER = 15
MONSTER_LENGTH = 20
MONSTER_HEIGHT = 3
MONSTER_PIXELS_IDX = [
    [18],
    [0, 5, 6, 11, 12, 17, 18, 19],
    [1, 4, 7, 10, 13, 16],
]


def get_tiles():
    tiles_strings = open("input.txt", "r").read().split('\n\n')
    return dict(parse_tile(tile_string) for tile_string in tiles_strings)


def parse_tile(tile_string):
    lines = tile_string.split('\n')
    number = int(lines[0][5:-1])
    return number, lines[1:]


def get_column(array, column_idx):
    column = [row[column_idx] for row in array]
    return ''.join(column)


def normalize_edge(edge):
    reversed_edge = ''.join(reversed(edge))

    return edge if edge < reversed_edge else reversed_edge


def get_edges(tile):
    top = tile[0]
    bot = tile[-1]

    return [top, bot, get_column(tile, 0), get_column(tile, -1)]


def get_normalized_edges(tile):
    all_edges = get_edges(tile)

    return [normalize_edge(edge) for edge in all_edges]


def get_tile_variations(tile):
    tile_rotations = get_tile_rotations(tile)
    tile_flip = get_tile_flip(tile)
    tile_flip_rotations = get_tile_rotations(tile_flip)

    return tile_rotations + tile_flip_rotations


def get_tile_flip(tile):
    return tile[::-1]


def get_tile_rotations(tile):
    tiles = [tile]

    for _ in range(3):
        rotated_tile = rotate_clockwise(tiles[-1])
        tiles.append(rotated_tile)

    return tiles


def rotate_clockwise(array):
    return list(map(
        lambda r: ''.join(r),
        zip(*array[::-1])
    ))


def find_fitting_tile(x, y, not_used_tiles, tiles_board, edge_edges):
    for number, tile in not_used_tiles.items():
        for tile_variation in get_tile_variations(tile):
            if not tile_fits(x, y, tiles_board, edge_edges, tile_variation):
                continue
            return number, tile_variation

    raise Exception('No tile found')


def tile_fits(x, y, tiles_board, edge_edges, tile):
    top_edge, _, left_edge, _ = get_edges(tile)

    if x == 0 and normalize_edge(left_edge) not in edge_edges:
        return False
    elif x > 0:
        left_neighbour = tiles_board[y][x - 1]
        _, _, _, neighbours_right_edge = get_edges(left_neighbour)

        if left_edge != neighbours_right_edge:
            return False

    if y == 0 and normalize_edge(top_edge) not in edge_edges:
        return False
    elif y > 0:
        upper_neighbour = tiles_board[y - 1][x]
        _, neighbours_bot_edge, _, _ = get_edges(upper_neighbour)

        if top_edge != neighbours_bot_edge:
            return False

    return True


def get_all_normalized_edges(tiles):
    all_normalized_edges = []
    for tile in tiles.values():
        all_normalized_edges += get_normalized_edges(tile)
    return all_normalized_edges


def print_tile(tile):
    for row in tile:
        print(''.join(row))

    print()


def inset_tiles(tiles):
    all_normalized_edges = get_all_normalized_edges(tiles)

    edge_occurrences = Counter(all_normalized_edges)
    edge_edges = set(filter(
        lambda e: edge_occurrences[e] == 1,
        all_normalized_edges
    ))
    image_size = int(sqrt(len(tiles)))
    tiles_board = [[None] * image_size for _ in range(image_size)]

    not_used_tiles = tiles.copy()

    for y, row in enumerate(tiles_board):
        for x in range(image_size):
            fitting_tile_number, fitting_tile = find_fitting_tile(x, y, not_used_tiles, tiles_board, edge_edges)
            row[x] = fitting_tile
            del not_used_tiles[fitting_tile_number]

    return tiles_board


def crop_all_tiles(tiles_board):
    return [[crop(tile) for tile in row] for row in tiles_board]


def crop(tile):
    return [row[1:-1] for row in tile[1:-1]]


def merge_tiles(board):
    image = []

    for board_row in board:
        new_image_rows = [[] for _ in range(len(board_row[0]))]

        for tile in board_row:
            for idx, tile_row in enumerate(tile):
                new_image_rows[idx] += tile_row

        image += new_image_rows

    return image


def count_pixels_on(image):
    pixels_on = 0
    for row in image:
        for pixel in row:
            pixels_on += pixel == PIXEL_ON

    return pixels_on


def count_monsters(image):
    monsters_count = 0
    height = len(image)
    width = len(image[0])

    for image_variation in get_tile_variations(image):
        for y in range(height - MONSTER_HEIGHT):
            for x in range(width - MONSTER_LENGTH):
                monsters_count += check_if_monster(image_variation, x, y)

    return monsters_count


def check_if_monster(image_variation, x, y):
    checked_chunk = [
        image_variation[y + dy][x:x + MONSTER_LENGTH]
        for dy in range(MONSTER_HEIGHT)
    ]

    for dy in range(MONSTER_HEIGHT):
        for dx in MONSTER_PIXELS_IDX[dy]:
            if checked_chunk[dy][dx] != PIXEL_ON:
                return False

    return True


if __name__ == '__main__':
    tiles = get_tiles()
    tiles_board = inset_tiles(tiles)
    cropped_tiles_board = crop_all_tiles(tiles_board)
    image = merge_tiles(cropped_tiles_board)
    pixels_on = count_pixels_on(image)
    monsters_count = count_monsters(image)
    result = pixels_on - monsters_count * PIXELS_PER_MONSTER
    print(result)
