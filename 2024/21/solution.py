class Mover:
    def cost(self, sequence: str) -> int:
        return sum(self.cost_single(s, t) for s, t in zip('A' + sequence, sequence))
    
    def cost_single(self, source: str, target: str) -> int:
        raise Exception('not implemented')

class NumpadRobot(Mover):
    def __init__(self, provider: Mover):
        self.mover = provider

class DirectpadRobot(Mover):
    def __init__(self, provider: Mover):
        self.mover = provider

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
    codes = read_lines()[:1]
    human = Human()
    cold_robot = DirectpadRobot(human)
    radiation_robot = DirectpadRobot(cold_robot)
    numpad_robot = NumpadRobot(radiation_robot)

    print(radiation_robot.cost('<A^A>^^AvvvA'))

    # result = sum(numpad_robot.cost(c) * int(c[:-1]) for c in codes)

run()
