from copy import deepcopy

class Number:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.top = None
        self.val = None

    @staticmethod
    def from_str(repr: str, top=None):
        number = Number()
        number.top = top

        if len(repr) == 1:
            number.val = int(repr)
            return number

        work_str = repr[1:-1]
        balance = 0
        for idx, char in enumerate(work_str):
            balance += char == '['
            balance -= char == ']'

            if char == ',' and balance == 0:
                number.left = Number.from_str(work_str[:idx], top=number)
                number.right = Number.from_str(work_str[idx+1:], top=number)
                return number

        raise Exception('from_str')

    def __add__(self, number):
        res = Number()
        res.left = deepcopy(self)
        res.right = deepcopy(number)
        res.reduce()
        return res

    def reduce(self) -> None:
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break


    def explode(self) -> bool:
        explosions = self.to_explode()
        for explosion in self.to_explode():
            leafs = list(self.left_to_right())
            left_idx = leafs.index(explosion.left)
            right_idx = left_idx + 1
            if left_idx != 0:
                leafs[left_idx-1].val += explosion.left.val
            if right_idx != len(leafs) - 1:
                leafs[right_idx+1].val += explosion.right.val

            explosion.left = None
            explosion.right = None
            explosion.val = 0

        return bool(explosions)

    def to_explode(self, depth=1) -> list:
        if self.val is not None:
            return []
        if depth == 5:
            return [self]

        return self.left.to_explode(depth=depth+1) + self.right.to_explode(depth=depth+1)

    def split(self) -> bool:

        for leaf in self.left_to_right():
            val = leaf.val
            if val < 10:
                continue

            left = Number()
            left.val = val // 2
            right = Number()
            right.val = (val // 2) + (val % 2)
            leaf.val = None
            leaf.left = left
            leaf.right = right
            return True

        return False


    def left_to_right(self):
        if self.val is not None:
            yield self
            return

        for x in self.left.left_to_right():
            yield x
        for x in self.right.left_to_right():
            yield x

    def magnitude(self) -> int:
        if self.val is not None:
            return self.val
        return 3*self.left.magnitude() + 2*self.right.magnitude()

    def __str__(self) -> str:
        if self.val is not None:
            return str(self.val)
        return f'[{self.left},{self.right}]'

    __repr__ = __str__        


def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_numbers() -> list[Number]:
    return [Number.from_str(l) for l in get_lines()]

curr_max = 0

for num1 in get_numbers():
    for num2 in get_numbers():
        if num1 == num2:
            continue
        magnitude = (num1 + num2).magnitude()
        if magnitude > curr_max:
            curr_max = magnitude

print(curr_max)
