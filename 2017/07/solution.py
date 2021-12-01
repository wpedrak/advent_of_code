def get_lines(filename='input'):
    f = open(f'{filename}.txt', 'r')
    return [line.strip() for line in f.readlines()]

def parse_tower(lines):
    return [parse_level(line) for line in lines]

def parse_level(line):
    splited = line.split()
    name = splited[0]
    weight = int(splited[1][1:-1])
    arrow_split = line.split(' -> ')
    next_programs = arrow_split[1].split(', ') if len(arrow_split) > 1 else []

    return name, weight, next_programs

lines = get_lines()
tower = parse_tower(lines)

bot = set()
top = set()

for bot_prog, _, top_progs in tower:
    bot.add(bot_prog)
    top |= set(top_progs)

print(bot - top)
