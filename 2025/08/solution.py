Box = tuple[int, int, int]

def read_lines(filename: str = 'input.txt') -> list[str]:
    return [line.rstrip('\n') for line in open(filename, 'r', encoding='utf-8')]

def read_boxes() -> list[Box]:
    boxes: list[Box] = []
    for line in read_lines():
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))

    return boxes

def line_dist(box1: Box, box2: Box) -> float:
    # skipping sqrt as it is monotonic
    return sum((b1-b2)**2 for b1, b2 in zip(box1, box2))

def find(unions: set[frozenset[int]], item: int) -> frozenset[int]:
    for union in unions:
        if item not in union:
            continue

        return union
    
    raise Exception(':<')

def run() -> None:
    boxes = read_boxes()
    dists: list[tuple[float, int, int]] = []
    for idx1, box1 in enumerate(boxes):
        for idx2 in range(idx1+1, len(boxes)):
            box2 = boxes[idx2]
            dists.append((line_dist(box1, box2), idx1, idx2))

    top_dists = sorted(dists)[:1000]
    unions: set[frozenset[int]] = set()
    for _, start, end in top_dists:
        unions.add(frozenset([start]))
        unions.add(frozenset([end]))

    for _, start, end in top_dists:
        u1 = find(unions, start)
        u2 = find(unions, end)
        unions.discard(u1)
        unions.discard(u2)
        unions.add(u1 | u2)

    a, b, c = sorted([len(u) for u in unions], reverse=True)[:3]
    print(a*b*c)

run()
