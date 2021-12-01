starting_sequence = [14, 1, 17, 0, 3, 20]

last_occurrences = {number: idx + 1 for idx, number in enumerate(starting_sequence[:-1])}

current_number = starting_sequence[-1]
rounds = 30000000

for round_number in range(len(starting_sequence) + 1, rounds + 1):
    if not round_number % 100000:
        print(f'{round_number // 100000}/{rounds // 100000}')

    if current_number not in last_occurrences:
        last_occurrences[current_number] = round_number - 1
        current_number = 0

        continue

    last_occurrence = last_occurrences[current_number]
    last_occurrences[current_number] = round_number - 1
    current_number = round_number - 1 - last_occurrence


print(current_number)
