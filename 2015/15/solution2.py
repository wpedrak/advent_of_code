import itertools
import functools


class Ingredient:
    def __init__(self, capacity, durability, flavor, texture, calories):
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def to_array(self):
        return [
            self.capacity,
            self.durability,
            self.flavor,
            self.texture,
            self.calories
        ]

    def __mul__(self, times):
        multiplied = [times * x for x in self.to_array()]
        return Ingredient(*multiplied)

    def __add__(self, ingredient):
        self_array = self.to_array()
        ingredient_array = ingredient.to_array()
        added = [(self_array[idx] + ingredient_array[idx]) for idx in range(len(self_array))]
        return Ingredient(*added)

    def score(self):
        without_negatives = [max(0, x) for x in self.to_array()]
        return functools.reduce(
            lambda x, y: x * y,
            without_negatives[:-1]
        )


def get_lines(filename='15/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_ingredients():
    return [parse_ingredient(line) for line in get_lines()]


def parse_ingredient(line):
    splited = line.split()
    capacity = int(splited[2][:-1])
    durability = int(splited[4][:-1])
    flavor = int(splited[6][:-1])
    texture = int(splited[8][:-1])
    calories = int(splited[-1])

    return Ingredient(capacity, durability, flavor, texture, calories)


def get_all_splits(number, number_of_splits):
    splits = []

    for thresholds in itertools.combinations_with_replacement(range(number), number_of_splits):
        thresholds = thresholds + (number,)
        current_split = [thresholds[idx+1] - thresholds[idx] for idx in range(len(thresholds) - 1)]
        splits.append(current_split)

    return splits


ingredients = get_ingredients()
room = 100
current_max = 0

for number_split in get_all_splits(room, len(ingredients)):
    quantitied_ingredients = list(map(
        lambda p: p[0] * p[1],
        zip(ingredients, number_split)
    ))
    bowl = quantitied_ingredients[0]
    for ingredient in quantitied_ingredients[1:]:
        bowl += ingredient

    current_max = max(current_max, bowl.score())

print(current_max)
