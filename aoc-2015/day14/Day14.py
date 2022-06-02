from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    reindeer = {}
    with open(file_name) as input_file:
        for line in input_file.readlines():
            start, end = line.split(' seconds, but then must rest for ')
            name, flight = start.split(' can fly ')
            speed, time = flight.split(' km/s for ')
            rest = end.split(' seconds.')[0]
            reindeer[name] = {'speed': int(speed), 'time': int(time), 'rest': int(rest)}
    return reindeer


def update(distances, reindeers):
    for reindeer, specs in reindeers.items():
        if distances[reindeer]['flying']:
            distances[reindeer]['distance'] += specs['speed']
            distances[reindeer]['time'] += 1
            if distances[reindeer]['time'] == specs['time']:
                distances[reindeer]['flying'] = False
                distances[reindeer]['time'] = 0
        else:
            distances[reindeer]['time'] += 1
            if distances[reindeer]['time'] == specs['rest']:
                distances[reindeer]['flying'] = True
                distances[reindeer]['time'] = 0
    return distances


@timed
def part1(reindeers):
    distances = {reindeer: {'flying': True, 'time': 0, 'distance': 0} for reindeer in reindeers}
    for i in range(2503):
        update(distances, reindeers)
    print(max(distances.values(), key=lambda x: x['distance'])['distance'])


@timed
def part2(reindeers):
    distances = {reindeer: {'flying': True, 'time': 0, 'distance': 0} for reindeer in reindeers}
    scores = defaultdict(int)
    for i in range(2503):
        update(distances, reindeers)
        winner = max(distances.items(), key=lambda x: x[1]['distance'])[0]
        scores[winner] += 1
    print(max(scores.values()))


if __name__ == '__main__':
    reindeer_list = read()
    part1(reindeer_list)
    part2(reindeer_list)
