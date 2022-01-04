class Dice():
    def __init__(self) -> None:
        self.value = 1
        self.__roll_cnt = 0

    def roll(self) -> int:
        self.__roll_cnt += 1
        value = self.value
        self.value = (value % 100) + 1
        return value

    def roll_cnt(self) -> int:
        return self.__roll_cnt

positions = [10, 7]

scores = [0, 0]

player = 0
dice = Dice()

while scores[0] < 1000 and scores[1] < 1000:
    move = sum(dice.roll() for _ in range(3)) % 10
    positions[player] = (positions[player] + move - 1) % 10 + 1
    scores[player] += positions[player]
    player = 1 - player

print(min(scores) * dice.roll_cnt())
