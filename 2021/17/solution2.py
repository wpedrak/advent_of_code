def hits(velocity, x_range, y_range):
    x, y = velocity
    v_x, v_y = velocity
    x_from, x_to = x_range
    y_from, y_to = y_range
    
    while x < x_from or y > y_to:
        v_x = max(0, v_x-1)
        v_y -= 1
        x += v_x
        y += v_y

    return x_from <= x <= x_to and y_from <= y <= y_to

x_range = (138, 184)
x_from, x_to = x_range
y_range = (-125, -71)
y_from, y_to = y_range

target_hits = []

for x in range(17, x_to+1): # 17+16+...+2+1 = 136 < x_from
    for y in range(y_from, (-y_from)+1):
        velocity = (x, y)
        if not hits(velocity, x_range, y_range):
            continue
        target_hits.append(velocity)

print(len(target_hits))
