import itertools
import functools


def split_presents(presents):
    presents = set(presents)
    desired_weight = sum(presents) // 4
    for size in range(len(presents) // 4):
        all_fronts = []
        for items in itertools.combinations(presents, size):
            if sum(items) == desired_weight:
                all_fronts.append(set(items))

        print(f'Found {len(all_fronts)} fronts of size {size}')
        if not all_fronts:
            continue

        solutions = []

        for idx, front in enumerate(all_fronts):
            print(f'Checked {idx}/{len(all_fronts)}')
            if can_split(presents - front):
                solutions.append(front)

        print(f'{len(solutions)} of them are possible to archieve')

        if not solutions:
            continue

        return min(quantum_entanglement(front) for front in solutions)

    raise Exception('Impossible split')


def can_split(presents):
    desired_weight = sum(presents) // 3
    for size in range(len(presents) // 3):
        for items in itertools.combinations(presents, size):
            if sum(items) == desired_weight:
                for size2 in range((len(presents) - size) // 2):
                    for items2 in itertools.combinations(presents - set(items), size2):
                        if sum(items) == desired_weight:
                            return True

    return False


def quantum_entanglement(presents):
    return functools.reduce(
        lambda x, y: x * y,
        presents
    )


presents = [1, 2, 3, 7, 11, 13, 17, 19, 23, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
result = split_presents(presents)

print(result)
