#!/usr/bin/env python3
"""Solve Day 22/Part 1 of the AdventOfCode

"""

import enum
import sys
import random

class Boss(object):
    def __init__(self, hit_points, damage):
        self.hit_points = hit_points
        self.damage = damage

    def copy(self):
        return Boss(self.hit_points, self.damage)

class Player(object):
    def __init__(self, hit_points, mana, armor=0):
        self.hit_points = hit_points
        self.mana = mana
        self.armor = armor

    def copy(self):
        return Player(self.hit_points, self.mana, self.armor)

class Effect(object):
    def __init__(self, effect_type, duration, cost):
        self.effect_type = effect_type
        self.duration = duration
        self.cost = cost

    def copy(self):
        return Effect(self.effect_type, self.duration, self.cost)

    def __eq__(self, other):
        return self.effect_type == other.effect_type

EffectType = enum.Enum('EffectType', 'MagicMissile Drain Shield Poison Recharge')

RechargeEffect = Effect(EffectType.Recharge, duration=5, cost=229)
PoisonEffect = Effect(EffectType.Poison, duration=6, cost=173)
ShieldEffect = Effect(EffectType.Shield, duration=6, cost=113)
DrainEffect = Effect(EffectType.Drain, duration=0, cost=73)
MagicMissileEffect = Effect(EffectType.MagicMissile, duration=0, cost=53)

effects = [
    RechargeEffect,
    PoisonEffect,
    ShieldEffect,
#    DrainEffect,
    MagicMissileEffect,
]

DEBUG = True

def find_solution(boss, player, current_spells=None, players_turn=True):
    if current_spells is None:
        current_spells = []

    for effect in current_spells:
        if effect == PoisonEffect:
            boss.hit_points -= 3

        if effect == RechargeEffect:
            player.mana += 101

        effect.duration -= 1

        if effect.duration <= 0:
            if effect == ShieldEffect:
                player.armor = 0

    current_spells = [x for x in current_spells if x.duration > 0]

    if boss.hit_points <= 0:
        return 0

    if players_turn:
        player.hit_points -= 1

    if player.hit_points <= 0:
        return float('inf')

    if players_turn:
        possible = [x for x in effects if x not in current_spells and x.cost <= player.mana]

        if len(possible) == 0:
            return float('inf')

        chosen = random.choice(possible)

        player.mana -= chosen.cost

        if chosen == MagicMissileEffect:
            boss.hit_points -= 4

        elif chosen == DrainEffect:
            boss.hit_points -= 2
            player.hit_points += 2

        elif chosen == ShieldEffect:
            player.armor = 7

        return chosen.cost + find_solution(boss, player, current_spells + [chosen.copy()], False)

    else:
        player.hit_points -= max(1, boss.damage - player.armor)

        return find_solution(boss, player, current_spells, True)



def main(filename):
    with open(filename, 'r') as f:
        boss_hit_points = int(f.readline().split(': ')[-1])
        boss_damage = int(f.readline().split(': ')[-1])

    player_hit_points = 50
    player_mana = 500

    boss = Boss(boss_hit_points, boss_damage)
    player = Player(player_hit_points, player_mana)

    lowest_cost_win = float('inf')
    for _ in range(30 * 1000 * 1000):
        cost = find_solution(boss.copy(), player.copy())
        if cost < lowest_cost_win:
            import sys; print("Cost = {}".format(cost), file=sys.stderr)
            lowest_cost_win = cost

    print(lowest_cost_win)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
