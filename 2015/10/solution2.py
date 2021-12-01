def look_and_say(sequence):
    current_letter = sequence[0]
    slice_size = 0

    result = []

    for letter in sequence:
        if current_letter == letter:
            slice_size += 1
            continue

        result.append(str(slice_size))
        result.append(current_letter)
        slice_size = 1
        current_letter = letter

    result.append(str(slice_size))
    result.append(current_letter)

    return ''.join(result)


sequence = '1113222113'
rounds = 50
for _ in range(rounds):
    sequence = look_and_say(sequence)

print(len(sequence))
