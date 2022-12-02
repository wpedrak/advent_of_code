def shape_points(opponent_shape, outcome):
    opponent_normalised = ord(opponent_shape) - ord('A')
    outcome_normalised = ord(outcome) - ord('X') - 1

    me_normalised = (opponent_normalised + outcome_normalised) % 3
    return me_normalised + 1

def outcome_points(outcome):
    result = ord(outcome) - ord('X')
    return result * 3

result = 0
for line in open('input.txt', 'r', encoding='utf-8'):
    line = line.rstrip()
    opponent, outcome = line.split()
    result += shape_points(opponent, outcome) + outcome_points(outcome)


print(result)
