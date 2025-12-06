Point = tuple[int, int]

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def is_accessible(papers: set[Point], paper: Point) -> bool:
    x, y = paper
    return sum((x+dx, y+dy) in papers for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)) < 4

def remove(papers: set[Point]) -> tuple[set[Point], int]:
    return {p for p in papers if not is_accessible(papers, p)}, sum(is_accessible(papers, p) for p in papers)

papers: set[Point] = set()

for y, row in enumerate(read_lines()):
    for x, item in enumerate(row):
        if item == '@':
            papers.add((x, y))

new_papers: set[Point] = set()
accessible = 0
while True:
    papers, removed_count = remove(papers)
    print(removed_count)
    accessible += removed_count
    if not removed_count:
        break

print(accessible)
