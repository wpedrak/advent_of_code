Box = dict[str, tuple[int, int]]

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def get_hash(string: str) -> int:
    current_value = 0
    for char in string:
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value

def remove(box: Box, label: str) -> None:
    if label not in box:
        return 
    position = box[label][0]
    del box[label]
    for key, (p, f) in box.items():
        if p <= position:
            continue
        box[key] = (p-1, f)

def upsert(box: Box, label: str, focal_length: int):
    if label not in box:
        box[label] = (len(box), focal_length)
        return
    position, _ = box[label]
    box[label] = (position, focal_length)


steps = get_lines()[0].split(',')
boxes = [{} for _ in range(256)]
for step in steps:
    if step[-1] == '-':
        label = step[:-1]
        remove(boxes[get_hash(label)], label)
        continue
    
    label, focal_length = step.split('=')
    upsert(boxes[get_hash(label)], label, int(focal_length))

result = 0
for idx, box in enumerate(boxes):
    for position, focal_length in box.values():
        result += (idx+1) * (position+1) * focal_length

print(result)
