import functools
import itertools
import numpy as np

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r')]

def get_scaners_readouts() -> list:
    scaners = []
    current_readout = []

    for line in get_lines():
        if line.startswith('---'):
            continue
        if line == '':
            scaners.append(current_readout)
            current_readout = []
            continue

        point = np.array([[int(x)] for x in line.split(',')])
        current_readout.append(point)

    if current_readout:
        scaners.append(current_readout)

    return scaners

def get_rotation_matrices() -> list:
    x_rot = np.array([
        [1, 0,  0],
        [0, 0, -1],
        [0, 1,  0],
    ])
    y_rot = np.array([
        [ 0, 0, 1],
        [ 0, 1, 0],
        [-1, 0, 0],
    ])
    z_rot = np.array([
        [0, -1, 0],
        [1,  0, 0],
        [0,  0, 1]
    ])
    rotations = []
    for xt, yt, zt in itertools.product(range(1, 5), repeat=3):
        rotation = arr_pow(xt, x_rot) @ arr_pow(yt, y_rot) @ arr_pow(zt, z_rot)
        rotations.append(rotation)


    return np.unique(np.array(rotations), axis=0).tolist()

def arr_pow(times: int, arr):
    if times == 1:
        return arr
    return np.linalg.multi_dot([arr for _ in range(times)])


def count_overlaps(rotations: list, readouts1: list, readouts2: list) -> tuple[int, np.ndarray, np.ndarray]:
    counts = [(*count_overlaps_with_rotation(r, readouts1, readouts2), r) for r in rotations]
    return max(counts, key=lambda x: x[0])

def count_overlaps_with_rotation(rotation, readouts1: list, readouts2: list) -> tuple[int, np.ndarray]:
    rotated_readouts2 = [rotation @ v for v in readouts2]
    a = [
        (count_overlaps_with_fixed_points(v1, v2, readouts1, rotated_readouts2), v1 - v2)
        for v1 in readouts1 
        for v2 in rotated_readouts2
    ]
    return max(
        a, key=lambda x: x[0]
    )

def count_overlaps_with_fixed_points(p1: np.ndarray, p2: np.ndarray, readouts1: list[np.ndarray], readouts2: list[np.ndarray]) -> int:
    shift = p1 - p2
    shifted_readouts2 = [r + shift for r in readouts2]
    all_readouts = readouts1 + shifted_readouts2
    unique_redouts = np.unique(np.array(all_readouts), axis=0)
    return len(all_readouts) - unique_redouts.shape[0]

def manhatan(v1, v2) -> int:
    return np.sum(np.abs(v1 - v2))


scaner_readouts = get_scaners_readouts()
scaners = [None for _ in scaner_readouts]
scaners[0] = np.array([0, 0, 0]).reshape((3, 1))
rotations = get_rotation_matrices()

to_visit = [0]
visited = set()
iterations_to_do = len(scaner_readouts)*(len(scaner_readouts)-1) // 2
padding = len(str(iterations_to_do))
iteration = 0

while to_visit:
    scaner1 = to_visit.pop()
    if scaner1 in visited:
        continue
    visited.add(scaner1)

    for scaner2 in set(range(len(scaner_readouts))) - visited:
        readouts1 = scaner_readouts[scaner1]
        readouts2 = scaner_readouts[scaner2]

        overlap_count, shift, rotation = count_overlaps(rotations, readouts1, readouts2)
        iteration += 1
        print(f'{iteration:{padding}d}/{iterations_to_do:{padding}d}')
        if overlap_count < 12:
            continue

        rebased_readouts2 = [rotation @ v + shift for v in readouts2]
        scaner_readouts[scaner2] = rebased_readouts2
        scaners[scaner2] = shift
        to_visit.append(scaner2)

print(max(
    manhatan(s1, s2)
    for s1 in scaners
    for s2 in scaners
))
