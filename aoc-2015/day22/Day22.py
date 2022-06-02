from sys import maxsize
from copy import copy, deepcopy
from queue import Queue

from shared.Util import timed


@timed
def read():
    spells = {
        'mm': {
            'cost': 53,
            'damage': 4,
            'heal': 0,
            'effect': None
        },
        'drain': {
            'cost': 73,
            'damage': 2,
            'heal': 2,
            'effect': None
        },
        'shield': {
            'cost': 113,
            'damage': 0,
            'heal': 0,
            'effect': ('shield', {'damage': 0, 'armor': 7, 'mana': 0}, 6)
        },
        'poison': {
            'cost': 173,
            'damage': 0,
            'heal': 0,
            'effect': ('poison', {'damage': 3, 'armor': 0, 'mana': 0}, 6)
        },
        'recharge': {
            'cost': 229,
            'damage': 0,
            'heal': 0,
            'effect': ('recharge', {'damage': 0, 'armor': 0, 'mana': 101}, 5)
        }
    }
    return spells


def take_turn(spell, boss_stats, player_stats):
    player_stats['armor'] += sum(map(lambda e: e[1]['armor'], player_stats['effects']))
    player_stats['mana'] += sum(map(lambda e: e[1]['mana'], player_stats['effects']))

    boss_stats['hp'] -= spell['damage']
    player_stats['mana'] -= spell['cost']
    player_stats['hp'] += spell['heal']

    if spell['effect'] and spell['effect'][0] == 'poison':
        player_stats['effects'].append(copy(spell['effect']))

    boss_stats['hp'] -= sum(map(lambda e: e[1]['damage'], player_stats['effects']))
    player_stats['hp'] -= max(boss_stats['damage'] - player_stats['armor'], 1)

    player_stats['armor'] -= sum(map(lambda e: e[1]['armor'], player_stats['effects']))

    player_stats['effects'] = [(name, gah, inc - 1) for name, gah, inc in player_stats['effects'] if inc > 1]

    return boss_stats, player_stats


@timed
def part1(spells):
    player_stats = {
        'hp': 50,
        'mana': 500,
        'armor': 0,
        'effects': []
    }
    boss_stats = {
        'hp': 58,
        'damage': 9
    }
    queue = Queue()
    queue.put((boss_stats, player_stats, 0))
    min_mana = float('inf')
    while not queue.empty():
        curr_boss, curr_player, curr_cost = queue.get()
        # print(curr_boss, curr_player, curr_cost)
        if curr_boss['hp'] <= 0:
            min_mana = min(min_mana, curr_cost)
        elif player_stats['hp'] <= 0:
            pass
        else:
            for name, spell in spells.items():
                if curr_player['mana'] >= spell['cost'] and name not in [e[0] for e in player_stats['effects']]:
                    new_boss, new_player = take_turn(spell, curr_boss.copy(), deepcopy(curr_player))
                    queue.put((new_boss.copy(), deepcopy(new_player), spell['cost'] + curr_cost))
    print(min_mana)


@timed
def part2(spells):
    # max_gold = 0
    # for weapon, armor, ring in product(shop['Weapons'], shop['Armor'], shop['Rings']):
    #     player_stats = {
    #         'hp': 100,
    #         'mana': 500,
    #         'armor': armor['armor'] + ring['armor']
    #     }
    #     if not play(player_stats, boss_stats.copy()):
    #         max_gold = max(max_gold, weapon['cost'] + armor['cost'] + ring['cost'])
    # print(max_gold)
    pass



# 0=manacost, 1=dmg, 2=hp, 3=armour, 4=mana, 5=turns, 6=index
missile = (53,4,0,0,0,0,0)
drain = (73,2,2,0,0,0,1)
shield = (113,0,0,7,0,6,2)
poison = (173,3,0,0,0,6,3)
recharge = (229,0,0,0,101,5,4)
spells = [missile, drain, shield, poison, recharge]
leastManaUsed = maxsize
partTwo = True


def main():
    sim(58, 50, 500, [], True, 0)
    print(leastManaUsed)


def sim(bossHP, myHP, myMana, activespells, playerTurn, manaUsed):
    bossDmg = 9
    myArmour = 0

    if partTwo and playerTurn:
        myHP -= 1
        if myHP <= 0:
            return False

    newActiveSpells = []
    for activespell in activespells:
        if activespell[5] >= 0: # spell effect applies now
            bossHP -= activespell[1]
            myHP += activespell[2]
            myArmour += activespell[3]
            myMana += activespell[4]

        newActiveSpell = (activespell[0], activespell[1], activespell[2], activespell[3], activespell[4], activespell[5]-1, activespell[6])
        if newActiveSpell[5] > 0: # spell carries over
            newActiveSpells.append(newActiveSpell)

    if bossHP <= 0:
        global leastManaUsed
        if manaUsed < leastManaUsed:
            leastManaUsed = manaUsed
        return True

    if manaUsed >= leastManaUsed:
        return False

    if (playerTurn):
        for i in range(len(spells)):
            spell = spells[i]
            spellAlreadyActive = False
            for j in range(len(newActiveSpells)):
                if newActiveSpells[j][6] == spell[6]:
                    spellAlreadyActive = True
                    break

            spellManaCost = spell[0]
            if spellManaCost <= myMana and not spellAlreadyActive:
                a = deepcopy(newActiveSpells)
                a.append(spell)
                sim(bossHP, myHP, myMana - spellManaCost, a, False, manaUsed+spellManaCost)
    else:
        myHP += myArmour-bossDmg if myArmour-bossDmg < 0 else -1
        if myHP > 0:
            sim(bossHP,myHP,myMana,newActiveSpells, True,manaUsed)


if __name__ == '__main__':
    main()
