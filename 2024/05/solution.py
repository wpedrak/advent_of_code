def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_rules() -> list[tuple[int, int]]:
    lines = read_lines()    
    return [tuple(map(int, l.split('|'))) for l in lines[:lines.index('')]]

def read_updates() -> list[list[int]]:
    lines = read_lines()    
    return [list(map(int, l.split(','))) for l in lines[lines.index('')+1:]]

def is_valid(rules: list[tuple[int, int]], update: list[int]) -> bool:
    update_dict = {value: idx for idx, value in enumerate(update)}
    return all(update_dict[before] < update_dict[after] 
               for before, after in rules 
               if before in update_dict 
               if after in update_dict)

def run() -> None:
    rules = read_rules()
    updates = read_updates()

    result = sum(u[len(u)//2] for u in updates if is_valid(rules, u))

    print(result)

run()
