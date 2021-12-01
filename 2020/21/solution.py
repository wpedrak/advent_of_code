from collections import defaultdict


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


def get_products():
    return [parse_product(line) for line in get_lines()]


def parse_product(line):
    contains_text = ' (contains '
    contains_idx = line.index(contains_text)
    ingredients = line[:contains_idx].split()
    allergens = line[contains_idx + len(contains_text):].split(', ')
    allergens[-1] = allergens[-1][:-1]
    return set(ingredients), set(allergens)


def get_ingredient_sets_by_allergen(products):
    result = defaultdict(lambda: [])

    for ingredients, allergens in products:
        for allergen in allergens:
            result[allergen].append(ingredients)

    return result


def get_possible_ingredients(ingredient_sets):
    if not ingredient_sets:
        raise Exception('no options for this allergen')

    current_result = next(iter(ingredient_sets))
    for ingredient_set in ingredient_sets:
        current_result = current_result & ingredient_set

    return current_result


def remove_from_all_sets(ingredient_sets, ingredient):
    for ingredient_set in ingredient_sets:
        ingredient_set -= {ingredient}


if __name__ == '__main__':
    products = get_products()
    not_mapped_allergens = {allergen for _, allergens in products for allergen in allergens}
    all_ingredient_sets = [ingredient_set for ingredient_set, _ in products]

    ingredient_sets_by_allergen = get_ingredient_sets_by_allergen(products)

    allergen_to_ingredient_mapping = {}

    while not_mapped_allergens:
        for allergen in list(not_mapped_allergens):
            ingredient_sets = ingredient_sets_by_allergen[allergen]
            possible_ingredients = get_possible_ingredients(ingredient_sets)
            if len(possible_ingredients) > 1:
                continue

            ingredient = next(iter(possible_ingredients))
            allergen_to_ingredient_mapping[allergen] = ingredient
            not_mapped_allergens.remove(allergen)
            remove_from_all_sets(all_ingredient_sets, ingredient)

    result = sum(map(len, all_ingredient_sets))
    print(result)
