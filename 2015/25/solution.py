def grid_to_seq(row, column):
    diagonal_sum = row + column
    return first_in_diagonal(diagonal_sum) + column - 1


def first_in_diagonal(row):
    return sum(range(row-1)) + 1


def next_code(code):
    return (code * 252533) % 33554393


row = 3010
column = 3019
seq_number = grid_to_seq(row, column)
code = 20151125

for number in range(seq_number - 1):
    if number % 10000 == 0:
        print(f'{number//10000}/{seq_number//10000}')
    code = next_code(code)

print(code)

# 9446911 too high