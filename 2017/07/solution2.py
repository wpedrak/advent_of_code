from collections import defaultdict


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


def get_bot(tower):
    bot = set()
    top = set()

    for bot_prog, _, top_progs in tower:
        bot.add(bot_prog)
        top |= set(top_progs)

    return list(bot - top)[0]


def fill_weights(weights, edges, single_weight, bot):
    this_level = []
    for new_bot in edges[bot]:
        fill_weights(weights, edges, single_weight, new_bot)
        this_level.append(weights[new_bot])

    weights[bot] = sum(this_level) + single_weight[bot]


lines = get_lines()
tower = parse_tower(lines)
edges = defaultdict(lambda: [])
single_weight = {}

for bot_prog, weight, top_progs in tower:
    edges[bot_prog] = top_progs
    single_weight[bot_prog] = weight

bot = get_bot(tower)

weights = defaultdict(lambda: [])
fill_weights(weights, edges, single_weight, bot)

for top_progs in edges.values():
    disc_weights = [weights[prog] for prog in top_progs]
    if all(map(lambda w: w == disc_weights[0], disc_weights)):
        continue

    print(disc_weights) # simply look at the one with lowest valueas here as it is the highest one
    print([single_weight[prog] for prog in top_progs])
    print(list(sorted(disc_weights))[1])
    print(max(disc_weights) - min(disc_weights))