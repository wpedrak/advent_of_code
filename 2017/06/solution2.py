def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]


def get_memories():
    lines = get_lines()
    return [int(x) for x in lines[0].split()]


def redistribute(memories):
    max_blocks = max(memories)
    max_idx = memories.index(max_blocks)
    memories[max_idx] = 0
    for block in range(1, max_blocks+1):
        memories[(max_idx + block) % len(memories)] +=1


memories = get_memories()
visited = set()
visited_list = []

while tuple(memories) not in visited:
    tupled_memories = tuple(memories)
    visited.add(tupled_memories)
    visited_list.append(tupled_memories)
    redistribute(memories)

first_occurence = visited_list.index(tuple(memories))
print(len(visited) - first_occurence)