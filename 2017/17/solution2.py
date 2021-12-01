STEPS_BEFORE_INSERT = 377

buffer_length = 1
current_position = 0


for number_to_be_inserted in range(1, 50000000 + 1):
    if number_to_be_inserted % 1000000 == 0:
        print(f'{number_to_be_inserted // 1000000}/50')
    insert_position = (current_position + STEPS_BEFORE_INSERT) % buffer_length + 1
    buffer_length += 1
    current_position = insert_position
    if current_position == 1:
        print(number_to_be_inserted)
