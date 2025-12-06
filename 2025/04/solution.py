Point = tuple[int, int]

def read_lines(file_name: str = 'input.txt') -> list[str]:
    return [line.rstrip() for line in open(file_name, 'r', encoding='utf-8')]

def is_accessible(papers: set[Point], paper: Point) -> bool:
    x, y = paper
    return sum((x+dx, y+dy) in papers for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)) < 4

papers: set[Point] = set()

for y, row in enumerate(read_lines()):
    for x, item in enumerate(row):
        if item == '@':
            papers.add((x, y))

accessible = 0
for paper in papers:
    accessible += is_accessible(papers, paper)

print(accessible)
