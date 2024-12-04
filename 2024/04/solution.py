import numpy as np

def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def count_xmas_rows(array):
    cnt = 0
    for row in array:
        row_str = ''.join(row)
        cnt += row_str.count('XMAS')
        cnt += row_str.count('SAMX')

    return cnt

def get_diagonals(array):
    return [np.diag(array, k=i) for i in range(-len(array) + 1, len(array))]

def run() -> None:
    arr = np.array([list(l) for l in read_lines()])
    result = 0

    # rows
    result += count_xmas_rows(arr)
    # columns
    arr = np.rot90(arr)
    result += count_xmas_rows(arr)
    # / diagonals
    result += count_xmas_rows(get_diagonals(arr))
    # \ diagonals
    arr = np.rot90(arr)
    result += count_xmas_rows(get_diagonals(arr))
    
    print(result)

run()
