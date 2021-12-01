def translate_to_xy(position):
    x, y = 0, 0

    x_direction = 1
    y_direction = -1

    current_position = 1
    edge = 1

    while current_position < position:
        # print(current_position, edge)
        x += edge * x_direction
        x_direction *= -1

        current_position += edge

        if current_position >= position:
            diff = current_position - position
            return x + x_direction * diff, y

        y += edge * y_direction
        y_direction *= -1

        current_position += edge
        edge += 1

    diff = current_position - position
    return x, y + y_direction * diff


position = 361527

x, y = translate_to_xy(position)

print(x, y)
print(abs(x) + abs(y))
