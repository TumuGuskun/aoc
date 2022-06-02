from collections import defaultdict
from itertools import product
from pprint import pprint

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        shop = defaultdict(list)
        boss_stats = {
            'hp': 104,
            'damage': 8,
            'armor': 1
        }
        category = ''
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            if line:
                if line.startswith('Weapons') or line.startswith('Armor') or line.startswith('Rings'):
                    category = line.split(':')[0]
                else:
                    equipment, cost, damage, armor = line.split()
                    shop[category].append({'cost': int(cost), 'damage': int(damage), 'armor': int(armor)})

    shop['Armor'].append({'cost': 0, 'damage': 0, 'armor': 0})
    num_rings = len(shop['Rings'])
    for i, ring in enumerate(shop['Rings']):
        for j in range(i + 1, num_rings):
            new_cost = ring['cost'] + shop['Rings'][j]['cost']
            new_dam = ring['damage'] + shop['Rings'][j]['damage']
            new_arm = ring['armor'] + shop['Rings'][j]['armor']
            shop['Rings'].append({'cost': new_cost, 'damage': new_dam, 'armor': new_arm})
    shop['Rings'].append({'cost': 0, 'damage': 0, 'armor': 0})
    return shop, boss_stats


def play(player_stats, boss_stats):
    while True:
        boss_stats['hp'] -= max(player_stats['damage'] - boss_stats['armor'], 1)
        player_stats['hp'] -= max(boss_stats['damage'] - player_stats['armor'], 1)
        if boss_stats['hp'] <= 0:
            return True
        elif player_stats['hp'] <= 0:
            return False


@timed
def part1(shop, boss_stats):
    min_gold = float('inf')
    for weapon, armor, ring in product(shop['Weapons'], shop['Armor'], shop['Rings']):
        player_stats = {
            'hp': 100,
            'damage': weapon['damage'] + ring['damage'],
            'armor': armor['armor'] + ring['armor']
        }
        if play(player_stats, boss_stats.copy()):
            min_gold = min(min_gold, weapon['cost'] + armor['cost'] + ring['cost'])
    print(min_gold)


@timed
def part2(shop, boss_stats):
    max_gold = 0
    for weapon, armor, ring in product(shop['Weapons'], shop['Armor'], shop['Rings']):
        player_stats = {
            'hp': 100,
            'damage': weapon['damage'] + ring['damage'],
            'armor': armor['armor'] + ring['armor']
        }
        if not play(player_stats, boss_stats.copy()):
            max_gold = max(max_gold, weapon['cost'] + armor['cost'] + ring['cost'])
    print(max_gold)


if __name__ == '__main__':
    stat_list, boss = read()
    part1(stat_list, boss)
    part2(stat_list, boss)
