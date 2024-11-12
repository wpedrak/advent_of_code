def read_lines(filename='input.txt') -> list[str]:
    return [line.rstrip() for line in open(filename, 'r', encoding='utf-8')]

def read_plots() -> list[str]:
    lines = read_lines()
    plots = []
    for line in lines:
        plots.append('#' + line + '#')
    width = len(lines[0])
    return ['#' * width] + plots + ['#' * width] 

def find_starting_plot(plots: list[str]) -> tuple[int, int]:
    for y, row in enumerate(plots):
        try:
            x = row.index('S')
        except:
            continue
        return x, y
    
    raise Exception(':<')

def run() -> None:
    plots = read_plots()
    start_position = find_starting_plot(plots)
    reached = {start_position}
    deltas = [(1,0), (-1,0), (0,1), (0, -1)]

    for _ in range(64):
        reached = {(x+dx, y+dy) for x, y in reached for dx, dy in deltas if plots[y+dy][x+dx] != '#'}

    print(len(reached))

run()
