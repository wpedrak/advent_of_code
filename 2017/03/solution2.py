def translate_to_xy(position):
    x, y = 0, 0

    x_direction = 1
    y_direction = -1

    current_position = 1
    edge = 1

    while current_position < position:
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


def neighbours_sum(memory, x, y):
    neighbours = [
        (x + dx, y + dy)
        for dx in range(-1, 2)
        for dy in range(-1, 2)
    ]

    return sum([memory[y][x] for x, y in neighbours])

threshold = 361527
size = 100
dx = dy = size // 2
memory = [[0] * size for _ in range(size)]

x, y = 0, 0
memory[y+dy][x+dx] = 1
position = 2

while memory[y+dy][x+dx] < threshold:
    x, y = translate_to_xy(position)
    position += 1
    memory[y+dy][x+dx] = neighbours_sum(memory, x+dx, y+dy)

print(memory[y+dy][x+dx])