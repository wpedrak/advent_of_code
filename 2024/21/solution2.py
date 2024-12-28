import functools
import itertools

class Mover:
    def cost(self, sequence: str) -> int:
        return sum(self.cost_single(s, t) for s, t in zip('A' + sequence, sequence))
    
    def cost_single(self, source: str, target: str) -> int:
        raise Exception('not implemented')

class NumpadRobot(Mover):
    def __init__(self, provider: Mover):
        self.mover = provider

    @functools.cache
    def cost_single(self, source: str, target: str) -> int:
        sx, sy = self.coordinates(source)
        tx, ty = self.coordinates(target)

        path = ''
        while sx != tx:
            path += '>' if sx < tx else '<'
            sx += 1 if sx < tx else -1
        
        while sy != ty:
            path += 'v' if sy < ty else '^'
            sy += 1 if sy < ty else -1

        paths = {''.join(p) for p in itertools.permutations(path) if self.is_valid_path(source, target, ''.join(p))}
        return min(self.mover.cost(p + 'A') for p in paths)
        
    def is_valid_path(self, source: str, target: str, path: str) -> bool:
        last_row = {'0': 1, 'A': 2}
        if source in last_row:
            return not path.startswith('<' * last_row[source])

        if target in last_row:
            return not path.endswith('>' * last_row[target])

        return True

    def coordinates(self, key: str) -> tuple[int, int]:
        for y, row in enumerate(['789', '456', '123', 'x0A']):
            try:
                return row.index(key), y
            except:
                pass
        raise Exception(':<')

class DirectpadRobot(Mover):
    def __init__(self, provider: Mover):
        self.mover = provider

    @functools.cache
    def cost_single(self, source: str, target: str) -> int:
        moves = {
            'A': {'^': ['<'], 'v': ['<v', 'v<'], '<': ['<v<', 'v<<'], '>': ['v'], 'A': ['']},
            '<': {'^': ['>^'], 'v': ['>'], '<': [''], '>': ['>>'], 'A': ['>>^', '>^>']},
            '>': {'^': ['^<', '<^'], 'v': ['<'], '<': ['<<'], '>': [''], 'A': ['^']},
            '^': {'v': ['v'], '<': ['v<'], '>': ['>v', 'v>'], '^': [''], 'A': ['>']},
            'v': {'^': ['^'], 'v': [''], '<': ['<'], '>': ['>'], 'A': ['>^', '^>']},
        }[source][target]
        return min(self.mover.cost(m + 'A') for m in moves)
        

class Human(Mover):
    def cost_single(self, source: str, target: str) -> int:
        return 1


def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def run() -> None:
    codes = read_lines()
    human = Human()
    mover = human
    dpadRobot = None
    for _ in range(25):
        dpadRobot = DirectpadRobot(mover)
        mover = dpadRobot
    numpad_robot = NumpadRobot(dpadRobot)

    result = sum(numpad_robot.cost(c) * int(c[:-1]) for c in codes)
    print(result)

run()
