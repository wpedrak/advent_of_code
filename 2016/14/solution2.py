class Raindeer:
    def __init__(self, speed, fly_time, rest_time):
        self.speed = speed
        self.fly_time = fly_time
        self.rest_time = rest_time
        self.points = 0

    def distance(self, time):
        cycle_time = self.fly_time + self.rest_time
        full_cycles = time // cycle_time
        fly_in_last_cycle = min(self.fly_time, time % cycle_time)
        fly_time = full_cycles * self.fly_time + fly_in_last_cycle
        return fly_time * self.speed

    def give_point(self):
        self.points += 1


def get_lines(filename='14/input.txt'):
    file = open(filename, 'r')
    return [line.rstrip('\n') for line in file.readlines()]


def get_raindeers():
    return [parse_raindeer(line) for line in get_lines()]


def parse_raindeer(line):
    splited = line.split()
    speed = int(splited[3])
    fly_time = int(splited[6])
    rest_time = int(splited[-2])

    return Raindeer(speed, fly_time, rest_time)


time_limit = 2503
raindeers = get_raindeers()

for time in range(1, time_limit + 1):
    distances = [r.distance(time) for r in raindeers]
    max_dist = max(distances)
    fastest_raindeers = filter(
        lambda r: r.distance(time) == max_dist,
        raindeers
    )
    for raindeer in fastest_raindeers:
        raindeer.give_point()

result = max(raindeers, key=lambda r: r.points).points

print(result)
