def shape_points(shape):
    return ord(shape) - ord('X') + 1

def outcome_points(opponent_shape, my_shape):
    opponent_normalised = ord(opponent_shape) - ord('A')
    me_normalised = ord(my_shape) - ord('X')
    result = (me_normalised - opponent_normalised) % 3

    return [3, 6, 0][result]

result = 0
for line in open('input.txt', 'r', encoding='utf-8'):
    line = line.rstrip()
    opponent, me = line.split()
    result += shape_points(me) + outcome_points(opponent, me)


print(result)
