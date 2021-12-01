def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

maze = [int(jump) for jump in get_lines()]

pointer = 0
time = 0

while 0 <= pointer < len(maze):
    time += 1
    prev_position = pointer
    pointer += maze[pointer]
    maze[prev_position] += 1

print(time)
