#!/usr/bin/env python3
"""Solve Day 22/Part 1 of the AdventOfCode

"""

import enum

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

effects = [
    Effect(EffectType.Recharge, 5, 229),
    Effect(EffectType.Poison, 6, 173),
    Effect(EffectType.Shield, 6, 113),
    Effect(EffectType.Drain, 0, 73),
    Effect(EffectType.MagicMissile, 0, 53),
]

def simulate_all_games(boss, player, players_turn=True, current_effects=None,
                       used_spells=None):
    if current_effects is None:
        current_effects = []

    if used_spells is None:
        used_spells = []

    for effect in current_effects:
        effect.duration -= 1

        if effect.duration < 0:
            if effect.effect_type == EffectType.Shield:
                player.armor = 0

        else:
            if effect.effect_type == EffectType.Poison:
                boss.hit_points -= 3

            elif effect.effect_type == EffectType.Recharge:
                player.mana += 101

    if boss.hit_points <= 0:
        yield (True, [x.copy() for x in used_spells])
        return

    current_effects = [x for x in current_effects if x.duration > 0]

    if players_turn:
        if all(x.cost > player.mana for x in effects):
            yield (False, [x.copy() for x in used_spells])
            return

        for effect in effects:
            if effect in current_effects:
                continue

            if effect.cost > player.mana:
                continue

            player_copy = player.copy()
            boss_copy = boss.copy()
            current_effects_copy = [x.copy() for x in current_effects]
            used_spells_copy = [x.copy() for x in used_spells]

            current_effects_copy.append(effect.copy())
            used_spells_copy.append(effect.copy())

            player_copy.mana -= effect.cost

            if effect.effect_type == EffectType.MagicMissile:
                boss_copy.hit_points -= 4

            elif effect.effect_type == EffectType.Drain:
                boss_copy.hit_points -= 2
                player_copy.hit_points += 2

            elif effect.effect_type == EffectType.Shield:
                player_copy.armor = 7

            yield from simulate_all_games(
                boss_copy,
                player_copy,
                not players_turn,
                current_effects_copy,
                used_spells_copy,
            )

    else:
        player.hit_points -= max(1, boss.damage - player.armor)

        if player.hit_points <= 0:
            yield (False, [x.copy() for x in used_spells])
            return

        yield from simulate_all_games(
            boss,
            player,
            not players_turn,
            current_effects,
            used_spells,
        )

def main(filename):
    with open(filename, 'r') as f:
        boss_hit_points = int(f.readline().split(': ')[-1])
        boss_damage = int(f.readline().split(': ')[-1])

    player_hit_points = 50
    player_mana = 500

    boss = Boss(boss_hit_points, boss_damage)
    player = Player(player_hit_points, player_mana)

    game_results = simulate_all_games(boss, player)
    winning_spells = (spells for won, spells in game_results if won)
    cost_of_winning_spells = (sum(x.cost for x in spells) for spells in winning_spells)

    lowest_cost_win = min(cost_of_winning_spells)

    print(lowest_cost_win)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
