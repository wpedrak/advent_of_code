import itertools

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def find_galaxies(sky: list[str]) -> list[tuple[int, int]]:
    galaxies = []
    for y, row in enumerate(sky):
        for x, symbol in enumerate(row):
            if symbol != '#':
                continue
            galaxies.append((x, y))

    return galaxies

def dist(g1: tuple[int, int], g2: tuple[int, int]) -> int:
    return abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])

sky = get_lines()
galaxies = find_galaxies(sky)
expanded_rows = set(range(len(sky))) - {g[1] for g in galaxies}
expanded_columns = set(range(len(sky[0]))) - {g[0] for g in galaxies}
dist = sum(dist(g1, g2) for g1, g2 in itertools.combinations(galaxies, 2))

for y in expanded_rows:
    dist += sum(g[1] < y for g in galaxies) * sum(g[1] > y for g in galaxies) * 999_999
for x in expanded_columns:
    dist += sum(g[0] < x for g in galaxies) * sum(g[0] > x for g in galaxies) * 999_999

print(dist)
