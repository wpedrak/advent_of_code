import re
from collections import namedtuple

Game = namedtuple('Game', ['id', 'draws'])
Draw = namedtuple('Draw', ['r', 'g', 'b'])

def get_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def parse_game(line: str) -> Game:
    id_part, draws_part = line.split(': ')
    game_id = int(id_part.split(' ')[1])
    draws = []
    for draw_part in draws_part.split(';'):
        draws.append(Draw(
            r=find_count('red', draw_part),
            g=find_count('green', draw_part),
            b=find_count('blue', draw_part)
        ))
    return Game(id=game_id, draws=draws)

def find_count(color: str, text: str) -> int:
    match = re.search(r'(\d+) ' + color, text)
    if not match:
        return 0
    return int(match[1])

result = 0
for line in get_lines():
    game = parse_game(line)
    r = max(d.r for d in game.draws)
    g = max(d.g for d in game.draws)
    b = max(d.b for d in game.draws)
    result += r * g * b

print(result)
