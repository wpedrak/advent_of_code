from collections import Counter


def get_tiles():
    tiles_strings = open("input.txt", "r").read().split('\n\n')
    return [parse_tile(tile_string) for tile_string in tiles_strings]


def parse_tile(tile_string):
    lines = tile_string.split('\n')
    number = int(lines[0][5:-1])
    return number, lines[1:]


def get_column(array, column_idx):
    column = []
    for row_idx, row in enumerate(array):
        column.append(row[column_idx])

    return ''.join(column)


def get_edges(tile):
    top = tile[0]
    bot = tile[-1]

    return [top, bot, get_column(tile, 0), get_column(tile, -1)]


tiles = get_tiles()

possible_edges = []

for number, tile in tiles:
    tile_edges = get_edges(tile)
    possible_tile_edges = tile_edges + [''.join(reversed(edge)) for edge in tile_edges]
    possible_edges += possible_tile_edges

counter = Counter(possible_edges)

result = 1

for number, tile in tiles:
    tile_edges = get_edges(tile)
    not_parried_edges_count = 0
    for edge in tile_edges:
        not_parried_edges_count += counter[edge] == 1

    if not_parried_edges_count == 2:
        result *= number

print(result)
