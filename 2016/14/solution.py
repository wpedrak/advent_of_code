class Raindeer:
    def __init__(self, speed, fly_time, rest_time):
        self.speed = speed
        self.fly_time = fly_time
        self.rest_time = rest_time

    def distance(self, time):
        cycle_time = self.fly_time + self.rest_time
        full_cycles = time // cycle_time
        fly_in_last_cycle = min(self.fly_time, time % cycle_time)
        fly_time = full_cycles * self.fly_time + fly_in_last_cycle
        return fly_time * self.speed


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


max_dist = 0
time = 2503
for raindeer in get_raindeers():
    dist = raindeer.distance(time)
    max_dist = max(dist, max_dist)

print(max_dist)
