STEPS_BEFORE_INSERT = 377

buffer = [0]
current_position = 0

for number_to_be_inserted in range(1, 2017 + 1):
    insert_position = (current_position + STEPS_BEFORE_INSERT) % len(buffer) + 1
    buffer.insert(insert_position, number_to_be_inserted)
    current_position = buffer.index(number_to_be_inserted)

print(buffer[current_position + 1])
